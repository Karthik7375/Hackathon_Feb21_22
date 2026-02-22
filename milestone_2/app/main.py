from fastapi import FastAPI, status
from datetime import datetime
import time
from app.models import TicketRequest
from app.queue import enqueue_ticket, acquire_lock
from app.ml.classifier import classify_ticket
from app.ml.sentiment import urgency_score
from app.orchestrator import check_create_master_incident, fallback_classify

app = FastAPI()


@app.post("/tickets", status_code=status.HTTP_202_ACCEPTED)
async def create_ticket(ticket: TicketRequest):

    if not acquire_lock(ticket.ticket_id):
        return {"message": "Duplicate ticket ignored"}

    # Circuit-breaker: time the classifier and fall back if it exceeds 500ms
    start = time.perf_counter()
    try:
        category = classify_ticket(ticket.description)
    except Exception:
        category = fallback_classify(ticket.description)
    elapsed = time.perf_counter() - start
    if elapsed > 0.5:
        # transformer too slow — fallback to lightweight classifier
        category = fallback_classify(ticket.description)

    score = urgency_score(ticket.description)

    # Record embeddings & detect potential master incident. This may create a Master Incident
    master_created = check_create_master_incident(ticket.description, ticket.ticket_id)

    internal_ticket = {
        "ticket_id": ticket.ticket_id,
        "description": ticket.description,
        "category": category,
        "urgency_score": score,
        "timestamp": datetime.utcnow().isoformat(),
        "master_incident": bool(master_created)
    }

    enqueue_ticket(internal_ticket)

    resp = {
        "status": "accepted",
        "urgency_score": score
    }
    if master_created:
        resp["master_incident"] = True

    return resp

