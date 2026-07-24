from transformers import pipeline


classifier = None


def get_sentiment_model():

    global classifier

    if classifier is None:

        print("Loading Sentiment Model...")

        classifier = pipeline(
            "sentiment-analysis"
        )

        print("Sentiment Model Loaded")

    return classifier



def analyze_sentiment(text):

    model = get_sentiment_model()

    result = model(text)[0]

    return {
        "label": result["label"],
        "score": round(result["score"],4)
    }