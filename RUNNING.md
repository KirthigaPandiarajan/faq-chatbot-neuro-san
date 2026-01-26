# Step-by-Step Running Guide

This guide provides complete step-by-step instructions for running the FAQ Chatbot with neuro-san integration.

## Prerequisites Check

Before starting, verify you have:

```bash
# Check Docker
docker --version      # Should be 20.10+
docker-compose --version  # Should be 1.29+

# Check Python (for local development)
python --version      # Should be 3.10+

# Check Node.js (for frontend development)
node --version        # Should be 16+
```

---

## Method 1: Docker Compose (Easiest - Recommended)

### Step 1: Get Your OpenAI API Key

1. Go to: https://platform.openai.com/api/keys
2. Sign in to your account (create one if needed)
3. Click "Create new secret key"
4. Copy the key immediately (you won't see it again)

### Step 2: Set Environment Variable

**Windows (PowerShell) - Open PowerShell as Administrator**:
```powershell
$env:OPENAI_API_KEY = "sk-your-key-here"
```

**Windows (Command Prompt)**:
```cmd
set OPENAI_API_KEY=sk-your-key-here
```

**Linux/Mac (Terminal)**:
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

### Step 3: Navigate to Project Directory

```bash
cd path/to/faq-chatbot-neuro-san
```

### Step 4: Build and Run with Docker Compose

```bash
docker-compose up --build
```

This will:
- Build backend Docker image (will install neuro-san automatically)
- Build frontend Docker image
- Start both services
- Display logs in your terminal

**Wait for these lines to appear:**
```
backend  | INFO:     Uvicorn running on http://0.0.0.0:8000
frontend | webpack 5.88.0 compiled successfully
```

### Step 5: Access the Application

Open your browser and visit:

- **Frontend (Chat UI)**: http://localhost:3000
- **Backend API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Step 6: Test the Chatbot

1. Open http://localhost:3000 in your browser
2. Type a message like: "How do I switch funds?"
3. The chatbot should respond with an FAQ answer

### Step 7: Stop the Application

In your terminal, press: `Ctrl+C`

Then run:
```bash
docker-compose down
```

---

## Method 2: Local Development (Without Docker)

### Part A: Backend Setup

#### Step 1: Navigate to Backend Directory
```bash
cd backend
```

#### Step 2: Create Virtual Environment

**Windows (PowerShell)**:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt)**:
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/Mac**:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install neuro-san and all required packages (may take 2-3 minutes).

#### Step 4: Set Environment Variables

**Windows (PowerShell)**:
```powershell
$env:OPENAI_API_KEY = "sk-your-key-here"
$env:AGENT_MANIFEST_FILE = "./registries/manifest.hocon"
$env:PYTHONUNBUFFERED = "1"
```

**Linux/Mac**:
```bash
export OPENAI_API_KEY="sk-your-key-here"
export AGENT_MANIFEST_FILE="./registries/manifest.hocon"
export PYTHONUNBUFFERED=1
```

#### Step 5: Run Backend Server
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Keep this terminal open!** Backend is now running at: http://localhost:8000

### Part B: Frontend Setup (In New Terminal)

#### Step 1: Navigate to Frontend Directory
```bash
cd frontend
```

#### Step 2: Install Dependencies
```bash
npm install
```

This will take 1-2 minutes and install React and dependencies.

#### Step 3: Run Frontend Server
```bash
npm start
```

**Expected Output:**
```
webpack 5.88.0 compiled successfully

You can now view faq-chatbot-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

**Browser will open automatically** to http://localhost:3000

### Step 4: Test the Application

1. Type a question in the chat window
2. Wait for the response (first request takes ~3-5 seconds)
3. Continue the conversation

### Step 5: Stop the Application

**Backend (Terminal 1)**: Press `Ctrl+C`
**Frontend (Terminal 2)**: Press `Ctrl+C`

---

## Method 3: Testing with API Directly

Without opening the frontend, you can test the backend API.

### Step 1: Start Backend

Follow **Method 2, Part A** (Steps 1-5) to start the backend server.

### Step 2: Test in New Terminal

**Windows (PowerShell)**:
```powershell
$body = @{
    session_id = "test_user"
    message = "How do I switch funds?"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:8000/chat" `
    -Method Post `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body

$response.Content | ConvertFrom-Json | ConvertTo-Json
```

**Linux/Mac (curl)**:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test_user",
    "message": "How do I switch funds?"
  }' | jq .
```

### Step 3: View API Documentation

Open in browser: http://localhost:8000/docs

This opens interactive Swagger UI where you can:
- See all available endpoints
- Try endpoints directly
- View request/response schemas

---

## Quick Reference: Common Commands

### Check if Services are Running

**Windows (PowerShell)**:
```powershell
# Check backend
Invoke-WebRequest http://localhost:8000/health

