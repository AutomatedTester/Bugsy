class BugException(Exception):
    """If trying to do something to a Bug this will be thrown"""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "Message: %s" % self.msg


class Bug(object):
    """This represents a Bugzilla Bug"""

    _bug = {'id':None}

    def __init__(self, **kwargs):
        """
            Defaults are set if there are no kwargs passed in. To pass in
            a dict create the Bug object like the following
              bug = Bug(**myDict)
        """
        self._bug['id'] = kwargs.get('id', None)
        self._bug['summary'] = kwargs.get('summary', '')
        self._bug['status'] = kwargs.get('status', '')

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

    def status():
        doc = "The status property."
        def fget(self):
            return self._bug['status']
        def fset(self, value):
            if self._bug['id']:
                self._bug['status'] = value
            else:
                raise BugException("Can not set status unless there is a bug id. Please call Update() before setting")
        def fdel(self):
            del self._bug['status']
        return locals()
    status = property(**status())

    def id():
        doc = "The id property."
        def fget(self):
            return self._bug['id']
        return locals()
    id = property(**id())
