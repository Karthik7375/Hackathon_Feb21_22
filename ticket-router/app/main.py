from fastapi import FastAPI
import heapq
from datetime import datetime
import uvicorn
#Our files
from .models import TicketRequest,InternalTicket
from .logic.classifier import get_metadata


app = FastAPI(title="Intelligent MVR")
ticketqueue = []


@app.post("/tickets/triage")
async def triage_ticket(payload : TicketRequest):
    #We get the ticket's category, priority(whether it is urgent or not) and finally the words which make it a priority
    category, priority, triggers = get_metadata(payload.description)


    ticket = InternalTicket(
        priority=priority,
        timestamp=datetime.now(),
        ticket_id=payload.ticket_id,
        category=category,
        description=payload.description,
    )

    #push the ticket into a priority queue which is a heap structure
    heapq.heappush(ticketqueue,ticket)

    return {
        "ticket_id": ticket.ticket_id,
        "priority_score": priority,
        "triggers_detected": triggers
    }

@app.post("/tickets/inspect")
async def inspect_queue():
    sorted_view = sorted(ticketqueue)
    return [
        {   
            "position" : i + 1,
            "id" : t.ticket_id,
            "urgency": "HIGH" if t.priority == 0 else "NORMAL",
            "category": t.category,
            "wait_time_seconds": (datetime.now() - t.timestamp).seconds
        }
        for i,t in enumerate(sorted_view)
    ]