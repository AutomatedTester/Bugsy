import requests
from bug import Bug


class Search(object):
    """
        This allows searching for bugs in Bugzilla
    """
    def __init__(self, bugzilla_url, token):
        """
            Initialises the search object

            :param bugzilla_url: This is the Bugzilla REST URL endpoint. Defaults to None
            :param token: Login token generated when instantiating a Bugsy() object with
                          a valid username and password
        """
        self.bugzilla_url = bugzilla_url
        self.token = token
        self.includefields = []
        self.keywrds = []
        self.assigned = []

    def include_fields(self, *args):
        """
            Include fields is the fields that you want to be returned when searching

            :param args:
            :return self: return the original object you were using allowing for fluent
                          searches

            >>> bugzilla.search_for.include_fields("summary", "product")
        """
        self.includefields = list(args)
        return self

    def keywords(self, *args):
        """
            When search() is called it will search for the keywords passed in here

            :param args:
            :return self: return the original object you were using allowing for fluent
                          searches

            >>> bugzilla.search_for.keywords("checkin-needed")
        """
        self.keywrds = list(args)
        return self

    def assigned_to(self, *args):
        """
            When search() is called it will search for bugs assigned to these users
            :param args:
            :return self: return the original object you were using allowing for fluent
            searches

            >>> bugzilla.search_for.assigned_to("dburns@mozilla.com")
        """
        self.assigned = list(args)
        return self

    def search(self):
        r"""
            Call the Bugzilla endpoint that will do the search. It will take the information
            used in other methods on the Search object and build up the query string. If no
            bugs are found then an empty list is returned.

            >>> bugs = bugzilla.search_for\
            ...                .keywords("checkin-needed")\
            ...                .include_fields("product", "Summary")\
            ...                .search()
        """
        include_fields = ""
        for field in self.includefields:
            include_fields = include_fields + "include_fields=%s&" % field

        keywrds = ""
        for word in self.keywrds:
            keywrds = keywrds + "keywords=%s&" % word

        assigned = ""
        for assign in self.assigned:
            assigned = assigned + "assigned_to=%s&" % assign

        url = self.bugzilla_url +"/bug?" + include_fields + keywrds + assigned
        if self.token:
            url = url + "token=%s" % self.token
        results = requests.get(url).json()
        return [Bug(self.bugzilla_url, self.token, **bug) for bug in results['bugs']]