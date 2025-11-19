from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.code_analyzer import CodeAnalyzer

router = APIRouter()

class CodeInput(BaseModel):
    code: str

@router.post("/analyze")
def analyze_code(payload: CodeInput):
    analyzer = CodeAnalyzer()
    result = analyzer.analyze(payload.code)

    return {
        "status": "success",
        "analysis": result
    }
