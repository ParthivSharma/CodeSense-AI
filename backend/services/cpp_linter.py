"""
Simple C++ linter (pattern-based).
Detects common issues like 'using namespace std', raw malloc/free, header guard problems.
"""

import re
from typing import List, Dict

class CppLinter:
    def __init__(self):
        pass

    def lint(self, code: str) -> List[Dict]:
        issues = []
        lines = code.splitlines()

        # 1. using namespace std
        for i, line in enumerate(lines, start=1):
            if re.search(r'\busing\s+namespace\s+std\b', line):
                issues.append({
                    "type": "Using namespace std",
                    "line": i,
                    "detail": "Avoid 'using namespace std;' in headers or global scope."
                })

        # 2. malloc/free or new/delete mismatches
        for i, line in enumerate(lines, start=1):
            if re.search(r'\bmalloc\s*\(', line) or re.search(r'\bcalloc\s*\(', line):
                issues.append({
                    "type": "C allocation",
                    "line": i,
                    "detail": "Prefer new/delete or smart pointers (unique_ptr/shared_ptr) in modern C++."
                })
            if re.search(r'\bfree\s*\(', line):
                issues.append({
                    "type": "Free call",
                    "line": i,
                    "detail": "Ensure matching allocation/deallocation; prefer RAII."
                })

        # 3. Raw pointer usage (heuristic)
        for i, line in enumerate(lines, start=1):
            if re.search(r'\b\w+\s*\*\s*\w+', line) and not re.search(r'\b(std::unique_ptr|std::shared_ptr)\b', line):
                issues.append({
                    "type": "Raw pointer",
                    "line": i,
                    "detail": "Consider using smart pointers instead of raw pointers."
                })

        # 4. Header guard / include-guard check (heuristic)
        if len(lines) >= 10:
            first_lines = "\n".join(lines[:20])
            if '#pragma once' not in first_lines and not re.search(r'#ifndef\s+\w+\s*\n#define\s+\w+', first_lines):
                issues.append({
                    "type": "Header guard missing",
                    "detail": "Add `#pragma once` or include guards."
                })

        # 5. Long file
        if len(lines) > 2000:
            issues.append({
                "type": "Large file",
                "detail": f"File has {len(lines)} lines; consider splitting modules."
            })

        return issues
