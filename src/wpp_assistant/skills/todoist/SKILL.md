---
name: todoist
description: >
  Todoist task and project management via MCP. Use this skill when the user
  asks about tasks, to-do items, projects, or anything related to their
  personal or shared task lists.
metadata:
  author: wpp-assistant
  version: "1.0"
---

# Todoist Task Management

You have access to the user's Todoist account through an MCP integration.
Use it to query, create, update, and complete tasks on behalf of the user.

## Rules

1. Never filter by assignee — no tasks are assigned to anyone.
2. Never set `startDate` on tasks — only use `dueString` for dates.
3. "My tasks" or "tasks to do" = unassigned tasks across all projects.
4. Shared/household tasks = the "Casa" project (the only shared project).
5. All other projects are personal.

See `references/` for detailed querying patterns and project conventions.
