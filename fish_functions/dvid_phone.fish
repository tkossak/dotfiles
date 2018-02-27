# Defined in /tmp/fish.XBe3hn/dvid_phone.fish @ line 1
function dvid_phone
	youtube-dl -f "worstvideo[height>=480]+bestaudio[abr<=128]" -o '%(title)s_%(id)s.%(ext)s' $argv
end
