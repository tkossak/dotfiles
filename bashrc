# If not running interactively, don't do anything
# [[ "$-" != *i* ]] && exit
[[ $- != *i* ]] && return

# echo ".bashrc start"
# [[ -z "$PS1" ]] && exit
# echo "~/.bashrc starting"
# [[ -z ${USER_BASHRC} ]] && USER_BASHRC="1" || return

#anger set a fancy prompt (non-color, unless we know we "want" color)
# case "$TERM" in
# xterm-color) color_prompt=yes;;
# esac
color_prompt=yes;

[[ -n "$TMUX" ]] &&
    export TERM=screen-256color ||
    export TERM=xterm-256color

[[ -r ~/.dotfiles/source/src_bash_vars_colors ]] &&
    source ~/.dotfiles/source/src_bash_vars_colors ||
    echo "No src_bash_vars_colors files!"
# eval `dircolors ~/.dir_colors`

# set -o vi
# bind -m vi-command ".":insert-last-argument

# don't put duplicate lines or lines starting with space in the history.  # See bash(1) for more options
HISTCONTROL=ignoreboth
# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=10000

# check the window size after each command and, if necessary, update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# export XONSH_SHOW_TRACEBACK=True

# ----------------------------------------------------------------------
source $HOME/.dotfiles/source/src_bash_vars_myos
source $HOME/.dotfiles/source/src_bash_basic_functions

source "$HOME/.bashrc.local"
add_to_path "$HOME/.local/bin"

export EDITOR=vim
# export GREP_OPTIONS='-i'

alias l='ls -lFh --color=auto'
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
alias lsblk_='sudo lsblk -fm'
alias blkid_='blkid -o list'
alias vi='vim'
alias ncal="ncal -M"
alias vbox='sudo mount -t vboxsf vbox_shared /mnt/vs && cd /mnt/vs'
alias vboxd='sudo mount -t vboxsf vbox_shared /mnt/vs && cd /mnt/vs/dotfiles'

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# sudos
alias iftop='sudo iftop'
alias nethogs='sudo nethogs'
alias tcptrack='sudo tcptrack'
alias atop='sudo atop'

# apps
alias glances='glances -b'
alias mplayer='mplayer -fs -softvol -softvol-max 300'
alias gn='geeknote'

# internet
alias wanip='dig +short myip.opendns.com @resolver1.opendns.com'
alias dmp3='youtube-dl -cx --audio-format mp3 --restrict-filenames'
alias dm4a='youtube-dl -cx --audio-format m4a --restrict-filenames'
alias dogg='youtube-dl -cx --audio-format vorbis --restrict-filenames'
alias dvid='youtube-dl -c --restrict-filenames'
alias yt='youtube-dl'

# tools
alias extension_count="find . -type f | sed 's/.*\.//gI' | sort | uniq -c"
alias clearm="clear; for i in {1..50}; do echo; done"
alias wttrd='curl wttr.in/dabrowa_gornicza'
alias wttrk='curl wttr.in/katowice'


# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

if [ -x /usr/bin/mint-fortune ]; then
     /usr/bin/mint-fortune
fi

function countdown(){
   date1=$((`date +%s` + $1));
   while [ "$date1" -ge `date +%s` ]; do
     echo -ne "$(date -u --date @$(($date1 - `date +%s`)) +%H:%M:%S)\r";
     sleep 0.1
   done
}
function stopwatch(){
  date1=`date +%s`;
   while true; do
    echo -ne "$(date -u --date @$((`date +%s` - $date1)) +%H:%M:%S)\r";
    sleep 0.1
   done
}

# get all descendants of given PID (child processes - direct or indirect)
# return only PIDS:
function getcpid() {
    cpids=`pgrep -P $1|xargs`
    for cpid in $cpids;
    do
        echo "$cpid"
        getcpid $cpid
    done
}
# return ps -f:
function getcpidf() {
    ps -fp $(getcpid $1)
}

