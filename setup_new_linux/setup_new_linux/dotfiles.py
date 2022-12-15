from pathlib import Path
import re

from setup_new_linux import info
from setup_new_linux.classes.dotfilesc import Dotfile
from setup_new_linux.utils.helpers import check_if_cmd_present, do_regexp_replaces
from setup_new_linux.utils.setup import log


dd = info.dotfiles_dir
dl = info.dotfiles_local_dir
hh = Path.home()


def get_xonsh_dotfiles():
    """Get Paths for all xonsh dotfiles
    """
    if not (Path.home() / '.config/xonsh').exists:
        return
    dotfiles_list = []
    yield Dotfile(
            src=dd / 'xonshrc',
            dst=hh / '.xonshrc',
        )
    for file in (dl / 'xonsh').glob('*.xsh'):
        yield Dotfile(
                src=file,
                dst=hh / f'.config/xonsh/rc.d/{file.name}',
            ),

class RangerDotfile(Dotfile):

    def install(self):
        if not check_if_cmd_present('ranger'):
            return

        # RC file
        rc_file = Path.home() / '.config/ranger/rc.conf'
        if rc_file.exists():
            rc_file_text = rc_file.read_text()
            rc_file_text = do_regexp_replaces(rc_file_text, (
                (re.compile(r'^set show_hidden false$'), 'set show_hidden true'),
                (re.compile(r'^set preview_files true$'), 'set preview_files false'),
                (re.compile(r'^set preview_directories true$'), 'set preview_directories false'),
                # (re.compile(r'^set preview_images false$'), 'set preview_images true'),
            ))
        else:
            msg = "Ranger rc.conf doesn't exist: {rc_file}"
            log.error(msg)
            info.errors.append(msg)

        # RIFLE file
        rifle_file = Path.home() / '.config/ranger/rifle.conf'
        if rifle_file.exists():
            rifle_file_text = rifle_file.read_text()
            replaces = (
                (  # open archives in vim
                    re.compile(r'(^# Define the editor for non-text files \+ pager as last action$)'),
                    r'# TK: archives:\next tar\|gz\|bzip2\|xz\|tgz\|tbzip2\|txz\|zip\|rar = vim -- "$@"\n\1'
                ),
                (  # add extensions: pls, sql
                    '!mime ^text, label editor, ext xml|json|csv|tex|py|pl|rb|js|sh|php = ${VISUAL:-$EDITOR} -- "$@"',
                    '!mime ^text, label editor, ext xml|json|csv|tex|py|pl|pls|rb|js|sh|php|sql = ${VISUAL:-$EDITOR} -- "$@"'
                ),
                (  # add extensions: pls, sql
                    '!mime ^text, label pager,  ext xml|json|csv|tex|py|pl|rb|js|sh|php = "$PAGER" -- "$@"',
                    '!mime ^text, label pager,  ext xml|json|csv|tex|py|pl|pls|rb|js|sh|php|sql = "$PAGER" -- "$@"'
                ),
            )

            if 'viewnior' not in rifle_file_text:  # add viewnior for images
                replaces.append((
                    re.compile('(^' + re.escape('mime ^image/svg, has inkscape, X, flag f = inkscape -- "$@"') + '$)'),
                    r'mime ^image, has viewnior,  X, flag f = viewnior -- "$@"\n\1'
                ))
            if 'xreader' not in rifle_file_text:  # add xreader to pdfs
                replaces.append((
                    re.compile('(^' + re.escape('ext pdf, has qpdfview, X, flag f = qpdfview "$@"') + '$)'),
                    r'\1\next pdf, has xreader,  X, flag f = xreader -- "$@"'
                ))

            # # add options to feh
            # sed -i 's/mime ^image, has feh,       X, flag f = feh -- "$@"/mime ^image, has feh,       X, flag f = feh -. --auto-rotate -- "$@"/' "${rifleconf}"

            rifle_file_text = do_regexp_replaces(rifle_file_text, replaces)
        else:
            msg = "Ranger rifle.conf doesn't exist: {rc_file}"
            log.error(msg)
            info.errors.append(msg)

        # TODO: below, but split the dotfiles to public and private (with "torrentts")
        # LINUX)
        #     if [[ ${__myhost} = H ]]; then
        #         cat ~/.config/ranger/rifle.conf "${__dir_dotlocal}/rifle.conf.h.linux" > ~/.config/ranger/rifletmp.conf
        #         mv ~/.config/ranger/rifletmp.conf ~/.config/ranger/rifle.conf
        #         loguj -i -t "${ltype}" "CP: rifle.conf (L-H)"
        #     elif [[ ${__myhost} = W ]]; then
        #         cat ~/.config/ranger/rifle.conf "${__dir_dotlocal}/rifle.conf.w.linux" > ~/.config/ranger/rifletmp.conf
        #         mv ~/.config/ranger/rifletmp.conf ~/.config/ranger/rifle.conf
        #         loguj -i -t "${ltype}" "CP: rifle.conf (L-W)"
        #     else
        #         loguj -i -t "${ltype}" "Ranger - linux - unknown host Copying default file."
        #         cat ~/.config/ranger/rifle.conf "${__dir_dotfiles_new}/rifle.conf" > ~/.config/ranger/rifletmp.conf
        #         mv ~/.config/ranger/rifletmp.conf ~/.config/ranger/rifle.conf
        #         loguj -i -t "${ltype}" "CP: rifle.conf (L-OTHER)"
        #     fi
        #     ;;
        # *)
        #     cat ~/.config/ranger/rifle.conf "${__dir_dotfiles_new}/rifle.conf" > ~/.config/ranger/rifletmp.conf
        #     mv ~/.config/ranger/rifletmp.conf ~/.config/ranger/rifle.conf
        #     loguj -i -t "${ltype}" "CP: rifle.conf (OTHER-OTHER)"
        #     ;;

        # TODO: a jeśli nie ma dotfiles local, to było to:
        # else
        #     cat ~/.config/ranger/rifle.conf "${__dir_dotfiles_new}/rifle.conf" > ~/.config/ranger/rifletmp.conf
        #     mv ~/.config/ranger/rifletmp.conf ~/.config/ranger/rifle.conf
        #     # loguj -i -t "${ltype}" "Ranger - no local dotfiles. Copying default file."
        #     loguj -i -t "${ltype}" "CP: rifle.conf (default - no local dotfiles)"
        # fi

