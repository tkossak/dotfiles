from enum import Enum, auto
import logging

log = logging.getLogger(__name__)


class Distro(Enum):
    MANJARO = 'manjaro'
    UBUNTU = 'ubuntu'


class InstallGroup(Enum):
    all = auto()
    home = auto()
    work = auto()


class CheckInstallationBy(Enum):
    pkg = auto()        # pkg managers shows this pkg is installed
    cmd = auto()        # cmd exists in $PATH
    files_any = auto()  # at least 1 file from provided list exists
    any = auto()        # pkg / cmd / files_any

class Groups(Enum):
    all = auto()  # install app in all groupes
    cli = auto()  # only console apps (no GUI)
    home = auto() # apps for home comp
    work = auto() # apps for work comp