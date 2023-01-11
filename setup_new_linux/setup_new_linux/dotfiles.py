from pathlib import Path
import re
import os

from setup_new_linux import info
from setup_new_linux.classes.dotfilesc import Dotfile, LocalDotfile, ReplaceSnippetDotfile
from setup_new_linux.utils import (
    helpers as H,
    constants as C,
)
from setup_new_linux.utils.setup import log
from setup_new_linux.classes.packagesc import PipxPackage


dd = info.dotfiles_dir
dl = info.dotfiles_local_dir
hh = Path.home()

xonshrc = Dotfile(
        src=dd / 'xonshrc',
        dst=hh / '.xonshrc',
    )

def get_xonsh_dotfiles():
    """Get Paths for xonsh rc.d dotfiles
    """

    for file in (dl / 'xonsh').glob('*.xsh'):
        yield Dotfile(
                src=file,
                dst=hh / f'.config/xonsh/rc.d/{file.name}',
            )


# must be here instead of packages.py, because of circular import
ranger_pkg = PipxPackage('ranger-fm')

class RangerDotfile(Dotfile):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ranger_config = Path.home() / '.config/ranger'
        self.rc_file = self.ranger_config / 'rc.conf'
        self.rifle_file = self.ranger_config / 'rifle.conf'

    def install(self):
        # if not ranger_config.exists():
        if not (ranger_pkg.is_pkg_installed or ranger_pkg.is_cmd_available):
            return

        self.ranger_config.mkdir(parents=True, exist_ok=True)

        for file in (
            self.ranger_config / 'commands.py',
            self.ranger_config / 'commands_full.py',
            self.ranger_config / 'rc.conf',
            self.ranger_config / 'rifle.conf',
            self.ranger_config / 'scope.sh',
        ):
            if file.exists():
                file.unlink()

        # re-create default ranger dotfiles:
        myenv = os.environ
        myenv['TERM'] = 'xterm'
        myenv['TERMINFO'] = '/etc/terminfo'
        H.run_cmd(
            f'{str(Path.home() / ".local/bin/ranger")} --copy-config all',
            shell=True,
            env=myenv
        )

        #######################################################################
        # RC FILE
        rc_file_text = self.rc_file.read_text()
        rc_file_text_new = H.do_regexp_replaces(rc_file_text, (
            (re.compile(r'^set show_hidden false$', re.MULTILINE), 'set show_hidden true'),
            (re.compile(r'^set preview_files true$', re.MULTILINE), 'set preview_files false'),
            (re.compile(r'^set preview_directories true$', re.MULTILINE), 'set preview_directories false'),
            # (re.compile(r'^set preview_images false$'), 'set preview_images true'),
        ))
        if rc_file_text != rc_file_text_new:
            self.rc_file.write_text(rc_file_text_new)

        #######################################################################
        # RIFLE file
        rifle_file_text = self.rifle_file.read_text()
        replaces = [
            (  # open archives in vim
                re.compile(r'(^# Define the editor for non-text files \+ pager as last action$)', re.MULTILINE),
                r'# TK: archives:\next tar|gz|bzip2|xz|tgz|tbzip2|txz|zip|rar = vim -- "$@"\n\1'
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
        if 'onlyoffice' not in rifle_file_text:
            replaces.append((
                re.compile('(^' + re.escape('ext pptx?|od[dfgpst]|docx?|sxc|xlsx?|xlt|xlw|gnm|gnumeric, has libreoffice, X, flag f = libreoffice "$@"') + '$)', re.MULTILINE),
                r'ext pptx?|od[dfgpst]|docx?|sxc|xlsx?|xlt|xlw|gnm|gnumeric, has onlyoffice,  X, flag f = onlyoffice -- "$@"\n\1'
            ))

        # # add options to feh
        # sed -i 's/mime ^image, has feh,       X, flag f = feh -- "$@"/mime ^image, has feh,       X, flag f = feh -. --auto-rotate -- "$@"/' "${rifleconf}"

        rifle_file_text_new = H.do_regexp_replaces(rifle_file_text, replaces)

        if rifle_file_text != rifle_file_text_new:
            self.rifle_file.write_text(rifle_file_text_new)

        log.info('Ranger dotfiles created')

ranger = RangerDotfile(name='ranger')
ranger_pkg.configure = ranger.install
ranger_dotfiles = [
    ranger,
    ReplaceSnippetDotfile(src=dd / 'rifle.conf.snippet', dst=ranger.rifle_file),
    ReplaceSnippetDotfile(
        src=dl / 'rifle.conf.h.snippet',
        dst=ranger.rifle_file,        tag='Kossak home',
        groups=C.Groups.home,
        dont_add_errors_to_info_if_no_locals=True,
    )
]

def get_bashrc_snippet_for_xonsh_aliases() -> str:
    xonshrc_lines = xonshrc.src.read_text().splitlines()
    bash_aliases_l = []
    for line in xonshrc_lines:
        if (
            not (line.startswith('abbrevs[') or line.startswith('aliases['))
            or '# nobash' in line
        ):
            continue

        s = line
        s = s.replace('<edit>', '')
        name, _, s = s.partition('=')

        # alias name:
        name_quote = "'" if "'" in name else '"'
        name = name.split(name_quote)[1]

        # alias definition:
        if '#' in s:
            s = s.rpartition('#')[0]
        s = s.strip(' ga()r')
        q = s[0]  # quote type of the alias
        s = s[1:-1]
        if q not in '"\'':
            log.debug(f'bashrc skip xonsh alias: {line}')
            continue
        s = s.replace('$', r'\$')
        # replace quotes inside:
        s = s.replace(q, f'{q}\\{q}{q}')
        if s:
            bash_aliases_l.append(f"alias {name}={q}{s}{q}")

    return '\n'.join(bash_aliases_l) + '\n'

bashrc = ReplaceSnippetDotfile(src=dd / 'bashrc.snippet', dst=hh / '.bashrc')
bashrc_aliases = ReplaceSnippetDotfile(
    name='bashrc aliases',
    snippet=get_bashrc_snippet_for_xonsh_aliases(),
    dst=hh / '.bashrc',
    tag='Kossak aliases from xonsh',
)


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

def asdf_remove_unneeded_shims():
    log.info('Remove unneeded asdf shims')
    asdf_shims = C.ASDF_DIR / 'shims'
    for f in (
        'powerline*', 'xz', 'sqlite3', 'xmllint', 'iconv', 'envsubst', 'clear',
        'gettext', 'gettext.sh', 'tput', 'envsubst', 'pandoc', 'pipx', 'bsdtar',
        'reset', 'zstd', 'bzip2'
    ):
        for file in asdf_shims.glob(f):
            log.info(f'Removing: {file}')
            file.unlink()


dotfiles = [
    etc_environment,
    bashrc,
    bashrc_aliases,
    bashprofile,
    Dotfile(
        src=dd / 'tmux.conf_2.9',
        dst=hh / '.tmux.conf',
    ),
    *ranger_dotfiles,
    Dotfile(
        src=dd / 'broot.conf.hjson',
        dst=hh / '.config/broot/conf.hjson',
    ),
    Dotfile(
        src=dd / 'gitconfig',
        dst=hh / '.gitconfig',
    ),
    LocalDotfile(
        src=dl / 'gitconfig.h.local',
        dst=hh / '.gitconfig.local',
        groups=C.Groups.home,
    ),
    # LocalDotfile(
    #     src=dl / 'gitconfig.w.local',
    #     dst=hh / '.gitconfig.local',
    #     groups=C.Groups.work,
    # ),
    *vim_dotfiles,
    Dotfile(
        src=dd / 'spacemacs',
        dst=hh / '.spacemacs',
    ),
    xonshrc,
    *list(get_xonsh_dotfiles()),
    Dotfile(
        src=dd / 'visidatarc',
        dst=hh / '.visidatarc',
    ),
    asdf_remove_unneeded_shims,
]
