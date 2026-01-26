# Complete Integration Guide - FAQ Chatbot with Neuro-SAN

## Summary of Changes Made

This document outlines all the modifications made to integrate neuro-san's `DirectAgentSessionFactory` into the FAQ Chatbot.

---

## What Changed

### 1. Backend Dependencies (`backend/requirements.txt`)

**Added**:
- `neuro-san>=0.1.0` - Core agent framework
- `pyyaml==6.0.1` - For HOCON configuration parsing
- `requests==2.31.0` - HTTP client
- `python-multipart==0.0.6` - For form data handling
- `aiofiles==23.2.1` - Async file operations
- Pinned versions for reliability

**Why**: These are required to use neuro-san's agent session factory and handle configuration files.

---

### 2. Backend API (`backend/app/main.py`)

**Complete Rewrite** with:

```python
# Key additions:

# 1. Import neuro-san
from neuro_san.client.agent_session_factory import DirectAgentSessionFactory

# 2. CORS middleware for frontend communication
app.add_middleware(CORSMiddleware, ...)

# 3. Proper request/response models
class ChatRequest(BaseModel):
    session_id: str
    message: str

# 4. Agent invocation function
def invoke_faq_agent(agent_name, user_text, session_id, sly_data):
    factory = DirectAgentSessionFactory()
    session = factory.create_session(
        agent_name=agent_name,
        use_direct=True,
        metadata={"session_id": session_id}
    )
    stream = session.streaming_chat(request_payload)
    # Collect and return messages

# 5. Main chat endpoint
@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    # Invoke agent and return response

# 6. Additional utility endpoints
@app.get("/health")              # Health check
@app.get("/sessions/{session_id}")  # Session history
@app.delete("/sessions/{session_id}")  # Clear session
```

**Key Features**:
- Uses `DirectAgentSessionFactory` for direct agent invocation (no network overhead)
- Streaming response handling (processes agent output in real-time)
- Session management (stores conversation history)
- Error handling and proper HTTP status codes
- OpenAPI/Swagger documentation support

---

### 3. Agent Configuration (`backend/registries/faq_agent.hocon`)

**New File** with:

```hocon
{
    "llm_config": {
        "model_name": "gpt-4o-mini",      # LLM model
        "temperature": 0.2,                # Lower = more deterministic
        "max_tokens": 1000                 # Response length limit
    },

    "tools": [
        {
            "name": "FAQAgent",            # Agent identifier
            "function": {
                "description": "..."       # What agent does
            },
            "instructions": "..."          # System prompt
        }
    ]
}
```

**Key Points**:
- Defines which LLM model to use
- Sets model parameters (temperature, tokens)
- Provides instructions for agent behavior
- Can be easily modified without code changes

---

### 4. Agent Manifest (`backend/registries/manifest.hocon`)

**New File** with:

```hocon
{
    "faq_agent.hocon": true
}
```

**Purpose**:
- Neuro-san discovers agents from this manifest
- `true` = agent is enabled
- Add more agents by adding more lines
- Example:
  ```hocon
  {
      "faq_agent.hocon": true,
      "general_support_agent.hocon": true,
      "sales_agent.hocon": false  # Disabled
  }
  ```

---

### 5. Docker Compose (`docker-compose.yml`)

**Enhanced with**:

```yaml
services:
  backend:
    # Environment variables
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - AGENT_MANIFEST_FILE=/app/registries/manifest.hocon
      - PYTHONUNBUFFERED=1
    
    # Volume mounts (to access configuration files)
    volumes:
      - ./backend/registries:/app/registries
      - ./backend/data:/app/data
    
    # Health check
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
```

**New Features**:
- Proper environment variable passing
- Volume mounts for dynamic configuration
- Health checks for reliability
- Shared network for backend-frontend communication

---

### 6. Dockerfile (`backend/Dockerfile`)

**Updated with**:

