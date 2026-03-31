---
name: gmail
description: >
  Gmail email reading capabilities. Use this skill when the user asks about
  emails, wants to check their inbox, read a specific message, or review an
  email thread.
metadata:
  author: wpp-assistant
  version: "1.0"
---

# Gmail Email Access

You have read access to the user's Gmail account through the CrewAI platform
integration. Use it to fetch emails, read individual messages, and retrieve
full conversation threads.

## Rules

1. Only fetch what the user asks for — don't over-read their inbox.
2. Summarize email content concisely; don't dump raw payloads.
3. When listing emails, include sender, subject, and date at minimum.
4. For threads, present messages in chronological order.

See `references/` for detailed parameter usage and querying patterns.
