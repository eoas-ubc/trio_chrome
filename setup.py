#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from setuptools import setup
import sys

setup(
    name='chroman',
    version='0.1',
    packages=['chroman'],
    package_dir={'chroman': 'chroman'},
    entry_points={
        'console_scripts': [
            'install_chromium = chroman.command:install_chromium',
            'find_chromium = chroman.command:find_chromium',
            'clean_chromium = chroman.command:clean_chromium',
            'print_page = chroman.command:print_page',
        ],
    },
    python_requires='>=3.5',
)
