"""
Calculates comment density of a given source code.

Return:
 - float between 0 and 1 (ratio of comment lines / total lines)
"""

import re


def get_comment_density(code: str) -> float:
    """
    Calculates how much of the code contains comments.
    Works for Python, JS, and C++ style // /* */ comments as well.
    """

    if not code.strip():
        return 0.0

    lines = code.split("\n")
    total_lines = 0
    comment_lines = 0
    in_block_comment = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue  # ignore blank lines

        total_lines += 1

        # Start block comment (/* ... */)
        if "/*" in stripped and "*/" not in stripped:
            in_block_comment = True
            comment_lines += 1
            continue

        # End block comment
        if "*/" in stripped and in_block_comment:
            in_block_comment = False
            comment_lines += 1
            continue

        # Inside block comment region
        if in_block_comment:
            comment_lines += 1
            continue

        # Single-line comments (# or //)
        if stripped.startswith("#") or stripped.startswith("//"):
            comment_lines += 1
            continue

        # Python docstring (only count full-line)
        if re.match(r'^(\'\'\'|""")', stripped) and re.match(r'(\'\'\'|""")$', stripped):
            comment_lines += 1
            continue

    if total_lines == 0:
        return 0.0

    return comment_lines / total_lines
