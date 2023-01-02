import platform
import subprocess
from subprocess import run
from pathlib import Path
from typing import Tuple, Optional
import json

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
    msg = "Can't find dotfiles folder"
    log.error(msg)
    errors.append(msg)
    return None

def get_dotfiles_local_dir() -> Tuple[bool, Path]:
    """Find local dotfiles folder and return its existence and path
    :returns: 1'st element: True if returned Path exists
              2'nd element: Path to local dotfiles (existing or not)
    :rtype: Tuple[bool, Path]
    """
    global errors

    for p in (
        Path.home() / '.dotfiles.local',
        Path.home() / 'Kossak/files_not_synced/dotfiles.local',
        Path.home() / 'apps/dotfiles.local',
    ):
        if p.is_dir():
            return True, p

    p = Path(__file__)
    while True:
        p = p.parent
        dotfile = p / 'dotfiles.local'
        if dotfile.is_dir():
            return True, dotfile
        if p == p.parent:
            break

    msg = "Can't find local dotfiles folder"
    log.error(msg)
    errors.append(msg)
    return False, Path('/tmp/NO_LOCAL_DOTFILES')


def get_dotfiles_local_info() -> Tuple[bool, Path, dict]:
    """
    :returns: 3-element tuple:
        First 2 elements: see `get_dotfiles_local_dir()`
        3'rd element: json object with local dotfiles config
    """
    global errors
    ret_local_config_json = {}
    ret_local_exists, ret_local_dir = get_dotfiles_local_dir()
    if ret_local_exists:
        json_file = ret_local_dir / 'dotfiles.local.config.json'
        try:
            with json_file.open('rt') as fh:
                ret_local_config_json = json.load(fh)
        except:
            msg = f"Can't open local dotfiles config json!: {json_file}"
            log.error(msg)
            errors.append(msg)

    return ret_local_exists, ret_local_dir, ret_local_config_json


# pouplated by other modules
errors: list = []
verify: list = []
pkg_installed: list = []

# info variables:
dotfiles_dir = get_dotfiles_path()

(
    dotfiles_local_exists,
    dotfiles_local_dir,
    dotfiles_local_config,
) = get_dotfiles_local_info()

distro: str = get_distro()
systemd: bool = check_if_using_systemd()

