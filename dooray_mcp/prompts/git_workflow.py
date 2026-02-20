"""MCP prompt for updating Dooray issues from git commits."""

from dooray_mcp import mcp


@mcp.prompt()
def update_issues_from_commits(
    author: str = "jaeyoung.heo",
    commit_count: int = 10,
) -> str:
    """Update Dooray issues with details from recent git commits."""
    return f"""\
Follow these steps to update Dooray issues from recent git commits:

## 1. Find commits with issue references

Run this command:
```
git log --author="{author}" --oneline -{commit_count}
```

- Only process commits by **{author}**
- Parse `[#PROJECT/NUMBER]` or `[PROJECT/NUMBER]` patterns from commit messages
- Group commits by issue number (multiple commits may reference the same issue)

## 2. Understand the code changes

For each commit:
- Read the **actual diff**: `git diff HASH^..HASH`
- Read the **source files** that were changed to understand context
- Do NOT just summarize the commit message — analyze the real code changes

## 3. Find the Dooray issue

- Use `find_task_by_number` with the project code and task number
- If that returns wrong results, use `list_tasks` with keyword search
- Common project codes: APS, A.I.-RL

## 4. Update the issue body

- Use `update_task` to set the body content
- Write in **Korean** (matching team convention)
- Format in markdown with:
  - `## 변경 내용` — one-line summary of what changed and why
  - Subsections per major change area (file or feature)
  - Explain the **what** and **why**, not just list files
  - Reference actual class names, method names, and technical details from the code
  - `### 커밋` — list all related commit hashes with messages at the bottom
"""
