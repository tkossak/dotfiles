import subprocess
from subprocess import run
from abc import ABC, abstractmethod
import json
from typing import Union
from setup_new_linux.utils import setup

from setup_new_linux.utils.setup import log
from setup_new_linux.utils.helpers import check_if_cmd_present

pkg = None
pipx = None

class PkgManagerABC(ABC):

    @abstractmethod
    def install(self, pkg: str): pass

    @abstractmethod
    def install_if_not_installed(self, pkg: str) -> None: pass

    @abstractmethod
    def is_pkg_installed(self, pkg: str): pass

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.pkg_manager}>'


class OsPkgManagerGenerator(PkgManagerABC):

    def __init__(self,
        cmd: str,
        install_options: Union[str, list],
        is_installed_options: Union[str, list],
    ):
        self.pkg_manager = cmd
        self.install_options = [install_options] if isinstance(install_options, str) else install_options
        self.is_installed_options = [is_installed_options] if isinstance(is_installed_options, str) else is_installed_options

    def install(self,
        pkg: str
    ) -> None:
        """Install without checking if pkg is installed
        """
        if not pkg:
            raise Exception(f'{self.pkg_manager} empty pkg provided!')

        log.info(f'{self.pkg_manager} install: {pkg}')
        run(
            [self.pkg_manager] + self.install_options + [pkg],
            check=True
        )

    def install_if_not_installed(self,
        pkg: str
    ) -> int:
        """Install only if pkg is not already installed
        :returns: 0 - pkg was installed just now
                  1 - pkg was already installed
        """
        if not pkg:
            raise Exception(f'{self.pkg_manager} empty pkg provided!')

        if not self.is_pkg_installed(pkg):
            log.info(f'{self.pkg_manager} install: {pkg}')
            self.install(pkg)
            # run([self.pkg_manager,self.install_options, pkg])
            return 0
        else:
            log.debug(f'{self.pkg_manager} already installed: {pkg}')
            return 1

    def is_pkg_installed(self, pkg: str) -> bool:
        p = run(
            [self.pkg_manager] + self.is_installed_options + [pkg],
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
        if p.returncode == 0:
            return True
        else:
            return False


class Pipx(PkgManagerABC):

    def __init__(self):
        pass

    def install(self, pkg: str) -> None:
        """Install without checking if pkg is installed
        """
        log.info(f'Pipx pkg install: {pkg}')
        run(['pipx', 'install', pkg], check=True)

    def install_if_not_installed(self, pkg: str) -> None:
        """Install only if pkg is not already installed
        """

        # TODO: add return int (0 - installed just now, 1 - already installed)
        if not pkg:
            raise Exception('pipx empty pkg provided!')

        if not self.is_pkg_installed():
            self.install(pkg)
        else:
            log.debug(f'Pipx pkg already installed: {pkg}')

    def is_pkg_installed(self, pkg: str) -> bool:
        p = run(
            ['pipx', 'list', '--json'],
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
        j = json.loads(p.stdout)
        if pkg in j['venvs'].keys():
            return True
        return False


yay = OsPkgManagerGenerator(
    cmd='yay',
    install_options=['-S'] + ([] if setup.args.ask else ['--noconfirm']),
    is_installed_options='-Q',
)

pacman = OsPkgManagerGenerator(
    cmd='pacman',
    install_options=['-S'] + ([] if setup.args.ask else ['--noconfirm']),
    is_installed_options='-Q'
)


def get_os_pkg_manager():
    if check_if_cmd_present('yay'):
        return yay
    elif check_if_cmd_present('pacman'):
        return pacman
    else:
        raise Exception('Package manager not known')


pkg = get_os_pkg_manager()
pipx = Pipx()
