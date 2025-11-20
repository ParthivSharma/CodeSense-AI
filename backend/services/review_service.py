"""
Comprehensive Code Review Service.

Provides a detailed review for Python, C++, and JavaScript code:
- Quality score
- Readability score
- Performance suggestions
- Detected issues
- Summary and feedback
"""

from typing import Dict, List
import re

class ReviewService:
    def __init__(self):
        pass

    # ---------------------- Main Review Method ----------------------
    def build_review(self, analysis: Dict) -> Dict:
        """
        Takes analysis output from CodeAnalyzerService and returns a detailed review.
        """
        issues = analysis.get("issues", [])
        language = analysis.get("language", "unknown")
        
        readability = self.readability_score(analysis)
        performance = self.performance_suggestions(analysis, language)
        quality_score = self.compute_quality_score(issues, readability)

        feedback = self.generate_feedback(issues, performance)
        summary = self.generate_summary(quality_score, len(issues))

        return {
            "score": quality_score,
            "readability_score": readability,
            "performance": performance,
            "issues": issues,
            "feedback": feedback,
            "summary": summary
        }

    # ---------------------- Compute Quality Score ----------------------
    def compute_quality_score(self, issues: List[Dict], readability: int) -> int:
        """
        Base 100 minus weighted issues and readability penalties.
        """
        weight = 0
        for it in issues:
            t = it.get("type", "").lower()
            if "error" in t or "syntax" in t:
                weight += 10
            elif "high" in t or "complex" in t or "raw pointer" in t:
                weight += 7
            elif "missing" in t or "unused" in t or "deprecated" in t:
                weight += 3
            else:
                weight += 1
        score = max(0, 100 - weight - (10 - readability))
        return score

    # ---------------------- Readability ----------------------
    def readability_score(self, analysis: Dict) -> int:
        """
        Returns 1–10 readability score based on lines and complexity.
        """
        code = analysis.get("meta", {}).get("code", "")
        lines = code.split("\n") if code else []
        avg_len = sum(len(line) for line in lines) / max(1, len(lines))

        score = 10
        if avg_len > 90:
            score -= 3
        if any("\t" in line and "    " in line for line in lines):
            score -= 2
        if len(lines) > 300:
            score -= 2
        return max(1, score)

    # ---------------------- Performance Suggestions ----------------------
    def performance_suggestions(self, analysis: Dict, language: str) -> List[str]:
        code = analysis.get("meta", {}).get("code", "")
        suggestions = []

        if language == "python":
            if "for" in code and "range" in code:
                suggestions.append("Use list comprehensions or generators instead of loops for better performance.")
            if "print(" in code:
                suggestions.append("Remove print/debug statements in production.")
        elif language in ("cpp", "c++"):
            if "new " in code:
                suggestions.append("Avoid unnecessary object creation inside loops.")
            if "*" in code:
                suggestions.append("Prefer smart pointers over raw pointers for memory safety.")
        elif language in ("js", "javascript"):
            if "==" in code:
                suggestions.append("Use === instead of == for strict equality.")
            if "var " in code:
                suggestions.append("Use let or const instead of var.")
        return suggestions

    # ---------------------- Feedback Generation ----------------------
    def generate_feedback(self, issues: List[Dict], performance: List[str]) -> List[str]:
        feedback = []

        for issue in issues:
            feedback.append(f"{issue.get('type')}: {issue.get('detail')}")

        feedback.extend(performance)
        return feedback

    # ---------------------- Summary ----------------------
    def generate_summary(self, score: int, issue_count: int) -> str:
        if score > 85:
            return "Excellent code quality. Minor improvements possible."
        elif score > 70:
            return "Good code quality but has room for improvement."
        elif score > 50:
            return "Average code quality. Needs refactoring."
        else:
            return "Poor code quality. Major improvements required."
