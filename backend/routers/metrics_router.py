from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.code_analyzer import CodeAnalyzerService   # ✔ Correct class import

router = APIRouter(prefix="/metrics", tags=["metrics"])

class CodeRequest(BaseModel):
    code: str
    language: str | None = "python"      # ✔ allow user to choose language

@router.post("/")
def analyze_metrics(request: CodeRequest):
    service = CodeAnalyzerService()      # ✔ no argument in constructor
    return service.analyze(request.code, request.language)   # ✔ call with code + language
