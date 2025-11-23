import ast

def detect_unused_imports(code: str):
    tree = ast.parse(code)

    imported_names = set()
    used_names = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_names.add(alias.asname or alias.name.split('.')[0])

        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imported_names.add(alias.asname or alias.name)

        elif isinstance(node, ast.Name):
            used_names.add(node.id)

    return list(imported_names - used_names)
