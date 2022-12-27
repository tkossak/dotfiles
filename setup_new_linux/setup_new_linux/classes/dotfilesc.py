from pathlib import Path
from typing import Union
import time
import shutil

from setup_new_linux.utils.setup import log
from setup_new_linux.utils import helpers as H


class Dotfile:

    def __init__(
        self,
        src: Union[str, Path] = None,
        dst: Union[str, Path] = None,
        name: str = '',
        mode: str = 'link',  # 'copy'
        f_backup_first: bool = True,
        f_raise_if_src_doesnt_exist: bool = True,
        remove_dst_if_it_exists: bool = True,
    ):
        """Dotfile to link or copy
        :param src: source file
        :param dst: destination file
        :param name: nice name, only for __repr__
        :param mode: link or copy file
        :param f_backup_first: if dst already exists, back it up first
        :param f_raise_if_src_doesnt_exist:
        """
        self.remove_dst_if_it_exists = remove_dst_if_it_exists
        self.src = Path(src) if src else None
        self.dst = Path(dst) if dst else None
        self.name = name or self.src.name
        if mode not in ('link', 'copy'):
            raise Exception(f'Wrong mode: {mode}')
        self.mode = mode
        self.f_backup_first = f_backup_first
        self.f_raise_if_src_doesnt_exist = f_raise_if_src_doesnt_exist
        self.installed = False

    def _install(self):
        if self.mode == 'link':
            self.dst.symlink_to(self.src)
            log.info(f'dotfile linked: {self.src.name} ==to== {self.dst}')
        else:  # copy mode
            shutil.copy(self.src, self.dst)
            log.info(f'dotfile copied: {self.src.name} ==to== {self.dst}')

    def install(self):
        if self.installed:
            log.debug(f'dotfile already installed: {self.src.name}')
            return

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

        if self.remove_dst_if_it_exists and self.dst.exists():
            if self.f_backup_first and not self.dst.is_symlink():
                log.info(f'Dotfile backing up: {self.dst}')
                self.dst.rename(f'{self.dst}.old_{time.strftime("%Y%m%d_%H%M%S")}')

            if self.dst.is_dir():
                shutil.rmtree(self.dst)
            else:
                self.dst.unlink()

        # create link:
        self._install()
        self.installed = True

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.name}>'

class LocalDotfile(Dotfile):
    """Dotfile that is not logged to info.errors
    """


class ReplaceSnippetDotfile(Dotfile):
    def __init__(self,
        start_line: str = None,
        end_line: str = None,
        sudo: bool = False,
        **kwargs,
    ):
        """Insert or replace snippet in `dst` file, instead of linking whole file
        :param src: file containing snippet to insert
        :param dst: insert (or replace) snippet in into file
        :param start_line: snippet begins with this string
        :param end_line: snippet ends with this string
        """
        kwargs['remove_dst_if_it_exists'] = False
        super().__init__(**kwargs)
        self.start_line = start_line
        self.end_line = end_line
        self.sudo = sudo
        self.installed = False


    def install(self):
        if self.installed:
            log.debug(f'dotfile already installed: {self.src.name}')
            return
        my_snippet = self.src.read_text()
        if H.insert_or_replace_snippet(
            snippet=my_snippet,
            file=self.dst,
            start_line=self.start_line,
            end_line=self.end_line,
            sudo=self.sudo,
        ):
            log.info(f'Snippet installed in {self.dst}')
        else:
            log.debug(f'Snippet already installed in {self.dst}')
        self.installed = True
