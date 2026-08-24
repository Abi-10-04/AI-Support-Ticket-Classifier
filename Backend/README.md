[4:03 PM, 7/21/2026] 🌟: # AI Support Ticket Classifier

An AI-powered web application that classifies customer support tickets,
explains its reasoning, analyzes sentiment, and drafts a suggested reply.

## Tech Stack
- Backend: Django + Django REST Framework
- Database: SQLite
- Frontend: React (Vite)
- AI: OpenRouter API

## Features
- Ticket classification (Category, Priority, Suggested Owner)
- Confidence score
- Reason for classification
- Sentiment analysis
- AI-generated reply suggestion
- Ticket history with search
- Fallback rule-based classifier if the AI API is unavailable,
  ensuring the app stays functional even during API downtime or rate limits

## Setup Instructions

### Backend
From a terminal in the repository root:

```powershell
cd Backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Edit Backend/.env and add your OpenRouter API key.
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

The backend runs at http://127.0.0.1:8000.

### Frontend
Open a second terminal in the repository root:

```powershell
cd Frontend
npm install
npm run dev
```

Open the URL printed by Vite, normally http://localhost:5173.

## API Endpoints
- POST /api/classify/ — submit a ticket for classification
- GET /api/history/ — retrieve ticket history (supports ?search= query param)

## Prompt Used for AI Classification
[4:06 PM, 7/21/2026] 🌟: Classify the support ticket below and return ONLY valid JSON with this exact schema:
{"category": "", "priority": "", "owner": "", "confidence": 0, "reason": "", "sentiment": "", "ai_reply": ""}
Rules:
category: one of Support, Billing, Technical, Account, Product, Sales, Other
priority: one of Low, Medium, High, Critical
owner: one of Support, Billing, Engineering, Product, Sales, Operations
confidence: integer from 0 to 100
reason: concise explanation in one sentence
sentiment: one of Positive, Neutral, Negative
ai_reply: a helpful customer-facing response