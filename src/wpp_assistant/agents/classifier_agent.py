from crewai import Agent, Crew, Process, Task

from wpp_assistant.types import Capability, ClassifyResponse, Conversation


class ClassifierAgent:
    def classify(self, conversation: Conversation) -> set[Capability]:
        agent = Agent(
            role="Capability Classifier",
            goal=(
                "Determine which capabilities are needed to handle a WhatsApp message. "
                "Return ONLY the ones that are required.\n\n"
                "Available capabilities:\n"
                "- web_search: Web search and website scraping. Use when the user asks "
                "to look something up online or needs real-time information.\n"
                "- history: Extended conversation history retrieval. Use when the user "
                "references past conversations from previous days.\n"
                "- gmail: Email access — fetching inbox messages, reading specific "
                "emails, and retrieving full email threads. Use when the user asks "
                "about emails.\n"
                "- todoist: Task and project management — querying, creating, updating, "
                "and completing tasks. Use when the user asks about tasks, to-dos, or "
                "projects.\n\n"
                "If the message is casual chat, a greeting, or a simple question "
                "answerable from general knowledge, return an empty list."
            ),
            backstory=(
                "You are a routing classifier that inspects incoming WhatsApp "
                "messages and decides which system capabilities are required to "
                "fulfill the request. You never answer the user directly — you "
                "only output the list of capabilities needed."
            ),
            llm="gpt-5.4-mini",
            verbose=True,
        )
        task = Task(
            description="Classify the capabilities needed for this conversation: {conversation}",
            expected_output="A JSON object with a 'capabilities' list.",
            agent=agent,
            output_pydantic=ClassifyResponse,
        )
        result = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True,
        ).kickoff(inputs={"conversation": conversation.model_dump()})
        return set(result.pydantic.capabilities)
