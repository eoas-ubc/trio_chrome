"""
define the path to important folders without having
to install anything -- just do:

import context

"""

import sys
from pathlib import Path

path = Path(__file__).resolve()  # this file
this_dir = path.parent  # this folder
testhtml_dir = this_dir / 'testhtml'

# sys.path.insert(0,str(lib_dir))
# sep = "*" * 30
# print(f"{sep}\ncontext imported. Front of path:\n{sys.path[0]}\n"
#       f"back of path: {sys.path[-1]}\n{sep}\n")


