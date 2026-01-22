from fastapi import FastAPI
from neuro_san import DirectAgentSession  # The correct 2026 class
from tools import FAQSearchTool

app = FastAPI()

# Initialize the session by pointing to your HOCON and registering tools
session = DirectAgentSession(
    agent_config_path="config/network.hocon",
    custom_tools={"faq_search_tool": FAQSearchTool()}
)

@app.post("/chat")
async def chat(payload: dict):
    user_input = payload.get("message")
    context = payload.get("context", [])

    # In 2026, use 'chat' which returns a ChatResponse object
    # This automatically handles the AAOSA protocol delegation
    response = await session.chat(user_input, context=context)

    return {
        "reply": response.text,
        "context": response.updated_context
    }
