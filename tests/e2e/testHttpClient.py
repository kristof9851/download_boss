import unittest
import requests
from requests import HTTPError
from requests.exceptions import SSLError

from download_boss.HttpClient import HttpClient
from download_boss.RequestEnvelope import RequestEnvelope

class TestHttpClient(unittest.TestCase):

    def testSuccess(self):
        client = HttpClient()
        request = RequestEnvelope(requests.Request(method='get', url='https://httpbin.org/get?id=testGet'))
        response = client.download(request)

        self.assertEqual(response.status_code, 200)
        self.assertRegex(response.text, r'"id":\s*"testGet"')

    def testFailure(self):
        client = HttpClient()
        request = RequestEnvelope(requests.Request(method='get', url='https://httpbin.org/status/500'))

        self.assertRaises(HTTPError, client.download, request)

    def testHeaders(self):
        client = HttpClient()
        request = RequestEnvelope(requests.Request(method='get', url='https://httpbin.org/get?id=testHeaders', headers={'Test-Header': '1234567890'}))
        response = client.download(request)

        self.assertEqual(response.status_code, 200)
        self.assertRegex(response.text, r'"id":\s*"testHeaders"')
        self.assertRegex(response.text, r'"Test-Header":\s*"1234567890"')

    def testClientFlags(self):
        client = HttpClient()

        request = RequestEnvelope(requests.Request(method='get', url='https://self-signed.badssl.com/'), verify=True)
        self.assertRaises(SSLError, client.download, request)

        request = RequestEnvelope(requests.Request(method='get', url='https://self-signed.badssl.com/'), verify=False)
        response = client.download(request)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
