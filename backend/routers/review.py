from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.code_analyzer import CodeAnalyzerService
from backend.services.review_service import ReviewService

router = APIRouter(tags=["Code Review"])

analyzer = CodeAnalyzerService()
reviewer = ReviewService()

# ---------------------- Request Model ----------------------
class ReviewRequest(BaseModel):
    code: str
    language: str   # python, javascript, cpp

# ---------------------- Route Handler ----------------------
@router.post("/")
async def review_code(req: ReviewRequest):

    code = req.code.strip()
    language = req.language.lower().strip()

    # Validate inputs
    if not code:
        raise HTTPException(status_code=400, detail="Code cannot be empty.")

    if language not in ["python", "javascript", "cpp"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid language. Use: python, javascript, cpp"
        )

    # 1. Analyze code
    analysis_result = analyzer.analyze(code, language)

    # 2. Build review on top of analysis
    review_result = reviewer.build_review(analysis_result)

    # 3. Combine into final response
    return {
        "status": "success",
        "language": language,
        "issues": analysis_result.get("issues", []),
        "analysis_score": analysis_result.get("score", 0),
        "review_score": review_result.get("score", 0),
        "summary": review_result.get("summary", ""),
        "feedback": review_result.get("feedback", [])
    }
