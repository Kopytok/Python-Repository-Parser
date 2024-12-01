from abc import ABC, abstractmethod


class BaseFruit(ABC):

    @property
    @abstractmethod
    def color(self) -> str:
        pass

    @abstractmethod
    def fall(self):
        pass
