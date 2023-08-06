"""
Class for performing Singular Value Decomposition
"""

from numpy import zeros, shape

from thunder.rdds.series import Series
from thunder.rdds.matrices import RowMatrix


class SVD(object):
    """
    Singular value decomposiiton on a distributed matrix.

    Parameters
    ----------
    k : int, optional, default = 3
        Number of singular vectors to estimate

    method : string, optional, default "direct"
        Whether to use a direct or iterative method

    maxiter : int, optional, default = 20
        Maximum number of iterations if using an iterative method

    tol : float, optional, default = 0.00001
        Tolerance for convergence of iterative algorithm

    Attributes
    ----------
    `u` : RowMatrix, nrows, each of shape (k,)
        Left singular vectors

    `s` : array, shape(nrows,)
        Singular values

    `v` : array, shape (k, ncols)
        Right singular vectors
    """
    def __init__(self, k=3, method="direct", maxiter=20, tol=0.00001):
        self.k = k
        self.method = method
        self.maxiter = maxiter
        self.tol = tol

    def calc(self, mat):
        """
        Calcuate singular vectors

        Parameters
        ----------
        mat :  Series or a subclass (e.g. RowMatrix)
            Matrix to compute singular vectors from

        Returns
        ----------
        self : returns an instance of self.
        """

        from numpy import random, sum, argsort, dot, outer, sqrt
        from scipy.linalg import inv, orth
        from numpy.linalg import eigh

        if not (isinstance(mat, Series)):
            raise Exception('Input must be Series or a subclass (e.g. RowMatrix)')

        if not (isinstance(mat, RowMatrix)):
            mat = mat.toRowMatrix()

        if self.method == "direct":

            # get the normalized gramian matrix
            cov = mat.gramian() / mat.nrows

            # do a local eigendecomposition
            eigw, eigv = eigh(cov)
            inds = argsort(eigw)[::-1]
            s = sqrt(eigw[inds[0:self.k]]) * sqrt(mat.nrows)
            v = eigv[:, inds[0:self.k]].T

            # project back into data, normalize by singular values
            u = mat.times(v.T / s)

            self.u = u
            self.s = s
            self.v = v

        if self.method == "em":

            # initialize random matrix
            c = random.rand(self.k, mat.ncols)
            iter = 0
            error = 100

            # define an accumulator
            from pyspark.accumulators import AccumulatorParam

            class MatrixAccumulatorParam(AccumulatorParam):
                def zero(self, value):
                    return zeros(shape(value))

                def addInPlace(self, val1, val2):
                    val1 += val2
                    return val1

            # define an accumulator function
            global runsum

            def outerSumOther(x, y):
                global runsum
                runsum += outer(x, dot(x, y))

            # iterative update subspace using expectation maximization
            # e-step: x = (c'c)^-1 c' y
            # m-step: c = y x' (xx')^-1
            while (iter < self.maxiter) & (error > self.tol):

                c_old = c

                # pre compute (c'c)^-1 c'
                c_inv = dot(c.T, inv(dot(c, c.T)))

                # compute (xx')^-1 through a map reduce
                xx = mat.times(c_inv).gramian()
                xx_inv = inv(xx)

                # pre compute (c'c)^-1 c' (xx')^-1
                premult2 = mat.rdd.context.broadcast(dot(c_inv, xx_inv))

                # compute the new c using an accumulator
                # direct approach: c = mat.rows().map(lambda x: outer(x, dot(x, premult2.value))).sum()
                runsum = mat.rdd.context.accumulator(zeros((mat.ncols, self.k)), MatrixAccumulatorParam())
                mat.rows().foreach(lambda x: outerSumOther(x, premult2.value))
                c = runsum.value

                # transpose result
                c = c.T

                error = sum(sum((c - c_old) ** 2))
                iter += 1

            # project data into subspace spanned by columns of c
            # use standard eigendecomposition to recover an orthonormal basis
            c = orth(c.T)
            cov = mat.times(c).gramian() / mat.nrows
            eigw, eigv = eigh(cov)
            inds = argsort(eigw)[::-1]
            s = sqrt(eigw[inds[0:self.k]]) * sqrt(mat.nrows)
            v = dot(eigv[:, inds[0:self.k]].T, c.T)
            u = mat.times(v.T / s)

            self.u = u
            self.s = s
            self.v = v

        return self




