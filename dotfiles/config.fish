# setup powerline:
begin
    if type -q powerline-daemon
        powerline-daemon -q
    end
    set -l dirs \
        '/home/kossak/anaconda3/lib/python3.6/site-packages/powerline/bindings/fish' \
        '/home/kossak/.pyenv/versions/anaconda3-5.1.0/lib/python3.6/site-packages/powerline/bindings/fish' \
        '/home/kossak/.pyenv/versions/3.6.4/lib/python3.6/site-packages/powerline/bindings/fish' \
        '/home/kossak/.pyenv/versions/3.6.5/lib/python3.6/site-packages/powerline/bindings/fish'
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
complete --command pipenv --arguments "(env _PIPENV_COMPLETE=complete-fish COMMANDLINE=(commandline -cp) pipenv)" -f

# pyenv
if test -d "$HOME/.pyenv"
    set -x PATH "/home/kossak/.pyenv/bin" $PATH
    status --is-interactive; and . (pyenv init -|psub)
    status --is-interactive; and . (pyenv virtualenv-init -|psub)
end
