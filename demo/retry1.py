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