# Check frontend
Invoke-WebRequest http://localhost:3000
```

**Linux/Mac**:
```bash
# Check backend
curl http://localhost:8000/health

# Check frontend
curl http://localhost:3000
```

### Rebuild Docker Images

```bash
# Without cache (slower but fresh)
docker-compose build --no-cache

# Then start
docker-compose up
```

### View Docker Logs

```bash
# All services
docker-compose logs

# Just backend
docker-compose logs backend

# Just frontend
docker-compose logs frontend

# Follow logs (like tail -f)
docker-compose logs -f backend
```

### Stop and Clean Up

```bash
# Stop containers but keep images
docker-compose down

# Remove everything (containers, images, volumes)
docker-compose down -v
```

---

## Troubleshooting During Setup

### Issue: "OPENAI_API_KEY is not set"

**Error in logs:**
```
Error: OpenAI API key not provided
```

**Fix**:
1. Check variable is set: `echo $OPENAI_API_KEY`
2. Verify it starts with `sk-`
3. Re-set the variable in the SAME terminal you're running from
4. Check for typos

### Issue: "Port 8000 already in use"

**Error:**
```
Address already in use: ('0.0.0.0', 8000)
```

**Fix**:

**Windows**:
```powershell
netstat -ano | findstr :8000
# Copy the PID from the output
taskkill /PID <PID> /F
```

**Linux/Mac**:
```bash
lsof -i :8000
# Copy the PID from the output
kill -9 <PID>
```

### Issue: "neuro-san module not found"

**Error:**
```
ModuleNotFoundError: No module named 'neuro_san'
```

**Fix**:
```bash
# Make sure you're in the backend directory
cd backend

# Make sure virtual environment is activated
# (you should see (venv) in your terminal prompt)

# Reinstall requirements
pip install -r requirements.txt

# Check installation
python -c "import neuro_san; print('OK')"
```

### Issue: "npm command not found"

**Fix**:
1. Install Node.js from: https://nodejs.org/
2. Close and reopen your terminal
3. Verify: `node --version` and `npm --version`

### Issue: "Agent not found"

**Error in browser:**
```
"Agent 'faq_agent' not found"
```

**Fix**:
1. Verify files exist:
   - `backend/registries/manifest.hocon`
   - `backend/registries/faq_agent.hocon`
2. Check manifest contains: `"faq_agent.hocon": true`
3. Restart backend service

### Issue: "Frontend cannot connect to backend"

**Error in browser console:**
```
Failed to fetch http://localhost:8000/chat
```

**Fix**:
1. Check backend is running: `curl http://localhost:8000/health`
2. Check frontend environment variable (if needed):
   - For Docker: `REACT_APP_API_URL=http://localhost:8000`
   - For local: Usually auto-detected as http://localhost:8000
3. Check Docker network if using Docker (should auto-connect)

---

## Performance Expectations

### First Run
- Backend startup: ~30 seconds (first LLM request takes longer)
- Frontend startup: ~20 seconds
- First chat response: ~3-5 seconds (model initialization)

### Subsequent Runs
- Backend startup: ~5-10 seconds
- Frontend startup: ~5-10 seconds
- Chat response: ~1-2 seconds

### If Responses are Slow
1. Check internet connection (API calls to OpenAI)
2. Try `gpt-3.5-turbo` in `faq_agent.hocon` (faster but less capable)
3. Reduce `max_tokens` in agent config
4. Check system resources (CPU, memory)

---

## Next Steps After Running

1. **Test Endpoints**:
   - Visit http://localhost:8000/docs
   - Try POST /chat with different questions
   - Try GET /sessions/{session_id}

2. **Customize FAQ Data**:
   - Edit `backend/data/faq.json`
   - Restart backend to load new data

3. **Modify Agent Behavior**:
   - Edit `backend/registries/faq_agent.hocon`
   - Change instructions or model
   - Restart backend

4. **View Logs**:
   - Backend logs show agent invocations
   - Frontend logs show API requests
   - Useful for debugging issues

5. **Deploy to Production**:
   - Use docker-compose with proper resource limits
   - Set up environment variables in CI/CD
   - Use process manager (supervisor, systemd)

---

## Summary

**Quickest way to run:**
```bash
export OPENAI_API_KEY=sk-your-key-here
docker-compose up --build
# Visit http://localhost:3000
```

**For local development:**
```bash
# Terminal 1
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-your-key-here
python -m uvicorn app.main:app --reload

# Terminal 2
cd frontend && npm install && npm start
```

For detailed documentation, see:
- [SETUP.md](SETUP.md) - Comprehensive setup guide
- [QUICKSTART.md](QUICKSTART.md) - Quick reference
- [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) - How everything works together
