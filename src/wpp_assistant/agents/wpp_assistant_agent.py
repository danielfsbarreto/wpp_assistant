from __future__ import annotations

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
from wpp_assistant.types import Capability, Conversation

SKILLS_DIR = Path(__file__).parent.parent / "skills"


class WppAssistantAgent:
    def __init__(
        self,
        conversation: Conversation,
        conversation_repo: ConversationRepository,
    ) -> None:
        self._conversation = conversation
        self._conversation_repo = conversation_repo

        config_path = Path(__file__).parent / "config" / "agents.yaml"
        with open(config_path) as f:
            self._config = yaml.safe_load(f)["wpp_assistant"]

        self._tools: list[Any] = [
            MarkMessageAsReadTool(conversation=conversation),
            SendTextMessageTool(
                conversation=conversation,
                conversation_repo=conversation_repo,
            ),
        ]
        self._apps: list[str] = []
        self._mcps: list[Any] = []
        self._skills: list[Path] = [SKILLS_DIR / "whatsapp-messaging"]

    def with_web_search_support(self) -> WppAssistantAgent:
        self._tools.extend(
            [
                SerperDevTool(),
                SerperScrapeWebsiteTool(),
            ]
        )
        self._skills.extend([SKILLS_DIR / "web-search"])
        return self

    def with_history_support(self) -> WppAssistantAgent:
        self._tools.extend(
            [
                FetchDayMessagesTool(conversation_repo=self._conversation_repo),
            ]
        )
        return self

    def with_gmail_support(self) -> WppAssistantAgent:
        self._apps.extend(
            [
                "gmail/fetch_emails",
                "gmail/get_message",
                "gmail/fetch_thread",
            ]
        )
        self._skills.extend([SKILLS_DIR / "gmail"])
        return self

    def with_todoist_support(self) -> WppAssistantAgent:
        self._mcps.extend(
            [
                MCPServerHTTP(
                    url="https://ai.todoist.net/mcp",
                    headers={
                        "Authorization": f"Bearer {os.getenv('TODOIST_API_KEY')}",
                    },
                )
            ]
        )
        self._skills.extend([SKILLS_DIR / "todoist"])
        return self

    def with_capabilities(self, capabilities: set[Capability]) -> WppAssistantAgent:
        capability_map = {
            Capability.WEB_SEARCH: self.with_web_search_support,
            Capability.HISTORY: self.with_history_support,
            Capability.GMAIL: self.with_gmail_support,
            Capability.TODOIST: self.with_todoist_support,
        }
        for cap in capabilities:
            capability_map[cap]()
        return self

    def build(self) -> Agent:
        return Agent(
            **self._config,
            tools=self._tools,
            apps=self._apps,
            mcps=self._mcps,
            skills=self._skills,
            inject_date=True,
        )
