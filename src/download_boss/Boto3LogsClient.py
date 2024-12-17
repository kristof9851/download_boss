import boto3
from botocore.exceptions import ClientError
import logging
import time

from .AbstractClient import AbstractClient
from .error.ClientRetriable import ClientRetriable

class StatusResponse:
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code

class Boto3LogsClient(AbstractClient):

    def __init__(self, awsAuthGenerator, region, retryExpiredToken=True, sleepSecondsBetweenQueryChecks=20):
        self.awsAuthGenerator = awsAuthGenerator
        self.region = region
        self.retryExpiredToken = retryExpiredToken
        self.sleepSecondsBetweenQueryChecks = sleepSecondsBetweenQueryChecks
        self.client = None

        self._refreshClient()

    def _refreshClient(self):
        credentials = self.awsAuthGenerator.get()

        self.client = boto3.client(
            'logs',
            region_name=self.region,
            aws_access_key_id=credentials['accessKeyId'],
            aws_secret_access_key=credentials['secretAccessKey'],
            aws_session_token=credentials['sessionToken']
        )

    def download(self, boto3LogsRequestEnvelope):
        logging.info(f'Requesting: {boto3LogsRequestEnvelope}')

        try:
            response = self.client.start_query(**boto3LogsRequestEnvelope.kwargs)

            query_id = response['queryId']
            while True:
                response = self.client.get_query_results(queryId=query_id)
                if response['status'] == 'Complete':
                    break

                logging.info(f'Waiting for CloudWatch Logs query to complete for query_id={query_id}...')
                time.sleep(self.sleepSecondsBetweenQueryChecks)

            return response['results']

        except ClientError as e:
            if self.retryExpiredToken and e.response['Error']['Code'] == 'ExpiredTokenException':
                logging.info('ExpiredTokenException received, refreshing...')
                self._refreshClient()
                raise ClientRetriable( StatusResponse(e.response['Error']['Message'], 401) )
            
            raise e
