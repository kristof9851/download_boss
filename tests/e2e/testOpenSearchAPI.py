import unittest
import requests
from requests import HTTPError
from requests.exceptions import SSLError

from download_boss.error.RetriesExhausted import RetriesExhausted
from download_boss.error.ClientRetriable import ClientRetriable
from download_boss.HttpClient import HttpClient
from download_boss.OpenSearchAPI import OpenSearchAPI
from download_boss.auth.BasicAuthGenerator import BasicAuthGenerator

class TestOpenSearchAPI(unittest.TestCase):

    def testSearchMatchSuccess(self):
        os = OpenSearchAPI(
            'https://httpbin.org/anything', 
            HttpClient(), 
            BasicAuthGenerator("user", "pass")
        )
        response = os.searchMatch({"key": "value"})
        self.assertEqual(response.status_code, 200)

        json = response.json()
        self.assertEqual(json['method'], "GET")
        self.assertEqual(json['url'], "https://httpbin.org/anything/_search")
        self.assertEqual(json['headers']['Authorization'], "Basic dXNlcjpwYXNz")
        self.assertEqual(json['headers']['Content-Type'], "application/json")
        self.assertEqual(json['json'], {
            "_source": False,
            "query": {
                "bool": {
                    "must": [{
                        "match": { "key": "value" }
                    }]
                }
            },
            "size": 1000
        })

    def testSearchMatchRetriable(self):
        os = OpenSearchAPI(
            'https://httpbin.org/anything', 
            HttpClient(clientRetriableStatusCodeRanges=[200]), 
            BasicAuthGenerator("user", "pass"),
            authRetriableStatusCodeRanges=[200]
        )

        with self.assertRaises(RetriesExhausted) as e:
            os.searchMatch({"key": "value"})
    
    def testSearchMatchNonRetriable(self):
        os = OpenSearchAPI(
            'https://httpbin.org/non-existent', 
            HttpClient(clientRetriableStatusCodeRanges=[404]), 
            BasicAuthGenerator("user", "pass"),
            authRetriableStatusCodeRanges=[403]
        )

        with self.assertRaises(ClientRetriable) as e:
            os.searchMatch({"key": "value"})


if __name__ == '__main__':
    unittest.main()
