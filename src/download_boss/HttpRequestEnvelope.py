import os
import re
import hashlib

from .AbstractRequestEnvelope import AbstractRequestEnvelope

class HttpRequestEnvelope(AbstractRequestEnvelope):

    """
    Parameters:
        request (Request): https://requests.readthedocs.io/en/latest/api/#requests.Request
        kwargs:            kwargs
    """
    def __init__(self, request, **kwargs):
        self.request = request
        self.kwargs = kwargs

    def __repr__(self):
        return f'{self.request.method} {self.request.url}'

    def getCacheKey(self):
        r = {}
        r['method'] = self.request.method
        r['url'] = self.request.url
        r['headers'] = self.request.headers
        r['data'] = self.request.data
        r['json'] = self.request.json
        r['params'] = self.request.params

        hash = hashlib.md5(str(r).encode()).hexdigest()

        return self._urlToFileName(self.request.url) + '_' + hash + '.txt'
    
    def _urlToFileName(self, url):
        # https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file
        return re.sub(r'[<>:"/\\|?*]', '_', url)
    