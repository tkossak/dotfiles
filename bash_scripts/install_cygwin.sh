#!/usr/bin/env bash

# set -o errexit
set -o pipefail
set -o nounset
# set -o xtrace

# Set magic variables for current file & dir
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
#__root="$(cd "$(dirname "${__dir}")" && pwd)" # <-- change this
__file="${__dir}/$(basename "${BASH_SOURCE[0]}")"
#__base="$(basename ${__file} .sh)"

# arg1="${1:-}"

# function creating links
create_link()
{

    file_src="$1"
    file_dst="$2"

    if [[ -e "$file_src" ]]; then
        if  [[ -L "$file_dst" ]]; then
            rm "$file_dst"
        elif [[ -e "$file_dst" ]]; then
            "ERROR: File_dst $file_dst already exists"
            return 1
        fi
        ln -s "$file_src" "$file_dst"
        echo "OK: Created link $file_dst (to $file_src)"
    else
        echo "ERROR: No $file_src file"
        return 1
    fi
}



# ffmpeg links
src_path="/cygdrive/c/Program Files/ffmpeg/bin"
dst_path="/usr/bin"
create_link "${src_path}/ffmpeg.exe" "${dst_path}/ffmpeg"
create_link "${src_path}/ffplay.exe" "${dst_path}/ffplay"
create_link "${src_path}/ffprobe.exe" "${dst_path}/ffprobe"

# dotfiles scripts
src_path="${__dir}"
dst_path="/usr/bin"
create_link "${src_path}/txz.sh" "${dst_path}/txz"
create_link "${src_path}/txzm.sh" "${dst_path}/txzm"
create_link "${src_path}/create_bash.sh" "${dst_path}/create_bash"


