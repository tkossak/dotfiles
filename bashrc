# If not running interactively, don't do anything
[[ -z "$PS1" ]] && exit

# set a fancy prompt (non-color, unless we know we "want" color)
# case "$TERM" in
# xterm-color) color_prompt=yes;;
# esac
color_prompt=yes;

[[ -n "$TMUX" ]] &&
    export TERM=screen-256color ||
    export TERM=xterm-256color

[[ -r ~/.bashrc.colors ]] &&
    source ~/.bashrc.colors
# eval `dircolors ~/.dir_colors`

# set -o vi
# bind -m vi-command ".":insert-last-argument

# don't put duplicate lines or lines starting with space in the history.  # See bash(1) for more options
HISTCONTROL=ignoreboth
# append to the history file, don't overwrite it
shopt -s histappend

HISTSIZE=1000
HISTFILESIZE=10000
# check the window size after each command and, if necessary, update the values of LINES and COLUMNS.
shopt -s checkwinsize

# ----------------------------------------------------------------------

[[ -r ~/.bashrc.local ]] &&
    source ~/.bashrc.local

export EDITOR=vim

alias ll='ls -lFh --color=auto'
alias lla='ls -lAFh --color=auto'
alias ls='ls -F --color=auto'
alias la='ls -AF --color=auto'
alias ld='echo */'
alias lld='ls -lFh | grep --color=never ^d'
alias grep='grep --color'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias .....='cd ../../../..'
alias .4='cd ../../../../'
alias .5='cd ../../../../..'
alias pls='sudo $(history -p !!)'
alias mkdir='mkdir -p'
alias bc='bc -l'
alias du='du -ch'
alias df='df -h'
alias lsblk='lsblk -fm'
alias blkid='blkid -o list'
alias vi='vim'
alias vbox='sudo mount -t vboxsf vbox_shared /mnt/vs && cd /mnt/vs'
alias vboxd='sudo mount -t vboxsf vbox_shared /mnt/vs && cd /mnt/vs/dotfiles'
alias glances='glances -b'
alias mplayer='mplayer -fs -softvol -softvol-max 300'

alias dmp3='youtube-dl -cx --audio-format mp3 --restrict-filenames'
alias dvid='youtube-dl -c --restrict-filenames'
alias yt='youtube-dl'
alias gn='geeknote'

# TMUX
alias tl='tmux list-sessions'
alias ta='tmux attach-session'
alias tat='tmux attach-session -t'
alias tn='tmux new-session'
alias tns='tmux new-session -s'

# say something
say(){ mplayer -user-agent Mozilla "http://translate.google.com/translate_tts?tl=en&q=$(echo $* | sed 's#\ #\+#g')" > /dev/null 2>&1 ; }
saypl(){ mplayer -user-agent Mozilla "http://translate.google.com/translate_tts?tl=pl&q=$(echo $* | sed 's#\ #\+#g')" > /dev/null 2>&1 ; }

