from abc import ABC
from pathlib import Path
from typing import Optional, Iterable, Union, Callable

from setup_new_linux import info
from setup_new_linux.utils.constants import CheckInstallationBy as cib
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

    @property
    def is_pkg_installed(self) -> bool:
        return self.pkg_manager.is_pkg_installed(self.pkg_name)

    @property
    def is_cmd_available(self) -> Optional[bool]:
        return check_if_cmd_present(self.cmd_name)

    def install_if_not_installed(self) -> None:
        if self.pkg_name:
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
                self.pkg_manager.install(self.pkg_name)
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
        pkg_name: str = None,
        cmd_name: str = None,
        file_locations: Iterable[Union[str, Path]] = None,
        # check_install_by_pkg_not_cmd: bool = False,
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
            Used to check if packages is installed
        """
        if file_locations is None:
            file_locations = ()
        if distros:
            if info.distro in distros:
                pkg_name = distros[info.distro]
            elif 'default' in distros:
                pkg_name = distros['default']

        self.name = name
        self.pkg_name = pkg_name if pkg_name else name
        self.cmd_name = cmd_name if cmd_name else name
        self.file_locations = {Path(f) for f in file_locations}
        self.pkg_manager = pkg_manager if pkg_manager else package_managers.pkg
        self.check_install_by = check_install_by
        if configure_func:
            self.configure = configure_func
