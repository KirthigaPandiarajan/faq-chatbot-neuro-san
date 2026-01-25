# FAQ Chatbot with Neuro-SAN
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
