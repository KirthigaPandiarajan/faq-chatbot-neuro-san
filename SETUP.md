# FAQ Chatbot with Neuro-SAN - Setup Guide

This guide walks you through setting up and running the FAQ Chatbot with integrated neuro-san agent network.

## Overview

The FAQ Chatbot is a full-stack application that:
- Uses neuro-san's `DirectAgentSessionFactory` to invoke agents directly
- Answers customer questions using an FAQ dataset
- Maintains multi-turn conversations
- Provides both REST API backend and React frontend
- Fully containerized with Docker

## Architecture

```
Frontend (React)
    ↓ (HTTP)
Backend API (FastAPI)
    ↓ (Python imports)
Neuro-SAN Agent (DirectAgentSessionFactory)
    ↓
LLM Model (OpenAI GPT-4o-mini) + FAQ Data
```

## Prerequisites

Before starting, ensure you have installed:

1. **Git** - For version control
2. **Docker & Docker Compose** - For containerized deployment
3. **Python 3.10+** - For local development (optional, not needed for Docker)
4. **Node.js 16+** - For frontend development (optional, not needed for Docker)
5. **OpenAI API Key** - Required for LLM functionality
6. **neuro-san** - Will be installed automatically via requirements.txt

## Quick Start with Docker

### Step 1: Set Environment Variables

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=sk-your-key-here
```

Or set it via command line:

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY = "sk-your-key-here"
```

**Linux/Mac (Bash):**
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

### Step 2: Build and Run with Docker Compose

```bash
# From the project root directory
docker-compose up --build
```

This command will:
- Build the backend Docker image (includes neuro-san and dependencies)
- Build the frontend Docker image
- Start both services on configured ports
- Set up the shared network

### Step 3: Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Step 4: Stop the Application

```bash
docker-compose down
```

---

## Local Development Setup (Without Docker)

### Backend Setup

#### 1. Navigate to backend directory:
```bash
cd backend
```

#### 2. Create a virtual environment (recommended):

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

#### 4. Set environment variables:

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY = "sk-your-key-here"
$env:AGENT_MANIFEST_FILE = "./registries/manifest.hocon"
$env:PYTHONUNBUFFERED = "1"
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="sk-your-key-here"
export AGENT_MANIFEST_FILE="./registries/manifest.hocon"
export PYTHONUNBUFFERED=1
```

#### 5. Run the backend server:
```bash
# From backend directory
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

### Frontend Setup

#### 1. Navigate to frontend directory:
```bash
cd frontend
```

#### 2. Install dependencies:
```bash
npm install
```

#### 3. Set environment variable (optional):

Create `.env` file in the `frontend` directory:
```
REACT_APP_API_URL=http://localhost:8000
```

#### 4. Run the frontend development server:
```bash
npm start
```

Frontend will be available at: `http://localhost:3000`

---

## Project Structure

```
faq-chatbot-neuro-san/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application with agent integration
│   │   └── agent_logic.py       # Agent invocation logic
│   ├── registries/              # Agent configurations
│   │   ├── faq_agent.hocon      # FAQ agent configuration
│   │   └── manifest.hocon       # Agent manifest (registry of agents)
│   ├── config/
│   │   └── network.hocon        # Network configuration
│   ├── data/
│   │   └── faq.json             # FAQ dataset
│   ├── Dockerfile               # Backend Docker image
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.js               # Main React component
│   │   ├── ChatWindow.js        # Chat UI component
│   │   └── index.js             # React entry point
│   ├── public/
│   │   └── index.html           # HTML template
│   ├── Dockerfile               # Frontend Docker image
│   └── package.json             # Node.js dependencies
├── docker-compose.yml           # Docker Compose configuration
└── README.md                    # Project overview
```

---

## API Endpoints

### Chat Endpoint

**POST** `/chat`

Send a message to the FAQ agent:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "user_123",
    "message": "How do I switch funds in my policy?"
  }'
