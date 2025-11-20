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
            "meta": {}
        }

        try:
            # ---------------- Python ----------------
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
                            "detail": str(e)
                        }],
                        "issue_count": 1,
                        "meta": {"score": 0}
                    }

                issues = self.py_linter.lint(code)

            # ---------------- JavaScript ----------------
            elif language in ("js", "javascript"):
                issues = self.js_linter.lint(code)

            # ---------------- C++ ----------------
            elif language in ("cpp", "c++"):
                issues = self.cpp_linter.lint(code)

            else:
                issues = [{
                    "type": "Unsupported Language",
                    "detail": f"Language '{language}' is not supported yet."
                }]

            # Save issues
            result["issues"] = issues
            result["issue_count"] = len(issues)

            # Score calculation
            weight = 0
            for item in issues:
                t = item.get("type", "").lower()
                if "syntax" in t or "error" in t:
                    weight += 10
                elif "high" in t or "infinite" in t or "raw pointer" in t:
                    weight += 7
                elif "missing" in t or "deprecated" in t or "unused" in t:
                    weight += 3
                else:
                    weight += 1

            score = max(0, 100 - weight)
            result["meta"]["score"] = score

        except Exception as e:
            result["status"] = "error"
            result["issues"] = [{
                "type": "Analyzer Failure",
                "detail": str(e),
                "trace": traceback.format_exc()
            }]
            result["issue_count"] = 1
            result["meta"]["score"] = 0

        return result
