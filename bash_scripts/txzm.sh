#!/usr/bin/env bash

# compress files into tar.xz
# $N - last argument is archive name
# $1-(N-1) - files to compress
# If there is only one argument, archive name is created automatically


# set -o errexit
set -o pipefail
set -o nounset
# set -o xtrace

if (( $# == 0 )); then
    echo "No arguments."
    exit 1
elif (( $# == 1 )); then
    file_in=( "$1" )
    file_out="${1%%/}.tar.xz"
else
    file_in=( "${@:1:$#-1}" )
    file_out="${@: -1}"
fi


if [[ -e $file_out ]]; then
    echo "Output file: $file_out already exists!"
    exit 1;
fi

# compress
tar -cvf - "${file_in[@]}" | xz -e9zf - > "${file_out}"
if [[ "$?" != "0" ]]; then
    echo -n "ERROR compressing files. Removing archive..."
    rm "${file_out}"
    echo " Done."
    exit 1
fi

echo
echo "Testing ${file_out}..."
echo

# test
tar -tJf "${file_out}"
if [[ "$?" = "0" ]]; then
    echo
    echo "OK test."
else
    echo
    echo -n "ERROR: archive broken! Removing archive..."
    rm "${file_out}"
    echo " Done."
    exit 2
fi

# remove src
echo -n "Removing original files..."
rm -rf "${file_in}"
if [[ "$?" = "0" ]]; then
    echo " Done."
else
    echo
    echo "ERROR removing original files"
    exit 3
fi

