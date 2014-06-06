VALID_STATUS = ["RESOLVED", "ASSIGNED", "NEW", "UNCONFIRMED"]
VALID_RESOLUTION = ["FIXED", "INCOMPLETE", "INVALID", "WORKSFORME", "DUPLICATE", "WONTFIX"]



class BugException(Exception):
    """If trying to do something to a Bug this will be thrown"""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "Message: %s" % self.msg


class Bug(object):
    """This represents a Bugzilla Bug"""

    _bug = {'id':None}

    def id():
        doc = "The id property."
        def fget(self):
            return self._bug['id']
        return locals()
    id = property(**id())

    def __init__(self, **kwargs):
        """
            Defaults are set if there are no kwargs passed in. To pass in
            a dict create the Bug object like the following
              bug = Bug(**myDict)
        """
        self._bug['id'] = kwargs.get('id', None)
        self._bug['summary'] = kwargs.get('summary', '')
        self._bug['status'] = kwargs.get('status', '')
        self._bug['resolution'] = kwargs.get('resolution', '')

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
                if value in VALID_STATUS:
                    self._bug['status'] = value
                else:
                    raise BugException("Invalid status type was used")
            else:
                raise BugException("Can not set status unless there is a bug id. Please call Update() before setting")
        def fdel(self):
            del self._bug['status']
        return locals()
    status = property(**status())

    def resolution():
        doc = "The resolution property."
        def fget(self):
            return self._bug['resolution']
        def fset(self, value):
            if value in VALID_RESOLUTION:
                self._bug['resolution'] = value
            else:
                raise BugException("Invalid resolution type was used")
        def fdel(self):
            del self._bug['resolution']
        return locals()
    resolution = property(**resolution())

    def to_dict(self):
        return self._bug