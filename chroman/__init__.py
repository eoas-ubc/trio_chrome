#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Meta data"""

import os
from pathlib import Path

from appdirs import AppDirs

__chromium_revision__ = '588429'
if 'CONDA_PREFIX' in os.environ.keys():
    __chroman_home__ = str(Path(os.environ.get('CONDA_PREFIX')) / 'bin')
else:
    __chroman_home__ = os.environ.get(
        'INSTALL_CHROMIUM_HOME', AppDirs('chroman').user_data_dir)  # type: str
print(f"chromium install folder is {__chroman_home__}")
