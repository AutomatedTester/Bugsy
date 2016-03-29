try:
    from urllib import parse
except:
    import urllib as parse
from bugsy import Bugsy


def rest_url(*parts, **kwargs):
    base = '/'.join(['https://bugzilla.mozilla.org/rest'] +
                    [str(p) for p in parts])
    kwargs.setdefault('include_fields', Bugsy.DEFAULT_SEARCH)
    params = parse.urlencode(kwargs, True)
    if params:
        return '%s?%s' % (base, params)
    return base
