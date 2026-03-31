from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from wpp_assistant.repositories import ConversationRepository
from wpp_assistant.types import PhoneNumber


class FetchDayMessagesToolInput(BaseModel):
    phone_number: PhoneNumber = Field(
        ..., description="The phone number to fetch messages for"
    )
    date: str = Field(
        ..., description="The date to fetch messages for, in YYYY-MM-DD format"
    )


class FetchDayMessagesTool(BaseTool):
    name: str = "FetchDayMessagesTool"
    description: str = (
        "Fetch the WhatsApp conversation history for a specific phone number on a "
        "given day. Use this to retrieve past conversation context when the user "
        "references something from a previous day."
    )
    conversation_repo: ConversationRepository = None
    args_schema: Type[BaseModel] = FetchDayMessagesToolInput

    def __init__(self, conversation_repo: ConversationRepository):
        super().__init__(conversation_repo=conversation_repo)

    def _run(self, phone_number: PhoneNumber, date: str) -> list[dict]:
        messages = self.conversation_repo.get_messages_by_date(phone_number, date)
        return [msg.model_dump() for msg in messages]
