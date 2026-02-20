"""Task-related MCP tools."""

from __future__ import annotations

from typing import Any

from dooray_mcp import mcp
from dooray_mcp.http import _get, _post, _put


@mcp.tool()
async def list_tasks(
    project_id: str,
    page: int = 0,
    size: int = 20,
    workflow_ids: list[str] | None = None,
    tag_ids: list[str] | None = None,
    milestone_ids: list[str] | None = None,
    to_member_ids: list[str] | None = None,
    keyword: str | None = None,
    order: str = "-createdAt",
) -> dict:
    """List tasks (posts) in a project with optional filters."""
    params: dict[str, Any] = {"page": page, "size": size, "order": order}
    if workflow_ids:
        params["workflowIds"] = ",".join(workflow_ids)
    if tag_ids:
        params["tagIds"] = ",".join(tag_ids)
    if milestone_ids:
        params["milestoneIds"] = ",".join(milestone_ids)
    if to_member_ids:
        params["toMemberIds"] = ",".join(to_member_ids)
    if keyword:
        params["keyword"] = keyword
    return await _get(f"/project/v1/projects/{project_id}/posts", params)


@mcp.tool()
async def get_task(project_id: str, task_id: str) -> dict:
    """Get a single task's full details."""
    return await _get(f"/project/v1/projects/{project_id}/posts/{task_id}")


@mcp.tool()
async def create_task(
    project_id: str,
    subject: str,
    body_content: str = "",
    body_mime_type: str = "text/x-markdown",
    priority: str | None = None,
    to_member_ids: list[str] | None = None,
    tag_ids: list[str] | None = None,
    milestone_id: str | None = None,
    due_date: str | None = None,
) -> dict:
    """Create a new task (post) in a project.

    Args:
        project_id: The project to create the task in.
        subject: Task title / subject line.
        body_content: Task description (markdown by default).
        body_mime_type: MIME type of the body ("text/x-markdown" or "text/html").
        priority: Priority string (e.g. "none", "low", "normal", "high", "urgent").
        to_member_ids: List of member IDs to assign.
        tag_ids: List of tag IDs to attach.
        milestone_id: Milestone ID to associate.
        due_date: Due date in ISO-8601 format (e.g. "2025-12-31T23:59:59+09:00").
    """
    payload: dict[str, Any] = {
        "subject": subject,
        "body": {"mimeType": body_mime_type, "content": body_content},
    }
    if priority:
        payload["priority"] = priority
    if to_member_ids:
        payload["toMemberIds"] = to_member_ids
    if tag_ids:
        payload["tagIds"] = tag_ids
    if milestone_id:
        payload["milestoneId"] = milestone_id
    if due_date:
        payload["dueDateFlag"] = True
        payload["dueDate"] = due_date
    return await _post(f"/project/v1/projects/{project_id}/posts", payload)


@mcp.tool()
async def update_task(
    project_id: str,
    task_id: str,
    subject: str | None = None,
    body_content: str | None = None,
    body_mime_type: str = "text/x-markdown",
    priority: str | None = None,
    due_date: str | None = None,
) -> dict:
    """Update an existing task's fields. Only supplied fields are changed."""
    payload: dict[str, Any] = {}
    if subject is not None:
        payload["subject"] = subject
    if body_content is not None:
        payload["body"] = {"mimeType": body_mime_type, "content": body_content}
    if priority is not None:
        payload["priority"] = priority
    if due_date is not None:
        payload["dueDateFlag"] = True
        payload["dueDate"] = due_date
    if not payload:
        return {"message": "No fields to update"}
    return await _put(f"/project/v1/projects/{project_id}/posts/{task_id}", payload)


@mcp.tool()
async def set_task_workflow(project_id: str, task_id: str, workflow_id: str) -> dict:
    """Change a task's workflow status."""
    return await _put(
        f"/project/v1/projects/{project_id}/posts/{task_id}/set-workflow",
        {"workflowId": workflow_id},
    )


@mcp.tool()
async def mark_task_done(project_id: str, task_id: str) -> dict:
    """Mark a task as done."""
    return await _put(f"/project/v1/projects/{project_id}/posts/{task_id}/set-done")


@mcp.tool()
async def find_task_by_number(project_code: str, task_number: int) -> dict:
    """Find a task by its display number within a project.

    Useful for resolving references like [#APS/1689] from commit messages.
    First resolves the project by code, then searches for the task number.

    Args:
        project_code: The project code (e.g. "APS").
        task_number: The task display number (e.g. 1689).
    """
    # Step 1: find the project by code
    projects = await _get("/project/v1/projects", {"code": project_code})
    if not projects:
        return {"error": f"No project found with code '{project_code}'"}

    # projects may be a list or wrapped
    project_list = projects if isinstance(projects, list) else [projects]
    project = None
    for p in project_list:
        if p.get("code", "").upper() == project_code.upper():
            project = p
            break
    if project is None:
        project = project_list[0]

    project_id = project["id"]

    # Step 2: search for the task by number
    tasks = await _get(
        f"/project/v1/projects/{project_id}/posts",
        {"postNumber": task_number},
    )

    if isinstance(tasks, list):
        for t in tasks:
            if t.get("number") == task_number:
                return t
        if tasks:
            return tasks[0]

    return tasks or {"error": f"Task #{task_number} not found in project {project_code}"}
