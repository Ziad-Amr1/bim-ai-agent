# ai_server/mcp_server.py
from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("BIM AI Agent")

FLASK_BASE_URL = "http://localhost:5000"


@mcp.tool()
def get_wall_count() -> str:
    """
    Ask Revit to count walls.
    """
    requests.get(f"{FLASK_BASE_URL}/api/walls/count")
    return "Counting walls in Revit..."


@mcp.tool()
def rename_views(old_prefix: str, new_prefix: str) -> str:
    """
    Rename Revit views.
    """
    requests.post(
        f"{FLASK_BASE_URL}/api/views/rename",
        json={
            "old_prefix": old_prefix,
            "new_prefix": new_prefix
        }
    )
    return f"Renaming views from {old_prefix} to {new_prefix}."


@mcp.tool()
def get_last_result() -> dict:
    """
    Get last result from Revit.
    """
    r = requests.get(f"{FLASK_BASE_URL}/api/result")
    return r.json()


if __name__ == "__main__":
    mcp.run()
