import os
import ast
from pathlib import Path
from typing import Generator, Union

from pyrepa.errors import CantParseError


def get_module_name(
    file_path: str,
    root_dir: Path,
) -> str:
    """
    Construct a python module_name from:
    - python file_path
    - project root directory
    """
    module_name = (
        os.path.relpath(file_path, root_dir)
        .replace(os.sep, ".")
    )
    if module_name.endswith(".py"):
        module_name = module_name[:-3]

    return module_name


def iter_file_paths(
    root_dir: Union[str, Path],
) -> Generator[str, None, None]:
    """
    Iterate over all python files in a repository
    Return a tuple of ('file_name.py', '/file_path/file_name.py')
    """
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                yield os.path.join(root, file)


def parse_ast(file_path: str) -> ast.AST:
    """
    Parse a python file into an Abstract Syntax Tree (AST)
    """
    with open(file_path, "r", encoding="utf-8") as file:
        try:
            return ast.parse(file.read(), filename=file_path)
        except SyntaxError:
            raise CantParseError(file_path)
