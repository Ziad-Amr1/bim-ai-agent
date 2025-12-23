# 🤖 BIM AI Agent – Revit × Claude (MCP)

---

## 🇬🇧 English Documentation

📌 Project Overview

BIM AI Agent is a professional and safe bridge between Generative AI (Claude) and Autodesk Revit.

The project demonstrates how AI can analyze, query, and suggest actions on a BIM model without directly controlling Revit or violating Revit API constraints.

Key Idea:
AI prepares the command, Revit executes it safely.

The system enables:

Asking natural language questions about a Revit model (Query)

Triggering controlled and user‑approved changes inside Revit (Action)

This architecture is fully local, stable, and Revit‑API‑compliant, and intentionally avoids:

Background threads inside Revit

Socket listeners or live servers in the Revit process

Direct AI‑to‑Revit execution

All Revit operations are executed only through pyRevit and require explicit user interaction, ensuring safety, transparency, and compliance with Revit best practices.

---

## 🎯 Project Objective

Bridge the gap between **Generative AI** and **BIM software** by enabling:

* Natural language queries on a Revit model
* Controlled, user-approved actions inside Revit
* A live, demonstrable AI–BIM workflow

This implementation satisfies:

✅ Query (e.g. count walls)

✅ Action (e.g. rename views)

✅ Live demo capability

✅ Revit API safety

---

## 🧠 System Architecture

```
Claude Desktop (LLM)
        │
        ▼
MCP Server (mcp_server.py)
        │
        ▼
Flask API (simple-flask-server.py)
        │   (writes command.json)
        ▼
User clicks AI_Bridge button
        │
        ▼
Revit + pyRevit (AI_Bridge.pushbutton)
        │   (executes Revit API)
        ▼
result.json
        │
        ▼
Claude reads final result
```
### Why This Architecture?

- Revit API **must run on the UI thread**

- Background listeners and sockets are unsafe

- User‑triggered execution is required

- This design strictly follows **Revit API best practices** and professional BIM workflows.

---

## 🧩 System Components

### 1️⃣ Claude (AI)

* Interprets natural language requests
* Decides *what should be done*
* Calls MCP tools only
* ❌ No direct access to Revit

### 2️⃣ MCP Server

* Exposes tools to Claude
* Handles AI-to-backend communication

### 3️⃣ Flask Server

* Lightweight local backend
* Writes `command.json`
* Reads `result.json`
* Contains **no Revit logic**

### 4️⃣ File-Based IPC

* `command.json`: AI → Revit instructions
* `result.json`: Revit → AI execution results

### 5️⃣ pyRevit Bridge

* Runs inside Revit
* Reads commands
* Executes them using Revit API transactions
* Writes results
* **Triggered manually by the user**

### 6️⃣ Autodesk Revit

* The only component allowed to modify the model
* All changes occur inside safe transactions

---


## 🛠️ Available Commands

The following commands are exposed through the MCP server and can be invoked by the LLM to interact safely with Autodesk Revit.
All modification commands follow a human-in-the-loop approach and require explicit user confirmation inside Revit before execution.

## 📊 Information & Queries

These commands do not modify the Revit model and are safe to run at any time.

`ping`
Checks whether the MCP server is running and reachable.
Useful for validating that the AI–Revit bridge is active.

`get_wall_count`
Returns the total number of wall elements in the current Revit project.

`ai_suggestions`
Requests an AI-based analysis of the model.
The analysis is executed inside Revit after user confirmation and may return design observations or potential improvement notes.
(An empty result indicates that no issues were detected or the model is too simple for analysis.)

`get_last_result`
Retrieves the result of the most recently executed operation.
This command is intended for programmatic feedback and verification rather than direct user interaction.

## ✏️ Model Modifications

These commands do not execute immediately.
Each request is queued and requires the user to press the AI_Bridge button inside Revit and approve the action.

`rename_views`
Renames Revit views by replacing an existing name prefix with a new one.
This allows batch renaming of views in a controlled and predictable manner.

Example:
Rename views starting with Level → Arc Level

`flip_doors`
Safely attempts to flip the orientation of door elements.
The system checks Revit API capabilities and skips doors that cannot be flipped to avoid errors or unintended behavior.

`modify_parameter`
Modifies a specific parameter of a given element.
Requires:

Element ID

Parameter name

New value

The operation is executed only after user confirmation inside Revit.

## ↩️ Revert & Recovery

`revert_last`
Reverts the last successful modification operation, when supported.
This provides a basic rollback mechanism for safe experimentation.

## 🔐 Safety Model

The AI never modifies the Revit model directly

All changes are:

- Requested by the AI

