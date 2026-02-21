# Hackathon_Feb21_22 -  Ticket Classifier

Simple rule-based ticket classification module.

## Overview

`classifier.py` provides a single function:

```python
get_metadata(text: str)
```

It analyzes a ticket description and returns:

- **Category** (Billing, Legal, Technical, or General)
- **Priority** (0 = HIGH, 1 = NORMAL)
- **Detected urgency triggers** (list of matched words)

---

## How It Works

### 1. Category Detection

The classifier uses regular expressions to match keywords:

- **Billing** → billing, invoice, charge, refund, payment  
- **Legal** → legal, gdpr, tos, lawsuit, compliance  
- **Technical** → broken, error, api, bug, crash, login  
- **General** → default if no match

The first matching category is assigned.

### 2. Priority Detection

Urgent keywords:

```
emergency
critical
as soon as possible
fast
quick
broken
down
asap
```

If any urgent word is found:

```
priority = 0  # HIGH
```

Otherwise:

```
priority = 1  # NORMAL
```

Lower priority number means higher urgency.
## Requirements
- Python 3.8+
- Standard library  (`re`,`fastapi`,`uvicorn`)
---
