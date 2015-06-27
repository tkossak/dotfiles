#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
# set -o xtrace

# magic variables for links
__file="$(readlink -f ${BASH_SOURCE[0]})"
__dir="$(cd "$(dirname "${__file}")" && pwd)"

arg1="${1:-}"
model="${__dir}/create_bash.model"

if [[ -z "$arg1" ]]; then
    echo "No filename given."
    exit 1
elif [[ -e "$arg1" ]]; then
    echo "File already exists."
    exit 2
fi

cat "$model" > "$arg1"
chmod u+x "$arg1"

