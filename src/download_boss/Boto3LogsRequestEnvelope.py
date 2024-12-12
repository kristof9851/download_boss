import hashlib

from .AbstractRequestEnvelope import AbstractRequestEnvelope

class Boto3LogsRequestEnvelope(AbstractRequestEnvelope):

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __repr__(self):
        NL = '\n'
        return f'{self.kwargs["queryString"][0:150].replace(NL, " ")}...'

    def getCacheKey(self):
        sorted_kwargs = {k: self.kwargs[k] for k in sorted(self.kwargs)}

        hash = hashlib.md5(str(sorted_kwargs).encode()).hexdigest()

        return 'boto3-logs-request_' + hash + '.txt'
    