# Gmail — Querying Patterns & Parameter Reference

## Available Actions

### gmail/fetch_emails

Retrieve a list of messages from the user's inbox.

| Parameter          | Type    | Required | Default | Description                                                          |
| :----------------- | :------ | :------- | :------ | :------------------------------------------------------------------- |
| `userId`           | string  | yes      | `"me"`  | The user's email address or `"me"` for the authenticated user.       |
| `q`                | string  | no       | —       | Gmail search query (e.g. `"from:boss@co.com is:unread"`).           |
| `maxResults`       | integer | no       | 100     | Max messages to return (1–500).                                      |
| `pageToken`        | string  | no       | —       | Page token for paginated results.                                    |
| `labelIds`         | array   | no       | —       | Only return messages matching all specified label IDs.               |
| `includeSpamTrash` | boolean | no       | false   | Include messages from SPAM and TRASH.                                |

**When to use:** The user asks to "check email", "see what's new", or wants a
filtered list (e.g. "unread emails from Alice").

### gmail/get_message

Retrieve a single message by its ID.

| Parameter         | Type   | Required | Default  | Description                                                         |
| :---------------- | :----- | :------- | :------- | :------------------------------------------------------------------ |
| `userId`          | string | yes      | `"me"`   | The user's email address or `"me"`.                                 |
| `id`              | string | yes      | —        | The message ID to retrieve.                                         |
| `format`          | string | no       | `"full"` | Return format: `"full"`, `"metadata"`, `"minimal"`, or `"raw"`.     |
| `metadataHeaders` | array  | no       | —        | When format is `"metadata"`, only include these headers.            |

**When to use:** After fetching a list with `fetch_emails`, the user asks to
"open" or "read" a specific email. Use the `id` from the list results.

### gmail/fetch_thread

Retrieve a full email thread (all messages in a conversation) by thread ID.

| Parameter         | Type   | Required | Default  | Description                                                     |
| :---------------- | :----- | :------- | :------- | :-------------------------------------------------------------- |
| `userId`          | string | yes      | `"me"`   | The user's email address or `"me"`.                             |
| `id`              | string | yes      | —        | The thread ID to retrieve.                                      |
| `format`          | string | no       | `"full"` | Return format: `"full"`, `"metadata"`, or `"minimal"`.          |
| `metadataHeaders` | array  | no       | —        | When format is `"metadata"`, only include these headers.        |

**When to use:** The user wants the full back-and-forth of a conversation, or
asks something like "show me the whole thread" or "what was the email chain
about X".

## Common Query Patterns

| User says                                    | Action                                                                |
| :------------------------------------------- | :-------------------------------------------------------------------- |
| "check my email" / "anything new?"           | `fetch_emails` with `q: "is:unread"` and a reasonable `maxResults`    |
| "emails from Alice"                          | `fetch_emails` with `q: "from:alice@example.com"`                     |
| "unread emails from this week"               | `fetch_emails` with `q: "is:unread newer_than:7d"`                    |
| "read that email" (after listing)            | `get_message` with the `id` from the previous fetch result            |
| "show the full thread"                       | `fetch_thread` with the `threadId` from the message                   |
| "emails about the project proposal"          | `fetch_emails` with `q: "subject:project proposal"`                   |
| "what did marketing send last month?"        | `fetch_emails` with `q: "from:marketing older_than:0d newer_than:30d"` |

## Gmail Search Query Syntax (for the `q` parameter)

- `from:user@example.com` — sender filter
- `to:user@example.com` — recipient filter
- `subject:keyword` — subject line filter
- `is:unread` / `is:read` — read status
- `is:starred` — starred messages
- `has:attachment` — messages with attachments
- `newer_than:Nd` / `older_than:Nd` — relative date (N = number of days)
- `after:YYYY/MM/DD` / `before:YYYY/MM/DD` — absolute date
- `label:LABEL_NAME` — label filter
- Combine with spaces (AND) or `OR` / `{ }` for OR logic

## Presentation Tips

- When listing emails, always include: **sender**, **subject**, and **date**.
- Keep summaries short — the user is reading on WhatsApp, not a desktop client.
- For threads, present messages in chronological order with clear sender labels.
- If a message body is long, summarize the key points rather than quoting it all.
- When the user asks vague questions ("any important emails?"), default to
  fetching unread messages and highlighting those from known contacts or with
  urgent-sounding subjects.
