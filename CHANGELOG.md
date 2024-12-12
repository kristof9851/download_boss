# Changelog

## 0.0.7

- RequestEnvelope renamed to HttpRequestEnvelope, added AbstractRequestEnvelope to formalize it. getCacheKey is now part of it, instead of FileCacheWrapper
- Added Boto3LogsRequestEnvelope
- Added logic to FileCacheWrapper to load/save different *RequestEnvelope-s based on the class
- Moved `requests.packages.urllib3.disable_warnings()` to the test files, instead of the source files
- AwsAuthGenerator now only returns raw AWS credentials. Added RequestsAwsAuthGenerator that extends AwsAuthGenerator and returns AWS4Auth object with credentials
- Added Boto3LogsClient for querying CloudWatch logs with Boto3 package

## 0.0.6

- Fix CacheWrapper filectime -> filemtime

## 0.0.5

- Some bugfixes
- Rename clientRetriable params

## 0.0.4

- Added Basic and Aws auth generators
- Added Opensearch API

## 0.0.3

- Added request envelop to further customize the download action
- Change cache file naming pattern
- Made HTTPClient download retries fully customizable 

## 0.0.2

- Added a demo file
- Added logging so it's obvious which wrapper / client is actually doing something
- Fixed FileCacheWrapper bug

## 0.0.1

- First version
