import ast

class PythonLinter(ast.NodeVisitor):
    """Performs AST-based linting for Python code."""

    def __init__(self):
        self.issues = []
        self.current_function = None

    # -----------------------------------------------------
    # PUBLIC METHOD
    # -----------------------------------------------------
    def lint(self, code: str):
        self.issues = []

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            self.issues.append({
                "type": "Syntax Error",
                "line": e.lineno,
                "detail": e.msg
            })
            return self.issues

        self.visit(tree)
        return self.issues

    # -----------------------------------------------------
    # AST VISITORS
    # -----------------------------------------------------

    def visit_FunctionDef(self, node):
        self.current_function = node.name
        self.check_function_length(node)
        self.check_missing_docstring(node)
        self.generic_visit(node)

    def visit_If(self, node):
        self.check_complex_condition(node)
        self.generic_visit(node)

    def visit_For(self, node):
        self.check_for_loop(node)
        self.generic_visit(node)

    def visit_While(self, node):
        self.check_while_loop(node)
        self.generic_visit(node)

    def visit_Assign(self, node):
        self.check_unused_assignment(node)
        self.generic_visit(node)

    # -----------------------------------------------------
    # CHECKS
    # -----------------------------------------------------

    def check_missing_docstring(self, node):
        if ast.get_docstring(node) is None:
            self.issues.append({
                "type": "Missing Docstring",
                "line": node.lineno,
                "detail": f"Function '{node.name}' has no docstring."
            })

    def check_function_length(self, node):
        length = node.body[-1].lineno - node.body[0].lineno + 1
        if length > 50:
            self.issues.append({
                "type": "Long Function",
                "line": node.lineno,
                "detail": f"Function '{node.name}' is too long ({length} lines)."
            })

    def check_complex_condition(self, node):
        if isinstance(node.test, ast.BoolOp) and len(node.test.values) > 3:
            self.issues.append({
                "type": "Complex Condition",
                "line": node.lineno,
                "detail": f"Condition has {len(node.test.values)} boolean checks."
            })

    def check_for_loop(self, node):
        if isinstance(node.iter, ast.Call) and getattr(node.iter.func, 'id', None) == 'range':
            if len(node.body) > 20:
                self.issues.append({
                    "type": "Long Loop",
                    "line": node.lineno,
                    "detail": "Loop contains more than 20 statements."
                })

    def check_while_loop(self, node):
        if isinstance(node.test, ast.Name) and node.test.id == "True":
            self.issues.append({
                "type": "Potential Infinite Loop",
                "line": node.lineno,
                "detail": "While True loop detected."
            })

    def check_unused_assignment(self, node):
        targets = [t.id for t in node.targets if isinstance(t, ast.Name)]

        for var in targets:
            if not self._is_used_later(node, var):
                self.issues.append({
                    "type": "Unused Variable",
                    "line": node.lineno,
                    "detail": f"Variable '{var}' is assigned but never used."
                })

    # -----------------------------------------------------
    # Helper Functions
    # -----------------------------------------------------
    def _is_used_later(self, node, var):
        parent = node.parent
        if not parent:
            return False

        for sibling in parent.body:
            if hasattr(sibling, 'value') and isinstance(sibling.value, ast.Name):
                if sibling.value.id == var:
                    return True

        return False
