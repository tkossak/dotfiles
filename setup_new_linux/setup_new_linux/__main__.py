import traceback
from pathlib import Path
import getpass
import sys
import os

from setup_new_linux import (
    __version__,
    dos,
    info,
    packages,
    dotfiles
)
from setup_new_linux.classes.packagesc import OsPackage
from setup_new_linux.classes.dotfilesc import Dotfile
from setup_new_linux.utils.setup import args, log
from setup_new_linux.utils import constants as C
from setup_new_linux.utils import helpers as H

# TODO: copy to pendrive
# .emacs.d/
# Kossak/org/
# Kossak/obsidian/


def install_packages():
    for pkg in packages.packages:
        if isinstance(pkg, str):
            pkg = OsPackage(pkg)
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
            # if isinstance(d, LocalDotfile) and not info.dotfiles_local_exists:
            if isinstance(d, Dotfile) and d.dont_add_errors_to_info_if_no_locals and not info.dotfiles_local_exists:
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


def print_groups_info():
    if args.groups == C.Groups(0):
        packages_to_print = packages.packages  # all packages
        groups_to_print_str = '<any/all packages>'
    else:
        packages_to_print = [p for p in packages.packages if p.groups & args.groups == args.groups]
        groups_to_print_list = []
        for v in C.Groups.__members__.values():
            if v in args.groups:
                groups_to_print_list.append(v.name)
        groups_to_print_str = ', '.join(g for g in groups_to_print_list)

    packages_to_print.sort(key=lambda p: (p.get_group_names_str(), p.name))
    max_pkg_name_length = max(len(p.name) for p in packages_to_print)

    print(f'\nPackages matching all of the groups: {groups_to_print_str}:')
    for pkg in packages_to_print:
        # pkg_name = pkg.name.ljust(20)
        print(f'{pkg.name:<{max_pkg_name_length}} - {pkg.get_group_names_str()}')
    print()


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

    if args.os_repos or args.os_configure or args.install_packages or args.install_dotfiles:
        if os.geteuid() == 0:
            answer = input('You are running as root! You should switch to non-root user. Continue as root? (y/n) ')
            if answer.lower() != 'y':
                return

        home_local_bin = Path.home() / '.local/bin'
        home_local_bin.mkdir(parents=True, exist_ok=True)
        paths = [
            str(Path.home() / '.asdf/bin'),
            str(home_local_bin),
            str(Path.home() / '.poetry/bin'),
        ]
        paths_str = os.pathsep.join(paths)
        os.environ['PATH'] = f'{paths_str}{os.pathsep}{os.environ["PATH"]}'

    if args.groups_info:
        print_groups_info()

    if args.os_repos:
        dos.os_update_repos()
    if args.os_configure:
        dos.os_configure()

    if args.install_packages:
        install_packages()
    if args.install_dotfiles:
        install_dotfiles()
        dos.create_kossak_links()

    if info.pkg_installed:
        print('\n━━━━ INSTALLED PKGS: ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        info.pkg_installed.sort()
        print(f'{len(info.pkg_installed)} pkgs installed: {", ".join(info.pkg_installed)}')
        # for e in info.pkg_installed:
        #     log.error(e)
        # log.info(f'Errors: {len(info.errors)}')

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


def test():
    # dos.create_kossak_links()
    ...


if __name__ == '__main__':
    main()
    # test()
