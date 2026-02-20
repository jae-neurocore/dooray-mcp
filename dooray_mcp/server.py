"""Dooray MCP Server — minimal entry point."""

from dooray_mcp import mcp  # noqa: F401 — shared FastMCP instance
from dooray_mcp import prompts, tools  # noqa: F401 — register decorators


def main():
    mcp.run()


if __name__ == "__main__":
    main()
