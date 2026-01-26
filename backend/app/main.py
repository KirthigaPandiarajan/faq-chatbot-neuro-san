import os
import warnings
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from dataclasses import dataclass
from typing import Optional, Dict, Any, List
import json
from pathlib import Path

# Suppress coroutine warnings for cleaner output
warnings.filterwarnings('ignore', category=RuntimeWarning)

# Import neuro-san components (optional - for production)
try:
    from neuro_san.client.agent_session_factory import DirectAgentSessionFactory
    NEURO_SAN_AVAILABLE = True
except ImportError:
    NEURO_SAN_AVAILABLE = False
    print("⚠️  WARNING: neuro-san not installed. Using mock agent for development only.")
    
    # Mock DirectAgentSessionFactory for development/testing
    class DirectAgentSessionFactory:
        """Mock implementation for local development without neuro-san"""
        def create_session(self, **kwargs):
            return MockAgentSession()
    
    class MockAgentSession:
        """Mock agent session that simulates agent responses"""
        def streaming_chat(self, payload):
            """Simulate agent response"""
            user_msg = payload.get("user_message", {}).get("text", "")
            faq_context = payload.get("faq_context", "")
            
            # Simple mock response based on input
            if any(word in user_msg.lower() for word in ["switch", "fund"]):
                response_text = "You can switch funds through your Online Account under Transactions > Switch Funds, or visit a branch."
            elif any(word in user_msg.lower() for word in ["redirect", "premium"]):
                response_text = "Use Premium Redirection to direct future premiums to a different fund. Processing takes 4 working days."
            elif any(word in user_msg.lower() for word in ["automatic", "atp", "ats"]):
                response_text = "Automatic Transfer Strategy (ATS) automatically transfers a fixed amount from debt fund to equity fund monthly."
            else:
                response_text = f"Based on your question about '{user_msg}', I'd recommend checking our FAQ or contacting support for detailed assistance."
            
            return [{"response": {"text": response_text}, "done": True}]

# Import FAQ database from Python module
from data.faq_data import get_faq_database, get_faq_count, search_faq

# Initialize FastAPI app
app = FastAPI(title="FAQ Chatbot API", version="1.0.0")

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store conversation sessions
session_histories: Dict[str, list] = {}

# Global FAQ data storage
FAQ_DATA: List[Dict[str, Any]] = []

# Define request/response dataclasses for validation
@dataclass
class ChatRequest:
    """Dataclass for chat request validation"""
    session_id: str
    message: str
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create instance from dictionary with validation"""
        if not isinstance(data, dict):
            raise ValueError("Request must be a dictionary")
        if "session_id" not in data or not data["session_id"]:
            raise ValueError("session_id is required")
        if "message" not in data or not data["message"]:
            raise ValueError("message is required")
        return cls(session_id=data["session_id"], message=data["message"])


@dataclass
class ChatResponse:
    """Dataclass for chat response"""
    session_id: str
    reply: str
    status: str
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON response"""
        return {
            "session_id": self.session_id,
            "reply": self.reply,
            "status": self.status
        }


def load_faq_data() -> List[Dict[str, Any]]:
    """Load FAQ data from Python module"""
    try:
        data = get_faq_database()
        print(f"✓ Loaded {get_faq_count()} FAQ items from faq_data.py")
        return data
    except Exception as e:
        print(f"❌ Error loading FAQ data: {str(e)}")
        return []


def format_faq_context(faq_items: List[Dict[str, Any]]) -> str:
    """Format FAQ data into a readable context string for the agent"""
    if not faq_items:
        return "No FAQ data available."
    
    context = "=== FAQ DATABASE ===\n\n"
    for i, item in enumerate(faq_items, 1):
        context += f"{i}. Q: {item.get('question', 'N/A')}\n"
        context += f"   A: {item.get('answer', 'N/A')}\n"
        if item.get('additional_info'):
            context += f"   Info: {item.get('additional_info')}\n"
        context += "\n"
    
    return context


