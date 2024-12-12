import unittest
import requests

from download_boss.HttpRequestEnvelope import HttpRequestEnvelope
from download_boss.HttpClient import HttpClient
from download_boss.RetryWrapper import RetryWrapper
from download_boss.error.RetriesExhausted import RetriesExhausted
from download_boss.error.ClientRetriable import ClientRetriable

requests.packages.urllib3.disable_warnings()

class TestRetryWrapper(unittest.TestCase):

    def testNothingToRetry(self):
        wrapper = RetryWrapper(HttpClient())
        request = HttpRequestEnvelope(requests.Request(method='get', url='https://httpbin.org/status/200'))
        response = wrapper.download(request)

        self.assertEqual(response.status_code, 200)

    def testRetriableInt(self):
        wrapper = RetryWrapper(HttpClient(throwRetriableStatusCodeRanges=[500]))
        request = HttpRequestEnvelope(requests.Request(method='get', url='https://httpbin.org/status/500'))

        with self.assertRaises(RetriesExhausted) as e:
            wrapper.download(request)
        self.assertEqual(500, e.exception.message.status_code)

    def testRetriableRange(self):
        wrapper = RetryWrapper(HttpClient(throwRetriableStatusCodeRanges=[range(500, 600)]))
        request = HttpRequestEnvelope(requests.Request(method='get', url='https://httpbin.org/status/504'))

        with self.assertRaises(RetriesExhausted) as e:
            wrapper.download(request)
        self.assertEqual(504, e.exception.message.status_code)

    def testNonRetriable(self):
        wrapper = RetryWrapper(HttpClient())
        request = HttpRequestEnvelope(requests.Request(method='get', url='https://httpbin.org/status/500'))

        response = wrapper.download(request)
        self.assertEqual(response.status_code, 500)

    def testNonRetriableRange(self):
        wrapper = RetryWrapper(HttpClient(throwRetriableStatusCodeRanges=[range(300, 400)]))
        request = HttpRequestEnvelope(requests.Request(method='get', url='https://httpbin.org/status/500'))

        response = wrapper.download(request)
        self.assertEqual(response.status_code, 500)

    def testCustomRetriableStatusUnhandled(self):
        wrapper = RetryWrapper(HttpClient(throwRetriableStatusCodeRanges=[500]), catchRetriableStatusCodeRanges=[400])
        request = HttpRequestEnvelope(requests.Request(method='get', url='https://httpbin.org/status/500'))

        with self.assertRaises(ClientRetriable) as e:
            wrapper.download(request)
        self.assertEqual(500, e.exception.message.status_code)
    
    def testCustomRetriableStatusHandled(self):
        wrapper = RetryWrapper(HttpClient(throwRetriableStatusCodeRanges=[500]), catchRetriableStatusCodeRanges=[500])
        request = HttpRequestEnvelope(requests.Request(method='get', url='https://httpbin.org/status/500'))

        with self.assertRaises(RetriesExhausted) as e:
            wrapper.download(request)
        self.assertEqual(500, e.exception.message.status_code)

if __name__ == '__main__':
    unittest.main()
