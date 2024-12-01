import ast
import logging
from typing import Dict


class InitImportVisitor(ast.NodeVisitor):

    def __init__(
        self,
        *,
        module_name: str,
        init_imports: Dict[str, str],
    ):
        self.module_name = module_name.replace(".__init__", "")
        self.init_imports = init_imports

    def visit_Import(self, node: ast.Import):
        """
        __init__.py
        import ...
        """
        for alias in node.names:
            k = f"{self.module_name}.{alias.asname or alias.name}"
            v = f"{self.module_name}.{alias.name}"
            logging.info(f"Init import: {k} -> {v}")
            self.init_imports[k] = v

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """
        __init__.py
        from ... import ...
        """
        module = node.module or ""
        module = f"{self.module_name}.{module.lstrip('.')}"

        for alias in node.names:
            imported_name = alias.asname or alias.name
            k = f"{self.module_name}.{imported_name}"
            v = f"{module}.{alias.name}".lstrip(".")
            logging.info(f"Init import from: {k} -> {v}")
            self.init_imports[k] = v
