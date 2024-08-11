import requests
import os
import json

from download_boss.HttpClient import HttpClient
from download_boss.RetryWrapper import RetryWrapper
from download_boss.DelayWrapper import DelayWrapper
from download_boss.FileCacheWrapper import FileCacheWrapper

# Cache responses in folder
cacheFolder = os.path.join( os.path.dirname(__file__), "tmp" )

# Create HTTP client with wrappers
client = FileCacheWrapper( DelayWrapper( RetryWrapper( HttpClient() ), length=0 ), cacheFolderPath=cacheFolder )

# Download two responses
jsonBaseUrl = 'https://httpbin.org/anything/'
jsonIds = ['one', 'two']

for id in jsonIds:
    # Send data with the request, so we can use read it from the response
    request = requests.Request(method='POST', url=jsonBaseUrl + id, json=[{"subId": "111"}, {"subId": "222"}])
    response = client.download(request)
    
    # Use the response to construct sub-requests
    jsonText = json.loads(response.text)
    for o in jsonText['json']:
        sid = o['subId']

        # Download and cache subrequests
        newUrl = 'https://httpbin.org/anything/' + sid
        request = requests.Request(method='GET', url=newUrl)
        client.download(request)

# The second time this is run, it will run instantly because FileCacheWrapper's cacheLength is not set (=None) so it caches responses indefinitely