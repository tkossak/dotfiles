from pathlib import Path
from typing import List, Tuple
from itertools import chain
import os
import subprocess

from setup_new_linux.utils import constants as C, helpers as H
from setup_new_linux.utils.setup import log
from setup_new_linux.classes.dotfilesc import Dotfile

from setup_new_linux import (
    info,
    dotfiles,
    packages,
    services,
)


def os_update_mirrors_and_repos(dry_run: bool = False):
    if dry_run:
        print('dry run: os_update_mirrors_and_repos')
        return

    log.info(f'START os update repos: {info.distro.value}')
    if info.distro == C.Distro.manjaro:
        log.info('Setup manjaro/pacman mirrors')
        H.run_cmd('sudo pacman-mirrors -c Poland,Germany')

        log.info('Update pacman repos')
        H.run_cmd('sudo pacman -Syy')
    elif info.distro == C.Distro.ubuntu:
        log.info('Setup ubuntu repos')
        H.run_cmd('sudo apt clean && sudo apt update')
        # sudo apt upgrade -y && sudo apt install

    else:
        msg = f'NOT updating repos: unknown distro: {info.distro.value}'
        log.warning(msg)
        info.errors.append(msg)


def configure_ssh(dry_run: bool = False):
    if dry_run:
        print('dry run: configure_ssh')
        return
    log.info('configure ssh')
    packages.sshd.install_if_not_installed()
    services.sshd.set_presence()
    if services.sshd.is_present:
        services.sshd.enable()
        services.sshd.start()
    else:
        msg = "Not starting sshd service: can't find it"
        log.error(msg)
        info.errors.append(msg)


def configure_ntpdate(dry_run: bool = False):
    if dry_run:
        print('dry run: configure_ntpdate')
        return
    log.info('configure ntpdate')
    H.run_cmd('systemctl start ntpdate.service')
    H.run_cmd('systemctl enable ntpdate.service')