- Queued through the bridge

- Explicitly reviewed and confirmed by the user inside Revit

- This design prioritizes transparency, control, and model integrity over blind automation.

---

## 🔐 Design & Safety Philosophy

* User-in-the-loop execution
* Explicit approval for every action
* No hidden automation

> This approach mirrors professional workflows such as Git pull requests or CI/CD approvals.

---

## 📁 Project Structure

```
BIM_AI_Agent/
│
├── command.json # Temporary command file (created at runtime)
├── result.json # Result written by Revit execution
├── ai_server/
│   ├── command_writer.py # Writes AI commands to command.json
│   ├── simple-flask-server.py # Flask API (AI → file bridge)
│   └── mcp_server.py # MCP server used by Claude Desktop
└── revit/
    └── KaydaTools.extension/
        └── MyScripts.tab/
            ├── Utils.panel/
            ├── CountWalls.pushbutton/
            │ └── script.py
            ├── AI_Bridge.pushbutton/
            └── script.py
```

---

## ⚙️ Requirements


### Software
- Autodesk Revit 2025
- pyRevit (installed and loaded)
- Python 3.10+ (for Flask + MCP)
- Claude Desktop (with MCP enabled)


### Python Packages
```bash
pip install flask requests mcp
```

---

## 🚀 How to Run

1. Start Flask server
    ```bash
    cd BIM_AI_Agent\ai_server
    python simple-flask-server.py
    ```
    This server:
    - Receives AI requests
    - Writes `command.json`
2. Start MCP server
    ```bash
    cd BIM_AI_Agent\ai_server
    python mcp_server.py
    ```
    ⚠️ Do **not** type anything in this terminal.
    The MCP server is driven by Claude, not manually.
3. Open Claude Desktop (MCP enabled)
    - Enable MCP tools
    - Ensure MCP status = **connected**
4. Open Revit and reload pyRevit
    - Open your project
    - Reload pyRevit (once)
    - Ask Claude for an action
    - Press **Bridge Button** in Revit
    - Ask Claude to read last result

---

## 🧠 Key Takeaway

> **The AI is an intelligent assistant, not a decision-maker.**
> Execution authority always remains inside Revit and under human control.

### 💡 Note
⚠️ This project uses a local project root path.
Please update PROJECT_ROOT in the Revit bridge script
to match your local directory structure.

---

### 📺 Demo
🎥 A short demo video is available on LinkedIn (see post).

---

## 🇪🇬 الشرح باللغة العربية

## 📌 فكرة المشروع

مشروع **BIM AI Agent** بيربط بين **الذكاء الاصطناعي (Claude)** و **برنامج Revit** بطريقة آمنة ومهنية، من غير ما يدي الـ AI أي صلاحية مباشرة للتعديل على الموديل.

الفكرة الأساسية:

* الـ AI يفهم طلب المستخدم
* يحوّل الطلب لأمر منظم
* الأمر يتكتب في ملف `command.json`
* **Revit فقط** هو اللي ينفّذ التعديل بعد موافقة المستخدم

> **الفكرة المحورية:**
> الـ AI يقترح، وRevit ينفّذ بأمان.

---

## 🧠 ليه التصميم ده؟

* Revit API لازم يشتغل على UI Thread
* أي تشغيل في الخلفية خطر وغير آمن
* لازم تدخل بشري صريح في التنفيذ

وده التزام مباشر بقواعد Revit الاحترافية.

---

## 🧩 مكونات النظام

* **Claude:** يفهم ويقترح فقط
* **Flask + MCP:** طبقة وسيطة للاتصال
* **ملفات JSON:** وسيلة تواصل آمنة
* **Bridge داخل Revit:** تنفيذ حقيقي

---

## 🔐 فلسفة الأمان

* لا تنفيذ تلقائي
* لا تعديل بدون موافقة المستخدم
* التحكم دايمًا في إيد المهندس

---

## ✅ استخدامات مناسبة

* عدّ العناصر
* تنظيم أسماء الـ Views
* فحص جودة الموديل
* تقارير QA / QC

---

## 🚫 استخدامات غير مسموحة

* حذف عناصر تلقائيًا
* تعديل Geometry مباشر
* تحكم AI كامل في الموديل

---

## 🏁 الخلاصة

> الـ AI هنا مساعد ذكي، مش بديل عن المهندس.
> التنفيذ الحقيقي بيتم داخل Revit وبموافقة المستخدم.

---

## 👤 Author

**Ziad Amr Said**
Architecture • Frontend • BIM Automation • AI Integration

Built as part of an academic BIM course and independent experimentation.
---

## 📄 License

Educational / Research Use Only
