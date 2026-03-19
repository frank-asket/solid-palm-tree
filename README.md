# DjÊ Backend 🚀

DjÊ is a WhatsApp-first AI financial assistant that helps people track money using natural language, understand spending behavior, and get practical insights they can act on.

## ✨ What DjÊ Does

- Tracks income and expenses from plain text messages (for example: `I spent 50 on food`)
- Stores transactions per user (phone number identity)
- Generates simple financial summaries and health signals
- Replies directly in WhatsApp with a concise, user-friendly analysis

## 🧱 Tech Stack

- **FastAPI**: web framework and webhook endpoints
- **PostgreSQL + SQLAlchemy**: persistent storage and data modeling
- **OpenAI API**: structured extraction of financial intent from text
- **WhatsApp Cloud API**: user communication channel
- **Uvicorn**: ASGI server for local/dev deployment

## 🗂️ Project Structure

```text
app/
├── main.py                     # FastAPI app entry point
├── core/
│   ├── config.py               # Environment loading and settings
│   └── deps.py                 # Dependency injection (DB session)
├── models/
│   ├── database.py             # SQLAlchemy engine/session/base
│   ├── user.py                 # User model (phone identity)
│   └── transaction.py          # Transaction model (income/expense)
├── routes/
│   └── whatsapp.py             # WhatsApp webhook (GET verify, POST events)
├── services/
│   ├── ai_service.py           # NLP extraction logic (OpenAI + fallback)
│   ├── transaction_service.py  # User/transaction data operations
│   └── insight_service.py      # Financial metrics and health messaging
└── utils/
    └── whatsapp.py             # WhatsApp API sender utility

init_db.py                      # DB table initialization script
requirements.txt                # Python dependencies
README.md
```

## ⚙️ Prerequisites

- Python 3.11+ recommended
- PostgreSQL running locally or hosted
- Meta Developer app with WhatsApp Cloud API enabled
- OpenAI API key

## 🚀 Quick Start

### 1) Clone and enter project

```bash
git clone <your-repo-url>
cd solid-palm-tree
```

### 2) Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate       # Windows PowerShell
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Configure environment

Create `.env` in project root (or copy from `.env.example`):

```env
OPENAI_API_KEY=your_openai_key
WHATSAPP_TOKEN=your_whatsapp_token
PHONE_NUMBER_ID=your_phone_number_id
VERIFY_TOKEN=your_verify_token
DATABASE_URL=postgresql://user:password@localhost/dje
```

### 5) Initialize database

```sql
CREATE DATABASE dje;
```

```bash
python3 init_db.py
```

### 6) Run the API

```bash
uvicorn app.main:app --reload
```

Server:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/health`

## 🔗 WhatsApp Webhook Setup

To receive WhatsApp events locally, expose your server (for example with ngrok):

```bash
ngrok http 8000
```

Use the HTTPS URL for your webhook in Meta:

- **Callback URL**: `https://<ngrok-url>/webhook`
- **Verify token**: same value as `VERIFY_TOKEN` in `.env`

Subscribe to event fields such as:

- `messages`
- `message_status`

## 🔄 End-to-End Flow

1. User sends a WhatsApp text message.
2. Meta forwards the webhook payload to `POST /webhook`.
3. Backend extracts transaction intent (`income`/`expense`, amount, category, note).
4. Transaction is saved to PostgreSQL under the correct user.
5. Insight service computes totals, savings, and health message.
6. A reply is sent back to the user via WhatsApp Cloud API.

## 🧠 AI Extraction Behavior

DjÊ uses deterministic extraction with validation:

- Model temperature set to `0`
- JSON-first extraction contract
- Runtime validation of type and amount
- Regex fallback when model output/API is unavailable

Example:

**Input**

```text
I spent 50 on food
```

**Structured output**

```json
{
  "type": "expense",
  "amount": 50,
  "category": "food",
  "note": null
}
```

## 📊 Insights Engine

Current computed signals include:

- Total income
- Total expenses
- Savings (`income - expenses`)
- Savings rate (%)
- Expense category breakdown
- Health message (negative / break-even / positive saving)

Typical response summary:

```text
📊 Summary
Income: 1200.0
Expenses: 900.0
Savings: 300.0 (25.0%)
✅ You're saving well. Keep it up!
```

## 🧪 Testing and Validation Tips

- Run import sanity checks with your virtual environment Python
- Verify health endpoint (`GET /health`)
- Send sample webhook payloads to `POST /webhook`
- Confirm records are inserted into `users` and `transactions`
- Validate WhatsApp response delivery in Meta logs

## 🔐 Security and Reliability Notes

- Phone number (`wa_id`) is the user identity key
- Secrets are loaded via environment variables, not hardcoded
- Non-text messages are safely handled
- Missing sender IDs are guarded to avoid runtime crashes
- Webhook verification token must match exactly in Meta and `.env`

## ⚠️ Current MVP Limitations

- Category understanding is basic
- Single-currency assumptions
- No budgets/goals engine yet
- No advanced forecasting/investment models yet
- Basic operational logging (can be expanded)

## 🗺️ Roadmap

- Richer trend analytics and monthly comparisons
- Budget recommendations and alerts
- Voice-note transaction parsing
- Multi-language and locale-aware formatting
- Better observability (structured logs, metrics, tracing)
- Automated tests for webhook and services

## 👩‍💻 Development Principles

- Keep business logic in `services`, not route handlers
- Keep extraction prompts strict and parseable
- Validate all AI outputs before persistence
- Prefer safe fallbacks over hard failures
- Optimize for trust and clarity in user-facing messages

## 📬 Contact

- **Project**: DjÊ
- **Organization**: Klingbo Intelligence

## 💡 Vision

DjÊ aims to be more than a chatbot: a lightweight financial intelligence layer in a channel people already use every day.

Start simple. Ship quickly. Learn from users. Scale with confidence.
