from actions import eat
from actions.action_throw import throw

from fruits import Apple, Banana


APPLE_PROXY = Apple
FRUITS_LIST_1 = FRUITS_LIST_2 = [Apple, Banana]
FRUITS_TUPLE = (Apple, Banana)
FRUITS_DICT = {
    "apple": Apple,
    "banana": Banana,
}
ENCAPSULATED_LIST = [
    len([Apple, Banana]),
]


def proceed():
    eat()
    throw()
