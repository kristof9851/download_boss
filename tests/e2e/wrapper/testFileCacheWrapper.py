import unittest
import requests
import time
import os

from download_boss.client.request.HttpRequestEnvelope import HttpRequestEnvelope
from download_boss.client.HttpClient import HttpClient
from download_boss.wrapper.FileCacheWrapper import FileCacheWrapper
from ..util.TestUtil import getCacheDirPath


requests.packages.urllib3.disable_warnings()


class TestFileCacheWrapper(unittest.TestCase):

    def testNoCachedFile(self):
        wrapper = FileCacheWrapper(HttpClient(), cacheFolderPath=getCacheDirPath())
        request = HttpRequestEnvelope(requests.Request(method='get', url=f'https://httpbin.org/uuid'))

        wrapper.removeCache(request)
        cacheKeyPath = os.path.join(getCacheDirPath(), request.getCacheKey())
        self.assertFalse( os.path.isfile(cacheKeyPath) )
        wrapper.download(request)
        self.assertTrue( os.path.isfile(cacheKeyPath) )

    def testCachedFileExpired(self):
        wrapper = FileCacheWrapper(HttpClient(), cacheFolderPath=getCacheDirPath(), cacheLength=0)
        request = HttpRequestEnvelope(requests.Request(method='get', url=f'https://httpbin.org/uuid'))

        response1 = wrapper.download(request)
        time.sleep(1)
        response2 = wrapper.download(request)
        self.assertNotEqual(response1.text, response2.text)
        
    def testCachedFileReused(self):
        wrapper = FileCacheWrapper(HttpClient(), cacheFolderPath=getCacheDirPath())
        request = HttpRequestEnvelope(requests.Request(method='get', url=f'https://httpbin.org/uuid'))

        response1 = wrapper.download(request)
        time.sleep(1)
        response2 = wrapper.download(request)
        self.assertEqual(response1.text, response2.text)

if __name__ == '__main__':
    unittest.main()
