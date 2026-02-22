from pydantic import BaseModel
from dataclasses import dataclass, field
from datetime import datetime

class TicketRequest(BaseModel):
    ticket_id: str
    description: str

@dataclass(order=True)
class InternalTicket:
    priority: float
    timestamp: datetime = field(compare=True)
    ticket_id: str = field(compare=True)
    category: str = field(compare=True)
    description: str = field(compare=True)

