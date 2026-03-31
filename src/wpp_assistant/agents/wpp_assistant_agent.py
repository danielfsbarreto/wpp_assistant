import os
from pathlib import Path
from typing import Any

import yaml
from crewai import Agent
from crewai.mcp import MCPServerHTTP
from crewai_tools import SerperDevTool, SerperScrapeWebsiteTool

from wpp_assistant.repositories import ConversationRepository
from wpp_assistant.tools import (
    FetchDayMessagesTool,
    MarkMessageAsReadTool,
    SendTextMessageTool,
)
from wpp_assistant.types import Conversation

SKILLS_DIR = Path(__file__).parent.parent / "skills"


class WppAssistantAgent:
    @classmethod
    def __create(
        cls,
        conversation: Conversation,
        conversation_repo: ConversationRepository,
        *,
        extra_tools: list[Any] | None = None,
        apps: list[str] | None = None,
        mcps: list[Any] | None = None,
        skills: list[Path] | None = None,
    ) -> Agent:
        config_path = Path(__file__).parent / "config" / "agents.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)["wpp_assistant"]

        return Agent(
            **config,
            tools=[
                MarkMessageAsReadTool(conversation=conversation),
                SendTextMessageTool(
                    conversation=conversation,
                    conversation_repo=conversation_repo,
                ),
                *(extra_tools or []),
            ],
            apps=apps or [],
            mcps=mcps or [],
            skills=skills or [],
            inject_date=True,
        )

    @classmethod
    def full(
        cls,
        conversation: Conversation,
        conversation_repo: ConversationRepository,
    ) -> Agent:
        return cls.__create(
            conversation,
            conversation_repo,
            extra_tools=[
                SerperDevTool(),
                SerperScrapeWebsiteTool(),
                FetchDayMessagesTool(
                    conversation_repo=conversation_repo,
                ),
            ],
            apps=[
                "gmail/fetch_emails",
                "gmail/get_message",
                "gmail/fetch_thread",
            ],
            mcps=[
                MCPServerHTTP(
                    url="https://ai.todoist.net/mcp",
                    headers={
                        "Authorization": f"Bearer {os.getenv('TODOIST_API_KEY')}",
                    },
                )
            ],
            skills=[SKILLS_DIR],
        )

    @classmethod
    def minimal(
        cls,
        conversation: Conversation,
        conversation_repo: ConversationRepository,
    ) -> Agent:
        return cls.__create(
            conversation,
            conversation_repo,
            skills=[SKILLS_DIR / "whatsapp-messaging"],
        )
