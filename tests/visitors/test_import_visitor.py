import os
from pyrepa.helpers import parse_ast
from pyrepa.visitors.import_visitor import ImportVisitor


def test_functions_import_visitor(repo_path):
    # Setup
    module_name = "module.name"
    tree = parse_ast(os.path.join(repo_path, "main.py"))
    expected_imports = {
        "Apple": "fruits.Apple",
        "Banana": "fruits.Banana",
        "proceed": "utils.proceed",
    }

    # Run
    visitor = ImportVisitor(
        module_name=module_name,
    )
    visitor.visit(tree)

    # Check
    assert visitor.import_map == expected_imports, \
        "Wrong imports after visiting tree"


def test_classes_import_visitor(repo_path):
    # Setup
    module_name = "fruits.banana"
    tree = parse_ast(os.path.join(repo_path, "fruits/banana.py"))
    expected_imports = {
        "BaseFruit": "fruits.base.BaseFruit",
    }

    # Run
    visitor = ImportVisitor(
        module_name=module_name,
    )
    visitor.visit(tree)

    # Check
    assert visitor.import_map == expected_imports, \
        "Wrong imports after visiting tree"
