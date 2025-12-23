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
### Why this architecture?

- Revit API **must run on the UI thread**

- Background listeners and sockets are unsafe

- User‑triggered execution is required

- This design follows **Revit best practices**.

---

## ❓ Why This Architecture?

* Revit API **must run on the UI thread**
* Background listeners, sockets, or polling inside Revit are unsafe
* Execution must be explicitly user-triggered

This design strictly follows **Revit API best practices** and professional BIM workflows.

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

## ⚙️ Supported Features

### ✔️ Query / Analysis

* Count walls
* Read model data
* Generate reports

### ✔️ Controlled Actions (With Approval)

* Rename views by prefix / suffix

### 🚧 Planned Extensions

* Door flip suggestions
* Door placement recommendations
* QA/QC and validation checks

---

## 🚫 What the AI Does NOT Do

* Modify geometry directly
* Add or delete elements automatically
* Run background processes inside Revit
* Execute commands without user consent

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

---

## 📄 License

Educational / Research Use Only
