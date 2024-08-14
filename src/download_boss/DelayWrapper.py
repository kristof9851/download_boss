import time
import random
import logging

from .AbstractWrapper import AbstractWrapper

class DelayWrapper(AbstractWrapper):

    """
    Parameters:
        client (AbstractClient): Ie. HttpClient
        length (int):            Delay length in seconds
        maxLength (int):         If specified, delay will be a random value between length and maxLength
    """
    def __init__(self, client, length=0, maxLength=None):
        super().__init__(client)
        self.length = length
        self.maxLength = maxLength

    """
    Parameters:
        requestEnvelope (RequestEnvelope): The request
        
    Returns: 
        (Response): https://requests.readthedocs.io/en/latest/api/#requests.Response
    """
    def download(self, requestEnvelope):
        delay = self._generateDelayLength()
        logging.info(f'Delaying by {delay}s ... {requestEnvelope}')
        
        time.sleep(delay)
        return self.client.download(requestEnvelope)

    def _generateDelayLength(self):
        if self.maxLength is None:
            return self.length
        else:
            return random.randrange(self.length, self.maxLength+1)
