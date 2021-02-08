# Defined in /tmp/fish.BEwqOu/watch_tvtrwam.fish @ line 1
function net_monitor
    # 0 - top left
    tmux new-window -n 'NET monitor'
    tmux send-keys 'mtr -no "LRD N ABWV" 192.168.0.1' Enter

    # 2 - top right
    tmux split-window -h
    tmux send-keys 'mtr -o "LRD N ABWV" 192.168.202.68' Enter

    # 3 - bottom right
    tmux split-window -v
    tmux send-keys 'watch -n 1 "ip r"' Enter

    # 1 - bottom left
    tmux select-pane -t 0
    tmux split-window -v
    tmux send-keys 'mtr -o "LRD N ABWV" google.pl' Enter
end
