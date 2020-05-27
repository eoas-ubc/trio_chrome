#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Commands"""

import logging
import click
from pathlib import Path
import shutil

from .chromium_downloader import (check_chromium,
                                  download_chromium,
                                  chromium_executable,
                                  __installchromium_home__)

@click.command()
def install_chromium() -> None:
    """Download chromium if not installed"""
    if not check_chromium():
        download_chromium()
    else:
        logging.getLogger(__name__).warning('chromium is already installed.')

@click.command()
def find_chromium() -> None:
    """find path to chromium"""
    the_path=chromium_executable()
    if the_path.is_file():
        print(f"Path to chromium: \n{str(the_path)}")
    else:
        print(f"chromium not installed, execute install_chromium")
        

@click.command()
def clean_chromium() -> None:
    """remove chromium if it exists"""
    chromium_dir = Path(__installchromium_home__) / 'local-chromium'
    if chromium_dir.is_dir():
        print(f"removing {str(chromium_dir)}")
        shutil.rmtree(chromium_dir)
    else:
        print(f"no installation found at {str(chromium_dir)}, execute install_chromium")
        
