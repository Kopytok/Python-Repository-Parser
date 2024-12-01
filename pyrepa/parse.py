import os
import logging

from typing import Dict, List, Tuple
from pathlib import Path

from pyrepa.errors import CantParseError
from pyrepa.helpers import (
    get_module_name,
    iter_file_paths,
    parse_ast,
)
from pyrepa.visitors import (
    InitImportVisitor,
    ImportVisitor,
    CallVisitor,
)

logging.basicConfig(level=logging.INFO)


def collect_init_imports(
    root_dir: Path,
) -> Dict[str, str]:

    init_imports = {}
    for file_path in iter_file_paths(root_dir):
        if file_path.split(os.sep)[-1] == "__init__.py":

            try:
                tree = parse_ast(file_path)
            except CantParseError:
                continue

            visitor = InitImportVisitor(
                module_name=get_module_name(file_path, root_dir),
                init_imports=init_imports,
            )
            visitor.visit(tree)

    return init_imports


def parse_one_file(
    file_path: str,
    root_dir: Path,
) -> List[Tuple[str, str]]:
    try:
        tree = parse_ast(file_path)
    except CantParseError:
        return []

    module_name = get_module_name(file_path, root_dir)

    import_visitor = ImportVisitor(
        module_name=module_name,
    )
    import_visitor.visit(tree)

    function_visitor = CallVisitor(
        module_name=module_name,
        import_map=import_visitor.import_map,
    )
    function_visitor.visit(tree)

    return function_visitor.dependencies


def collect_dependencies(
    root_dir: Path,
) -> List[Tuple[str, str]]:
    dependencies = []
    for file_path in iter_file_paths(root_dir):
        dependencies.extend(parse_one_file(file_path, root_dir))
    return dependencies


def analyze_project(path: Path) -> List[Tuple[str, str]]:
    init_imports = collect_init_imports(path)
    dependencies = collect_dependencies(path)
    for k, v in init_imports.items():
        dependencies.append((k, v))
    return dependencies
