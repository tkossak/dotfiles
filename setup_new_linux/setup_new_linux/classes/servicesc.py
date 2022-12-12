import subprocess
from subprocess import run

from setup_new_linux.utils.helpers import check_if_cmd_present


class SystemDService:

    def __init__(self, service):
        self.service = service
        self.is_available = self.get_if_installed()
        if not check_if_cmd_present('systemctl'):
            raise Exception('Systemctl is not present on this system')

    def get_if_installed(self) -> bool:
        """Checked only once, during object creation
        """
        full_name = f'{self.service}.service'
        p = run(
            ['systemctl', 'list-units', '--full', '--all', '--no-legend', '--no-pager', full_name],
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
        if p.stdout:
            return True
        else:
            return False

    @property
    def is_active(self):
        """Is this service currently running?
        """
        p = run(['systemctl', 'is-active', '--quiet',self.service])
        return not bool(p.returncode)

    @property
    def is_enabled(self):
        """Is this service set to start on system startup?
        """
        p = run(['systemctl', 'is-enabled', '--quiet',self.service])
        return not bool(p.returncode)

    def enable(self):
        """Eanble service to be started at system startup
        """
        if self.is_available and not self.is_enabled:
            run(['systemctl', 'enable', self.service], check=True)

    def start(self):
        """Start service now
        """
        if self.is_available and not self.is_active:
            run(['systemctl', 'start', self.service], check=True)


