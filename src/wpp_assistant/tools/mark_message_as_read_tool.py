import os

from crewai.tools import BaseTool

from wpp_assistant.clients import WhatsappMessenger
from wpp_assistant.types import Conversation


class MarkMessageAsReadTool(BaseTool):
    name: str = "MarkMessageAsReadTool"
    description: str = (
        "Mark the latest message in the conversation as read and show a typing "
        "indicator. Call this before composing each reply — no arguments needed."
    )
    client: WhatsappMessenger = None
    conversation: Conversation = None

    def __init__(self, conversation: Conversation):
        super().__init__(client=WhatsappMessenger(), conversation=conversation)

    def _run(self, **kwargs) -> dict:
        message_id = self.conversation.messages[-1].id

        if os.getenv("DEV_MODE") == "true":
            return {"status": "read", "message_id": message_id}

        return self.client.mark_as_read(message_id)
