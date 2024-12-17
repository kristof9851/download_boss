# Download Boss
![Python CI Build](https://github.com/kristof9851/download_boss/actions/workflows/python-ci.yml/badge.svg)
![PyPI Downloads](https://img.shields.io/pypi/dm/download_boss?label=PyPI%20Downloads&color=rgb(50%2C%20165%2C%20233)
)
![PyPI Version](https://img.shields.io/pypi/v/download_boss)


*Python download library*

## 1. Installation

```bash
pip install download_boss
```

&nbsp;

## 2. Usage

### 2.1 HttpClient
Simple request
```python
from requests import Request
from download_boss.RequestEnvelope import RequestEnvelope
from download_boss.HttpClient import HttpClient

request = RequestEnvelope(
    Request(method='POST', url='https://httpbin.org/anything/hello', json={"hello": "world"},
    {'verify': False, 'timeout': 10})
)
response = HttpClient().download(request)
print(response.text)

```

Retry based on HTTP status codes
```python
from requests import Request
from download_boss.RequestEnvelope import RequestEnvelope
from download_boss.HttpClient import HttpClient
from download_boss.error.ClientRetriable import ClientRetriable

request = RequestEnvelope(
    Request(method='GET', url='https://httpbin.org/anything/hello')
)
client = HttpClient(throwRetriableStatusCodeRanges=[401, range(500,599)])

while True:
    try:
        response = client.download(request)
        print(response.text)
        break
    except ClientRetriable:
        continue

```

Kerberos authentication:
```python
from requests import Request
from requests_kerberos import HTTPKerberosAuth, OPTIONAL
from download_boss.RequestEnvelope import RequestEnvelope
from download_boss.HttpClient import HttpClient

request = RequestEnvelope(
    Request(method='POST', url='https://httpbin.org/anything/kerb', auth=HTTPKerberosAuth(mutual_authentication=OPTIONAL))
)
response = HttpClient().download(request)
```

### 2.2. RetryWrapper

Retry automatically some HTTP status codes
```python
from requests import Request
from download_boss.RequestEnvelope import RequestEnvelope
from download_boss.HttpClient import HttpClient
from download_boss.RetryWrapper import RetryWrapper
from download_boss.error.RetriesExhausted import RetriesExhausted

request = RequestEnvelope(
    Request(method='GET', url='https://httpbin.org/status/500')
)
client = HttpClient(throwRetriableStatusCodeRanges=[401, range(500,599)])
client = RetryWrapper(client, count=1, catchRetriableStatusCodeRanges=[range(500,599)])

try:
    response = client.download(request)
except RetriesExhausted:
    print("Retries exhausted!")

"""
2024-12-03 11:51:10,085 [ INFO] HttpClient.py :: download() - Requesting: GET https://httpbin.org/status/500
2024-12-03 11:51:10,485 [ INFO] RetryWrapper.py :: download() - Retrying... GET https://httpbin.org/status/500
2024-12-03 11:52:10,485 [ INFO] HttpClient.py :: download() - Requesting: GET https://httpbin.org/status/500
Retries exhausted!
"""
```

### 2.3. DelayWrapper

Delay download calls by 2-5 seconds

```python
from requests import Request
from download_boss.RequestEnvelope import RequestEnvelope
from download_boss.HttpClient import HttpClient
from download_boss.RetryWrapper import RetryWrapper
from download_boss.DelayWrapper import DelayWrapper
from download_boss.error.RetriesExhausted import RetriesExhausted

client = HttpClient(throwRetriableStatusCodeRanges=[401, range(500,599)])
client = RetryWrapper(client, count=1, catchRetriableStatusCodeRanges=[range(500,599)]) 
client = DelayWrapper(client, length=2, maxLength=5) 

requests = [
    RequestEnvelope( Request(method='GET', url='https://httpbin.org/anything/one') ),
    RequestEnvelope( Request(method='GET', url='https://httpbin.org/anything/two') ),
    RequestEnvelope( Request(method='GET', url='https://httpbin.org/anything/three') )
]

for r in requests:
    response = client.download(r)

"""
2024-12-03 12:00:28,804 [ INFO] DelayWrapper.py :: download() - Delaying by 3s ... GET https://httpbin.org/anything/one
2024-12-03 12:00:31,805 [ INFO] HttpClient.py :: download() - Requesting: GET https://httpbin.org/anything/one
2024-12-03 12:00:32,206 [ INFO] DelayWrapper.py :: download() - Delaying by 2s ... GET https://httpbin.org/anything/two
2024-12-03 12:00:34,208 [ INFO] HttpClient.py :: download() - Requesting: GET https://httpbin.org/anything/two
2024-12-03 12:00:34,827 [ INFO] DelayWrapper.py :: download() - Delaying by 5s ... GET https://httpbin.org/anything/three
2024-12-03 12:00:39,830 [ INFO] HttpClient.py :: download() - Requesting: GET https://httpbin.org/anything/three
"""

```

### 2.4. FileCacheWrapper
```python
from os.path import join, dirname
from requests import Request
from download_boss.RequestEnvelope import RequestEnvelope
from download_boss.HttpClient import HttpClient
from download_boss.RetryWrapper import RetryWrapper
from download_boss.DelayWrapper import DelayWrapper
from download_boss.FileCacheWrapper import FileCacheWrapper

cacheFolderPath = join(dirname(__file__), "cache")
cacheLength = 60*60*24 # 1 day

client = HttpClient(throwRetriableStatusCodeRanges=[401, range(500,599)]) 
client = RetryWrapper(client, count=1, catchRetriableStatusCodeRanges=[range(500,599)]) 
client = DelayWrapper(client, length=2, maxLength=5)
client = FileCacheWrapper(client, cacheFolderPath, cacheLength)

requests = [
    RequestEnvelope( Request(method='GET', url='https://httpbin.org/anything/one') ),
    RequestEnvelope( Request(method='GET', url='https://httpbin.org/anything/one') ),
    RequestEnvelope( Request(method='GET', url='https://httpbin.org/anything/one') )
]

for r in requests:
    response = client.download(r)

"""
2024-12-03 13:26:24,921 [ INFO] FileCacheWrapper.py :: _getCache() - Cache miss: GET https://httpbin.org/anything/one
2024-12-03 13:26:24,921 [ INFO] DelayWrapper.py :: download() - Delaying by 3s ... GET https://httpbin.org/anything/one
2024-12-03 13:26:27,923 [ INFO] HttpClient.py :: download() - Requesting: GET https://httpbin.org/anything/one
2024-12-03 13:26:27,956 [DEBUG] connectionpool.py :: _new_conn() - Starting new HTTPS connection (1): httpbin.org:443
2024-12-03 13:26:29,256 [DEBUG] connectionpool.py :: _make_request() - https://httpbin.org:443 "GET /anything/one HTTP/11" 200 370
2024-12-03 13:26:29,257 [DEBUG] FileCacheWrapper.py :: _getCache() - Cache found: GET https://httpbin.org/anything/one
2024-12-03 13:26:29,263 [DEBUG] FileCacheWrapper.py :: _getCache() - Cache found: GET https://httpbin.org/anything/one
"""
```

&nbsp;

## 3. Contribute

### 3.1. Install locally

Install pip/python.

Clone the project.

Create virtual env:
```bash
# Install virtualenv module
pip install --upgrade virtualenv
cd <PROJECT_ROOT>

# Create venv in your project
python -m venv venv

# Activate your virtual environment (Windows)
.\venv\Scripts\activate

# Activate your virtual environment (Linux)
chmod +x venv/bin/activate
source venv/bin/activate
```

Install project dependencies:
```bash
pip install -r requirements.txt
```

Install module locally as editable
```bash
pip install -e .
```

&nbsp;

### 3.2. Testing

```bash
# Run test suite (Windows)
.\wtests.bat

# Run test suite (Linux)
./tests.sh
```

&nbsp;

### 3.3. Release (automated)

Git add/commit/push to GitHub. The GitHub action will automatically publish the new version to PyPi.

&nbsp;

### 3.4. Release (manual)

Install dependencies

```bash
pip install --upgrade setuptools wheel build twine
```

Build the package (wheel and sdist)
```bash
python -m build 
```

Ensure `.pypirc` in user folder is correct, then upload
```bash
python -m twine upload dist/*
```