ranger = RangerDotfile(name='ranger')

dotfiles = [
    Dotfile(
        src=dd / 'tmux.conf_2.9',
        dst=hh / '.tmux.conf',
    ),
    ranger,
    Dotfile(
        src=dd / 'broot.conf.hjson',
        dst=hh / '.config/broot/conf.hjson',
    ),
    Dotfile(
        src=dd / 'gitconfig',
        dst=hh / '.gitconfig',
    ),
    Dotfile(
        src=dl / 'gitconfig.local',
        dst=hh / '.gitconfig.local',
    ),
    Dotfile(
        src=dd / 'vimrc',
        dst=hh / '.vimrc',
    ),
    Dotfile(
        src=dd / 'vimrc.local',
        dst=hh / '.vimrc.local',
    ),
    Dotfile(
        src=dd / 'vimrc.plugins',
        dst=hh / '.vimrc.plugins',
    ),
    Dotfile(
        src=dd / 'vimrc.functions',
        dst=hh / '.vimrc.functions',
    ),
    # Dotfile(
    #     src=dl / 'UltiSnips',
    #     dst=hh / '.vim/UltiSnips',
    # ),

    # if [[ -d ~/.gconf/apps/gnome-terminal ]]; then
    #     install_link "${__dir_dotfiles}/gnome-terminal" ~/.gconf/apps/gnome-terminal || true
    # fi

    Dotfile(
        src=dd / 'spacemacs',
        dst=hh / '.spacemacs',
    ),
    Dotfile(
        src=dd / 'spacemacs.local',
        dst=hh / '.spacemacs.local',
    ),

    *list(get_xonsh_dotfiles()),
    # ranger_install_dotfiles,
]



