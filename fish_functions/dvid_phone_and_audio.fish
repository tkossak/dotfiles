# Defined in /tmp/fish.r2ELv9/dvid_phone_and_audio.fish @ line 2
function dvid_phone_and_audio
	youtube-dl -kx -f "worstvideo[height>=480]+bestaudio[abr<=128]" -o '%(title)s_%(id)s.%(ext)s' $argv
end
