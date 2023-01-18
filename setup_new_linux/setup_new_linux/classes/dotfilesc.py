from pathlib import Path
from typing import Union
import time
import shutil

from setup_new_linux import info
from setup_new_linux.utils.setup import log, args
from setup_new_linux.utils import (
    helpers as H,
    constants as C,
)


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
        dont_add_errors_to_info_if_no_locals: bool = False,
        groups: C.Groups = None,
    ):
        """Dotfile to link or copy
        :param src: source file
        :param dst: destination file
        :param name: nice name, only for __repr__
        :param mode: link or copy file
        :param f_backup_first: if dst already exists, back it up first
        :param f_raise_if_src_doesnt_exist:

        :param dont_add_errors_to_info_if_no_locals: for external functions:
            if install error occurs, do not add it to info.errors list if
            local dotfiles folder doesn't exist

        :param groups: for installing only specific groups
            At least one group from cli args must match one group from the
            dotfile, for it to be installed.
            Default: GROUPS_ALL
        """
        self.remove_dst_if_it_exists = remove_dst_if_it_exists
        self.src = Path(src) if src else None
        self.dst = Path(dst) if dst else None
        if name:
            self.name = name
        elif self.src:
            self.name = self.src.name
        else:
            self.name = self.dst.name
        if mode not in ('link', 'copy'):
            raise Exception(f'Wrong mode: {mode}')
        self.mode = mode
        self.f_backup_first = f_backup_first
        self.f_raise_if_src_doesnt_exist = f_raise_if_src_doesnt_exist
        self.dont_add_errors_to_info_if_no_locals = dont_add_errors_to_info_if_no_locals
        self.installed = False
        self.groups = groups if isinstance(groups, C.Groups) else C.GROUPS_ALL
        self.install_for_current_groups = bool(args.groups & self.groups)

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

        if not self.install_for_current_groups:
            groups_names = ', '.join(v.name for v in C.Groups if v in args.groups)
            log.debug(f"Dotfile {self.name} not installing, it doesn't match any group: {groups_names}")
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

        # broken dst link:
        if self.dst.is_symlink() and not self.dst.exists():
            self.dst.unlink()

        if self.remove_dst_if_it_exists and self.dst.exists():
            if self.f_backup_first and not self.dst.is_symlink():
                log.info(f'Dotfile backing up: {self.dst}')
                new_file_name = f'{self.dst}.old_{time.strftime("%Y%m%d_%H%M%S")}'
                self.dst.rename(new_file_name)
                info.verify.append(f'Remove old dotfile: {new_file_name}')

            if self.dst.is_dir() and not self.dst.is_symlink():
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

    def __init__(self, **kwargs):
        kwargs['dont_add_errors_to_info_if_no_locals'] = True
        super().__init__(**kwargs)


class ReplaceSnippetDotfile(Dotfile):
    def __init__(self,
        snippet: str = None,
        tag: str = None,
        sudo: bool = False,
        start_line: str = None,
        end_line: str = None,
        **kwargs,
    ):
        """Insert or replace snippet in `dst` file, instead of linking whole file
        :param src: file containing snippet to insert
        :param dst: insert (or replace) snippet in into file
        :param snippet: use this snippet. If not provide, read snippet from src file
        :param start_line: snippet begins with this string
        :param end_line: snippet ends with this string
        :param tag: name used in `start_line` and `end_line`
        """
        kwargs['remove_dst_if_it_exists'] = False
        super().__init__(**kwargs)
        self.snippet = snippet
        self.tag = tag
        self.sudo = sudo
        self.start_line = start_line
        self.end_line = end_line
        self.installed = False

    def install(self):
        if self.installed:
            log.debug(f'dotfile already installed: {self.src.name}')
            return
        elif not self.install_for_current_groups:
            groups_names = ', '.join(v.name for v in C.Groups if v in args.groups)
            log.debug(f"Dotfile {self.name} not installing, it doesn't match any group: {groups_names}")
            return

        my_snippet = self.snippet if self.snippet is not None else self.src.read_text()
        if H.insert_or_replace_snippet(
            snippet=my_snippet,
            file=self.dst,
            start_line=self.start_line,
            end_line=self.end_line,
            tag=self.tag,
            sudo=self.sudo,
        ):
            log.info(f'Snippet installed in {self.dst}')
        else:
            log.debug(f'Snippet already installed in {self.dst}')
        self.installed = True
