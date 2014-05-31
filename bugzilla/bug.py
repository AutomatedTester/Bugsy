class Bug(object):
    """This represents a bug"""
    def __init__(self, _summary=''):
        self._summary = _summary

    def summary():
        doc = "The summary property."
        def fget(self):
            return self._summary
        def fset(self, value):
            self._summary = value
        def fdel(self):
            del self._summary
        return locals()
    summary = property(**summary())
