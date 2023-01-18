import argparse
import logging
import sys
from pathlib import Path
import shutil

from setup_new_linux.utils import constants as C

args = None
log = None


def setup_args():
    p = argparse.ArgumentParser()
    p.add_argument('--all'             , '-a', action='store_true', help='Do all steps, except priv')
    p.add_argument('--os-repos'        , '-r', action='store_true', help='Configure os eg: update mirrors')
    p.add_argument('--os-configure'    , '-c', action='store_true', help='Configure os eg: $PATH in bash')
    p.add_argument('--install-packages', '-p', action='store_true', help='Install packages')
    p.add_argument('--install-dotfiles', '-d', action='store_true', help='Install dotfiles')
    p.add_argument('--priv'            ,       action='store_true', help='Run method from local dotfiles')

    # if pkg should be installed: all args groups must match the package groups
    p.add_argument('--groups'          , '-g', help=f'which groups to install ({", ".join(C.Groups._member_names_)}) - they all must match for packages!')
    p.add_argument('--pkg'             ,       help='Install only these packages (comma separated)')
    p.add_argument('--pkg-configure'   ,       help='Run configure method for these packages')
    p.add_argument('--except-pkg'      ,       help='Do NOT install these packages (comma separated)')
    p.add_argument('--force'           , '-f', action='store_true', help='Install packages even if they are already installed')
    p.add_argument('--local-python'    , '-l', action='store_true', help='use local python for pipx packages')
    p.add_argument('--live-usb'        , '-u', action='store_true', help='Options and packages suitable for live usb (-l and without base-devel)')

    p.add_argument('--groups-info'     , '-i', action='store_true', help=f'Print info about groups')
    p.add_argument('--sort-by-name'    , '-n', action='store_true', help=f'Sort by name (when printing groups/packages')
    p.add_argument('--verbose'         , '-v', action='store_true', help='Set DEBUG lvl of logging')
    p.add_argument('--ask'             , '-k', action='store_true', help='display yes/no confirmations for pkg managers')
    a = p.parse_args()

    if a.pkg:
        a.pkg = a.pkg.split(',')
        a.install_packages = True
    else:
        a.pkg = []

    a.pkg_configure = a.pkg_configure.split(',') if a.pkg_configure else []

    if a.except_pkg:
        a.except_pkg = a.except_pkg.split(',')
        a.install_packages = True
    else:
        a.except_pkg = []

    if a.live_usb:
        a.local_python = True
        a.except_pkg.append('base-devel')  # because it updates ssl/crypto libraries and many things stop working
        # TODO: try installing with 'base-devel' but first update os???
        a.install_dotfiles = True

    if a.groups:
        for g in a.groups.split(','):
            v = C.Groups(0)
            if g not in C.Groups._member_names_:
                p.error(f'Invalid group: {g}')
            v |= C.Groups._member_map_[g]
        a.groups = v
    else:
        a.groups = C.Groups.cli

    if a.all:
        a.os_repos = True
        a.os_configure = True
        a.install_packages = True
        a.install_dotfiles = True

    if a.local_python:
        C.PYTHON_BINARY_MAIN_PATH = Path(shutil.which('python'))

    return a


class MyFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.DEBUG:
            self._style._fmt = '━━━[%(levelname)1.1s %(message)s'
        elif record.levelno == logging.INFO:
            self._style._fmt = '━━━[%(levelname)1.1s➽ %(message)s'
        else:
            self._style._fmt = '━━━[%(levelname)1.1s❌  [%(module)s:%(lineno)d] %(message)s'
        return super().format(record)


def setup_logging(name: str, lvl: int):
    mylog = logging.getLogger(name)
    mylog.setLevel(lvl)
    sh = logging.StreamHandler(sys.stdout)
    # sh.setFormatter(logging.Formatter('━━━➽ %(asctime)s %(levelname)1.1s [%(module)s:%(lineno)d] %(message)s'))
    sh.setFormatter(MyFormatter())
    sh.setLevel(lvl)
    mylog.addHandler(sh)
    return mylog


def setup_args_and_logging():
    global args, log
    args = setup_args()
    if args.verbose:
        lvl = logging.DEBUG
    else:
        lvl = logging.INFO
    log = setup_logging(__name__, lvl)
