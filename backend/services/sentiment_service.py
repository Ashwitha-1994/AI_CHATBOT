from transformers import pipeline

print("Loading Sentiment Model...")

classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

print("Sentiment Model Loaded")


def analyze_sentiment(text):

    result = classifier(text)[0]

    return {
        "label": result["label"],
        "score": round(result["score"], 4)
    }