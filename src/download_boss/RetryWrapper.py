import time
import logging

from .AbstractWrapper import AbstractWrapper
from .error.RetriesExhausted import RetriesExhausted
from .error.ClientRetriable import ClientRetriable

class RetryWrapper(AbstractWrapper):

    """
    Parameters:
        client (AbstractClient): Ie. HttpClient
        count (int):             Max retry count
    """
    def __init__(self, client, count=3):
        super().__init__(client)
        self.count = count

    """
    Parameters:
        requestEnvelope (RequestEnvelope): The request
        
    Returns: 
        (Response): https://requests.readthedocs.io/en/latest/api/#requests.Response

    Throws:
        RetriesExhausted : If all retries have been exhausted of a failed request
    """
    def download(self, requestEnvelope):
        retriesLeft = self.count

        while True:
            try:
                response = self.client.download(requestEnvelope)
                return response
            except ClientRetriable:
                if retriesLeft > 0:
                    logging.info(f'Retrying... {requestEnvelope}')
                    
                    retriesLeft = retriesLeft - 1
                    time.sleep(1)
                else:
                    raise RetriesExhausted(requestEnvelope)
