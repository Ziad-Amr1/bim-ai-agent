# ai_server/simple-flask-server.py
from flask import Flask, jsonify, request
from command_writer import (
    write_count_walls,
    write_rename_views
)
import os
import json
import sys
from datetime import datetime

# ---------- helpers ----------

def log(msg):
    time = datetime.now().strftime("%H:%M:%S")
    print(f"[FLASK {time}] {msg}")
    sys.stdout.flush()

# ---------- app ----------

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT_FILE = os.path.join(BASE_DIR, "result.json")

log("🚀 Flask Server Initializing...")
log(f"📂 BASE_DIR = {BASE_DIR}")
log(f"📄 RESULT_FILE = {RESULT_FILE}")

# ---------- endpoints ----------

@app.route("/api/walls/count", methods=["GET"])
def api_count_walls():
    log("🧱 Endpoint HIT: /api/walls/count")

    try:
        success = write_count_walls()
        log(f"✍️ write_count_walls() → {success}")
        return jsonify({"command_written": success})
    except Exception as e:
        log(f"❌ Error in count walls: {e}")
        return jsonify({
            "command_written": False,
            "error": str(e)
        }), 500


@app.route("/api/views/rename", methods=["POST"])
def api_rename_views():
    log("✏️ Endpoint HIT: /api/views/rename")

    data = request.json or {}
    old_prefix = data.get("old_prefix")
    new_prefix = data.get("new_prefix")

    log(f"📥 Payload received: old='{old_prefix}', new='{new_prefix}'")

    try:
        success = write_rename_views(old_prefix, new_prefix)
        log(f"✍️ write_rename_views() → {success}")

        return jsonify({"command_written": success})
    except Exception as e:
        log(f"❌ Error in rename views: {e}")
        return jsonify({
            "command_written": False,
            "error": str(e)
        }), 500


@app.route("/api/result", methods=["GET"])
def api_get_result():
    log("📤 Endpoint HIT: /api/result")

    if not os.path.exists(RESULT_FILE):
        log("⏳ result.json not found → waiting for Revit")
        return jsonify({
            "status": "pending",
            "message": "Waiting for Revit execution"
        })

    try:
        with open(RESULT_FILE, "r") as f:
            result = json.load(f)

        log("✅ result.json loaded successfully")
        return jsonify(result)

    except Exception as e:
        log(f"❌ Error reading result.json: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ---------- run ----------

if __name__ == "__main__":
    log("🟢 Flask Server is RUNNING on http://localhost:5000")
    app.run(port=5000, debug=True)
