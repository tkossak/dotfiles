# If not running interactively, don't do anything
[[ $- != *i* ]] && return

#set a fancy prompt (non-color, unless we know we "want" color)
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
# [ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# export XONSH_SHOW_TRACEBACK=True

# ----------------------------------------------------------------------
if [[ -r "$HOME/.dotfiles/source/src_bash_vars_myos" ]]; then
    source "$HOME/.dotfiles/source/src_bash_vars_myos"
fi
if [[ -r "$HOME/.dotfiles/source/src_bash_basic_functions" ]]; then
    source "$HOME/.dotfiles/source/src_bash_basic_functions"
fi
if [[ -e "$HOME/.bashrc.local" ]]; then
    source "$HOME/.bashrc.local"
fi

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

# TMUX
alias tl='tmux list-sessions'
alias ta='tmux attach-session'
alias tn='tmux new-session'

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
# if [[ -r "${HOME}/.dotfiles/source/git-prompt.sh" ]]; then
#     source "${HOME}/.dotfiles/source/git-prompt.sh"
#     PS1+="\[${Yellow}\]"'$(__git_ps1 " (%s)")'
# elif hash git 2>/dev/null; then
#     PS1+="\[${Green}\]\$( git rev-parse --abbrev-ref HEAD 2> /dev/null || echo -n "")"
# fi

# last char based on root or not:
PS1+=" \[${BRed}\]$((($UID == 0)) && echo '#' || echo '»' )"
#Turn colors off + add space
PS1+="\[${Color_Off}\] "

export PS1

# paths
# if [[ -e "$HOME/.local/bin" ]]; then
#     add_to_path "$HOME/.local/bin"
# fi
# if [[ -e "$HOME/.dotfiles/bin" ]]; then
#     add_to_path "$HOME/.dotfiles/bin"
# fi
# if [[ -e "$HOME/.dotfiles.local/bin" ]]; then
#     add_to_path "$HOME/.dotfiles.local/bin"
# fi

# Anaconda3 4.0.0
# if [[ -e "/home/kossak/anaconda3/bin" ]]; then
#     add_to_path "/home/kossak/anaconda3/bin"
# fi

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

