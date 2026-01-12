from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class GenerateReportResponse(BaseModel):
    report_id: str
    transcript: str
    notes_markdown: str
    metadata: Optional[Dict[str, Any]] = None

class GenerateReportStatus(BaseModel):
    status: str
    detail: Optional[str] = None