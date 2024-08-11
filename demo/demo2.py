import requests
import os
from requests_kerberos import HTTPKerberosAuth, OPTIONAL

from download_boss.HttpClient import HttpClient
from download_boss.RetryWrapper import RetryWrapper
from download_boss.DelayWrapper import DelayWrapper
from download_boss.FileCacheWrapper import FileCacheWrapper

# Cache responses in folder
cacheFolder = os.path.join( os.path.dirname(__file__), "tmp" )

# Create HTTP client with wrappers
client = FileCacheWrapper( DelayWrapper( RetryWrapper( HttpClient() ), length=0 ), cacheFolderPath=cacheFolder )

# Create request with Kerberos auth
newUrl = 'https://httpbin.org/anything/kerb'
request = requests.Request(method='POST', url=newUrl, auth=HTTPKerberosAuth(mutual_authentication=OPTIONAL))
client.download(request)
