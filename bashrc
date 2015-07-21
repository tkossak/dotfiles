# If not running interactively, don't do anything
[[ -z "$PS1" ]] && return

# set a fancy prompt (non-color, unless we know we "want" color)
# case "$TERM" in
# xterm-color) color_prompt=yes;;
# esac
color_prompt=yes;

# export TERM=screen
export TERM=screen-256color
# export TERM=screen-256color-bce
# export TERM=xterm-256color

# [[ -z "$TMUX" ]] && exec tmux attach

# eval `dircolors ~/.dir_colors`

# Reset
Color_Off='\e[0m' # Text Reset

# Regular Colors
Black='\e[0;30m' # Black
Red='\e[0;31m' # Red
Green='\e[0;32m' # Green
Yellow='\e[0;33m' # Yellow
Blue='\e[0;34m' # Blue
Purple='\e[0;35m' # Purple
Cyan='\e[0;36m' # Cyan
White='\e[0;37m' # White

# Bold
BBlack='\e[1;30m' # Black
BRed='\e[1;31m' # Red
BGreen='\e[1;32m' # Green
BYellow='\e[1;33m' # Yellow
BBlue='\e[1;34m' # Blue
BPurple='\e[1;35m' # Purple
BCyan='\e[1;36m' # Cyan
BWhite='\e[1;37m' # White

# Underline
UBlack='\e[4;30m' # Black
URed='\e[4;31m' # Red
UGreen='\e[4;32m' # Green
UYellow='\e[4;33m' # Yellow
UBlue='\e[4;34m' # Blue
UPurple='\e[4;35m' # Purple
UCyan='\e[4;36m' # Cyan
UWhite='\e[4;37m' # White

# Background
On_Black='\e[40m' # Black
On_Red='\e[41m' # Red
On_Green='\e[42m' # Green
On_Yellow='\e[43m' # Yellow
On_Blue='\e[44m' # Blue
On_Purple='\e[45m' # Purple
On_Cyan='\e[46m' # Cyan
On_White='\e[47m' # White

# High Intensity
IBlack='\e[0;90m' # Black
IRed='\e[0;91m' # Red
IGreen='\e[0;92m' # Green
IYellow='\e[0;93m' # Yellow
IBlue='\e[0;94m' # Blue
IPurple='\e[0;95m' # Purple
ICyan='\e[0;96m' # Cyan
IWhite='\e[0;97m' # White

# Bold High Intensity
BIBlack='\e[1;90m' # Black
BIRed='\e[1;91m' # Red
BIGreen='\e[1;92m' # Green
BIYellow='\e[1;93m' # Yellow
BIBlue='\e[1;94m' # Blue
BIPurple='\e[1;95m' # Purple
BICyan='\e[1;96m' # Cyan
BIWhite='\e[1;97m' # White

# High Intensity backgrounds
On_IBlack='\e[0;100m' # Black
On_IRed='\e[0;101m' # Red
On_IGreen='\e[0;102m' # Green
On_IYellow='\e[0;103m' # Yellow
On_IBlue='\e[0;104m' # Blue
On_IPurple='\e[0;105m' # Purple
On_ICyan='\e[0;106m' # Cyan
On_IWhite='\e[0;107m' # White

# ----------------------------------------------------------------------
# set -o vi
# bind -m vi-command ".":insert-last-argument

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=10000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# ----------------------------------------------------------------------

if [ -f ~/.bashrc.local ]; then
    source ~/.bashrc.local
fi

export EDITOR=vim

alias ll='ls -lFh --color=auto'
alias lla='ls -lAFh --color=auto'
alias ls='ls -F --color=auto'
alias la='ls -AF --color=auto'
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

alias dmp3='youtube-dl -cx --audio-format mp3 --restrict-filenames'
alias dvid='youtube-dl -c --restrict-filenames'
alias yt='youtube-dl'
alias tmuxa='tmux attach'
alias tmuxl='tmux list-sessions'
alias gn='geeknote'

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

_myos="$(uname)"
_myhost="$(uname -n)"

case ${_myos} in
CYGWIN*)

# -----------------------------------------------------------------------
# -- CYGWIN
# -----------------------------------------------------------------------

export LANG=en_US.UTF-8
#export LC_ALL='C' # needed for uniq to work on polish letters

cyginstq() { $(get_param p_cdde)/setup-x86.exe -nqP "$1"; }
cyginst()  { $(get_param p_cdde)/setup-x86.exe -nP "$1"; }
cs() { cygstart $*; }

_vTmp1="$(get_param p_cdp)"
_vTmp2="$(get_param p_ccp)"
if [ -e "${_vTmp1}/Nmap/nmap.exe" ]; then
    alias nmap="\"${_vTmp1}/Nmap/nmap.exe\""
elif [ -e "${_vTmp2}/Nmap/nmap.exe" ]; then
    alias nmap="\"${_vTmp2}/Nmap/nmap.exe\""
