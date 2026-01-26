import os
import warnings
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from marshmallow import Schema, fields, ValidationError
from typing import Optional, Dict, Any, List
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

# Global FAQ data storage
FAQ_DATA: List[Dict[str, Any]] = []

# Define request/response schemas using marshmallow
class ChatRequestSchema(Schema):
    """Schema for chat request validation"""
    session_id = fields.Str(required=True, error_messages={"required": "session_id is required"})
    message = fields.Str(required=True, error_messages={"required": "message is required"})


class ChatResponseSchema(Schema):
    """Schema for chat response"""
    session_id = fields.Str()
    reply = fields.Str()
    status = fields.Str()


# Initialize schemas
chat_request_schema = ChatRequestSchema()
chat_response_schema = ChatResponseSchema()


def load_faq_data() -> List[Dict[str, Any]]:
    """Load FAQ data from JSON file"""
    try:
        # Try multiple possible paths
        possible_paths = [
            Path("./data/faq.json"),
            Path("./backend/data/faq.json"),
            Path("data/faq.json"),
        ]
        
        for faq_path in possible_paths:
            if faq_path.exists():
                with open(faq_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"✓ Loaded {len(data)} FAQ items from {faq_path}")
                    return data
        
        print("⚠️ Warning: FAQ file not found at expected paths")
        return []
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
    
    print(f"✓ FAQ Chatbot API initialized")
    print(f"✓ Manifest file: {os.environ.get('AGENT_MANIFEST_FILE')}")
    print(f"✓ FAQ database: {len(FAQ_DATA)} items loaded")


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
        
        # Validate request using marshmallow
        validated_data = chat_request_schema.load(req_data)
        
        # Invoke the agent with DirectAgentSessionFactory
        response = invoke_faq_agent(
            agent_name="faq_agent",
            user_text=validated_data["message"],
            session_id=validated_data["session_id"]
        )
        
        # Extract the response text
        reply_text = response.get("response", {}).get("text", "I couldn't generate a response.")
        
        # Store in session history
        session_id = validated_data["session_id"]
        if session_id not in session_histories:
            session_histories[session_id] = []
        
        session_histories[session_id].append({
            "user": validated_data["message"],
            "bot": reply_text
        })
        
        # Create response data
        response_data = {
            "session_id": session_id,
            "reply": reply_text,
            "status": "success"
        }
        
        # Validate and return response
        validated_response = chat_response_schema.dump(response_data)
        return validated_response
    
    except ValidationError as e:
        print(f"Validation error: {e.messages}")
        raise HTTPException(status_code=400, detail=e.messages)
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