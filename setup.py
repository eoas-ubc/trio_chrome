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
            'eoas_ubc-chromium-install = installchromium.command:install',
        ],
    },
    python_requires='>=3.5',
)
