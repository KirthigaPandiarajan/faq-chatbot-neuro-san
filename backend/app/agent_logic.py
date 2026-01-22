from neuro_san import AgenticNetwork
from tools import FAQSearchTool

class FAQBotManager:
    def __init__(self, hocon_path: str):
        # Register the custom CodedTool before loading the network
        self.network = AgenticNetwork.from_hocon(
            hocon_path,
            custom_tools={"faq_search_tool": FAQSearchTool()}
        )

    async def get_response(self, user_message: str, context: list = None):
        # execute handles the agent-to-agent delegation defined in HOCON
        result = await self.network.async_execute(
            input_text=user_message,
            context=context or []
        )
        return {
            "reply": result.text,
            "context": result.updated_context # Essential for multi-turn history
        }
