# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2023 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""Python setup.py installer script."""

# Standard library imports
import ast
import os
import sys

# Third party imports
from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))


def get_version(module='swmmhub'):
    return "0.1"


def get_description():
    """Get long description."""
    with open(os.path.join(HERE, 'README.rst'), 'r') as f:
        data = f.read()
    return data





setup(
    name='swmmhub',
    version=get_version(),
    description='swmmhub',
    long_description_content_type='text/markdown',
    author='Bryant E. McDonnell',
    packages=find_packages(exclude=['contrib', 'docs']),
    include_package_data=True,
    license="",
    keywords="swmm5, swmm, hydraulics, hydrology, modeling, collection system",
    classifiers=[
        "Topic :: Scientific/Engineering",
        "Topic :: Documentation :: Sphinx",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
    ])
