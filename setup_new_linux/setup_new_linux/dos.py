from pathlib import Path
from typing import List, Tuple

from setup_new_linux.utils import constants as C, helpers as H
from setup_new_linux.utils.setup import log

from setup_new_linux import (
    info,
    dotfiles,
    packages,
    services,
)


def os_update_mirrors_and_repos():
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


def os_configure():
    """One-time setup after installing Os
    """
    log.info(f'START os configure: {info.distro.value}')
    (Path.home() / '.local/bin').mkdir(parents=True, exist_ok=True)

    if info.distro == C.Distro.manjaro:
        # install yay:
        packages.yay.install_if_not_installed()
        dotfiles.etc_environment.install()
        dotfiles.bashrc.install()
        dotfiles.bashprofile.install()

        # SSH
        packages.sshd.install_if_not_installed()
        services.sshd.set_presence()
        if services.sshd.is_present:
            services.sshd.enable()
            services.sshd.start()
        else:
            msg = "Not starting sshd service: can't find it"
            log.error(msg)
            info.errors.append(msg)
        # TODO: secure sshd? change port, key logging, root logging, etc

        # TODO: change colors for pacman/yay
    else:
        msg = f'NOT configuring os: unknown distro: {info.distro.value}'
        log.warning(msg)
        info.errors.append(msg)


def create_kossak_links():
    log.info('Configure Kossak/links')
    hh = Path.home()
    kl = hh / 'Kossak/links'
    kl_desktop_shortcuts = kl / 'desktop_shortcuts'
    kl_systemd = kl / 'systemd'
    kl_steam = kl / 'steam'

    links_to_create: List[Tuple[Path, Path]] = []

    # different links
    links_to_create.extend((
        (kl / 'poetry_venv', hh / '.cache/pypoetry/virtualenvs'),
        (kl / 'pipx_venv'  , hh / '.local/pipx/venvs'),
        (kl / 'pipenv_venv', hh / '.local/share/virtualenvs'),
        (kl / 'pipsi_venv' , hh / '.local/venvs'),
        (kl_desktop_shortcuts / 'usr_share_applications'       , Path('/usr/share/applications')),
        (kl_desktop_shortcuts / 'home_local_share_applications', hh / '.local/share/applications'),
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
    for s in (
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
    ):
        links_to_create.append((
            kl_systemd / s.lstrip('/').replace('/', '_'),
            Path(s),
        ))

    # create all links
    for link, file in links_to_create:
        if file.exists():
            if link.exists() and link.is_symlink():
                link.unlink()
            link.parent.mkdir(parents=True, exist_ok=True)
            link.symlink_to(file)


def configure_spacemacs():
    ...


def configure_gocryptfs():
    ...
    # 'gocryptfs'


def enable_date_time_sync():
    ...


