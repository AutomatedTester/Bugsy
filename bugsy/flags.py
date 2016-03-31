class FlagException(Exception):
    """This is an error that is thrown if a flag has not been set correctly."""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "Message: {message} Code: {code}".format(message=self.msg,
                                                        code=self.code)


CLEAR = "X"
REQUEST = "?"
APPROVE = "+"
DENY = "-"

class Flags(object):
    """This is a base class for all Flags that can be used"""
    def __init__(self, status, requestee, name=None):
        self.name = name
        self.status = status


class NeedInfo(Flags):
    """docstring for NeedInfo"""
    def __init__(self, status=REQUEST, requestee=None):
        Flags.__init__(self, status, requestee, name="need-info")
        self.status = status
        self.requestee = requestee
