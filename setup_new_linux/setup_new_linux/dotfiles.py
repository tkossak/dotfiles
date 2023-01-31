from pathlib import Path
import re
import os

from setup_new_linux import info
from setup_new_linux.classes.dotfilesc import Dotfile, LocalDotfile, ReplaceSnippetDotfile
from setup_new_linux.utils import (
    helpers as H,
    constants as C,
)
from setup_new_linux.utils.constants import Groups as G
from setup_new_linux.utils.setup import log
from setup_new_linux.classes.packagesc import PipxPackage, OsPackage


dd = info.dotfiles_dir
dl = info.dotfiles_local_dir
hh = Path.home()
xonsh_rc_d = hh / '.config/xonsh/rc.d/'
xonsh_dotfiles_dir = dd.parent / 'xonsh'
xonsh_dotfiles_local_dir = dl.parent / 'xonsh'


# XONSH #######################################################################

xonshrc = Dotfile(
        src=dd / 'xonshrc',
        dst=hh / '.xonshrc',
    )

def xonsh_remove_broken_links():
    for f in xonsh_rc_d.glob('*'):
        if f.is_symlink() and not f.exists():
            f.unlink()

def get_xonsh_dotfiles():
    """Get Paths for xonsh rc.d dotfiles
    """
    # get standard dotfiles:
    if not xonsh_dotfiles_dir.exists():
        msg = f"Dotfile folder for xonsh doesn't exist: {xonsh_dotfiles_dir}"
        log.error(msg)
        info.errors.append(msg)
    else:
        for file in xonsh_dotfiles_dir.glob('*.xsh'):
            yield Dotfile(
                    src=file,
                    dst=xonsh_rc_d / file.name,
                )

    # get local dotfiles:
    if not xonsh_dotfiles_local_dir.exists():
        msg = f"Local dotfiles folder for xonsh doesn't exist: {xonsh_dotfiles_local_dir}"
        log.error(msg)
        info.errors.append(msg)
    else:
        for file in xonsh_dotfiles_local_dir.glob('*'):
            if file.name.endswith('.xsh'):
                yield Dotfile(
                        src=file,
                        dst=xonsh_rc_d / file.name,
                    )
            elif file.name.endswith('xsh.h'):
                yield Dotfile(
                        src=file,
                        dst=xonsh_rc_d / file.name.replace(".h", ""),
                        groups=C.Groups.home,
                    )
            elif file.name.endswith('xsh.w'):
                yield Dotfile(
                        src=file,
                        dst=xonsh_rc_d / file.name.replace(".w", ""),
                        groups=C.Groups.work,
                    )
xonsh_local_dots = list(get_xonsh_dotfiles())

xonsh_dots = [
    xonsh_remove_broken_links,
    xonshrc,
    *xonsh_local_dots
]


# must be here instead of packages.py, because of circular import
ranger_pkg = PipxPackage(
    'ranger',
    pkg_name='ranger-fm',
    groups=C.GROUPS_DEFAULT_PKG | G.liveusb,
)


# BASH ########################################################################

def generate_bashrc_snippet_from_xonsh_file(xonsh_file_src: Path) -> str:
    # xonshrc_lines = xonshrc.src.read_text().splitlines()
    xonshrc_lines = xonsh_file_src.read_text().splitlines()
    bash_aliases_d = {}
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

        if '# bash: ' in line:
            # bash version of the alias is written in comment
            s = s.partition('# bash: ')[2]

        else:
            # convet xonsh alias to bash alias

            if '#' in s:
                s = s.rpartition('#')[0]

        s = s.strip()
        if (
            s == "ga('''\\"
            or s.startswith('_')
        ):
            continue

        if s.startswith(('abbrevs[', 'aliases[')):
            copy_from_name = s.strip('abrevs[]li')[1:-1]
            if copy_from_name in bash_aliases_d:
                bash_aliases_d[name] = bash_aliases_d[copy_from_name]
            else:
                log.debug('Alias {copy_from_name} does not exist')
            continue

        s = s.strip('ga()rf')
        q = s[0]  # quote style of the alias
        if (
            q not in '"\''
            or s[-1] != q
        ):
            log.debug(f'bashrc skip xonsh alias: {line}')
            continue
        s = s[1:-1]
        s = s.replace('@$', '$')

        # escape quotes:
        s = s.replace(f'\\{q}', f'{q}\\{q}{q}')
        if q == '"':
            s = s.replace("'", f"'\\''")

        if s.strip(' \t;\':",./<>?[]\\{}|!@#$%^&*()_+`~'):
            bash_aliases_d[name] = s

    bash_aliases = '\n'.join(
        f"alias {name}='{definition}'"
        for name, definition
        in bash_aliases_d.items()
    ) + '\n'

    return bash_aliases

