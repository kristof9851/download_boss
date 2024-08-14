import unittest
import requests
import time
import os

from download_boss.HttpClient import HttpClient
from download_boss.FileCacheWrapper import FileCacheWrapper
from .util.TestUtil import getCacheDirPath

class TestFileCacheWrapper(unittest.TestCase):

    def testNoCachedFile(self):
        wrapper = FileCacheWrapper(HttpClient(), cacheFolderPath=getCacheDirPath())
        request = requests.Request(method='get', url=f'https://httpbin.org/uuid')

        wrapper.removeCache(request)
        cacheKey = wrapper._getCacheKey(request)
        self.assertFalse( os.path.isfile(cacheKey) )
        wrapper.download(request)
        self.assertTrue( os.path.isfile(cacheKey) )

    def testCachedFileExpired(self):
        wrapper = FileCacheWrapper(HttpClient(), cacheFolderPath=getCacheDirPath(), cacheLength=0)
        request = requests.Request(method='get', url=f'https://httpbin.org/uuid')

        response1 = wrapper.download(request)
        time.sleep(1)
        response2 = wrapper.download(request)
        self.assertNotEqual(response1.text, response2.text)

if __name__ == '__main__':
    unittest.main()
