import requests


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

    def __init__(self, bugzilla_url=None, token=None, **kwargs):
        """
            Defaults are set if there are no kwargs passed in. To pass in
            a dict create the Bug object like the following
              bug = Bug(**myDict)
        """
        self.bugzilla_url = bugzilla_url
        self.token = token
        self._bug = dict(**kwargs)

    def id():
        doc = "The id property."
        def fget(self):
            return self._bug.get('id', None)
        return locals()
    id = property(**id())

    def summary():
        doc = "The summary property."
        def fget(self):
            return self._bug.get('summary', '')
        def fset(self, value):
            self._bug['summary'] = value
        def fdel(self):
            del self._bug['summary']
        return locals()
    summary = property(**summary())

    def status():
        doc = "The status property."
        def fget(self):
            return self._bug.get('status', '')
        def fset(self, value):
            if self._bug.get('id', None):
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

    def update(self):
        if self._bug.has_key('id'):
            result = requests.get(self.bugzilla_url + "/bug/%s" % self._bug['id']).json()
            self._bug = dict(**result['bugs'][0])
        else:
            raise BugException("Unable to update bug that isn't in Bugzilla")
