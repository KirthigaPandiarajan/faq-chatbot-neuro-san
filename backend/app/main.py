import os
import warnings
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json
from pathlib import Path

# Suppress coroutine warnings for cleaner output
warnings.filterwarnings('ignore', category=RuntimeWarning)

# Import neuro-san components
from neuro_san.client.agent_session_factory import DirectAgentSessionFactory

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

# Request/Response models
class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    status: str = "success"


# Initialize agent at startup
@app.on_event("startup")
async def startup_event():
    """Initialize the FAQ agent and verify manifest path"""
    # Set the manifest location if not already set
    if "AGENT_MANIFEST_FILE" not in os.environ:
        os.environ["AGENT_MANIFEST_FILE"] = "./registries/manifest.hocon"
    print(f"✓ FAQ Chatbot API initialized")
    print(f"✓ Manifest file: {os.environ.get('AGENT_MANIFEST_FILE')}")


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest) -> ChatResponse:
    """
    Main chat endpoint that invokes the FAQ agent
    
    Args:
        req: ChatRequest with session_id and message
    
    Returns:
        ChatResponse with the agent's reply
    """
    try:
        # Invoke the agent with DirectAgentSessionFactory
        response = invoke_faq_agent(
            agent_name="faq_agent",
            user_text=req.message,
            session_id=req.session_id
        )
        
        # Extract the response text
        reply_text = response.get("response", {}).get("text", "I couldn't generate a response.")
        
        # Store in session history
        if req.session_id not in session_histories:
            session_histories[req.session_id] = []
        
        session_histories[req.session_id].append({
            "user": req.message,
            "bot": reply_text
        })
        
        return ChatResponse(
            session_id=req.session_id,
            reply=reply_text,
            status="success"
        )
    
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "FAQ Chatbot",
        "manifest_file": os.environ.get("AGENT_MANIFEST_FILE")
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