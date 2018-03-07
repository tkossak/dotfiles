function __ssh_is_agent_started -d "return True if ssh-agent is started, otherwise False"
    if not test -f $SSH_ENV
        return 1
    end

    source $SSH_ENV > /dev/null

    if test -z "$SSH_AGENT_PID"; or not ps --pid $SSH_AGENT_PID > /dev/null
        return 1
    end

    return 0
end
