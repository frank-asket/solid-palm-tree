:::writing{variant=“standard” id=“dje02”}

DjÊ Backend 🚀

Overview

DjÊ is a WhatsApp-based AI financial assistant designed to help users:
	•	Track income and expenses using natural language
	•	Understand their financial habits
	•	Receive simple, actionable insights
	•	Improve money management over time

This repository contains the production-ready backend powering DjÊ.

⸻

🧱 Tech Stack
	•	FastAPI – Backend framework
	•	PostgreSQL – Database
	•	OpenAI API – AI processing (data extraction & insights)
	•	WhatsApp Cloud API – User interface

⸻

📁 Project Structure

app/
│
├── main.py                # App entry point
│
├── core/
│   ├── config.py         # Environment config
│   └── deps.py           # Dependency injection (DB)
│
├── models/
│   ├── database.py       # DB connection
│   ├── user.py           # User model
│   └── transaction.py    # Transaction model
│
├── routes/
│   └── whatsapp.py       # Webhook endpoints
│
├── services/
│   ├── ai_service.py     # AI extraction logic
│   ├── transaction_service.py
│   └── insight_service.py
│
├── utils/
│   └── whatsapp.py       # WhatsApp API sender


⸻

⚙️ Setup Instructions

1. Clone the Repository

git clone <your-repo-url>
cd dje-backend


⸻

2. Create Virtual Environment

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows


⸻

3. Install Dependencies

pip install -r requirements.txt


⸻

🔐 Environment Variables

Create a .env file in the root:

OPENAI_API_KEY=your_openai_key
WHATSAPP_TOKEN=your_whatsapp_token
PHONE_NUMBER_ID=your_phone_number_id
VERIFY_TOKEN=your_verify_token
DATABASE_URL=postgresql://user:password@localhost/dje


⸻

🗄️ Database Setup

Make sure PostgreSQL is running.

Create database:

CREATE DATABASE dje;

Initialize tables:

python init_db.py


⸻

▶️ Run the Server

uvicorn app.main:app --reload

Server runs on:

http://127.0.0.1:8000


⸻

🌐 Expose Local Server (for WhatsApp)

Use ngrok:

ngrok http 8000

Copy the HTTPS URL and use it for webhook configuration.

⸻

📱 WhatsApp Integration
	1.	Create a Meta Developer App
	2.	Add WhatsApp product
	3.	Configure webhook:

https://your-ngrok-url/webhook

	4.	Set your VERIFY_TOKEN
	5.	Subscribe to:
	•	messages
	•	message_status

⸻

🔁 How It Works
	1.	User sends a message via WhatsApp
	2.	Webhook receives message
	3.	AI extracts structured financial data
	4.	Transaction is saved in database
	5.	Analytics engine computes insights
	6.	Response is sent back to user

⸻

🧠 AI System

DjÊ uses structured AI processing:
	•	Deterministic extraction (temperature = 0)
	•	JSON-only outputs
	•	Validation layer for accuracy
	•	Fallback handling for errors

Example:

Input:

"I spent 50 on food"

Output:

{
  "type": "expense",
  "amount": 50,
  "category": "food"
}


⸻

📊 Features (MVP)
	•	✅ Expense tracking
	•	✅ Income tracking
	•	✅ Basic financial insights
	•	✅ WhatsApp-based interaction

⸻

📈 Analytics Engine

DjÊ computes:
	•	Total income vs expenses
	•	Category breakdown
	•	Savings estimation
	•	Basic financial health insights

Example insight:

⚠️ You are spending more than you earn.


⸻

🔐 Security
	•	Phone number = unique user identity
	•	No cross-user data access
	•	Environment-based secrets
	•	Input validation to prevent corruption

⸻

⚠️ Known Limitations (MVP)
	•	Limited category detection
	•	No multi-currency support yet
	•	No advanced investment logic yet
	•	Basic insight engine

⸻

🚀 Roadmap
	•	Advanced analytics (trends, forecasts)
	•	Investment recommendations
	•	Voice message support
	•	Multi-language support
	•	Agent-based workflows (future upgrade)

⸻

💡 Vision

DjÊ is not just a chatbot.

It is:

A financial intelligence layer that helps people understand, control, and grow their money — starting from WhatsApp.

⸻

👨‍💻 Development Notes
	•	Keep logic in services, not routes
	•	Keep AI prompts minimal and structured
	•	Always validate AI outputs
	•	Prioritize user trust over complexity

⸻

📬 Contact

For questions or collaboration:
	•	Project: DjÊ
	•	Built under: Klingbo Intelligence

⸻

⭐ Final Note

Start small.
Ship fast.
Learn from real users.

Then scale intelligently.

⸻

:::