"""
Integrated Code Analyzer service.

Entry:
 - analyze(code: str, language: str) -> Dict

Uses:
 - PythonLinter
 - JSLinter
 - CppLinter
 - ast_utils.add_parents
"""

from typing import Dict, Any
import traceback
import ast

from backend.services.python_linter import PythonLinter
from backend.services.js_linter import JSLinter
from backend.services.cpp_linter import CppLinter
from backend.services.ast_utils import add_parents

# NEW
from backend.analyzers.unused_imports import detect_unused_imports
from backend.analyzers.cyclomatic_complexity import get_function_complexity
from backend.analyzers.comment_density import get_comment_density


class CodeAnalyzerService:
    def __init__(self):
        self.py_linter = PythonLinter()
        self.js_linter = JSLinter()
        self.cpp_linter = CppLinter()

    def analyze(self, code: str, language: str) -> Dict[str, Any]:
        language = (language or "python").lower().strip()

        result = {
            "status": "success",
            "language": language,
            "issues": [],
            "issue_count": 0,
            "meta": {
                "cyclomatic_complexity": [],
                "comment_density": None,
                "score": 100
            }
        }

        try:
            # -------- PYTHON --------
            if language == "python":
                try:
                    tree = ast.parse(code)
                    add_parents(tree)
                except SyntaxError as e:
                    return {
                        "status": "error",
                        "language": "python",
                        "issues": [{
                            "type": "Syntax Error",
                            "line": e.lineno,
                            "detail": str(e),
                            "severity": "high"
                        }],
                        "issue_count": 1,
                        "meta": {"score": 0}
                    }

                issues = self.py_linter.lint(code)

                # ---- Unused imports ----
                for name in detect_unused_imports(code):
                    issues.append({
                        "type": "Unused Import",
                        "detail": f"'{name}' imported but never used",
                        "severity": "low"
                    })

                # ---- Cyclomatic complexity ----
                complexities = get_function_complexity(code)
                result["meta"]["cyclomatic_complexity"] = complexities

                for item in complexities:
                    cx = item["complexity"]
                    if cx > 20:
                        issues.append({
                            "type": "High Cyclomatic Complexity",
                            "detail": f"Function '{item['name']}' has complexity = {cx}",
                            "severity": "high"
                        })
                    elif cx > 10:
                        issues.append({
                            "type": "Moderate Cyclomatic Complexity",
                            "detail": f"Function '{item['name']}' has complexity = {cx}",
                            "severity": "medium"
                        })

                # ---- Comment density ----
                density = get_comment_density(code)
                result["meta"]["comment_density"] = float(density)

                if density < 0.05:  # <5%
                    issues.append({
                        "type": "Low Documentation",
                        "detail": "Very few comments found — write documentation for clarity",
                        "severity": "medium"
                    })

            # -------- JAVASCRIPT --------
            elif language in ("js", "javascript"):
                issues = self.js_linter.lint(code)

            # -------- C++ --------
            elif language in ("cpp", "c++"):
                issues = self.cpp_linter.lint(code)

            # -------- unsupported --------
            else:
                issues = [{
                    "type": "Unsupported Language",
                    "detail": f"Language '{language}' not supported",
                    "severity": "high"
                }]

            result["issues"] = issues
            result["issue_count"] = len(issues)

            # ---- scoring ----
            score = 100
            for item in issues:
                lvl = item.get("severity", "").lower()
                if lvl == "low":
                    score -= 1
                elif lvl == "medium":
                    score -= 3
                elif lvl == "high":
                    score -= 7

            result["meta"]["score"] = max(0, score)

        except Exception as e:
            result["status"] = "error"
            result["issues"] = [{
                "type": "Analyzer Failure",
                "detail": str(e),
                "trace": traceback.format_exc(),
                "severity": "high"
            }]
            result["issue_count"] = 1
            result["meta"]["score"] = 0

        return result
