from requests import Request
from download_boss.RequestEnvelope import RequestEnvelope
from download_boss.HttpClient import HttpClient

request = RequestEnvelope(
    Request(method='POST', url='https://httpbin.org/anything/hello', json={"hello": "world"}),
    {'verify': False, 'timeout': 10}
)
response = HttpClient().download(request)
print(response.text)

"""
2024-12-03 11:00:11,227 [ INFO] HttpClient.py :: download() - Requesting: POST https://httpbin.org/anything/hello
{
  "args": {}, 
  "data": "{\"hello\": \"world\"}", 
  "files": {}, 
  "form": {}, 
  "headers": {
    "Accept-Encoding": "identity", 
    "Content-Length": "18", 
    "Content-Type": "application/json", 
    "Host": "httpbin.org", 
    "User-Agent": "python-urllib3/2.2.3", 
    "X-Amzn-Trace-Id": "Root=1-674ee4bb-51982739127f1458babf58"
  }, 
  "json": {
    "hello": "world"
  }, 
  "method": "POST", 
  "origin": "111.444.222.111", 
  "url": "https://httpbin.org/anything/hello"
}
"""
