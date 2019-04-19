# Defined in /tmp/fish.Gh8SiW/tarb.fish @ line 2
function tarb
	if [ (count $argv) = 0 ]
        echo 'Provide at least one argument!'
        return
    else if [ (count $argv) = 1 ]
        set -l new_file "$argv[1]".(date +'%Y%m%d_%H%M%S').tar.gz
        set -l new_file (string replace -a '/' '' $new_file)
        tar -cavf $new_file $argv
    else
        set -l new_file backup.(date +'%Y%m%d_%H%M%S').tar.gz
        tar -cavf $new_file $argv
    end
end
