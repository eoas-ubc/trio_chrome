#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Meta data"""

import os

from appdirs import AppDirs

__chromium_revision__ = '588429'
__PNAME_home__ = os.environ.get(
    'PNAME_HOME', AppDirs('PNAME').user_data_dir)  # type: str