```

**Response:**
```json
{
  "session_id": "user_123",
  "reply": "Fund switch allows you to transfer current funds to another of your choice...",
  "status": "success"
}
```

### Health Check

**GET** `/health`

Check if the API is running:

```bash
curl http://localhost:8000/health
```

### Session History

**GET** `/sessions/{session_id}`

Retrieve conversation history:

```bash
curl http://localhost:8000/sessions/user_123
```

### Clear Session

**DELETE** `/sessions/{session_id}`

Clear conversation history:

```bash
curl -X DELETE http://localhost:8000/sessions/user_123
```

### API Documentation

**GET** `/docs`

Interactive API documentation (Swagger UI):
```
http://localhost:8000/docs
```

---

## How It Works

### 1. Frontend to Backend Communication

1. User types a message in the React frontend
2. Frontend sends HTTP POST request to `/chat` endpoint
3. Request includes: `session_id` and `message` text

### 2. Agent Invocation (Backend)

The backend's `main.py` uses `DirectAgentSessionFactory`:

```python
from neuro_san.client.agent_session_factory import DirectAgentSessionFactory

factory = DirectAgentSessionFactory()
session = factory.create_session(
    agent_name="faq_agent",
    use_direct=True,
    metadata={"session_id": session_id}
)
```

### 3. Agent Configuration

The FAQ agent is configured in `backend/registries/faq_agent.hocon`:

```hocon
{
    "llm_config": {
        "model_name": "gpt-4o-mini",
        "temperature": 0.2
    },
    "tools": [
        {
            "name": "FAQAgent",
            "instructions": "You are a helpful FAQ customer support chatbot..."
        }
    ]
}
```

### 4. Response Processing

1. Agent streams response through streaming_chat()
2. Backend collects all message chunks
3. Extracts text response and returns to frontend
4. Frontend displays the reply to the user

---

## Configuration Details

### Agent Configuration (`faq_agent.hocon`)

Key sections:

- **llm_config**: Specifies the LLM model and parameters
  - `model_name`: The LLM model to use (gpt-4o-mini, gpt-4o, claude-3, etc.)
  - `temperature`: Controls response creativity (0.0-1.0)
  
- **tools**: Array of agent tools
  - `name`: Agent identifier
  - `description`: What the agent does
  - `instructions`: System prompt for agent behavior

### Manifest (`manifest.hocon`)

Lists all available agents:

```hocon
{
    "faq_agent.hocon": true      # Enable FAQ agent
    # "other_agent.hocon": true  # Can add more agents here
}
```

---

## Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `OPENAI_API_KEY` | Yes | - | Your OpenAI API key for LLM calls |
| `AGENT_MANIFEST_FILE` | No | `./registries/manifest.hocon` | Path to agent manifest |
| `PYTHONUNBUFFERED` | No | `1` | Unbuffered Python output |
| `OPENAI_MODEL` | No | `gpt-4o-mini` | Default LLM model |

---

## Troubleshooting

### Issue: Agent Not Found Error

**Error**: `Agent 'faq_agent' not found`

**Solutions**:
1. Verify manifest file exists: `backend/registries/manifest.hocon`
2. Check manifest contains: `"faq_agent.hocon": true`
3. Ensure `AGENT_MANIFEST_FILE` environment variable is set correctly
4. Check agent config file exists: `backend/registries/faq_agent.hocon`

### Issue: OpenAI API Key Error

**Error**: `Invalid API key` or `Authentication failed`

**Solutions**:
1. Verify your API key is correct: `echo $OPENAI_API_KEY`
2. Check API key has correct permissions in OpenAI dashboard
3. Regenerate API key if expired
4. Use format: `sk-...` (starts with sk-)

### Issue: Port Already in Use

**Error**: `Address already in use: ('0.0.0.0', 8000)`

**Solutions**:
```bash
# Check what's using the port
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Kill the process (Linux/Mac)
kill -9 <PID>

