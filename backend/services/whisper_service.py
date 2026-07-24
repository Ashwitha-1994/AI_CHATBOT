import whisper


model = None


def get_whisper_model():

    global model

    if model is None:

        print("Loading Whisper tiny model...")

        model = whisper.load_model(
            "tiny",
            device="cpu"
        )

        print("Whisper Loaded")

    return model



def speech_to_text(file_path):

    whisper_model = get_whisper_model()

    result = whisper_model.transcribe(
        file_path,
        fp16=False
    )

    return result["text"]