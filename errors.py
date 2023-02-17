class AuthenticationError(Exception):
    pass


class FileTooLargeError(Exception):
    pass


class UnsupportedFormatError(Exception):
    pass


class UploadFailedError(Exception):
    pass


class CloudStorageFullError(Exception):
    pass


class NoPermissionError(Exception):
    pass


class ContentModificationError(Exception):
    pass


class ConnectionError(Exception):
    pass


class CorruptedFileError(Exception):
    pass


class NoTextFoundError(Exception):
    pass


class DocumentParsingError(Exception):
    pass


class InvalidAPIKeyError(Exception):
    pass


class RateLimitExceededError(Exception):
    pass


class DependencyError(Exception):
    pass


class InternalServerError(Exception):
    pass


class TimeoutError(Exception):
    pass


class ValidationError(Exception):
    pass