def create_kossak_links(dry_run: bool = False):
    if dry_run:
        print('dry run: create_kossak_links')
        return

    log.info('Configure Kossak/links')
    hh = Path.home()
    kl = hh / 'Kossak/links'
    kl_desktop_shortcuts = kl / 'desktop_shortcuts'
    kl_systemd = kl / 'systemd'
    kl_steam = kl / 'steam'

    links_to_create: List[Tuple[Path, Path]] = []  # DST, SRC

    # different links
    links_to_create.extend((
        (kl / 'poetry_venv', hh / '.cache/pypoetry/virtualenvs'),
        (kl / 'pipx_venv'  , hh / '.local/pipx/venvs'),
        (kl / 'pipenv_venv', hh / '.local/share/virtualenvs'),
        (kl / 'pipsi_venv' , hh / '.local/venvs'),
        (kl_desktop_shortcuts / 'usr_share_applications'       , Path('/usr/share/applications')),
        (kl_desktop_shortcuts / 'home_local_share_applications', hh / '.local/share/applications'),
        (kl_desktop_shortcuts / 'home_config_autostart'        , hh / '.config/autostart'),
    ))

    # gaming links
    steam_libraries = {
        'main': hh / '.local/share/Steam',  # main is where 'userdata' and 'steamapps' folders are
        'second': Path('/mnt/data_lin/steam_games'),  # additional libraries. No 'userdata' folder here, but there's 'steamapps' folder
    }
    for name_prefix, relative_dir in (
        ('steam_common', 'steamapps/common'),
        ('steam_compatdata', 'steamapps/compatdata'),
    ):
        for name_suffix, steam_root_folder in steam_libraries.items():
            links_to_create.append((
                kl_steam / f'{name_prefix}_{name_suffix}',
                steam_root_folder / relative_dir
            ))

    # gaming links in steam folder
    for name_suffix, game_id in (
        ('No_Mans_Sky', '275850'),
    ):
        for _, steam_root_folder in steam_libraries.items():
            links_to_create.append((
                steam_root_folder / f'steamapps/compatdata/{game_id}_{name_suffix}',
                steam_root_folder / f'steamapps/compatdata/{game_id}',
            ))

    # links for steam user ids:
    if 'steam_user_ids' in info.dotfiles_local_config:
        for user_id, user_name in info.dotfiles_local_config['steam_user_ids'].items():
            # 2 links to user folder:
            links_to_create.extend((
                (  # link in Kossak
                    kl_steam / f'steam_userdata_{user_name}',
                    steam_libraries['main'] / f'userdata/{user_id}'
                ),
                (  # link in steam folder
                    steam_libraries['main'] / f'userdata/{user_id}_{user_name}',
                    steam_libraries['main'] / f'userdata/{user_id}'
                ),
            ))
            # inside user folder, links to app ids:
            for app_id, app_name in (
                ('241100', 'controller'),
            ):
                links_to_create.append((
                    steam_libraries['main'] / f'userdata/{user_id}/{app_id}_{app_name}_{user_name}',
                    steam_libraries['main'] / f'userdata/{user_id}/{app_id}'
                ))

    # systemd
    systemd_folders_to_search = {
        '/etc/systemd/system',
        '/etc/systemd/system.control',
        '/etc/systemd/user',
        '/run/systemd/generator',
        '/run/systemd/generator.early',
        '/run/systemd/generator.late',
        '/run/systemd/system',
        '/run/systemd/system.control',
        '/run/systemd/transient',
        '/run/systemd/user',
        '/usr/lib/systemd/system',
        '/usr/lib/systemd/user',
        '/usr/local/lib/systemd/system',
        '/usr/local/lib/systemd/user',
        '$HOME/.config/systemd/user',
        '$HOME/.local/share/systemd/user',
    }
    for var in ('XDG_CONFIG_HOME', 'XDG_RUNTIME_DIR', 'XDG_DATA_HOME'):
        if var in os.environ and os.environ[var]:
            systemd_folders_to_search.add(
                f'{os.environ[var]}/systemd/user'
            )

    for cmd in (
        ['systemd-analyze', '--user', 'unit-paths'],
        ['systemd-analyze', '--global', 'unit-paths'],
        ['systemd-analyze', '--system', 'unit-paths'],
    ):
        folders = H.run_cmd(cmd, stdout=subprocess.PIPE)
        for p in folders.stdout.splitlines():
            systemd_folders_to_search.add(p.strip())
    for s in systemd_folders_to_search:
        link_name = s.replace('$HOME', 'home').lstrip('/').replace('/', '_')
        s = s.replace('$HOME', str(Path.home()))
        links_to_create.append((
            kl_systemd / link_name,
            Path(s),
        ))

    # yay/pacman packages:
    links_to_create.extend((
        (kl / 'manjaro_pkgs/yay', hh / '.cache/yay/'),
        (kl / 'manjaro_pkgs/pacman', '/var/cache/pacman/pkg'),
    ))


    # create all links
    for link, file in links_to_create:
        if isinstance(link, str):
            link = Path(link)
        if isinstance(file, str):
            file = Path(file)
        if file.exists():
            if link.exists() and link.is_symlink():
                link.unlink()
            link.parent.mkdir(parents=True, exist_ok=True)
            link.symlink_to(file)


def make_dotfiles_bin_executable(dry_run: bool = False):
    if dry_run:
        print('dry run: make_dotfiles_bin_executable')
        return
    log.info('Make dotfiles bin executable')
    dotfiles_bin_dir = info.dotfiles_dir.parent / 'bin'
    dotfiles_local_bin_dir = info.dotfiles_local_dir.parent / 'bin'
    for f in chain(
        dotfiles_bin_dir.glob('*'),
        dotfiles_local_bin_dir.glob('*'),
    ):
        f.chmod(0o700)

def install_kde_autostart_scripts(dry_run: bool = False):
    if dry_run:
        print('dry run: install_kde_autostart_scripts')
        return
    log.info('Install kde autostart scripts')
    kde_startup_dir = Path.home() / '.config/autostart'
    kde_startup_src_dir = info.dotfiles_dir.parent / 'autostart_desktop_shortcuts'

    msg = None
    if not kde_startup_dir.exists():
        msg = f'KDE startup dir does not exist: {kde_startup_dir}'
        log.error('msg')
        info.errors.append(msg)
        return
    if not kde_startup_src_dir.exists():
        msg = f'KDE startup source dir does not exist: {kde_startup_src_dir}'
        log.error('msg')
        info.errors.append(msg)
        return

    for f in kde_startup_src_dir.glob('*.desktop'):
        Dotfile(
            src=f,
            dst=kde_startup_dir / f.name,
        ).install()





def configure_spacemacs():
    ...


def configure_gocryptfs():
    ...
    # 'gocryptfs'


def enable_date_time_sync():
    ...