def get_all_bashrc_aliases_from_xonsh():
    home_aliases = []
    work_aliases = []
    local_aliases = []
    for d in xonsh_local_dots:
        s = generate_bashrc_snippet_from_xonsh_file(d.src)
        if s.strip():
            if C.Groups.home in d.groups:
                home_aliases.append(s)
            elif C.Groups.work in d.groups:
                work_aliases.append(s)
            else:
                local_aliases.append(s)
    home_aliases_str = '\n'.join(home_aliases)
    work_aliases_str = '\n'.join(work_aliases)
    local_aliases_str = '\n'.join(local_aliases)
    if home_aliases_str.strip():
        yield ReplaceSnippetDotfile(
            name='bashrc home aliases',
            snippet=home_aliases_str,
            dst=hh / '.bashrc',
            tag='Kossak home aliases from xonsh',
            groups=C.Groups.home,
        )
    if work_aliases_str.strip():
        yield ReplaceSnippetDotfile(
            name='bashrc work aliases',
            snippet=work_aliases_str,
            dst=hh / '.bashrc',
            tag='Kossak work aliases from xonsh',
            groups=C.Groups.work,
        )
    if local_aliases_str.strip():
        yield ReplaceSnippetDotfile(
            name='bashrc local aliases',
            snippet=local_aliases_str,
            dst=hh / '.bashrc',
            tag='Kossak local aliases from xonsh',
        )


bashrc = ReplaceSnippetDotfile(src=dd / 'bashrc.snippet', dst=hh / '.bashrc')
bashrc_aliases = ReplaceSnippetDotfile(
    name='bashrc aliases',
    snippet=generate_bashrc_snippet_from_xonsh_file(xonshrc.src),
    dst=hh / '.bashrc',
    tag='Kossak aliases from xonsh',
)
bashprofile = ReplaceSnippetDotfile(src=dd / 'bash_profile.snippet', dst=hh / '.bash_profile')
bash_dots = [
    bashrc,
    bashrc_aliases,
    bashprofile,
    *get_all_bashrc_aliases_from_xonsh(),
]


# RANGER ######################################################################

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

ranger_dot = RangerDotfile(name='ranger')
ranger_pkg.configure = ranger_dot.install
ranger_dots = [
    ranger_dot,
    ReplaceSnippetDotfile(src=dd / 'rifle.conf.snippet', dst=ranger_dot.rifle_file),
    ReplaceSnippetDotfile(
        src=dl / 'rifle.conf.h.snippet',
        dst=ranger_dot.rifle_file,
        tag='Kossak home',
        groups=G.home,
        dont_add_errors_to_info_if_no_locals=True,
    )
]


# TMUX ########################################################################

tmux_dot = Dotfile(
        src=dd / 'tmux.conf_2.9',
        dst=hh / '.tmux.conf',
    )

# must be here, because of circular import
class TmuxOsPackage(OsPackage):

    def __init__(self):
        super().__init__(
            'tmux',
            groups=C.GROUPS_DEFAULT_PKG | G.server | G.liveusb
        )

    def configure(self):
        H.run_cmd(['git', 'clone', 'https://github.com/tmux-plugins/tpm', Path.home() / '.tmux/plugins/tpm'])
        self.tmux_plugins_install_and_update()

    def tmux_plugins_install_and_update(self):
        log.info('tmux configure')
        tmux_dot.install()

        # TODO: see here if it asks to press enter to continue:
        # https://github.com/tmux-plugins/tpm/issues/6

        script_install = Path.home() / '.tmux/plugins/tpm/scripts/install_plugins.sh'
        if script_install.exists:
            log.info('tmux install plugins')
            H.run_cmd([str(script_install)])

        script_update = Path.home() / '.tmux/plugins/tpm/bin/update_plugins'
        if script_update.exists():
            log.info('tmux update plugins')
            H.run_cmd([str(script_update), 'all'])

tmux_pkg = TmuxOsPackage()
tmux_dots = (
    tmux_dot,
    tmux_pkg.tmux_plugins_install_and_update,
)


# VIM #########################################################################

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

# INNE ########################################################################

etc_environment = ReplaceSnippetDotfile(
    src=info.dotfiles_dir / 'environment.snippet',
    dst='/etc/environment',
    sudo=True,
)
# etc_profile = ReplaceSnippetDotfile(
#     src=dd / 'etc_profile.snippet',
#     dst='/etc/profile', sudo=True
# )


# DOTFILES LIST ###############################################################

dotfiles = [
    etc_environment,
    # etc_profile,
    *bash_dots,
    *xonsh_dots,
    *tmux_dots,
    *ranger_dots,
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
        groups=G.home,
    ),
    LocalDotfile(
        src=dl / 'gitconfig.w.local',
        dst=hh / '.gitconfig.local',
        groups=G.work,
    ),
    *vim_dotfiles,
    Dotfile(
        src=dd / 'spacemacs',
        dst=hh / '.spacemacs',
    ),
    Dotfile(
        src=dd / 'visidatarc',
        dst=hh / '.visidatarc',
    ),
    Dotfile(
        src=dd / 'xmodmap_mine',
        dst=hh / '.xmodmap',
    ),
    asdf_remove_unneeded_shims,
]

# # TODO: remove
# dotfiles = [
#     *bash_dots
# ]