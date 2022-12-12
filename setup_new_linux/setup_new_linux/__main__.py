import traceback
from pathlib import Path

from setup_new_linux import __version__, dos, info, packages as pkgs, dotfiles
from setup_new_linux.classes import package_managers
from setup_new_linux.classes.packagesc import OsPackage
from setup_new_linux.classes.dotfilesc import Dotfile
from setup_new_linux.utils.setup import args, log
from setup_new_linux.utils.constants import Distro
from setup_new_linux.utils.helpers import run_cmd


def manjaro_update_pacman_repos():
    log.info('Configure manjaro')

    log.info('Setup pacman distros')
    run_cmd('sudo pacman-mirrors -c Poland,Germany')

    log.info('Update repos')
    run_cmd('sudo pacman -Syy')


def manjaro_configure():
    # install yay:
    if pkgs.yay.install_if_not_installed() == 0:
        package_managers.pkg = package_managers.get_os_pkg_manager()
        for pkg in pkgs.Packages:
            if isinstance(pkg, pkgs.PackageABC):
                pkg.pkg_manager = package_managers.pkg

    dos.enable_and_start_sshd()
    # TODO: update PATH in bash

    # TODO: change colors for pacman/yay


def install_packages():
    for pkg in pkgs.Packages:
        if isinstance(pkg, str):
            pkg =  OsPackage(pkg)
        try:
            pkg.install_if_not_installed()
        except Exception as e:
            msg = f'Pkg {pkg.name} install error, type: {type(e).__name__}, e: {e}, traceback:\n{traceback.format_exc()}'
            log.error(msg)
            info.errors.append(msg)


def install_dotfiles():
    if not info.dotfiles_dir:
        log.error('Not installing dotfiles, because no dotfiles dir found')
    for d in dotfiles.dotfiles:
        name = str(d)
        try:
            if isinstance(d, Dotfile):
                name = d.src.name
                d.install()
            elif callable(d):
                d()
            else:
                raise Exception(f'Wrong type of dotfile: {type(d)}')
        except Exception as e:
            msg = f'Dotfile {name} install error, type: {type(e).__name__}, e: {e}, traceback:\n{traceback.format_exc()}'
            log.error(msg)
            info.errors.append(msg)

    # remove unwanted shims from asdf:
    asdf_shims = Path.home() / '.asdf/shims'
    for f in ['powerline*', 'xz', 'sqlite3', 'xmllint', 'iconv', 'envsubst', 'clear', 'gettext', 'gettext.sh', 'tput', 'envsubst', 'pandoc', 'pipx', 'bsdtar', 'reset', 'zstd', 'bzip2']:
        for file in asdf_shims.glob(f):
            log.info(f'Removing: {file}')
            file.unlink()

    # maybe TODO: link fish files


def main():
    log.info(f'Main START, version: {__version__}')
    log.info(f'distro: {info.distro}')
    log.info(f'Systemd: {info.systemd}')
    log.info(f'Dotfiles dir: {info.dotfiles_dir}')

    if args.os_repos and info.distro == Distro.MANJARO:
        manjaro_update_pacman_repos()
    if args.os_configure and info.distro == Distro.MANJARO:
        manjaro_configure()

    if args.install_packages:
        install_packages()
    if args.install_dotfiles:
        install_dotfiles()

    if info.errors:
        print('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        log.info('ALL ERRORS: ')
        for e in info.errors:
            log.error(e)
        log.info(f'Errors: {len(info.errors)}')
    else:
        log.info('NO ERRORS FOUND')

    log.info('Main END')


if __name__ == '__main__':
    main()
