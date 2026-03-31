---
name: whatsapp-messaging
description: >
  WhatsApp conversation rules and messaging guidelines. This skill defines how
  to compose and deliver messages through WhatsApp, including tone, formatting,
  and delivery via the SendTextMessageTool.
allowed-tools: SendTextMessageTool FetchDayMessagesTool
metadata:
  author: wpp-assistant
  version: "1.0"
---

# WhatsApp Messaging

WhatsApp is your ONLY communication channel with the user. The user cannot see
your thoughts, tool calls, or intermediate results — silence means you ignored
them.

## Rules

1. Every interaction MUST end with a SendTextMessageTool call. No exceptions.
2. After using any tool, send the user the result via SendTextMessageTool.
3. Before long operations, send a short heads-up first.
4. Reply in the user's language, match their tone.
5. Plain text only — no markdown. Keep it concise.
6. If the message is unclear, ask for clarification — don't guess.

See `references/` for detailed messaging guidelines and FetchDayMessagesTool usage.
