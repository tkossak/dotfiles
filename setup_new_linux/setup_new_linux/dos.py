from setup_new_linux.utils.setup import log
# from setup_new_linux.helpers import check_if_cmd_presentun_cmd
from setup_new_linux.classes.servicesc import SystemDService
from setup_new_linux import info


def enable_and_start_sshd():
    if not info.systemd:
        log.error("Can't enable sshd, because os doesn't use systemd")
        info.errors.append("sshd: not systemd present")

    log.info('Configure: sshd')
    sshd = SystemDService('sshd')
    if not sshd.is_available:
        log.error('sshd NOT installed!')
        return
    sshd.enable()
    sshd.start()

def create_Kossak_links():
    # WIP
    ...

def install_asdf():
    ...

def install_pipx():
    ...

def configure_python():
    ...

def configure_spacemacs():
    ...


def configure_secrets():
    ...
    # import gpg keys


def configure_gocryptfs():
    ...
    # 'gocryptfs'


def enable_date_time_sync():
    ...
