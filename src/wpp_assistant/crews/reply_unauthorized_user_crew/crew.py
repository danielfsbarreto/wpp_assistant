from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from wpp_assistant.agents import WppAssistantAgent
from wpp_assistant.repositories import ConversationRepository
from wpp_assistant.types import Conversation


@CrewBase
class ReplyUnauthorizedUserCrew:
    agents: List[BaseAgent]
    tasks: List[Task]

    tasks_config = "config/tasks.yaml"

    def __init__(
        self,
        conversation: Conversation,
        conversation_repo: ConversationRepository,
    ):
        self.conversation = conversation
        self.conversation_repo = conversation_repo

    @agent
    def wpp_assistant(self) -> Agent:
        return WppAssistantAgent(
            self.conversation,
            self.conversation_repo,
        ).build()

    @task
    def reply_user(self) -> Task:
        return Task(
            config=self.tasks_config["reply_user"],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
