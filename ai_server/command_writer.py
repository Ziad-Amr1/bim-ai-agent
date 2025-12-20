# ai_server/command_writer.py
import json
import os
import time
from datetime import datetime
import sys

# ROOT PROJECT DIR (one level above ai_server)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMAND_FILE = os.path.join(BASE_DIR, "command.json")

def log(msg):
    t = datetime.now().strftime("%H:%M:%S")
    print(f"[WRITER {t}] {msg}")
    sys.stdout.flush()


def write_command(command: dict):
    """
    Safely write command.json for Revit AI Bridge (atomic write)
    """
    if os.path.exists(COMMAND_FILE):
        log("⛔ command.json already exists → skipping write")
        return False

    command["timestamp"] = time.time()
    tmp_file = COMMAND_FILE + ".tmp"

    try:
        log(f"📝 Writing command: {command['action']}")

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
