#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Commands"""

import logging
import click
from pathlib import Path
import shutil
import os

from .chromium_downloader import (check_chromium,
                                  download_chromium,
                                  chromium_executable,
                                  __chroman_home__)

from .run_cdp import run

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
    chromium_dir = Path(__chroman_home__) / 'local-chromium'
    if chromium_dir.is_dir():
        print(f"removing {str(chromium_dir)}")
        shutil.rmtree(chromium_dir)
    else:
        print(f"no installation found at {str(chromium_dir)}, execute install_chromium")

@click.command()
@click.argument('target_in', nargs=1)
@click.argument('target_out', nargs=1)
@click.option('-s', '--sleeptime', default=3, help='How long to sleep while waiting for ' +
    'page to render.')
@click.option('-w/-f', '--webpage/--file', default=False, help="Use -w or --webpage if " + 
    "target is a website, -f or --file if target is a file. Default is file.")
def print_page(target_in, target_out, sleeptime, webpage) -> None:
    """render webpage and print to pdf"""
    if not webpage and not os.path.exists(target_in):
        print(f"target file does not exist")
        return

    if not check_chromium():
        print(f"chromium is not installed, execute install_chromium")
        return

    if webpage:
        target = [(target_in, target_out)]
    else:
        target = [(fr"file://" + os.path.abspath(target_in), target_out)]
    
    run(target, sleeptime)


        
