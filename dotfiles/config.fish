set -gx EDITOR vim
set -gx BROWSER opera

# set JAVA_HOME path, if it is not set already
# set -l dir_java "/usr/lib/jvm/java-8-openjdk-amd64"
set -l dir_java "/home/kossak/apps/jdk1.8.0_221"
if not set -q JAVA_HOME; and test -d "$dir_java"
    set -x JAVA_HOME "$dir_java"
end

# ssh-agent
# if test -z "$SSH_ENV"
#     set -xg SSH_ENV $HOME/.ssh/environment
# end
# if not __ssh_is_agent_started
#     __ssh_agent_start
# end

# powerline:
begin
    if type -q powerline-daemon
        powerline-daemon -q
    end
    set -l dirs \
        '/home/kossak/.asdf/installs/python/3.9.9/lib/python3.9/site-packages/powerline/bindings/fish' \
        '/home/kossak/.asdf/installs/python/3.9.7/lib/python3.9/site-packages/powerline/bindings/fish' \
        '/home/kossak/.asdf/installs/python/3.8.6/lib/python3.8/site-packages/powerline/bindings/fish' \
        '/home/kossak/.asdf/installs/python/3.6.9/lib/python3.6/site-packages/powerline/bindings/fish' \
        '/home/kossak/.asdf/installs/python/3.6.8/lib/python3.6/site-packages/powerline/bindings/fish' \
        '/home/kossak/.asdf/installs/python/3.6.6/lib/python3.6/site-packages/powerline/bindings/fish'
    for dir in $dirs
        if test -d "$dir"
            set fish_function_path $fish_function_path "$dir"
            powerline-setup
            break
        end
    end
end

# asdf:
set -l asdf_file "$HOME/.asdf/asdf.fish"
if test -r "$asdf_file"
    source "$asdf_file"
end
