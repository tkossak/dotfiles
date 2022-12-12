import argparse
import logging
import sys

args = None
log = None


def setup_args():
    p = argparse.ArgumentParser()
    p.add_argument('--os-repos',         '-r', action='store_true', help='Configure os eg: update mirrors')
    p.add_argument('--os-configure',     '-c', action='store_true', help='Configure os eg: $PATH in bash')
    p.add_argument('--install-packages', '-p', action='store_true', help='Install packages')
    p.add_argument('--install-dotfiles', '-d', action='store_true', help='Install dotfiles')

    p.add_argument('--verbose',          '-v', action='store_true', help='Set DEBUG lvl of logging')
    p.add_argument('--ask',              '-k', action='store_true', help='display yes/no confirmations for pkg managers')
    p.add_argument('--all',              '-a', action='store_true', help='Do all steps')
    a = p.parse_args()
    if a.all:
        a.os_repos = True
        a.os_configure = True
        a.install_packages = True
        a.install_dotfiles = True
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
