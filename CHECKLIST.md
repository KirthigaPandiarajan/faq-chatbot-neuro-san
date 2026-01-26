# FAQ Chatbot Setup Checklist

Use this checklist to verify your setup is complete and working correctly.

---

## Pre-Requisites

- [ ] Git installed and path available
- [ ] Docker installed (version 20.10+)
- [ ] Docker Compose installed (version 1.29+)
- [ ] OpenAI API Key obtained (starts with `sk-`)
- [ ] Project folder downloaded/cloned

---

## Files Verification

### Check Modified Files

- [ ] `backend/requirements.txt` contains `neuro-san>=0.1.0`
- [ ] `backend/app/main.py` imports from `neuro_san.client.agent_session_factory`
- [ ] `backend/Dockerfile` has proper setup commands
- [ ] `docker-compose.yml` has environment variables and volumes

### Check New Files

- [ ] `backend/registries/faq_agent.hocon` exists
- [ ] `backend/registries/manifest.hocon` exists
- [ ] `SETUP.md` exists
- [ ] `QUICKSTART.md` exists
- [ ] `ENV_SETUP.md` exists
- [ ] `RUNNING.md` exists
- [ ] `INTEGRATION_GUIDE.md` exists
- [ ] `IMPLEMENTATION_SUMMARY.md` exists

---

## Environment Setup

### Windows (PowerShell)

- [ ] OpenAI API Key set:
  ```powershell
  $env:OPENAI_API_KEY = "sk-your-key-here"
  # Verify:
  echo $env:OPENAI_API_KEY
  ```

### Linux/Mac (Bash)

- [ ] OpenAI API Key set:
  ```bash
  export OPENAI_API_KEY="sk-your-key-here"
  # Verify:
  echo $OPENAI_API_KEY
  ```

---

## Option A: Docker Setup

- [ ] Navigate to project directory:
  ```bash
  cd path/to/faq-chatbot-neuro-san
  ```

- [ ] Build images:
  ```bash
  docker-compose build
  ```

- [ ] Run containers:
  ```bash
  docker-compose up
  ```

- [ ] Check backend is running:
  ```bash
  curl http://localhost:8000/health
  ```
  ✅ Should return: `{"status": "healthy", ...}`

- [ ] Check frontend is running:
  ```bash
  curl http://localhost:3000
  ```
  ✅ Should return HTML content

- [ ] Open in browser:
  ```
  Frontend: http://localhost:3000
  API Docs: http://localhost:8000/docs
  ```

---

## Option B: Local Development Setup

### Backend Setup

- [ ] Navigate to backend:
  ```bash
  cd backend
  ```

- [ ] Create virtual environment:
  ```bash
  python -m venv venv
  # Activate:
  # Windows: venv\Scripts\activate
  # Linux/Mac: source venv/bin/activate
  ```

- [ ] Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

- [ ] Set environment variables:
  ```bash
  export OPENAI_API_KEY="sk-your-key-here"
  export AGENT_MANIFEST_FILE="./registries/manifest.hocon"
  ```

- [ ] Start backend:
  ```bash
  python -m uvicorn app.main:app --reload --port 8000
  ```

- [ ] Verify backend running:
  ```bash
  curl http://localhost:8000/health
  ```

### Frontend Setup (New Terminal)

- [ ] Navigate to frontend:
  ```bash
  cd frontend
  ```

- [ ] Install dependencies:
  ```bash
  npm install
  ```

- [ ] Start frontend:
  ```bash
  npm start
  ```

- [ ] Verify frontend running:
  ```
  Browser: http://localhost:3000
  ```

---

## Functionality Tests

### Test 1: Health Check

```bash
curl http://localhost:8000/health
```

- [ ] Returns JSON with status: "healthy"
- [ ] Shows correct manifest file path
- [ ] Shows service name: "FAQ Chatbot"

### Test 2: API Documentation

```
Visit: http://localhost:8000/docs
```

- [ ] Swagger UI loads
- [ ] Shows endpoints: /chat, /health, /sessions/{session_id}
- [ ] Can see request/response schemas

### Test 3: Chat Endpoint

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test_user",
    "message": "How do I switch funds?"
  }'
