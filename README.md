# 🧠 Health & Wellness Planner

An AI-powered full-stack health assistant that lets users chat with expert agents to get personalized advice on nutrition, injuries, wellness planning, and more.

---

## 🚀 Tech Stack

- ⚙️ **Backend**: FastAPI + OpenAI Agents SDK
- 🌐 **Frontend**: Next.js 14 + Tailwind CSS
- 🤖 Agents: Wellness Planner, Nutrition Expert, Injury Support, Escalation Trainer

---

## 🧩 Features

- 💬 Chat-like UI with real-time typing stream
- 🔀 Expert switching via dropdown
- 🎯 Agent memory and context retention
- 📥 POST `/chat` API powered by FastAPI

---

## 📂 Folder Structure
/backend
├── app.py
├── agents_utils.py
└── my_agents/
├── planner_agent.py
├── nutrition_expert_agent.py
├── injury_support_agent.py
└── escalation_agent.py

/frontend
├── app/
└── page.tsx
├── styles/
└── tsconfig.json

yaml
Copy
Edit

---

## 🧪 Local Setup

### 1. Backend (FastAPI)

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
2. Frontend (Next.js)
bash
Copy
Edit
cd frontend
npm install
npm run dev
🧠 Sample Usage
Select an expert: Nutrition, Planner, etc.

Type your question (e.g., "Suggest a high-protein diet")

The assistant will respond and ask, “Anything else I can help you with?”

Ask more questions!

