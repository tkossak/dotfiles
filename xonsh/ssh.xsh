
def _setup_ssh_agent(args):
    _SSH_AGENT_ENV=pf'{$XDG_RUNTIME_DIR}/ssh-agent.env'
    if not $(pgrep -u $USER ssh-agent):
        print('Create new ssh-agent')
        _SSH_AGENT_ENV.write_text($(ssh-agent -s))
        source-bash @(_SSH_AGENT_ENV)
        tmux setenv SSH_AUTH_SOCK $SSH_AUTH_SOCK
        tmux setenv SSH_AGENT_PID $SSH_AGENT_PID
    else:
        if _SSH_AGENT_ENV.exists():
            print('Use existing variables')
            source-bash @(_SSH_AGENT_ENV)
            tmux setenv SSH_AUTH_SOCK $SSH_AUTH_SOCK
            tmux setenv SSH_AGENT_PID $SSH_AGENT_PID
        else:
            echo "ssh-agent is running but _SSH_AGENT_ENV not found! killall ssh-agent"

aliases['sshagent'] = _setup_ssh_agent