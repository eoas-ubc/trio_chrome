#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from setuptools import setup
import sys

setup(
    name='installchromium',
    version='0.1',
    packages=['installchromium'],
    package_dir={'installchromium': 'installchromium'},
    entry_points={
        'console_scripts': [
            'install_chromium = installchromium.command:install_chromium',
            'find_chromium = installchromium.command:find_chromium',
            'clean_chromium = installchromium.command:clean_chromium',
        ],
    },
    python_requires='>=3.5',
)
