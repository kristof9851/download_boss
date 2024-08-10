import time

from .AbstractWrapper import AbstractWrapper
from .error.RetriesExhausted import RetriesExhausted

class RetryWrapper(AbstractWrapper):

    """
    Parameters:
        client (AbstractClient): Ie. HttpClient
        count (int):             Max retry count
        
    Returns: 
        (Response): https://requests.readthedocs.io/en/latest/api/#requests.Response

    Throws:
        RetriesExhausted : If all retries have been exhausted of a failed request
    """
    def __init__(self, client, count=3):
        super().__init__(client)
        self.count = count

    def download(self, request):
        retriesLeft = self.count

        while True:
            try:
                response = self.client.download(request)
                return response
            except:
                if retriesLeft > 0:
                    retriesLeft = retriesLeft - 1
                    time.sleep(1)
                else:
                    raise RetriesExhausted()
