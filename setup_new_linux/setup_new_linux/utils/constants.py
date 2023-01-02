from enum import Enum, auto, unique, Flag
import logging
from pathlib import Path
import operator
from functools import reduce

log = logging.getLogger(__name__)

MAIN_PYTHON_VERSION = '3.9.16'
ASDF_DIR = Path.home() / '.asdf'
ASDF_BINARY_PATH = ASDF_DIR / 'bin/asdf'
PYTHON_BINARY_PATH_TEMPLATE = f'{ASDF_DIR}/installs/python/{{version}}/bin/python'
PYTHON_BINARY_MAIN_PATH = Path(PYTHON_BINARY_PATH_TEMPLATE.format(version=MAIN_PYTHON_VERSION))


@unique
class Distro(Enum):
    manjaro = 'manjaro'
    ubuntu = 'ubuntu'
    unknown = 'unknown'

class Groups(Flag):   # default is cli + home + work
    cli = auto()      # only console apps (no GUI)
    gui = auto()      # only GUI apps
    home = auto()     # apps for home comp
    work = auto()     # apps for work comp
    server = auto()   # apps for server/VM

GROUPS_ALL = reduce(operator.or_, Groups.__members__.values())
# GROUPS_ALL = Groups(0)
# for v in Groups.__members__.values():
#     GROUPS_ALL |= v


@unique
class CheckInstallationBy(Enum):
    pkg = auto()        # pkg managers shows this pkg is installed
    cmd = auto()        # cmd exists in $PATH
    files_any = auto()  # at least 1 file from provided list exists
    any = auto()        # pkg / cmd / files_any
