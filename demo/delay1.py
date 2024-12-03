from requests import Request
from download_boss.RequestEnvelope import RequestEnvelope
from download_boss.HttpClient import HttpClient
from download_boss.RetryWrapper import RetryWrapper
from download_boss.DelayWrapper import DelayWrapper
from download_boss.error.RetriesExhausted import RetriesExhausted

client = HttpClient(throwRetriableStatusCodeRanges=[401, range(500,599)]) # Throw ClientRetriable error for some status codes
client = RetryWrapper(client, count=1, catchRetriableStatusCodeRanges=[range(500,599)]) # Retry 1x if ClientRetriable error is thrown for these
client = DelayWrapper(client, length=2, maxLength=5) # Delay download calls by 2-5 seconds (randomly generated in-between the two)

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
