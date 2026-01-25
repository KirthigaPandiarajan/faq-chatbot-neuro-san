from fastapi import FastAPI
from pydantic import BaseModel
from neuro_san import GraphRunner

# Initialize app
app = FastAPI()

# Load Neuro-SAN graph once at startup
graph = GraphRunner.from_yaml("faq_network.yml")

# Request model
class ChatRequest(BaseModel):
    session_id: str
    message: str
    session_histories = {}
@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    history = session_histories.get(req.session_id, [])
    user_msg = req.message
    
    # Run through Neuro-SAN
    result = graph.run(input=user_msg, "history": history)
    # store new history
    session_histories[req.session_id] = history + [user_msg, result.get("output_text", "")]
    
    return {"reply": result.get("output_text", "")}