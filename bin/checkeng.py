#!/usr/bin/env python3

# TODO: add first argument as file
# TODO: if no file provided, process stdin

from collections import Counter
import itertools

omit_words = """
a
as
be
by
for
get
give
have
i
in
is
lot
me
my
not
off
on
sb
that
the
their
this
to
up
was
we
will
you
""".strip().split()

words = Counter()
go = 0
with open('from_simplenote.txt', 'r') as fh:
    # for line in fh:
    for line in itertools.dropwhile(
            lambda x: not x.startswith(r'\-- learn zero'),
            fh):
        if line.startswith(r'\--'):
            continue
        for word in line.split():
            word = word.lower()
            if word in omit_words:
                continue
            else:
                words[word] += 1
                break

for w in sorted(words.most_common(20),
                key=lambda x: (x[1], x[0]), reverse=True):
    print('{:2} : {}'.format(w[1], w[0]))
