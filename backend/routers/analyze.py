from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.code_analyzer import CodeAnalyzerService
from backend.models.analyze_response import AnalyzeResponse

router = APIRouter(tags=["Code Analyzer"])
analyzer = CodeAnalyzerService()

class AnalyzeRequest(BaseModel):
    code: str
    language: str

@router.post("/", response_model=AnalyzeResponse)
async def analyze_code(req: AnalyzeRequest):
    code = req.code.strip()
    language = req.language.lower().strip()

    if not code:
        raise HTTPException(status_code=400, detail="Code cannot be empty.")
    if language not in ["python", "javascript", "cpp", "c++"]:
        raise HTTPException(status_code=400, detail="Invalid language. Use: python, javascript, cpp, c++")

    return analyzer.analyze(code, language)
