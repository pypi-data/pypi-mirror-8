#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of kryptomime, a Python module for email kryptography.
# Copyright © 2013,2014 Thomas Tanner <tanner@gmx.net>
# 
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the included LICENSE file for details.
#______________________________________________________________________________

from __future__ import absolute_import
from __future__ import print_function

import setuptools
from setuptools.command.test import test as TestCommand

__author__ = "Thomas Tanner"
__contact__ = 'tanner@gmx.net'
__url__ = 'https://github.com/ttanner/kryptomime'


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest, sys
        args = [self.pytest_args] if self.pytest_args else []
        errno = pytest.main(['tests']+args)
        sys.exit(errno)

setuptools.setup(
    name = "kryptomime",
    description="Python support for E-Mail kryptography",
    long_description=open('README.rst').read(),
    license="GPLv3+",

    version='0.4.1',
    author=__author__,
    author_email=__contact__,
    maintainer=__author__,
    maintainer_email=__contact__,
    url=__url__,

    package_dir={'kryptomime': 'kryptomime'},
    packages=['kryptomime'],
    package_data={'': ['README.rst', 'COPYING.txt', 'requirements.txt']},

    tests_require=['pytest','pytest-pythonpath','coverage'],
    cmdclass = {'test': PyTest},

    install_requires=['gnupg>=1.3.2','six>=1.4.1'],
    extras_require={'docs': ["Sphinx>=1.1", "repoze.sphinx"]},

    platforms="Linux, BSD, OSX, Windows",
    download_url="https://github.com/ttanner/kryptomime/archive/master.zip",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security :: Cryptography",
        "Topic :: Utilities",]
)
