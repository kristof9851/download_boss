import unittest
import requests
from requests import HTTPError
from requests.exceptions import SSLError

from download_boss.HttpClient import HttpClient
from download_boss.RequestEnvelope import RequestEnvelope
from download_boss.error.ClientRetriable import ClientRetriable

class TestHttpClient(unittest.TestCase):

    def testRequestSuccess(self):
        client = HttpClient()
        request = RequestEnvelope(requests.Request(method='get', url='https://httpbin.org/get?id=testGet'))
        response = client.download(request)

        self.assertEqual(response.status_code, 200)
        self.assertRegex(response.text, r'"id":\s*"testGet"')

    def testRequestFailure(self):
        client = HttpClient()
        request = RequestEnvelope(requests.Request(method='get', url='https://httpbin.org/status/500'))
        response = client.download(request)

        self.assertEqual(response.status_code, 500)

    def testRetriableStatusCodes(self):
        client = HttpClient(throwRetriableStatusCodeRanges=[401, range(500,600)])

        request = RequestEnvelope(requests.Request(method='get', url='https://httpbin.org/status/401'))
        with self.assertRaises(ClientRetriable) as e:
            client.download(request)
        self.assertEqual(401, e.exception.message.status_code)
        
        request = RequestEnvelope(requests.Request(method='get', url='https://httpbin.org/status/504'))
        with self.assertRaises(ClientRetriable) as e:
            client.download(request)
        self.assertEqual(504, e.exception.message.status_code)

        request = RequestEnvelope(requests.Request(method='get', url='https://httpbin.org/status/200'))
        response = client.download(request)
        self.assertEqual(response.status_code, 200)

    def testRequestWithHeaders(self):
        client = HttpClient()
        request = RequestEnvelope(requests.Request(method='get', url='https://httpbin.org/get?id=testHeaders', headers={'Test-Header': '1234567890'}))
        response = client.download(request)

        self.assertEqual(response.status_code, 200)
        self.assertRegex(response.text, r'"id":\s*"testHeaders"')
        self.assertRegex(response.text, r'"Test-Header":\s*"1234567890"')

    def testRequestWithKwargs(self):
        client = HttpClient()

        request = RequestEnvelope(requests.Request(method='get', url='https://self-signed.badssl.com/'), verify=True)
        self.assertRaises(SSLError, client.download, request)

        request = RequestEnvelope(requests.Request(method='get', url='https://self-signed.badssl.com/'), verify=False)
        response = client.download(request)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
