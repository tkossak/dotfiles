from pathlib import Path
import shlex
import subprocess
import re
from packaging.version import Version

from setup_new_linux.classes.packagesc import OsPackage
from setup_new_linux.utils.constants import Distro, CheckInstallationBy as Cib, Groups
from setup_new_linux.utils.helpers import run_cmd, check_if_cmd_present
from setup_new_linux.utils.setup import log
from setup_new_linux import info

yay = OsPackage('yay')

base_devel = OsPackage(
    'base-devel',
    cmd_name='gcc',
    distros={
        'default': None,
        Distro.MANJARO: 'base-devel',
    },
)

class VimOsPackage(OsPackage):
    def configure(self):
        vimplug_path = Path.home() / '.vim/autoload/plug.vim'
        if not vimplug_path.exists():
            run_cmd(['curl', '-fLo', str(vimplug_path), '--create-dirs', 'https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'])
            log.info('REMEMBER vim: run vim and :PlugInstall')
            # TODO: run automatic :PlugInstall after you download your dotfiles!

vim = VimOsPackage(
    'vim',
    distros={
        Distro.MANJARO: 'gvim',
    },
)

# TODO:
# ranger = ...

# TODO: change to manual install (download binary)
telegram = OsPackage(
    'telegram-desktop',
    # groups=Groups.gui | Groups.home | Groups.work,
    groups=Groups(0),  # temporarily disable installing
    check_install_by=Cib.any,
    cmd_name='Telegram',
    file_locations={
        '/home/kossak/apps/Telegram/Telegram',
    },
)

google_chrome = OsPackage(
    'google-chrome',
    groups=Groups.gui | Groups.home | Groups.work,
    check_install_by=Cib.pkg,
    cmd_name='chrome'
)

class AsdfOsPackage(OsPackage):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.asdf_dir = Path.home() / '.asdf'
        self.asdf_binary_path = self.asdf_dir / 'bin/asdf'
        self.install_latest_python_branch = '3.10'
        self.py_versions = {}

    def install(self):
        run_cmd(shlex.split(f'git clone https://github.com/asdf-vm/asdf.git {self.asdf_dir}'))
        p = run_cmd(
            'git tag --list --sort v:refname',
            cwd=self.asdf_dir,
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
            cwd=self.asdf_dir,
        )

        run_cmd(
            [self.asdf_binary_path, 'plugin-add', 'python'],
        )

        self.download_latest_python_versions()
        all_latest_versions = ' - '.join(v.public for v in sorted(self.py_versions.values(), reverse=True))
        msg = f'Asdf python latest versions: {all_latest_versions}'
        log.info(msg)
        info.verify.append(msg)
        info.verify.append(f'asdf install python {self.py_versions[self.install_latest_python_branch]}')


    def download_latest_python_versions(self) -> None:
        """Update self.py_versions and info.verify
        Get only latest version for each minor version
        """
        if self.py_versions:
            return

        p = run_cmd(
            f'{self.asdf_binary_path} list-all python',
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

        self.py_versions = py_versions

    def install_python_version(self):
        if not self.py_versions:
            self.download_latest_python_versions()

        # TODO: finish
        # maybe do it in background?
        print('TODO install python: ', self.py_versions[self.install_latest_python_branch])


asdf = AsdfOsPackage(
    'asdf',
    check_install_by=Cib.files_any,
    file_locations=(
        Path.home() / '.asdf',
    )
)


Packages = [
    base_devel,
    'curl', 'wget', 'git',
    vim,
    'tmux', 'pass', 'fd', OsPackage('ripgrep', cmd_name='rg'),
    'exa', 'xsel', 'xclip',
    'gocryptfs', 'mtr', 'cmake', 'dos2unix', 'ethtool',
    asdf,
    'mpv',
    OsPackage('seahorse', groups=Groups.gui | Groups.home | Groups.work),
    OsPackage('gnu-netcat', cmd_name='netcat'),
    OsPackage('bind-tools', cmd_name='dig'),

    telegram,
    google_chrome,
]
