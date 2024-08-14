class RequestEnvelope:

    """
    Parameters:
        request (Request): https://requests.readthedocs.io/en/latest/api/#requests.Request
        kwargs:            kwargs
    """
    def __init__(self, request, **kwargs):
        self.request = request
        self.kwargs = kwargs

    def __repr__(self):
        return f'{self.request.method} {self.request.url}'
