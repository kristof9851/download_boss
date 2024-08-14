import unittest
import requests
import time

from download_boss.RequestEnvelope import RequestEnvelope
from download_boss.HttpClient import HttpClient
from download_boss.DelayWrapper import DelayWrapper

class TestDelayWrapper(unittest.TestCase):

    def testNoDelay(self):
        wrapper = DelayWrapper(HttpClient())
        rrequest = RequestEnvelope(requests.Request(method='get', url='https://httpbin.org/status/200'))

        startTime = time.time()
        response = wrapper.download(request)
        endTime = time.time()

        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(endTime-startTime, 2, "Download took too long to complete")

    def testDelay(self):
        wrapper = DelayWrapper(HttpClient(), length=3)
        request = RequestEnvelope(requests.Request(method='get', url='https://httpbin.org/status/200'))

        startTime = time.time()
        response = wrapper.download(request)
        endTime = time.time()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(endTime-startTime, 2, "Download was not delayed")

if __name__ == '__main__':
    unittest.main()
