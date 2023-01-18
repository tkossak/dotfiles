import traceback
from pathlib import Path
import getpass
import sys
import os
import subprocess
import re
import socket

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

# TODO: install gcloud, obsidian
# TODO: debug borgbackup - strange error on laptop
# TODO: make sure pkg-config exists


def install_packages():
    for pkg in packages.packages:
        if (
            args.pkg and pkg.name not in args.pkg
            or args.except_pkg and pkg.name in args.except_pkg
        ):
            continue
        try:
            pkg.install_if_not_installed(force=args.force)
        except Exception as e:
            msg = f'Package {pkg.name} install error, type: {type(e).__name__}, e: {e}'
            log.error(f'{msg}, traceback: {traceback.format_exc()}')
            info.errors.append(msg)

def configure_packages():
    for pkg in packages.packages:
        if (
            args.pkg_configure and pkg.name not in args.pkg_configure
            or args.except_pkg and pkg.name in args.except_pkg
        ):
            continue
        try:
            pkg.configure()
        except Exception as e:
            msg = f'Package {pkg.name} configure error, type: {type(e).__name__}, e: {e}'
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

    if args.sort_by_name:
        packages_to_print.sort(key=lambda p: p.name)
    else:
        packages_to_print.sort(key=lambda p: (p.get_group_names_str(), p.name))
    max_pkg_name_length = max(len(p.name) for p in packages_to_print)

    print(f'\nPackages matching all of the groups: {groups_to_print_str}:')
    for pkg in packages_to_print:
        # pkg_name = pkg.name.ljust(20)
        print(f'{pkg.name:<{max_pkg_name_length}} - {pkg.get_group_names_str()}')
    print()


def print_all_logs():
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


def load_priv_method():
    if not info.dotfiles_local_exists:
        msg = f"Can't load priv method, local dotfiles not found"
        log.error(msg)
        info.errors.append(msg)

    sys.path.insert(0, str(info.dotfiles_local_dir / 'local_setup_new_linux'))
    import local_setup_new_linux as l
    l.main()


def print_header():
    # groups = []
    # for v in C.Groups.__members__.values():
    #     if v & args.groups:
    #         groups.append(v.name)
    # log.info(f'Groups: {", ".join(groups)}')
    log.info(f'distro: {info.distro.name}')
    log.info(f'hostname: {socket.gethostname()}')
    log.info(f'user: {getpass.getuser()}')
    log.info(f'systemd: {info.systemd}')
    log.info(f'dotfiles dir: {info.dotfiles_dir}')
    log.info(f'dotfiles local dir: {info.dotfiles_local_dir}')

    # print IPs:
    p = H.run_cmd(
        'ip -o addr',
        check=False,
        stdout=subprocess.PIPE,
    )
    if p.returncode == 0:
        for line in p.stdout.splitlines():
            if not 'inet ' in line:
                continue
            line = re.sub(' {2,}', ' ', line)
            fields = line.split(' ')
            interface = fields[1]
            ip = fields[3]
            log.info(f'{interface}: {ip}')


def is_everything_correct() -> bool:
    """
    return True if everything is correct
    """
    # print unknown distro info:
    if info.distro == C.Distro.unknown:
        print()
        H.run_cmd(['cat', '/etc/*release*'], check=False)
        print()
        ans = input('Distro unknown, do you want to continue? (y/n)')
        if ans.lower() != 'y':
            return False

    # check if root and setup path:
    if args.os_repos or args.os_configure or args.install_packages or args.install_dotfiles:
        if os.geteuid() == 0:
            answer = input('You are running as root! You should switch to non-root user. Continue as root? (y/n) ')
            if answer.lower() != 'y':
                return False

        home_local_bin = Path.home() / '.local/bin'
        home_local_bin.mkdir(parents=True, exist_ok=True)
        for p in (  # reverse order
            str(Path.home() / '.poetry/bin'),
            str(home_local_bin),
            str(Path.home() / '.asdf/bin'),
        ):
            if f'{os.pathsep}{p}{os.pathsep}' not in f'{os.pathsep}{os.environ["PATH"]}{os.pathsep}':
                os.environ['PATH'] = f'{p}{os.pathsep}{os.environ["PATH"]}'

    # check args:
    if args.pkg:
        packages_to_check: list = args.pkg.copy()
        for pkg in packages.packages:
            if pkg.name in packages_to_check:
                packages_to_check.remove(pkg.name)
            if not packages_to_check:
                break
        else:
            print(f'Wrong pkg names: {", ".join(packages_to_check)}')
            return False
    if args.pkg_configure:
        packages_to_check: list = args.pkg_configure.copy()
        for pkg in packages.packages:
            if pkg.name in packages_to_check:
                packages_to_check.remove(pkg.name)
            if not packages_to_check:
                break
        else:
            print(f'Wrong pkg_configure names: {", ".join(packages_to_check)}')
            return False

    return True


def main():
    print_header()

    log.info(f'Main START, version: {__version__}')
    if not is_everything_correct():
        return

    if args.groups_info:
        print_groups_info()

    if args.os_repos:
        dos.os_update_mirrors_and_repos()
    if args.os_configure:
        dos.os_configure()

    if args.install_packages:
        install_packages()
    if args.pkg_configure:
        configure_packages()
    if args.install_dotfiles:
        install_dotfiles()
        dos.create_kossak_links()
    if args.priv:
        load_priv_method()

    print_all_logs()

    log.info('Main END')


def test():
    # dos.create_kossak_links()
    ...


if __name__ == '__main__':
    main()
    # test()