# Or use a different port:
docker-compose down
# Edit docker-compose.yml port mapping
docker-compose up --build
```

### Issue: Docker Build Failures

**Error**: `failed to solve: neuro-san not found`

**Solutions**:
1. Ensure `requirements.txt` includes `neuro-san>=0.1.0`
2. Rebuild without cache: `docker-compose build --no-cache`
3. Check internet connectivity during build
4. Verify pip package index is accessible

### Issue: Frontend Cannot Connect to Backend

**Error**: `Failed to fetch` in browser console

**Solutions**:
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check CORS is enabled in backend (should be in main.py)
3. Verify `REACT_APP_API_URL` environment variable
4. For Docker, use service name: `http://backend:8000` inside container

---

## Performance Optimization

### For Production Deployment

1. **Update docker-compose.yml**:
   - Remove `--reload` flag from FastAPI command
   - Set appropriate resource limits

2. **Scale Backend**:
   - Use load balancer (nginx, HAProxy)
   - Run multiple backend instances

3. **Caching**:
   - Implement Redis for session storage
   - Cache FAQ data in memory

4. **Model Selection**:
   - Use `gpt-3.5-turbo` for faster, cheaper responses
   - Consider locally-hosted models (Ollama, Llama)

---

## Integration with neuro-san-studio

If you want to design agents in neuro-san-studio:

1. **Export Agent from Studio**:
   - Create/design agent in neuro-san-studio
   - Export as `.hocon` configuration file

2. **Copy to Registries**:
   ```bash
   cp studio_agent.hocon backend/registries/
   ```

3. **Register in Manifest**:
   ```hocon
   {
       "faq_agent.hocon": true,
       "studio_agent.hocon": true
   }
   ```

4. **Invoke in Code**:
   ```python
   invoke_faq_agent("studio_agent", "Your message")
   ```

---

## Integration with neuro-san Core

The application uses neuro-san's `DirectAgentSessionFactory` for direct in-process agent invocation:

**Advantages**:
- No network overhead
- Faster response times
- Better for development and testing

**Alternative**: HTTP Server Integration

To use neuro-san as a separate server:

```bash
# Terminal 1: Start neuro-san server
python -m neuro_san.service.main_loop.server_main_loop

# Terminal 2: Update main.py to use HTTP requests
# Replace DirectAgentSessionFactory with requests.post()
```

---

## Key Files Modified

### 1. `backend/requirements.txt`
- Added `neuro-san>=0.1.0`
- Added supporting libraries (pyyaml, requests, etc.)

### 2. `backend/app/main.py`
- Integrated `DirectAgentSessionFactory`
- Added `/chat` endpoint with agent invocation
- Added `/health` and session endpoints
- Implemented proper error handling

### 3. `backend/registries/`
- Created `faq_agent.hocon` - Agent configuration
- Created `manifest.hocon` - Agent registry

### 4. `docker-compose.yml`
- Added environment variables for OpenAI
- Added volume mounts for registries and data
- Configured proper networking
- Added health checks

### 5. `backend/Dockerfile`
- Updated to include registries and data
- Set proper environment variables
- Added health check command

---

## Next Steps

1. **Customize FAQ Data**: Edit `backend/data/faq.json` with your questions/answers
2. **Adjust Agent Behavior**: Modify instructions in `faq_agent.hocon`
3. **Test the API**: Use the `/docs` endpoint for interactive testing
4. **Deploy**: Follow Docker deployment best practices
5. **Monitor**: Add logging and monitoring (ELK stack, Datadog, etc.)

---

## Support

For issues or questions:

1. Check this guide's Troubleshooting section
2. Review neuro-san documentation: [https://github.com/neuro-san/neuro-san](https://github.com/neuro-san/neuro-san)
3. Check OpenAI API documentation: [https://platform.openai.com/docs](https://platform.openai.com/docs)
4. Review logs: `docker-compose logs -f backend`

---

## License

This project is provided as-is for educational and development purposes.
