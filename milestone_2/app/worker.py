from app.queue import dequeue_ticket
import time

def process(ticket):
    print("Processing:", ticket)

    if ticket["urgency_score"] > 0.8:
        print("🚨 HIGH URGENCY ALERT")

def start_worker():
    while True:
        ticket = dequeue_ticket()
        if ticket:
            process(ticket)
        time.sleep(1)

if __name__ == "__main__":
    start_worker()