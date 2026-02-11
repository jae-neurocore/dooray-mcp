# dooray-mcp

MCP (Model Context Protocol) server for [NHN Dooray](https://dooray.com) project management.

Gives AI assistants like Claude direct access to your Dooray projects, tasks, comments, and more.

## Tools

| Tool | Description |
|---|---|
| `search_projects` | Search/list projects by code |
| `get_project` | Get project details by ID |
| `get_workflows` | Get workflow statuses for a project |
| `list_tasks` | List tasks with filters (workflow, tags, assignee, keyword) |
| `get_task` | Get a single task's full details |
| `create_task` | Create a task with subject, body, priority, assignees, tags, milestone, due date |
| `update_task` | Update task fields |
| `set_task_workflow` | Change a task's workflow status |
| `mark_task_done` | Mark a task as done |
| `list_comments` | List comments on a task |
| `add_comment` | Add a comment to a task |
| `update_comment` | Edit an existing comment |
| `delete_comment` | Remove a comment |
| `get_tags` | Get project tags |
| `get_milestones` | Get project milestones |
| `get_project_members` | Get project members |
| `find_task_by_number` | Find a task by project code + number (e.g. `APS/1689`) |

## Setup

### 1. Get a Dooray API token

Go to **Dooray → Settings → API** and generate a token.

### 2. Install

```bash
git clone https://github.com/your-username/dooray-mcp.git
cd dooray-mcp
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 3. Configure Claude Code

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "dooray": {
      "command": "/path/to/dooray-mcp/.venv/bin/dooray-mcp",
      "env": {
        "DOORAY_API_TOKEN": "your-token-here"
      }
    }
  }
}
```

Restart Claude Code and the Dooray tools will be available.

## Use case: commit → task linking

Git commits following the pattern `[#PROJECT/NUMBER] description` can be automatically resolved:

```
find_task_by_number(project_code="APS", task_number=1689)
```

This lets AI assistants parse commit history and update the corresponding Dooray tasks.

## License

MIT
