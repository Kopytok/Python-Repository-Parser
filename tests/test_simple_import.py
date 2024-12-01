import logging
from pathlib import Path

from pyrepa import analyze_project


def test_analyze_project():
    expected_dependencies = {
        ("actions.eat", "actions.action_eat.eat"),
        ("fruits.Apple", "fruits.apple.Apple"),
        ("fruits.Banana", "fruits.banana.Banana"),
        ("fruits.banana.Banana", "fruits.base.BaseFruit"),
        ("fruits.base.BaseFruit", "abc.ABC"),
        ("main.main_func", "fruits.Apple"),
        ("main.main_func", "fruits.Banana"),
        ("main.main_func", "utils.proceed"),
        ("utils.APPLE_PROXY", "fruits.Apple"),
        ("utils.ENCAPSULATED_LIST", "fruits.Apple"),
        ("utils.ENCAPSULATED_LIST", "fruits.Banana"),
        ("utils.FRUITS_DICT", "fruits.Apple"),
        ("utils.FRUITS_DICT", "fruits.Banana"),
        ("utils.FRUITS_LIST_1", "fruits.Apple"),
        ("utils.FRUITS_LIST_1", "fruits.Banana"),
        ("utils.FRUITS_LIST_2", "fruits.Apple"),
        ("utils.FRUITS_LIST_2", "fruits.Banana"),
        ("utils.FRUITS_TUPLE", "fruits.Apple"),
        ("utils.FRUITS_TUPLE", "fruits.Banana"),
        ("utils.proceed", "actions.action_throw.throw"),
        ("utils.proceed", "actions.eat"),
    }

    path = Path("tests/sample_project")
    dependencies = analyze_project(path)
    logging.info(dependencies)
    assert set(dependencies) == expected_dependencies
