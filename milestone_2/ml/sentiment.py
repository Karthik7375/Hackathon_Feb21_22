from transformers import pipeline

sentiment_model = pipeline("sentiment-analysis")

# 🔥 warm-up
sentiment_model("test")

def urgency_score(text: str) -> float:
    result = sentiment_model(text)[0]

    score = result["score"]

    if result["label"] == "NEGATIVE":
        return round(score, 3)

    return round(1 - score, 3)