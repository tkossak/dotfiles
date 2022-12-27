from enum import Enum, auto, unique, Flag
import logging
from pathlib import Path

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


# # which group to install:
# @unique
# class InstallGroup(Enum):
#     all = auto()
#     home = auto()
#     work = auto()
#
# @unique
# class Group(Flag):  # default is cli + home + work
#     all = 'all'     # install app in all groupes
#     cli = 'cli'     # only console apps (no GUI)
#     gui = 'gui'     # only GUI apps
#     home = 'home'   # apps for home comp
#     work = 'work'   # apps for work comp

class Groups(Flag):   # default is cli + home + work
    # all = auto()      # install app in all groupes
    cli = auto()      # only console apps (no GUI)
    gui = auto()      # only GUI apps
    home = auto()     # apps for home comp
    work = auto()     # apps for work comp
    server = auto()   # apps for server/VM


@unique
class CheckInstallationBy(Enum):
    pkg = auto()        # pkg managers shows this pkg is installed
    cmd = auto()        # cmd exists in $PATH
    files_any = auto()  # at least 1 file from provided list exists
    any = auto()        # pkg / cmd / files_any
