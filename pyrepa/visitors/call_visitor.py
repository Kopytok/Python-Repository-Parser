import ast
import builtins
import logging

from typing import Dict


BUILTINS = dir(builtins)


class CallVisitor(ast.NodeVisitor):

    def __init__(
        self,
        module_name: str,
        import_map: Dict[str, str],
    ):
        self.module_name = module_name
        self.current_function = None
        self.variable_map = {}
        self.import_map = import_map
        self.dependencies = []

    def resolve_name(self, target_name: str, node: ast.Name):
        if isinstance(node, ast.Name):
            # Ignore builtins
            if node.id in BUILTINS:
                return None

            # Ignore functions that are not imported
            if node.id not in self.import_map:
                return None

            called_name = self.import_map.get(node.id)
            self.dependencies.append((target_name, called_name))

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """
        def function_name():
        """
        self.current_function = f"{self.module_name}.{node.name}"
        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node: ast.Call):
        """
        function(*args, **kwargs)
        """
        if self.current_function:

            if isinstance(node.func, ast.Name):
                self.resolve_name(self.current_function, node.func)

            elif isinstance(node.func, ast.Attribute):
                pass

        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        """
        class ClassName():
        """
        class_name = f"{self.module_name}.{node.name}"
        for base in node.bases:
            if isinstance(base, ast.Name):
                if base.id not in self.import_map:
                    continue
                base_name = self.import_map.get(base.id, base.id)
                if base_name:
                    # Direct inheritance
                    # `class ClassName(BaseName):`
                    logging.info(f"{base_name} -> {class_name}")
                    logging.info(f"{self.import_map}")
                    self.dependencies.append(
                        (class_name, base_name)
                    )

            elif isinstance(base, ast.Attribute):
                # Reference to a class attribute
                # `class ClassName(module.BaseName):`
                if isinstance(base.value, ast.Name):
                    if base.value.id not in self.import_map:
                        continue
                    base_name = base.value.id
                    base_class_name = (
                        f"{self.import_map.get(base_name, base_name)}"
                        f".{base.attr}"
                    )

                else:
                    base_class_name = base.attr

                if base_class_name:
                    self.dependencies.append(
                        (class_name, base_class_name)
                    )

        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        """
        variable = value
        variable =[
            value1,
            value2,
            ...
        ], etc.
        """
        for target in node.targets:
            if isinstance(target, ast.Name):
                if (
                    isinstance(node.value, ast.List)
                    or isinstance(node.value, ast.Tuple)
                    or isinstance(node.value, ast.Set)
                ):
                    for value in node.value.elts:
                        if isinstance(value, ast.Name):
                            if value.id in self.import_map:
                                calling_name = f"{self.module_name}.{target.id}"
                                called_name = self.import_map.get(value.id)
                                self.dependencies.append(
                                    (calling_name, called_name)
                                )
                        elif isinstance(value, ast.Call):
                            for arg in value.args:
                                for o in arg.elts:
                                    if isinstance(o, ast.Name):
                                        if o.id in self.import_map:
                                            calling_name = f"{self.module_name}.{target.id}"
                                            called_name = self.import_map.get(o.id)
                                            self.dependencies.append(
                                                (calling_name, called_name)
                                            )

                        else:
                            raise NotImplementedError(
                                f"Unsupported value type: {value}"
                            )

                elif isinstance(node.value, ast.Name):
                    if node.value.id in self.import_map:
                        call_name = self.import_map.get(node.value.id)
                        self.dependencies.append(
                            (f"{self.module_name}.{target.id}", call_name)
                        )

                elif isinstance(node.value, ast.Dict):
                    for value in node.value.values:
                        if isinstance(value, ast.Name):
                            if value.id in self.import_map:
                                calling_name = f"{self.module_name}.{target.id}"
                                called_name = self.import_map.get(value.id)
                                self.dependencies.append(
                                    (calling_name, called_name)
                                )

        self.generic_visit(node)
