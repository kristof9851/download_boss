import unittest
import requests

from download_boss.RequestEnvelope import RequestEnvelope
from download_boss.HttpClient import HttpClient
from download_boss.FileCacheWrapper import FileCacheWrapper

class TestFileCacheWrapper(unittest.TestCase):

    def setUp(self):
        self.wrapper = FileCacheWrapper(HttpClient(), cacheFolderPath='test')

    def testGetCacheKeysAreDifferent(self):
        envelope1 = RequestEnvelope(requests.Request(url="http://google.com", method="GET"))
        envelope2 = RequestEnvelope(requests.Request(url="http://google.com", method="POST"))
        self.assertNotEqual(self.wrapper._getCacheKey(envelope1), self.wrapper._getCacheKey(envelope2))

        envelope1 = RequestEnvelope(requests.Request(url="http://google.com", headers={"Content-Type": "application/json"}))
        envelope2 = RequestEnvelope(requests.Request(url="http://google.com", headers={"Content-Type": "text/html"}))
        self.assertNotEqual(self.wrapper._getCacheKey(envelope1), self.wrapper._getCacheKey(envelope2))

        envelope1 = RequestEnvelope(requests.Request(url="http://google.com", data="Data1"))
        envelope2 = RequestEnvelope(requests.Request(url="http://google.com", data="Data2"))
        self.assertNotEqual(self.wrapper._getCacheKey(envelope1), self.wrapper._getCacheKey(envelope2))

        envelope1 = RequestEnvelope(requests.Request(url="http://google.com", json={"key": "value1"}))
        envelope2 = RequestEnvelope(requests.Request(url="http://google.com", json={"key": "value2"}))
        self.assertNotEqual(self.wrapper._getCacheKey(envelope1), self.wrapper._getCacheKey(envelope2))

        envelope1 = RequestEnvelope(requests.Request(url="http://google.com", params={"query": "search"}))
        envelope2 = RequestEnvelope(requests.Request(url="http://google.com", params={"query": "delete"}))
        self.assertNotEqual(self.wrapper._getCacheKey(envelope1), self.wrapper._getCacheKey(envelope2))

    def testGetCacheKeyIsAlwaysSame(self):
        envelope1 = RequestEnvelope(requests.Request(url="http://google.com", params={"key": "value"}))
        envelope2 = RequestEnvelope(requests.Request(url="http://google.com", params={"key": "value"}))
        envelope3 = RequestEnvelope(requests.Request(url="http://google.com", params={"key": "value"}))
        self.assertEqual(self.wrapper._getCacheKey(envelope1), self.wrapper._getCacheKey(envelope2))
        self.assertEqual(self.wrapper._getCacheKey(envelope2), self.wrapper._getCacheKey(envelope3))

if __name__ == '__main__':
    unittest.main()
