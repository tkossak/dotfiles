# remove asdf folders from $PATH), so you can have system python
function asdf_disable
    # var used later to restore paths:
    set -g OLD_PATH $PATH
    set PATH (string match -v /home/kossak/.asdf/shims $PATH)
    set PATH (string match -v /home/kossak/.asdf/bin $PATH)
    which python
    which pip
end
