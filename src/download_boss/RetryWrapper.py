import time
import logging

from .AbstractWrapper import AbstractWrapper
from .error.RetriesExhausted import RetriesExhausted
from .error.ClientRetriable import ClientRetriable

class RetryWrapper(AbstractWrapper):

    """
    Parameters:
        client (AbstractClient):               Ie. HttpClient
        count (int):                           Max retry count
        catchRetriableStatusCodeRanges (list): List of int-s and/or range()-s of status codes that should be retried
    """
    def __init__(self, client, count=3, catchRetriableStatusCodeRanges=None):
        super().__init__(client)
        self.count = count
        self.catchRetriableStatusCodeRanges = catchRetriableStatusCodeRanges or [range(0, 1000)]

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
                return self.client.download(requestEnvelope)
            except ClientRetriable as e:
                isRetriable = False

                for statusCodes in self.catchRetriableStatusCodeRanges:
                    if (isinstance(statusCodes, int) and statusCodes == e.message.status_code) or (isinstance(statusCodes, range) and e.message.status_code in statusCodes):
                                
                        if retriesLeft > 0:
                            logging.info(f'Retrying... {requestEnvelope}')
                            isRetriable = True
                            
                            retriesLeft = retriesLeft - 1
                            time.sleep(1)
                            break
                        else:
                            raise RetriesExhausted(e.message)

                if not isRetriable:
                    raise e
