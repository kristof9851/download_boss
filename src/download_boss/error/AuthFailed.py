class AuthFailed(Exception):
    def __init__(self, message):
        super(AuthFailed, self).__init__(message)
        self.message = message
