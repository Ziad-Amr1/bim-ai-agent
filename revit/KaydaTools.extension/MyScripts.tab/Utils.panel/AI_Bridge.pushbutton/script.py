# -*- coding: utf-8 -*-
# BIM AI Agent – Full Stable Revit Bridge
# Features:
# - Permission Levels
# - Confirmation UI
# - Excel (CSV) Report

import os
import json
import time
import csv
from pyrevit import revit, script
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    Wall,
    FamilyInstance,
    BuiltInCategory,
    Transaction,
    StorageType,
    ElementId
)
from Autodesk.Revit.UI import (
    TaskDialog,
    TaskDialogCommonButtons,
    TaskDialogResult
)

# ================= PATH CONFIG =================
BASE_DIR = "E:\\course\\programming\\python\\BIM_AI_Agent_V3\\BIM_AI_Agent"
COMMAND_FILE = os.path.join(BASE_DIR, "command.json")
RESULT_FILE  = os.path.join(BASE_DIR, "result.json")
LOG_FILE     = os.path.join(BASE_DIR, "last_operation.json")
REPORT_FILE  = os.path.join(BASE_DIR, "report.csv")
# ==============================================

output = script.get_output()
doc = revit.doc


# ================= PERMISSIONS =================

PERMISSIONS = {
    "count_walls": "read",
    "rename_views": "modify",
    "flip_doors": "modify",
    "modify_parameter": "modify",
    "revert_last": "admin",
    "ai_suggestions": "read",
}
# Permissions reserved for future enforcement


# ================= HELPERS =================

def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)


def write_json(path, data):
    data["timestamp"] = time.time()
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def write_report(action, status, details):
    new_file = not os.path.exists(REPORT_FILE)
    with open(REPORT_FILE, "a") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["timestamp", "action", "status", "details"])
        writer.writerow([
            time.strftime("%Y-%m-%d %H:%M:%S"),
            action,
            status,
            details
        ])


def ask_confirmation(title, message):
    result = TaskDialog.Show(
        title,
        message,
        TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No
    )
    return result == TaskDialogResult.Yes


# ================= ACTIONS =================

# 🟢 Read
def handle_count_walls(_):
    count = len(
        FilteredElementCollector(doc)
        .OfClass(Wall)
        .WhereElementIsNotElementType()
        .ToElements()
    )
    return {
        "status": "success",
        "action": "count_walls",
        "result": count
    }


def handle_ai_suggestions(_):
    suggestions = []
    for w in (
        FilteredElementCollector(doc)
        .OfClass(Wall)
        .WhereElementIsNotElementType()
    ):
        if w.Width < 0.15:
            suggestions.append({
                "wall_id": w.Id.IntegerValue,
                "issue": "Thin wall",
                "suggestion": "Consider increasing thickness"
            })

    return {
        "status": "success",
        "action": "ai_suggestions",
        "suggestions": suggestions
    }


# 🟡 Modify
def handle_rename_views(command):
    if not ask_confirmation(
        "AI Confirmation",
        "AI suggests renaming views.\nDo you want to proceed?"
    ):
        return {"status": "cancelled", "action": "rename_views"}

    old_prefix = command.get("old_prefix", "")
    new_prefix = command.get("new_prefix", "")
    renamed = 0

    t = Transaction(doc, "AI Rename Views")
    t.Start()
    for v in FilteredElementCollector(doc).OfClass(revit.DB.View):
        if v.IsTemplate:
            continue
        if v.Name.startswith(old_prefix):
            v.Name = v.Name.replace(old_prefix, new_prefix, 1)
            renamed += 1
    t.Commit()

    return {
        "status": "success",
        "action": "rename_views",
        "renamed": renamed
    }


def handle_flip_doors(_):
    if not ask_confirmation(
        "AI Confirmation",
        "Flip all doors in the model?"
    ):
        return {"status": "cancelled", "action": "flip_doors"}

    flipped = []

    t = Transaction(doc, "AI Flip Doors")
    t.Start()
    for d in (
        FilteredElementCollector(doc)
        .OfCategory(BuiltInCategory.OST_Doors)
        .WhereElementIsNotElementType()
    ):
        if isinstance(d, FamilyInstance):
            d.FlipFacingOrientation()
            flipped.append(d.Id.IntegerValue)
    t.Commit()

    write_json(LOG_FILE, {
        "action": "flip_doors",
        "element_ids": flipped
    })

    return {
        "status": "success",
        "action": "flip_doors",
        "flipped_count": len(flipped)
    }


def handle_modify_parameter(command):
    if not ask_confirmation(
        "AI Confirmation",
        "Modify element parameter?"
    ):
        return {"status": "cancelled", "action": "modify_parameter"}

    eid = command.get("element_id")
    pname = command.get("parameter")
    value = command.get("value")

    el = doc.GetElement(ElementId(eid))
    if not el:
        return {"status": "error", "message": "Element not found"}

    param = el.LookupParameter(pname)
    if not param:
        return {"status": "error", "message": "Parameter not found"}

    t = Transaction(doc, "AI Modify Parameter")
    t.Start()

    if param.StorageType == StorageType.String:
        param.Set(str(value))
    elif param.StorageType == StorageType.Integer:
        param.Set(int(value))
    elif param.StorageType == StorageType.Double:
        param.Set(float(value))
    else:
        t.RollBack()
        return {"status": "error", "message": "Unsupported parameter type"}

    t.Commit()

    return {
        "status": "success",
        "action": "modify_parameter",
        "element_id": eid,
        "parameter": pname
    }


# 🔴 Admin
def handle_revert_last(_):
    if not ask_confirmation(
        "Admin Confirmation",
        "Revert last AI operation?"
    ):
        return {"status": "cancelled", "action": "revert_last"}

    log = load_json(LOG_FILE)
    if not log:
        return {"status": "error", "message": "No operation to revert"}

    if log["action"] == "flip_doors":
        t = Transaction(doc, "Revert Flip Doors")
        t.Start()
        for eid in log["element_ids"]:
            el = doc.GetElement(ElementId(eid))
            if isinstance(el, FamilyInstance):
                el.FlipFacingOrientation()
        t.Commit()

    os.remove(LOG_FILE)

    return {
        "status": "success",
        "action": "revert_last"
    }


# ================= ROUTER =================

ACTIONS = {
    "count_walls": handle_count_walls,
    "rename_views": handle_rename_views,
    "flip_doors": handle_flip_doors,
    "modify_parameter": handle_modify_parameter,
    "revert_last": handle_revert_last,
    "ai_suggestions": handle_ai_suggestions,
}


# ================= MAIN =================

if not doc:
    output.print_md("### ❌ No active Revit document")
    script.exit()

command = load_json(COMMAND_FILE)
if not command:
    output.print_md("### ℹ️ No AI command found")
    script.exit()

action = command.get("action")
handler = ACTIONS.get(action)

if not handler:
    result = {"status": "error", "message": "Unknown action"}
else:
    try:
        result = handler(command)
    except Exception as e:
        result = {"status": "error", "message": str(e)}

write_json(RESULT_FILE, result)
write_report(action, result.get("status"), json.dumps(result))
if os.path.exists(COMMAND_FILE):
    os.remove(COMMAND_FILE)


output.print_md("### ✅ Result Written")
output.print_code(json.dumps(result, indent=2))
