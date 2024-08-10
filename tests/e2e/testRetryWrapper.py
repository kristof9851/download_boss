import unittest
import requests

from download_boss.HttpClient import HttpClient
from download_boss.RetryWrapper import RetryWrapper
from download_boss.error.RetriesExhausted import RetriesExhausted

class TestRetryWrapper(unittest.TestCase):

    def testNoRetries(self):
        wrapper = RetryWrapper(HttpClient())
        request = requests.Request(method='get', url='https://httpbin.org/status/200')
        response = wrapper.download(request)

        self.assertEqual(response.status_code, 200)

    def testMaxRetries(self):
        wrapper = RetryWrapper(HttpClient())
        request = requests.Request(method='get', url='https://httpbin.org/status/500')

        self.assertRaises(RetriesExhausted, wrapper.download, request)

if __name__ == '__main__':
    unittest.main()