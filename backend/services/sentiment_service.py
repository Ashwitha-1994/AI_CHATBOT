from transformers import pipeline


sentiment_model = None


def get_sentiment_model():

    global sentiment_model

    if sentiment_model is None:

        print("Loading Sentiment Model...")

        sentiment_model = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=-1
        )

        print("Sentiment Model Loaded")

    return sentiment_model



def analyze_sentiment(text):

    model = get_sentiment_model()

    result = model(text)[0]

    return {
        "label": result["label"],
        "score": round(result["score"],4)
    }