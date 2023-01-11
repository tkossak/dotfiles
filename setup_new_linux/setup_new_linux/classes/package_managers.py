import subprocess
# from subprocess import run
from abc import ABC, abstractmethod
import json
from typing import Union, List
from setup_new_linux.utils import setup
import shlex
from pathlib import Path

from setup_new_linux.utils.setup import log
from setup_new_linux.utils.helpers import check_if_cmd_present, run_cmd
from setup_new_linux.utils import constants

os_pkg = None
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
        install_options: str,
        is_installed_options: str = None,
        is_installed_template: str = None,
        sudo_install: bool = False,
    ):
        """
        :param cmd: pkg manager executable name or full path to it

        :param is_installed_options: Options to check if package is installed.
            Package name will appended.
            Pass only 1 of:
                is_installed_options
                is_installed_template

        :param is_installed_template: if provided, must contain {pkg} param
        :param sudo_install: if True: run installations with sudo
        """
        if (
            not (is_installed_options or is_installed_template)
            or is_installed_options and is_installed_template
        ):
            raise Exception('One of the params must be set: is_installed_options / is_installed_template')

        self.pkg_manager = cmd
        self.pkg_manager_name = cmd.split('/')[-1]

        # install_options = shlex.split(install_options) if isinstance(install_options, str) else install_options
        # self.pkg_manager_run_install = (['sudo'] if sudo_install else []) + [self.pkg_manager] + self.install_options
        self.cmd_install_template = f'{"sudo " if sudo_install else ""}{self.pkg_manager} {install_options} {{pkg}}'

        if is_installed_template:
            # self.is_installed_template = shlex.split(is_installed_template) if isinstance(is_installed_template, str) else is_installed_template
            if '{pkg}' not in is_installed_template:
                raise Exception(f'No "{{pkg}}" in is_installed_options: {is_installed_options}')
            self.cmd_is_installed_template: str = is_installed_template
        elif is_installed_options:
            # is_installed_options = shlex.split(is_installed_options) if isinstance(is_installed_options, str) else is_installed_options
            # self.is_installed_template = [self.pkg_manager] + is_installed_options  + [os_pkg]
            is_installed_options: str = is_installed_options if isinstance(is_installed_options, str) else ' '.join(is_installed_options)
            self.cmd_is_installed_template = f'{self.pkg_manager} {is_installed_options} {{pkg}}'
        else:
            raise Exception('provide either is_installed_options or is_installed_template')

    def install(self,
        pkg: str
    ) -> None:
        """Install without checking if pkg is installed
        """
        if not pkg:
            raise Exception(f'{self.pkg_manager_name}: empty pkg provided!')

        log.info(f'{self.pkg_manager_name} install: {pkg}')
        cmd = shlex.split(self.cmd_install_template.format(pkg=pkg))
        run_cmd(cmd)

    def install_if_not_installed(self,
        pkg: str
    ) -> int:
        """Install only if pkg is not already installed
        :returns: 0 - pkg was installed just now
                  1 - pkg was already installed
        """
        if not pkg:
            raise Exception(f'{self.pkg_manager_name}: empty pkg provided!')

        if not self.is_pkg_installed(pkg):
            log.info(f'{self.pkg_manager_name} install: {pkg}')
            self.install(pkg)
            return 0
        else:
            log.debug(f'{self.pkg_manager_name} already installed: {pkg}')
            return 1

    def is_pkg_installed(self, pkg: str) -> bool:
        """
        :returns: True - if pkg is installed
                  False - if pkg is NOT installed
        """

        cmd = shlex.split(self.cmd_is_installed_template.format(pkg=pkg))
        p = run_cmd(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if p.returncode == 0:
            return True
        else:
            return False


class Pipx(PkgManagerABC):

    def __init__(self,
        python: Union[str, Path] = constants.PYTHON_BINARY_MAIN_PATH
    ):
        """
        :param python: Install pkgs using this python (path to binary) by default
        """
        pkg_manager = Path.home() / '.local/bin/pipx'
        self.pkg_manager_cmd = str(pkg_manager)
        self.pkg_manager_name = pkg_manager.name
        self.python = str(python)

    def install(self,
        pkg: str,
        python: Union[str, Path] = None,
    ) -> None:
        """Install without checking if pkg is installed
        :param pkg: Pkg to install
        :param python: Path to python interpreter used to install this package
        """
        if not pkg:
            raise Exception(f'{self.pkg_manager_name}: empty pkg provided!')
        python = str(python) if python else self.python

        log.info(f'{self.pkg_manager_name} install: {pkg}')
        run_cmd([self.pkg_manager_cmd, 'install', '--python', python, pkg])

    def install_if_not_installed(self,
        pkg: str,
        python: Union[str, Path] = None,
    ) -> int:
        """Install only if pkg is not already installed
        """
        if not pkg:
            raise Exception(f'{self.pkg_manager_name}: empty pkg provided!')
        python = str(python) if python else self.python

        if not self.is_pkg_installed():
            log.info(f'{self.pkg_manager_name} install: {pkg}')
            self.install(pkg, python)
            return 0
        else:
            log.debug(f'{self.pkg_manager_name} already installed: {pkg}')
            return 1

    def is_pkg_installed(self, pkg: str) -> bool:
        """
        :returns: True - if pkg is installed
                  False - if pkg is NOT installed
        """
        p = run_cmd(
            [self.pkg_manager_cmd, 'list', '--short'],
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
        if f'\n{pkg} ' in f'\n{p.stdout}':
            return True
        return False

    def inject(self,
        pkg: str,
        inject: Union[str, List[str]] = None,
    ):
        """
        :param inject: string (space separated) or list of packages to inject into `pkg`
        """
        if not pkg:
            raise Exception(f'{self.pkg_manager_name} inject: empty pkg provided!')
        if not inject:
            raise Exception(f'{self.pkg_manager_name} inject: empty inject list provided!')

        inject = [p.strip() for p in (inject.split(',') if isinstance(inject, str) else inject)]
        run_cmd([self.pkg_manager_cmd, 'inject', pkg] +  inject)

pipx = Pipx()


yay = OsPkgManagerGenerator(
    cmd='yay',
    # install_options=['-S'] + ([] if setup.args.ask else ['--noconfirm']),
    install_options=f'-S{"" if setup.args.ask else " --noconfirm"}',
    is_installed_options='-Q',
    # is_installed_template="-Qs '^{pkg}$'",
)


pacman = OsPkgManagerGenerator(
    cmd='pacman',
    # install_options=['-S'] + ([] if setup.args.ask else ['--noconfirm']),
    install_options=f'-S{"" if setup.args.ask else " --noconfirm"}',
    is_installed_options='-Q',
    sudo_install=True,
)

# TODO: apt, dnf, zypper

def get_os_pkg_manager():
    if check_if_cmd_present('yay'):
        return yay
    elif check_if_cmd_present('pacman'):
        return pacman
    else:
        raise Exception('Package manager not known')


os_pkg = get_os_pkg_manager()
pipx = Pipx()
