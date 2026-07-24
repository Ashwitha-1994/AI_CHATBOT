print("✅ Voice router loaded")

import os
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.services.whisper_service import speech_to_text


router = APIRouter()


@router.post("/voice")
async def voice_chat(audio: UploadFile = File(...)):

    try:

        # Validate audio file
        if not audio.filename:
            raise HTTPException(
                status_code=400,
                detail="No audio file provided"
            )


        # Create unique temporary filename
        file_extension = os.path.splitext(audio.filename)[1]

        temp_filename = f"temp_{uuid.uuid4()}{file_extension}"


        # Save uploaded audio
        with open(temp_filename, "wb") as f:

            content = await audio.read()

            f.write(content)


        print("Audio saved:", temp_filename)


        # Convert speech to text
        text = speech_to_text(temp_filename)


        print("Transcription completed")
        print(text)


        # Delete temporary file
        if os.path.exists(temp_filename):

            os.remove(temp_filename)


        return {

            "success": True,

            "recognized_text": text

        }


    except Exception as e:

        print("VOICE ERROR:")
        print(e)


        # Remove file if error happens
        if 'temp_filename' in locals():

            if os.path.exists(temp_filename):

                os.remove(temp_filename)


        raise HTTPException(

            status_code=500,

            detail=str(e)

        )