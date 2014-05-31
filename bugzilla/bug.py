class Bug(object):
    """This represents a bug"""

    _bug = {}

    def __init__(self, **kwargs):
        self._bug['summary'] = kwargs.get('summary', '')

    def summary():
        doc = "The summary property."
        def fget(self):
            return self._bug['summary']
        def fset(self, value):
            self._bug['summary'] = value
        def fdel(self):
            del self._bug['summary']
        return locals()
    summary = property(**summary())