# translate english => polish
t() { wget -U "Mozilla/5.0" -qO - "http://translate.google.com/translate_a/t?client=t&text=$1&sl=${2:-en}&tl=${3:-pl}" | sed 's/\[\[\[\"//' | cut -d \" -f 1; }

function ranger-cd
{
    local tempfile='/tmp/chosendir'
    if [[ -f /usr/bin/ranger ]]; then
        local ranger_path="/usr/bin/ranger"
    elif [[ -f /usr/local/bin/ranger ]]; then
        local ranger_path="/usr/local/bin/ranger"
    fi

    ${ranger_path} --choosedir="$tempfile" "${@:-$(pwd)}"
    test -f "$tempfile" &&
    if [ "$(cat -- "$tempfile")" != "$(echo -n `pwd`)" ]; then
        cd -- "$(cat "$tempfile")"
    fi
    rm -f -- "$tempfile"
}

bind '"\C-o":"ranger-cd\C-m"'

export PS1="\[${Cyan}\]$(((SHLVL>1)) && echo "${SHLVL}\[${IBlack}\].")\[${IGreen}\]\u\[${IBlack}\]@\[${Purple}\]\h\[${IYellow}\] \w \$ \[${Color_Off}\]"

__myos="$(uname)"
__myhost="$(uname -n)"

case ${__myos} in
    CYGWIN*)

        # -----------------------------------------------------------------------
        # -- CYGWIN
        # -----------------------------------------------------------------------

        export LANG=en_US.UTF-8
        #export LC_ALL='C' # needed for uniq to work on polish letters

        cyginstq() { $(get_param p_cdde)/setup-x86.exe -nqP "$1"; }
        cyginst()  { $(get_param p_cdde)/setup-x86.exe -nP "$1"; }
        cs() { cygstart $*; }

        __vTmp1="$(get_param p_cdp)"
        __vTmp2="$(get_param p_ccp)"
        if [ -e "${__vTmp1}/Nmap/nmap.exe" ]; then
            alias nmap="\"${__vTmp1}/Nmap/nmap.exe\""
        elif [ -e "${__vTmp2}/Nmap/nmap.exe" ]; then
            alias nmap="\"${__vTmp2}/Nmap/nmap.exe\""
        fi

        #------------------
        # Win variables
        _vTmpPathCyg="$(get_param p_temp_cyg)"
        #_vTmpPathWin="$(cygpath -aw ${_vTmpPathCyg})"
        __vTmp1="$(get_param p_cdkp)"
        __vTmp2="$(get_param p_cedpp)"
        if [[ -e $__vTmp1 ]]; then
            _vProgsPath="$__vTmp1"
        elif [[ -e $__vTmp2 ]]; then
            _vProgsPath="$__vTmp2"
        fi

        #------------------
        # Win progs aliases

        gvim() { cs "${_vProgsPath}/gvim/gvim.exe" $*; }
        # run last activity
        rla() { cs "${_vProgsPath}/_win_sys_tools/LastActivityView/LastActivityView.exe"; }
        # run last logins
        rll() { cs "${_vProgsPath}/_win_sys_tools/WinLogOnView/WinLogOnView.exe"; }
        # run last turned on
        rlt() { cs "${_vProgsPath}/_win_sys_tools\TurnedOnTimesView\TurnedOnTimesView.exe"; }
        #alias gvim="\"${_vProgsPath}/gvim/gvim.exe\""


        if [[ $__myhost == "$(get_param whost)" ]]; then
            proxyoff()
            {
                reg add "hklm\software\wow6432node\microsoft\windows\currentversion\internet settings" /f /v proxyenable /t reg_dword /d 0
                reg add "hklm\software\microsoft\windows\currentversion\internet settings" /f /v proxyenable /t reg_dword /d 0
                reg add "hkcu\software\wow6432node\microsoft\windows\currentversion\internet settings" /f /v proxyenable /t reg_dword /d 0
                reg add "hkcu\software\microsoft\windows\currentversion\internet settings" /f /v proxyenable /t reg_dword /d 0
            }
            alias updatedb='time updatedb --prunepaths="/tmp /var/spool /home/.ecryptfs /cygdrive/k /cygdrive/l /cygdrive/m /cygdrive/n /proc"'
            fixwin()
            {
                proxyoff
                net share C$ /delete
                net share D$ /delete
                net share IPC$ /delete
                net share ADMIN$ /delete
            }
            if [[ -z "${TMUX}" ]]; then
                fixwin
            fi
        fi

        # SSH-AGENT
        if [ -f ~/.agent.env ]; then
            . ~/.agent.env > /dev/null
            if ! kill -0 $SSH_AGENT_PID > /dev/null 2>&1; then
                echo "Stale agent file found. Spawning new agent… "
                eval `ssh-agent | tee ~/.agent.env`
                ssh-add
            fi
        else
            echo "Starting ssh-agent"
            eval `ssh-agent | tee ~/.agent.env`
            ssh-add
        fi

        aks()
        {
            while [[ $# > 0 ]]; do
                case "$1" in
                    anki)
                        cs /cygdrive/d/Kossak/ahk/anki.ahk
                        shift
                        ;;
                    sql)
                        cs /cygdrive/d/Kossak/ahk/plsql.ahk
                        shift
                        ;;
                    *)
                        echo "ERROR: Unknown option: ${1}"
                        return 1
                        ;;
                esac
            done
        }
        ;;
    Linux)

        # -----------------------------------------------------------------------
        # -- LINUX
        # -----------------------------------------------------------------------

        # for NOT ROOT only
        if [ $UID -ne 0 ]; then
            alias reboot='sudo reboot'
            alias apt-get='sudo apt-get'
            alias atop='sudo atop'
            alias umount='sudo umount'
        fi

        ri()
        {
            sudo ls
            sudo nohup roccatiskuconfig &> /dev/null &
        }

        capsoff()
        {
            #caps lock => escape
            xmodmap -e 'clear Lock'
            xmodmap -e 'keycode 66 = Escape'
            #KP_Separator => period
            xmodmap -e 'keycode 91 mod2 = KP_Delete period'
        }

        capson()
        {
            xmodmap -e 'keycode 66 = Caps_Lock'
            xmodmap -e 'clear lock'
            xmodmap -e 'add lock = Caps_Lock'
            xmodmap -e 'keycode 91 = KP_Delete KP_Separator KP_Delete KP_Separator'
        }


        alias cs="xdg-open"
        # alias aptgo='apt-get update && apt-get -y upgrade && apt-get -y dist-upgrade && apt-get -fy install && apt-get -y autoremove && apt-get -y autoclean && apt-get -y clean'
        alias aptgo='apt-get update && apt-get -y upgrade && apt-get -fy install && apt-get -y autoremove && apt-get -y autoclean && apt-get -y clean'
        alias iotop='sudo iotop --only'
        alias fping='ping -c 5 -i.2'

        ;;
    *)

        echo 'other os?';;

esac
# --- END CASE ---------------------------------------------------------

