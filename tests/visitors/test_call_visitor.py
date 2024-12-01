import logging
import os
from pyrepa.helpers import parse_ast
from pyrepa.visitors.import_visitor import ImportVisitor
from pyrepa.visitors.call_visitor import CallVisitor


def test_functions_call_visitor(repo_path):
    # Setup
    module_name = "module.name"
    tree = parse_ast(os.path.join(repo_path, "main.py"))

    import_visitor = ImportVisitor(
        module_name=module_name,
    )
    import_visitor.visit(tree)
    import_map = import_visitor.import_map
    expected_dependencies = [
        (f"{module_name}.main_func", "fruits.Apple"),
        (f"{module_name}.main_func", "fruits.Banana"),
        (f"{module_name}.main_func", "utils.proceed"),
    ]

    # Run
    visitor = CallVisitor(
        module_name=module_name,
        import_map=import_map,
    )
    visitor.visit(tree)

    # Check
    assert visitor.dependencies == expected_dependencies, \
        "Wrong dependencies after visiting tree"


def test_class_call_visitor(repo_path):
    # Setup
    module_name = "fruits.banana"
    tree = parse_ast(os.path.join(repo_path, "fruits/banana.py"))
    import_visitor = ImportVisitor(
        module_name=module_name,
    )
    import_visitor.visit(tree)
    import_map = import_visitor.import_map
    expected_dependencies = [
        ("fruits.banana.Banana", "fruits.base.BaseFruit"),
    ]

    # Run
    visitor = CallVisitor(
        module_name=module_name,
        import_map=import_map,
    )
    visitor.visit(tree)

    # Check
    assert visitor.dependencies == expected_dependencies, \
        "Wrong dependencies after visiting tree"


def test_assign_call_visitor(repo_path):
    # Setup
    module_name = "utils"
    tree = parse_ast(os.path.join(repo_path, "utils.py"))
    import_visitor = ImportVisitor(
        module_name=module_name,
    )
    import_visitor.visit(tree)
    import_map = import_visitor.import_map
    logging.info(f"{import_map}")
    expected_dependencies = [
        ("utils.APPLE_PROXY", "fruits.Apple"),
        ("utils.FRUITS_LIST_1", "fruits.Apple"),
        ("utils.FRUITS_LIST_1", "fruits.Banana"),
        ("utils.FRUITS_LIST_2", "fruits.Apple"),
        ("utils.FRUITS_LIST_2", "fruits.Banana"),
        ("utils.FRUITS_TUPLE", "fruits.Apple"),
        ("utils.FRUITS_TUPLE", "fruits.Banana"),
        ("utils.FRUITS_DICT", "fruits.Apple"),
        ("utils.FRUITS_DICT", "fruits.Banana"),
        ("utils.ENCAPSULATED_LIST", "fruits.Apple"),
        ("utils.ENCAPSULATED_LIST", "fruits.Banana"),
        ("utils.proceed", "actions.eat"),
        ("utils.proceed", "actions.action_throw.throw"),
    ]

    # Run
    visitor = CallVisitor(
        module_name=module_name,
        import_map=import_map,
    )
    visitor.visit(tree)

    # Check
    assert visitor.dependencies == expected_dependencies, \
        "Wrong dependencies after visiting tree"
