from transformers import pipeline


print("Loading Sentiment Model...")

sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)


print("Sentiment Model Loaded")


def analyze_sentiment(text):

    result = sentiment_model(text)[0]

    return {
        "label": result["label"],
        "score": round(result["score"],4)
    }