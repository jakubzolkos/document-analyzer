class InvalidCredentialsError(Exception):
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

class ModifyContentError(Exception):
    pass
