class RetriesExhausted(Exception):
    def __init__(self, message):
        super(RetriesExhausted, self).__init__(message)
        self.message = message
