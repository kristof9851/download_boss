import logging
import requests
import time

from download_boss.error.RetriesExhausted import RetriesExhausted
from download_boss.error.ClientRetriable import ClientRetriable
from download_boss.RequestEnvelope import RequestEnvelope

class OpenSearchAPI:
    
    def __init__(self, baseUrl, client, authGenerator, catchRetriableStatusCodeRanges=None, retryCount=3):
        self.baseUrl = baseUrl
        self.client = client
        self.authGenerator = authGenerator
        self.catchRetriableStatusCodeRanges = catchRetriableStatusCodeRanges or [401, 403]
        self.retryCount = retryCount

    def searchMatch(self, matchDict):
        return self.search(OpenSearchAPI._getMatchQuery(matchDict))

    def search(self, query):
        requestEnvelope = RequestEnvelope(
            requests.Request(
                method = 'GET',
                url = self.baseUrl + '/_search',
                headers = {'Content-Type': 'application/json'},
                auth = self.authGenerator.get(),
                json = query
            ),
            verify = False
        )

        retriesLeft = self.retryCount
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
                            self.authGenerator.refresh()
                            break
                        else:
                            raise RetriesExhausted(e.message)

                if not isRetriable:
                    raise e

    def _getMatchQuery(matchFields, returnFields=None, returnSource=False, size=1000):
        query = {
            'query': {
                'bool': {
                    'must': [ {'match': {key: value}} for key, value in matchFields.items() ]
                }
            },
            '_source': returnSource,
            'size': size
        }

        if isinstance(returnFields, dict):
            query['fields'] = returnFields

        return query
