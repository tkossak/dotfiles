from pathlib import Path
import re
import os

from setup_new_linux import info
from setup_new_linux.classes.dotfilesc import Dotfile, LocalDotfile, ReplaceSnippetDotfile
from setup_new_linux.utils import helpers as H
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
            )


class RangerDotfile(Dotfile):

    def install(self):
        ranger_config = Path.home() / '.config/ranger'
        if not ranger_config.exists():
            return

        # RC file
        rc_file = ranger_config / 'rc.conf'
        if not rc_file.exists():
            myenv = os.environ
            myenv['TERM'] = 'xterm'
            myenv['TERMINFO'] = '/etc/terminfo'
            H.run_cmd(
                f'{str(Path.home() / ".local/bin/ranger")} --copy-config all',
                shell=True,
                env=myenv
            )

        if rc_file.exists():
            rc_file_text = rc_file.read_text()
            rc_file_text_new = H.do_regexp_replaces(rc_file_text, (
                (re.compile(r'^set show_hidden false$', re.MULTILINE), 'set show_hidden true'),
                (re.compile(r'^set preview_files true$', re.MULTILINE), 'set preview_files false'),
                (re.compile(r'^set preview_directories true$', re.MULTILINE), 'set preview_directories false'),
                # (re.compile(r'^set preview_images false$'), 'set preview_images true'),
            ))
            if rc_file_text != rc_file_text_new:
                rc_file.write_text(rc_file_text_new)
        else:
            msg = f"Ranger rc.conf doesn't exist: {rc_file}"
            log.error(msg)
            info.errors.append(msg)

        # RIFLE file
        rifle_file = ranger_config / 'rifle.conf'
        if rifle_file.exists():
            rifle_file_text = rifle_file.read_text()
            replaces = [
                (  # open archives in vim
                    re.compile(r'(^# Define the editor for non-text files \+ pager as last action$)', re.MULTILINE),
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
            ]

            if 'viewnior' not in rifle_file_text:  # add viewnior for images
                replaces.append((
                    re.compile('(^' + re.escape('mime ^image/svg, has inkscape, X, flag f = inkscape -- "$@"') + '$)', re.MULTILINE),
                    r'mime ^image, has viewnior,  X, flag f = viewnior -- "$@"\n\1'
                ))
            if 'xreader' not in rifle_file_text:  # add xreader to pdfs
                replaces.append((
                    re.compile('(^' + re.escape('ext pdf, has qpdfview, X, flag f = qpdfview "$@"') + '$)', re.MULTILINE),
                    r'\1\next pdf, has xreader,  X, flag f = xreader -- "$@"'
                ))

            # # add options to feh
            # sed -i 's/mime ^image, has feh,       X, flag f = feh -- "$@"/mime ^image, has feh,       X, flag f = feh -. --auto-rotate -- "$@"/' "${rifleconf}"

            rifle_file_text_new = H.do_regexp_replaces(rifle_file_text, replaces)

            if rifle_file_text != rifle_file_text_new:
                rifle_file.write_text(rifle_file_text_new)
        else:
            msg = f"Ranger rifle.conf doesn't exist: {rc_file}"
            log.error(msg)
            info.errors.append(msg)

        log.info('Ranger dotfiles installed')
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

bashrc = ReplaceSnippetDotfile(src=dd / 'bashrc.snippet', dst=hh / '.bashrc')
bashprofile = ReplaceSnippetDotfile(src=dd / 'bash_profile.snippet', dst=hh / '.bash_profile')
etc_environment = ReplaceSnippetDotfile(
    src=info.dotfiles_dir / 'environment.snippet',
    dst='/etc/environment',
    sudo=True,
)


vimrc_plugins = Dotfile(
        src=dd / 'vimrc.plugins',
        dst=hh / '.vimrc.plugins',
    )

def vim_install_plugins():
    vimplug_path = Path.home() / '.vim/autoload/plug.vim'
    # TODO: run git update if dir already exists
    if not vimplug_path.exists():
        log.info('Vim get Plug manager')
        H.run_cmd(['curl', '-fLo', str(vimplug_path), '--create-dirs', 'https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'])
    # TODO: run :PlugUpdate if plugins are already installed? or --sync already handles it?
    if not (Path.home() / '.vim/plugged').exists():
        vimlog = Path('/tmp/vim_plugins.log')
        log.debug(f'Vim install plugins (output in {vimlog})')
        # H.run_cmd(f"vim -u '{vimrc_plugins.src}' +':PlugInstall --sync' +':qa!' >{vimlog} 2>&1")
        H.run_cmd(f"vim -u '{vimrc_plugins.src}' -es +':PlugInstall --sync' +':qa!'")
        # remove '-es' to see output (but it will be VIM TUI)
        # manual command without -es:
        #   vim -u '/app/dotfiles/vimrc.plugins' +':PlugInstall --sync' +':qa!'


vim_dotfiles = [
    Dotfile(
        src=dd / 'vimrc',
        dst=hh / '.vimrc',
    ),
    # LocalDotfile(
    #     src=dl / 'vimrc.local',
    #     dst=hh / '.vimrc.local',
    # ),
    vimrc_plugins,
    Dotfile(
        src=dd / 'vimrc.functions',
        dst=hh / '.vimrc.functions',
    ),
    # NoErrorDotfile(
    #     src=dl / 'UltiSnips',
    #     dst=hh / '.vim/UltiSnips',
    # ),
    vim_install_plugins,
]

dotfiles = [
    etc_environment,
    bashrc,
    bashprofile,
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
    LocalDotfile(
        src=dl / 'gitconfig.local',
        dst=hh / '.gitconfig.local',
    ),
    *vim_dotfiles,
    Dotfile(
        src=dd / 'spacemacs',
        dst=hh / '.spacemacs',
    ),
    LocalDotfile(
        src=dl / 'spacemacs.local',
        dst=hh / '.spacemacs.local',
    ),

    *list(get_xonsh_dotfiles()),
    # ranger_install_dotfiles,
]



