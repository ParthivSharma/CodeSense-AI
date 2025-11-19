import ast

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.imports = []

    def analyze(self, code: str):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {
                "error": f"Syntax Error: {e}"
            }

        self.visit(tree)

        suggestions = []

        # Rule 1: Too many functions
        if len(self.functions) > 10:
            suggestions.append("Your file has too many functions. Consider splitting the code.")

        # Rule 2: Missing docstrings
        for func in self.functions:
            if ast.get_docstring(func) is None:
                suggestions.append(f"Function '{func.name}' has no docstring.")

        # Rule 3: Unused imports
        # (simple placeholder rule)
        if self.imports and len(self.functions) == 0:
            suggestions.append("You imported modules but did not use any functions.")

        return {
            "total_functions": len(self.functions),
            "imports": self.imports,
            "suggestions": suggestions
        }

    def visit_FunctionDef(self, node):
        self.functions.append(node)
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.append(node.module)
        self.generic_visit(node)
