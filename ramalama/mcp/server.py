from datetime import datetime

from fastmcp import FastMCP

mcp = FastMCP("Time MCP Server")


@mcp.tool()
def current_time() -> datetime:
    """Get current time"""
    return datetime.now()
