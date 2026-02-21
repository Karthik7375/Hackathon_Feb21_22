import redis
import json
from datetime import datetime
from app.config import REDIS_URL, QUEUE_NAME, LOCK_EXPIRY

r = redis.Redis.from_url(REDIS_URL, decode_responses=True, socket_timeout=5)

def acquire_lock(ticket_id):
    return r.set(f"lock:{ticket_id}", "1", nx=True, ex=LOCK_EXPIRY)

def enqueue_ticket(ticket):
    r.lpush(QUEUE_NAME, json.dumps(ticket))

def dequeue_ticket():
    data = r.brpop(QUEUE_NAME, timeout=5)
    if data:
        return json.loads(data[1])