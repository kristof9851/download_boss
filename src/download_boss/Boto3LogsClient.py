import boto3
import logging
import time

from .AbstractClient import AbstractClient

class Boto3LogsClient(AbstractClient):

    def __init__(self, awsAuthGenerator, region, sleepSecondsBetweenQueryChecks=20):
        self.awsAuthGenerator = awsAuthGenerator
        self.region = region
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
        logging.info(f'Requesting: {requestEnvelope}')

        response = self.client.start_query(**boto3LogsRequestEnvelope.kwargs)

        query_id = response['queryId']
        while True:
            response = self.client.get_query_results(queryId=query_id)
            if response['status'] == 'Complete':
                break

            logging.info(f'Waiting for CloudWatch Logs query to complete for query_id={query_id}...')
            time.sleep(self.sleepSecondsBetweenQueryChecks)

        return response['results']
