import re


def get_metadata(text : str):
    text = text.lower()

    # 1. Category Logic
    categories = {
        "Billing": r"billing|invoice|charge|refund|payment",
        "Legal": r"legal|gdpr|tos|lawsuit|compliance",
        "Technical": r"broken|error|api|bug|crash|login"
    }

    assigned_cat = "General"
    for cat,pattern in categories.items():
        if re.search(pattern, text):
            assigned_cat = cat
            break

    urgent_words = ["emergency","critical","as soon as possible","fast","quick","broken","down","asap"]
    found_triggers = [word for word in urgent_words if word in text]

    #decides the priority if it is not urgent or urgent
    priority = 0 if found_triggers else 1

    return assigned_cat, priority, found_triggers