"""pypasswork exceptions"""


class PassworkBaseException(Exception):
    """Base PassworkAPI exception"""

    def __init__(self, message):
        self.msg = message

    def __str__(self) -> str:
        return self.msg

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(message={self.msg})'


class PassworkInteractionError(PassworkBaseException):
    """Error occurred while Passwork API interaction"""
