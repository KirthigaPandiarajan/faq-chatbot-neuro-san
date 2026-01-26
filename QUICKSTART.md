# Quick Start Guide - FAQ Chatbot

## 30-Second Setup

### Prerequisites
- Docker & Docker Compose installed
- OpenAI API Key ready

### Run It

```bash
# Set your API key
export OPENAI_API_KEY=sk-your-key-here

# Start the application
docker-compose up --build

# Access the app
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

## Without Docker (Local Development)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
export OPENAI_API_KEY=sk-your-key-here
export AGENT_MANIFEST_FILE=./registries/manifest.hocon
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend (New Terminal)
```bash
cd frontend
npm install
npm start
```

## Test the API

```bash
# Health check
curl http://localhost:8000/health

# Ask a question
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test", "message": "How do I switch funds?"}'

# View API docs
# Open: http://localhost:8000/docs
```

## Common Issues

| Issue | Fix |
|-------|-----|
| Port already in use | Kill process: `lsof -i :8000` then `kill -9 <PID>` |
| API key error | Check: `echo $OPENAI_API_KEY` |
| Agent not found | Verify: `backend/registries/manifest.hocon` exists |
| Docker build fails | Rebuild without cache: `docker-compose build --no-cache` |

## File Structure

```
backend/
├── registries/
│   ├── faq_agent.hocon       ← Agent configuration
│   └── manifest.hocon        ← Agent registry
├── data/
│   └── faq.json              ← Your FAQ data
├── app/
│   └── main.py               ← FastAPI + Agent logic
└── requirements.txt          ← Python dependencies
```

## Key Components

| Component | Purpose | Location |
|-----------|---------|----------|
| FastAPI Backend | Receives requests, invokes agents | `backend/app/main.py` |
| FAQ Agent | Answers questions from FAQ | `backend/registries/faq_agent.hocon` |
| React Frontend | User chat interface | `frontend/src/App.js` |
| FAQ Data | Questions and answers | `backend/data/faq.json` |

## Next Steps

1. **Customize FAQ**: Edit `backend/data/faq.json`
2. **Adjust Agent**: Modify `backend/registries/faq_agent.hocon`
3. **Test**: Use `/docs` endpoint
4. **Deploy**: Use Docker for production

For detailed setup, see [SETUP.md](SETUP.md)
