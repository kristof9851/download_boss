import logging
import requests
from requests_kerberos import HTTPKerberosAuth, OPTIONAL
from requests_aws4auth import AWS4Auth

from ..HttpClient import HttpClient
from ..RetryWrapper import RetryWrapper
from ..RequestEnvelope import RequestEnvelope
from ..error.AuthFailed import AuthFailed
from .AbstractAuthGenerator import AbstractAuthGenerator

class AwsAuthGenerator(AbstractAuthGenerator):

    def __init__(self, baseUrl, roleArn, authCookieBaseUrl, authCookieName='GSSSO', awsRegion='us-east-1', awsService='es', client=None):
        self.baseUrl = baseUrl
        self.roleArn = roleArn
        self.authCookieBaseUrl = authCookieBaseUrl
        self.authCookieName = authCookieName
        self.awsRegion = awsRegion
        self.awsService = awsService
        self.client = client or self._createClient()

        self.aws4auth = None

    def _createClient(self):
        httpClient = HttpClient(throwRetriableStatusCodeRanges=[range(500,600)])
        httpClient = RetryWrapper(httpClient)
        return httpClient

    """
    Return AWS4Auth with current credentials
    """
    def get(self):
        if self.aws4auth is None:
            self.aws4auth = self._auth()

        return self.aws4auth

    """
    Regenerate credentials for AWS4Auth, and store it
    """
    def refresh(self):
        self.aws4auth = self._auth()

    """
    Create AWS4Auth with fresh credentials

    Throws:
        AuthFailed: If any of the auth calls fail
    """
    def _auth(self):
        logging.info("Getting AWS credentials...")

        credentials = self._requestAuthCredentials()

        return AWS4Auth(
            credentials['accessKeyId'],
            credentials['secretAccessKey'],
            self.awsRegion,
            self.awsService,
            session_token=credentials['sessionToken']
        )

    def _requestAuthCredentials(self):
        request = requests.Request(
            method='POST',
            url=self.baseUrl,
            params={"role": self.roleArn},
            headers={
                "Content-Type": "application/json", 
                "Cookie": self.authCookieName + "=" + self._requestAuthCookie()
            }
        )
        response = self.client.download(RequestEnvelope(request, verify=False))
        if response.status_code != 200 or 'credentials' not in response.json():
            logging.error(f"Failed to get AWS credentials. Status {response.status_code}. Response: {response.text}")
            raise AuthFailed(response)

        return response.json()['credentials']

    def _requestAuthCookie(self):
        request = requests.Request(
            method='GET',
            url=self.authCookieBaseUrl,
            auth=HTTPKerberosAuth(mutual_authentication=OPTIONAL)
        )
        response = self.client.download(RequestEnvelope(request, verify=False))
        if response.status_code != 200 or self.authCookieName not in response.cookies:
            logging.error(f"Failed to get Auth cookie. Status {response.status_code}. Response: {response.text}")
            raise AuthFailed(response)

        return response.cookies[self.authCookieName]
