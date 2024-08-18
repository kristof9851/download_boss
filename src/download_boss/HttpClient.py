import requests
import logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from .AbstractClient import AbstractClient
from .error.ClientRetriable import ClientRetriable

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class HttpClient(AbstractClient):

    """
    Parameters:
        throwRetriableStatusCodeRanges (list) : List of int-s and/or range()-s when the client should throw a retriable exception
    """
    def __init__(self, throwRetriableStatusCodeRanges=None):
        self.throwRetriableStatusCodeRanges = throwRetriableStatusCodeRanges or []
        self.session = requests.Session()

    """
    Sends a HTTP request to download a resource based on request parameters.
    Docs:
        send():           https://requests.readthedocs.io/en/latest/api/#requests.Session.send
        PreparedRequest:  https://requests.readthedocs.io/en/latest/api/#requests.PreparedRequest

    Parameters:
        requestEnvelope (RequestEnvelope): The request

    Returns: 
        (Response): https://requests.readthedocs.io/en/latest/api/#requests.Response

    Throws:
        ClientRetriable: If the request should be retried
    """
    def download(self, requestEnvelope):
        logging.info(f'Requesting: {requestEnvelope}')

        response = self.session.send(requestEnvelope.request.prepare(), **requestEnvelope.kwargs)

        for statusCodes in self.throwRetriableStatusCodeRanges:
            if (isinstance(statusCodes, int) and statusCodes == response.status_code) or (isinstance(statusCodes, range) and response.status_code in statusCodes):
                raise ClientRetriable(response)

        return response
