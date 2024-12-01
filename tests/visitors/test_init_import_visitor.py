import os
from pyrepa.helpers import parse_ast
from pyrepa.visitors.init_import_visitor import InitImportVisitor


def test_init_import_visitor(repo_path):
    # Setup
    module_name = "module.name"
    tree = parse_ast(
        os.path.join(repo_path, "fruits/__init__.py")
    )
    expected_init_imports = {
        f"{module_name}.Apple": f"{module_name}.apple.Apple",
        f"{module_name}.Banana": f"{module_name}.banana.Banana",
    }

    # Run
    init_imports = {}
    visitor = InitImportVisitor(
        # __init__ is added in collect_init_imports.py
        module_name=module_name + ".__init__",
        init_imports=init_imports,
    )
    visitor.visit(tree)

    # Check
    assert visitor.init_imports == expected_init_imports, \
        "Wrong init_imports after visiting tree"
