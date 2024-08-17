class ClientRetriable(Exception):
    def __init__(self, message):
        super(ClientRetriable, self).__init__(message)
        self.message = message
