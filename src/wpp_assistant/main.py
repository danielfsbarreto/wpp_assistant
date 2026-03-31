#!/usr/bin/env python
import os

from arize.otel import register
from crewai.flow import Flow, listen, or_, router, start
from openinference.instrumentation.crewai import CrewAIInstrumentor

from wpp_assistant.crews import ReplyUnauthorizedUserCrew, ReplyUserCrew
from wpp_assistant.repositories import ConversationRepository
from wpp_assistant.types import Conversation, WppAssistantState
from wpp_assistant.utils import is_authorized_user

# Setup OTel and Arize exporter
tracer_provider = register(
    space_id=os.getenv("ARIZE_SPACE_ID"),
    api_key=os.getenv("ARIZE_API_KEY"),
    project_name=os.getenv("ARIZE_PROJECT_NAME"),
)

# Instrument CrewAI
CrewAIInstrumentor().instrument(
    tracer_provider=tracer_provider, use_event_listener=True
)


class WppAssistantFlow(Flow[WppAssistantState]):
    repo: ConversationRepository = None
    conversation: Conversation = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = ConversationRepository()

    @start()
    def load_messages(self):
        phone_number = self.state.messages[-1].from_
        self.conversation = self.repo.resolve_conversation(phone_number)
        self.repo.save_messages(self.conversation.id, self.state.messages)
        self.conversation = self.repo.get_conversation(self.conversation.id)

    @router(load_messages)
    def check_whitelisted_numbers(self):
        last_message = self.state.messages[-1]
        if not is_authorized_user(last_message.from_):
            ReplyUnauthorizedUserCrew(
                conversation=self.conversation,
                conversation_repo=self.repo,
            ).crew().kickoff(inputs={"conversation": self.conversation.model_dump()})
            return "UNAUTHORIZED"
        return "AUTHORIZED"

    @listen("AUTHORIZED")
    def reply_whitelisted_user(self):
        ReplyUserCrew(
            conversation=self.conversation,
            conversation_repo=self.repo,
        ).crew().kickoff(inputs={"conversation": self.conversation.model_dump()})

    @listen(or_(reply_whitelisted_user, check_whitelisted_numbers))
    def consolidate_output(self):
        return {"conversation_id": self.conversation.id}


def kickoff():
    WppAssistantFlow().kickoff(
        inputs={
            "messages": [
                {
                    "from": "558196448480",
                    "id": "wamid.test123",
                    "timestamp": "1774453258",
                    "type": "text",
                    "text": {"body": "Olá!"},
                }
            ],
        }
    )


def plot():
    WppAssistantFlow().plot()


if __name__ == "__main__":
    kickoff()
