import os
import time
import hashlib
import requests

from .AbstractWrapper import AbstractWrapper
from .error.CachedFileNotFound import CachedFileNotFound
from .error.CachedFileExpired import CachedFileExpired

class FileCacheWrapper(AbstractWrapper):

    """
    Parameters:
        client (AbstractClient): Ie. HttpClient
        cacheFolderPath (str):   Folder path to cache dir
        cacheLength (int):       How long should cached items last in seconds. None means infinite.
        
    Returns: 
        (Response): https://requests.readthedocs.io/en/latest/api/#requests.Response
    """
    def __init__(self, client, cacheFolderPath, cacheLength=None):
        super().__init__(client)
        self.cacheFolderPath = cacheFolderPath
        self.cacheLength = cacheLength

    def download(self, request):
        try:
            return self._getCache(request)
        except:
            response = self.client.download(request)
            self._setCache(request, response)
            return response

    def _setCache(self, request, response):
        cacheKey = self._getCacheKey(request)
        cacheValue = response.text

        with open(cacheKey, 'w') as f:
            f.write(cacheValue)

    def _getCache(self, request):
        cacheKey = self._getCacheKey(request)
        
        if not os.path.isfile(cacheKey):
            raise CachedFileNotFound(cacheKey)
        
        currentTime = time.time()
        fileTime = os.path.getctime(cacheKey)

        if fileTime > currentTime - self.cacheLength:
            raise CachedFileExpired(cacheKey)
        
        with open(cacheKey) as f:
            response = requests.Response()
            response.text = f.read()
            return response

    def _getCacheKey(self, request):
        r = {}
        r['method'] = request.method
        r['url'] = request.url
        r['headers'] = request.headers
        r['data'] = request.data
        r['params'] = request.params

        hash = hashlib.md5(str(r).encode()).hexdigest()

        fileName = self._urlToFileName(request.url) + '_' + hash + '.txt'

        return os.path.join(self.cacheFolderPath, fileName)
    
    def _urlToFileName(self, url):
        url = url.replace('http://', '')
        url = url.replace('https://', '')
        url = url.replace('/', '_')
        url = url.replace(':', '_')
        url = url.replace('?', '_')
        return url
    
    def removeCache(self, request):
        cacheKey = self._getCacheKey(request)
        
        if os.path.isfile(cacheKey):
            os.remove(cacheKey)
