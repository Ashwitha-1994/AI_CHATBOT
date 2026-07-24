from transformers import pipeline

print("Loading Intent Model...")

classifier = pipeline(
    "zero-shot-classification",
    model="valhalla/distilbart-mnli-12-1"
)

print("Intent Model Loaded")

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

    result = classifier(
        message,
        candidate_labels=INTENTS
    )

    print("Intent result:", result)

    return {
        "intent": result["labels"][0],
        "score": round(result["scores"][0], 4)
    }