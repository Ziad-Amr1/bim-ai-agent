from mcp.server.fastmcp import FastMCP
import requests
import sys

mcp = FastMCP("BIM AI Agent v3")

FLASK_BASE_URL = "http://localhost:5000"

# ================ PING =================
 
@mcp.tool()
def ping() -> str:
    """
    Check if MCP server is alive.
    """
    return "🟢 MCP is running and ready."


# ================= READ =================

@mcp.tool()
def get_wall_count() -> str:
    requests.get(f"{FLASK_BASE_URL}/api/walls/count")
    return "Wall count command sent to Revit."


@mcp.tool()
def ai_suggestions() -> str:
    """
    Ask Revit to analyze the model and return AI suggestions.
    """
    requests.post(
        f"{FLASK_BASE_URL}/api/command",
        json={"action": "ai_suggestions"}
    )
    return (
        "AI suggestions request sent to Revit.\n"
        "Please click the AI_Bridge button in Revit to execute."
    )


# ================= MODIFY =================

@mcp.tool()
def rename_views(old_prefix: str, new_prefix: str) -> str:
    requests.post(
        f"{FLASK_BASE_URL}/api/views/rename",
        json={
            "old_prefix": old_prefix,
            "new_prefix": new_prefix
        }
    )
    return f"Rename views command sent ({old_prefix} → {new_prefix})."


@mcp.tool()
def flip_doors() -> str:
    requests.post(f"{FLASK_BASE_URL}/api/doors/flip")
    return (
        "Flip doors command sent to Revit.\n"
        "Please click the AI_Bridge button in Revit to execute."
    )


@mcp.tool()
def modify_parameter(element_id: int, parameter: str, value) -> str:
    requests.post(
        f"{FLASK_BASE_URL}/api/command",
        json={
            "action": "modify_parameter",
            "element_id": element_id,
            "parameter": parameter,
            "value": value
        }
    )
    return (
        f"Modify parameter command sent (Element {element_id}).\n"
        "Please click the AI_Bridge button in Revit to execute."
    )


# ================= ADMIN =================

@mcp.tool()
def revert_last() -> str:
    requests.post(
        f"{FLASK_BASE_URL}/api/command",
        json={"action": "revert_last"}
    )
    return (
        "Revert last operation command sent to Revit.\n"
        "Please click the AI_Bridge button in Revit to execute."
    )


# ================= RESULT =================

@mcp.tool()
def get_last_result() -> dict:
    r = requests.get(f"{FLASK_BASE_URL}/api/result")
    return r.json()


if __name__ == "__main__":
    print("MCP server started", file=sys.stderr)
    mcp.run()
