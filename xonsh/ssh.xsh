
def _setup_ssh_agent(args):
    ssh_agent_env=pf'{$XDG_RUNTIME_DIR}/ssh-agent.env'
    ssh_sockets = (
        pf'{$XDG_RUNTIME_DIR}/keyring/ssh',
        pf'{$XDG_RUNTIME_DIR}/keyring/.ssh'
    )

    if not $(pgrep -u $USER ssh-agent):
        print('Create new ssh-agent')
        ssh_agent_env.write_text($(ssh-agent -s -a @(ssh_sockets[0])))
        source-bash --suppress-skip-message @(ssh_agent_env)
        tmux setenv SSH_AUTH_SOCK $SSH_AUTH_SOCK
        tmux setenv SSH_AGENT_PID $SSH_AGENT_PID
    else:
        print('ssh-agent already running')
        if ssh_agent_env.exists():
            print(f'Use existing variables from {ssh_agent_env}')
            source-bash --suppress-skip-message @(ssh_agent_env)
            tmux setenv SSH_AUTH_SOCK $SSH_AUTH_SOCK
            tmux setenv SSH_AGENT_PID $SSH_AGENT_PID
            return

        for p in ssh_sockets:
            if p.exists():
                # maybe: check if current user is the owner?
                print(f'{ssh_agent_env} not found, but using existing socket: {p}')
                $SSH_AUTH_SOCK = p
                tmux setenv SSH_AUTH_SOCK $SSH_AUTH_SOCK
                # TODO maybe: search which ssh-agent process is using the socket, and also export its PID to $SSH_AGENT_PID?
                break
        else:
            print(f'{ssh_agent_env} not found! killall ssh-agent')

aliases['sshagent'] = _setup_ssh_agent