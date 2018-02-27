# Defined in /tmp/fish.POpQCr/ranger_cd.fish @ line 2
function ranger_cd
	set -l tempfile '/tmp/chosendir'

    ranger --choosedir $tempfile (pwd)
    if [ -f "$tempfile" ]; and [ (cat -- $tempfile) != (echo -n (pwd)) ]
        cd (cat $tempfile)
    end
    rm -f -- $tempfile
end
