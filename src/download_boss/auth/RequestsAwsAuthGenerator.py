import logging
import requests
from requests_kerberos import HTTPKerberosAuth, OPTIONAL
from requests_aws4auth import AWS4Auth

from .AwsAuthGenerator import AwsAuthGenerator

class RequestsAwsAuthGenerator(AwsAuthGenerator):

    def __init__(self, baseUrl, roleArn, authCookieBaseUrl, authCookieName='GSSSO', awsRegion='us-east-1', awsService='es', client=None):
        super().__init__(baseUrl, roleArn, authCookieBaseUrl, authCookieName, awsRegion, awsService, client)

    """
    Return AWS4Auth with current credentials
    """
    def get(self):
        credentials = super().get()
        
        return AWS4Auth(
            credentials['accessKeyId'],
            credentials['secretAccessKey'],
            self.awsRegion,
            self.awsService,
            session_token=credentials['sessionToken']
        )
