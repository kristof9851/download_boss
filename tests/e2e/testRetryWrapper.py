import unittest
import requests

from download_boss.RequestEnvelope import RequestEnvelope
from download_boss.HttpClient import HttpClient
from download_boss.RetryWrapper import RetryWrapper
from download_boss.error.RetriesExhausted import RetriesExhausted

class TestRetryWrapper(unittest.TestCase):

    def testNothingToRetry(self):
        wrapper = RetryWrapper(HttpClient())
        request = RequestEnvelope(requests.Request(method='get', url='https://httpbin.org/status/200'))
        response = wrapper.download(request)

        self.assertEqual(response.status_code, 200)

    def testRetriableInt(self):
        wrapper = RetryWrapper(HttpClient(clientRetriableStatusCodeRanges=[500]))
        request = RequestEnvelope(requests.Request(method='get', url='https://httpbin.org/status/500'))

        self.assertRaises(RetriesExhausted, wrapper.download, request)

    def testRetriableRange(self):
        wrapper = RetryWrapper(HttpClient(clientRetriableStatusCodeRanges=[range(500, 600)]))
        request = RequestEnvelope(requests.Request(method='get', url='https://httpbin.org/status/500'))

        self.assertRaises(RetriesExhausted, wrapper.download, request)

    def testNonRetriable(self):
        wrapper = RetryWrapper(HttpClient())
        request = RequestEnvelope(requests.Request(method='get', url='https://httpbin.org/status/500'))

        response = wrapper.download(request)
        self.assertEqual(response.status_code, 500)

    def testNonRetriableRange(self):
        wrapper = RetryWrapper(HttpClient(clientRetriableStatusCodeRanges=[range(300, 400)]))
        request = RequestEnvelope(requests.Request(method='get', url='https://httpbin.org/status/500'))

        response = wrapper.download(request)
        self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()
