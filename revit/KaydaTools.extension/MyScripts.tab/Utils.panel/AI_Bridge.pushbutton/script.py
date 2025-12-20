# -*- coding: utf-8 -*-
# AI Bridge - Safe single execution for Revit (pyRevit / IronPython)

import os
import json
import time
# from pathlib import Path
from pyrevit import revit, script
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    Wall,
    View,
    Transaction
)

# ========= PATH CONFIG =========

BASE_DIR = r"E:\course\programming\python\BIM_AI_Agent_V3\BIM_AI_Agent"
print("BASE_DIR =", BASE_DIR)
COMMAND_FILE = os.path.join(BASE_DIR, "command.json")
print("COMMAND_FILE =", COMMAND_FILE)
RESULT_FILE = os.path.join(BASE_DIR, "result.json")
print("RESULT_FILE =", RESULT_FILE)
# ===============================

# BASE_DIR = Path("E:/course/programming/python/BIM_AI_Agent_V3/BIM_AI_Agent")
# COMMAND_FILE = BASE_DIR / "command.json"
# RESULT_FILE = BASE_DIR / "result.json"

# ========= OUTPUT =========

output = script.get_output()
doc = revit.doc


# ========= ACTIONS =========

def count_walls():
    walls = FilteredElementCollector(doc).OfClass(Wall).ToElements()
    return len(walls)


def rename_views(old_prefix, new_prefix):
    views = FilteredElementCollector(doc).OfClass(View).ToElements()
    renamed = 0

    t = Transaction(doc, "AI Rename Views")
    t.Start()

    for v in views:
        if v.IsTemplate:
            continue
        if v.Name.startswith(old_prefix):
            v.Name = v.Name.replace(old_prefix, new_prefix, 1)
            renamed += 1

    t.Commit()
    return renamed


# ========= MAIN =========

if not os.path.exists(COMMAND_FILE):
    output.print_md("### No AI command found.")
    script.exit()

try:
    # --- Safe read ---
    with open(COMMAND_FILE, "r") as f:
        content = f.read().strip()

    if not content:
        output.print_md("### ERROR")
        output.print_md("command.json is empty")
        script.exit()

    try:
        command = json.loads(content)
    except Exception:
        output.print_md("### ERROR")
        output.print_md("Invalid JSON in command.json")
        output.print_code(content)
        script.exit()

    output.print_md("### AI Command Received")
    output.print_code(json.dumps(command, indent=2))

    action = command.get("action")

    # --- Execute ---
    if action == "count_walls":
        result = {
            "status": "success",
            "action": action,
            "result": count_walls(),
            "timestamp": time.time()
        }

    elif action == "rename_views":
        result = {
            "status": "success",
            "renamed": rename_views(
                command.get("old_prefix", ""),
                command.get("new_prefix", "")
            )
        }

    else:
        result = {
            "status": "error",
            "message": "Unknown action"
        }

    # --- Write result ---
    with open(RESULT_FILE, "w") as f:
        json.dump(result, f, indent=2)

    # --- Cleanup ---
    os.remove(COMMAND_FILE)

    output.print_md("### Result Written")
    output.print_code(json.dumps(result, indent=2))

except Exception as e:
    output.print_md("### ERROR")
    output.print_code(str(e))