# translate english => polish
function t(){ wget -U "Mozilla/5.0" -qO - "http://translate.google.com/translate_a/t?client=t&text=$1&sl=${2:-en}&tl=${3:-pl}" | sed 's/\[\[\[\"//' | cut -d \" -f 1; }

# locate movies
function lom(){ locate -i --regex "$1"'.*\.(avi|mkv|mp4|rmvb|flv|ts)'; }
function lomf(){
    # find /mnt/win_d/filmy "/mnt/d750/filmy HD" -iregex '.*'"$1"'.*\.\(avi\|mkv\|mp4\|rmvb\|flv\|ts\)'
    find /mnt/win_d/filmy -iregex '.*'"$1"'.*\.\(avi\|mkv\|mp4\|rmvb\|flv\|ts\)'
}
function loml(){
    find -L /mnt/win_d/filmy /mnt/win_e/filmy "/mnt/d750/filmy HD" -samefile "$1"
}

# TMUX
alias tl='tmux list-sessions'
alias ta='tmux attach-session'
alias tat='tmux attach-session -t'
alias tn='tmux new-session'
alias tns='tmux new-session -s'

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

# export PS1="\[${Cyan}\]$(((SHLVL>1)) && echo "${SHLVL}\[${IBlack}\].")\[${IGreen}\]\u\[${IBlack}\]@\[${Purple}\]\h\[${IYellow}\] \w \$ \[${Color_Off}\]"
# host/user/full dir
# export PS1="\[${Cyan}\]$(((SHLVL>1)) && echo "${SHLVL}\[${IBlack}\].")\[${IGreen}\]\u\[${IBlack}\]@\[${Purple}\]\h\[${Blue}\]{ \w } \[${BRed}\]» \[${Color_Off}\]"
# host/user/last dir only/git
# export PS1="\[${Cyan}\]$( ((SHLVL>1)) && echo "${SHLVL}\[${IBlack}\]." )\[${IGreen}\]\u\[${IBlack}\]@\[${Purple}\]\h\[${Blue}\]{ \W }\[${Green}\]\$( git rev-parse --abbrev-ref HEAD 2> /dev/null || echo "" ) \[${BRed}\]» \[${Color_Off}\]"

PS1=""
# SHLVL:
PS1+="\[${Cyan}\]$( ((SHLVL>1)) && echo "${SHLVL}\[${IBlack}\]." )"
# user:
PS1+="\[${IGreen}\]\u"
# host:
if [[ "${__myhost}" = "OTHER" ]]; then
    unset __vTmp1
else
    __vTmp1="${__myhost}"
fi
PS1+="\[${IBlack}\]@\[${BBlack}\]${__vTmp1:-\h}"
# if [[ "${__myhost}" != "W" && "${__myhost}" != "H" ]]; then
#     # @host
#     PS1+="\[${IBlack}\]@\[${Purple}\]\h"
# fi
# working dir
PS1+="\[${Blue}\]{\W}"

# # git
if [[ -r "${HOME}/.dotfiles/source/git-prompt.sh" ]]; then
    source "${HOME}/.dotfiles/source/git-prompt.sh"
    PS1+="\[${Yellow}\]"'$(__git_ps1 " (%s)")'
elif hash git 2>/dev/null; then
    PS1+="\[${Green}\]\$( git rev-parse --abbrev-ref HEAD 2> /dev/null || echo -n "")"
fi

# last char based on root or not:
PS1+=" \[${BRed}\]$((($UID == 0)) && echo '#' || echo '»' )"
#Turn colors off + add space
PS1+="\[${Color_Off}\] "

export PS1

case ${__myos} in
    CYGWIN)

        # -----------------------------------------------------------------------
        # -- CYGWIN
        # -----------------------------------------------------------------------

        export LANG=en_US.UTF-8
        #export LC_ALL='C' # needed for uniq to work on polish letters

        # cyginstq() { $(get_param p_cdde)/setup-x86.exe -nqP "$1"; }
        # cyginst()  { $(get_param p_cdde)/setup-x86.exe -nP "$1"; }
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
        # cd windows hosts file
        cd_hosts() {
            cd /cygdrive/c/Windows/System32/drivers/etc
        }
        # cd tnsnames
        cd_tns() {
            cd /cygdrive/c/app/$USER/product/11.2.0/client_1/network/admin
        }

        if [[ ${__myhost} == "W" ]]; then
            fixwinchar()
            {
                iconv -f 852 -t utf8
            }
            proxyoff()
            {
                reg add "hklm\software\wow6432node\microsoft\windows\currentversion\internet settings" /f /v proxyenable /t reg_dword /d 0 |& fixwinchar
                reg add "hklm\software\microsoft\windows\currentversion\internet settings" /f /v proxyenable /t reg_dword /d 0 |& fixwinchar
                reg add "hkcu\software\wow6432node\microsoft\windows\currentversion\internet settings" /f /v proxyenable /t reg_dword /d 0 |& fixwinchar
                reg add "hkcu\software\microsoft\windows\currentversion\internet settings" /f /v proxyenable /t reg_dword /d 0 |& fixwinchar
            }
            alias updatedb='time updatedb --prunepaths="/tmp /var/spool /home/.ecryptfs /cygdrive/j /j /cygdrive/k /k /cygdrive/l /l /cygdrive/m /m /cygdrive/n /n /c /d /proc"'
            fixwin()
            {
                proxyoff
                net share C$ /delete |& fixwinchar
                net share D$ /delete |& fixwinchar
                net share IPC$ /delete |& fixwinchar
                net share ADMIN$ /delete |& fixwinchar
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
    LINUX)

        # -----------------------------------------------------------------------
        # -- LINUX
        # -----------------------------------------------------------------------

        # for NOT ROOT only
        if [ $UID -ne 0 ]; then
            alias reboot='sudo reboot'
            alias apt-get='sudo apt-get'
            alias umount='sudo umount'
            alias ri='gksu roccatiskuconfig &'
        fi

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
        alias aptgo='sudo apt-get update && sudo apt-get -y upgrade && apt-get -fy install && apt-get -y autoremove && apt-get -y autoclean'
        # alias aptgo='sudo apt-get update && sudo apt-get -y upgrade && sudo apt-get -y dist-upgrade && apt-get -fy install && apt-get -y autoremove && apt-get -y autoclean && apt-get -y clean'
        alias iotop='sudo iotop --only'
        alias fping='ping -c 5 -i.2'
        alias dstat_='dstat -lcdpymsn'
        alias steam_dl='env LD_PRELOAD='"'"'/usr/$LIB/libstdc++.so.6 /usr/$LIB/libgcc_s.so.1 /usr/$LIB/libxcb.so.1 /usr/$LIB/libgpg-error.so'"'"' steam'

        if [[ -r /etc/ssl/certs/ca-certificates.crt ]]; then
            export CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
        fi
        ;;
    *)
        echo 'other os?';;

