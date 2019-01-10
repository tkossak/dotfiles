# remove asdf folders from $PATH), so you can have system python
function asdf_disable
	set PATH (string match -v /home/kossak/.asdf/shims $PATH)
    set PATH (string match -v /home/kossak/.asdf/bin $PATH)
    for p in $PATH
        echo $p
    end
end
