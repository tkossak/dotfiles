import traceback
from pathlib import Path
import os
import subprocess
import sys
import getpass

from setup_new_linux import (
    __version__,
    dos,
    info,
    packages as package,
    services as service,
    dotfiles
)
from setup_new_linux.classes import package_managers as PM
from setup_new_linux.classes.packagesc import OsPackage
from setup_new_linux.classes.dotfilesc import Dotfile, LocalDotfile, ReplaceSnippetDotfile
from setup_new_linux.utils.setup import args, log
from setup_new_linux.utils import constants as C
from setup_new_linux.utils import helpers as H

# TODO: copy to pendrive
# .emacs.d/
# Kossak/org/
# Kossak/obsidian/


def os_update_repos():
    log.info(f'START os update repos: {info.distro.value}')
    if info.distro == C.Distro.manjaro:
        log.info('Setup manjaro/pacman mirrors')
        H.run_cmd('sudo pacman-mirrors -c Poland,Germany')

        log.info('Update pacman repos')
        H.run_cmd('sudo pacman -Syy')
    elif info.distro == C.Distro.ubuntu:
        log.info('Setup ubuntu repos')
        H.run_cmd('sudo apt clean && sudo apt update')
        # sudo apt upgrade -y && sudo apt install

    else:
        msg = f'NOT updating repos: unknown distro: {info.distro.value}'
        log.warning(msg)
        info.errors.append(msg)


def os_configure():
    """One-time setup after installing Os
    """
    log.info(f'START os configure: {info.distro.value}')
    (Path.home() / '.local/bin').mkdir(parents=True, exist_ok=True)

    if info.distro == C.Distro.manjaro:
        # install yay:
        package.yay.install_if_not_installed()
        dotfiles.etc_environment.install()
        dotfiles.bashrc.install()
        dotfiles.bashprofile.install()

        # SSH
        package.sshd.install_if_not_installed()
        service.sshd.set_presence()
        if service.sshd.is_present:
            service.sshd.enable()
            service.sshd.start()
        else:
            msg = "Not starting sshd service: can't find it"
            log.error(msg)
            info.errors.append(msg)
        # TODO: secure sshd? change port, key logging, root logging, etc

        # TODO: change colors for pacman/yay
    else:
        msg = f'NOT configuring os: unknown distro: {info.distro.value}'
        log.warning(msg)
        info.errors.append(msg)


def install_packages():
    for pkg in package.Packages:
        if isinstance(pkg, str):
            pkg =  OsPackage(pkg)
        try:
            pkg.install_if_not_installed()
        except Exception as e:
            msg = f'Package {pkg.name} install error, type: {type(e).__name__}, e: {e}'
            log.error(f'{msg}, traceback: {traceback.format_exc()}')
            info.errors.append(msg)


def install_dotfiles():
    if not info.dotfiles_dir:
        log.error('Not installing dotfiles, because no dotfiles dir found')
    for d in dotfiles.dotfiles:
        try:
            if isinstance(d, Dotfile):
                name = d.name
                d.install()
            elif callable(d):
                name = d.__name__
                d()
            else:
                raise Exception(f'Wrong type of dotfile: {type(d)}')
        except Exception as e:
            msg = f'Dotfile {name} install error, type: {type(e).__name__}, e: {e}'
            log.error(f'{msg}, traceback: {traceback.format_exc()}')
            if isinstance(d, LocalDotfile) and not info.dotfiles_local_exists:
                pass
            else:
                info.errors.append(msg)

    # remove unwanted shims from asdf:
    asdf_shims = Path.home() / '.asdf/shims'
    for f in ['powerline*', 'xz', 'sqlite3', 'xmllint', 'iconv', 'envsubst', 'clear', 'gettext', 'gettext.sh', 'tput', 'envsubst', 'pandoc', 'pipx', 'bsdtar', 'reset', 'zstd', 'bzip2']:
        for file in asdf_shims.glob(f):
            log.info(f'Removing: {file}')
            file.unlink()

    # maybe TODO: link fish files

    # TODO: create links to dirs
    # add links to pacman/yay cache folders
    # /var/cache/pacman/pkg
    # /home/kossak/.cache/yay/


def main():
    log.info(f'Main START, version: {__version__}')
    log.info(f'Current user: {getpass.getuser()}')
    log.info(f'distro: {info.distro}')
    log.info(f'Systemd: {info.systemd}')
    log.info(f'Dotfiles dir: {info.dotfiles_dir}')
    log.info(f'Dotfiles local dir: {info.dotfiles_local_dir}')

    if info.distro == C.Distro.unknown:
        print()
        H.run_cmd(['cat', '/etc/*release*'], check=False)
        print()
        ans = input('Distro unknown, do you want to continue? (y/n)')
        if ans.lower() != 'y':
            return

    if args.os_repos:
        os_update_repos()
    if args.os_configure:
        os_configure()

    if args.install_packages:
        install_packages()
    if args.install_dotfiles:
        install_dotfiles()

    if info.errors:
        print('\n━━━━ ALL ERRORS: ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        for e in info.errors:
            log.error(e)
        log.info(f'Errors: {len(info.errors)}')
    else:
        log.info('NO ERRORS FOUND')

    if info.verify:
        print('\n━━━━ VERIFY MANUALLY: ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        for e in info.verify:
            log.info(e)

    # TODO: print my IP

    log.info('Main END')

# def test():

if __name__ == '__main__':
    main()
    # test()
