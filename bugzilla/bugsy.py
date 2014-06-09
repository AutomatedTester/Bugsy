import json

import requests
from bug import Bug

class BugsyException(Exception):
    """If trying to do something to a Bug this will be thrown"""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "Message: %s" % self.msg

class LoginException(Exception):
    """If trying to do something to a Bug this will be thrown"""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "Message: %s" % self.msg

class Bugsy(object):
    """docstring for Bugsy"""
    def __init__(self, username=None, password=None, bugzilla_url='https://bugzilla.mozilla.org/rest'):
        self.username = username
        self.password = password
        self.token = None
        self.bugzilla_url = bugzilla_url
        if self.username and self.password:
            result = requests.get(bugzilla_url + '/login?login=%s&password=%s' % (self.username, self.password)).json()
            if result.has_key('token'):
                self.token = result['token']
            else:
                raise LoginException(result['message'])

    def get(self, bug_number):
        bug = requests.get(self.bugzilla_url + "/bug/%s" % bug_number).json()
        return Bug(self.bugzilla_url, self.token, **bug['bugs'][0])

    def put(self, bug):
        if (not self.username or not self.password) or not self.token:
            raise BugsyException("Unfortunately you can't put bugs in Bugzilla without credentials")

        if not isinstance(bug, Bug):
            raise BugsyException("Please pass in a Bug object when posting to Bugzilla")

        if not bug.id:
            result = requests.post(self.bugzilla_url + "/bug?token=%s" % self.token, bug.to_dict())
            bug._bug['id'] = json.loads(result.content)['id']
        else:
            requests.post(self.bugzilla_url + "/bug/%s?token=%s" % (bug.id, self.token), bug.to_dict())

