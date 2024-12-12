import logging
from abc import ABC, abstractmethod

from .util.Logs import Logs

logging.basicConfig(level=Logs.LEVEL, format=Logs.FORMAT)

class AbstractRequestEnvelope(ABC):

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def getCacheKey(self):
        pass
