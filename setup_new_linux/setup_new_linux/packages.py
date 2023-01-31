from pathlib import Path
import shlex
import subprocess
import re
from packaging.version import Version
import os
import urllib.request
from io import BytesIO
import zipfile
import json
import shutil

from setup_new_linux.classes.packagesc import Package, OsPackage, GuiOsPackage, PipxPackage
from setup_new_linux.classes.servicesc import SystemDService
from setup_new_linux.classes import package_managers as PM
from setup_new_linux.dotfiles import ranger_pkg, tmux_pkg

from setup_new_linux.utils import (
    constants as C,
    helpers   as H
)
from setup_new_linux.utils.constants import (
    Groups as G,
    CheckInstallationBy as Cib

)
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
            groups=C.GROUPS_DEFAULT_PKG | G.liveusb,
        )

    def configure(self) -> None:
        log.info('configure yay')
        PM.os_pkg = PM.get_os_pkg_manager()
        for pkg in packages:
            if pkg == PM.pacman:
                pkg.pkg_manager = PM.os_pkg

        # TODO: change colors for pacman/yay
        pacman_conf = Path('/etc/pacman.conf')
        if not pacman_conf.exists():
            return
        pacman_conf_text = pacman_conf.read_text()
        if (
            '\nColor' not in pacman_conf_text
            and '\n#Color' in pacman_conf_text
        ):
            pacman_conf_text_new = pacman_conf_text.replace('\n#Color', '\nColor')
            H.replace_file_with_text(
                text = pacman_conf_text_new,
                dst=pacman_conf,
                sudo=True,
            )


yay = YayOsPackage()


sshd = OsPackage(
    'sshd',
    pkg_name='openssh',
    groups=C.GROUPS_DEFAULT_PKG | G.liveusb,
)

base_devel = None
if info.distro == C.Distro.manjaro:
    base_devel = OsPackage(
        'base-devel',
        # cmd_name='gcc',
        # TODO: fix: doesn't work for `distros` pkg!!!!
        pkg_names_to_check_if_installed=['pkgconf'],
        check_install_by=Cib.pkg,
    )
else:
    pass
    # different os:
    # RHEL, centos, scientific linux, fedora ::
    #   yum groupinstall "Development Tools"
    # debian based ::
    #   sudo apt-get install build-essential
    #   sudo apt-get install checkinstall


