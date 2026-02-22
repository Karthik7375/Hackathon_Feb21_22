from app.queue import dequeue_ticket
import time
from app.orchestrator import is_master_incident_active
from app.agents import AgentRegistry, sample_register_agents


def process(ticket):
    print("Processing:", ticket["ticket_id"], ticket["category"], "urgency:", ticket["urgency_score"])

    # If a master incident is active, suppress individual alerts
    if ticket.get("master_incident") or is_master_incident_active():
        print("Master incident active — suppressing individual alerts for ticket", ticket["ticket_id"])
        return

    # Assign to best agent
    registry = AgentRegistry()
    sample_register_agents(registry)
    assigned = registry.assign_agent_for_category(ticket.get("category", "General"))
    if assigned:
        print(f"Assigned ticket {ticket['ticket_id']} to agent {assigned.agent_id}")
    else:
        # no suitable agent available — fallback to general pool / escalation
        print(f"No skilled agent available for {ticket['ticket_id']}. Escalating to general pool.")

    if ticket["urgency_score"] > 0.8:
        print("🚨 HIGH URGENCY ALERT for", ticket["ticket_id"])


def start_worker():
    while True:
        ticket = dequeue_ticket()
        if ticket:
            try:
                process(ticket)
            except Exception as e:
                print("Worker error:", e)
        time.sleep(1)


if __name__ == "__main__":
    start_worker()

