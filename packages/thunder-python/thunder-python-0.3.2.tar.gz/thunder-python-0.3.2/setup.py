#!/usr/bin/env python

from setuptools import setup
import thunder

setup(
	name='thunder-python',
  version=str(thunder.__version__),
  description='Large-scale neural data analysis in Spark',
  author='The Freeman Lab',
  author_email='the.freeman.lab@gmail.com',
  url='https://github.com/freeman-lab/thunder',
  packages=['thunder',
  					'thunder.regression',
  					'thunder.factorization',
  					'thunder.decoding',
  					'thunder.clustering',
  					'thunder.timeseries',
  					'thunder.utils',
  					'thunder.viz',
            'thunder.lib'],
  scripts = ['bin/thunder', 'bin/thunder-submit', 'bin/thunder-ec2'],
  package_data = {'thunder.utils': ['data/fish.txt', 'data/iris.txt'], 'thunder.lib': ['thunder_2.10-' + str(thunder.__version__) + '.jar']},
  long_description=open('README.rst').read(),
  install_requires=open('requirements.txt').read().split()
)