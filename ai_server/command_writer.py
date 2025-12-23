# ai_server/command_writer.py

import json
import os
import time
from datetime import datetime
import sys

# =====================================================
# Paths
# =====================================================

# ROOT PROJECT DIR (one level above ai_server)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMAND_FILE = os.path.join(BASE_DIR, "command.json")

# =====================================================
# Helpers
# =====================================================

def log(msg):
    t = datetime.now().strftime("%H:%M:%S")
    print(f"[WRITER {t}] {msg}")
    sys.stdout.flush()


# =====================================================
# Core Writer
# =====================================================

def write_command(command):
    """
    Safely write command.json for Revit AI Bridge (atomic write).
    Returns True if written, False otherwise.
    """

    if not isinstance(command, dict):
        log("❌ Command must be a dictionary")
        return False

    action = command.get("action")
    if not action:
        log("❌ Missing 'action' in command")
        return False

    # Prevent overwriting active command
    if os.path.exists(COMMAND_FILE):
        log("⛔ command.json already exists → skipping write")
        return False

    command["timestamp"] = time.time()
    tmp_file = COMMAND_FILE + ".tmp"

    try:
        log(f"📝 Writing command → action='{action}'")

        with open(tmp_file, "w") as f:
            json.dump(command, f, indent=2)

        os.rename(tmp_file, COMMAND_FILE)

        log("✅ command.json written successfully")
        return True

    except Exception as e:
        if os.path.exists(tmp_file):
            os.remove(tmp_file)

        log(f"❌ Failed to write command: {e}")
        return False


# =====================================================
# Convenience Helpers (Optional)
# =====================================================

def write_count_walls():
    return write_command({
        "action": "count_walls"
    })


def write_rename_views(old_prefix, new_prefix):
    if not old_prefix or not new_prefix:
        log("⚠️ Invalid rename arguments")
        return False

    return write_command({
        "action": "rename_views",
        "old_prefix": old_prefix,
        "new_prefix": new_prefix
    })


def write_flip_doors():
    return write_command({
        "action": "flip_doors"
    })


def write_ai_suggestions():
    return write_command({
        "action": "ai_suggestions"
    })


def write_modify_parameter(element_id, parameter, value):
    if not element_id or not parameter:
        log("⚠️ Invalid modify_parameter arguments")
        return False

    return write_command({
        "action": "modify_parameter",
        "element_id": element_id,
        "parameter": parameter,
        "value": value
    })


def write_revert_last():
    return write_command({
        "action": "revert_last"
    })
