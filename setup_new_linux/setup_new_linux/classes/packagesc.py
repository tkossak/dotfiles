from abc import ABC
from pathlib import Path
from typing import Optional, Iterable, Union, Callable, Set

from setup_new_linux import info
from setup_new_linux.utils.setup import args
from setup_new_linux.utils.constants import CheckInstallationBy as cib, Groups
from setup_new_linux.utils.helpers import check_if_cmd_present
from setup_new_linux.utils.setup import log
from setup_new_linux.classes import package_managers
from setup_new_linux.classes.package_managers import PkgManagerABC


class PackageABC(ABC):

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
    def __init__(
        self,
        name: str,
        groups: Groups,
    ):
        self.name = name
        self.groups = groups if isinstance(groups, Groups) else Groups.cli | Groups.home | Groups.work

    @property
    def is_pkg_installed(self) -> bool:
        return self.pkg_manager.is_pkg_installed(self.pkg_name)

    @property
    def is_cmd_available(self) -> Union[str, bool]:
        return check_if_cmd_present(self.cmd_name)

    def install(self):
        self.pkg_manager.install(self.pkg_name)

    def install_if_not_installed(self) -> None:
        if not self.install_for_current_distro:
            log.info(f'{self.name} package - not installing for current distro: {info.distro}')
        elif not self.install_for_current_groups:
            groups_names = ', '.join(v.name for v in Groups if v in args.groups)
            log.info(f'{self.name} package - not installing, it doesn''t match all groups: {groups_names}')
        else:  # if self.pkg_name:
            if (
                   self.check_install_by == cib.any and not (  # 1 is enough to knows it's installed:
                        any(f.exists() for f in self.file_locations)
                        or self.is_cmd_available
                        or self.is_pkg_installed
                    )
                or self.check_install_by == cib.files_any and not any(f.exists() for f in self.file_locations)
                or self.check_install_by == cib.cmd       and not self.is_cmd_available
                or self.check_install_by == cib.pkg       and not self.is_pkg_installed
            ):
                log.info(f'{self.name} package installing...')
                self.install()
                log.info(f'{self.name} package installed')
                self.configure()
            else:
                log.debug(f'{self.pkg_manager.pkg_manager} package already installed: {self.pkg_name}')

    def configure(self) -> None:
        pass

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.name}>'


class OsPackage(PackageABC):

    def __init__(self,
        name: str,
        groups: Groups = None,
        pkg_name: str = None,
        cmd_name: str = None,
        file_locations: Iterable[Union[str, Path]] = None,
        check_install_by: cib = cib.cmd,
        distros: dict = None,
        pkg_manager: PkgManagerABC = None,
        configure_func: Callable = None,
    ):
        """
        :param distros:
            {
                'default': None,  # skip installation on other distros
                'distro1': 'pkg_name',
                'distro2': 'pkg_name2',
                'distro3': None,  # skip installation for this distro
            }
        :param pkg_name: Package name to install
            If None: this package won't be installed at all
        :param cmd_name: Cmd name, that can be found in $PATH
        :param file_locations: Iterable of possible binary locations
            Used to check if package is installed
        """
        super().__init__(name, groups)

        self.install_for_current_distro = True
        if distros:
            if info.distro in distros:
                pkg_name = distros[info.distro]
            elif 'default' in distros:
                pkg_name = distros['default']
            else:
                self.install_for_current_distro = False

        if args.groups & self.groups == args.groups:  # all groups from cli must match the package!
            self.install_for_current_groups = True
        else:
            self.install_for_current_groups = False

        self.pkg_name = pkg_name if pkg_name else name
        self.cmd_name = cmd_name if cmd_name else name
        self.file_locations = {Path(f) for f in file_locations or ()}
        self.pkg_manager = pkg_manager if pkg_manager else package_managers.pkg
        self.check_install_by = check_install_by
        if configure_func:
            self.configure = configure_func
