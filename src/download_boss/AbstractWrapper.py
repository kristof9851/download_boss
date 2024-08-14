from .AbstractClient import AbstractClient

class AbstractWrapper(AbstractClient):

    def __init__(self, client):
        self.client = client

    # 
    # Invoke the client.download() in your method, and return its response
    #
    # def download(self, requestEnvelope):
    #     # Wrapper before...
    #     return self.client.download(requestEnvelope)
    #     # Wrapper after...
    # 
