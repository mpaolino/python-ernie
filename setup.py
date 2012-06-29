#!/usr/bin/env python

from distutils.core import setup

# The original author of this library is
# Ken Robertson ken@invalidlogic.com
# This version is a fork on github maintained by
# Miguel Paolino miguel@paolino.com.uy.
#
# Ken's library version number depended on
# the version number of python-bert. This is
# not suitable for an automated installation
# using pip which will automatically install 
# the dependencies listed in 'install_requires'.
# For this reason I manually set the version
# number.
__version__ = '2.0.0'

setup(
    name = 'ernie',
    version = __version__,
    description = 'BERT-Ernie Library',
    author = 'Miguel Paolino',
    author_email = 'miguel@paolino.com.uy',
    url = 'http://github.com/mpaolino/python-ernie',
    packages = ['ernie'],
    classifiers = [
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ], 
    install_requires = ["bert>=2.0.0"],
    dependency_links = [
        'http://github.com/samuel/python-bert/tarball/master#egg=bert-2.0.0'
    ]
)
