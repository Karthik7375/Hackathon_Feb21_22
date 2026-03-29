from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="bhadresh-savani/distilbert-base-uncased-emotion"
)

# 🔥 warm-up (loads model into memory)
classifier("test")

LABEL_MAP = {
    "Billing": ["payment", "invoice", "charge", "refund"],
    "Legal": ["legal", "gdpr", "compliance", "tos"],
    "Technical": ["error", "bug", "crash", "api", "login"]
}

def classify_ticket(text: str):
    text = text.lower()

    for category, keywords in LABEL_MAP.items():
        if any(word in text for word in keywords):
            return category

    return "General"