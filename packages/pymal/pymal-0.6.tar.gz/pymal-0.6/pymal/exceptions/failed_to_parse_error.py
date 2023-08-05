__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

__all__ = ['FailedToParseError', 'FailedToReloadError', 'FailedToAddError']


class FailedToParseError(RuntimeError):
    pass


class FailedToReloadError(FailedToParseError):
    pass


class FailedToAddError(FailedToParseError):
    pass
