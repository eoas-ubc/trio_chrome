#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from setuptools import setup
import sys

setup(
    name='PNAME',
    version='0.1',
    packages=['PNAME'],
    package_dir={'PNAME': 'PNAME'},
    entry_points={
        'console_scripts': [
            'eoas_ubc-chromium-install = PNAME.command:install',
        ],
    },
    python_requires='>=3.5',
)
