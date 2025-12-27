from urllib import request
from fastapi import APIRouter, UploadFile, File, Form

from app.schema.transcribe import TranscribeResponse
from app.services.transcribe_service import transcribe_audio as transcribe_service

router = APIRouter()


@router.post("/", response_model=TranscribeResponse)
async def transcribe_audio_endpoint(
    file: UploadFile = File(...),
    language: str = Form("es"),
    task: str = Form("transcribe"),
):
    return await transcribe_service(file=file, language=language, task=task)