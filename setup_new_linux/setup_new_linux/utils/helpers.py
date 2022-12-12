import shutil
from typing import Union, List
from subprocess import run
from pathlib import Path
import re

from setup_new_linux.utils.setup import log
from setup_new_linux import info


def check_if_cmd_present(cmd: str) -> bool:
    """return True if given app is present in $PATH folders
    :param cmd: cmd name
    """
    if cmd:
        r = shutil.which(cmd)
        return True if r else False
    return False


def run_cmd(cmd: Union[str, list]):
    """
    :param cmd: if str: run s shell
    """

    if cmd:
        if isinstance(cmd, str):
            p = run(
                cmd,
                shell=True
            )
        else:
            p = run(cmd)

        return p
    else:
        raise Exception('Empty cmd to run')

def do_regexp_replaces(
    text: str,
    replaces: List[str, re.Pattern]
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