fi

#------------------
# Win variables
_vTmpPathCyg="$(get_param p_temp_cyg)"
#_vTmpPathWin="$(cygpath -aw ${_vTmpPathCyg})"
_vTmp1="$(get_param p_cdkp)"
_vTmp2="$(get_param p_cedpp)"
if [[ -e $_vTmp1 ]]; then
    _vProgsPath="$_vTmp1"
elif [[ -e $_vTmp2 ]]; then
    _vProgsPath="$_vTmp2"
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


if [[ $_myhost == "$(get_param whost)" ]]; then
    proxyoff()
    {
        reg add "hklm\software\wow6432node\microsoft\windows\currentversion\internet settings" /f /v proxyenable /t reg_dword /d 0
        reg add "hklm\software\microsoft\windows\currentversion\internet settings" /f /v proxyenable /t reg_dword /d 0
        reg add "hkcu\software\wow6432node\microsoft\windows\currentversion\internet settings" /f /v proxyenable /t reg_dword /d 0
        reg add "hkcu\software\microsoft\windows\currentversion\internet settings" /f /v proxyenable /t reg_dword /d 0
    }
    alias updatedb='time updatedb --prunepaths="/tmp /var/spool /home/.ecryptfs /cygdrive/k /cygdrive/l /cygdrive/m /cygdrive/n /proc"'
fi


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


e()
{
    cs "http://dict.pl/dict?word=$1" >/dev/null
    cs "http://ling.pl/slownik/angielsko-polski/$1" >/dev/null
    cs "http://en.bab.la/dictionary/english-polish/$1" >/dev/null
    cs "http://www.thefreedictionary.com/$1" >/dev/null
    cs "http://en.pons.com/translate?q=$1&l=enpl&in=&lf=en" > /dev/null
}


# FASD -----------------------------------------------------------------
if hash fasd 2>/dev/null; then
    eval "$(fasd --init auto)"
    alias v='f -e vim' # quick opening files with vim
    alias j='fasd_cd -d'
    case $_myos in
        CYGWIN*)
            alias o='a -e cygstart'
            ;;
        Linux)
            alias o='a -e xdg-open'
    esac
    _fasd_bash_hook_cmd_complete f a s d v o
fi


# COMMACD: -------------------------------------------------------------
source ~/.commacd.bash


# fzf ------------------------------------------------------------------
if hash fzf 2>/dev/null; then
    [ -f ~/.fzf.bash ] && source ~/.fzf.bash
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

export PATH=~/.dotfiles/bin:${PATH}
# source ~/.bash-git-prompt/gitprompt.sh

# -----------------------------------------------------------------------
# -- bash start info
# -----------------------------------------------------------------------
# Today is:
echo "------------------------------------------------------------------"
echo -e "${IYellow}Today is: ${BWhite}$(date +'%F (%A) %T')"

# # Uptime:
# _vTmp3="$(uptime | sed -e 's:,[^,]\+user.*::I;s/.*up\s\+//')"
# [[ -n $_vTmp3 ]] && echo -e " ${IYellow}UPTIME:${BWhite} ${_vTmp3}" || echo ""

# # Tmux:
# _vTmp3="$(tmux list-sessions 2>/dev/null)"
# [[ -n $_vTmp3 ]] && echo -e "${IYellow}TMUX:${Color_Off} ${_vTmp3}"

# # Is Internet on Fire:
# if [[ "$_myhost" != "dziura" ]]; then
# echo -e "${IYellow}IS INTERNET ON FIRE?${Color_Off}"
# host -t txt istheinternetonfire.com | cut -f 2- -d '"' | sed 's/\. /\n/g;s/ http/\nhttp/g;s/\\;/;/g;s/" "//g;s/"$//g'
# echo
# fi

# Last logins:
if [[ ${_myos} == CYGWIN* ]]; then
    :
else
    echo -en "${IYellow}LAST logins:\n${Color_Off}"
    _vTmp3="$(last | uniq | head -13)"
    [[ -n $_vTmp3 ]] && echo -e "${Color_Off}${_vTmp3}"
fi


# finishing touches
unset _vTmp1 _vTmp2 _vTmp3
unset _myos _myhost

unset Color_Off Black Red Green Yellow Blue Purple Cyan White BBlack BRed BGreen BYellow BBlue BPurple BCyan BWhite UBlack URed UGreen UYellow UBlue UPurple UCyan UWhite On_Black On_Red On_Green On_Yellow On_Blue On_Purple On_Cyan On_White IBlack IRed IGreen IYellow IBlue IPurple ICyan IWhite BIBlack BIRed BIGreen BIYellow BIBlue BIPurple BICyan BIWhite On_IBlack On_IRed On_IGreen On_IYellow On_IBlue On_IPurple On_ICyan On_IWhite
