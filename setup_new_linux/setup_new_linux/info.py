import platform
import subprocess
from subprocess import run
from pathlib import Path
from typing import Tuple, Optional

from setup_new_linux.utils.setup import log
from setup_new_linux.utils.constants import Distro


def get_distro() -> str:
    current_distro = platform.release().lower()
    if 'manjaro' in current_distro:
        return Distro.manjaro
    else:
        return Distro.unknown
        # raise Exception(f'Unknown distro: {current_distro}')


def check_if_using_systemd() -> bool:
    p = run(
        ['ps', '--no-headers', '-o', 'comm', '1'],
        stdout=subprocess.PIPE,
        universal_newlines=True,
        check=True,
    )
    return True if 'systemd' in p.stdout else False

def get_dotfiles_path() -> Optional[Path]:
    """Find dotfiles folder and return its path
    :returns: Path to dotfile folder
    :rtype: Optional[Path]
    """
    p = Path(__file__)
    while True:
        p = p.parent
        dotfiles = p / 'dotfiles'
        if dotfiles.is_dir():
            return dotfiles
        if p == p.parent:
            break

    p = Path.home / '.dotfiles/dotfiles'
    if p.is_dir():
        return p
    tmp = "Can't find dotfiles folder"
    log.error(tmp)
    errors.append(tmp)
    return None

def get_dotfiles_local_path() -> Tuple[bool, Path]:
    """Find local dotfiles folder and return its existence and path
    :returns: 1'st element: True if returned Path exists
              2'nd element: Path to local dotfiles (existing or not)
    :rtype: Tuple[bool, Path]
    """
    global errors
    p = Path(__file__)
    while True:
        p = p.parent
        dotfile = p / 'dotfiles.local'
        if dotfile.is_dir():
            return True, dotfile
        if p == p.parent:
            break

    for p in (
        Path.home() / '.dotfiles.local',
        Path.home() / 'Kossak/files_not_synced/dotfiles.local',
        Path.home() / 'apps/dotfiles.local',
    ):
        if p.is_dir():
            return True, p
    tmp = "Can't find local dotfiles folder"
    log.error(tmp)
    errors.append(tmp)
    # return None
    return False, Path('/tmp/NO_LOCAL_DOTFILES')


# pouplated by other modules
errors: list = []
verify: list = []

# info variables:
dotfiles_dir = get_dotfiles_path()
dotfiles_local_exists, dotfiles_local_dir = get_dotfiles_local_path()
distro: str = get_distro()
systemd: bool = check_if_using_systemd()

