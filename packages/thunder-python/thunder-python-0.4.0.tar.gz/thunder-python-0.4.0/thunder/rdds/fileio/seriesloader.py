"""Provides SeriesLoader object and helpers, used to read Series data from disk or other filesystems.
"""
from collections import namedtuple
import json
from numpy import array, dtype, frombuffer, arange, load, vstack, unravel_index
from scipy.io import loadmat
from cStringIO import StringIO
import struct
import urlparse
import math

from thunder.rdds.fileio.writers import getParallelWriterForPath
from thunder.rdds.imageblocks import ImageBlocks
from thunder.rdds.fileio.readers import getFileReaderForPath, FileNotFoundError, selectByStartAndStopIndices
from thunder.rdds.series import Series
from thunder.utils.common import parseMemoryString


class SeriesLoader(object):
    """Loader object used to instantiate Series data stored in a variety of formats.
    """
    def __init__(self, sparkcontext, minPartitions=None):
        """Initialize a new SeriesLoader object.

        Parameters
        ----------
        sparkcontext: SparkContext
            The pyspark SparkContext object used by the current Thunder environment.

        minPartitions: int
            minimum number of partitions to use when loading data. (Used by fromText, fromMatLocal, and fromNpyLocal)
        """
        self.sc = sparkcontext
        self.minPartitions = minPartitions

    @staticmethod
    def __normalizeDatafilePattern(datapath, ext):
        if ext:
            if not ext.startswith("."):
                # protect (partly) against case where ext happens to *also* be the name
                # of a directory. If your directory is named "something.bin", well, you
                # get what you deserve, I guess.
                ext = "." + ext
            if not datapath.endswith(ext):
                if datapath.endswith("*"):
                    datapath += ext
                elif datapath.endswith("/"):
                    datapath += "*" + ext
                else:
                    datapath += "/*" + ext

        parseresult = urlparse.urlparse(datapath)
        if parseresult.scheme:
            # this appears to already be a fully-qualified URI
            return datapath
        else:
            return "file://" + datapath

    def fromText(self, datafile, nkeys=None, ext="txt"):
        """
        Loads Series data from text files.

        Parameters
        ----------
        datafile : string
            Specifies the file or files to be loaded. Datafile may be either a URI (with scheme specified) or a path
            on the local filesystem.
            If a path is passed (determined by the absence of a scheme component when attempting to parse as a URI),
            and it is not already a wildcard expression and does not end in <ext>, then it will be converted into a
            wildcard pattern by appending '/*.ext'. This conversion can be avoided by passing a "file://" URI.
        """
        datafile = self.__normalizeDatafilePattern(datafile, ext)

        def parse(line, nkeys_):
            vec = [float(x) for x in line.split(' ')]
            ts = array(vec[nkeys_:])
            keys = tuple(int(x) for x in vec[:nkeys_])
            return keys, ts

        lines = self.sc.textFile(datafile, self.minPartitions)
        data = lines.map(lambda x: parse(x, nkeys))

        return Series(data)

    BinaryLoadParameters = namedtuple('BinaryLoadParameters', 'nkeys nvalues keytype valuetype')
    BinaryLoadParameters.__new__.__defaults__ = (None, None, 'int16', 'int16')

    @staticmethod
    def __loadParametersAndDefaults(datafile, conffilename, nkeys, nvalues, keytype, valuetype):
        """Collects parameters to use for binary series loading.

        Priority order is as follows:
        1. parameters specified as keyword arguments;
        2. parameters specified in a conf.json file on the local filesystem;
        3. default parameters

        Returns
        -------
        BinaryLoadParameters instance
        """
        params = SeriesLoader.loadConf(datafile, conffile=conffilename)

        # filter dict to include only recognized field names:
        for k in params.keys():
            if not k in SeriesLoader.BinaryLoadParameters._fields:
                del params[k]
        keywordparams = {'nkeys': nkeys, 'nvalues': nvalues, 'keytype': keytype, 'valuetype': valuetype}
        for k, v in keywordparams.items():
            if not v:
                del keywordparams[k]
        params.update(keywordparams)
        return SeriesLoader.BinaryLoadParameters(**params)

    @staticmethod
    def __checkBinaryParametersAreSpecified(paramsObj):
        """Throws ValueError if any of the field values in the passed namedtuple instance evaluate to False.

        Note this is okay only so long as zero is not a valid parameter value. Hmm.
        """
        missing = []
        for paramname, paramval in paramsObj._asdict().iteritems():
            if not paramval:
                missing.append(paramname)
        if missing:
            raise ValueError("Missing parameters to load binary series files - " +
                             "these must be given either as arguments or in a configuration file: " +
                             str(tuple(missing)))

    def fromBinary(self, datafile, ext='bin', conffilename='conf.json',
                   nkeys=None, nvalues=None, keytype=None, valuetype=None):
        """
        Load a Series object from a directory of binary files.

        Parameters
        ----------

        datafile: string URI or local filesystem path
            Specifies the directory or files to be loaded. May be formatted as a URI string with scheme (e.g. "file://",
            "s3n://". If no scheme is present, will be interpreted as a path on the local filesystem. This path
            must be valid on all workers. Datafile may also refer to a single file, or to a range of files specified
            by a glob-style expression using a single wildcard character '*'.

        """

        paramsObj = self.__loadParametersAndDefaults(datafile, conffilename, nkeys, nvalues, keytype, valuetype)
        self.__checkBinaryParametersAreSpecified(paramsObj)

        datafile = self.__normalizeDatafilePattern(datafile, ext)

        keydtype = dtype(paramsObj.keytype)
        valdtype = dtype(paramsObj.valuetype)

        keysize = paramsObj.nkeys * keydtype.itemsize
        recordsize = keysize + paramsObj.nvalues * valdtype.itemsize

        lines = self.sc.newAPIHadoopFile(datafile, 'thunder.util.io.hadoop.FixedLengthBinaryInputFormat',
                                         'org.apache.hadoop.io.LongWritable',
                                         'org.apache.hadoop.io.BytesWritable',
                                         conf={'recordLength': str(recordsize)})

        data = lines.map(lambda (_, v):
                         (tuple(int(x) for x in frombuffer(buffer(v, 0, keysize), dtype=keydtype)),
                          frombuffer(buffer(v, keysize), dtype=valdtype)))

        return Series(data)

    def _getSeriesBlocksFromStack(self, datapath, dims, ext="stack", blockSize="150M", datatype='int16',
                                  startidx=None, stopidx=None):
        """Create an RDD of <string blocklabel, (int k-tuple indices, array of datatype values)>

        Parameters
        ----------

        datafile: string URI or local filesystem path
            Specifies the directory or files to be loaded. May be formatted as a URI string with scheme (e.g. "file://",
            "s3n://". If no scheme is present, will be interpreted as a path on the local filesystem. This path
            must be valid on all workers. Datafile may also refer to a single file, or to a range of files specified
            by a glob-style expression using a single wildcard character '*'.


        Returns
        ---------
        pair of (RDD, ntimepoints)

        RDD: sequence of keys, values pairs
            (call using flatMap)

        RDD Key: tuple of int
            zero-based indicies of position within original image volume

        RDD Value: numpy array of datatype
            series of values at position across loaded image volumes

        ntimepoints: int
            number of time points in returned series, determined from number of stack files found at datapath

        """

        datapath = self.__normalizeDatafilePattern(datapath, ext)
        blockSize = parseMemoryString(blockSize)
        totaldim = reduce(lambda x_, y_: x_*y_, dims)
        datatype = dtype(datatype)

        reader = getFileReaderForPath(datapath)()
        filenames = reader.list(datapath)
        if not filenames:
            raise IOError("No files found for path '%s'" % datapath)
        filenames = selectByStartAndStopIndices(filenames, startidx, stopidx)

        datasize = totaldim * len(filenames) * datatype.itemsize
        nblocks = max(datasize / blockSize, 1)  # integer division

        if len(dims) >= 3:
            # for 3D stacks, do calculations to ensure that
            # different planes appear in distinct files
            blocksperplane = max(nblocks / dims[-1], 1)

            pixperplane = reduce(lambda x_, y_: x_*y_, dims[:-1])

            # get the greatest number of blocks in a plane (up to as many as requested) that still divide the plane
            # evenly. This will always be at least one.
            kupdated = [x for x in range(1, blocksperplane+1) if not pixperplane % x][-1]
            nblocks = kupdated * dims[-1]
            blockSizePerStack = (totaldim / nblocks) * datatype.itemsize
        else:
            # otherwise just round to make contents divide into nearly even blocks
            blockSizePerStack = int(math.ceil(totaldim / float(nblocks)))
            nblocks = int(math.ceil(totaldim / float(blockSizePerStack)))
            blockSizePerStack *= datatype.itemsize

        filesize = totaldim * datatype.itemsize

        def readblock(blocknum):
            # copy size out from closure; will modify later:
            blockSizePerStack_ = blockSizePerStack
            # get start position for this block
            position = blocknum * blockSizePerStack_

            # adjust if at end of file
            if (position + blockSizePerStack_) > filesize:
                blockSizePerStack_ = int(filesize - position)
            # loop over files, loading one block from each
            bufs = []

            for fname in filenames:
                buf = reader.read(fname, startOffset=position, size=blockSizePerStack_)
                bufs.append(frombuffer(buf, dtype=datatype))

            buf = vstack(bufs).T  # dimensions are now linindex x time (images)
            del bufs

            # append subscript keys based on dimensions
            itemposition = position / datatype.itemsize
            itemblocksize = blockSizePerStack_ / datatype.itemsize
            linindx = arange(itemposition, itemposition + itemblocksize)  # zero-based

            keys = zip(*map(tuple, unravel_index(linindx, dims, order='F')))
            return zip(keys, buf)

        # map over blocks
        return self.sc.parallelize(range(0, nblocks), nblocks).flatMap(lambda bn: readblock(bn)), len(filenames)

    @staticmethod
    def __readMetadataFromFirstPageOfMultiTif(reader, filepath):
        import thunder.rdds.fileio.multitif as multitif

        # read first page of first file to get expected image size
        tiffp = reader.open(filepath)
        tiffparser = multitif.TiffParser(tiffp, debug=False)
        tiffheaders = multitif.TiffData()
        tiffparser.parseFileHeader(destination_tiff=tiffheaders)
        firstifd = tiffparser.parseNextImageFileDirectory(destination_tiff=tiffheaders)
        if not firstifd.isLuminanceImage():
            raise ValueError(("File %s does not appear to be a luminance " % filepath) +
                             "(greyscale or bilevel) TIF image, " +
                             "which are the only types currently supported")

        # keep reading pages until we reach the end of the file, in order to get number of planes:
        while tiffparser.parseNextImageFileDirectory(destination_tiff=tiffheaders):
            pass

        # get dimensions
        dims = (firstifd.getImageWidth(), firstifd.getImageHeight(), len(tiffheaders.ifds))

        # get datatype
        bitspersample = firstifd.getBitsPerSample()
        if not (bitspersample in (8, 16, 32, 64)):
            raise ValueError("Only 8, 16, 32, or 64 bit per pixel TIF images are supported, got %d" % bitspersample)

        sampleformat = firstifd.getSampleFormat()
        if sampleformat == multitif.SAMPLE_FORMAT_UINT:
            dtstr = 'uint'
        elif sampleformat == multitif.SAMPLE_FORMAT_INT:
            dtstr = 'int'
        elif sampleformat == multitif.SAMPLE_FORMAT_FLOAT:
            dtstr = 'float'
        else:
            raise ValueError("Unknown TIF SampleFormat tag value %d, should be 1, 2, or 3 for uint, int, or float"
                             % sampleformat)
        datatype = dtstr+str(bitspersample)

        return dims, datatype

    def _getSeriesBlocksFromMultiTif(self, datapath, ext="tif", blockSize="150M",
                                     startidx=None, stopidx=None):
        import thunder.rdds.fileio.multitif as multitif
        import itertools
        from PIL import Image
        from matplotlib.image import pil_to_array
        import io

        datapath = self.__normalizeDatafilePattern(datapath, ext)
        blockSize = parseMemoryString(blockSize)

        reader = getFileReaderForPath(datapath)()
        filenames = reader.list(datapath)
        if not filenames:
            raise IOError("No files found for path '%s'" % datapath)
        filenames = selectByStartAndStopIndices(filenames, startidx, stopidx)
        ntimepoints = len(filenames)

        dims, datatype = SeriesLoader.__readMetadataFromFirstPageOfMultiTif(reader, filenames[0])
        pixelbytesize = dtype(datatype).itemsize

        # intialize at one block per plane
        bytesperplane = dims[0] * dims[1] * pixelbytesize * ntimepoints
        bytesperblock = bytesperplane
        blocksperplane = 1
        # keep dividing while cutting our size in half still leaves us bigger than the requested size
        # should end up no more than 2x blockSize.
        while bytesperblock >= blockSize * 2:
            bytesperblock /= 2
            blocksperplane *= 2

        blocklen = max((dims[0] * dims[1]) / blocksperplane, 1)  # integer division

        # keys will be planeidx, blockidx:
        keys = list(itertools.product(xrange(dims[2]), xrange(blocksperplane)))

        def readblockfromtif(pidxbidx_):
            planeidx, blockidx = pidxbidx_
            blocks = []
            planeshape = None
            blockstart = None
            blockend = None
            for fname in filenames:
                reader_ = getFileReaderForPath(fname)()
                fp = reader_.open(fname)
                try:
                    tiffparser_ = multitif.TiffParser(fp, debug=False)
                    tiffilebuffer = multitif.packSinglePage(tiffparser_, page_idx=planeidx)
                    pilimg = Image.open(io.BytesIO(tiffilebuffer))
                    ary = pil_to_array(pilimg)
                    del tiffilebuffer, tiffparser_, pilimg
                    if not planeshape:
                        planeshape = ary.shape[:]
                        blockstart = blockidx * blocklen
                        blockend = min(blockstart+blocklen, planeshape[0]*planeshape[1])
                    blocks.append(ary.flatten(order='C')[blockstart:blockend])
                    del ary
                finally:
                    fp.close()

            buf = vstack(blocks).T  # dimensions are now linindex x time (images)
            del blocks

            # append subscript keys based on dimensions
            linindx = arange(blockstart, blockend)  # zero-based

            serieskeys = zip(*map(tuple, unravel_index(linindx, planeshape, order='C')))
            # add plane index to end of keys
            serieskeys = [tuple(list(keys_)[::-1]+[planeidx]) for keys_ in serieskeys]
            return zip(serieskeys, buf)

        # map over blocks
        rdd = self.sc.parallelize(keys, len(keys)).flatMap(readblockfromtif)
        metadata = (dims, ntimepoints, datatype)
        return rdd, metadata

    def fromStack(self, datapath, dims, ext="stack", blockSize="150M", datatype='int16', startidx=None, stopidx=None):
        """Load a Series object directly from binary image stack files.

        Parameters
        ----------

        datapath: string
            Path to data files or directory, specified as either a local filesystem path or in a URI-like format,
            including scheme. A datapath argument may include a single '*' wildcard character in the filename.

        dims: tuple of positive int
            Dimensions of input image data, similar to a numpy 'shape' parameter.

        ext: string, optional, default "stack"
            Extension required on data files to be loaded.

        blocksize: string formatted as e.g. "64M", "512k", "2G", or positive int. optional, default "150M"
            Requested size of Series partitions in bytes (or kilobytes, megabytes, gigabytes).

        datatype: string or numpy dtype. optional, default 'int16'
            Data type of binary stack data to load. datatype should be interpretable as a numpy dtype.

        startidx, stopidx: nonnegative int. optional.
            Indices of the first and last-plus-one data file to load, relative to the sorted filenames matching
            `datapath` and `ext`. Interpreted according to python slice indexing conventions.
        """
        seriesblocks, npointsinseries = self._getSeriesBlocksFromStack(datapath, dims, ext=ext, blockSize=blockSize,
                                                                       datatype=datatype, startidx=startidx,
                                                                       stopidx=stopidx)
        # TODO: initialize index here using npointsinseries?
        return Series(seriesblocks, dims=dims)

    def fromMultipageTif(self, datapath, ext="tif", blockSize="150M",
                         startidx=None, stopidx=None):
        """Load a Series object from multipage tiff files.

        Parameters
        ----------

        datapath: string
            Path to data files or directory, specified as either a local filesystem path or in a URI-like format,
            including scheme. A datapath argument may include a single '*' wildcard character in the filename.

        ext: string, optional, default "tif"
            Extension required on data files to be loaded.

        blocksize: string formatted as e.g. "64M", "512k", "2G", or positive int. optional, default "150M"
            Requested size of Series partitions in bytes (or kilobytes, megabytes, gigabytes).

        startidx, stopidx: nonnegative int. optional.
            Indices of the first and last-plus-one data file to load, relative to the sorted filenames matching
            `datapath` and `ext`. Interpreted according to python slice indexing conventions.
        """
        seriesblocks, metadata = self._getSeriesBlocksFromMultiTif(datapath, ext=ext, blockSize=blockSize,
                                                                   startidx=startidx, stopidx=stopidx)
        dims, npointsinseries, datatype = metadata
        return Series(seriesblocks, dims=dims)

    @staticmethod
    def __saveSeriesRdd(seriesblocks, outputdirname, dims, npointsinseries, datatype, overwrite=False):
        writer = getParallelWriterForPath(outputdirname)(outputdirname, overwrite=overwrite)

        def blockToBinarySeries(kviter):
            label = None
            keypacker = None
            buf = StringIO()
            for seriesKey, series in kviter:
                if keypacker is None:
                    keypacker = struct.Struct('h'*len(seriesKey))
                    label = ImageBlocks.getBinarySeriesNameForKey(seriesKey) + ".bin"
                buf.write(keypacker.pack(*seriesKey))
                buf.write(series.tostring())
            val = buf.getvalue()
            buf.close()
            return [(label, val)]

        seriesblocks.mapPartitions(blockToBinarySeries).foreach(writer.writerFcn)
        writeSeriesConfig(outputdirname, len(dims), npointsinseries, dims=dims, valuetype=datatype,
                          overwrite=overwrite)

    def saveFromStack(self, datapath, outputdirpath, dims, ext="stack", blockSize="150M", datatype='int16',
                      startidx=None, stopidx=None, overwrite=False):
        """Write out data from binary image stack files in the Series data flat binary format.

        Parameters
        ----------
        datapath: string
            Path to data files or directory, specified as either a local filesystem path or in a URI-like format,
            including scheme. A datapath argument may include a single '*' wildcard character in the filename.

        outputdirpath: string
            Path to a directory into which to write Series file output. An outputdir argument may be either a path
            on the local file system or a URI-like format, as in datapath.

        dims: tuple of positive int
            Dimensions of input image data, similar to a numpy 'shape' parameter.

        ext: string, optional, default "stack"
            Extension required on data files to be loaded.

        blocksize: string formatted as e.g. "64M", "512k", "2G", or positive int. optional, default "150M"
            Requested size of Series partitions in bytes (or kilobytes, megabytes, gigabytes).

        datatype: string or numpy dtype. optional, default 'int16'
            Data type of binary stack data to load. datatype should be interpretable as a numpy dtype.

        startidx, stopidx: nonnegative int. optional.
            Indices of the first and last-plus-one data file to load, relative to the sorted filenames matching
            `datapath` and `ext`. Interpreted according to python slice indexing conventions.

        overwrite: boolean, optional, default False
            If true, the directory specified by outputdirpath will first be deleted, along with all its contents, if it
            already exists. If false, a ValueError will be thrown if outputdirpath is found to already exist.

        """
        seriesblocks, npointsinseries = self._getSeriesBlocksFromStack(datapath, dims, ext=ext, blockSize=blockSize,
                                                                       datatype=datatype, startidx=startidx,
                                                                       stopidx=stopidx)
        SeriesLoader.__saveSeriesRdd(seriesblocks, outputdirpath, dims, npointsinseries, datatype, overwrite=overwrite)

    def saveFromMultipageTif(self, datapath, outputdirpath, ext="tif", blockSize="150M",
                             startidx=None, stopidx=None, overwrite=False):
        """Write out data from multipage tif files in the Series data flat binary format.

        Parameters
        ----------
        datapath: string
            Path to data files or directory, specified as either a local filesystem path or in a URI-like format,
            including scheme. A datapath argument may include a single '*' wildcard character in the filename.

        outputdirpath: string
            Path to a directory into which to write Series file output. An outputdir argument may be either a path
            on the local file system or a URI-like format, as in datapath.

        ext: string, optional, default "stack"
            Extension required on data files to be loaded.

        blocksize: string formatted as e.g. "64M", "512k", "2G", or positive int. optional, default "150M"
            Requested size of Series partitions in bytes (or kilobytes, megabytes, gigabytes).

        startidx, stopidx: nonnegative int. optional.
            Indices of the first and last-plus-one data file to load, relative to the sorted filenames matching
            `datapath` and `ext`. Interpreted according to python slice indexing conventions.

        overwrite: boolean, optional, default False
            If true, the directory specified by outputdirpath will first be deleted, along with all its contents, if it
            already exists. If false, a ValueError will be thrown if outputdirpath is found to already exist.

        """
        seriesblocks, metadata = self._getSeriesBlocksFromMultiTif(datapath, ext=ext, blockSize=blockSize,
                                                                   startidx=startidx, stopidx=stopidx)
        dims, npointsinseries, datatype = metadata
        SeriesLoader.__saveSeriesRdd(seriesblocks, outputdirpath, dims, npointsinseries, datatype, overwrite=overwrite)

    def fromMatLocal(self, datafile, varname, keyfile=None):
        """Loads Series data stored in a Matlab .mat file.

        `datafile` must refer to a path visible to all workers, such as on NFS or similar mounted shared filesystem.
        """
        data = loadmat(datafile)[varname]
        if data.ndim > 2:
            raise IOError('Input data must be one or two dimensional')
        if keyfile:
            keys = map(lambda x: tuple(x), loadmat(keyfile)['keys'])
        else:
            keys = arange(0, data.shape[0])

        rdd = Series(self.sc.parallelize(zip(keys, data), self.minPartitions))

        return rdd

    def fromNpyLocal(self, datafile, keyfile=None):
        """Loads Series data stored in the numpy save() .npy format.

        `datafile` must refer to a path visible to all workers, such as on NFS or similar mounted shared filesystem.
        """
        data = load(datafile)
        if data.ndim > 2:
            raise IOError('Input data must be one or two dimensional')
        if keyfile:
            keys = map(lambda x: tuple(x), load(keyfile))
        else:
            keys = arange(0, data.shape[0])

        rdd = Series(self.sc.parallelize(zip(keys, data), self.minPartitions))

        return rdd

    @staticmethod
    def loadConf(datafile, conffile='conf.json'):
        """Returns a dict loaded from a json file.

        Looks for file named `conffile` in same directory as `datafile`

        Returns {} if file not found
        """
        if not conffile:
            return {}

        reader = getFileReaderForPath(datafile)()
        try:
            jsonbuf = reader.read(datafile, filename=conffile)
        except FileNotFoundError:
            return {}

        params = json.loads(jsonbuf)

        if 'format' in params:
            raise Exception("Numerical format of value should be specified as 'valuetype', not 'format'")
        if 'keyformat' in params:
            raise Exception("Numerical format of key should be specified as 'keytype', not 'keyformat'")

        return params


def writeSeriesConfig(outputdirname, nkeys, nvalues, dims=None, keytype='int16', valuetype='int16',
                      confname="conf.json", overwrite=True):
    """Helper function to write out a conf.json file with required information to load Series binary data.
    """
    import json
    from thunder.rdds.fileio.writers import getFileWriterForPath

    filewriterclass = getFileWriterForPath(outputdirname)
    # write configuration file
    conf = {'input': outputdirname,
            'nkeys': nkeys, 'nvalues': nvalues,
            'valuetype': str(valuetype), 'keytype': str(keytype)}
    if dims:
        conf["dims"] = dims

    confwriter = filewriterclass(outputdirname, confname, overwrite=overwrite)
    confwriter.writeFile(json.dumps(conf, indent=2))

    # touch "SUCCESS" file as final action
    successwriter = filewriterclass(outputdirname, "SUCCESS", overwrite=overwrite)
    successwriter.writeFile('')
