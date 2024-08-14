# Download Boss
![Python CI Build](https://github.com/kristof9851/download_boss/actions/workflows/python-ci.yml/badge.svg)
![PyPI Downloads](https://img.shields.io/pypi/dm/download_boss?label=PyPI%20Downloads&color=rgb(50%2C%20165%2C%20233)
)

*Python download library*

## 1. Installation

```bash
pip install download_boss
```

## 2. Usage

### 2.1. HttpClient with Wrappers
```python
import requests
import os
import json

from download_boss.RequestEnvelope import RequestEnvelope
from download_boss.HttpClient import HttpClient
from download_boss.RetryWrapper import RetryWrapper
from download_boss.DelayWrapper import DelayWrapper
from download_boss.FileCacheWrapper import FileCacheWrapper

# Cache responses in folder
cacheFolder = os.path.join( os.path.dirname(__file__), "cache" )

# Create HTTP client with wrappers
client = FileCacheWrapper( DelayWrapper( RetryWrapper( HttpClient(clientRetriableStatusCodeRanges=[range(500,600)]) ), length=0 ), cacheFolderPath=cacheFolder )

# Download two responses
jsonBaseUrl = 'https://httpbin.org/anything/'
jsonIds = ['one', 'two']

for id in jsonIds:
    # Send data with the request, so we can use read it from the response
    request = RequestEnvelope(requests.Request(method='POST', url=jsonBaseUrl + id, json=[{"subId": "111"}, {"subId": "222"}]))
    response = client.download(request)
    
    # Use the response to construct sub-requests
    jsonText = json.loads(response.text)
    for o in jsonText['json']:
        sid = o['subId']

        # Download and cache subrequests
        newUrl = 'https://httpbin.org/anything/' + sid
        request = RequestEnvelope(requests.Request(method='GET', url=newUrl), )
        client.download(request)

# The second time this is run, it will run instantly because FileCacheWrapper's cacheLength is not set (=None) so it caches responses indefinitely
```

**Output from first run**

```bash
(venv) C:\apps\download_boss>python demo\demo1.py
2024-08-11 13:09:08,284 [ INFO] FileCacheWrapper.py :: _getCache() - Cache miss: POST https://httpbin.org/anything/one
2024-08-11 13:09:08,284 [ INFO] DelayWrapper.py :: download() - Delaying by 0s ... POST https://httpbin.org/anything/one
2024-08-11 13:09:08,284 [ INFO] HttpClient.py :: download() - Requesting: POST https://httpbin.org/anything/one
2024-08-11 13:09:08,688 [ INFO] FileCacheWrapper.py :: _getCache() - Cache miss: GET https://httpbin.org/anything/111
2024-08-11 13:09:08,688 [ INFO] DelayWrapper.py :: download() - Delaying by 0s ... GET https://httpbin.org/anything/111
2024-08-11 13:09:08,690 [ INFO] HttpClient.py :: download() - Requesting: GET https://httpbin.org/anything/111
2024-08-11 13:09:08,794 [ INFO] FileCacheWrapper.py :: _getCache() - Cache miss: GET https://httpbin.org/anything/222
2024-08-11 13:09:08,794 [ INFO] DelayWrapper.py :: download() - Delaying by 0s ... GET https://httpbin.org/anything/222
2024-08-11 13:09:08,794 [ INFO] HttpClient.py :: download() - Requesting: GET https://httpbin.org/anything/222
2024-08-11 13:09:08,894 [ INFO] FileCacheWrapper.py :: _getCache() - Cache miss: POST https://httpbin.org/anything/two
2024-08-11 13:09:08,895 [ INFO] DelayWrapper.py :: download() - Delaying by 0s ... POST https://httpbin.org/anything/two
2024-08-11 13:09:08,895 [ INFO] HttpClient.py :: download() - Requesting: POST https://httpbin.org/anything/two
2024-08-11 13:09:08,996 [ INFO] FileCacheWrapper.py :: _getCache() - Cache found: GET https://httpbin.org/anything/111
2024-08-11 13:09:08,999 [ INFO] FileCacheWrapper.py :: _getCache() - Cache found: GET https://httpbin.org/anything/222
```

**Output from second run**

```bash
(venv) C:\apps\download_boss>python demo\demo1.py
2024-08-11 13:09:10,905 [ INFO] FileCacheWrapper.py :: _getCache() - Cache found: POST https://httpbin.org/anything/one
2024-08-11 13:09:10,907 [ INFO] FileCacheWrapper.py :: _getCache() - Cache found: GET https://httpbin.org/anything/111
2024-08-11 13:09:10,907 [ INFO] FileCacheWrapper.py :: _getCache() - Cache found: GET https://httpbin.org/anything/222
2024-08-11 13:09:10,907 [ INFO] FileCacheWrapper.py :: _getCache() - Cache found: POST https://httpbin.org/anything/two
2024-08-11 13:09:10,909 [ INFO] FileCacheWrapper.py :: _getCache() - Cache found: GET https://httpbin.org/anything/111
2024-08-11 13:09:10,909 [ INFO] FileCacheWrapper.py :: _getCache() - Cache found: GET https://httpbin.org/anything/222
```

### 2.2. HttpClient with Kerberos auth

```python
import requests
import os
from requests_kerberos import HTTPKerberosAuth, OPTIONAL

from download_boss.RequestEnvelope import RequestEnvelope
from download_boss.HttpClient import HttpClient
from download_boss.FileCacheWrapper import FileCacheWrapper

# Cache responses in folder
cacheFolder = os.path.join( os.path.dirname(__file__), "cache" )

# Create HTTP client with wrappers
client = FileCacheWrapper( HttpClient(), cacheFolderPath=cacheFolder )

# Create request with Kerberos auth
newUrl = 'https://httpbin.org/anything/kerb'
request = RequestEnvelope(requests.Request(method='POST', url=newUrl, auth=HTTPKerberosAuth(mutual_authentication=OPTIONAL)))
client.download(request)
```

## 3. Maintainer documentation
See: [docs/README_MAINTAINER.md](docs/README_MAINTAINER.md)
