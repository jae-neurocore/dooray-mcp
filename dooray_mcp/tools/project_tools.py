"""Project-related MCP tools."""

from __future__ import annotations

from typing import Any

from dooray_mcp import mcp
from dooray_mcp.http import _get


@mcp.tool()
async def search_projects(code: str | None = None, page: int = 0, size: int = 20) -> dict:
    """Search / list Dooray projects. Optionally filter by project code."""
    params: dict[str, Any] = {"page": page, "size": size}
    if code:
        params["code"] = code
    return await _get("/project/v1/projects", params)
