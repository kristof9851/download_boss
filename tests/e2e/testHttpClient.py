import unittest
import requests
from requests import HTTPError

from download_boss.HttpClient import HttpClient

class TestHttpClient(unittest.TestCase):

    def testSuccess(self):
        client = HttpClient()
        request = requests.Request(method='get', url='https://httpbin.org/get?id=testGet')
        response = client.download(request)

        self.assertEqual(response.status_code, 200)
        self.assertRegex(response.text, r'"id":\s*"testGet"')

    def testFailure(self):
        client = HttpClient()
        request = requests.Request(method='get', url='https://httpbin.org/status/500')

        self.assertRaises(HTTPError, client.download, request)

    def testGetWithHeaders(self):
        client = HttpClient()
        request = requests.Request(method='get', url='https://httpbin.org/get?id=testGetWithHeaders', headers={'Test-Header': '1234567890'})
        response = client.download(request)

        self.assertEqual(response.status_code, 200)
        self.assertRegex(response.text, r'"id":\s*"testGetWithHeaders"')
        self.assertRegex(response.text, r'"Test-Header":\s*"1234567890"')

if __name__ == '__main__':
    unittest.main()
