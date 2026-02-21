from fastapi import FastAPI, status
from datetime import datetime
from app.models import TicketRequest
from app.queue import enqueue_ticket, acquire_lock
from app.ml.classifier import classify_ticket
from app.ml.sentiment import urgency_score

app = FastAPI()

@app.post("/tickets", status_code=status.HTTP_202_ACCEPTED)
async def create_ticket(ticket: TicketRequest):

    if not acquire_lock(ticket.ticket_id):
        return {"message": "Duplicate ticket ignored"}

    category = classify_ticket(ticket.description)
    score = urgency_score(ticket.description)

    internal_ticket = {
        "ticket_id": ticket.ticket_id,
        "description": ticket.description,
        "category": category,
        "urgency_score": score,
        "timestamp": datetime.utcnow().isoformat()
    }

    enqueue_ticket(internal_ticket)

    return {
        "status": "accepted",
        "urgency_score": score
    }