import os
import uuid
import subprocess
from pathlib import Path
from typing import Optional

from fastapi import HTTPException, UploadFile
from faster_whisper import WhisperModel

from app.schema.transcribe import TranscribeResponse

TMP_DIR = Path("./tmp")
TMP_DIR.mkdir(exist_ok=True)

MODEL_SIZE = os.getenv("WHISPER_MODEL", "small")
DEVICE = os.getenv("WHISPER_DEVICE", "cpu")
COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8")

model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)


async def convert_to_wav_16k_mono(input_path: Path, output_path: Path) -> None:
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-ac",
        "1",
        "-ar",
        "16000",
        "-c:a",
        "pcm_s16le",
        str(output_path),
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise HTTPException(
            status_code=400,
            detail=f"ffmpeg conversion failed: {result.stderr.decode(errors='ignore')[-500:]}",
        )


async def transcribe_audio(
    file: UploadFile,
    language: str = "es",
    task: str = "transcribe",
) -> TranscribeResponse:
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")

    ext = Path(file.filename).suffix.lower() or ".bin"
    raw_path = TMP_DIR / f"{uuid.uuid4().hex}{ext}"
    wav_path = TMP_DIR / f"{uuid.uuid4().hex}.wav"

    try:
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Empty file")
        raw_path.write_bytes(content)

        await convert_to_wav_16k_mono(raw_path, wav_path)

        segments, info = model.transcribe(
            str(wav_path),
            language=language,
            task=task,
            vad_filter=True,
            beam_size=5,
        )

        full_text_parts = [segment.text for segment in segments]

        return TranscribeResponse(
            transcription="".join(full_text_parts).strip(),
            language=getattr(info, "language", None),
            duration_seconds=getattr(info, "duration", None),
        )

    finally:
        try:
            if raw_path.exists():
                raw_path.unlink()
            if wav_path.exists():
                wav_path.unlink()
        except Exception:
            pass