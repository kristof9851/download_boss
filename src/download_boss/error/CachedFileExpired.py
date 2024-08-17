class CachedFileExpired(Exception):
    def __init__(self, message):
        super(CachedFileExpired, self).__init__(message)
        self.message = message
