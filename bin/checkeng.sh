#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
# set -o xtrace

# Set magic variables for current file & dir
# __dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# __file="${__dir}/$(basename "${BASH_SOURCE[0]}")"
# __base="$(basename ${__file} .sh)"
# __root="$(cd "$(dirname "${__dir}")" && pwd)"

# magic variables for links
#__file="$(readlink -f ${BASH_SOURCE[0]})"
#__dir="$(cd "$(dirname "${__file}")" && pwd)"


# sed -r '
# s/[,.!?]/ /g;
# s/\s{2,}/ /g;
# s/^\s+//g;
# s/\s+$//g;
# s/\<a\s+//g;
# s/\<the\s+//g' | cut -d' ' -f1 | sort | uniq -c | sort


sed -r -e '
s/[,.!?]/ /g;
s/\s{2,}/ /g;
s/^\s+//g;
s/\s+$//g;
s/\s+/\n/g;
' | sed -r '
/^is$/d;
/^the$/d;
/^sb$/d;
/^for$/d;
/^be$/d;
/^this$/d;
/^off$/d;
/^my$/d;
/^\)$/d;
/^-$/d;
/^i$/d;
/^you$/d;
/^their$/d;
/^on$/d;
/^lot$/d;
/^have$/d;
/^was$/d;
/^that$/d;
/^get$/d;
/^by$/d;
/^as$/d;
/^we$/d;
/^will$/d;
/^\(v\)$/d;
/^\(n\)$/d;
/^not?$/d;
/^not$/d;
' | sort | uniq -c | sort
