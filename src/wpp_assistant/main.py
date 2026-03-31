#!/usr/bin/env python
import os
import time

from arize.otel import register
from crewai.flow import Flow, listen, or_, router, start
from openinference.instrumentation.crewai import CrewAIInstrumentor
from openinference.instrumentation.openai import OpenAIInstrumentor

from wpp_assistant.crews import ReplyUnauthorizedUserCrew, ReplyUserCrew
from wpp_assistant.repositories import ConversationRepository
from wpp_assistant.types import Conversation, RunType, WppAssistantState
from wpp_assistant.utils import is_authorized_user

tracer_provider = register(
    space_id=os.getenv("ARIZE_SPACE_ID"),
    api_key=os.getenv("ARIZE_API_KEY"),
    project_name=os.getenv("ARIZE_PROJECT_NAME"),
)

CrewAIInstrumentor().instrument(tracer_provider=tracer_provider)
OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)


class WppAssistantFlow(Flow[WppAssistantState]):
    repo: ConversationRepository = None
    conversation: Conversation = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = ConversationRepository()

    @start()
    def initialize(self):
        return "Flow initialized"

    @router(initialize)
    def route_run_type(self):
        return self.state.run_type.value

    @listen(RunType.RESET_MEMORY.value)
    def reset_memory(self):
        self.repo.reset()

    @listen(RunType.DEFAULT.value)
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

    @listen(or_(reset_memory, reply_whitelisted_user, check_whitelisted_numbers))
    def consolidate_output(self):
        return self.state.model_dump()


def kickoff():
    WppAssistantFlow().kickoff(
        # OPTION 1: Sending a message to the assistant
        inputs={
            "messages": [
                {
                    "from": "558196448480",
                    "id": "wamid.test123",
                    "timestamp": str(int(time.time())),
                    "type": "text",
                    "text": {"body": "como vc se chama?"},
                }
            ]
        }
        # OPTION 2: Resetting the memory
        # inputs={"run_type": RunType.RESET_MEMORY.value}
    )


def plot():
    WppAssistantFlow().plot()


if __name__ == "__main__":
    kickoff()
