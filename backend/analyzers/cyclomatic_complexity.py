import ast

class ComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.complexity = 1

    def generic_visit(self, node):
        if isinstance(node, (
            ast.If, ast.For, ast.While,
            ast.And, ast.Or,
            ast.Try, ast.ExceptHandler,
            ast.With, ast.FunctionDef,
            ast.AsyncFunctionDef,
            ast.BoolOp, ast.Compare
        )):
            self.complexity += 1

        super().generic_visit(node)


def get_function_complexity(code: str):
    tree = ast.parse(code)
    results = []

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            visitor = ComplexityVisitor()
            visitor.visit(node)
            results.append({
                "name": node.name,
                "complexity": visitor.complexity
            })

    return results
