import ast

class CodeMetricsService:
    def __init__(self, code: str):
        self.code = code
        self.tree = ast.parse(code)
        self.lines = code.count("\n") + 1

    def get_function_count(self):
        return sum(isinstance(node, ast.FunctionDef) for node in ast.walk(self.tree))

    def get_class_count(self):
        return sum(isinstance(node, ast.ClassDef) for node in ast.walk(self.tree))

    def get_average_function_length(self):
        functions = [node for node in ast.walk(self.tree) if isinstance(node, ast.FunctionDef)]
        if not functions:
            return 0
        lengths = []
        for func in functions:
            start = func.lineno
            end = max((getattr(node, 'lineno', start) for node in ast.walk(func)))
            lengths.append(end - start + 1)
        return sum(lengths) / len(lengths)

    def cyclomatic_complexity(self):
        complexity_nodes = (
            ast.If, ast.For, ast.While, ast.And, ast.Or, ast.Try, ast.ExceptHandler
        )
        count = 1
        for node in ast.walk(self.tree):
            if isinstance(node, complexity_nodes):
                count += 1
        return count

    def analyze(self):
        return {
            "total_lines": self.lines,
            "function_count": self.get_function_count(),
            "class_count": self.get_class_count(),
            "average_function_length": round(self.get_average_function_length(), 2),
            "cyclomatic_complexity": self.cyclomatic_complexity()
        }
