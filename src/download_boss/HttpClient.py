import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from .AbstractClient import AbstractClient

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class HttpClient(AbstractClient):

    def __init__(self):
        self.session = requests.Session()

    """
    Sends a HTTP request to download a resource based on request parameter.
    Docs:
        send():           https://requests.readthedocs.io/en/latest/api/#requests.Session.send
        PreparedRequest:  https://requests.readthedocs.io/en/latest/api/#requests.PreparedRequest

    Parameters:
        request (Request): https://requests.readthedocs.io/en/latest/api/#requests.Request

    Returns: 
        (Response): https://requests.readthedocs.io/en/latest/api/#requests.Response

    Throws:
        HTTPError: If the request failed with 4xx or 5xx status
                   https://requests.readthedocs.io/en/latest/api/#requests.HTTPError
    """
    def download(self, request):
        response = self.session.send(request.prepare())
        response.raise_for_status()
        return response
