import requests
import os
import json

from download_boss.HttpClient import HttpClient
from download_boss.RetryWrapper import RetryWrapper
from download_boss.DelayWrapper import DelayWrapper
from download_boss.FileCacheWrapper import FileCacheWrapper

tmpFolder = os.path.join( os.path.dirname(__file__), "tmp" )
client = FileCacheWrapper( DelayWrapper( RetryWrapper( HttpClient() ), length=0 ), cacheFolderPath=tmpFolder )

jsonBaseUrl = 'https://httpbin.org/anything/'
jsonIds = ['one', 'two']

for id in jsonIds:
    request = requests.Request(method='POST', url=jsonBaseUrl + id, json=[{"subId": "111"}, {"subId": "222"}])
    response = client.download(request)
    
    jsonText = json.loads(response.text)
    for o in jsonText['json']:
        sid = o['subId']

        newUrl = 'https://httpbin.org/anything/' + sid
        request = requests.Request(method='GET', url=newUrl)
        client.download(request)
