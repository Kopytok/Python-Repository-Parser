from utils import proceed
from fruits import Apple, Banana


def local_func_ignored():
    """ This is ignored, since not imported """
    pass


def main_func():
    local_func_ignored()

    apple = Apple()
    _ = apple.color
    apple.fall()

    banana = Banana()
    banana.fall()

    proceed()