```dockerfile
# System dependencies
RUN apt-get install curl git

# Copy all necessary files
COPY backend/requirements.txt .
COPY backend/app ./app
COPY backend/registries ./registries
COPY backend/data ./data

# Environment variables
ENV AGENT_MANIFEST_FILE=/app/registries/manifest.hocon
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
    CMD curl -f http://localhost:8000/health || exit 1
```

---

## How It All Works Together

### Request Flow

```
1. User types message in React frontend
   ↓
2. Frontend sends HTTP POST to /chat endpoint
   {
     "session_id": "user_123",
     "message": "How do I switch funds?"
   }
   ↓
3. Backend receives request in main.py
   ↓
4. Backend calls invoke_faq_agent()
   ↓
5. DirectAgentSessionFactory creates session:
   factory.create_session(agent_name="faq_agent", use_direct=True)
   ↓
6. Agent loads configuration from registries/faq_agent.hocon
   - Reads LLM model: gpt-4o-mini
   - Reads system instructions
   - Reads temperature and other settings
   ↓
7. Agent sends request to OpenAI API:
   - Uses instructions from faq_agent.hocon
   - Can access FAQ data from backend/data/faq.json
   - Gets response from LLM
   ↓
8. Backend receives streamed response
   ↓
9. Response returned to frontend as JSON
   {
     "reply": "Fund switch allows you to...",
     "status": "success"
   }
   ↓
10. Frontend displays reply to user
```

### Configuration Flow

```
manifest.hocon → Lists available agents
      ↓
faq_agent.hocon → Configuration for specific agent
      ↓
    Contains: LLM model, temperature, instructions
      ↓
   Loaded by: DirectAgentSessionFactory
      ↓
    Used when: Agent is invoked
```

---

## Running the System

### Option 1: Docker Compose (Recommended)

```bash
# 1. Set API key
export OPENAI_API_KEY=sk-your-key-here

# 2. Start everything
docker-compose up --build

# 3. Access
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Docs: http://localhost:8000/docs
```

**What happens**:
- Docker builds backend image (installs neuro-san from requirements.txt)
- Docker builds frontend image
- Both containers start on shared network
- Registries mounted as volumes (can modify without rebuilding)
- Backend can access agent configurations
- Frontend can communicate with backend via HTTP

---

### Option 2: Local Development

```bash
# Terminal 1: Backend
cd backend
python -m venv venv
source venv/bin/activate
export OPENAI_API_KEY=sk-your-key-here
export AGENT_MANIFEST_FILE=./registries/manifest.hocon
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm install
npm start

# Terminal 3: Test (Optional)
curl http://localhost:8000/health
```

---

## Key Integration Points

### 1. DirectAgentSessionFactory

Located in: `backend/app/main.py`

```python
from neuro_san.client.agent_session_factory import DirectAgentSessionFactory

factory = DirectAgentSessionFactory()
session = factory.create_session(
    agent_name="faq_agent",     # Matches filename in registries/
    use_direct=True,             # Run in-process (not via HTTP)
    metadata={}                  # Optional metadata
)
```

**Why Direct Invocation**:
- Faster (no network latency)
- Simpler (no server management)
- Better for development
- Lower resource usage

---

### 2. Manifest Discovery

Located in: `backend/registries/manifest.hocon`

Neuro-san automatically discovers agents listed here:

```hocon
{
    "faq_agent.hocon": true        # Loaded automatically
}
```

When agent is created with name="faq_agent":
1. Neuro-san looks in manifest.hocon
2. Finds "faq_agent.hocon": true
3. Loads configuration from faq_agent.hocon file

---

### 3. Agent Configuration

Located in: `backend/registries/faq_agent.hocon`

Controls agent behavior without code changes:

```hocon
"llm_config": {
    "model_name": "gpt-4o-mini"  # Change model here
}

"instructions": "..."             # Change behavior here
```

---

## Customization Examples

### Change LLM Model

Edit `backend/registries/faq_agent.hocon`:

```hocon
"llm_config": {
    "model_name": "gpt-4o"        # Use more capable model
}
```

Or:

```hocon
"model_name": "gpt-3.5-turbo"    # Use faster/cheaper model
```

### Change Agent Behavior

