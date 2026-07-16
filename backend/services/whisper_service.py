import whisper

print("Loading Whisper model...")

model = whisper.load_model("base")

print("Whisper Loaded")


def speech_to_text(audio_path):
    result = model.transcribe(audio_path)
    return result["text"]