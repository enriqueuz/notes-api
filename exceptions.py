""" Exceptions """

class AuthorizationError(Exception):
    """ A base class for exceptions used by bottle. """
    def __init__(self, msg):
        self.msg = msg