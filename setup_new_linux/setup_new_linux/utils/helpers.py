import shutil
from typing import Union, List, Iterable
from subprocess import run
from pathlib import Path
import re
import tempfile
import os

from setup_new_linux.utils.setup import log
from setup_new_linux import info


def check_if_cmd_present(cmd: str) -> bool:
    """return True if given app is present in $PATH folders
    :param cmd: cmd name
    """
    if cmd:
        r = shutil.which(cmd)
        # return True if r else False
        return r
    return False


def run_cmd(cmd: Union[str, list], *args, **kwargs):
    """Run given cmd
    They return value is checked by default

    :param cmd: if str: run in shell
    """

    if not cmd:
        raise Exception('Empty cmd to run')

    kwargs['universal_newlines'] = True
    if isinstance(cmd, str) and 'shell' not in kwargs:
        kwargs['shell'] = True

    p = run(cmd, *args, **kwargs, )
    if 'check' not in kwargs:
        p.check_returncode()
    return p


def do_regexp_replaces(
    text: str,
    replaces: Iterable[Union[str, re.Pattern]]
) -> str:
    for o, n in replaces:
        prev_text = text
        if isinstance(o, str):
            text = text.replace(o, n)
        elif isinstance(o, re.Pattern):
            text = o.sub(n, text)
        else:
            raise Exception('Wrong type of replace object: {type(o)}')
        if prev_text == text:
            msg = f"text wasn't found/replaced: {o}"
            log.warning(msg)
            info.errors.append(f'Warning: {msg}')
    return text


def replace_file_with_text(
    text: str,
    dst: Union[Path, str],
    sudo: bool = False,
):
    """
    :param text: text to insert into dst file (instead of its content)
    :param dst: dst file
    :param sudo: use sudo
    """
    dst = Path(dst)
    if sudo:
        with tempfile.NamedTemporaryFile(
            mode='wt',
            delete=False,
        ) as tf:
            tf.file.write(text)

        replace_file_with_file(
            src=tf.name,
            dst=dst,
            sudo=sudo,
        )
    else:
        dst.write_text(text)


def replace_file_with_file(
    src: Union[Path, str],
    dst: Union[Path, str],
    sudo: bool = False,
):
    """Move src to dst, keeping the same owner and permissions

    :param src: source file (to copy/move to dst file)
    :param dst: copy src file here
    :param sudo: use sudo
    """
    src = Path(src)
    dst = Path(dst)
    if not src.exists():
        raise Exception(f'File does not exist: {src}')

    add_sudo = ['sudo'] if sudo else []
    run_cmd(add_sudo + ['chmod', '--reference', dst, src])
    run_cmd(add_sudo + ['chown', '--reference', dst, src])
    run_cmd(add_sudo + ['mv', src, dst])


def insert_or_replace_snippet(
    snippet: str,
    file: Union[str, Path],
    start_line: str = None,
    end_line: str = None,
    tag: str = None,
    sudo: bool = False,
) -> bool:
    """Insert (or replace if exists) custom snippet into any file

    Search for part in the `file` begining with `start_line` and ending with
    `end_line`. Replace this fragment with `snippet`.
    If start and end lines are not found - append snippet at the end.

    :param tag: name used in `start_line` and `end_line`
    :param sudo: if True: write to file using sudo

    :returns: True if snippet was inserted, False if not (because eg: it's
              already included)

    """
    if not tag:
        tag = 'Kossak'

    file_content = file.read_text().strip()
    if not start_line:
        start_line = f'##### START {tag} ###################################'
    if not end_line:
        end_line   = f'##### END {tag} #####################################'
    my_snippet = '\n'.join([
        f'{start_line}\n',
        snippet,
        end_line,
    ])

    if start_line in file_content and end_line in file_content:
        si = file_content.index(start_line)
        ei = file_content.index(end_line) + len(end_line)
        file_content_new = file_content[:si] + my_snippet + file_content[ei:]
    elif sum(v in file_content for v in (start_line, end_line)) == 1:
        raise('bashrc error: only start or end line exists in bashrc')
    else:
        file_content_new = f'{file_content}\n\n{my_snippet}\n'

    if file_content != file_content_new:
        replace_file_with_text(
            text=file_content_new,
            dst=file,
            sudo=sudo,
        )
#         if sudo:
#             with tempfile.NamedTemporaryFile(
#                 mode='wt',
#                 delete=False,
#             ) as tf:
#                 tf.file.write(file_content_new)
#
#             # move tmp file into original one
#             run_cmd(['sudo', 'chmod', '--reference', file, tf.name])
#             run_cmd(['sudo', 'chown', '--reference', file, tf.name])
#             run_cmd(['sudo', 'mv', tf.name, str(file)])
#
#         else:
#             file.write_text(file_content_new)
        return True
    return False