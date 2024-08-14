import logging
from abc import ABC, abstractmethod

from .util.Logs import Logs

logging.basicConfig(level=Logs.LEVEL, format=Logs.FORMAT)

class AbstractClient(ABC):

    @abstractmethod
    def download(self, requestEnvelope):
        pass
