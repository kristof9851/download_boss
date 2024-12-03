from os.path import join, dirname
from requests import Request
from download_boss.RequestEnvelope import RequestEnvelope
from download_boss.HttpClient import HttpClient
from download_boss.RetryWrapper import RetryWrapper
from download_boss.DelayWrapper import DelayWrapper
from download_boss.FileCacheWrapper import FileCacheWrapper

cacheFolderPath = join(dirname(__file__), "cache")
cacheLength = 60*60*24 # 1 day

client = HttpClient(throwRetriableStatusCodeRanges=[401, range(500,599)]) # Throw ClientRetriable error for some status codes
client = RetryWrapper(client, count=1, catchRetriableStatusCodeRanges=[range(500,599)]) # Retry 1x if ClientRetriable error is thrown for these
client = DelayWrapper(client, length=2, maxLength=5) # Delay download calls by 2-5 seconds (randomly generated in-between the two)
client = FileCacheWrapper(client, cacheFolderPath, cacheLength)

requests = [
    RequestEnvelope( Request(method='GET', url='https://httpbin.org/anything/one') ),
    RequestEnvelope( Request(method='GET', url='https://httpbin.org/anything/one') ),
    RequestEnvelope( Request(method='GET', url='https://httpbin.org/anything/one') )
]

for r in requests:
    response = client.download(r)
    print('Received response!')

"""
2024-12-03 13:26:24,921 [ INFO] FileCacheWrapper.py :: _getCache() - Cache miss: GET https://httpbin.org/anything/one
2024-12-03 13:26:24,921 [ INFO] DelayWrapper.py :: download() - Delaying by 3s ... GET https://httpbin.org/anything/one
2024-12-03 13:26:27,923 [ INFO] HttpClient.py :: download() - Requesting: GET https://httpbin.org/anything/one
2024-12-03 13:26:27,956 [DEBUG] connectionpool.py :: _new_conn() - Starting new HTTPS connection (1): httpbin.org:443
2024-12-03 13:26:29,256 [DEBUG] connectionpool.py :: _make_request() - https://httpbin.org:443 "GET /anything/one HTTP/11" 200 370
Received response!
2024-12-03 13:26:29,257 [DEBUG] FileCacheWrapper.py :: _getCache() - Cache found: GET https://httpbin.org/anything/one
Received response!
2024-12-03 13:26:29,263 [DEBUG] FileCacheWrapper.py :: _getCache() - Cache found: GET https://httpbin.org/anything/one
Received response!
"""