# class VimOsPackage(OsPackage):
#
#     def __init__(self):
#         super().__init__(
#             'vim',
#             distros={
#                 C.Distro.manjaro: 'gvim',
#             },
#             groups=G.cli | G.home | G.work | G.server,
#         )
# vim = VimOsPackage()
vim = OsPackage(
    'vim',
    distros={
        C.Distro.manjaro: 'gvim',
    },
    groups=C.GROUPS_DEFAULT_PKG | G.liveusb | G.server,

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
        H.run_cmd(shlex.split(f'git clone https://github.com/asdf-vm/asdf.git {C.ASDF_DIR}'))
        p = H.run_cmd(
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
        H.run_cmd(
            ['git', 'checkout', newest_tag],
            cwd=C.ASDF_DIR,
        )

        H.run_cmd(
            [C.ASDF_BINARY_PATH, 'plugin-add', 'python'],
        )

    def configure(self):
        log.info('configure asdf')
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
            p = H.run_cmd(
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
        H.run_cmd(
            [C.ASDF_BINARY_PATH, 'global', 'python', C.MAIN_PYTHON_VERSION],
            cwd=str(Path.home()),
        )
        H.run_cmd([
                C.PYTHON_ASDF_BINARY_MAIN_PATH, '-m', 'pip', 'install', '-U',
                'pip', 'setuptools', 'wheel',  # needed if you have older tools
                'pkgconfig',  # eg: for borgbackup
            ],
            cwd=str(Path.home()),
        )

    def install_python_version(self, version) -> None:
        # TODO: maybe run it in background and check when it ends?

        python_binary_path = Path(C.PYTHON_ASDF_BINARY_PATH_TEMPLATE.format(version=version))
        if python_binary_path.exists():
            log.debug(f'Asdf python already installed: {version}')
            return
        log.info(f'Asdf install python: {version}')
        H.run_cmd(
            [C.ASDF_BINARY_PATH, 'install', 'python', version]
        )
        H.run_cmd(
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
    groups=C.GROUPS_DEFAULT_PKG | G.liveusb | G.pipx,
)


xonsh = PipxPackage(
    'xonsh',
    # pkg_names_to_install='xonsh[full]',
    pkg_names_to_install='xonsh[full]==0.12.6',  # because 0.13.* have tmux+xonsh+ranger cwd problem when splitting panes
    inject='tabulate pdir2 pendulum xontrib-fzf-widgets xontrib-argcomplete xontrib-broot',
    groups=C.GROUPS_DEFAULT_PKG | G.liveusb,
)

class EmacsOsPackage(OsPackage):

    def __init__(self):
        super().__init__(
            'emacs',
            # groups=C.GROUPS_DEFAULT_PKG | G.liveusb,
        )

    def configure(self):
        log.info('configure (spac)emacs')
        # git clone https://github.com/syl20bnr/spacemacs ~/.emacs.d
        # TODO: copy .emacs from Kossak_pendrive if it exists
        H.run_cmd(['git', 'clone', 'https://github.com/syl20bnr/spacemacs', str(Path.home() / '.emacs.d')])
        info.verify.append('Run emacs to finish installing spacemacs')

emacs = EmacsOsPackage()

pamac = OsPackage(
    'pamac',
    distros={
        'default': None,
        C.Distro.manjaro: 'pamac-cli',
    },
    groups=C.GROUPS_DEFAULT_PKG | G.liveusb,
)

class PoetryPipxPackage(PipxPackage):
    def configure(self):
        log.info('configure poetry')
        H.run_cmd([str(Path.home() / '.local/bin/poetry'), 'config', 'virtualenvs.prefer-active-python', 'true'])
        H.run_cmd([str(Path.home() / '.local/bin/poetry'), 'self', 'add', 'poetry-plugin-up'])

poetry = PoetryPipxPackage('poetry')


# If it throws cipher/ssl/dso error:
# commount out: providers = provider_sect in /etc/ssl/openssl.cnf
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

    @property
    def is_unlocked(self) -> False:
        r = H.run_cmd(
            ['bw', 'status'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        j = json.loads(r.stdout)
        if 'status' in j and j['status'] == 'unlocked':
                return True
        return False


bitwarden = BitWarden()


# class ObsidianOsPackage(OsPackage):
#
#     def __init__(self):
#         super().__init__(
#             'obsidian',
#             groups=C.Groups.gui | C.Groups.home | C.Groups.work | G.liveusb,
#         )

# TODO: during installation make separate exception for configure function
obsidian = OsPackage(
    'obsidian',
    groups=C.GROUPS_DEFAULT_PKG | C.Groups.gui | C.Groups.liveusb,
)


class VpnCiscoAnyConnect(Package):

    def __init__(self):
        super().__init__(
            'CiscoAnyConnect',
            cmd_name='vpn',
        )

    def install():
        # TODO: finish
        ...


# TODO: change to manual install (download binary)
telegram = GuiOsPackage(
    'telegram-desktop',
    check_install_by=Cib.any,
    cmd_name='Telegram',
    file_locations={
        Path.home() / 'apps/Telegram/Telegram',
    },
    groups=G.home | G.work
)

class Telegram(GuiOsPackage):

    def __init__(self):
        super().__init__(
            'telegram',
            cmd_name='Telegram',
            pkg_name='telegram-desktop',
            check_install_by=Cib.any,
            file_locations=(
                '/home/kossak/apps/Telegram/Telegram',
            ),
        )

    def install(self):
        url = 'https://telegram.org/dl/desktop/linux'
        headers = {
            "User-Agent": "python-urllib",
        }
        req = urllib.request.Request(url, None, headers)
        with urllib.request.urlopen(req) as f:
            tar_xz_data = BytesIO(f.read())
        # TODO: finish
        # zf = zipfile.ZipFile(zip_data)
        # file_data = zf.open('bw').read()
        # p = Path.home() / '.local/bin/bw'
        # p.write_bytes(file_data)
        # p.chmod(0o755)
        # info.pkg_installed.append(self.name)


packages = []

if base_devel:
    packages.append(base_devel)

packages.extend((
    'pkgconf',  # should be in base_devel
    'make',     # should be in base_devel
    'cmake',    # should be in base_devel
    # openssl - ??? (included in base_devel)
    yay,
    pamac,
    OsPackage('curl', groups=C.GROUPS_DEFAULT_PKG | G.server),
    OsPackage('wget', groups=C.GROUPS_DEFAULT_PKG | G.server),
    OsPackage('git', groups=C.GROUPS_DEFAULT_PKG | G.liveusb | G.server),
    'jq',
    vim,
    sshd,
    emacs,
    'tidy',
    tmux_pkg,
    'pass',
    OsPackage('fd', groups=C.GROUPS_DEFAULT_PKG | G.liveusb),
    OsPackage(
        'ripgrep',
        cmd_name='rg',
        groups=C.GROUPS_DEFAULT_PKG | G.liveusb,
    ),
    OsPackage('zstd'),
    OsPackage(
        'exa',
        groups=C.GROUPS_DEFAULT_PKG | G.liveusb,
    ),
    OsPackage(
        'xsel',
        groups=C.GROUPS_DEFAULT_PKG | G.liveusb,
    ),
    OsPackage(
        'xclip',
        groups=C.GROUPS_DEFAULT_PKG | G.liveusb,
    ),
    'gocryptfs', 'mtr', 'dos2unix', 'ethtool', 'ncdu',
    asdf, pipx, xonsh, ranger_pkg, poetry,
    bitwarden,
    PipxPackage('glances', inject='py-cpuinfo netifaces hddtemp python-dateutil'),

    # needed fo vscode xonsh and poetry:
    PipxPackage('python-lsp-server', pkg_names_to_install='python-lsp-server[all]'),

    PipxPackage('pypiserver'),
    PipxPackage(
        name='borg',
        pkg_name='borgbackup',
        cmd_name='borgbackup',
        pkg_names_to_install=[
            'borgbackup[pyfuse3]',  # newer than llfuse, works on manjaro
            'borgbackup[fuse]',
            'borgbackup[llfuse]',   # older
        ],
        # groups=C.GROUPS_DEFAULT_PKG | G.liveusb,
    ),
    PipxPackage('ps-mem'),
    PipxPackage('yt-dlp'),
    PipxPackage('visidata'),
    PipxPackage('magic-wormhole'),
    # TODO: copy pypi_packages to pendrive
    # TODO: pipxil kossak_cli_tools
    # TODO: pipxil  kossakhome

    OsPackage(
        'gnu-netcat',
        cmd_name='netcat',
        # groups=C.GROUPS_DEFAULT_PKG | G.liveusb,
    ),
    OsPackage('bind-tools', cmd_name='dig'),
    'xcape', 'mosh',

    # GUI:
    obsidian,
    GuiOsPackage('mpv'),
    GuiOsPackage('seahorse'),
    GuiOsPackage('vscode', pkg_name='visual-studio-code-bin', cmd_name='code'),
    # telegram,
    google_chrome,
    OsPackage('plex-media-server', groups=G.gui | G.home),
))

for i, p in enumerate(packages):
    if isinstance(p, str):
        pkg = OsPackage(p)
        packages[i] = pkg
