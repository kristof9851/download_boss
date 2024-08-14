import os
import re
import time
import hashlib
import requests
import logging
import traceback

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
        except Exception as e:
            if not isinstance(e, CachedFileNotFound) and not isinstance(e, CachedFileExpired):
                traceback.print_exc()
            
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
            logging.info(f'Cache miss: {request.method} {request.url}')
            raise CachedFileNotFound(cacheKey)
        
        currentTime = time.time()
        fileTime = os.path.getctime(cacheKey)

        if self.cacheLength is not None and fileTime + self.cacheLength < currentTime:
            logging.info(f'Cache expired: {request.method} {request.url}')
            raise CachedFileExpired(cacheKey)
        
        with open(cacheKey) as f:
            logging.debug(f'Cache found: {request.method} {request.url}')
            response = requests.Response()
            response._content = f.read().encode('utf-8')
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
        # https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file
        return re.sub(r'[<>:"/\\|?*]', '_', url)
    
    def removeCache(self, request):
        cacheKey = self._getCacheKey(request)
        
        if os.path.isfile(cacheKey):
            os.remove(cacheKey)
