import time
import json
from datetime import datetime, timedelta
from typing import List

import numpy as np

from app.queue import r
from app.ml.embeddings import get_embedding, cosine_similarity

# Redis keys / prefixes
EMB_LIST_KEY = "recent:embeddings"  # a Redis list of JSON blobs: {"ticket_id","ts","vec"}
MASTER_INCIDENT_KEY = "master_incident"  # set when an incident is created

WINDOW_SECONDS = 300  # 5 minutes
MASTER_THRESHOLD = 10
SIMILARITY_THRESHOLD = 0.9

def record_embedding(ticket_id: str, text: str):
    vec = get_embedding(text).tolist()
    payload = {"ticket_id": ticket_id, "ts": time.time(), "vec": vec}
    # push to left
    r.lpush(EMB_LIST_KEY, json.dumps(payload))
    # trim to reasonable length (keep last 2000)
    r.ltrim(EMB_LIST_KEY, 0, 2000)

def _load_recent_embeddings(window_seconds: int = WINDOW_SECONDS):
    items = r.lrange(EMB_LIST_KEY, 0, -1)
    cutoff = time.time() - window_seconds
    results = []
    for it in items:
        try:
            obj = json.loads(it)
            if obj.get("ts", 0) >= cutoff:
                results.append(obj)
        except Exception:
            continue
    return results

def find_similar(text: str, threshold: float = SIMILARITY_THRESHOLD, window_seconds: int = WINDOW_SECONDS) -> List[str]:
    """
    Return list of ticket_ids with cosine similarity > threshold in the time window.
    """
    vec = get_embedding(text)
    recent = _load_recent_embeddings(window_seconds)
    matches = []
    for obj in recent:
        other = np.array(obj["vec"], dtype=float)
        score = cosine_similarity(vec, other)
        if score >= threshold:
            matches.append(obj["ticket_id"])
    return matches

def check_create_master_incident(text: str, ticket_id: str) -> bool:
    """
    Record embedding and check if a master incident should be created.
    If more than MASTER_THRESHOLD similar tickets in WINDOW_SECONDS, set MASTER_INCIDENT_KEY and return True.
    """
    # record current ticket first
    record_embedding(ticket_id, text)

    similar = find_similar(text)
    if len(similar) > MASTER_THRESHOLD:
        # create a simple marker with timestamp
        r.set(MASTER_INCIDENT_KEY, json.dumps({"created_at": time.time(), "count": len(similar)}), ex=WINDOW_SECONDS)
        return True
    return False

def is_master_incident_active() -> bool:
    return r.exists(MASTER_INCIDENT_KEY) == 1


def fallback_classify(text: str) -> str:
    """
    Lightweight regex-based fallback classifier (compatible with Milestone 1).
    """
    import re
    text = text.lower()
    categories = {
        "Billing": r"billing|invoice|charge|refund|payment",
        "Legal": r"legal|gdpr|tos|lawsuit|compliance",
        "Technical": r"broken|error|api|bug|crash|login"
    }
    for cat, pattern in categories.items():
        if re.search(pattern, text):
            return cat
    return "General"

