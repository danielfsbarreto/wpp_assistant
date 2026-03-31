# WhatsApp Assistant

A crewAI Flow that acts as a conversational WhatsApp assistant. It receives incoming messages, routes them based on authorization, and replies using AI agents with access to web search, Todoist, and other tools.

## Setup

Requires Python >=3.10 <3.14 and [UV](https://docs.astral.sh/uv/).

```bash
crewai install
```

Copy `.env.example` to `.env` and fill in the values:

| Variable | Purpose |
|----------|---------|
| `AUTHORIZED_NUMBERS` | Comma-separated phone numbers allowed to interact |
| `OPENAI_API_KEY` | LLM provider |
| `SERPER_API_KEY` | Web search via SerperDev |
| `TODOIST_API_KEY` | Todoist integration (MCP) |
| `WHATSAPP_MESSENGER_URL` | WhatsApp Cloud API endpoint |
| `WHATSAPP_MESSENGER_TOKEN` | WhatsApp Cloud API token |

Set `DEV_MODE=true` to skip actual WhatsApp API calls during development.

## Running

```bash
crewai run        # run the flow
crewai flow plot  # visualize the flow graph
```

## How it works

```
Incoming message
      │
      ▼
 load_messages ──► check_whitelisted_numbers
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
         AUTHORIZED          UNAUTHORIZED
              │                   │
              ▼                   ▼
     ReplyAuthorizedUserCrew  ReplyUnauthorizedUserCrew
              │                   │
              └─────────┬─────────┘
                        ▼
               consolidate_output
```

1. **load_messages** — appends incoming messages to the persisted conversation.
2. **check_whitelisted_numbers** — routes based on whether the sender is in `AUTHORIZED_NUMBERS`.
3. **ReplyAuthorizedUserCrew** — full agent with web search, Todoist, and scraping tools. Replies conversationally.
4. **ReplyUnauthorizedUserCrew** — minimal agent that politely declines.
5. **consolidate_output** — returns the updated conversation state.

State is persisted across invocations via `@persist()`, so the agent maintains conversation history.

## Project structure

```
src/wpp_assistant/
├── main.py                        # Flow definition & entrypoints
├── agents/                        # Agent factory + config
│   ├── wpp_assistant_agent.py
│   └── config/agents.yaml
├── crews/                         # Crew definitions
│   ├── reply_authorized_user_crew/
│   └── reply_unauthorized_user_crew/
├── tools/                         # Custom tools
│   └── send_text_message_tool.py
├── types/                         # Pydantic models
│   ├── whatsapp_message.py
│   ├── text_message.py
│   ├── conversation.py
│   └── wpp_assistant_state.py
├── clients/                       # External API clients
└── utils/                         # Helpers (auth check, etc.)
```
