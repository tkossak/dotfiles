# set JAVA_HOME path, if it is not set already
set -l dir_java "/usr/lib/jvm/java-8-openjdk-amd64"
if test -d "$dir_java"; and not set -q JAVA_HOME
    set -x JAVA_HOME "$dir_java"
end

# setup powerline:
begin
    if type -q powerline-daemon
        powerline-daemon -q
    end
    set -l dirs \
        '/home/kossak/.pyenv/versions/3.6.5/lib/python3.6/site-packages/powerline/bindings/fish' \
        '/home/kossak/anaconda3/lib/python3.6/site-packages/powerline/bindings/fish' \
        '/home/kossak/.pyenv/versions/miniconda3-4.3.30/lib/python3.6/site-packages/powerline/bindings/fish'
    for dir in $dirs
        if test -d "$dir"
            set fish_function_path $fish_function_path "$dir"
            powerline-setup
            break
        end
    end
end

# ssh-agent
if test -z "$SSH_ENV"
    set -xg SSH_ENV $HOME/.ssh/environment
end

if not __ssh_is_agent_started
    __ssh_agent_start
end

# pipenv completions
# should be this, but it's slow:
# eval (pipenv --completion)
# complete --command pipenv --arguments "(env _PIPENV_COMPLETE=complete-fish COMMANDLINE=(commandline -cp) pipenv)" -f

# pyenv
set -l pyenv_root "$HOME/.pyenv"
if test -d "$pyenv_root"
    # remove these PATHs if they already exist in $PATH
    if string match "$pyenv_root/bin" $PATH > /dev/null
        set -x PATH (string match -v "$pyenv_root/bin" $PATH)
        set -x PATH (string match -v "$pyenv_root/shims" $PATH)
        set -x PATH (string match -v "$pyenv_root/plugins/pyenv-virtualenv/shims" $PATH)
    end
    # set $PATH:
    set -x PATH "$pyenv_root/bin" $PATH
    # auto complete:
    status --is-interactive; and . (pyenv init -|psub)
    status --is-interactive; and . (pyenv virtualenv-init -|psub)
end