```

- [ ] Returns JSON response
- [ ] Contains "reply" field with actual response
- [ ] Status is "success"
- [ ] Response mentions "Fund switch" (from FAQ data)

### Test 4: Frontend Chat

```
Visit: http://localhost:3000
```

- [ ] Chat interface loads
- [ ] Can type messages
- [ ] Can send messages (button works)
- [ ] Receives responses from backend
- [ ] Responses are FAQ-based

### Test 5: Session History

```bash
curl http://localhost:8000/sessions/test_user
```

- [ ] Returns JSON with session history
- [ ] Shows previous questions and answers
- [ ] History is properly stored

---

## Configuration Checks

### Agent Configuration

- [ ] File exists: `backend/registries/faq_agent.hocon`
- [ ] Contains `llm_config` section
- [ ] Contains `model_name`: "gpt-4o-mini"
- [ ] Contains `tools` array with agent definition
- [ ] Contains `instructions` for agent behavior

### Manifest Configuration

- [ ] File exists: `backend/registries/manifest.hocon`
- [ ] Contains: `"faq_agent.hocon": true`
- [ ] Properly formatted HOCON syntax

### FAQ Data

- [ ] File exists: `backend/data/faq.json`
- [ ] Contains JSON array of Q&A pairs
- [ ] Each entry has "question" and "answer"

---

## Docker-Specific Checks

### Images Built

```bash
docker images | grep faq-chatbot
```

- [ ] `faq-chatbot-neuro-san-backend` image exists
- [ ] `faq-chatbot-neuro-san-frontend` image exists

### Containers Running

```bash
docker ps
```

- [ ] `faq-chatbot-backend` container is running
- [ ] `faq-chatbot-frontend` container is running
- [ ] Both are healthy (health check passed)

### Logs Check

```bash
docker-compose logs backend
```

- [ ] No error messages
- [ ] Shows "Application startup complete"
- [ ] Shows "Uvicorn running on 0.0.0.0:8000"

### Volume Mounts

```bash
# Inside container
docker exec faq-chatbot-backend ls -la /app/registries/
```

- [ ] `faq_agent.hocon` file visible
- [ ] `manifest.hocon` file visible

---

## Performance Checks

### Backend Response Time

- [ ] First response takes 3-5 seconds (acceptable)
- [ ] Subsequent responses take 1-2 seconds
- [ ] No timeout errors

### Memory Usage

```bash
docker stats
```

- [ ] Backend memory usage: < 500MB
- [ ] Frontend memory usage: < 300MB
- [ ] No excessive CPU usage

### Network Connectivity

- [ ] Frontend can reach backend (no CORS errors)
- [ ] Backend can reach OpenAI API
- [ ] No connection timeout errors

---

## Troubleshooting Checklist

If something isn't working, check these:

### Agent Not Found Error

- [ ] Manifest file exists: `backend/registries/manifest.hocon`
- [ ] Agent is enabled: `"faq_agent.hocon": true`
- [ ] Agent config exists: `backend/registries/faq_agent.hocon`
- [ ] AGENT_MANIFEST_FILE env var is set correctly
- [ ] Backed is restarted after changes

### OpenAI API Key Error

- [ ] API key starts with `sk-`
- [ ] Environment variable is set: `echo $OPENAI_API_KEY`
- [ ] API key is valid (check OpenAI dashboard)
- [ ] Not expired or revoked
- [ ] Proper permissions set in OpenAI

### Port Already in Use

- [ ] Kill process using port 8000
- [ ] Kill process using port 3000
- [ ] Restart docker-compose
- [ ] Or change ports in docker-compose.yml

### Docker Build Failures

- [ ] Check internet connection
- [ ] Rebuild without cache: `docker-compose build --no-cache`
- [ ] Check Docker daemon is running
- [ ] Check sufficient disk space

### Frontend Cannot Connect

- [ ] Backend is running (curl health check)
- [ ] CORS is enabled in main.py (it is)
- [ ] Frontend API URL is correct
- [ ] No firewall blocking port 8000
- [ ] Services on same Docker network

---

## Post-Setup Actions

### Customize FAQ Data

- [ ] Edit `backend/data/faq.json`
- [ ] Add/remove Q&A pairs
- [ ] Restart backend to load changes
- [ ] Test with new questions

### Customize Agent Behavior

- [ ] Edit `backend/registries/faq_agent.hocon`
- [ ] Change model, temperature, or instructions
- [ ] Restart backend
- [ ] Test changes

### Add New Agent

- [ ] Create `backend/registries/new_agent.hocon`
- [ ] Update `backend/registries/manifest.hocon`
- [ ] Create new endpoint in `main.py`
- [ ] Test the new agent

### Monitor Logs

- [ ] Docker: `docker-compose logs -f`
- [ ] Local backend: Check terminal output
- [ ] Local frontend: Check browser console (F12)

---

## Documentation Check

- [ ] Read [QUICKSTART.md](QUICKSTART.md) for overview
- [ ] Read [RUNNING.md](RUNNING.md) for step-by-step instructions
- [ ] Read [SETUP.md](SETUP.md) for comprehensive guide
- [ ] Read [ENV_SETUP.md](ENV_SETUP.md) for environment setup
- [ ] Read [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) for technical details

---

## Sign-Off

When all items are checked:

✅ **Setup is complete and working!**

You can now:
- Use the FAQ chatbot
- Customize agent behavior
- Add new agents
- Deploy to production
- Integrate with other systems

---

## Quick Command Reference

```bash
# Start with Docker
export OPENAI_API_KEY=sk-your-key-here
docker-compose up --build

# Start locally (terminal 1)
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-your-key-here
python -m uvicorn app.main:app --reload

# Start locally (terminal 2)
cd frontend && npm install && npm start

# Test API
curl http://localhost:8000/health

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Clean everything
docker-compose down -v
```

---

## Support

For issues:
1. Check the **Troubleshooting Checklist** above
2. Check the relevant guide: SETUP.md, RUNNING.md, ENV_SETUP.md
3. Check logs: `docker-compose logs -f backend`
4. Verify environment variables are set
5. Verify files exist and have correct content

Good luck! 🚀
