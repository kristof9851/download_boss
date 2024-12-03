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

"""
2024-12-03 11:38:51,769 [ INFO] HttpClient.py :: download() - Requesting: GET https://httpbin.org/anything/hello
{
  "args": {}, 
  "data": "", 
  "files": {}, 
  "form": {}, 
  "headers": {
    "Accept-Encoding": "identity", 
    "Host": "httpbin.org", 
    "User-Agent": "python-urllib3/2.2.3", 
    "X-Amzn-Trace-Id": "Root=1-2f23f23f-0943248b7acf4f3076e1b936c"
  }, 
  "json": null, 
  "method": "GET", 
  "origin": "111.222.333.444", 
  "url": "https://httpbin.org/anything/hello"
}
"""
