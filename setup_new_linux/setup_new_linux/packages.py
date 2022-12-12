from pathlib import Path
from setup_new_linux.classes.packagesc import OsPackage
from setup_new_linux.utils.constants import Distro, CheckInstallationBy as Cib
from setup_new_linux.utils.helpers import run_cmd
from setup_new_linux.utils.setup import log

yay = OsPackage('yay')

def vim_configure():
    vimplug_path = Path.home() / '.vim/autoload/plug.vim'
    if not vimplug_path.exists():
        run_cmd(['curl', '-fLo', str(vimplug_path), '--create-dirs', 'https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'])
        log.info('REMEMBER vim: run vim and :PlugInstall')
        # TODO: run automatic :PlugInstall after you download your dotfiles!

base_devel = OsPackage(
    'base-devel',
    cmd_name='gcc',
    distros={
        'default': None,
        Distro.MANJARO: 'base-devel',
    },
)

vim = OsPackage(
    'vim',
    configure_func=vim_configure,
    distros={
        Distro.MANJARO: 'gvim',
    },
)

# TODO: change to manual install (download binary)
telegram = OsPackage(
    'telegram-desktop',
    check_install_by=Cib.any,
    cmd_name='Telegram',
    file_locations={
        '/home/kossak/apps/Telegram/Telegram',
    },
)


Packages = [
    base_devel,
    'curl', 'wget',
    vim,
    'tmux', 'gocryptfs', 'exa', 'xsel',
    'xclip', 'tmux', 'pass', 'mtr', 'cmake', 'dos2unix', 'ethtool', 'fd',
    'seahorse',
    'mpv',
    OsPackage('gnu-netcat', cmd_name='netcat'),
    OsPackage('bind-tools', cmd_name='dig'),
    OsPackage('ripgrep', cmd_name='rg'),

    telegram,
    OsPackage('google-chrome', check_install_by=Cib.pkg, cmd_name='chrome'),
]
