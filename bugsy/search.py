import requests
from bug import Bug


class Search(object):
    """

    """
    def __init__(self, bugzilla_url, token):
        self.bugzilla_url = bugzilla_url
        self.token = token

    def include_fields(self, *args):
        self.include_fields = list(args)
        return self

    def search(self):
        include_fields = ""
        for field in self.include_fields:
            include_fields = include_fields + "include_fields=%s" % field
        results = requests.get(self.bugzilla_url +"?" + include_fields).json()
        return [Bug(self.bugzilla_url, self.token, **bug) for bug in results['bugs']]