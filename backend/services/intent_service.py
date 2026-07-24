from transformers import pipeline


classifier = None


def get_intent_model():

    global classifier

    if classifier is None:

        print("Loading Intent Model...")

        classifier = pipeline(
            "zero-shot-classification",
            model="typeform/distilbert-base-uncased-mnli",
            device=-1
        )

        print("Intent Model Loaded")

    return classifier



INTENTS = [
    "Greeting",
    "General Knowledge",
    "Personal Memory",
    "Coding",
    "Interview",
    "Goodbye",
    "Help"
]


def detect_intent(message):

    print("Running intent detection...")
    print("Message:", message)

    model = get_intent_model()

    result = model(
        message,
        candidate_labels=INTENTS
    )

    print("Intent result:")
    print(result)


    return {

        "intent": result["labels"][0],

        "score": round(
            result["scores"][0],
            4
        )

    }