import unittest
import requests

from download_boss.client.request.HttpRequestEnvelope import HttpRequestEnvelope
from download_boss.client.HttpClient import HttpClient
from download_boss.wrapper.FileCacheWrapper import FileCacheWrapper


requests.packages.urllib3.disable_warnings()


class TestFileCacheWrapper(unittest.TestCase):

    def setUp(self):
        self.wrapper = FileCacheWrapper(HttpClient(), cacheFolderPath='test')

    def testGetCacheKeysAreDifferent(self):
        envelope1 = HttpRequestEnvelope(requests.Request(url="http://google.com", method="GET"))
        envelope2 = HttpRequestEnvelope(requests.Request(url="http://google.com", method="POST"))
        self.assertNotEqual(envelope1.getCacheKey(), envelope2.getCacheKey())

        envelope1 = HttpRequestEnvelope(requests.Request(url="http://google.com", headers={"Content-Type": "application/json"}))
        envelope2 = HttpRequestEnvelope(requests.Request(url="http://google.com", headers={"Content-Type": "text/html"}))
        self.assertNotEqual(envelope1.getCacheKey(), envelope2.getCacheKey())

        envelope1 = HttpRequestEnvelope(requests.Request(url="http://google.com", data="Data1"))
        envelope2 = HttpRequestEnvelope(requests.Request(url="http://google.com", data="Data2"))
        self.assertNotEqual(envelope1.getCacheKey(), envelope2.getCacheKey())

        envelope1 = HttpRequestEnvelope(requests.Request(url="http://google.com", json={"key": "value1"}))
        envelope2 = HttpRequestEnvelope(requests.Request(url="http://google.com", json={"key": "value2"}))
        self.assertNotEqual(envelope1.getCacheKey(), envelope2.getCacheKey())

        envelope1 = HttpRequestEnvelope(requests.Request(url="http://google.com", params={"query": "search"}))
        envelope2 = HttpRequestEnvelope(requests.Request(url="http://google.com", params={"query": "delete"}))
        self.assertNotEqual(envelope1.getCacheKey(), envelope2.getCacheKey())

    def testGetCacheKeyIsAlwaysSame(self):
        envelope1 = HttpRequestEnvelope(requests.Request(url="http://google.com", params={"key": "value"}))
        envelope2 = HttpRequestEnvelope(requests.Request(url="http://google.com", params={"key": "value"}))
        envelope3 = HttpRequestEnvelope(requests.Request(url="http://google.com", params={"key": "value"}))
        self.assertEqual(envelope1.getCacheKey(), envelope2.getCacheKey())
        self.assertEqual(envelope1.getCacheKey(), envelope3.getCacheKey())

if __name__ == '__main__':
    unittest.main()
