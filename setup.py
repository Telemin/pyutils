#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='pyutils',
    version='0.1',
    description='Ecelectic collection of useful functions',
    author='Phil Tooley',
    author_email='phil.tooley@protonmail.ch',
    url='acceleratedscience.co.uk',
    package_dir={'': 'src'},
    packages=find_packages('src', exclude='tests'),
)
