# 🚀 Smart Support Ticket Router — Milestone 2

An intelligent, production-style support ticket routing engine built for the **Smart-Support Hackathon Challenge**.

This service automatically classifies incoming support tickets, estimates urgency using NLP, and processes them asynchronously using a Redis-backed queue.

---

## 🎯 Milestone 2 Objectives Achieved

✅ Transformer-based NLP processing
✅ Continuous urgency scoring (S ∈ [0,1])
✅ Asynchronous broker architecture (Redis)
✅ Background worker processing
✅ Immediate API response (202 Accepted)
✅ Concurrency-safe & duplicate prevention

---

# 🧠 What This System Does

When a ticket is submitted:

1️⃣ API receives the request
2️⃣ Duplicate protection lock is applied
3️⃣ Transformer models classify & score urgency
4️⃣ Ticket is pushed into Redis queue
5️⃣ API instantly returns **202 Accepted**
6️⃣ Worker processes the ticket in background
7️⃣ High urgency tickets trigger alerts

---

# 🏗️ Project Structure

```
milestone_2
│
├── app
│   ├── config.py
│   ├── main.py
│   ├── models.py
│   ├── queue.py
│   └── worker.py
│
├── ml
│   ├── classifier.py
│   ├── embeddings.py
│   └── sentiment.py
│
└── requirements.txt
```

---

# ⚙️ How the System Works (Execution Flow)

## 🔄 Step-by-Step Flow

```
Client Request
      ↓
FastAPI (main.py)
      ↓
Duplicate Lock (queue.py)
      ↓
ML Processing
   ├── classifier.py
   └── sentiment.py
      ↓
Redis Queue (queue.py)
      ↓
Background Worker (worker.py)
      ↓
Processing & Alerts
```

---

# 📄 File-by-File Explanation

---

## 🟦 app/config.py

### Purpose:

Central configuration for Redis & queue behavior.

### Key Settings:

* Redis connection URL
* Queue name
* Lock expiry time

### Why it exists:

Keeps environment settings separate from logic.

---

## 🟦 app/main.py

### 🚀 Entry point of the API

### What it does:

✔ creates FastAPI app
✔ receives ticket requests
✔ prevents duplicate submissions
✔ calls ML models
✔ queues ticket for async processing
✔ returns **202 Accepted immediately**

### Endpoint:

```
POST /tickets
```

### Flow inside:

1. Validate request data
2. Acquire duplicate lock
3. Classifies ticket category
4. Computes urgency score
5. Pushes ticket to Redis queue
6. Returns response instantly

---

## 🟦 app/models.py

### Purpose:

Defines data structures & validation.

### Components:

#### TicketRequest (Pydantic Model)

Validates incoming JSON request.

Required fields:

* ticket_id
* description

#### InternalTicket (Dataclass)

Defines structure for queue processing.

Includes:

* priority
* timestamp
* category
* description

---

## 🟦 app/queue.py

### Purpose:

Handles queue operations & concurrency safety.

### Responsibilities:

✔ Connect to Redis
✔ Prevent duplicate ticket processing
✔ Push tickets into queue
✔ Retrieve tickets for workers

### Important Functions:

**acquire_lock()**

* prevents duplicate processing
* ensures atomic request handling

**enqueue_ticket()**

* pushes ticket into Redis queue

**dequeue_ticket()**

* blocking pop for worker processing

---

## 🟦 app/worker.py

### Purpose:

Background processor for queued tickets.

### What it does:

✔ continuously listens for tickets
✔ processes tickets asynchronously
✔ triggers alert for high urgency tickets

### Why needed?

Separates heavy processing from API for speed & scalability.

---

# 🧠 Machine Learning Components

---

## 🟩 ml/classifier.py

### Purpose:

Categorizes tickets into:

* Billing
* Legal
* Technical
* General

### How it works:

✔ Transformer pipeline initialized
✔ Model warmed up at startup
✔ Keyword-assisted classification logic

### Why warm-up?

Preloads model → prevents slow first request.

---

## 🟩 ml/sentiment.py

### Purpose:

Generates urgency score:

```
S ∈ [0,1]
```

### How it works:

✔ Transformer sentiment model
✔ Negative sentiment → higher urgency
✔ Continuous urgency score output

---

## 🟩 ml/embeddings.py

### Purpose:

Converts text into semantic vectors.

### Enables:

✔ semantic similarity detection
✔ duplicate ticket detection
✔ clustering similar issues

(Used in later milestones)

---

# ⚡ Order of Execution (What Runs First)

## When server starts:

1️⃣ classifier model loads & warms up
2️⃣ sentiment model loads & warms up
3️⃣ FastAPI app starts

---

## When a ticket arrives:

1️⃣ API receives request
2️⃣ lock prevents duplicates
3️⃣ ML processing runs
4️⃣ ticket queued in Redis
5️⃣ API responds immediately

---

## Worker lifecycle:

1️⃣ waits for queue messages
2️⃣ pulls ticket
3️⃣ processes ticket
4️⃣ triggers alert if urgent

---

# 🚀 Installation & Setup

## 1️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

## 2️⃣ Start Redis

### Using Docker:

```
docker run -p 6379:6379 redis
```

---

## 3️⃣ Start API

```
uvicorn app.main:app --reload
```

---

## 4️⃣ Start Worker (new terminal)

```
python -m app.worker
```

---

# 🧪 Test the API

### Example Request

```
POST http://127.0.0.1:8000/tickets
```

### JSON Body

```
{
  "ticket_id": "101",
  "description": "API login error ASAP"
}
```

### Response

```
{
  "status": "accepted",
  "urgency_score": 0.92
}
```

---

# ⚡ Concurrency & Reliability Features

✔ Redis-backed async queue
✔ atomic locking prevents duplicates
✔ background processing
✔ immediate response for high throughput

---

# 🏁 Summary

This system transforms raw support tickets into structured, prioritized tasks using:

* Transformer-based NLP
* Async queue architecture
* Concurrency-safe processing
* Real-time urgency detection

It is designed for **scalability, reliability, and real-world deployment readiness**.

---

# 👨‍💻 Built For

Smart-Support Hackathon Challenge — Milestone 2
