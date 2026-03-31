# Todoist — Querying Patterns & Conventions

## Projects

- Most projects are personal and not shared with anyone.
- The only shared project is called "Casa" — use it for household/shared tasks.

## Task Assignment

- No tasks in any project are assigned to anyone, including the "Casa" project.
- Always filter tasks without any assignee filter — never filter by assignee.

## Common Queries

| User says                          | What to do                                          |
| :--------------------------------- | :-------------------------------------------------- |
| "my tasks" / "tasks to do"         | Unassigned tasks across all projects                |
| "shared tasks" / "household tasks" | Tasks in the "Casa" project                         |
| "what's due today"                 | Use `find-tasks-by-date` with startDate = 'today'   |
| "completed tasks"                  | Use `find-completed-tasks` (defaults to last 7 days) |

## Key MCP Tools

- **find-tasks**: Search by text, project, section, labels, or filter string.
- **find-tasks-by-date**: Get tasks by date range or specific day counts.
- **find-completed-tasks**: View completed tasks by completion or due date.
- **get-overview**: Comprehensive view of entire account or a specific project.
- **add-tasks**: Create tasks (max 25 per call) with content, priority, dueString.
- **complete-tasks**: Mark tasks as done by task ID.
- **update-tasks**: Modify existing tasks (get IDs from search first).
- **reschedule-tasks**: Move task due dates (preserves recurrence patterns).
