import ast
import os
import logging

from typing import List, Tuple
from pathlib import Path


logging.basicConfig(level=logging.INFO)


def parse_one_file(file_path: str) -> List[Tuple[str, str]]:
    logging.info(f"Parsing {file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        try:
            tree = ast.parse(file.read(), filename=file_path)
        except SyntaxError:
            return []

    logging.info(f"{tree=}")

    dependencies = []
    import_map = {}

    class ImportVisitor(ast.NodeVisitor):

        def visit_Import(self, node: ast.Import):
            for alias in node.names:
                import_map[alias.asname or alias.name] = alias.name

        def visit_ImportFrom(self, node: ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                full_name = f"{module}.{alias.name}".strip(".")
                import_map[alias.asname or alias.name] = full_name

    class FunctionVisitor(ast.NodeVisitor):

        def __init__(self, current_module: str):
            self.current_module = current_module
            self.current_function = None

        def visit_FunctionDef(self, node: ast.FunctionDef):
            self.current_function = f"{self.current_module}.{node.name}"
            self.generic_visit(node)
            self.current_function = None

        def visit_Call(self, node: ast.Call):

            if self.current_function:

                if isinstance(node.func, ast.Name):
                    called_name = import_map.get(node.func.id, node.func.id)
                    dependencies.append(
                        (self.current_function, called_name)
                    )

                elif isinstance(node.func, ast.Attribute):
                    value = node.func.value
                    if isinstance(value, ast.Name):
                        base_name = import_map.get(value.id, value.id)
                        called_name = f"{base_name}.{node.func.attr}"
                        dependencies.append(
                            (self.current_function, called_name)
                        )

            self.generic_visit(node)

    module_path = file_path.replace("/", ".").replace("\\", ".").rstrip(".py")
    visitor = FunctionVisitor(current_module=module_path)
    resolver = ImportVisitor()
    resolver.visit(tree)
    visitor.visit(tree)
    return dependencies


def analyze_project(path: Path) -> List[Tuple[str, str]]:
    dependencies = []
    logging.info(f"Analyzing project at {path=}")
    for root, _, files in os.walk(path):
        logging.info(f"Analyzing {root=}, {files=}")
        for file in files:
            logging.info(f"Analyzing {file=}")
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                dependencies.extend(parse_one_file(file_path))
    return dependencies
