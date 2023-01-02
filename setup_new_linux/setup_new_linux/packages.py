from pathlib import Path
import shlex
import subprocess
import re
from packaging.version import Version
import os
import urllib.request
from io import BytesIO
import zipfile

from setup_new_linux.classes.packagesc import Package, OsPackage, GuiOsPackage, PipxPackage
from setup_new_linux.classes.servicesc import SystemDService
from setup_new_linux.classes import package_managers as PM
from setup_new_linux.dotfiles import ranger_pkg

from setup_new_linux.utils import constants as C
from setup_new_linux.utils.constants import CheckInstallationBy as Cib
from setup_new_linux.utils.helpers import run_cmd, check_if_cmd_present
from setup_new_linux.utils.setup import log
from setup_new_linux import info


class YayOsPackage(OsPackage):

    def __init__(self):
        super().__init__(
            'yay',
            distros={
                'default': None,
                C.Distro.manjaro: 'yay',
            },
        )

    def configure(self) -> None:
        PM.os_pkg = PM.get_os_pkg_manager()
        for pkg in packages:
            if pkg == PM.pacman:
                pkg.pkg_manager = PM.os_pkg

yay = YayOsPackage()


sshd = OsPackage(
    'sshd',
    pkg_name='openssh',
)

base_devel = OsPackage(
    'base-devel',
    cmd_name='gcc',
    distros={
        'default': None,
        C.Distro.manjaro: 'base-devel',
    },
)


# class VimOsPackage(OsPackage):
#
#     def __init__(self):
#         super().__init__(
#             'vim',
#             distros={
#                 C.Distro.manjaro: 'gvim',
#             },
#             groups=C.Groups.cli | C.Groups.home | C.Groups.work | C.Groups.server,
#         )
# vim = VimOsPackage()
vim = OsPackage(
    'vim',
    distros={
        C.Distro.manjaro: 'gvim',
    },
    groups=C.Groups.cli | C.Groups.home | C.Groups.work | C.Groups.server,
)


# TODO: change to manual install (download binary)
telegram = GuiOsPackage(
    'telegram-desktop',
    check_install_by=Cib.any,
    cmd_name='Telegram',
    file_locations={
        '/home/kossak/apps/Telegram/Telegram',
    },
)

google_chrome = GuiOsPackage(
    'google-chrome',
    check_install_by=Cib.pkg,
    cmd_name='chrome'
)

class AsdfPackage(Package):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._py_versions = None

    def install(self):
        run_cmd(shlex.split(f'git clone https://github.com/asdf-vm/asdf.git {C.ASDF_DIR}'))
        p = run_cmd(
            'git tag --list --sort v:refname',
            cwd=C.ASDF_DIR,
            stdout=subprocess.PIPE,
        )

        newest_tag = '0'
        newest_ver = Version(newest_tag)
        for vstr in p.stdout.strip().splitlines():
            v = Version(vstr)
            if v > newest_ver:
                newest_ver = v
                newest_tag = vstr

        # checkout asdf git tag:
        msg = f'ASDF git tag set: {newest_tag}'
        info.verify.append(msg)
        log.info(msg)
        run_cmd(
            ['git', 'checkout', newest_tag],
            cwd=C.ASDF_DIR,
        )

        run_cmd(
            [C.ASDF_BINARY_PATH, 'plugin-add', 'python'],
        )

        all_latest_versions = ' - '.join(v.public for v in sorted(self.py_versions.values(), reverse=True))
        msg = f'asdf python latest versions: {all_latest_versions}'
        log.info(msg)
        info.verify.append(msg)
        # info.verify.append(f'asdf install python {self.py_versions[self.install_latest_python_branch]}')
        self.install_main_python()
        info.verify.append(f'asdf installed python: {C.MAIN_PYTHON_VERSION}')

    @property
    def py_versions(self):
        if not self._py_versions:
            # Update self._py_versions
            # Get only latest version for each minor version
            p = run_cmd(
                f'{C.ASDF_BINARY_PATH} list-all python',
                stdout=subprocess.PIPE,
            )
            py_versions = {}  # {'3.11': <Version 3.11.1>}
            for py in re.finditer(r'^(\d+)\.(\d+)\.(\d+)$', p.stdout, re.MULTILINE):
                v = Version(py.group())
                if v <= Version('3.6.6'):
                    continue
                branch = '.'.join(str(e) for e in v.release[:2])

                if v > py_versions.setdefault(branch, v):
                    py_versions[branch] = v

            self._py_versions = py_versions
        return self._py_versions

    def install_main_python(self) -> None:
        self.install_python_version(C.MAIN_PYTHON_VERSION)
        run_cmd(
            [C.ASDF_BINARY_PATH, 'global', 'python', C.MAIN_PYTHON_VERSION],
            cwd=str(Path.home()),
        )
        run_cmd([
                C.PYTHON_BINARY_MAIN_PATH, '-m', 'pip', 'install', '-U',
                'pip', 'setuptools', 'wheel',  # needed if you have older tools
                'pkgconfig',  # eg: for borgbackup
            ],
            cwd=str(Path.home()),
        )

    def install_python_version(self, version) -> None:
        # TODO: maybe run it in background and check when it ends?

        python_binary_path = Path(C.PYTHON_BINARY_PATH_TEMPLATE.format(version=version))
        if python_binary_path.exists():
            log.debug(f'Asdf python already installed: {version}')
            return
        log.info(f'Asdf install python: {version}')
        run_cmd(
            [C.ASDF_BINARY_PATH, 'install', 'python', version]
        )
        run_cmd(
            [python_binary_path, '-m', 'pip', 'install', '-U', 'pip', 'pdir2'],
        )

