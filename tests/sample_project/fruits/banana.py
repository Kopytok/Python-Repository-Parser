from .base import BaseFruit


class IgnoreThisClass:
    pass


class Banana(BaseFruit, IgnoreThisClass):

    @property
    def color(self) -> str:
        return "yellow"

    def fall(self):
        pass
