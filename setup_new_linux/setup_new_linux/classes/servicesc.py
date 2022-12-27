import subprocess
from subprocess import run

from setup_new_linux.utils import helpers as H  ##import check_if_cmd_present
from setup_new_linux import info


class SystemDService:

    def __init__(self, service):
        self.service_name = f'{service}.service'
        self.is_present = self.check_if_service_present()
        if not H.check_if_cmd_present('systemctl'):
            raise Exception('Systemctl is not present on this system')

    def check_if_service_present(self) -> bool:
        """Checked only once, during object creation
        """
        if not info.systemd:
            return False
        # full_name = f'{self.service}.service'
        p = H.run_cmd(
            ['systemctl', 'list-units', '--full', '--all', '--no-legend', '--no-pager', self.service_name],
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
        if p.stdout:
            return True
        else:
            return False

    def set_presence(self):
        self.is_present = self.check_if_service_present()

    @property
    def is_active(self) -> bool:
        """Is this service currently running?
        """
        if self.is_present:
            p = run(['systemctl', 'is-active', '--quiet',self.service_name])
            return not bool(p.returncode)
        else:
            return False

    @property
    def is_enabled(self) -> bool:
        """Is this service set to start on system startup?
        """
        if self.is_present:
            p = run(['systemctl', 'is-enabled', '--quiet',self.service_name])
            return not bool(p.returncode)
        else:
            return False

    def enable(self):
        """Eanble service to be started at system startup
        """
        if self.is_present and not self.is_enabled:
            run(['systemctl', 'enable', self.service_name], check=True)

    def start(self):
        """Start service now
        """
        if self.is_present and not self.is_active:
            run(['systemctl', 'start', self.service_name], check=True)


