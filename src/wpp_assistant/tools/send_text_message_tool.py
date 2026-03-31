import os
import time
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from wpp_assistant.clients import WhatsappMessenger
from wpp_assistant.repositories import ConversationRepository
from wpp_assistant.types import Conversation, PhoneNumber, TextBody, TextMessage


class SendTextMessageToolInput(BaseModel):
    to: PhoneNumber = Field(..., description="The phone number to send the message to")
    content: str = Field(..., description="The message content to send the user")


class SendTextMessageTool(BaseTool):
    name: str = "SendTextMessageTool"
    description: str = "Send a text message to the user via WhatsApp"
    client: WhatsappMessenger = None
    conversation: Conversation = None
    conversation_repo: ConversationRepository = None
    args_schema: Type[BaseModel] = SendTextMessageToolInput

    def __init__(
        self,
        conversation: Conversation,
        conversation_repo: ConversationRepository,
    ):
        super().__init__(
            client=WhatsappMessenger(),
            conversation=conversation,
            conversation_repo=conversation_repo,
        )

    def _run(self, to: PhoneNumber, content: str) -> dict:
        message = TextMessage(
            from_=os.getenv("WHATSAPP_BOT_PHONE_NUMBER"),
            timestamp=str(int(time.time())),
            type="text",
            text=TextBody(body=content),
        )

        if os.getenv("DEV_MODE") == "true":
            self.conversation_repo.save_messages(self.conversation.id, [message])
            self.conversation.messages.append(message)
            return message.model_dump()

        response = self.client.send_text_message(to, content)
        message.id = response.get("messages", [{}])[0].get("id", "")
        self.conversation_repo.save_messages(self.conversation.id, [message])
        self.conversation.messages.append(message)
        return message.model_dump()
