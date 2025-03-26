import logging
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time
import json
from types import SimpleNamespace

from download_boss.error.RetriesExhausted import RetriesExhausted
from download_boss.error.ClientRetriable import ClientRetriable
from download_boss.HttpRequestEnvelope import HttpRequestEnvelope

class OpenSearchAPI:
    
    def __init__(self, baseUrl, client, authGenerator, catchRetriableStatusCodeRanges=None, retryCount=3):
        self.baseUrl = baseUrl
        self.client = client
        self.authGenerator = authGenerator
        self.catchRetriableStatusCodeRanges = catchRetriableStatusCodeRanges or [401, 403]
        self.retryCount = retryCount

    def searchMatch(self, matchDict, getAllResults=False):
        return self.search(
            OpenSearchAPI._getMatchQuery(matchDict),
            getAllResults
        )

    def _getMatchQuery(matchFields, returnFields=None, searchFrom=0, searchSize=1000):
        query = {
            'query': {
                'bool': {
                    'must': [ {'match': {key: value}} for key, value in matchFields.items() ]
                }
            },
            'from': searchFrom,
            'size': searchSize
        }

        if isinstance(returnFields, dict):
            query['fields'] = returnFields

        return query

    def search(self, query, getAllResults):
        if getAllResults:
            searchFrom = query.get('from', 0)
            searchSize = query.get('size', 1000)

            allResults = {
                'hits': {
                    'total': {'value': 0},
                    'hits': []
                }
            }
            while True:
                query['from'] = searchFrom
                query['size'] = searchSize

                response = self._searchWithRetries(query)
                if response.status_code != 200:
                    return response

                responseJson = response.json()
                hits = responseJson['hits']['hits']

                allResults['hits']['hits'].extend(hits)
                allResults['hits']['total']['value'] += len(hits)

                if len(hits) < searchSize:
                    r = SimpleNamespace()
                    r.status_code = 200
                    r.text = json.dumps(allResults)
                    return r

                searchFrom += searchSize
        else:
            return self._searchWithRetries(query)

    def _searchWithRetries(self, query):
        httpRequestEnvelope = HttpRequestEnvelope(
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
                return self.client.download(httpRequestEnvelope)
            except ClientRetriable as e:
                isRetriable = False

                for statusCodes in self.catchRetriableStatusCodeRanges:
                    if (isinstance(statusCodes, int) and statusCodes == e.message.status_code) or (isinstance(statusCodes, range) and e.message.status_code in statusCodes):
                        
                        if retriesLeft > 0:
                            logging.info(f'Retrying... {httpRequestEnvelope}')
                            isRetriable = True

                            retriesLeft = retriesLeft - 1
                            time.sleep(1)
                            self.authGenerator.refresh()
                            break
                        else:
                            raise RetriesExhausted(e.message)

                if not isRetriable:
                    raise e
