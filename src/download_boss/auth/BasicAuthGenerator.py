import logging
from requests.auth import HTTPBasicAuth

from .AbstractAuthGenerator import AbstractAuthGenerator

class BasicAuthGenerator(AbstractAuthGenerator):

    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.auth = None

    """
    Return HTTPBasicAuth with current credentials
    """
    def get(self):
        if self.auth is None:
            self.auth = self._auth()

        return self.auth

    """
    Recreate HTTPBasicAuth and store it
    """
    def refresh(self):
        self.auth = self._auth()

    """
    Create HTTPBasicAuth
    """
    def _auth(self):
        return HTTPBasicAuth(self.username, self.password)
