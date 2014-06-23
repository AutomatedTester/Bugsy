import requests
from bug import Bug


class Search(object):
    """

    """
    def __init__(self, bugzilla_url, token):
        self.bugzilla_url = bugzilla_url
        self.token = token
        self.includefields = []
        self.keywrds = []

    def include_fields(self, *args):
        self.includefields = list(args)
        return self

    def keywords(self, *args):
        self.keywrds = list(args)
        return self

    def search(self):
        include_fields = ""
        for field in self.includefields:
            include_fields = include_fields + "include_fields=%s&" % field

        keywrds = ""
        for word in self.keywrds:
            keywrds = keywrds + "keywords=%s&" % word
        url = self.bugzilla_url +"?" + include_fields + keywrds
        if self.token:
            url = url + "token=%s" % self.token
        results = requests.get(url).json()
        return [Bug(self.bugzilla_url, self.token, **bug) for bug in results['bugs']]