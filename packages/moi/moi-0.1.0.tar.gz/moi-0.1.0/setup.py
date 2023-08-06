#!/usr/bin/env python

# -----------------------------------------------------------------------------
# Copyright (c) 2013, The qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

__version__ = "0.1.0"

from setuptools import setup


classes = """
    Development Status :: 4 - Beta
    License :: OSI Approved :: BSD License
    Topic :: Software Development :: Libraries :: Python Modules
    Programming Language :: Python
    Programming Language :: Python :: 2.7
    Programming Language :: Python :: Implementation :: CPython
    Operating System :: OS Independent
    Operating System :: POSIX :: Linux
    Operating System :: MacOS :: MacOS X
"""

long_description = """MOI: compute like a mustached octo ironman"""

classifiers = [s.strip() for s in classes.split('\n') if s]

setup(name='moi',
      version=__version__,
      long_description=long_description,
      license="BSD",
      description='Compute ninja',
      author="Qiita development team",
      author_email="mcdonadt@colorado.edu",
      url='http://github.com/biocore/mustached-octo-ironman',
      test_suite='nose.collector',
      packages=['moi'],
      extras_require={'test': ["nose >= 0.10.1", "pep8", 'mock']},
      install_requires=['future==0.13.0', 'tornado==3.1.1', 'toredis', 'redis',
                        'ipython[all]'],
      classifiers=classifiers
      )
