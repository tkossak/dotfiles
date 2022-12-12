from pathlib import Path
from typing import Union
import time
import shutil

from setup_new_linux.utils.setup import log


class Dotfile:

    def __init__(
        self,
        src: Union[str, Path],
        dst: Union[str, Path],
        mode: str = 'link',  # 'copy'
        f_backup_first: bool = True,
        f_raise_if_src_doesnt_exist: bool = True,
    ):
        """Dotfile to link or copy
        :param src: source file
        :param dst: destination file
        :param mode: link or copy file
        :param f_backup_first: if dst already exists, back it up first
        """
        self.src = Path(src)
        self.dst = Path(dst)
        if mode not in ('link', 'copy'):
            raise Exception(f'Wrong mode: {mode}')
        self.mode = mode
        self.f_backup_first = f_backup_first
        self.f_raise_if_src_doesnt_exist = f_raise_if_src_doesnt_exist

    def install(self):

        # check src existence
        if not self.src.exists():
            if self.f_raise_if_src_doesnt_exist:
                raise Exception(f"dotfile: src doesn't exist: {self.src}")
            else:
                log.info(f"dotfile: src doesn't exist: {self.src}")
                return

        # create parent dir  # check dst parent dir existance
        if not self.dst.parent.exists():
            self.dst.parent.mkdir(parents=True)
            # raise Exception(f"dotfile: parent dir of dst doesn't exist, dst: {self.dst}")

        if self.dst.is_symlink():
            self.dst.unlink()

        # if dst exists - backup or remove
        if self.dst.exists():
            if self.f_backup_first:
                if not self.dst.is_symlink():  # we don't backup symlinks
                    log.info(f'Dotfiles: backing up: {self.dst}')
                    self.dst.rename(f'{self.dst}.old_{time.strftime("%Y%m%d_%H%M%S")}')
            else:
                if self.dst.is_dir():
                    shutil.rmtree(self.dst)
                else:
                    self.dst.unlink()

        # create link:
        if self.mode == 'link':
            self.dst.symlink_to(self.src)
            log.info(f'dotfile linked: {self.src.name} ==to== {self.dst}')
        else:  # copy mode
            shutil.copy(self.src, self.dst)
            log.info(f'dotfile copied: {self.src.name} ==to== {self.dst}')