e()
{
    local word="$*"
    word="${word// /+}"
    cs "http://dict.pl/dict?word=${word}" >/dev/null
    cs "http://ling.pl/slownik/angielsko-polski/${word}" >/dev/null
    cs "http://en.bab.la/dictionary/english-polish/${word}" >/dev/null
    cs "http://www.thefreedictionary.com/${word}" >/dev/null
    cs "http://en.pons.com/translate?q=${word}&l=enpl&in=&lf=en" > /dev/null
    cs "http://www.urbandictionary.com/define.php?term=${word}" > /dev/null
}


# FASD -----------------------------------------------------------------
if hash fasd 2>/dev/null; then
    eval "$(fasd --init auto)"
    alias v='f -e vim' # quick opening files with vim
    alias j='fasd_cd -d'
    case $__myos in
        CYGWIN*)
            alias o='a -e cygstart'
            ;;
        Linux)
            alias o='a -e xdg-open'
    esac
    _fasd_bash_hook_cmd_complete f a s d v o
fi


# COMMACD: -------------------------------------------------------------
if [[ -r ~/.commacd.bash ]]; then
    source ~/.commacd.bash
fi


# fzf ------------------------------------------------------------------
if [[ -r ~/.fzf.bash ]]; then
    source ~/.fzf.bash
    export FZF_COMPLETION_OPTS='-x'
    export FZF_DEFAULT_OPTS='-x'
    # default keys/func/
    # CTRL-T - find file
    # CTRL-R - search history
    # **<TAB> - autocompletion
    # kill -9 <TAB>

    # fd - cd into directory
    fd() {
        local dir
        dir=$(find . -type d 2> /dev/null | fzf --query="$1" --select-1) && cd "$dir"
    }

    # fdl - cd into directory - only maxdepth=1 dirs
    fdl() {
        local dir
        dir=$(find . -type d -maxdepth 1 2> /dev/null | fzf --query="$1" --select-1) && cd "$dir"
    }

    # ff - cd into the directory of the selected file
    ff() {
        local file
        local dir
        file=$(fzf +m -q "$1") && dir=$(dirname "$file") && cd "$dir"
    }

    # fv [FUZZY PATTERN] - Open the selected file with the default editor
    # - Bypass fuzzy finder if there's only one match (--select-1)
    # - Exit if there's no match (--exit-0)
    fv() {
        local file
        file=$(fzf --query="$1" --select-1 --exit-0)
        [ -n "$file" ] && ${EDITOR:-vim} "$file"
    }

    # fkill - kill process
    # fkill() {
    # pid=$(ps -ef | sed 1d | fzf -m | awk '{print $2}')
    #
    # if [ "x$pid" != "x" ]
    # then
    # kill -${1:-9} $pid
    # fi
    # }
fi

[[ -d ~/.dotfiles/bin ]] && export PATH=~/.dotfiles/bin:${PATH}
# source ~/.bash-git-prompt/gitprompt.sh

# -----------------------------------------------------------------------
# -- bash start info
# -----------------------------------------------------------------------
# Today is:
echo "------------------------------------------------------------------"
echo -e "${IYellow}Today is: ${BWhite}$(date +'%F (%A) %T')"

# # Uptime:
# __vTmp3="$(uptime | sed -e 's:,[^,]\+user.*::I;s/.*up\s\+//')"
# [[ -n $__vTmp3 ]] && echo -e " ${IYellow}UPTIME:${BWhite} ${__vTmp3}" || echo ""

# # Tmux:
# __vTmp3="$(tmux list-sessions 2>/dev/null)"
# [[ -n $__vTmp3 ]] && echo -e "${IYellow}TMUX:${Color_Off} ${__vTmp3}"

# # Is Internet on Fire:
# if [[ "$__myhost" != "dziura" ]]; then
# echo -e "${IYellow}IS INTERNET ON FIRE?${Color_Off}"
# host -t txt istheinternetonfire.com | cut -f 2- -d '"' | sed 's/\. /\n/g;s/ http/\nhttp/g;s/\\;/;/g;s/" "//g;s/"$//g'
# echo
# fi

# Last logins:
if [[ ! ${__myos} == CYGWIN* ]]; then
    echo -en "${IYellow}LAST logins:\n${Color_Off}"
    __vTmp3="$(last | uniq | head -13)"
    [[ -n $__vTmp3 ]] && echo -e "${Color_Off}${__vTmp3}"
fi

# finishing touches
unset __vTmp1 __vTmp2 __vTmp3
unset __myos __myhost

unset Color_Off Black Red Green Yellow Blue Purple Cyan White BBlack BRed BGreen BYellow BBlue BPurple BCyan BWhite UBlack URed UGreen UYellow UBlue UPurple UCyan UWhite On_Black On_Red On_Green On_Yellow On_Blue On_Purple On_Cyan On_White IBlack IRed IGreen IYellow IBlue IPurple ICyan IWhite BIBlack BIRed BIGreen BIYellow BIBlue BIPurple BICyan BIWhite On_IBlack On_IRed On_IGreen On_IYellow On_IBlue On_IPurple On_ICyan On_IWhite

# export PAGER=/usr/local/bin/vimpager
# alias less=$PAGER
# alias zless=$PAGER
