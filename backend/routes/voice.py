print("✅ Voice router loaded")
from fastapi import APIRouter, UploadFile, File

from services.whisper_service import speech_to_text

router = APIRouter()


@router.post("/voice")

async def voice_chat(audio: UploadFile = File(...)):

    file_path = f"temp_{audio.filename}"

    with open(file_path, "wb") as f:
        f.write(await audio.read())

    text = speech_to_text(file_path)

    return {
        "recognized_text": text
    }