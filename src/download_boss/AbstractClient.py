from abc import ABC, abstractmethod

class AbstractClient(ABC):

    @abstractmethod
    def download(self, request):
        pass
