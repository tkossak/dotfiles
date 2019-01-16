# restore $PATH from $OLD_PATH variable
function asdf_restore
    if set -q OLD_PATH
        set -x PATH $OLD_PATH
        which python
        which pip
    else
        echo Run asdf_disable first!
    end
end
