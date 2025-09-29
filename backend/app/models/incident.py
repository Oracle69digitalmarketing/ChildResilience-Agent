from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4

class Incident(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    reporter_name: str
    location: str
    description: str
    language: str
    file_url: Optional[str] = None
    classification: dict
    child_impact_tags: List[str] = []
    severity_score: float = 0.0
    response_text: Optional[str] = ""
    equity_priority_score: float = 0.0  # optional UNICEF equity layer
