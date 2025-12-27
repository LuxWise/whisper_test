from typing import Optional
from pydantic import BaseModel, Field

class TranscribeRequest(BaseModel):
    language: str = "es",
    task: str = "transcribe",


class TranscribeResponse(BaseModel):
    transcription: str
    language: Optional[str] = None
    duration_seconds: Optional[float] = None

