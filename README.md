# Hackathon_Feb21_22


## Members In Team
### 22PT36 - V Sreenivasan
### 22PC13 - Hamanth M
### 22PC18 - Mahadev Manohar
### 22PC12 - G Karthik


## Milestones

### Milestone 1
`
Implemented a static weight classifier that prioritises the tickets based on the description of the ticket 
We get the description from which category, triggers for priority and if the ticket is priority or not

Deatils and code are available in **milestone-1** branch

### Milestone 2
`
The **Smart Support Ticket Router Milestone 2** is a FastAPI service that classifies support tickets, calculates urgency using transformer-based NLP, and processes them asynchronously through a Redis queue. When a ticket is submitted, the API validates input, prevents duplicates with an atomic lock, categorizes the issue, computes an urgency score (0–1) from sentiment, and immediately returns **202 Accepted** while placing the ticket in the queue. A background worker then processes queued tickets and triggers alerts for high-urgency cases, ensuring fast response and scalability. The system is modular, with configuration for Redis settings, models for validation and structure, queue utilities for locking and messaging, and a worker for async processing. ML components include a warmed-up transformer classifier, a sentiment model for urgency scoring, and embeddings support for future semantic matching and duplicate detection. Models preload at startup to avoid latency, and the architecture ensures concurrency safety and reliable high-throughput handling.

### Milestone 3

Autonomous Orchestrator (short description)
Adds an autonomous orchestration layer that makes the router resilient and agent-aware.
Key features
i) Semantic deduplication: ticket text → sentence embeddings; cosine similarity groups similar tickets and detects “ticket storms”.
ii) Master-incident detection: when many semantically-similar tickets appear in a short window the system suppresses duplicate alerts and creates a single incident marker.
iii) Circuit breaker & fallback: measures transformer latency and falls back to a lightweight regex classifier (Milestone‑1 style) if model inference is slow or fails.
iv) Skill-based routing: simple AgentRegistry that assigns tickets to agents by skill vector and capacity, with escalation if no skilled agent is available.
v) Compatible architecture: uses the existing FastAPI + Redis queue + background worker flow; API returns 202 immediately while workers process routing/alerts.
