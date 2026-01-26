# # FAQ Chatbot with Neuro-SAN

A FastAPI-based FAQ chatbot application integrated with the Neuro-SAN agent framework. This application provides intelligent FAQ retrieval and conversation management with both React frontend and Python backend.

---

## 📋 Prerequisites

- **Python 3.10+** - [Download](https://www.python.org)
- **Node.js 18+** - [Download](https://nodejs.org)

---

## 🚀 Quick Start

### 1. Backend Setup (Python)

```powershell
# Navigate to backend
cd backend

# Install dependencies
python -m pip install -r requirements.txt --only-binary :all:

# Run the server
python -m uvicorn app.main:app --reload
```

**Backend will be available at:** `http://localhost:8000`  
**API Documentation:** `http://localhost:8000/docs`

---

### 2. Frontend Setup (React)

**In a new terminal:**

```powershell
# Navigate to frontend
cd "c:\Users\Balaji M Vanan\Downloads\faq-chatbot-neuro-san\frontend"

# Install dependencies
&"C:\Program Files\nodejs\npm.cmd" install

# Start the development server
&"C:\Program Files\nodejs\npm.cmd" start
```

**Frontend will be available at:** `http://localhost:3000`

---

## 📁 Project Structure

```
faq-chatbot-neuro-san/
├── backend/
│   ├── app/
│   │   └── main.py              # FastAPI application with agent integration
│   ├── data/
│   │   └── faq_data.py          # FAQ database (9 Q&A items)
│   ├── registries/
│   │   ├── manifest.hocon       # Agent registry
│   │   └── faq_agent.hocon      # FAQ agent configuration
│   ├── requirements.txt          # Python dependencies
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── ChatWindow.js        # Main chat component
│   │   └── index.js
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml           # Multi-container setup
```

---

## 🎯 Features

✅ **9 Pre-loaded FAQ Items** - ICICI Prulife insurance FAQs  
✅ **Smart FAQ Search** - Keyword-based matching  
✅ **Session Management** - Conversation history per session  
✅ **Mock Agent** - Works without neuro-san (for development)  
✅ **API Endpoints** - Full REST API with Swagger documentation  
✅ **Dataclass Validation** - Type-safe request/response handling  

---

## 📡 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/chat` | Send message to chatbot |
| GET | `/health` | Health check |
| GET | `/faq/all` | Get all FAQ items |
| GET | `/faq/search?keyword=...` | Search FAQ by keyword |
| GET | `/sessions/{session_id}` | Get conversation history |
| DELETE | `/sessions/{session_id}` | Clear conversation |

---

## 💬 Example Usage

**Terminal 1 - Backend:**
```powershell
cd backend
python -m uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
&"C:\Program Files\nodejs\npm.cmd" start
```

**Open browser:** `http://localhost:3000`  
**Ask a question:** "How do I switch funds?"  
**Expected response:** FAQ answer from database

---

## 🐳 Docker Deployment

```powershell
docker compose up --build
```

Access at:
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`

---

## 📝 FAQ Database

Located in `backend/data/faq_data.py`:

1. How do I switch funds in my policy?
2. How can I redirect future premiums to a different fund?
3. What is the Automatic Transfer Strategy/Plan (ATS/ATP)?
4. How do I enable ATS/ATP in my policy?
5. What is a Portfolio Investment Strategy?
6. How do I change the Portfolio Investment Strategy?
7. How do I top-up my policy?
8. How do I get a copy of my policy/unit statement?
9. How do I request for Partial Withdrawal of funds?

---

## 🔧 Troubleshooting

**npm command not found:**
```powershell
&"C:\Program Files\nodejs\npm.cmd" install
```

**Python dependencies error:**
```powershell
python -m pip install -r requirements.txt --only-binary :all:
```

**Port already in use:**
- Backend: Change port in `python -m uvicorn app.main:app --port 8001`
- Frontend: Change port in `.env` file (create one with `REACT_APP_PORT=3001`)

---

## 📚 Technology Stack

- **Backend:** FastAPI, Uvicorn, Neuro-SAN (optional)
- **Frontend:** React 18, JavaScript
- **Database:** Python dataclass (in-memory)
- **Validation:** Python dataclasses
- **Containerization:** Docker & Docker Compose

---

## 📞 Support

For questions about FAQ content: Refer to ICICI Prulife documentation  
For technical issues: Check API docs at `http://localhost:8000/docs`

---

**Last Updated:** January 2026  
**Version:** 1.0.0 with Neuro-SAN
A full-stack FAQ chatbot that answers user questions using a static FAQ dataset and multi-turn conversation handling via Neuro-SAN.

# Overview
This project implements a simple chatbot that:

Supports multi-turn conversations
Answers questions using an FAQ dataset
Uses a Neuro-SAN agentic network to orchestrate responses
Is fully dockerized with CI/CD via GitHub Actions

# Architecture
Web UI → Backend API → Neuro-SAN Agent → LLM + FAQ Data

# Components:
Web UI: Minimal chat interface for users
Backend API: Exposes REST endpoint to receive user messages
Neuro-SAN Agent: Handles conversation logic, context, and dataset lookup
LLM + FAQ Data: Language model that's queried to generate answers

# Tech Stack
Frontend: [React / Vue / HTML + CSS]
Backend: Python (Flask / FastAPI)
Neuro-SAN: Cognitive agentic network integration
Docker: Containerization for frontend and backend
CI/CD: GitHub Actions
FAQ Data: Static JSON/text dataset

# How Neuro-SAN Conversation Works
The Neuro-SAN agent works as a graph of smaller reasoning and retrieval components:

Input Reception: Backend receives user message via /chat.
Context Integration: Maintains conversation history (multi-turn).
Dataset Access: FAQ data is available as structured context or retriever.
Agentic Reasoning: Neuro-SAN orchestrates:
Memory logic
RAG or direct FAQ lookup
LLM prompt generation
Output: Answer text returned to frontend.
Multi-Turn Handling
Conversation state is passed with every request.
The agent uses history to produce context-relevant replies.

# API Endpoints
POST /chat

Request
{
  "session_id": "abc123",
  "message": "How do I change my bank account?"
}

Response
{
  "reply": "You can change your registered bank account by submitting a request..."
}

# Installation & Usage
Without Docker
Backend:
cd backend
pip install -r requirements.txt
python app.py
Frontend:
cd frontend
npm install
npm start

With Docker
Build backend:
docker build -t faq-chatbot-backend backend/
Build frontend:
docker build -t faq-chatbot-frontend frontend/
Run:
docker run -p 5000:5000 faq-chatbot-backend
docker run -p 3000:3000 faq-chatbot-frontend

Docker Compose
docker-compose up --build

# CI/CD – GitHub Actions
This project includes a workflow that:

Runs on main branch commits
Builds frontend and backend Docker images
Pushes both to DockerHub
Example workflow file:
.github/workflows/ci-cd.yml

# DockerHub Image Links
Replace these with your actual published images:
Backend: https://hub.docker.com/repository/docker/yourname/faq-chatbot-backend
Frontend: https://hub.docker.com/repository/docker/yourname/faq-chatbot-frontend

# Assumptions & Limitations
Dataset is static and needs updating manually
LLM may return approximate answers
No user authentication
Conversation history stored temporarily (not in DB)

# References
Neuro-SAN GitHub: https://github.com/cognizant-ai-lab/neuro-san
Quickstart Instructions: https://github.com/cognizant-ai-lab/neuro-san-studio/blob/main/docs/integration_quickstart.md

# Contact / Support
If you have questions or want to improve this chatbot, feel free to reach out!
