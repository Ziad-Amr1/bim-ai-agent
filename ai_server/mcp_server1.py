# ai_server/mcp_server.py
from mcp.server.fastmcp import FastMCP
import requests
import sys
from datetime import datetime

# ---------- helpers ----------

def log(msg):
    time = datetime.now().strftime("%H:%M:%S")
    print(f"[{time}] {msg}")
    sys.stdout.flush()  # مهم علشان الطباعة تظهر فورًا

# ---------- MCP ----------

mcp = FastMCP("BIM AI Agent")

FLASK_BASE_URL = "http://localhost:5000"

log("🚀 Starting BIM AI Agent MCP Server...")
log(f"🔗 Connected to Flask at {FLASK_BASE_URL}")

# ---------- TOOLS ----------

@mcp.tool()
def get_wall_count() -> str:
    """
    Ask Revit to count walls.
    """
    log("🧱 Tool called: get_wall_count")

    try:
        r = requests.get(f"{FLASK_BASE_URL}/api/walls/count")
        log(f"✅ Request sent, status = {r.status_code}")
    except Exception as e:
        log(f"❌ Error while counting walls: {e}")

    return "Counting walls in Revit..."


@mcp.tool()
def rename_views(old_prefix: str, new_prefix: str) -> str:
    """
    Rename Revit views.
    """
    log(f"✏️ Tool called: rename_views ({old_prefix} → {new_prefix})")

    try:
        r = requests.post(
            f"{FLASK_BASE_URL}/api/views/rename",
            json={
                "old_prefix": old_prefix,
                "new_prefix": new_prefix
            }
        )
        log(f"✅ Rename request sent, status = {r.status_code}")
    except Exception as e:
        log(f"❌ Error while renaming views: {e}")

    return f"Renaming views from {old_prefix} to {new_prefix}."


@mcp.tool()
def get_last_result() -> dict:
    """
    Get last result from Revit.
    """
    log("📥 Tool called: get_last_result")

    try:
        r = requests.get(f"{FLASK_BASE_URL}/api/result")
        log("✅ Result received from Revit")
        return r.json()
    except Exception as e:
        log(f"❌ Error getting result: {e}")
        return {"error": str(e)}

# ---------- RUN ----------

if __name__ == "__main__":
    log("🟢 MCP Server is now running and waiting for tools...")
    mcp.run()