esac
# --- END CASE ---------------------------------------------------------
# translate word in different dictionaries in the browser
e()
{
    local word="$*"
    word="${word// /+}"
    cs "http://dict.pl/dict?word=${word}"
    cs "http://ling.pl/slownik/angielsko-polski/${word}"
    cs "http://en.bab.la/dictionary/english-polish/${word}"
    cs "http://en.pons.com/translate?q=${word}&l=enpl&in=&lf=en"
    cs "http://www.urbandictionary.com/define.php?term=${word}"
    cs "http://www.thefreedictionary.com/${word}"
    cs "http://www.merriam-webster.com/dictionary/${word}"
    cs "https://www.wordnik.com/words/${word}"
    cs "http://dictionary.cambridge.org/dictionary/english/${word}"
    cs "http://dictionary.reference.com/browse/${word}?s=t"
} > /dev/null

# FASD -----------------------------------------------------------------
if hash fasd 2>/dev/null; then

    fasd_cache="$HOME/.fasd-init-bash"
    if [ "$(command -v fasd)" -nt "$fasd_cache" -o ! -s "$fasd_cache" ]; then
        fasd --init posix-alias bash-hook bash-ccomp bash-ccomp-install >| "$fasd_cache"
    fi
    source "$fasd_cache"
    unset fasd_cache

    # eval "$(fasd --init auto)"
    # quick opening files with vim
    alias v='fasd -fe vim'
    alias j='fasd_cd -d'
    case $__myos in
        CYGWIN)
            alias o='fasd -ae cygstart'
            ;;
        Linux)
            alias o='fasd -ae xdg-open'
    esac
    _fasd_bash_hook_cmd_complete v o
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