asdf = AsdfPackage(
    'asdf',
    check_install_by=Cib.files_any,
    file_locations=(
        Path.home() / '.asdf',
    )
)


pipx = Package(
    'pipx',
    check_install_by=Cib.files_any,
    file_locations=(
        Path.home() / '.local/bin/pipx',
    ),
    install_cmd=[C.PYTHON_BINARY_MAIN_PATH, '-m', 'pip', 'install', '-U', '--user', 'pipx'],
)


xonsh = PipxPackage(
    'xonsh',
    pkg_names_to_install='xonsh[full]',
    inject='tabulate pdir2 pendulum xontrib-fzf-widgets xontrib-argcomplete xontrib-broot',
)

class EmacsOsPackage(OsPackage):
    def configure(self):
        # git clone https://github.com/syl20bnr/spacemacs ~/.emacs.d
        # TODO: put ready .emacs.d/ on pendrive
        run_cmd(['git', 'clone', 'https://github.com/syl20bnr/spacemacs', str(Path.home() / '.emacs.d')])
        info.verify.append('Run emacs to finish installing spacemacs')

emacs = EmacsOsPackage('emacs')
pamac = OsPackage(
    'pamac',
    distros={
        'default': None,
        C.Distro.manjaro: 'pamac-cli',
    }
)


class PoetryPipxPackage(PipxPackage):
    def configure(self):
        run_cmd([str(Path.home() / '.local/bin/poetry'), 'config', 'virtualenvs.prefer-active-python', 'true'])
        run_cmd([str(Path.home() / '.local/bin/poetry'), 'self', 'add', 'poetry-plugin-up'])

poetry = PoetryPipxPackage('poetry')


class BitWarden(Package):

    def __init__(self):
        super().__init__(
            'bitwarden',
            cmd_name='bw',
        )

    def install(self):
        log.info(f'Download and install: {self.name}')
        url = 'https://vault.bitwarden.com/download/?app=cli&platform=linux'
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "python-urllib",
        }
        req = urllib.request.Request(url, None, headers)
        with urllib.request.urlopen(req) as f:
            zip_data = BytesIO(f.read())
        zf = zipfile.ZipFile(zip_data)
        file_data = zf.open('bw').read()
        p = Path.home() / '.local/bin/bw'
        p.write_bytes(file_data)
        p.chmod(0o755)
        info.pkg_installed.append(self.name)

    def is_unlocked():
        # TODO: finish
        ...



bitwarden = BitWarden()


class VpnCiscoAnyConnect(Package):

    def __init__(self):
        super().__init__(
            'CiscoAnyConnect',
            cmd_name='vpn',
        )

    def install():
        # TODO: finish
        ...


packages = [
    # prod:
    base_devel, 'cmake',
    # openssl - ??? (included in base_devel)
    yay,
    pamac,
    OsPackage('curl', groups=C.Groups.cli | C.Groups.home | C.Groups.work | C.Groups.server),
    OsPackage('wget', groups=C.Groups.cli | C.Groups.home | C.Groups.work | C.Groups.server),
    OsPackage('git', groups=C.Groups.cli | C.Groups.home | C.Groups.work | C.Groups.server),
    vim,
    sshd,
    emacs,
    'tmux', 'pass', 'fd', OsPackage('ripgrep', cmd_name='rg'),
    OsPackage('zstd'),
    'exa', 'xsel', 'xclip',
    'gocryptfs', 'mtr', 'dos2unix', 'ethtool', 'ncdu',
    asdf, pipx, xonsh, ranger_pkg, poetry,
    # needed fo vscode xonsh e poetryn:
    PipxPackage('glances', inject='py-cpuinfo netifaces hddtemp python-dateutil'),
    PipxPackage('python-lsp-server', pkg_names_to_install='python-lsp-server[all]'),
    PipxPackage('pypiserver'),
    PipxPackage(
        'borgbackup',
        pkg_names_to_install=[
            'borgbackup[fuse]',
            'borgbackup[pyfuse3]',  # newer than llfuse
            'borgbackup[llfuse]',   # older
        ]
    ),
    PipxPackage('ps-mem'),
    PipxPackage('yt-dlp'),
    PipxPackage('visidata'),
    PipxPackage('magic-wormhole'),
    # TODO: copy pypi_packages to pendrive
    # TODO: pipxil kossak_cli_tools
    # TODO: pipxil  kossakhome

    OsPackage('gnu-netcat', cmd_name='netcat'),
    OsPackage('bind-tools', cmd_name='dig'),
    bitwarden,

    # GUI:
    GuiOsPackage('mpv'),
    GuiOsPackage('seahorse'),
    GuiOsPackage('vscode', pkg_name='visual-studio-code-bin', cmd_name='code'),
    # telegram,
    google_chrome,
]

for i, p in enumerate(packages):
    if isinstance(p, str):
        pkg = OsPackage(p)
        packages[i] = pkg
