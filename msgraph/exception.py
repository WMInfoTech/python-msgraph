import logging


logger = logging.getLogger(__name__)


class MicrosoftException(Exception):
    """
    An exception raised from the Microsoft Graph API

    Attributes:
        code (object):  The unique code denoting a particular type of exception
        message (str):  The message describing the exception
    """

    def __init__(self, code, message):
        super(MicrosoftException, self).__init__(message)
        self.code = code


class MicrosoftAuthenticationException(MicrosoftException):
    """
    An exception raised while attempting to authenticate with the Microsoft
    Graph API

    Attributes:
        code (object):  The unique code denoting a particular type of exception
        message (str):  The message describing the exception
    """
    pass
