---
name: todoist
description: >
  Todoist task and project management via MCP. Use this skill when the user
  asks about tasks, to-do items, projects, or anything related to their
  personal or shared task lists.
allowed-tools: find-tasks find-tasks-by-date find-completed-tasks find-projects find-sections find-comments find-labels find-filters find-activity find-project-collaborators get-overview get-productivity-stats user-info list-workspaces view-attachment fetch-object fetch search
metadata:
  author: wpp-assistant
  version: "1.0"
---

# Todoist Task Management

You have access to the user's Todoist account through an MCP integration.
Use it to query, create, update, and complete tasks on behalf of the user.

## Projects

- Most projects are personal and not shared with anyone.
- The only shared project is called "Casa".

## Task Assignment

- No tasks in any project are assigned to anyone, including the "Casa" project.
- Always filter tasks without any assignee filter — never filter by assignee.

## Querying Tasks

- When the user asks about "my tasks" or "tasks to do", assume they are asking
  about unassigned tasks across all projects.
- When the user asks about shared tasks or household tasks, focus on the "Casa"
  project.
