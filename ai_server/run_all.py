#ai_server/run_all.py
import subprocess
import sys
import os
import time
import threading
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON = sys.executable

SERVERS = {
    "flask": {
        "script": "simple-flask-server.py",
        "process": None
    },
    "mcp": {
        "script": "mcp_server.py",
        "process": None
    }
}

running = True


# ---------- utils ----------

def log(msg):
    t = datetime.now().strftime("%H:%M:%S")
    print(f"[MANAGER {t}] {msg}")
    sys.stdout.flush()


def start_server(name):
    server = SERVERS[name]

    log(f"🚀 Starting {name}...")
    server["process"] = subprocess.Popen(
        [PYTHON, server["script"]],
        cwd=BASE_DIR
    )


def stop_server(name):
    proc = SERVERS[name]["process"]
    if proc and proc.poll() is None:
        log(f"🛑 Stopping {name}...")
        proc.terminate()


def status_server(name):
    proc = SERVERS[name]["process"]
    if not proc:
        return "NOT STARTED"
    if proc.poll() is None:
        return "RUNNING"
    return f"STOPPED (code {proc.returncode})"


# ---------- supervisor ----------

def monitor_loop():
    global running

    while running:
        for name in SERVERS:
            proc = SERVERS[name]["process"]
            if proc and proc.poll() is not None:
                log(f"⚠️ {name} stopped unexpectedly → restarting")
                start_server(name)

        time.sleep(2)


# ---------- input listener ----------

def input_loop():
    global running

    while running:
        cmd = input().strip().lower()

        if cmd == "c":
            log("==========================")
            log("... STATUS CHECK ...")
            log("==========================")
            log("")
            log("📊 STATUS CHECK")
            for name in SERVERS:
                log(f"  {name}: {status_server(name)}")

        elif cmd == "q":
            log("👋 Shutting down all servers...")
            running = False
            for name in SERVERS:
                stop_server(name)
            break


# ---------- main ----------

if __name__ == "__main__":
    log("🟢 AI Bridge Manager starting")

    # start servers
    for name in SERVERS:
        start_server(name)

    log("⌨️ Commands: [c] check status | [q] quit")

    # background threads
    threading.Thread(target=monitor_loop, daemon=True).start()
    input_loop()

    log("✅ Manager exited cleanly")
