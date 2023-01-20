from enum import Enum, auto, unique, Flag
import logging
from pathlib import Path
import operator
from functools import reduce

# will be installed by asdf and set as global:
MAIN_PYTHON_VERSION = '3.9.16'
ASDF_DIR = Path.home() / '.asdf'
ASDF_BINARY_PATH = ASDF_DIR / 'bin/asdf'
PYTHON_ASDF_BINARY_PATH_TEMPLATE = f'{ASDF_DIR}/installs/python/{{version}}/bin/python'
PYTHON_ASDF_BINARY_MAIN_PATH = Path(PYTHON_ASDF_BINARY_PATH_TEMPLATE.format(version=MAIN_PYTHON_VERSION))

# it will be used for pipx installation and its packages
PYTHON_BINARY_MAIN_PATH = PYTHON_ASDF_BINARY_MAIN_PATH  # may be changed via CLI options


@unique
class Distro(Enum):
    manjaro = 'manjaro'
    ubuntu = 'ubuntu'
    unknown = 'unknown'

class Groups(Flag):   # default is cli + home + work
    cli = auto()      # apps CLI
    gui = auto()      # apps GUI
    home = auto()     # apps for home comp
    work = auto()     # apps for work comp
    server = auto()   # apps for server/VM
    liveusb = auto()  # apps for live usb
    pipx = auto()     # pipx and its apps (so you can remove pipx and install all apps at once)

GROUPS_ALL = reduce(operator.or_, Groups.__members__.values())
GROUPS_DEFAULT_PKG = Groups.cli | Groups.home | Groups.work
# GROUPS_ALL = Groups(0)
# for v in Groups.__members__.values():
#     GROUPS_ALL |= v


@unique
class CheckInstallationBy(Enum):
    pkg = auto()        # pkg managers shows this pkg is installed
    cmd = auto()        # cmd exists in $PATH
    files_any = auto()  # at least 1 file from provided list exists
    any = auto()        # pkg / cmd / files_any
