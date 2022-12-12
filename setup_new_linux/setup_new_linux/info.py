import platform
import subprocess
from subprocess import run
from pathlib import Path

from setup_new_linux.utils.setup import log
from setup_new_linux.utils.constants import Distro


def get_distro() -> str:
    current_distro = platform.release().lower()
    if 'manjaro' in current_distro:
        return Distro.MANJARO
    else:
        raise Exception(f'Unknown distro: {current_distro}')


def check_if_using_systemd() -> bool:
    p = run(
        ['ps', '--no-headers', '-o', 'comm', '1'],
        stdout=subprocess.PIPE,
        universal_newlines=True,
        check=True,
    )
    return True if 'systemd' in p.stdout else False

def get_dotfiles_path():
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
    log.error("Can't find dotfiles folder")
    return None

def get_dotfiles_local_path():
    p = Path(__file__)
    while True:
        p = p.parent
        dotfiles = p / 'dotfiles'
        if dotfiles.is_dir():
            return dotfiles
        if p == p.parent:
            break

    for p in (
        Path.home() / '.dotfiles.local',
        Path.home() / 'Kossak/files_not_synced/dotfiles.local',
        Path.home() / 'apps/dotfiles.local',
    ):
        if p.is_dir():
            return p
    log.error("Can't find dotfiles folder")
    return None


dotfiles_dir = get_dotfiles_path()
dotfiles_local_dir = get_dotfiles_local_path()
distro: str = get_distro()
systemd: bool = check_if_using_systemd()
errors: list = []




