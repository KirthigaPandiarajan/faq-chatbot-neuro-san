from fastapi import FastAPI
from neuro_san import AgenticNetwork  # Core class for local orchestration
from .tools import FAQSearchTool

app = FastAPI()

# Standard 2026 initialization
# Use register_tools to connect your custom Python logic to the HOCON agents
network = AgenticNetwork(
    hocon_path="config/network.hocon",
    custom_tools={"faq_search_tool": FAQSearchTool()}
)

@app.post("/chat")
async def chat(payload: dict):
    user_input = payload.get("message")
    context = payload.get("context", []) # semi-opaque chat history data

    # execute() is the standard method for running a turn in 2026
    # It returns a response object containing text and the new context
    response = await network.execute(user_input, chat_context=context)

    return {
        "reply": response.text,
        "context": response.chat_context  # This must be sent back in the next API call
    }