# Initialize agent at startup
@app.on_event("startup")
async def startup_event():
    """Initialize the FAQ agent and verify manifest path"""
    global FAQ_DATA
    
    # Set the manifest location if not already set
    if "AGENT_MANIFEST_FILE" not in os.environ:
        os.environ["AGENT_MANIFEST_FILE"] = "./registries/manifest.hocon"
    
    # Load FAQ data
    FAQ_DATA = load_faq_data()
    
    # Print startup info
    mode = "🚀 PRODUCTION (neuro-san)" if NEURO_SAN_AVAILABLE else "🧪 DEVELOPMENT (mock agent)"
    print(f"\n{'='*60}")
    print(f"✓ FAQ Chatbot API initialized")
    print(f"✓ Mode: {mode}")
    print(f"✓ Manifest file: {os.environ.get('AGENT_MANIFEST_FILE')}")
    print(f"✓ FAQ database: {len(FAQ_DATA)} items loaded")
    print(f"{'='*60}\n")


@app.post("/chat")
async def chat_endpoint(request: Request):
    """
    Main chat endpoint that invokes the FAQ agent
    
    Args:
        request: Request with session_id and message
    
    Returns:
        Response with the agent's reply
    """
    try:
        # Parse JSON request body
        req_data = await request.json()
        
        # Validate request using dataclass
        try:
            validated_data = ChatRequest.from_dict(req_data)
        except ValueError as e:
            print(f"Validation error: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        
        # Invoke the agent with DirectAgentSessionFactory
        response = invoke_faq_agent(
            agent_name="faq_agent",
            user_text=validated_data.message,
            session_id=validated_data.session_id
        )
        
        # Extract the response text
        reply_text = response.get("response", {}).get("text", "I couldn't generate a response.")
        
        # Store in session history
        session_id = validated_data.session_id
        if session_id not in session_histories:
            session_histories[session_id] = []
        
        session_histories[session_id].append({
            "user": validated_data.message,
            "bot": reply_text
        })
        
        # Create and return response using dataclass
        chat_response = ChatResponse(
            session_id=session_id,
            reply=reply_text,
            status="success"
        )
        return chat_response.to_dict()
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "FAQ Chatbot",
        "manifest_file": os.environ.get("AGENT_MANIFEST_FILE"),
        "faq_count": get_faq_count()
    }


@app.get("/faq/search")
async def search_faq_endpoint(keyword: str):
    """Search FAQ by keyword"""
    if not keyword:
        raise HTTPException(status_code=400, detail="keyword parameter is required")
    
    results = search_faq(keyword)
    return {
        "keyword": keyword,
        "count": len(results),
        "results": results
    }


@app.get("/faq/all")
async def get_all_faq():
    """Get all FAQ items"""
    return {
        "count": get_faq_count(),
        "faq_items": get_faq_database()
    }


@app.get("/sessions/{session_id}")
async def get_session_history(session_id: str):
    """Get conversation history for a session"""
    if session_id not in session_histories:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session_id,
        "history": session_histories[session_id]
    }


@app.delete("/sessions/{session_id}")
async def clear_session(session_id: str):
    """Clear conversation history for a session"""
    if session_id in session_histories:
        del session_histories[session_id]
    
    return {"status": "cleared", "session_id": session_id}


def invoke_faq_agent(agent_name: str, user_text: str, session_id: str = None, sly_data=None) -> Dict[str, Any]:
    """
    Invoke a neuro-san FAQ agent and return its response.
    
    Args:
        agent_name: Name of the agent to invoke (without .hocon extension)
        user_text: The message to send to the agent
        session_id: Optional session identifier
        sly_data: Optional additional data to pass to the agent
    
    Returns:
        The final message from the agent containing the response
    """
    try:
        # Create the factory and session
        factory = DirectAgentSessionFactory()
        session = factory.create_session(
            agent_name=agent_name,
            use_direct=True,
            metadata={"session_id": session_id} if session_id else {},
        )

        # Prepare the request with FAQ context
        request_payload = {
            "user_message": {
                "text": user_text,
            }
        }
        
        # Add FAQ context to the request
        if FAQ_DATA:
            faq_context = format_faq_context(FAQ_DATA)
            request_payload["faq_context"] = faq_context
        
        if sly_data:
            request_payload["sly_data"] = sly_data

        # Stream the response and collect messages
        stream = session.streaming_chat(request_payload)
        msg = []
        for chat_msg in stream:
            msg.append(chat_msg)
            if chat_msg.get("done") is True:
                break
        
        # Return the last message (which contains the complete response)
        if msg:
            return msg[-1]
        else:
            return {"response": {"text": "No response generated"}}
    
    except Exception as e:
        print(f"Error invoking agent: {str(e)}")
        raise


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)