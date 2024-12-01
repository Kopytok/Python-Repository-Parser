import ast
import logging


class ImportVisitor(ast.NodeVisitor):

    def __init__(
        self,
        module_name: str,
    ):
        self.module_name = module_name
        self.import_map = {}

    def visit_Import(self, node: ast.Import):
        """
        import ...
        """
        for alias in node.names:
            logging.info(f"Import: {alias.name} as {alias.asname}")
            self.import_map[alias.asname or alias.name] = alias.name

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """
        from ... import ...
        """
        if node.level > 0:
            # Relative import
            base_module = ".".join(self.module_name.split(".")[:-node.level])
            resolved_module = f"{base_module}.{node.module}".strip(".")
        elif node.module:
            # Absolute import
            resolved_module = node.module
        else:
            raise ValueError("Invalid import statement")

        module = node.module or ""
        for alias in node.names:
            logging.info(f"From {module} import {alias.name} as {alias.asname}")
            full_name = f"{resolved_module}.{alias.name}".strip(".")
            self.import_map[alias.asname or alias.name] = full_name
