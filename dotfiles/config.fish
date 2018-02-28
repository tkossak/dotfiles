# setup powerline:
if type -q powerline-daemon
  powerline-daemon -q
end
set fish_function_path $fish_function_path "/home/kossak/anaconda3/lib/python3.6/site-packages/powerline/bindings/fish"
powerline-setup

# ssh-agent
if test -z "$SSH_ENV"
    set -xg SSH_ENV $HOME/.ssh/environment
end

if not __ssh_agent_is_started
    __ssh_agent_start
end
