# Defined in /tmp/fish.POpQCr/ranger_cd.fish @ line 2
function ranger_cd
	set -l tempfile '/tmp/chosendir'

    __fish_disable_bracketed_paste
    ranger --choosedir $tempfile (pwd)
    __fish_enable_bracketed_paste
    if [ -f "$tempfile" ]; and [ (cat -- $tempfile) != (echo -n (pwd)) ]
        cd (cat $tempfile)
    end
    rm -f -- $tempfile
end
