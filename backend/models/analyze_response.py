from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class IssueModel(BaseModel):
    type: str
    detail: str
    severity: Optional[str] = None

class MetaModel(BaseModel):
    score: int
    complexity: Any | None = None
    comment_density: float | None = None

class AnalyzeResponse(BaseModel):
    status: str
    language: str
    issues: List[IssueModel]
    issue_count: int
    meta: MetaModel