Edit `backend/registries/faq_agent.hocon`:

```hocon
"instructions": """You are a sales agent. Provide product recommendations
rather than just answering FAQs. Be more promotional in tone."""
```

### Add Multiple Agents

1. Create `backend/registries/sales_agent.hocon`
2. Update `backend/registries/manifest.hocon`:
   ```hocon
   {
       "faq_agent.hocon": true,
       "sales_agent.hocon": true
   }
   ```
3. Create endpoint in `backend/app/main.py`:
   ```python
   def invoke_sales_agent(user_text):
       return invoke_faq_agent("sales_agent", user_text)
   ```

---

## Connection to neuro-san-studio and neuro-san Core

### neuro-san-studio
- **Used for**: Designing and visually building agents
- **Output**: `.hocon` configuration files
- **Integration**: Export agents and copy to `backend/registries/`

### neuro-san Core (neuro-san library)
- **Used for**: Running agents programmatically
- **Installed by**: `requirements.txt` (pip install neuro-san)
- **Used by**: `DirectAgentSessionFactory` in main.py

### Architecture
```
neuro-san-studio (GUI for design)
        ↓
    exports .hocon files
        ↓
backend/registries/ (stores configurations)
        ↓
neuro-san core (via DirectAgentSessionFactory)
        ↓
Agent execution
```

---

## Troubleshooting Checklist

| Issue | Check | Fix |
|-------|-------|-----|
| Agent not found | `registries/manifest.hocon` exists | Create file with `{"faq_agent.hocon": true}` |
| Agent not found | Agent enabled in manifest | Change `false` to `true` |
| Agent not found | `faq_agent.hocon` exists | Create agent config file |
| API key error | Variable is set | `echo $OPENAI_API_KEY` |
| Port conflict | Port 8000 free | `lsof -i :8000` then kill process |
| Docker build fails | Internet connected | `docker-compose build --no-cache` |
| Frontend can't reach backend | Services on same network | Check docker-compose.yml networks |

---

## Testing the Integration

### 1. Health Check
```bash
curl http://localhost:8000/health
```

Expected:
```json
{
  "status": "healthy",
  "service": "FAQ Chatbot",
  "manifest_file": "./registries/manifest.hocon"
}
```

### 2. Chat Request
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test_user",
    "message": "How do I switch funds in my policy?"
  }'
```

Expected:
```json
{
  "session_id": "test_user",
  "reply": "Fund switch allows...",
  "status": "success"
}
```

### 3. API Documentation
Visit: `http://localhost:8000/docs`
- Interactive Swagger UI
- Try out endpoints directly
- See request/response schemas

---

## Files at a Glance

| File | Purpose | Modified |
|------|---------|----------|
| `backend/requirements.txt` | Python dependencies | ✅ Added neuro-san |
| `backend/app/main.py` | FastAPI application | ✅ Complete rewrite with agent logic |
| `backend/registries/faq_agent.hocon` | Agent configuration | ✨ New file |
| `backend/registries/manifest.hocon` | Agent manifest | ✨ New file |
| `docker-compose.yml` | Container orchestration | ✅ Added env vars, volumes, health checks |
| `backend/Dockerfile` | Backend image definition | ✅ Enhanced with registries, data, health checks |
| `SETUP.md` | Detailed setup guide | ✨ New comprehensive guide |
| `QUICKSTART.md` | Quick reference | ✨ New quick guide |
| `ENV_SETUP.md` | Environment variables | ✨ New environment guide |

---

## Summary

You now have:

✅ Fully integrated neuro-san agent framework
✅ DirectAgentSessionFactory for agent invocation
✅ HOCON configuration files for easy customization
✅ Docker containerization for easy deployment
✅ Complete documentation and guides
✅ Multiple ways to run (Docker, local, HTTP)

Ready to use immediately - just set your OpenAI API key and run!

```bash
export OPENAI_API_KEY=sk-your-key-here
docker-compose up --build
# Visit http://localhost:3000
```

For detailed instructions, see [SETUP.md](SETUP.md)
