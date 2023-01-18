def _asdf_disable(args):
    for p in [
        p'~/.asdf/shims',
        p'~/.asdf/bin',
    ]:
        if str(p) in $PATH:
            $PATH.remove(str(p))

def _asdf_enable(args):
    paths = [
        p'~/.asdf/shims',
        p'~/.asdf/bin',
    ]
    paths = [str(p) for p in paths if p.exists()]
    $PATH = paths + [p for p in $PATH if p not in paths]

aliases['asdf_disable'] = _asdf_disable
aliases['asdf_enable'] = _asdf_enable
