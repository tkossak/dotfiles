from abc import ABC
from pathlib import Path
from typing import Optional, Iterable, Union, Callable, Set, List

from setup_new_linux import info
from setup_new_linux.utils.setup import args
from setup_new_linux.utils import constants as C
from setup_new_linux.utils.constants import CheckInstallationBy as Cib
from setup_new_linux.utils.helpers import check_if_cmd_present, run_cmd
from setup_new_linux.utils.setup import log
from setup_new_linux.classes import package_managers
from setup_new_linux.classes.package_managers import PkgManagerABC


class Package():

#     @abstractproperty
#     def pkg_name(self): pass
#
#     @abstractproperty
#     def cmd_name(self): pass
#
#     @abstractproperty
#     def pkg_manager(self) -> PkgManagerABC: pass
#
#     @abstractproperty
#     def check_if_installed_by_cmd_not_pkg(self) -> bool: pass
    def __init__(self,
        name: str,
        groups: C.Groups = None,
        install_cmd: Union[str, Iterable] = None,
        pkg_manager: PkgManagerABC = None,
        pkg_name: Union[str, List[str]] = None,
        cmd_name: str = None,
        file_locations: Iterable[Union[str, Path]] = None,
        check_install_by: Cib = Cib.cmd,
        distros: dict = None,
        configure_func: Callable = None,
    ):
        """
        :param distros:
            {
                'default'       : None,  # skip installation on not specified here distros
                C.Distro.value1: 'pkg_name1',
                C.Distro.value2: 'pkg_name2',
                C.Distro.value3: None, # skip installation for this distro
            }
        :param pkg_name: Package name to install. If you pass list of package
            names, it will try to install them in sequence until the first,
            that succeeds


        :param cmd_name: Cmd name, that can be found in $PATH

        :param file_locations: Iterable of possible binary locations. Used to
            check if package is installed
        """

        assert isinstance(pkg_name, (str, list, None.__class__))

        if not pkg_name:
            pkg_names = [name]
        elif isinstance(pkg_name, str):
            pkg_names = [pkg_name]
        self.pkg_name = pkg_names[0]

        self.install_for_current_distro = True
        if distros:
            if info.distro in distros:
                pkg_names = distros[info.distro]
            elif 'default' in distros:
                pkg_names = distros['default']
            else:
                self.install_for_current_distro = False

            assert isinstance(pkg_names, (str, list, None.__class__))

            if isinstance(pkg_names, (str, None.__class__)):
                pkg_names = [pkg_names]

        if not pkg_names[0]:
            self.install_for_current_distro = False

        self.pkg_names_to_install = pkg_names

        self.name = name
        self.groups = groups if isinstance(groups, C.Groups) else C.Groups.cli | C.Groups.home | C.Groups.work
        self.install_cmd = install_cmd
        self.pkg_manager = pkg_manager if pkg_manager else package_managers.os_pkg
        self.cmd_name = cmd_name if cmd_name else name
        self.file_locations = {Path(f) for f in file_locations or ()}
        self.check_install_by = check_install_by
        if configure_func:
            self.configure = configure_func

        if args.groups & self.groups == args.groups:  # all groups from cli must match the package!
            self.install_for_current_groups = True
        else:
            self.install_for_current_groups = False


    @property
    def is_pkg_installed(self) -> bool:
        """check if self.pkg_name is installed
        """
        return self.pkg_manager.is_pkg_installed(self.pkg_name)

    @property
    def is_any_pkg_installed(self) -> bool:
        """check if at least one package from self.pkg_name_alternatives is installed
        """
        return any(self.pkg_manager.is_pkg_installed(p) for p in self.pkg_names_to_install)

    @property
    def is_cmd_available(self) -> Union[str, bool]:
        return check_if_cmd_present(self.cmd_name)

    def install(self, pkg_name=None):
        if not pkg_name:
            pkg_name = self.pkg_name

        if self.install_cmd:
            log.info(f'Install: {self.name}')
            run_cmd(self.install_cmd)
        else:
            self.pkg_manager.install(pkg_name)

    def install_if_not_installed(self) -> int:
        """
        :returns: 0 - pkg was just installed
                  1 - pkg was already installed
                  2 - not installing (eg. doesn't match groups)

        """
        if not self.install_for_current_groups:
            groups_names = ', '.join(v.name for v in C.Groups if v in args.groups)
            log.debug(f"{self.name} package not installing, it doesn't match all groups: {groups_names}")
            return 2
        elif not self.install_for_current_distro:
            log.info(f'{self.pkg_manager.pkg_manager_name}: {self.name} package not installing for current distro: {info.distro}')
            return 2
        else:  # if self.pkg_name:
            if (
                   self.check_install_by == Cib.any and not (  # 1 is enough to knows it's installed:
                        any(f.exists() for f in self.file_locations)
                        or self.is_cmd_available
                        or self.is_pkg_installed
                    )
                or self.check_install_by == Cib.files_any and not any(f.exists() for f in self.file_locations)
                or self.check_install_by == Cib.cmd       and not self.is_cmd_available
                or self.check_install_by == Cib.pkg       and not self.is_pkg_installed
            ):
                for p in self.pkg_names_to_install:
                    try:
                        # self.pkg_name = p
                        self.install(p)
                        break
                    except Exception as e:
                        pass
                else:
                    raise e
                self.configure()
                return 0
            else:
                log.debug(f'{self.pkg_manager.pkg_manager_name} package already installed: {self.pkg_name}')
                return 1

    def configure(self) -> None:
        pass

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.name}>'


class OsPackage(Package):
    """
    By default installation is checked by cmd_name.
    Groups are default
    """


class GuiOsPackage(Package):
    """
    By default installation is checked by cmd_name
    Groups are: gui, work, home
    """

    def __init__(self, *args, **kwargs):
        if 'groups' not in kwargs:
            kwargs['groups'] = C.Groups.gui | C.Groups.home | C.Groups.work
        super().__init__(*args, **kwargs)


class PipxPackage(Package):
    """
    By default installation is checked by pkg_name
    Groups are default
    """

    def __init__(self,
        name,
        pkg_name_to_install: Union[str, List[str]] = None,
        inject: Union[str, List[str]] = None,
        python: Union[str, Path] = None,
        **kwargs,
    ):
        """
        :param name: Will also be used as pkg_name (to check if package is installed)
                     and for `pkg_name_to_install` if it is empty.
        :param pkg_name_to_install: Package name to install. If you pass list of package
            names, it will try to install them in sequence until the first,
            that succeeds
        """
        kwargs['name'] = name
        kwargs['pkg_manager'] = package_managers.pipx
        kwargs['check_install_by'] = Cib.pkg
        kwargs['install_cmd'] = None
        super().__init__(**kwargs)

        if pkg_name_to_install:
            self.pkg_names_to_install = pkg_name_to_install if isinstance(pkg_name_to_install, list) else  [pkg_name_to_install]
        self.python = python
        self.inject = [p.strip() for p in (inject.split(' ') if isinstance(inject, str) else inject or ()) if p.strip()]

    def install(self, pkg_name: str = None):
        if not pkg_name:
            pkg_name = self.pkg_name

        self.pkg_manager.install(pkg_name, self.python)
        if self.inject:
            self.pkg_manager.inject(self.pkg_name, self.inject)