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
    """
    def __init__(self, client, cacheFolderPath, cacheLength=None):
        super().__init__(client)
        self.cacheFolderPath = cacheFolderPath
        self.cacheLength = cacheLength

    """
    Parameters:
        requestEnvelope (RequestEnvelope): The request
        
    Returns: 
        (Response): https://requests.readthedocs.io/en/latest/api/#requests.Response
    """
    def download(self, requestEnvelope):
        try:
            return self._getCache(requestEnvelope)
        except Exception as e:
            if not isinstance(e, CachedFileNotFound) and not isinstance(e, CachedFileExpired):
                traceback.print_exc()
            
            response = self.client.download(requestEnvelope)
            self._setCache(requestEnvelope, response)
            return response

    def _setCache(self, requestEnvelope, response):
        cacheKey = self._getCacheKey(requestEnvelope)
        cacheValue = response.text

        with open(cacheKey, 'w') as f:
            f.write(cacheValue)

    def _getCache(self, requestEnvelope):
        cacheKey = self._getCacheKey(requestEnvelope)
        
        if not os.path.isfile(cacheKey):
            logging.info(f'Cache miss: {requestEnvelope}')
            raise CachedFileNotFound(cacheKey)
        
        currentTime = time.time()
        fileTime = os.path.getctime(cacheKey)

        if self.cacheLength is not None and fileTime + self.cacheLength < currentTime:
            logging.info(f'Cache expired: {requestEnvelope}')
            raise CachedFileExpired(cacheKey)
        
        with open(cacheKey) as f:
            logging.debug(f'Cache found: {requestEnvelope}')
            response = requests.Response()
            response._content = f.read().encode('utf-8')
            return response

    def _getCacheKey(self, requestEnvelope):
        r = {}
        r['method'] = requestEnvelope.request.method
        r['url'] = requestEnvelope.request.url
        r['headers'] = requestEnvelope.request.headers
        r['data'] = requestEnvelope.request.data
        r['json'] = requestEnvelope.request.json
        r['params'] = requestEnvelope.request.params

        hash = hashlib.md5(str(r).encode()).hexdigest()

        fileName = self._urlToFileName(requestEnvelope.request.url) + '_' + hash + '.txt'

        return os.path.join(self.cacheFolderPath, fileName)
    
    def _urlToFileName(self, url):
        # https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file
        return re.sub(r'[<>:"/\\|?*]', '_', url)
    
    def removeCache(self, requestEnvelope):
        cacheKey = self._getCacheKey(requestEnvelope)
        
        if os.path.isfile(cacheKey):
            os.remove(cacheKey)
