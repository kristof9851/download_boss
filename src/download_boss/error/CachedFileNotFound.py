class CachedFileNotFound(Exception):
    def __init__(self, message):
        super(CachedFileNotFound, self).__init__(message)
        self.message = message