add_to_path "$HOME/.local/bin"
add_to_path "$HOME/.dotfiles/bin"
add_to_path "$HOME/.dotfiles.local/bin"

# source ~/.bash-git-prompt/gitprompt.sh

function bashrc_info()
{
# -----------------------------------------------------------------------
# -- bash start info
# -----------------------------------------------------------------------
# Today is:
echo "------------------------------------------------------------------"
echo -e "${IYellow}Today is: ${BWhite}$(date +'%F (%A) %T')"

# Last logins:
if [[ ! ${__myos} == CYGWIN* ]]; then
    echo -en "${IYellow}LAST logins:\n${Color_Off}"
    __vTmp3="$(last | uniq | head -13)"
    [[ -n $__vTmp3 ]] && echo -e "${Color_Off}${__vTmp3}"
fi

echo -e "${IYellow}os:${Color_Off} $(uname -o), $(uname -m), $(getconf LONG_BIT) bit"
echo -e "${IYellow}kernel:${Color_Off} $(uname -s)"
echo -e "${IYellow}node:${Color_Off} $(uname -n)"
echo -e "${IYellow}uptime:${Color_Off} $(uptime)"
echo
}

# export PAGER=/usr/local/bin/vimpager
# alias less=$PAGER
# alias zless=$PAGER

# Anaconda3 4.0.0
add_to_path "/home/kossak/anaconda3/bin"

# Linux Brew
if [[ -r "$HOME/.linuxbrew" ]]; then
    add_to_path "$HOME/.linuxbrew/bin"
    export MANPATH="$HOME/.linuxbrew/share/man:$MANPATH"
    export INFOPATH="$HOME/.linuxbrew/share/info:$INFOPATH"
fi

# gpg-agent
# export SSH_AUTH_SOCK_LINK="/tmp/ssh-$USER/agent"
# # if ! [ -r $(readlink -m $SSH_AUTH_SOCK_LINK) ] && [ -r $SSH_AUTH_SOCK ]; then
# if [[ $SSH_AUTH_SOCK_LINK != $SSH_AUTH_SOCK ]] && [[ -r $SSH_AUTH_SOCK ]]; then
# 	mkdir -p "$(dirname $SSH_AUTH_SOCK_LINK)" &&
# 	chmod go= "$(dirname $SSH_AUTH_SOCK_LINK)" &&
# 	ln -sfn $SSH_AUTH_SOCK $SSH_AUTH_SOCK_LINK &&
#     export export SSH_AUTH_SOCK=$SSH_AUTH_SOCK_LINK &&
#     unset SSH_AGENT_PID
# fi

# finishing touches
unset __vTmp1 __vTmp2 __vTmp3
unset __myos __myhost
unset Color_Off Black Red Green Yellow Blue Purple Cyan White BBlack BRed BGreen BYellow BBlue BPurple BCyan BWhite UBlack URed UGreen UYellow UBlue UPurple UCyan UWhite On_Black On_Red On_Green On_Yellow On_Blue On_Purple On_Cyan On_White IBlack IRed IGreen IYellow IBlue IPurple ICyan IWhite BIBlack BIRed BIGreen BIYellow BIBlue BIPurple BICyan BIWhite On_IBlack On_IRed On_IGreen On_IYellow On_IBlue On_IPurple On_ICyan On_IWhite

