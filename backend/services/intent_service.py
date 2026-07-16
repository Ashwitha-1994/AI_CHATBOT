from transformers import pipeline

print("Loading Intent Model...")

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
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

    result = classifier(

        message,

        candidate_labels=INTENTS

    )

    return {

        "intent": result["labels"][0],

        "score": round(result["scores"][0], 4)

    }