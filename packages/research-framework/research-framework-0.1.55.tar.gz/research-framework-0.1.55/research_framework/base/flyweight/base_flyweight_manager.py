from abc import ABC, abstractmethod

class BaseFlyManager(ABC):
    @abstractmethod
    def fit(self, data_hashcode:str, data): ...
    @abstractmethod
    def predict(self, data_hashcode:str, data_name:str, data): ...