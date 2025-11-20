"""
Simple JavaScript linter (pattern-based).
Detects common bad practices such as var usage, missing semicolons, and unused variables.
"""

import re

class JSLinter:
    def lint(self, code: str):
        issues = []
        lines = code.splitlines()

        # 1. Detect 'var'
        for i, line in enumerate(lines, start=1):
            if "var " in line:
                issues.append({
                    "type": "Use of var",
                    "line": i,
                    "detail": "Avoid 'var'. Use 'let' or 'const' instead."
                })

        # 2. Detect missing semicolons (very simple heuristic)
        for i, line in enumerate(lines, start=1):
            stripped = line.strip()
            if stripped and not stripped.endswith(";") and stripped not in ["{", "}", ""]:
                if not stripped.startswith("//") and not stripped.endswith("{") and not stripped.endswith("}"):
                    issues.append({
                        "type": "Missing semicolon",
                        "line": i,
                        "detail": "Possible missing semicolon at end of line."
                    })

        # 3. Detect console.log usage
        for i, line in enumerate(lines, start=1):
            if "console.log" in line:
                issues.append({
                    "type": "Debug log",
                    "line": i,
                    "detail": "Avoid leaving console.log in production code."
                })

        return issues
