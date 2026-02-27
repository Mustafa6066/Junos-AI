#!/usr/bin/env python3
"""
Junos AI Network Operations Center — Web UI v21.1

A visually stunning, agentic web-based dashboard for the Junos MCP Bridge.
Features:
  - Interactive topology visualization with D3.js force-directed graphs
  - Real-time device monitoring via MCP live polling
  - Configuration diff engine with syntax highlighting
  - AI chat interface connected to Ollama + MCP Bridge
  - Jinja2 template rendering & deployment engine
  - Scheduled task management with CRON-style scheduler
  - Log forensics viewer with filtering
  - Workflow builder for chaining MCP operations
  - Dark/Light mode with HPE color theming
"""

import os
import sys
import json
import time
import re
import difflib
import hashlib
import sqlite3
import asyncio
import threading
import glob
import yaml
import logging
import httpx
import traceback
import subprocess
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from functools import wraps
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, render_template, jsonify, request, send_from_directory, Response
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# Quantum-Inspired Network Optimization Engine
from quantum_engine import (
    calculate_network_stats_v2,
    TarjanSPOF,
    fast_diameter_approx,
    QuantumAnnealingOptimizer,
    QuantumWalkAnomalyDetector,
    LouvainCommunityDetector,
    get_clustered_topology,
    optimize_topology,
    detect_anomalies,
    benchmark as quantum_benchmark
)

try:
    from jinja2 import Template, Environment, BaseLoader, UndefinedError
except ImportError:
    from jinja2 import Template, Environment, BaseLoader

# ── Path Setup ─────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

GOLDEN_CONFIG_DIR = BASE_DIR / "golden_configs"
DEVICES_JSON = BASE_DIR / "junos-mcp-server" / "devices.json"
CONFIG_YAML = BASE_DIR / "config.yaml"
AUDIT_DB = BASE_DIR / "audit_history.db"
ANALYSIS_DB = BASE_DIR / "analysis_memory.db"
CONVERSATIONS_DIR = BASE_DIR / "conversations"
TEMPLATES_DIR = BASE_DIR / "templates"
TASKS_DIR = BASE_DIR / "tasks"
LOGS_DIR = BASE_DIR / "logs"
SCHEDULED_DB = BASE_DIR / "web_ui" / "scheduled_tasks.db"
WORKFLOWS_DIR = BASE_DIR / "web_ui" / "workflows"
POOLS_DB = BASE_DIR / "web_ui" / "device_pools.db"
RESULTS_DIR = BASE_DIR / "web_ui" / "results"
GIT_EXPORT_DIR = BASE_DIR / "web_ui" / "git_export"
NOTIFICATIONS_DB = BASE_DIR / "web_ui" / "notifications.db"

# ── Logging ────────────────────────────────────────────────────
logger = logging.getLogger("noc-webui")
logger.setLevel(logging.INFO)

# ── Flask App ──────────────────────────────────────────────────
app = Flask(__name__,
            template_folder="templates",
            static_folder="static")

# ── Security: Generate per-instance secret key (stored locally) ──
_secret_key_file = Path(__file__).parent / ".secret_key"
if _secret_key_file.exists():
    app.config["SECRET_KEY"] = _secret_key_file.read_text().strip()
else:
    import secrets as _secrets
    _generated_key = _secrets.token_hex(32)
    _secret_key_file.write_text(_generated_key)
    app.config["SECRET_KEY"] = _generated_key
    logger.info("Generated new Flask SECRET_KEY (stored in .secret_key)")

# ── Security: Restrict CORS to localhost only ──
_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5555", "http://localhost:5555",
    "http://127.0.0.1:*", "http://localhost:*",
]
CORS(app, origins=_ALLOWED_ORIGINS)
socketio = SocketIO(app, cors_allowed_origins=_ALLOWED_ORIGINS, async_mode="threading",
                    logger=False, engineio_logger=False)

# ── Security: Optional API key authentication ──
_API_KEY = os.environ.get("NOC_API_KEY", "")  # Set NOC_API_KEY env var to enable

def _check_api_key():
    """Middleware: if NOC_API_KEY is set, require it on all API requests."""
    if _API_KEY and request.path.startswith("/api/"):
        provided = request.headers.get("X-API-Key", "") or request.args.get("api_key", "")
        if provided != _API_KEY:
            return jsonify({"error": "Unauthorized — set X-API-Key header"}), 401

app.before_request(_check_api_key)

# ── Prevent ALL API response caching ──
@app.after_request
def _no_cache(response):
    """Ensure no API responses are cached by the browser."""
    if request.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response

# ── Thread pool for async MCP/Ollama calls from Flask ──────────
_executor = ThreadPoolExecutor(max_workers=4)

# ── Load Config ────────────────────────────────────────────────
def load_config():
    try:
        with open(CONFIG_YAML) as f:
            return yaml.safe_load(f)
    except Exception:
        return {}

_cfg = load_config()
MCP_SERVER_URL = _cfg.get("mcp", {}).get("url", "http://127.0.0.1:30030/mcp/")
MCP_CALL_TIMEOUT = _cfg.get("mcp", {}).get("call_timeout", 120.0)
OLLAMA_URL = _cfg.get("ai", {}).get("ollama_url", "http://127.0.0.1:11434")
OLLAMA_MODEL = _cfg.get("ai", {}).get("model", "gpt-oss")
OLLAMA_NUM_CTX = _cfg.get("ai", {}).get("context_window", 32768)
OLLAMA_TEMPERATURE = _cfg.get("ai", {}).get("temperature", 0.12)

def load_devices():
    """Load device inventory — first from devices.json, fallback to MCP router list."""
    try:
        with open(DEVICES_JSON) as f:
            return json.load(f)
    except Exception:
        pass
    # Fallback: query MCP server for router list
    try:
        raw = run_async(mcp_get_router_list())
        # Parse router list text into device dict
        devices = {}
        for line in raw.splitlines():
            line = line.strip().strip("-").strip()
            if line and not line.startswith("Available") and not line.startswith("="):
                name = line.split()[0] if line.split() else line
                if name and name.isalnum() or re.match(r'^[A-Za-z0-9_-]+$', name):
                    devices[name] = {"ip": "", "port": ""}
        if devices:
            return devices
    except Exception:
        pass
    return {}


# ── Auto-create required directories on startup ───────────────
for _dir in [GOLDEN_CONFIG_DIR, WORKFLOWS_DIR, RESULTS_DIR, GIT_EXPORT_DIR,
             CONVERSATIONS_DIR, TEMPLATES_DIR, TASKS_DIR, LOGS_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)


# ══════════════════════════════════════════════════════════════
#  MCP BRIDGE — Direct connection to Junos MCP Server
# ══════════════════════════════════════════════════════════════

_mcp_session_id = None  # Cached session ID

def parse_sse_response(text: str) -> dict:
    """Parse SSE event stream and extract the final JSON-RPC result."""
    parsed = []
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("data: "):
            try:
                parsed.append(json.loads(line[6:]))
            except json.JSONDecodeError:
                continue
    for msg in reversed(parsed):
        if "result" in msg:
            return msg
    return parsed[-1] if parsed else {}


async def _mcp_post(client, session_id, payload, timeout=30.0):
    """Low-level MCP JSON-RPC POST."""
    headers = {"Accept": "application/json, text/event-stream"}
    if session_id:
        headers["mcp-session-id"] = session_id
    resp = await client.post(MCP_SERVER_URL, json=payload, headers=headers, timeout=timeout)
    new_sid = resp.headers.get("mcp-session-id", session_id)
    ct = resp.headers.get("content-type", "")
    raw = resp.text
    data = parse_sse_response(raw) if "text/event-stream" in ct else resp.json()
    return data, new_sid


async def mcp_initialize(client):
    """Initialize MCP session and return session ID."""
    data, sid = await _mcp_post(client, None, {
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-03-26", "capabilities": {},
                   "clientInfo": {"name": "noc-webui", "version": "21.1"}}
    })
    await client.post(MCP_SERVER_URL,
        json={"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
        headers={"Accept": "application/json, text/event-stream", "mcp-session-id": sid},
        timeout=10.0)
    return sid


async def mcp_call_tool(client, sid, tool_name, arguments):
    """Call an MCP tool and return text result."""
    data, _ = await _mcp_post(client, sid, {
        "jsonrpc": "2.0", "id": 3, "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments}
    }, timeout=MCP_CALL_TIMEOUT)
    content = data.get("result", {}).get("content", [])
    text = "\n".join(c.get("text", "") for c in content if c.get("type") == "text")
    return text if text else json.dumps(data)


async def mcp_get_session(client):
    """Get or create MCP session. Clears stale sessions on failure."""
    global _mcp_session_id
    if _mcp_session_id is None:
        _mcp_session_id = await mcp_initialize(client)
    return _mcp_session_id


def mcp_clear_session():
    """Clear cached MCP session so the next call re-initializes."""
    global _mcp_session_id
    _mcp_session_id = None


async def mcp_execute_command(router_name: str, command: str) -> str:
    """Execute a single Junos command on a router via MCP. Retries on stale session."""
    for attempt in range(2):
        try:
            async with httpx.AsyncClient(timeout=MCP_CALL_TIMEOUT + 10) as client:
                sid = await mcp_get_session(client)
                result = await mcp_call_tool(client, sid, "execute_junos_command", {
                    "router_name": router_name, "command": command
                })
                return result
        except Exception as e:
            if attempt == 0:
                logger.warning(f"MCP execute_command failed (attempt 1), clearing session: {e}")
                mcp_clear_session()
            else:
                logger.error(f"MCP execute_command failed: {e}")
                return f"Error: {e}"
    return "Error: MCP command failed after retries"


async def mcp_execute_batch(command: str, router_names: list) -> str:
    """Execute a command on multiple routers via MCP batch."""
    try:
        async with httpx.AsyncClient(timeout=MCP_CALL_TIMEOUT + 30) as client:
            sid = await mcp_get_session(client)
            result = await mcp_call_tool(client, sid, "execute_junos_command_batch", {
                "command": command, "router_names": router_names
            })
            return result
    except Exception as e:
        logger.error(f"MCP batch failed: {e}")
        return f"Error: {e}"


async def mcp_get_config(router_name: str) -> str:
    """Get running config from a router via MCP."""
    try:
        async with httpx.AsyncClient(timeout=MCP_CALL_TIMEOUT + 10) as client:
            sid = await mcp_get_session(client)
            result = await mcp_call_tool(client, sid, "get_junos_config", {
                "router_name": router_name
            })
            return result
    except Exception as e:
        logger.error(f"MCP get_config failed: {e}")
        return f"Error: {e}"


async def mcp_get_facts(router_name: str) -> str:
    """Get device facts from a router via MCP."""
    try:
        async with httpx.AsyncClient(timeout=MCP_CALL_TIMEOUT + 10) as client:
            sid = await mcp_get_session(client)
            result = await mcp_call_tool(client, sid, "gather_device_facts", {
                "router_name": router_name
            })
            return result
    except Exception as e:
        logger.error(f"MCP get_facts failed: {e}")
        return f"Error: {e}"


async def mcp_load_config(router_name: str, config_text: str, commit_comment: str = "NOC WebUI") -> str:
    """Load and commit configuration on a router via MCP."""
    try:
        async with httpx.AsyncClient(timeout=MCP_CALL_TIMEOUT + 30) as client:
            sid = await mcp_get_session(client)
            result = await mcp_call_tool(client, sid, "load_and_commit_config", {
                "router_name": router_name,
                "config_text": config_text,
                "commit_comment": commit_comment
            })
            return result
    except Exception as e:
        logger.error(f"MCP load_config failed: {e}")
        return f"Error: {e}"


async def mcp_get_router_list() -> str:
    """Get list of routers from MCP server."""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            sid = await mcp_get_session(client)
            result = await mcp_call_tool(client, sid, "get_router_list", {})
            return result
    except Exception as e:
        logger.error(f"MCP get_router_list failed: {e}")
        return f"Error: {e}"


def run_async(coro):
    """Run an async coroutine from sync Flask context."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# ══════════════════════════════════════════════════════════════
#  OLLAMA AI ENGINE — Direct connection to Ollama
# ══════════════════════════════════════════════════════════════

# ── Model auto-detection at startup ──
def detect_ollama_model():
    """Check Ollama availability and auto-detect model if configured model is missing."""
    global OLLAMA_MODEL
    try:
        resp = httpx.get(f"{OLLAMA_URL}/api/tags", timeout=5.0)
        if resp.status_code == 200:
            models = [m["name"] for m in resp.json().get("models", [])]
            if not models:
                logger.warning("⚠ Ollama is running but no models installed. AI features will be unavailable.")
                return
            if OLLAMA_MODEL in models or OLLAMA_MODEL.split(":")[0] in [m.split(":")[0] for m in models]:
                logger.info(f"✓ Ollama model '{OLLAMA_MODEL}' is available")
            else:
                old_model = OLLAMA_MODEL
                OLLAMA_MODEL = models[0]
                logger.warning(f"⚠ Ollama model '{old_model}' not found. Auto-selected '{OLLAMA_MODEL}' from {len(models)} available models: {models}")
        else:
            logger.warning(f"⚠ Ollama returned status {resp.status_code}. AI features may be unavailable.")
    except Exception as e:
        logger.warning(f"⚠ Cannot connect to Ollama at {OLLAMA_URL}: {e}. AI features will be unavailable.")

detect_ollama_model()


async def ollama_chat_async(messages: list, stream: bool = False, model: str = "") -> dict:
    """Send chat to Ollama and return response."""
    payload = {
        "model": model or OLLAMA_MODEL,
        "messages": messages,
        "stream": stream,
        "options": {
            "num_ctx": OLLAMA_NUM_CTX,
            "temperature": OLLAMA_TEMPERATURE,
            "top_p": 0.9,
            "repeat_penalty": 1.1,
        }
    }
    try:
        async with httpx.AsyncClient(timeout=600.0) as client:
            resp = await client.post(f"{OLLAMA_URL}/api/chat", json=payload)
            if resp.status_code != 200:
                error_text = resp.text[:500]
                logger.error(f"Ollama returned {resp.status_code}: {error_text}")
                return {"message": {"content": f"AI Error (HTTP {resp.status_code}): {error_text}"}}
            return resp.json()
    except httpx.ConnectError:
        return {"message": {"content": "⚠ Cannot connect to Ollama. Please ensure it is running at " + OLLAMA_URL}}
    except httpx.ReadTimeout:
        return {"message": {"content": "⚠ Ollama request timed out. The model may be loading or the query is too complex."}}
    except Exception as e:
        logger.error(f"ollama_chat_async error: {e}")
        return {"message": {"content": f"⚠ AI Error: {str(e)}"}}


async def ollama_analyze_async(system: str, data: str, question: str) -> str:
    """Send data to Ollama for focused analysis (no tools)."""
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": f"DATA:\n{data}\n\nQUESTION: {question}"}
    ]
    result = await ollama_chat_async(messages)
    return result.get("message", {}).get("content", "No response from AI")


async def ollama_stream_async(messages: list):
    """Stream chat responses from Ollama token by token."""
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": True,
        "options": {
            "num_ctx": OLLAMA_NUM_CTX,
            "temperature": OLLAMA_TEMPERATURE,
        }
    }
    try:
        async with httpx.AsyncClient(timeout=600.0) as client:
            async with client.stream("POST", f"{OLLAMA_URL}/api/chat", json=payload) as resp:
                if resp.status_code != 200:
                    yield f"⚠ Ollama returned HTTP {resp.status_code}. Please check model availability."
                    return
                async for line in resp.aiter_lines():
                    if line.strip():
                        try:
                            chunk = json.loads(line)
                            token = chunk.get("message", {}).get("content", "")
                            if token:
                                yield token
                            if chunk.get("done"):
                                break
                        except json.JSONDecodeError:
                            continue
    except httpx.ConnectError:
        yield "⚠ Cannot connect to Ollama. Please ensure it is running at " + OLLAMA_URL
    except httpx.ReadTimeout:
        yield "⚠ Ollama stream timed out."
    except Exception as e:
        yield f"⚠ AI Streaming Error: {str(e)}"


# ══════════════════════════════════════════════════════════════
#  SCHEDULED TASKS ENGINE
# ══════════════════════════════════════════════════════════════

def init_scheduled_db():
    """Initialize the scheduled tasks database."""
    SCHEDULED_DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(SCHEDULED_DB))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS scheduled_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            task_type TEXT NOT NULL,
            schedule TEXT NOT NULL,
            target_routers TEXT NOT NULL,
            command TEXT NOT NULL,
            enabled INTEGER DEFAULT 1,
            last_run TEXT,
            last_result TEXT,
            next_run TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            run_count INTEGER DEFAULT 0
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS task_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            run_at TEXT,
            result TEXT,
            status TEXT,
            duration_ms INTEGER,
            FOREIGN KEY (task_id) REFERENCES scheduled_tasks(id)
        )
    """)
    conn.commit()
    conn.close()

init_scheduled_db()

_scheduler_running = False
_scheduler_thread = None


def calculate_next_run(schedule_str: str) -> str:
    """Calculate next run time from a schedule string like '5m', '1h', '30s', '24h' or cron expressions."""
    now = datetime.now()
    schedule_str = schedule_str.strip()
    # Check for cron expression (5 space-separated fields or alias)
    if schedule_str.startswith("@") or len(schedule_str.split()) == 5:
        return parse_cron_expression(schedule_str)
    match = re.match(r'(\d+)(s|m|h|d)', schedule_str.lower())
    if not match:
        return (now + timedelta(hours=1)).isoformat()
    val, unit = int(match.group(1)), match.group(2)
    delta = {"s": timedelta(seconds=val), "m": timedelta(minutes=val),
             "h": timedelta(hours=val), "d": timedelta(days=val)}[unit]
    return (now + delta).isoformat()


def scheduler_loop():
    """Background scheduler that checks and runs due tasks."""
    global _scheduler_running
    _scheduler_running = True
    while _scheduler_running:
        try:
            conn = sqlite3.connect(str(SCHEDULED_DB))
            conn.row_factory = sqlite3.Row
            now = datetime.now().isoformat()
            due_tasks = conn.execute(
                "SELECT * FROM scheduled_tasks WHERE enabled=1 AND (next_run IS NULL OR next_run <= ?)", (now,)
            ).fetchall()
            for task in due_tasks:
                task_dict = dict(task)
                routers = json.loads(task_dict["target_routers"])
                command = task_dict["command"]
                start = time.time()
                try:
                    if len(routers) == 1:
                        result = run_async(mcp_execute_command(routers[0], command))
                    else:
                        result = run_async(mcp_execute_batch(command, routers))
                    status = "success"
                except Exception as e:
                    result = str(e)
                    status = "error"
                duration = int((time.time() - start) * 1000)
                next_run = calculate_next_run(task_dict["schedule"])
                conn.execute(
                    "UPDATE scheduled_tasks SET last_run=?, last_result=?, next_run=?, run_count=run_count+1 WHERE id=?",
                    (now, result[:5000], next_run, task_dict["id"])
                )
                conn.execute(
                    "INSERT INTO task_history (task_id, run_at, result, status, duration_ms) VALUES (?,?,?,?,?)",
                    (task_dict["id"], now, result[:5000], status, duration)
                )
                conn.commit()
                logger.info(f"Scheduled task '{task_dict['name']}' ran: {status} ({duration}ms)")
                # Emit result via WebSocket
                socketio.emit("task_result", {
                    "task_id": task_dict["id"], "name": task_dict["name"],
                    "status": status, "result": result[:2000], "duration": duration
                })
            conn.close()
        except Exception as e:
            logger.error(f"Scheduler error: {e}")
        time.sleep(10)  # Check every 10 seconds


def start_scheduler():
    """Start the background scheduler thread."""
    global _scheduler_thread
    if _scheduler_thread is None or not _scheduler_thread.is_alive():
        _scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
        _scheduler_thread.start()
        logger.info("Scheduler started")


# ══════════════════════════════════════════════════════════════
#  WORKFLOW ENGINE
# ══════════════════════════════════════════════════════════════

WORKFLOWS_DIR.mkdir(parents=True, exist_ok=True)


def load_workflows():
    """Load all saved workflows from disk."""
    workflows = []
    for f in sorted(WORKFLOWS_DIR.glob("*.json")):
        try:
            wf = json.loads(f.read_text())
            wf["filename"] = f.name
            workflows.append(wf)
        except Exception:
            continue
    return workflows


def save_workflow(workflow: dict):
    """Save a workflow to disk."""
    name = workflow.get("name", f"workflow_{int(time.time())}")
    safe_name = re.sub(r'[^\w\-]', '_', name)
    path = WORKFLOWS_DIR / f"{safe_name}.json"
    workflow["updated_at"] = datetime.now().isoformat()
    if "created_at" not in workflow:
        workflow["created_at"] = datetime.now().isoformat()
    path.write_text(json.dumps(workflow, indent=2))
    return str(path)


async def execute_workflow(workflow: dict) -> list:
    """Execute a workflow — a sequence of MCP steps."""
    results = []
    variables = workflow.get("variables", {})
    
    for i, step in enumerate(workflow.get("steps", [])):
        step_result = {"step": i + 1, "name": step.get("name", f"Step {i+1}"),
                       "type": step.get("type", "command"), "status": "running"}
        start = time.time()
        
        try:
            step_type = step.get("type", "command")
            
            if step_type == "command":
                router = step.get("router", "")
                cmd = step.get("command", "")
                # Variable substitution
                for k, v in variables.items():
                    cmd = cmd.replace(f"{{{{{k}}}}}", str(v))
                    router = router.replace(f"{{{{{k}}}}}", str(v))
                result = await mcp_execute_command(router, cmd)
                step_result["output"] = result
                
            elif step_type == "batch":
                routers = step.get("routers", [])
                cmd = step.get("command", "")
                for k, v in variables.items():
                    cmd = cmd.replace(f"{{{{{k}}}}}", str(v))
                result = await mcp_execute_batch(cmd, routers)
                step_result["output"] = result
                
            elif step_type == "template":
                template_name = step.get("template", "")
                tmpl_vars = step.get("variables", {})
                tmpl_vars.update(variables)
                tmpl_path = TEMPLATES_DIR / f"{template_name}.j2"
                if tmpl_path.exists():
                    env = Environment(loader=BaseLoader())
                    tmpl = env.from_string(tmpl_path.read_text())
                    rendered = tmpl.render(**tmpl_vars)
                    step_result["output"] = rendered
                    step_result["rendered_config"] = rendered
                else:
                    step_result["output"] = f"Template not found: {template_name}"
                    step_result["status"] = "error"
                    
            elif step_type == "deploy":
                router = step.get("router", "")
                config = step.get("config", "")
                # Config can come from previous step
                if config.startswith("$step_"):
                    ref_idx = int(config.split("_")[1]) - 1
                    if 0 <= ref_idx < len(results):
                        config = results[ref_idx].get("rendered_config", results[ref_idx].get("output", ""))
                comment = step.get("commit_comment", "NOC Workflow Deployment")
                result = await mcp_load_config(router, config, comment)
                step_result["output"] = result
                
            elif step_type == "ai_analyze":
                data = step.get("data", "")
                if data.startswith("$step_"):
                    ref_idx = int(data.split("_")[1]) - 1
                    if 0 <= ref_idx < len(results):
                        data = results[ref_idx].get("output", "")
                question = step.get("question", "Analyze this output")
                system = step.get("system", "You are a Junos network expert. Analyze the following data.")
                result = await ollama_analyze_async(system, data, question)
                step_result["output"] = result
                
            elif step_type == "condition":
                check_step = int(step.get("check_step", 1)) - 1
                pattern = step.get("pattern", "")
                if 0 <= check_step < len(results):
                    prev_output = results[check_step].get("output", "")
                    if re.search(pattern, prev_output, re.IGNORECASE):
                        step_result["output"] = "Condition MET"
                        step_result["condition_met"] = True
                    else:
                        step_result["output"] = "Condition NOT MET"
                        step_result["condition_met"] = False
                        if step.get("skip_rest_on_fail"):
                            step_result["status"] = "skipped"
                            results.append(step_result)
                            break
                            
            elif step_type == "wait":
                seconds = int(step.get("seconds", 5))
                await asyncio.sleep(seconds)
                step_result["output"] = f"Waited {seconds}s"
            
            step_result["status"] = step_result.get("status", "success")
            
        except Exception as e:
            step_result["status"] = "error"
            step_result["output"] = str(e)
            if step.get("stop_on_error", False):
                results.append(step_result)
                break
        
        step_result["duration_ms"] = int((time.time() - start) * 1000)
        results.append(step_result)
        
        # Emit progress via WebSocket
        socketio.emit("workflow_progress", {
            "step": i + 1, "total": len(workflow.get("steps", [])),
            "name": step_result["name"], "status": step_result["status"]
        })
    
    return results

# ── Topology Engine ────────────────────────────────────────────
def build_topology_from_golden_configs():
    """Parse golden configs to build topology graph for web visualization."""
    topology = {
        "nodes": [],
        "links": [],
        "loopbacks": {},
        "roles": {},
        "bgp_peers": {},
        "interfaces": {},
        "isis_metrics": {},
        "mpls_interfaces": {},
        "vpn_instances": {}
    }
    seen_links = set()
    
    if not GOLDEN_CONFIG_DIR.exists():
        GOLDEN_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    conf_files = sorted(GOLDEN_CONFIG_DIR.glob("*.conf"))
    
    # Fallback: if no golden configs exist, build minimal topology from devices.json
    if not conf_files:
        devices = load_devices()
        for name, info in devices.items():
            role = "PE" if name.upper().startswith("PE") else ("RR" if name in ("P12","P22") else "P")
            topology["nodes"].append({
                "id": name, "role": role, "loopback": info.get("ip", ""),
                "interfaces": [], "isis_interfaces": [],
                "bgp_neighbors": [], "ldp": False, "vpn": False,
                "descriptions": {}, "addresses": {}
            })
            topology["roles"][name] = role
            if info.get("ip"):
                topology["loopbacks"][name] = info["ip"]
        return topology
    
    for fname in conf_files:
        router = fname.stem
        
        try:
            lines = fname.read_text().splitlines()
        except Exception:
            continue
        
        # Determine role
        if router.startswith("PE"):
            role = "PE"
        elif router in ("P12", "P22"):
            role = "RR"
        else:
            role = "P"
        topology["roles"][router] = role
        
        descriptions = {}
        addresses = {}
        isis_intfs = []
        ldp_intfs = []
        mpls_intfs = []
        bgp_neighbors = []
        vpn_instances = []
        
        for line in lines:
            line = line.strip()
            
            # Interface descriptions
            m = re.match(r'set interfaces (ge-\d+/\d+/\d+) description "?(.+?)"?\s*$', line)
            if m:
                descriptions[m.group(1)] = m.group(2)
            
            # IPv4 addresses
            m = re.match(r'set interfaces (ge-\d+/\d+/\d+) unit \d+ family inet address (\d+\.\d+\.\d+\.\d+/\d+)', line)
            if m:
                addresses[m.group(1)] = m.group(2)
            
            # Loopback
            m = re.match(r'set interfaces lo0 unit 0 family inet address (\d+\.\d+\.\d+\.\d+)/32', line)
            if m:
                topology["loopbacks"][router] = m.group(1)
            
            # BGP neighbors
            m = re.match(r'set protocols bgp group \S+ neighbor (\d+\.\d+\.\d+\.\d+)', line)
            if m:
                bgp_neighbors.append(m.group(1))
            
            # IS-IS interfaces
            m = re.match(r'set protocols isis interface (ge-\d+/\d+/\d+)\.\d+', line)
            if m:
                if m.group(1) not in isis_intfs:
                    isis_intfs.append(m.group(1))
            
            # IS-IS metrics
            m = re.match(r'set protocols isis interface (ge-\d+/\d+/\d+)\.\d+ level \d+ metric (\d+)', line)
            if m:
                topology["isis_metrics"].setdefault(router, {})[m.group(1)] = int(m.group(2))
            
            # LDP interfaces
            m = re.match(r'set protocols ldp interface (ge-\d+/\d+/\d+)', line)
            if m:
                ldp_intfs.append(m.group(1))
            
            # MPLS interfaces
            m = re.match(r'set protocols mpls interface (ge-\d+/\d+/\d+)', line)
            if m:
                mpls_intfs.append(m.group(1))
            
            # VPN instances
            m = re.match(r'set routing-instances (\S+) instance-type (\S+)', line)
            if m:
                vpn_instances.append({"name": m.group(1), "type": m.group(2)})
        
        topology["bgp_peers"][router] = bgp_neighbors
        topology["interfaces"][router] = {
            "physical": list(descriptions.keys()),
            "isis": isis_intfs,
            "ldp": ldp_intfs,
            "mpls": mpls_intfs
        }
        if vpn_instances:
            topology["vpn_instances"][router] = vpn_instances
        
        # Build node (fields match frontend JS expectations)
        topology["nodes"].append({
            "id": router,
            "label": router,
            "role": "Route Reflector" if role == "RR" else role,
            "loopback": topology["loopbacks"].get(router, ""),
            "interfaces": list(descriptions.keys()),
            "isis_interfaces": isis_intfs,
            "bgp_neighbors": bgp_neighbors,
            "ldp": len(ldp_intfs) > 0,
            "mpls": len(mpls_intfs) > 0,
            "rsvp": False,
            "vpn": vpn_instances[0]["name"] if vpn_instances else None,
            "status": "up"
        })
        
        # Build links
        for intf, desc in descriptions.items():
            m = re.match(r'(\w+)->(\w+)', desc)
            if m:
                local_name = m.group(1)
                remote_name = m.group(2)
                link_key = tuple(sorted([local_name, remote_name]))
                if link_key not in seen_links:
                    seen_links.add(link_key)
                    subnet = addresses.get(intf, "")
                    metric = topology["isis_metrics"].get(router, {}).get(intf, 10)
                    topology["links"].append({
                        "source": local_name,
                        "target": remote_name,
                        "source_intf": intf,
                        "subnet": subnet,
                        "metric": metric,
                        "protocols": {
                            "isis": intf in isis_intfs,
                            "ldp": intf in ldp_intfs,
                            "mpls": intf in mpls_intfs
                        },
                        "status": "up"
                    })
    
    # Build iBGP session links
    ip_to_name = {ip: name for name, ip in topology["loopbacks"].items()}
    bgp_links = []
    bgp_seen = set()
    for router, peers in topology["bgp_peers"].items():
        for peer_ip in peers:
            peer_name = ip_to_name.get(peer_ip, peer_ip)
            key = tuple(sorted([router, peer_name]))
            if key not in bgp_seen and peer_name != peer_ip:
                bgp_seen.add(key)
                bgp_links.append({
                    "source": router,
                    "target": peer_name,
                    "type": "ibgp",
                    "status": "established"
                })
    topology["bgp_links"] = bgp_links
    
    return topology


# ── Config Diff Engine ─────────────────────────────────────────
def get_config_diff(router_name, config_text=None):
    """Compare running config against golden config."""
    golden_path = GOLDEN_CONFIG_DIR / f"{router_name}.conf"
    if not golden_path.exists():
        # Try to auto-fetch from MCP if no golden config
        try:
            fetched = run_async(mcp_get_config(router_name))
            if fetched and not fetched.startswith("Error:") and len(fetched) > 50:
                golden_path.write_text(fetched)
            else:
                return {"error": f"No golden config for {router_name}. Use Sync from MCP to pull configs."}
        except Exception:
            return {"error": f"No golden config for {router_name}. Use Sync from MCP to pull configs."}
    
    golden_lines = golden_path.read_text().splitlines()
    
    if config_text:
        running_lines = config_text.splitlines()
    else:
        running_lines = golden_lines  # Fallback to self-compare
    
    differ = difflib.unified_diff(
        golden_lines, running_lines,
        fromfile=f"golden/{router_name}.conf",
        tofile=f"running/{router_name}",
        lineterm=""
    )
    
    diff_lines = list(differ)
    
    additions = sum(1 for l in diff_lines if l.startswith("+") and not l.startswith("+++"))
    deletions = sum(1 for l in diff_lines if l.startswith("-") and not l.startswith("---"))
    
    return {
        "router": router_name,
        "diff": "\n".join(diff_lines),
        "additions": additions,
        "deletions": deletions,
        "golden_lines": len(golden_lines),
        "running_lines": len(running_lines),
        "match": additions == 0 and deletions == 0,
        "timestamp": datetime.now().isoformat()
    }


# ── Shortest Path Analysis ────────────────────────────────────
def find_shortest_path(source, target, topology=None):
    """Dijkstra's shortest path using IS-IS metrics from topology."""
    if topology is None:
        topology = build_topology_from_golden_configs()
    
    # Build adjacency graph with weights
    graph = {}
    for link in topology["links"]:
        src, dst = link["source"], link["target"]
        weight = link.get("metric", 10)
        graph.setdefault(src, []).append((dst, weight, link))
        graph.setdefault(dst, []).append((src, weight, link))
    
    if source not in graph or target not in graph:
        return {"error": f"Unknown node(s): {source}, {target}", "path": [], "cost": -1}
    
    # Dijkstra
    import heapq
    dist = {source: 0}
    prev = {source: None}
    prev_link = {source: None}
    pq = [(0, source)]
    visited = set()
    
    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        if u == target:
            break
        for v, w, link in graph.get(u, []):
            if v not in visited:
                new_dist = d + w
                if new_dist < dist.get(v, float("inf")):
                    dist[v] = new_dist
                    prev[v] = u
                    prev_link[v] = link
                    heapq.heappush(pq, (new_dist, v))
    
    if target not in prev:
        return {"error": f"No path from {source} to {target}", "path": [], "cost": -1}
    
    # Reconstruct
    path = []
    links_used = []
    node = target
    while node is not None:
        path.append(node)
        if prev_link.get(node):
            links_used.append(prev_link[node])
        node = prev.get(node)
    path.reverse()
    links_used.reverse()
    
    return {
        "path": path,
        "links": links_used,
        "cost": dist[target],
        "hops": len(path) - 1,
        "source": source,
        "target": target
    }


# ── Config Search Engine ──────────────────────────────────────
def search_configs(pattern, regex=False):
    """Search across all golden configs for a pattern."""
    results = []
    for fname in sorted(GOLDEN_CONFIG_DIR.iterdir()):
        if not fname.name.endswith(".conf"):
            continue
        router = fname.stem
        lines = fname.read_text().splitlines()
        for i, line in enumerate(lines, 1):
            try:
                if regex:
                    if re.search(pattern, line, re.IGNORECASE):
                        results.append({"router": router, "line": i, "text": line.strip()})
                else:
                    if pattern.lower() in line.lower():
                        results.append({"router": router, "line": i, "text": line.strip()})
            except re.error:
                pass
    return results


# ── Audit History ─────────────────────────────────────────────
def get_audit_history():
    """Retrieve audit history from SQLite."""
    if not AUDIT_DB.exists():
        return []
    try:
        conn = sqlite3.connect(str(AUDIT_DB))
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM audit_runs ORDER BY start_time DESC LIMIT 20"
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        return []


# ── Conversation History ──────────────────────────────────────
def get_conversations():
    """Load conversation index."""
    index_path = CONVERSATIONS_DIR / "_index.json"
    if not index_path.exists():
        return []
    try:
        data = json.loads(index_path.read_text())
        return sorted(data.get("conversations", []),
                      key=lambda c: c.get("updated_at", ""), reverse=True)
    except Exception:
        return []


# ── Network Stats Calculator ─────────────────────────────────
def calculate_network_stats(topology):
    """Compute network topology statistics similar to OSMnx."""
    nodes = topology["nodes"]
    links = topology["links"]
    
    if not nodes or not links:
        return {}
    
    # Build adjacency for analysis
    adj = {}
    for link in links:
        adj.setdefault(link["source"], set()).add(link["target"])
        adj.setdefault(link["target"], set()).add(link["source"])
    
    degrees = [len(adj.get(n["id"], set())) for n in nodes]
    
    # Simple graph diameter (BFS from each node)
    def bfs_max_dist(start):
        visited = {start: 0}
        queue = [start]
        while queue:
            node = queue.pop(0)
            for neighbor in adj.get(node, set()):
                if neighbor not in visited:
                    visited[neighbor] = visited[node] + 1
                    queue.append(neighbor)
        return max(visited.values()) if visited else 0
    
    node_ids = [n["id"] for n in nodes]
    max_dists = [bfs_max_dist(n) for n in node_ids]
    
    # Single points of failure
    spof = []
    for node in node_ids:
        # Remove node and check connectivity
        remaining = [n for n in node_ids if n != node]
        if not remaining:
            continue
        visited = {remaining[0]}
        queue = [remaining[0]]
        while queue:
            current = queue.pop(0)
            for neighbor in adj.get(current, set()):
                if neighbor not in visited and neighbor in remaining:
                    visited.add(neighbor)
                    queue.append(neighbor)
        if len(visited) < len(remaining):
            spof.append(node)
    
    return {
        "total_nodes": len(nodes),
        "total_links": len(links),
        "pe_count": sum(1 for n in nodes if n["role"] == "PE"),
        "p_count": sum(1 for n in nodes if n["role"] == "P"),
        "rr_count": sum(1 for n in nodes if n["role"] == "Route Reflector"),
        "avg_degree": round(sum(degrees) / len(degrees), 1) if degrees else 0,
        "max_degree": max(degrees) if degrees else 0,
        "min_degree": min(degrees) if degrees else 0,
        "graph_diameter": max(max_dists) if max_dists else 0,
        "avg_path_length": round(sum(max_dists) / len(max_dists), 1) if max_dists else 0,
        "total_bgp_sessions": sum(len(n.get("bgp_neighbors", [])) for n in nodes),
        "total_isis_adjacencies": sum(len(n.get("isis_interfaces", [])) for n in nodes),
        "total_ldp_sessions": sum(1 for n in nodes if n.get("ldp")),
        "total_vpn_instances": sum(1 for n in nodes if n.get("vpn")),
        "single_points_of_failure": spof,
        "redundancy_score": round((1 - len(spof) / len(nodes)) * 100, 1) if nodes else 0,
        "connectivity": "full-mesh" if not spof else "partial-mesh"
    }


# ══════════════════════════════════════════════════════════════
#  API ROUTES
# ══════════════════════════════════════════════════════════════

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/favicon.ico")
def favicon():
    return "", 204


# ══════════════════════════════════════════════════════════════
#  BOOTSTRAP & CONFIG SYNC — Zero-config onboarding
#  Pull live configs from MCP devices and save as golden configs
#  so the entire tool works from just MCP + devices
# ══════════════════════════════════════════════════════════════

@app.route("/api/bootstrap/status")
def api_bootstrap_status():
    """Check if golden configs exist — used by frontend for first-run detection."""
    has_configs = any(GOLDEN_CONFIG_DIR.glob("*.conf"))
    devices = load_devices()
    device_count = len(devices)
    config_count = len(list(GOLDEN_CONFIG_DIR.glob("*.conf")))
    missing = [d for d in devices if not (GOLDEN_CONFIG_DIR / f"{d}.conf").exists()]
    return jsonify({
        "bootstrapped": has_configs and config_count >= device_count,
        "device_count": device_count,
        "config_count": config_count,
        "missing_configs": missing,
        "golden_config_dir": str(GOLDEN_CONFIG_DIR)
    })

@app.route("/api/bootstrap/sync", methods=["POST"])
def api_bootstrap_sync():
    """Pull live configs from all MCP devices and save as golden configs.
    This is the one-click onboarding — after this, everything works."""
    data = request.json or {}
    routers = data.get("routers", [])
    if not routers:
        devices = load_devices()
        routers = list(devices.keys())
    if not routers:
        return jsonify({"error": "No devices found. Check devices.json or MCP server."}), 400

    results = {}
    synced = 0
    failed = 0
    for router in routers:
        try:
            config = run_async(mcp_get_config(router))
            if config and not config.startswith("Error:") and len(config) > 50:
                config_path = GOLDEN_CONFIG_DIR / f"{router}.conf"
                config_path.write_text(config)
                # Write metadata
                meta_path = GOLDEN_CONFIG_DIR / f"{router}.meta"
                meta = {
                    "synced_at": datetime.now().isoformat(),
                    "source": "mcp_live_sync",
                    "lines": len(config.splitlines()),
                    "size_bytes": len(config)
                }
                meta_path.write_text(json.dumps(meta, indent=2))
                results[router] = {"status": "synced", "lines": len(config.splitlines())}
                synced += 1
            else:
                results[router] = {"status": "failed", "error": config[:200] if config else "Empty config"}
                failed += 1
        except Exception as e:
            results[router] = {"status": "failed", "error": str(e)}
            failed += 1

    return jsonify({
        "results": results, "synced": synced, "failed": failed,
        "total": len(routers), "timestamp": datetime.now().isoformat(),
        "message": f"Synced {synced}/{len(routers)} device configs. " +
                   ("All ready!" if failed == 0 else f"{failed} failed — check MCP connectivity.")
    })

@app.route("/api/bootstrap/sync-one/<router>", methods=["POST"])
def api_bootstrap_sync_one(router):
    """Pull and save config for a single router."""
    try:
        config = run_async(mcp_get_config(router))
        if config and not config.startswith("Error:") and len(config) > 50:
            config_path = GOLDEN_CONFIG_DIR / f"{router}.conf"
            config_path.write_text(config)
            meta_path = GOLDEN_CONFIG_DIR / f"{router}.meta"
            meta = {
                "synced_at": datetime.now().isoformat(),
                "source": "mcp_live_sync",
                "lines": len(config.splitlines()),
                "size_bytes": len(config)
            }
            meta_path.write_text(json.dumps(meta, indent=2))
            return jsonify({"status": "synced", "router": router,
                            "lines": len(config.splitlines())})
        else:
            return jsonify({"status": "failed", "error": config[:200] if config else "Empty"}), 500
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)}), 500

@app.route("/api/topology")
def api_topology():
    topo = build_topology_from_golden_configs()
    clustered = request.args.get("clustered", "auto")
    max_visible = int(request.args.get("max_visible", 200))

    if clustered == "true" or (clustered == "auto" and len(topo["nodes"]) > max_visible):
        topo = get_clustered_topology(topo, max_visible)

    return jsonify({
        "nodes": topo["nodes"],
        "links": topo["links"],
        "bgp_links": topo.get("bgp_links", []),
        "clustered": topo.get("clustered", False),
        "original_node_count": topo.get("original_node_count", len(topo["nodes"])),
    })

@app.route("/api/topology/stats")
def api_topology_stats():
    topo = build_topology_from_golden_configs()
    stats = calculate_network_stats_v2(topo)
    return jsonify(stats)

@app.route("/api/devices")
def api_devices():
    devices = load_devices()
    topo = build_topology_from_golden_configs()
    result = []
    for name, info in devices.items():
        node = next((n for n in topo["nodes"] if n["id"] == name), None)
        result.append({
            "name": name,
            "ip": info.get("ip", ""),
            "port": info.get("port", ""),
            "role": node["role"] if node else "unknown",
            "loopback": node["loopback"] if node else "",
            "interfaces": len(node["interfaces"]) if node else 0,
            "isis": len(node["isis_interfaces"]) if node else 0,
            "bgp": len(node["bgp_neighbors"]) if node else 0,
            "ldp": node["ldp"] if node else False,
            "status": "online"
        })
    return jsonify(result)

@app.route("/api/golden-configs")
def api_golden_configs():
    configs = []
    for fname in sorted(GOLDEN_CONFIG_DIR.iterdir()):
        if not fname.name.endswith(".conf"):
            continue
        content = fname.read_text()
        meta_path = GOLDEN_CONFIG_DIR / f"{fname.stem}.meta"
        meta = {}
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text())
            except Exception:
                pass
        configs.append({
            "router": fname.stem,
            "lines": len(content.splitlines()),
            "size": len(content),
            "sha256": hashlib.sha256(content.encode()).hexdigest()[:16],
            "saved_at": meta.get("saved_at", ""),
            "content": content
        })
    return jsonify(configs)

@app.route("/api/golden-configs/<router>")
def api_golden_config(router):
    path = GOLDEN_CONFIG_DIR / f"{router}.conf"
    if path.exists():
        content = path.read_text()
    else:
        # Fallback: pull live config via MCP and auto-save as golden config
        content = run_async(mcp_get_config(router))
        if not content or content.startswith("Error:") or len(content) < 50:
            return jsonify({"error": f"No config found for {router}. Try syncing from MCP."}), 404
        # Auto-save for future use
        path.write_text(content)
        meta_path = GOLDEN_CONFIG_DIR / f"{router}.meta"
        meta_path.write_text(json.dumps({
            "synced_at": datetime.now().isoformat(),
            "source": "auto_fetch", "lines": len(content.splitlines())
        }, indent=2))
    return jsonify({
        "router": router,
        "config": content,
        "lines": len(content.splitlines())
    })

@app.route("/api/config-diff/<router>")
def api_config_diff(router):
    diff = get_config_diff(router)
    return jsonify(diff)

@app.route("/api/config-search")
def api_config_search():
    pattern = request.args.get("q", "")
    regex = request.args.get("regex", "false").lower() == "true"
    if not pattern:
        return jsonify({"results": []})
    raw = search_configs(pattern, regex)
    results = [{"router": r["router"], "line_number": r["line"], "line": r["text"]} for r in raw]
    return jsonify({"results": results})

@app.route("/api/shortest-path")
def api_shortest_path():
    source = request.args.get("source", "")
    target = request.args.get("target", "")
    if not source or not target:
        return jsonify({"error": "source and target required"})
    result = find_shortest_path(source, target)
    return jsonify({
        "path": result.get("path", []),
        "total_cost": result.get("cost", 0),
        "hops": result.get("hops", 0),
        "links": result.get("links", []),
        "error": result.get("error")
    })


# ══════════════════════════════════════════════════════════════
#  QUANTUM-INSPIRED NETWORK OPTIMIZATION API
# ══════════════════════════════════════════════════════════════

@app.route("/api/quantum/optimize", methods=["POST"])
def api_quantum_optimize():
    """Quantum Annealing: find optimal new links to eliminate SPOFs."""
    data = request.json or {}
    max_links = data.get("max_new_links", 5)
    topo = build_topology_from_golden_configs()
    from collections import defaultdict
    adj = defaultdict(set)
    for link in topo["links"]:
        adj[link["source"]].add(link["target"])
        adj[link["target"]].add(link["source"])
    try:
        result = optimize_topology(dict(adj), topo["nodes"], max_links)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/quantum/anomalies")
def api_quantum_anomalies():
    """Quantum Walk anomaly detection across the network graph."""
    topo = build_topology_from_golden_configs()
    from collections import defaultdict
    adj = defaultdict(set)
    for link in topo["links"]:
        adj[link["source"]].add(link["target"])
        adj[link["target"]].add(link["source"])
    roles = {n["id"]: n.get("role", "unknown") for n in topo["nodes"]}
    try:
        result = detect_anomalies(dict(adj), roles)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/quantum/communities")
def api_quantum_communities():
    """Louvain community detection for topology clustering."""
    topo = build_topology_from_golden_configs()
    from collections import defaultdict
    adj = defaultdict(set)
    for link in topo["links"]:
        adj[link["source"]].add(link["target"])
        adj[link["target"]].add(link["source"])
    try:
        result = LouvainCommunityDetector(dict(adj)).detect()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/quantum/spof")
def api_quantum_spof():
    """Tarjan's O(V+E) articulation point + bridge detection."""
    topo = build_topology_from_golden_configs()
    from collections import defaultdict
    adj = defaultdict(set)
    for link in topo["links"]:
        adj[link["source"]].add(link["target"])
        adj[link["target"]].add(link["source"])
    try:
        spof, bridges = TarjanSPOF(dict(adj)).find_all()
        return jsonify({
            "single_points_of_failure": spof,
            "critical_links": [{"source": u, "target": v} for u, v in bridges],
            "spof_count": len(spof),
            "bridge_count": len(bridges),
            "algorithm": "Tarjan O(V+E)"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/quantum/benchmark")
def api_quantum_benchmark():
    """Benchmark quantum engine on synthetic graph."""
    node_count = int(request.args.get("nodes", 2000))
    avg_degree = int(request.args.get("degree", 3))
    node_count = min(node_count, 10000)  # Safety cap
    try:
        result = quantum_benchmark(node_count, avg_degree)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/audit-history")
def api_audit_history():
    return jsonify(get_audit_history())

@app.route("/api/conversations")
def api_conversations():
    return jsonify(get_conversations())

@app.route("/api/templates")
def api_templates():
    templates = []
    if TEMPLATES_DIR.exists():
        for fname in sorted(TEMPLATES_DIR.iterdir()):
            if fname.suffix in (".j2", ".jinja2"):
                templates.append({
                    "name": fname.stem,
                    "filename": fname.name,
                    "content": fname.read_text(),
                    "lines": len(fname.read_text().splitlines())
                })
    return jsonify(templates)

@app.route("/api/config")
def api_config():
    cfg = load_config()
    if "mcp" in cfg:
        cfg["mcp"].pop("url", None)
    return jsonify(cfg)

@app.route("/api/logs")
def api_logs():
    log_files = []
    if LOGS_DIR.exists():
        for fname in sorted(LOGS_DIR.iterdir(), reverse=True):
            if fname.suffix == ".log":
                content = fname.read_text()
                log_files.append({
                    "filename": fname.name,
                    "size": len(content),
                    "lines": len(content.splitlines()),
                    "last_modified": datetime.fromtimestamp(fname.stat().st_mtime).isoformat()
                })
    return jsonify(log_files)

@app.route("/api/network-stats")
def api_network_stats():
    topo = build_topology_from_golden_configs()
    stats = calculate_network_stats_v2(topo)
    return jsonify({
        "total_nodes": stats.get("total_nodes", 0),
        "total_links": stats.get("total_links", 0),
        "diameter": stats.get("graph_diameter", 0),
        "redundancy_score": stats.get("redundancy_score", 0) / 100.0 if stats.get("redundancy_score", 0) > 1 else stats.get("redundancy_score", 0),
        "single_points_of_failure": stats.get("single_points_of_failure", []),
        "critical_links": stats.get("critical_links", []),
        "high_risk_nodes": stats.get("high_risk_nodes", []),
        "communities": stats.get("communities", 0),
        "computation_time_ms": stats.get("computation_time_ms", 0),
        "avg_degree": stats.get("avg_degree", 0),
        "max_degree": stats.get("max_degree", 0),
        "min_degree": stats.get("min_degree", 0),
        "avg_path_length": stats.get("avg_path_length", 0),
        "connectivity": stats.get("connectivity", "unknown")
    })

# ── MCP Live Device Polling ───────────────────────────────────

@app.route("/api/mcp/execute", methods=["POST"])
def api_mcp_execute():
    """Execute a Junos command on a router via MCP."""
    data = request.json or {}
    router = data.get("router", "")
    command = data.get("command", "")
    if not router or not command:
        return jsonify({"error": "router and command required"}), 400
    try:
        result = run_async(mcp_execute_command(router, command))
        return jsonify({"router": router, "command": command, "output": result, "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/mcp/batch", methods=["POST"])
def api_mcp_batch():
    """Execute a command on multiple routers via MCP batch."""
    data = request.json or {}
    routers = data.get("routers", [])
    command = data.get("command", "")
    if not routers or not command:
        return jsonify({"error": "routers and command required"}), 400
    try:
        result = run_async(mcp_execute_batch(command, routers))
        return jsonify({"routers": routers, "command": command, "output": result, "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/mcp/facts/<router>")
def api_mcp_facts(router):
    """Get device facts from a router via MCP."""
    try:
        result = run_async(mcp_get_facts(router))
        return jsonify({"router": router, "facts": result, "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/mcp/live-config/<router>")
def api_mcp_live_config(router):
    """Get running config from router via MCP and diff against golden."""
    try:
        running = run_async(mcp_get_config(router))
        diff = get_config_diff(router, running)
        return jsonify({
            "router": router, "running_config": running,
            "diff": diff, "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/mcp/deploy-config", methods=["POST"])
def api_mcp_deploy_config():
    """Deploy configuration to a router via MCP."""
    data = request.json or {}
    router = data.get("router", "")
    config_text = data.get("config", "")
    comment = data.get("comment", "NOC WebUI Deployment")
    if not router or not config_text:
        return jsonify({"error": "router and config required"}), 400
    try:
        result = run_async(mcp_load_config(router, config_text, comment))
        return jsonify({"router": router, "result": result, "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/mcp/poll-status", methods=["POST"])
def api_mcp_poll_status():
    """Poll live status from all devices for dashboard."""
    try:
        devices = load_devices()
        router_names = list(devices.keys())
        result = run_async(mcp_execute_batch("show system uptime | display json", router_names))
        return jsonify({"output": result, "routers": router_names, "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/mcp/live-devices", methods=["GET"])
def api_mcp_live_devices():
    """Discover live devices from MCP server and return their reachability status.

    Returns structured per-device data indicating which routers are live vs unreachable,
    merged with golden config topology data when available.
    """
    result = {
        "live_devices": [],
        "unreachable": [],
        "data_source": "offline",  # 'live', 'offline', or 'mixed'
        "mcp_connected": False,
        "timestamp": datetime.now().isoformat()
    }

    # 1. Get devices registered in MCP
    devices = load_devices()
    router_names = list(devices.keys())

    if not router_names:
        # No devices registered at all — fall back to golden configs
        topo = build_topology_from_golden_configs()
        result["live_devices"] = [
            {"name": n["id"], "ip": n.get("loopback", ""), "role": n.get("role", "P"),
             "status": "config-only", "source": "golden_config"}
            for n in topo.get("nodes", [])
        ]
        result["data_source"] = "offline"
        return jsonify(result)

    # 2. Try to poll via MCP
    try:
        raw = run_async(mcp_execute_batch("show system information | display json", router_names))
        result["mcp_connected"] = True

        # Parse MCP batch response
        try:
            batch_data = json.loads(raw) if isinstance(raw, str) else raw
        except (json.JSONDecodeError, TypeError):
            batch_data = {}

        # Determine per-device status from batch results
        if isinstance(batch_data, dict):
            # Batch response format: { "results": { "router": { ... } } } or per-key
            results_map = batch_data.get("results", batch_data)
            for rname in router_names:
                dev_info = {"name": rname, "ip": devices[rname].get("ip", ""),
                            "role": "PE" if rname.upper().startswith("PE") else ("RR" if rname in ("P12", "P22") else "P")}
                rdata = results_map.get(rname, "")
                rdata_str = str(rdata) if not isinstance(rdata, str) else rdata
                if rdata_str and "Error" not in rdata_str and "error" not in rdata_str.lower()[:50]:
                    dev_info["status"] = "live"
                    dev_info["source"] = "mcp"
                    result["live_devices"].append(dev_info)
                else:
                    dev_info["status"] = "unreachable"
                    dev_info["source"] = "mcp"
                    result["unreachable"].append(dev_info)
        else:
            # Fallback: treat all as status-unknown
            for rname in router_names:
                result["live_devices"].append({
                    "name": rname, "ip": devices[rname].get("ip", ""),
                    "role": "PE" if rname.upper().startswith("PE") else ("RR" if rname in ("P12", "P22") else "P"),
                    "status": "unknown", "source": "mcp"
                })

        result["data_source"] = "live"
    except Exception as e:
        logger.warning(f"MCP live-devices poll failed: {e}")
        # MCP batch failed — routers unreachable but MCP server may still be up
        # Mark all devices as unreachable via MCP
        result["mcp_connected"] = True  # MCP server itself responded
        for rname in router_names:
            result["unreachable"].append({
                "name": rname, "ip": devices[rname].get("ip", ""),
                "role": "PE" if rname.upper().startswith("PE") else ("RR" if rname in ("P12", "P22") else "P"),
                "status": "unreachable", "source": "mcp"
            })
        result["data_source"] = "live"  # We tried live — devices are just down

    return jsonify(result)

# ── Template Rendering & Deployment ───────────────────────────

@app.route("/api/templates/render", methods=["POST"])
def api_template_render():
    """Render a Jinja2 template with variables."""
    data = request.json or {}
    template_name = data.get("template", "")
    variables = data.get("variables", {})
    tmpl_path = TEMPLATES_DIR / f"{template_name}.j2"
    if not tmpl_path.exists():
        # Try with .jinja2 extension
        tmpl_path = TEMPLATES_DIR / f"{template_name}.jinja2"
    if not tmpl_path.exists():
        return jsonify({"error": f"Template '{template_name}' not found"}), 404
    try:
        env = Environment(loader=BaseLoader())
        tmpl = env.from_string(tmpl_path.read_text())
        rendered = tmpl.render(**variables)
        return jsonify({
            "template": template_name, "rendered": rendered,
            "lines": len(rendered.splitlines()), "variables_used": list(variables.keys())
        })
    except Exception as e:
        return jsonify({"error": f"Template render error: {e}"}), 400

@app.route("/api/templates/deploy", methods=["POST"])
def api_template_deploy():
    """Render a template and deploy to a router via MCP."""
    data = request.json or {}
    template_name = data.get("template", "")
    variables = data.get("variables", {})
    router = data.get("router", "")
    comment = data.get("comment", f"NOC Template: {template_name}")
    if not router:
        return jsonify({"error": "router required"}), 400
    # First render
    tmpl_path = TEMPLATES_DIR / f"{template_name}.j2"
    if not tmpl_path.exists():
        return jsonify({"error": f"Template '{template_name}' not found"}), 404
    try:
        env = Environment(loader=BaseLoader())
        tmpl = env.from_string(tmpl_path.read_text())
        rendered = tmpl.render(**variables)
        # Then deploy via MCP
        result = run_async(mcp_load_config(router, rendered, comment))
        return jsonify({
            "template": template_name, "router": router, "rendered": rendered,
            "deploy_result": result, "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ── Scheduled Tasks ───────────────────────────────────────────

@app.route("/api/scheduled-tasks")
def api_scheduled_tasks():
    """List all scheduled tasks."""
    conn = sqlite3.connect(str(SCHEDULED_DB))
    conn.row_factory = sqlite3.Row
    tasks = conn.execute("SELECT * FROM scheduled_tasks ORDER BY created_at DESC").fetchall()
    conn.close()
    return jsonify([dict(t) for t in tasks])

@app.route("/api/scheduled-tasks", methods=["POST"])
def api_create_scheduled_task():
    """Create a new scheduled task."""
    data = request.json or {}
    name = data.get("name", "")
    task_type = data.get("task_type", "command")
    schedule = data.get("schedule", "1h")
    routers = json.dumps(data.get("routers", []))
    command = data.get("command", "")
    if not name or not command:
        return jsonify({"error": "name and command required"}), 400
    next_run = calculate_next_run(schedule)
    conn = sqlite3.connect(str(SCHEDULED_DB))
    conn.execute(
        "INSERT INTO scheduled_tasks (name, task_type, schedule, target_routers, command, next_run) VALUES (?,?,?,?,?,?)",
        (name, task_type, schedule, routers, command, next_run)
    )
    conn.commit()
    task_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return jsonify({"id": task_id, "name": name, "next_run": next_run})

@app.route("/api/scheduled-tasks/<int:task_id>", methods=["DELETE"])
def api_delete_scheduled_task(task_id):
    """Delete a scheduled task."""
    conn = sqlite3.connect(str(SCHEDULED_DB))
    conn.execute("DELETE FROM scheduled_tasks WHERE id=?", (task_id,))
    conn.execute("DELETE FROM task_history WHERE task_id=?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"deleted": task_id})

@app.route("/api/scheduled-tasks/<int:task_id>/toggle", methods=["POST"])
def api_toggle_scheduled_task(task_id):
    """Enable/disable a scheduled task."""
    conn = sqlite3.connect(str(SCHEDULED_DB))
    conn.execute("UPDATE scheduled_tasks SET enabled = CASE WHEN enabled=1 THEN 0 ELSE 1 END WHERE id=?", (task_id,))
    conn.commit()
    row = conn.execute("SELECT enabled FROM scheduled_tasks WHERE id=?", (task_id,)).fetchone()
    conn.close()
    return jsonify({"id": task_id, "enabled": row[0] if row else 0})

@app.route("/api/scheduled-tasks/<int:task_id>/run", methods=["POST"])
def api_run_scheduled_task_now(task_id):
    """Run a scheduled task immediately."""
    conn = sqlite3.connect(str(SCHEDULED_DB))
    conn.row_factory = sqlite3.Row
    task = conn.execute("SELECT * FROM scheduled_tasks WHERE id=?", (task_id,)).fetchone()
    conn.close()
    if not task:
        return jsonify({"error": "Task not found"}), 404
    task_dict = dict(task)
    routers = json.loads(task_dict["target_routers"])
    command = task_dict["command"]
    start = time.time()
    try:
        if len(routers) == 1:
            result = run_async(mcp_execute_command(routers[0], command))
        else:
            result = run_async(mcp_execute_batch(command, routers))
        status = "success"
    except Exception as e:
        result = str(e)
        status = "error"
    duration = int((time.time() - start) * 1000)
    now = datetime.now().isoformat()
    conn = sqlite3.connect(str(SCHEDULED_DB))
    conn.execute("UPDATE scheduled_tasks SET last_run=?, last_result=?, run_count=run_count+1 WHERE id=?",
                 (now, result[:5000], task_id))
    conn.execute("INSERT INTO task_history (task_id, run_at, result, status, duration_ms) VALUES (?,?,?,?,?)",
                 (task_id, now, result[:5000], status, duration))
    conn.commit()
    conn.close()
    return jsonify({"task_id": task_id, "status": status, "result": result[:3000], "duration_ms": duration})

@app.route("/api/scheduled-tasks/<int:task_id>/history")
def api_task_history(task_id):
    """Get history of a scheduled task."""
    conn = sqlite3.connect(str(SCHEDULED_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM task_history WHERE task_id=? ORDER BY run_at DESC LIMIT 20", (task_id,)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

# ── Workflow Engine ───────────────────────────────────────────

@app.route("/api/workflows")
def api_list_workflows():
    """List all saved workflows."""
    return jsonify(load_workflows())

@app.route("/api/workflows", methods=["POST"])
def api_save_workflow():
    """Save a workflow."""
    data = request.json or {}
    if not data.get("name"):
        return jsonify({"error": "name required"}), 400
    path = save_workflow(data)
    return jsonify({"saved": path, "name": data["name"]})

@app.route("/api/workflows/<name>", methods=["DELETE"])
def api_delete_workflow(name):
    """Delete a workflow."""
    safe = re.sub(r'[^\w\-]', '_', name)
    path = WORKFLOWS_DIR / f"{safe}.json"
    if path.exists():
        path.unlink()
        return jsonify({"deleted": name})
    return jsonify({"error": "Not found"}), 404

@app.route("/api/workflows/execute", methods=["POST"])
def api_execute_workflow():
    """Execute a workflow (delegates to v2 with enhanced step types)."""
    data = request.json or {}
    if not data.get("steps"):
        return jsonify({"error": "steps required"}), 400
    try:
        # Use v2 executor which supports all step types
        results = run_async(execute_workflow_v2(data))
        return jsonify({"workflow": data.get("name", "unnamed"), "results": results,
                        "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ── Log Viewer ────────────────────────────────────────────────

@app.route("/api/logs/<filename>")
def api_log_content(filename):
    """Get contents of a log file with optional filtering."""
    safe_name = Path(filename).name
    log_path = LOGS_DIR / safe_name
    if not log_path.exists():
        return jsonify({"error": "Not found"}), 404
    content = log_path.read_text()
    level_filter = request.args.get("level", "").upper()
    search = request.args.get("search", "")
    tail = int(request.args.get("tail", 0))
    lines = content.splitlines()
    if level_filter:
        lines = [l for l in lines if f"[{level_filter}]" in l]
    if search:
        lines = [l for l in lines if search.lower() in l.lower()]
    if tail > 0:
        lines = lines[-tail:]
    return jsonify({
        "filename": safe_name, "lines": lines, "total_lines": len(content.splitlines()),
        "filtered_lines": len(lines)
    })

# ── AI Chat (Ollama Connected) ────────────────────────────────

@app.route("/api/ai/chat", methods=["POST"])
def api_ai_chat():
    """Send a message to the AI and get a response."""
    data = request.json or {}
    message = data.get("message", "")
    history = data.get("history", [])
    if not message:
        return jsonify({"error": "message required"}), 400
    
    # Build system prompt
    topo = build_topology_from_golden_configs()
    stats = calculate_network_stats_v2(topo)
    system_prompt = f"""You are the Junos AI Network Operations Center assistant.
You have access to a network with {stats.get('total_nodes', 0)} Junos routers:
- PE Routers: {stats.get('pe_count', 0)} (Provider Edge — customer-facing)
- P Routers: {stats.get('p_count', 0)} (Provider core)  
- Route Reflectors: {stats.get('rr_count', 0)} (iBGP RR — P12, P22)
- Physical Links: {stats.get('total_links', 0)}
- Protocols: IS-IS L2, iBGP, LDP, MPLS, L3VPN (VPN-A on PE routers)
- Graph Diameter: {stats.get('graph_diameter', 0)}, Redundancy: {stats.get('redundancy_score', 0)}%
- SPOFs: {', '.join(stats.get('single_points_of_failure', [])) or 'None'}

Device list: {', '.join(n['id'] for n in topo['nodes'])}

You can help with:
1. Network topology analysis and troubleshooting
2. Configuration review and best practices
3. IS-IS, BGP, MPLS, LDP, VPN questions
4. Shortest path analysis between routers
5. Security hardening recommendations
6. Performance optimization

Respond concisely using Markdown formatting. Use code blocks for configs/commands."""

    messages = [{"role": "system", "content": system_prompt}]
    for h in history[-10:]:
        messages.append({"role": h.get("role", "user"), "content": h.get("content", "")})
    messages.append({"role": "user", "content": message})
    
    try:
        result = run_async(ollama_chat_async(messages))
        response = result.get("message", {}).get("content", "No response from AI engine")
        return jsonify({
            "response": response,
            "model": OLLAMA_MODEL,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"AI chat error: {e}")
        return jsonify({"error": f"AI engine unavailable: {e}", "fallback": True}), 503

@app.route("/api/ai/stream", methods=["POST"])
def api_ai_stream():
    """Stream AI response token by token (SSE) with queue-based true streaming."""
    import queue, threading
    
    data = request.json or {}
    message = data.get("message", "")
    history = data.get("history", [])
    
    topo = build_topology_from_golden_configs()
    stats = calculate_network_stats_v2(topo)
    system_prompt = f"""You are the Junos AI NOC assistant — a Principal Juniper Network Engineer (JNCIE-SP level).
Network: {stats.get('total_nodes',0)} routers ({stats.get('pe_count',0)} PE, {stats.get('p_count',0)} P, {stats.get('rr_count',0)} RR).
Topology: Dual-plane IS-IS L2, full-mesh iBGP with route reflectors (P12, P22), LDP, RSVP-TE, MPLS, L3VPN.
Devices: {', '.join(n['id'] for n in topo.get('nodes', []))}.
Answer concisely in Markdown. Use technical precision."""
    
    messages = [{"role": "system", "content": system_prompt}]
    for h in history[-10:]:
        messages.append({"role": h.get("role", "user"), "content": h.get("content", "")})
    messages.append({"role": "user", "content": message})
    
    token_queue = queue.Queue()
    
    def _async_producer():
        """Run in a background thread — streams tokens into queue."""
        loop = asyncio.new_event_loop()
        try:
            payload = {
                "model": OLLAMA_MODEL,
                "messages": messages,
                "stream": True,
                "options": {"num_ctx": OLLAMA_NUM_CTX, "temperature": OLLAMA_TEMPERATURE}
            }
            async def _run():
                async with httpx.AsyncClient(timeout=600.0) as client:
                    async with client.stream("POST", f"{OLLAMA_URL}/api/chat", json=payload) as resp:
                        async for line in resp.aiter_lines():
                            if line.strip():
                                try:
                                    chunk = json.loads(line)
                                    token = chunk.get("message", {}).get("content", "")
                                    done = chunk.get("done", False)
                                    if token:
                                        token_queue.put(json.dumps({"token": token}))
                                    if done:
                                        token_queue.put(json.dumps({"done": True}))
                                        return
                                except json.JSONDecodeError:
                                    continue
            loop.run_until_complete(_run())
        except Exception as e:
            token_queue.put(json.dumps({"error": str(e)}))
        finally:
            token_queue.put(None)  # sentinel
            loop.close()
    
    # Start async producer in background thread
    threading.Thread(target=_async_producer, daemon=True).start()
    
    def generate():
        """Synchronous generator — yields SSE events from queue in real-time."""
        while True:
            item = token_queue.get()
            if item is None:
                break
            yield f"data: {item}\n\n"
    
    return Response(generate(), mimetype='text/event-stream',
                    headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})

@app.route("/api/ai/analyze", methods=["POST"])
def api_ai_analyze():
    """AI-powered analysis of data (config, output, etc.)."""
    data = request.json or {}
    content = data.get("data", "")
    question = data.get("question", "Analyze this data")
    system = data.get("system", "You are a Junos network expert. Analyze the following data and provide insights.")
    if not content:
        return jsonify({"error": "data required"}), 400
    try:
        result = run_async(ollama_analyze_async(system, content, question))
        return jsonify({"analysis": result, "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 503

# ── MCP Health Check ──────────────────────────────────────────

@app.route("/api/health")
def api_health():
    """Check connectivity to MCP server and Ollama."""
    health = {"mcp": "unknown", "ollama": "unknown", "timestamp": datetime.now().isoformat()}
    # Check MCP
    try:
        result = run_async(mcp_get_router_list())
        health["mcp"] = "connected" if result and "Error" not in result else "error"
        health["mcp_routers"] = result
    except Exception as e:
        health["mcp"] = f"error: {e}"
    # Check Ollama
    try:
        resp = httpx.get(f"{OLLAMA_URL}/api/tags", timeout=5.0)
        models = resp.json().get("models", [])
        health["ollama"] = "connected"
        health["ollama_model"] = OLLAMA_MODEL
        health["ollama_models"] = json.dumps([m.get("name", "") for m in models])
    except Exception as e:
        health["ollama"] = f"error: {e}"
    return jsonify(health)

@app.route("/api/ai/models")
def api_ai_models():
    """List available Ollama models and the active model."""
    try:
        resp = httpx.get(f"{OLLAMA_URL}/api/tags", timeout=5.0)
        models = [m.get("name", "") for m in resp.json().get("models", [])]
        return jsonify({"active": OLLAMA_MODEL, "models": models, "ollama_url": OLLAMA_URL})
    except Exception as e:
        return jsonify({"active": OLLAMA_MODEL, "models": [], "error": str(e), "ollama_url": OLLAMA_URL})


# ══════════════════════════════════════════════════════════════
#  HYPERED BRAIN API — Agentic Investigation Engine (Phase 1)
#  Bridges the 6-layer Brain + 7-stage Reasoning Engine to Web UI
# ══════════════════════════════════════════════════════════════

# ── Import Brain & Reasoning Engine (local modules) ──
try:
    from hypered_brain import (
        hypered_brain_analyze, quick_brain_analyze,
        SMART_SCRIPTS, select_scripts_for_query,
        BrainState, BrainLayer, FactAccumulator,
    )
    _BRAIN_AVAILABLE = True
    logger.info("Hypered Brain engine loaded successfully")
except ImportError as _e:
    _BRAIN_AVAILABLE = False
    logger.warning(f"Hypered Brain not available: {_e}")

try:
    from reasoning_engine import classify_problem, ProblemDomain, Complexity
    _REASONING_AVAILABLE = True
    logger.info("Reasoning Engine loaded successfully")
except ImportError as _e:
    _REASONING_AVAILABLE = False
    logger.warning(f"Reasoning Engine not available: {_e}")

# ── RAG Knowledge Base (local vector store) ──
_kb_store = None


def _init_kb_store():
    """Initialize the knowledge base vector store (lazy, local-only)."""
    global _kb_store
    if _kb_store is not None:
        return _kb_store
    try:
        from kb_vectorstore import KBVectorStore
        _kb_store = run_async(KBVectorStore.create())
        logger.info(f"KB VectorStore loaded: {len(_kb_store.chunks)} chunks")
    except Exception as e:
        logger.warning(f"KB VectorStore not available: {e}")
    return _kb_store


# ── Query Classification ──
def classify_query_web(message: str) -> dict:
    """Classify a user query for routing (knowledge vs status vs troubleshoot vs config)."""
    msg_lower = message.lower()

    # Knowledge questions — pure RAG retrieval, no MCP tools needed
    _knowledge_patterns = [
        r'\b(what is|explain|describe|how does|tell me about|define|difference between)\b',
        r'\b(what are|overview of|concept of|meaning of|purpose of)\b',
    ]
    for p in _knowledge_patterns:
        if re.search(p, msg_lower):
            return {"type": "knowledge", "confidence": 0.85}

    # Config requests — need safety gates
    _config_patterns = [
        r'\b(configure|deploy|push|apply|set |delete |deactivate|commit)\b',
        r'\b(add .* to|remove .* from|create .* on|enable .* on)\b',
    ]
    for p in _config_patterns:
        if re.search(p, msg_lower):
            return {"type": "config", "confidence": 0.8}

    # Troubleshoot — needs full brain investigation
    _troubleshoot_patterns = [
        r'\b(why is|troubleshoot|diagnose|investigate|fix|down|flap|error|fail|broken)\b',
        r'\b(root cause|not working|issue|problem|can\'t reach|unreachable)\b',
    ]
    for p in _troubleshoot_patterns:
        if re.search(p, msg_lower):
            devices_mentioned = []
            topo = build_topology_from_golden_configs()
            for n in topo.get("nodes", []):
                if n["id"].lower() in msg_lower:
                    devices_mentioned.append(n["id"])
            return {"type": "troubleshoot", "confidence": 0.85, "devices": devices_mentioned}

    # Status check — needs MCP but not full investigation
    _status_patterns = [
        r'\b(check|show|status|health|state|verify|list|get)\b',
    ]
    for p in _status_patterns:
        if re.search(p, msg_lower):
            devices_mentioned = []
            topo = build_topology_from_golden_configs()
            for n in topo.get("nodes", []):
                if n["id"].lower() in msg_lower:
                    devices_mentioned.append(n["id"])
            return {"type": "status", "confidence": 0.75, "devices": devices_mentioned}

    return {"type": "general", "confidence": 0.5}


# ── Brain-compatible MCP wrapper functions ──
async def _brain_run_batch(client, sid, cmd, routers, label=""):
    """Wrapper for brain's run_batch_fn — routes through our MCP bridge."""
    return await mcp_execute_batch(cmd, routers)


async def _brain_run_single(client, sid, cmd, router, label=""):
    """Wrapper for brain's run_single_fn — routes through our MCP bridge."""
    return await mcp_execute_command(router, cmd)


async def _brain_ai_analyze(system_prompt, data, question, include_kb=False):
    """Wrapper for brain's ai_analyze_fn — routes through Ollama with optional RAG."""
    context_data = data
    if include_kb:
        store = _init_kb_store()
        if store:
            try:
                chunks = await store.retrieve(question, top_k=3)
                if chunks:
                    rag_context = "\n\nREFERENCE KNOWLEDGE:\n" + "\n---\n".join(
                        [c.get("text", "") for c in chunks]
                    )
                    context_data = data + rag_context
            except Exception:
                pass
    return await ollama_analyze_async(system_prompt, context_data, question)


@app.route("/api/brain/status")
def api_brain_status():
    """Check Brain engine availability and capabilities."""
    return jsonify({
        "brain_available": _BRAIN_AVAILABLE,
        "reasoning_available": _REASONING_AVAILABLE,
        "rag_available": _init_kb_store() is not None,
        "smart_scripts": len(SMART_SCRIPTS) if _BRAIN_AVAILABLE else 0,
        "brain_version": "18.0",
        "capabilities": {
            "investigate": _BRAIN_AVAILABLE,
            "classify": _REASONING_AVAILABLE,
            "rag_retrieval": _init_kb_store() is not None,
            "quick_analysis": _BRAIN_AVAILABLE,
        },
        "timestamp": datetime.now().isoformat()
    })


@app.route("/api/brain/scripts")
def api_brain_scripts():
    """List all available Smart Scripts with categories and commands."""
    if not _BRAIN_AVAILABLE:
        return jsonify({"error": "Brain engine not available"}), 503
    scripts = []
    for sid, s in SMART_SCRIPTS.items():
        scripts.append({
            "id": sid, "name": s.name, "category": s.category.value,
            "commands": s.commands, "depends_on": s.depends_on,
            "description": s.description, "priority": s.priority,
        })
    return jsonify({"scripts": scripts, "total": len(scripts)})


@app.route("/api/brain/scripts/select", methods=["POST"])
def api_brain_scripts_select():
    """Select appropriate scripts for a query (perception layer)."""
    if not _BRAIN_AVAILABLE:
        return jsonify({"error": "Brain engine not available"}), 503
    data = request.json or {}
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "query required"}), 400
    topo = build_topology_from_golden_configs()
    devices = [n["id"] for n in topo.get("nodes", [])]
    selected = select_scripts_for_query(query)
    return jsonify({
        "query": query,
        "selected_scripts": [{"id": s.id, "name": s.name, "category": s.category.value} for s in selected],
        "total_selected": len(selected),
    })


@app.route("/api/brain/classify", methods=["POST"])
def api_brain_classify():
    """Classify a query using the Reasoning Engine."""
    data = request.json or {}
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "query required"}), 400
    web_class = classify_query_web(query)
    reasoning_class = {}
    if _REASONING_AVAILABLE:
        try:
            result = classify_problem(query)
            reasoning_class = {
                "domain": result.domain.value if hasattr(result.domain, 'value') else str(result.domain),
                "complexity": result.complexity.value if hasattr(result.complexity, 'value') else str(result.complexity),
                "protocols": result.protocols_involved,
                "devices": result.devices_mentioned,
                "osi_layers": result.osi_layers,
            }
        except Exception as e:
            reasoning_class = {"error": str(e)}
    return jsonify({
        "web_classification": web_class,
        "reasoning_classification": reasoning_class,
        "timestamp": datetime.now().isoformat()
    })


@app.route("/api/brain/investigate", methods=["POST"])
def api_brain_investigate():
    """Run a full Hypered Brain investigation with WebSocket progress events."""
    if not _BRAIN_AVAILABLE:
        return jsonify({"error": "Brain engine not available. Check hypered_brain.py import."}), 503
    data = request.json or {}
    query = data.get("query", "")
    mode = data.get("mode", "full")  # "full" or "quick"
    target_devices = data.get("devices", [])
    if not query:
        return jsonify({"error": "query required"}), 400

    topo = build_topology_from_golden_configs()
    all_devices = [n["id"] for n in topo.get("nodes", [])]
    if not target_devices:
        classification = classify_query_web(query)
        target_devices = classification.get("devices", all_devices)
    if not target_devices:
        target_devices = all_devices
    device_map = {d: d for d in target_devices}

    socketio.emit("brain_progress", {
        "event": "investigation_start", "query": query, "mode": mode,
        "devices": target_devices, "timestamp": datetime.now().isoformat()
    })

    def _progress_console(msg, **kwargs):
        msg_str = str(msg)
        if "Layer 0:" in msg_str or "PERCEPTION" in msg_str:
            socketio.emit("brain_progress", {"event": "layer_change", "layer": "perception"})
        elif "Layer 1:" in msg_str or "EXECUTION" in msg_str:
            socketio.emit("brain_progress", {"event": "layer_change", "layer": "execution"})
        elif "Layer 2:" in msg_str or "ANALYSIS" in msg_str:
            socketio.emit("brain_progress", {"event": "layer_change", "layer": "analysis"})
        elif "Layer 3:" in msg_str or "VALIDATION" in msg_str:
            socketio.emit("brain_progress", {"event": "layer_change", "layer": "validation"})
        elif "Layer 4:" in msg_str or "SYNTHESIS" in msg_str:
            socketio.emit("brain_progress", {"event": "layer_change", "layer": "synthesis"})
        elif "scripts selected" in msg_str.lower():
            socketio.emit("brain_progress", {"event": "scripts_selected", "detail": msg_str})
        elif "confidence" in msg_str.lower():
            socketio.emit("brain_progress", {"event": "confidence_update", "detail": msg_str})
        elif "PROBE" in msg_str or "probe" in msg_str:
            socketio.emit("brain_progress", {"event": "probe_executing", "detail": msg_str})
        socketio.emit("brain_log", {"message": msg_str})

    start_time = time.time()
    try:
        if mode == "quick":
            result = run_async(quick_brain_analyze(
                query=query, device_map=device_map, mcp_client=None, session_id="",
                run_batch_fn=_brain_run_batch, run_single_fn=_brain_run_single,
                ai_analyze_fn=_brain_ai_analyze, console_fn=_progress_console,
                max_concurrent=3, available_devices=target_devices,
            ))
        else:
            result = run_async(hypered_brain_analyze(
                query=query, device_map=device_map, mcp_client=None, session_id="",
                run_batch_fn=_brain_run_batch, run_single_fn=_brain_run_single,
                ai_analyze_fn=_brain_ai_analyze, console_fn=_progress_console,
                max_concurrent=3, available_devices=target_devices,
            ))
        duration_ms = int((time.time() - start_time) * 1000)

        # Save to investigation history
        try:
            conn = sqlite3.connect(str(_INVESTIGATION_DB))
            conn.execute(
                "INSERT INTO investigations (query, classification, devices, response, mode, duration_ms) VALUES (?,?,?,?,?,?)",
                (query, mode,
                 json.dumps(target_devices), result[:5000], mode, duration_ms)
            )
            conn.commit()
            conn.close()
        except Exception:
            pass

        socketio.emit("brain_progress", {
            "event": "investigation_complete", "query": query,
            "duration_ms": duration_ms, "timestamp": datetime.now().isoformat()
        })
        return jsonify({
            "response": result, "mode": mode, "devices": target_devices,
            "query": query, "engine": "hypered_brain_v18",
            "duration_ms": duration_ms, "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Brain investigation error: {e}")
        socketio.emit("brain_progress", {"event": "investigation_error", "error": str(e)})
        return jsonify({"error": str(e)}), 503


@app.route("/api/brain/rag", methods=["POST"])
def api_brain_rag():
    """Query the local RAG knowledge base for relevant knowledge chunks."""
    data = request.json or {}
    query = data.get("query", "")
    top_k = data.get("top_k", 5)
    if not query:
        return jsonify({"error": "query required"}), 400
    store = _init_kb_store()
    if not store:
        return jsonify({"error": "Knowledge base not available. Run kb_vectorstore.py first."}), 503
    try:
        chunks = run_async(store.retrieve(query, top_k=top_k))
        return jsonify({
            "query": query, "chunks": chunks, "total": len(chunks),
            "kb_chunks_total": len(store.chunks), "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 503


# ══════════════════════════════════════════════════════════════
#  AGENTIC CHAT — AI with Brain + RAG + MCP Tool Calling
# ══════════════════════════════════════════════════════════════

@app.route("/api/ai/chat-agentic", methods=["POST"])
def api_ai_chat_agentic():
    """Full agentic AI chat — classifies query, routes to Brain/RAG/MCP.
    All processing is LOCAL: Ollama + MCP + RAG — zero external calls.
    """
    data = request.json or {}
    message = data.get("message", "")
    history = data.get("history", [])
    if not message:
        return jsonify({"error": "message required"}), 400

    classification = classify_query_web(message)
    query_type = classification.get("type", "general")
    socketio.emit("ai_thinking", {"stage": "classifying", "type": query_type})

    response_data = {
        "classification": classification, "model": OLLAMA_MODEL,
        "engine": "local_only", "timestamp": datetime.now().isoformat()
    }

    try:
        if query_type == "knowledge":
            socketio.emit("ai_thinking", {"stage": "rag_retrieval"})
            rag_context = ""
            sources = []
            store = _init_kb_store()
            if store:
                try:
                    chunks = run_async(store.retrieve(message, top_k=5))
                    rag_context = "\n\nREFERENCE KNOWLEDGE:\n" + "\n---\n".join(
                        [c.get("text", "") for c in chunks]
                    )
                    sources = [{"heading": c.get("heading", ""), "score": c.get("score", 0)} for c in chunks]
                except Exception:
                    pass

            system_prompt = (
                "You are a JNCIE-SP certified Junos expert. Answer using ONLY the reference knowledge provided. "
                "If the knowledge doesn't cover the question, say so. Use Markdown formatting."
            )
            messages = [{"role": "system", "content": system_prompt}]
            for h in history[-6:]:
                messages.append({"role": h.get("role", "user"), "content": h.get("content", "")})
            messages.append({"role": "user", "content": message + rag_context})
            result = run_async(ollama_chat_async(messages))
            response_data["response"] = result.get("message", {}).get("content", "No response")
            response_data["sources"] = sources
            response_data["type"] = "knowledge"

        elif query_type == "troubleshoot" and _BRAIN_AVAILABLE:
            socketio.emit("ai_thinking", {"stage": "brain_investigation", "devices": classification.get("devices", [])})
            topo = build_topology_from_golden_configs()
            all_devices = [n["id"] for n in topo.get("nodes", [])]
            target_devices = classification.get("devices", []) or all_devices[:5]
            device_map = {d: d for d in target_devices}

            def _console_ws(msg, **kwargs):
                socketio.emit("brain_log", {"message": str(msg)})

            brain_result = run_async(hypered_brain_analyze(
                query=message, device_map=device_map, mcp_client=None, session_id="",
                run_batch_fn=_brain_run_batch, run_single_fn=_brain_run_single,
                ai_analyze_fn=_brain_ai_analyze, console_fn=_console_ws,
                max_concurrent=3, available_devices=target_devices,
            ))
            response_data["response"] = brain_result
            response_data["type"] = "investigation"
            response_data["devices_checked"] = target_devices

        elif query_type == "status":
            socketio.emit("ai_thinking", {"stage": "status_check"})
            devices = classification.get("devices", [])
            if devices and _BRAIN_AVAILABLE:
                device_map = {d: d for d in devices}

                def _console_noop(msg, **kwargs):
                    pass

                brain_result = run_async(quick_brain_analyze(
                    query=message, device_map=device_map, mcp_client=None, session_id="",
                    run_batch_fn=_brain_run_batch, run_single_fn=_brain_run_single,
                    ai_analyze_fn=_brain_ai_analyze, console_fn=_console_noop,
                    max_concurrent=3, available_devices=devices,
                ))
                response_data["response"] = brain_result
                response_data["type"] = "quick_status"
                response_data["devices_checked"] = devices
            else:
                topo = build_topology_from_golden_configs()
                stats = calculate_network_stats_v2(topo)
                system_prompt = f"You are a Junos AI NOC assistant. Network has {stats.get('total_nodes', 0)} routers. Answer concisely."
                messages = [{"role": "system", "content": system_prompt}]
                for h in history[-8:]:
                    messages.append({"role": h.get("role", "user"), "content": h.get("content", "")})
                messages.append({"role": "user", "content": message})
                result = run_async(ollama_chat_async(messages))
                response_data["response"] = result.get("message", {}).get("content", "No response")
                response_data["type"] = "status"

        elif query_type == "config":
            socketio.emit("ai_thinking", {"stage": "config_safety_check"})
            system_prompt = (
                "You are a JNCIE-SP Junos configuration expert. "
                "When asked to configure something, generate the EXACT Junos set commands needed. "
                "ALWAYS include a WARNING section listing potential impacts. "
                "NEVER auto-deploy — just show the commands for review. "
                "Use Markdown code blocks for commands."
            )
            messages = [{"role": "system", "content": system_prompt}]
            for h in history[-6:]:
                messages.append({"role": h.get("role", "user"), "content": h.get("content", "")})
            messages.append({"role": "user", "content": message})
            result = run_async(ollama_chat_async(messages))
            response_data["response"] = result.get("message", {}).get("content", "No response")
            response_data["type"] = "config"
            response_data["requires_approval"] = True

        else:
            socketio.emit("ai_thinking", {"stage": "general_response"})
            rag_context = ""
            store = _init_kb_store()
            if store:
                try:
                    chunks = run_async(store.retrieve(message, top_k=3))
                    if chunks and chunks[0].get("score", 0) > 0.6:
                        rag_context = "\n\nREFERENCE:\n" + "\n---\n".join(
                            [c.get("text", "")[:500] for c in chunks[:2]]
                        )
                except Exception:
                    pass
            topo = build_topology_from_golden_configs()
            stats = calculate_network_stats_v2(topo)
            system_prompt = f"""You are the Junos AI NOC assistant — JNCIE-SP level.
Network: {stats.get('total_nodes',0)} routers. Devices: {', '.join(n['id'] for n in topo.get('nodes', []))}.
Answer concisely in Markdown."""
            messages = [{"role": "system", "content": system_prompt}]
            for h in history[-8:]:
                messages.append({"role": h.get("role", "user"), "content": h.get("content", "")})
            messages.append({"role": "user", "content": message + rag_context})
            result = run_async(ollama_chat_async(messages))
            response_data["response"] = result.get("message", {}).get("content", "No response")
            response_data["type"] = "general"

    except Exception as e:
        logger.error(f"Agentic chat error: {e}\n{traceback.format_exc()}")
        response_data["response"] = f"AI engine error: {str(e)}"
        response_data["type"] = "error"

    socketio.emit("ai_thinking", {"stage": "complete", "type": response_data.get("type")})
    return jsonify(response_data)


@app.route("/api/ai/quick-actions", methods=["POST"])
def api_ai_quick_actions():
    """Generate dynamic AI quick actions based on current context."""
    data = request.json or {}
    view = data.get("view", "dashboard")
    device = data.get("device", "")
    topo = build_topology_from_golden_configs()
    stats = calculate_network_stats_v2(topo)
    device_list = [n["id"] for n in topo.get("nodes", [])]

    actions = []
    actions.append({"label": "Network Health Check", "action": "investigate",
                    "query": "Run a full health check on all routers", "icon": "activity"})
    spofs = stats.get("single_points_of_failure", [])
    if spofs:
        actions.append({"label": f"SPOF Analysis ({len(spofs)} found)", "action": "investigate",
                        "query": f"Investigate single points of failure: {', '.join(spofs[:3])}", "icon": "alert-triangle"})

    if view == "topology":
        actions.append({"label": "Redundancy Assessment", "action": "investigate",
                        "query": "Analyze network redundancy and recommend improvements", "icon": "shield"})
    elif view == "configs":
        actions.append({"label": "Config Compliance Audit", "action": "investigate",
                        "query": "Run a security compliance audit on all golden configs", "icon": "clipboard-check"})
    elif view == "ai-chat":
        actions.append({"label": "Protocol Health Scan", "action": "investigate",
                        "query": "Check ISIS, BGP, LDP, and MPLS status across all routers", "icon": "scan"})

    if device and device in device_list:
        actions.append({"label": f"Deep Dive: {device}", "action": "investigate",
                        "query": f"Run a comprehensive investigation on {device}", "icon": "search"})
        actions.append({"label": f"Security Audit: {device}", "action": "investigate",
                        "query": f"Run a security hardening assessment on {device}", "icon": "shield"})

    return jsonify({"actions": actions[:8], "context": {"view": view, "device": device}})


# ══════════════════════════════════════════════════════════════
#  PHASE 2 — Confidence Scoring + Copilot Proactive Suggestions
# ══════════════════════════════════════════════════════════════

@app.route("/api/ai/copilot-suggest", methods=["POST"])
def api_copilot_suggest():
    """Brain-powered proactive suggestions for the copilot sidebar."""
    data = request.json or {}
    view = data.get("view", "dashboard")
    context = data.get("context", {})

    topo = build_topology_from_golden_configs()
    stats = calculate_network_stats_v2(topo)
    suggestions = []

    # Always-relevant suggestions
    spofs = stats.get("single_points_of_failure", [])
    if spofs:
        suggestions.append({
            "type": "warning", "icon": "alert-triangle",
            "title": f"{len(spofs)} Single Point(s) of Failure",
            "description": f"Devices {', '.join(spofs[:3])} lack redundancy",
            "action": f"Investigate single points of failure: {', '.join(spofs[:3])}"
        })

    redundancy = stats.get("redundancy_score", "N/A")
    if isinstance(redundancy, (int, float)) and redundancy < 0.7:
        suggestions.append({
            "type": "warning", "icon": "shield-off",
            "title": "Low Redundancy Score",
            "description": f"Network redundancy at {redundancy:.0%} — below 70% threshold",
            "action": "Analyze network redundancy and recommend improvements"
        })

    # View-specific suggestions
    if view == "configs":
        suggestions.append({
            "type": "suggestion", "icon": "git-compare",
            "title": "Config Drift Check",
            "description": "Compare running configs against golden baselines",
            "action": "Check all routers for configuration drift from golden configs"
        })
    elif view == "topology":
        suggestions.append({
            "type": "info", "icon": "route",
            "title": "Path Diversity Analysis",
            "description": "Verify multiple paths exist between all PE routers",
            "action": "Analyze path diversity between all PE routers"
        })
    elif view == "dashboard":
        suggestions.append({
            "type": "suggestion", "icon": "activity",
            "title": "Proactive Health Scan",
            "description": "Run protocol checks across all devices",
            "action": "Check ISIS, BGP, LDP, and MPLS status across all routers"
        })

    # Brain-powered classification if available
    if _REASONING_AVAILABLE and context.get("last_query"):
        try:
            result = classify_problem(context["last_query"])
            if hasattr(result, "protocols_involved") and result.protocols_involved:
                protos = ", ".join(result.protocols_involved[:3])
                suggestions.append({
                    "type": "info", "icon": "layers",
                    "title": f"Related: {protos}",
                    "description": f"Your last query involved {protos}. Review these protocols?",
                    "action": f"Run a health check on {protos} across all routers"
                })
        except Exception:
            pass

    return jsonify({
        "suggestions": suggestions[:6],
        "view": view,
        "timestamp": datetime.now().isoformat()
    })


@app.route("/api/ai/confidence-score", methods=["POST"])
def api_confidence_score():
    """Score the confidence of an AI response based on source and validation."""
    data = request.json or {}
    response_type = data.get("type", "general")
    response_text = data.get("response", "")
    sources = data.get("sources", [])
    devices_checked = data.get("devices_checked", [])

    score = 50  # Base
    factors = []

    # Source-based scoring
    if response_type == "knowledge" and sources:
        best_score = max(s.get("score", 0) for s in sources) if sources else 0
        if best_score > 0.8:
            score += 30
            factors.append("High RAG relevance")
        elif best_score > 0.6:
            score += 20
            factors.append("Moderate RAG relevance")
        else:
            score += 10
            factors.append("Partial RAG match")

    elif response_type == "investigation":
        score += 25  # Brain investigation is thorough
        factors.append("Full brain investigation")
        if devices_checked:
            score += min(15, len(devices_checked) * 2)
            factors.append(f"{len(devices_checked)} devices verified")

    elif response_type == "quick_status":
        score += 20
        factors.append("Quick status check")
        if devices_checked:
            score += min(10, len(devices_checked) * 2)

    elif response_type == "config":
        score += 15
        factors.append("Config generation (review required)")

    # Response quality heuristics
    if len(response_text) > 500:
        score += 5
        factors.append("Detailed response")
    if "```" in response_text:
        score += 5
        factors.append("Includes code examples")
    if any(w in response_text.lower() for w in ["warning", "caution", "risk", "impact"]):
        score += 5
        factors.append("Risk-aware")

    score = min(100, max(10, score))
    level = "high" if score >= 80 else ("medium" if score >= 60 else "low")

    return jsonify({
        "score": score, "level": level, "factors": factors,
        "type": response_type
    })


# ══════════════════════════════════════════════════════════════
#  PHASE 3 — Remediation Engine with Approval Gates
# ══════════════════════════════════════════════════════════════

_REMEDIATION_DB = Path(__file__).parent / "remediations.db"


def _init_remediation_db():
    conn = sqlite3.connect(str(_REMEDIATION_DB))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS remediations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT, description TEXT,
            target_router TEXT, commands TEXT,
            risk_level TEXT DEFAULT 'medium',
            ai_analysis TEXT, status TEXT DEFAULT 'pending',
            approved_at TEXT, executed_at TEXT,
            result TEXT, rollback_commands TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


_init_remediation_db()


@app.route("/api/remediate/propose", methods=["POST"])
def api_remediate_propose():
    """AI proposes remediation commands for a detected issue."""
    data = request.json or {}
    issue = data.get("issue", "")
    router = data.get("router", "")
    if not issue:
        return jsonify({"error": "issue description required"}), 400

    # Use Brain + AI to generate remediation
    try:
        analysis = run_async(ollama_analyze_async(
            "You are a JNCIE-SP certified Junos remediation engineer. "
            "Generate SAFE remediation commands. Always include rollback commands.",
            f"Issue: {issue}\nTarget router: {router or 'unspecified'}",
            "Provide:\n"
            "1. TITLE: One-line summary of the fix\n"
            "2. COMMANDS: Exact Junos set/delete commands to fix the issue (one per line)\n"
            "3. ROLLBACK: Commands to undo the fix if needed (one per line)\n"
            "4. RISK: low/medium/high\n"
            "5. IMPACT: Brief description of what this change affects\n"
            "Use the exact headings TITLE:, COMMANDS:, ROLLBACK:, RISK:, IMPACT:"
        ))

        # Parse structured response
        title = ""
        commands = []
        rollback = []
        risk = "medium"
        impact = ""

        section = None
        for line in analysis.split("\n"):
            stripped = line.strip()
            upper = stripped.upper()
            if upper.startswith("TITLE:"):
                title = stripped[6:].strip()
                section = "title"
            elif upper.startswith("COMMANDS:"):
                section = "commands"
            elif upper.startswith("ROLLBACK:"):
                section = "rollback"
            elif upper.startswith("RISK:"):
                r = stripped[5:].strip().lower()
                risk = r if r in ("low", "medium", "high") else "medium"
                section = "risk"
            elif upper.startswith("IMPACT:"):
                impact = stripped[7:].strip()
                section = "impact"
            elif section == "commands" and stripped and not stripped.startswith("#"):
                cmd = stripped.lstrip("- •*").strip().strip("`")
                if cmd.startswith("set ") or cmd.startswith("delete ") or cmd.startswith("deactivate "):
                    commands.append(cmd)
            elif section == "rollback" and stripped and not stripped.startswith("#"):
                cmd = stripped.lstrip("- •*").strip().strip("`")
                if cmd.startswith("set ") or cmd.startswith("delete ") or cmd.startswith("activate "):
                    rollback.append(cmd)
            elif section == "impact" and stripped:
                impact += " " + stripped

        if not title:
            title = f"Remediation for: {issue[:60]}"

        # Save proposal to DB
        conn = sqlite3.connect(str(_REMEDIATION_DB))
        conn.execute(
            "INSERT INTO remediations (title, description, target_router, commands, "
            "risk_level, ai_analysis, rollback_commands) VALUES (?,?,?,?,?,?,?)",
            (title, issue, router, json.dumps(commands), risk, analysis, json.dumps(rollback))
        )
        conn.commit()
        rem_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.close()

        return jsonify({
            "id": rem_id, "title": title, "commands": commands,
            "rollback_commands": rollback, "risk_level": risk,
            "impact": impact.strip(), "router": router,
            "ai_analysis": analysis, "status": "pending",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 503


@app.route("/api/remediate/list")
def api_remediate_list():
    """List all remediation proposals with status."""
    conn = sqlite3.connect(str(_REMEDIATION_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT id, title, target_router, risk_level, status, created_at, "
        "approved_at, executed_at FROM remediations ORDER BY created_at DESC LIMIT 30"
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/remediate/<int:rem_id>")
def api_remediate_detail(rem_id):
    """Get full details of a remediation proposal."""
    conn = sqlite3.connect(str(_REMEDIATION_DB))
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM remediations WHERE id=?", (rem_id,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Not found"}), 404
    d = dict(row)
    for field in ("commands", "rollback_commands"):
        try:
            d[field] = json.loads(d[field])
        except Exception:
            d[field] = []
    return jsonify(d)


@app.route("/api/remediate/<int:rem_id>/approve", methods=["POST"])
def api_remediate_approve(rem_id):
    """Approve a remediation proposal for execution."""
    conn = sqlite3.connect(str(_REMEDIATION_DB))
    row = conn.execute("SELECT status FROM remediations WHERE id=?", (rem_id,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Not found"}), 404
    if row[0] != "pending":
        conn.close()
        return jsonify({"error": f"Cannot approve — status is '{row[0]}'"}), 400
    conn.execute(
        "UPDATE remediations SET status='approved', approved_at=? WHERE id=?",
        (datetime.now().isoformat(), rem_id)
    )
    conn.commit()
    conn.close()
    return jsonify({"id": rem_id, "status": "approved", "message": "Remediation approved. Ready to execute."})


@app.route("/api/remediate/<int:rem_id>/reject", methods=["POST"])
def api_remediate_reject(rem_id):
    """Reject a remediation proposal."""
    conn = sqlite3.connect(str(_REMEDIATION_DB))
    conn.execute("UPDATE remediations SET status='rejected' WHERE id=?", (rem_id,))
    conn.commit()
    conn.close()
    return jsonify({"id": rem_id, "status": "rejected"})


@app.route("/api/remediate/<int:rem_id>/execute", methods=["POST"])
def api_remediate_execute(rem_id):
    """Execute an APPROVED remediation via MCP. Only approved proposals can run."""
    conn = sqlite3.connect(str(_REMEDIATION_DB))
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM remediations WHERE id=?", (rem_id,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Not found"}), 404
    d = dict(row)
    if d["status"] != "approved":
        conn.close()
        return jsonify({"error": f"Cannot execute — status is '{d['status']}'. Must be approved first."}), 400

    router = d["target_router"]
    try:
        commands = json.loads(d["commands"])
    except Exception:
        commands = []

    if not router or not commands:
        conn.close()
        return jsonify({"error": "Missing router or commands"}), 400

    socketio.emit("brain_progress", {
        "event": "remediation_start", "id": rem_id, "router": router
    })

    config_text = "\n".join(commands)
    try:
        result = run_async(mcp_load_config(
            router, config_text, f"NOC Remediation #{rem_id}: {d['title']}"
        ))
        conn.execute(
            "UPDATE remediations SET status='executed', executed_at=?, result=? WHERE id=?",
            (datetime.now().isoformat(), str(result)[:5000], rem_id)
        )
        conn.commit()
        conn.close()
        socketio.emit("brain_progress", {
            "event": "remediation_complete", "id": rem_id, "router": router
        })
        return jsonify({
            "id": rem_id, "status": "executed", "router": router,
            "result": result, "commands_applied": len(commands),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        conn.execute(
            "UPDATE remediations SET status='failed', result=? WHERE id=?",
            (str(e)[:5000], rem_id)
        )
        conn.commit()
        conn.close()
        socketio.emit("brain_progress", {
            "event": "remediation_error", "id": rem_id, "error": str(e)
        })
        return jsonify({"error": str(e), "id": rem_id, "status": "failed"}), 503


@app.route("/api/deploy/safe", methods=["POST"])
def api_deploy_safe():
    """AI pre-flight safety check before config deployment."""
    data = request.json or {}
    router = data.get("router", "")
    config_text = data.get("config", "")
    if not router or not config_text:
        return jsonify({"error": "router and config required"}), 400

    # AI pre-flight analysis
    try:
        safety = run_async(ollama_analyze_async(
            "You are a JNCIE-SP Junos change management engineer.",
            f"Router: {router}\nProposed config:\n{config_text}",
            "Perform a pre-flight safety analysis:\n"
            "1. RISK_LEVEL: low/medium/high/critical\n"
            "2. SAFE: yes/no — is this safe to deploy?\n"
            "3. WARNINGS: List any potential issues (protocol flaps, traffic impact, etc.)\n"
            "4. AFFECTED_PROTOCOLS: Which protocols will be affected?\n"
            "5. RECOMMENDATION: Deploy, modify, or abort?"
        ))

        is_safe = "SAFE: yes" in safety.upper() or "SAFE:YES" in safety.upper().replace(" ", "")
        risk = "low"
        for level in ["critical", "high", "medium"]:
            if level in safety.lower():
                risk = level
                break

        return jsonify({
            "router": router, "safe": is_safe, "risk_level": risk,
            "analysis": safety, "config_preview": config_text[:500],
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 503


# ══════════════════════════════════════════════════════════════
#  PHASE 4 — Multi-Model Ensemble + Predictive Analysis
# ══════════════════════════════════════════════════════════════

@app.route("/api/ai/ensemble", methods=["POST"])
def api_ai_ensemble():
    """Query multiple Ollama models and produce a consensus answer."""
    data = request.json or {}
    question = data.get("question", "")
    context_data = data.get("context", "")
    if not question:
        return jsonify({"error": "question required"}), 400

    # Discover available models (properly close the httpx client)
    available_models = []
    try:
        async def _list_models():
            async with httpx.AsyncClient(timeout=5) as client:
                return await client.get(f"{OLLAMA_URL}/api/tags")
        resp = run_async(_list_models())
        if resp.status_code == 200:
            models_data = resp.json().get("models", [])
            available_models = [m["name"] for m in models_data]
    except Exception:
        available_models = [OLLAMA_MODEL]

    if not available_models:
        available_models = [OLLAMA_MODEL]

    # Use up to 3 models for ensemble
    ensemble_models = available_models[:3]
    if OLLAMA_MODEL not in ensemble_models:
        ensemble_models[0] = OLLAMA_MODEL

    results = []
    system_prompt = (
        "You are a JNCIE-SP Junos network expert. "
        "Give a concise, accurate, technical answer. "
        "End with CONFIDENCE: <0-100>% indicating your confidence."
    )

    for model in ensemble_models:
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{context_data}\n\n{question}" if context_data else question}
            ]
            resp = run_async(ollama_chat_async(messages, model=model))
            answer = resp.get("message", {}).get("content", "")

            # Extract self-reported confidence
            confidence = 70
            conf_match = re.search(r'CONFIDENCE:\s*(\d+)', answer, re.IGNORECASE)
            if conf_match:
                confidence = min(100, max(0, int(conf_match.group(1))))

            results.append({
                "model": model, "answer": answer,
                "confidence": confidence, "success": True
            })
        except Exception as e:
            results.append({
                "model": model, "answer": str(e),
                "confidence": 0, "success": False
            })

    # Consensus: pick highest confidence, note agreement
    successful = [r for r in results if r["success"]]
    if not successful:
        return jsonify({"error": "All models failed", "results": results}), 503

    best = max(successful, key=lambda r: r["confidence"])
    avg_confidence = sum(r["confidence"] for r in successful) / len(successful)

    return jsonify({
        "consensus": best["answer"],
        "consensus_model": best["model"],
        "consensus_confidence": best["confidence"],
        "average_confidence": round(avg_confidence, 1),
        "models_queried": len(ensemble_models),
        "models_succeeded": len(successful),
        "all_results": results,
        "timestamp": datetime.now().isoformat()
    })


@app.route("/api/brain/predict", methods=["POST"])
def api_brain_predict():
    """Predictive failure analysis using investigation history + current state."""
    data = request.json or {}
    scope = data.get("scope", "all")  # "all" or specific router

    # Gather historical investigation data
    conn = sqlite3.connect(str(_INVESTIGATION_DB))
    conn.row_factory = sqlite3.Row
    history = conn.execute(
        "SELECT query, classification, devices, response, created_at "
        "FROM investigations ORDER BY created_at DESC LIMIT 20"
    ).fetchall()
    conn.close()
    history_text = "\n".join(
        f"[{r['created_at']}] Query: {r['query']} | Devices: {r['devices']}"
        for r in history
    ) if history else "No investigation history available."

    # Current topology state
    topo = build_topology_from_golden_configs()
    stats = calculate_network_stats_v2(topo)
    spofs = stats.get("single_points_of_failure", [])
    nodes_summary = ", ".join(
        f"{n['id']}({n['role']}, BGP:{len(n.get('bgp_neighbors',[]))}, "
        f"ISIS:{len(n.get('isis_interfaces',[]))}, LDP:{n.get('ldp','?')}, MPLS:{n.get('mpls','?')})"
        for n in topo.get("nodes", [])
    )

    try:
        prediction = run_async(ollama_analyze_async(
            "You are a predictive network analytics AI with JNCIE-SP expertise.",
            f"NETWORK STATE:\n{nodes_summary}\n\n"
            f"SPOFs: {', '.join(spofs) if spofs else 'None'}\n"
            f"Redundancy Score: {stats.get('redundancy_score', 'N/A')}\n"
            f"Total Devices: {stats.get('total_nodes', 0)}\n\n"
            f"INVESTIGATION HISTORY:\n{history_text}",
            "Based on the current network state and investigation history, predict:\n"
            "1. TOP 3 RISKS: Most likely failure scenarios with probability (high/medium/low)\n"
            "2. EARLY WARNINGS: Patterns that suggest emerging issues\n"
            "3. RECOMMENDED ACTIONS: Proactive steps to prevent failures\n"
            "4. HEALTH FORECAST: 24-hour network health prediction\n"
            "Be specific about which devices and protocols are at risk."
        ))

        return jsonify({
            "prediction": prediction,
            "scope": scope,
            "spofs": spofs,
            "history_entries": len(history) if history else 0,
            "network_size": stats.get("total_nodes", 0),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 503


# ══════════════════════════════════════════════════════════════
#  INVESTIGATION HISTORY (local SQLite)
# ══════════════════════════════════════════════════════════════

_INVESTIGATION_DB = Path(__file__).parent / "investigations.db"


def _init_investigation_db():
    conn = sqlite3.connect(str(_INVESTIGATION_DB))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS investigations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT, classification TEXT, devices TEXT,
            response TEXT, mode TEXT, duration_ms INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


_init_investigation_db()


@app.route("/api/brain/history")
def api_brain_history():
    """Get recent investigation history."""
    conn = sqlite3.connect(str(_INVESTIGATION_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT id, query, classification, devices, mode, duration_ms, created_at "
        "FROM investigations ORDER BY created_at DESC LIMIT 20"
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/brain/history/<int:inv_id>")
def api_brain_history_detail(inv_id):
    """Get full investigation details."""
    conn = sqlite3.connect(str(_INVESTIGATION_DB))
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM investigations WHERE id=?", (inv_id,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Not found"}), 404
    return jsonify(dict(row))


# ── WebSocket Events ──────────────────────────────────────────
@socketio.on("connect")
def handle_connect():
    emit("connected", {"status": "ok", "timestamp": datetime.now().isoformat()})

@socketio.on("request_topology")
def handle_topology_request():
    topo = build_topology_from_golden_configs()
    emit("topology_update", topo)

@socketio.on("request_path")
def handle_path_request(data):
    result = find_shortest_path(data.get("source", ""), data.get("target", ""))
    emit("path_result", result)

@socketio.on("chat_message")
def handle_chat(data):
    """Handle AI chat messages — connected to Ollama."""
    message = data.get("message", "")
    history = data.get("history", [])
    
    # Build context-aware system prompt
    topo = build_topology_from_golden_configs()
    stats = calculate_network_stats_v2(topo)
    system_prompt = f"""You are the Junos AI NOC assistant. Network: {stats.get('total_nodes',0)} routers. Protocols: IS-IS L2, iBGP, LDP, MPLS, L3VPN. Respond concisely in Markdown."""
    
    messages = [{"role": "system", "content": system_prompt}]
    for h in history[-10:]:
        messages.append({"role": h.get("role", "user"), "content": h.get("content", "")})
    messages.append({"role": "user", "content": message})
    
    try:
        result = run_async(ollama_chat_async(messages))
        response = result.get("message", {}).get("content", "No response")
        emit("chat_response", {
            "response": response,
            "model": OLLAMA_MODEL,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        # Fallback to local responses when Ollama is unavailable
        emit("chat_response", {
            "response": generate_local_response(message, topo, stats),
            "model": "local-fallback",
            "timestamp": datetime.now().isoformat()
        })

@socketio.on("mcp_command")
def handle_mcp_command(data):
    """Execute MCP command via WebSocket for real-time results."""
    router = data.get("router", "")
    command = data.get("command", "")
    if not router or not command:
        emit("mcp_result", {"error": "router and command required"})
        return
    try:
        result = run_async(mcp_execute_command(router, command))
        emit("mcp_result", {"router": router, "command": command, "output": result,
                            "timestamp": datetime.now().isoformat()})
    except Exception as e:
        emit("mcp_result", {"error": str(e)})

@socketio.on("poll_devices")
def handle_poll_devices():
    """Poll all devices for live status update."""
    devices = load_devices()
    router_names = list(devices.keys())
    try:
        result = run_async(mcp_execute_batch("show system uptime | display json", router_names))
        emit("device_status", {"output": result, "routers": router_names,
                               "timestamp": datetime.now().isoformat()})
    except Exception as e:
        emit("device_status", {"error": str(e)})


def generate_local_response(msg: str, topo: dict, stats: dict) -> str:
    """Local fallback response when Ollama is unavailable."""
    lower = msg.lower()
    if "topology" in lower or "summary" in lower:
        return f"**Network Topology**\n\n• Devices: {len(topo.get('nodes', []))}\n• Links: {len(topo.get('links', []))}\n• PE: {stats.get('pe_count', 0)} | P: {stats.get('p_count', 0)} | RR: {stats.get('rr_count', 0)}\n• Diameter: {stats.get('graph_diameter', 0)} | Redundancy: {stats.get('redundancy_score', 0)}%"
    if "spof" in lower or "failure" in lower:
        spofs = stats.get("single_points_of_failure", [])
        return f"{'No SPOFs detected — network is fully redundant.' if not spofs else 'SPOFs detected: ' + ', '.join(spofs)}"
    if "bgp" in lower:
        nodes = topo.get("nodes", [])
        bgp = [n for n in nodes if n.get("bgp_neighbors")]
        return "**BGP Sessions**\n\n" + "\n".join(f"• {n['id']}: {len(n['bgp_neighbors'])} peers → {', '.join(n['bgp_neighbors'])}" for n in bgp)
    return f"AI engine offline — using local fallback.\n\nTry: topology summary, SPOF analysis, BGP status"


# ══════════════════════════════════════════════════════════════
#  DEVICE POOLS ENGINE (Feature #10)
# ══════════════════════════════════════════════════════════════

def init_pools_db():
    """Initialize device pools database."""
    POOLS_DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(POOLS_DB))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS device_pools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT DEFAULT '',
            devices TEXT NOT NULL DEFAULT '[]',
            tags TEXT DEFAULT '[]',
            color TEXT DEFAULT '#01A982',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_pools_db()

@app.route("/api/pools")
def api_list_pools():
    conn = sqlite3.connect(str(POOLS_DB))
    conn.row_factory = sqlite3.Row
    pools = conn.execute("SELECT * FROM device_pools ORDER BY name").fetchall()
    conn.close()
    return jsonify([dict(p) for p in pools])

@app.route("/api/pools", methods=["POST"])
def api_create_pool():
    data = request.json or {}
    name = data.get("name", "").strip()
    if not name:
        return jsonify({"error": "name required"}), 400
    devices = json.dumps(data.get("devices", []))
    tags = json.dumps(data.get("tags", []))
    description = data.get("description", "")
    color = data.get("color", "#01A982")
    try:
        conn = sqlite3.connect(str(POOLS_DB))
        conn.execute("INSERT INTO device_pools (name, description, devices, tags, color) VALUES (?,?,?,?,?)",
                     (name, description, devices, tags, color))
        conn.commit()
        pid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.close()
        return jsonify({"id": pid, "name": name})
    except sqlite3.IntegrityError:
        return jsonify({"error": f"Pool '{name}' already exists"}), 409

@app.route("/api/pools/<int:pool_id>", methods=["PUT"])
def api_update_pool(pool_id):
    data = request.json or {}
    conn = sqlite3.connect(str(POOLS_DB))
    fields = []
    vals = []
    for key in ("name", "description", "color"):
        if key in data:
            fields.append(f"{key}=?")
            vals.append(data[key])
    if "devices" in data:
        fields.append("devices=?")
        vals.append(json.dumps(data["devices"]))
    if "tags" in data:
        fields.append("tags=?")
        vals.append(json.dumps(data["tags"]))
    fields.append("updated_at=?")
    vals.append(datetime.now().isoformat())
    vals.append(pool_id)
    conn.execute(f"UPDATE device_pools SET {','.join(fields)} WHERE id=?", vals)
    conn.commit()
    conn.close()
    return jsonify({"updated": pool_id})

@app.route("/api/pools/<int:pool_id>", methods=["DELETE"])
def api_delete_pool(pool_id):
    conn = sqlite3.connect(str(POOLS_DB))
    conn.execute("DELETE FROM device_pools WHERE id=?", (pool_id,))
    conn.commit()
    conn.close()
    return jsonify({"deleted": pool_id})

@app.route("/api/pools/ai-recommend", methods=["POST"])
def api_pools_ai_recommend():
    """AI recommends optimal device groupings based on topology analysis."""
    topo = build_topology_from_golden_configs()
    stats = calculate_network_stats_v2(topo)
    nodes_summary = json.dumps([{"id": n["id"], "role": n["role"], "loopback": n.get("loopback", ""),
                                  "bgp_peers": len(n.get("bgp_neighbors", [])),
                                  "isis": len(n.get("isis_interfaces", [])),
                                  "ldp": n.get("ldp"), "vpn": n.get("vpn")} for n in topo["nodes"]], indent=2)
    prompt = f"""Analyze this network topology and recommend optimal device pool groupings.

DEVICES:
{nodes_summary}

NETWORK STATS:
- SPOFs: {stats.get('single_points_of_failure', [])}
- Redundancy: {stats.get('redundancy_score', 0)}%

Recommend 3-5 device pools with:
1. Pool name & description
2. List of devices in each pool
3. Suggested color (hex)
4. Tags for each pool
5. Reasoning for each grouping

Return as JSON array: [{{"name": "...", "description": "...", "devices": [...], "color": "#...", "tags": [...], "reasoning": "..."}}]
Respond ONLY with the JSON array, no markdown fences."""
    try:
        result = run_async(ollama_analyze_async(
            "You are a Junos network architect. Return ONLY valid JSON.", nodes_summary, prompt))
        # Try to parse AI response as JSON
        try:
            # Strip markdown fences if present
            clean = re.sub(r'^```(?:json)?\s*', '', result.strip())
            clean = re.sub(r'\s*```$', '', clean)
            recommendations = json.loads(clean)
        except json.JSONDecodeError:
            recommendations = result
        return jsonify({"recommendations": recommendations, "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 503


# ══════════════════════════════════════════════════════════════
#  PING / REACHABILITY SERVICE (Feature #7)
# ══════════════════════════════════════════════════════════════

@app.route("/api/ping/<router>")
def api_ping_router(router):
    """Ping a single router via MCP 'show system uptime'."""
    start = time.time()
    try:
        result = run_async(mcp_execute_command(router, "show system uptime"))
        latency = int((time.time() - start) * 1000)
        reachable = "Error" not in result and "error" not in result.lower()
        return jsonify({"router": router, "reachable": reachable, "latency_ms": latency,
                        "output": result[:1000], "timestamp": datetime.now().isoformat()})
    except Exception as e:
        latency = int((time.time() - start) * 1000)
        return jsonify({"router": router, "reachable": False, "latency_ms": latency,
                        "error": str(e), "timestamp": datetime.now().isoformat()})

@app.route("/api/ping/sweep", methods=["POST"])
def api_ping_sweep():
    """Ping all (or selected) routers and return reachability status."""
    data = request.json or {}
    routers = data.get("routers", [])
    if not routers:
        devices = load_devices()
        routers = list(devices.keys())
    start = time.time()
    try:
        result = run_async(mcp_execute_batch("show system uptime", routers))
        total_ms = int((time.time() - start) * 1000)
        # Parse batch results
        results = []
        for r in routers:
            reachable = r in result and "error" not in result.lower()
            results.append({"router": r, "reachable": reachable})
        return jsonify({"results": results, "total_ms": total_ms, "raw": result[:3000],
                        "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/ping/ai-analyze", methods=["POST"])
def api_ping_ai_analyze():
    """AI analyzes ping sweep results for patterns and recommendations."""
    data = request.json or {}
    ping_results = data.get("results", "")
    if not ping_results:
        return jsonify({"error": "results required"}), 400
    try:
        analysis = run_async(ollama_analyze_async(
            "You are a Junos NOC engineer specializing in reachability monitoring.",
            json.dumps(ping_results) if isinstance(ping_results, (list, dict)) else str(ping_results),
            "Analyze these ping/reachability results. Identify unreachable devices, potential causes, "
            "affected services (VPN, MPLS, BGP), and recommend remediation steps."
        ))
        return jsonify({"analysis": analysis, "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 503


# ══════════════════════════════════════════════════════════════
#  DATA VALIDATION SERVICE (Feature #9)
# ══════════════════════════════════════════════════════════════

@app.route("/api/validate", methods=["POST"])
def api_validate_data():
    """Validate command output against regex patterns."""
    data = request.json or {}
    router = data.get("router", "")
    command = data.get("command", "")
    pattern = data.get("pattern", "")
    match_type = data.get("match_type", "contains")  # contains, regex, exact, not_contains
    if not router or not command or not pattern:
        return jsonify({"error": "router, command, and pattern required"}), 400
    try:
        output = run_async(mcp_execute_command(router, command))
        if match_type == "regex":
            passed = bool(re.search(pattern, output, re.IGNORECASE | re.MULTILINE))
        elif match_type == "exact":
            passed = pattern.strip() == output.strip()
        elif match_type == "not_contains":
            passed = pattern.lower() not in output.lower()
        else:
            passed = pattern.lower() in output.lower()
        return jsonify({
            "router": router, "command": command, "pattern": pattern,
            "match_type": match_type, "passed": passed,
            "output": output[:3000], "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/validate/batch", methods=["POST"])
def api_validate_batch():
    """Run validation across multiple routers."""
    data = request.json or {}
    routers = data.get("routers", [])
    command = data.get("command", "")
    pattern = data.get("pattern", "")
    match_type = data.get("match_type", "contains")
    if not routers or not command or not pattern:
        return jsonify({"error": "routers, command, and pattern required"}), 400
    results = []
    for router in routers:
        try:
            output = run_async(mcp_execute_command(router, command))
            if match_type == "regex":
                passed = bool(re.search(pattern, output, re.IGNORECASE | re.MULTILINE))
            elif match_type == "not_contains":
                passed = pattern.lower() not in output.lower()
            else:
                passed = pattern.lower() in output.lower()
            results.append({"router": router, "passed": passed, "output": output[:500]})
        except Exception as e:
            results.append({"router": router, "passed": False, "error": str(e)})
    passed_count = sum(1 for r in results if r.get("passed"))
    return jsonify({"results": results, "total": len(results), "passed": passed_count,
                    "failed": len(results) - passed_count, "timestamp": datetime.now().isoformat()})

@app.route("/api/validate/ai-compliance", methods=["POST"])
def api_validate_ai_compliance():
    """AI-powered compliance check against best practices."""
    data = request.json or {}
    router = data.get("router", "")
    if not router:
        return jsonify({"error": "router required"}), 400
    # Get the golden config or pull live from MCP
    config_path = GOLDEN_CONFIG_DIR / f"{router}.conf"
    if config_path.exists():
        config = config_path.read_text()
    else:
        config = run_async(mcp_get_config(router))
        if not config or config.startswith("Error:"):
            return jsonify({"error": f"No config available for {router}"}), 404
    try:
        analysis = run_async(ollama_analyze_async(
            "You are a JNCIE-SP certified Junos security and compliance auditor.",
            config,
            "Perform a comprehensive compliance audit on this Junos configuration. Check for:\n"
            "1. NTP configuration\n2. SNMP community security\n3. Login class restrictions\n"
            "4. SSH hardening (no telnet)\n5. IS-IS authentication\n6. BGP MD5 authentication\n"
            "7. MPLS security\n8. Firewall filters on lo0\n9. Syslog configuration\n"
            "10. Unused interfaces should be disabled\n\n"
            "For each check, indicate PASS/FAIL/WARNING with explanation and remediation config."
        ))
        return jsonify({"router": router, "compliance": analysis, "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 503


# ══════════════════════════════════════════════════════════════
#  NOTIFICATION SERVICE (Feature #8)
# ══════════════════════════════════════════════════════════════

def init_notifications_db():
    NOTIFICATIONS_DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(NOTIFICATIONS_DB))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notification_channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            channel_type TEXT NOT NULL,
            webhook_url TEXT DEFAULT '',
            config TEXT DEFAULT '{}',
            enabled INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notification_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id INTEGER,
            title TEXT, message TEXT, severity TEXT DEFAULT 'info',
            sent_at TEXT DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'sent',
            response TEXT DEFAULT ''
        )
    """)
    conn.commit()
    conn.close()

init_notifications_db()

@app.route("/api/notifications/channels")
def api_list_notification_channels():
    conn = sqlite3.connect(str(NOTIFICATIONS_DB))
    conn.row_factory = sqlite3.Row
    channels = conn.execute("SELECT * FROM notification_channels ORDER BY name").fetchall()
    conn.close()
    return jsonify([dict(c) for c in channels])

@app.route("/api/notifications/channels", methods=["POST"])
def api_create_notification_channel():
    data = request.json or {}
    name = data.get("name", "")
    channel_type = data.get("channel_type", "webhook")  # webhook, slack, mattermost, email
    webhook_url = data.get("webhook_url", "")
    config = json.dumps(data.get("config", {}))
    if not name:
        return jsonify({"error": "name required"}), 400
    conn = sqlite3.connect(str(NOTIFICATIONS_DB))
    conn.execute("INSERT INTO notification_channels (name, channel_type, webhook_url, config) VALUES (?,?,?,?)",
                 (name, channel_type, webhook_url, config))
    conn.commit()
    cid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return jsonify({"id": cid, "name": name})

@app.route("/api/notifications/channels/<int:cid>", methods=["DELETE"])
def api_delete_notification_channel(cid):
    conn = sqlite3.connect(str(NOTIFICATIONS_DB))
    conn.execute("DELETE FROM notification_channels WHERE id=?", (cid,))
    conn.commit()
    conn.close()
    return jsonify({"deleted": cid})

@app.route("/api/notifications/send", methods=["POST"])
def api_send_notification():
    """Send a notification via configured channel."""
    data = request.json or {}
    channel_id = data.get("channel_id")
    title = data.get("title", "NOC Alert")
    message = data.get("message", "")
    severity = data.get("severity", "info")
    if not channel_id or not message:
        return jsonify({"error": "channel_id and message required"}), 400
    conn = sqlite3.connect(str(NOTIFICATIONS_DB))
    conn.row_factory = sqlite3.Row
    channel = conn.execute("SELECT * FROM notification_channels WHERE id=?", (channel_id,)).fetchone()
    if not channel:
        conn.close()
        return jsonify({"error": "Channel not found"}), 404
    channel = dict(channel)

    # ── Security: Validate webhook URL is local/private ──
    import urllib.parse as _urlparse
    _webhook_url = channel.get("webhook_url", "")
    _allow_external = os.environ.get("NOC_ALLOW_EXTERNAL_WEBHOOKS", "").lower() == "true"
    if _webhook_url and not _allow_external:
        _parsed = _urlparse.urlparse(_webhook_url)
        _host = _parsed.hostname or ""
        _LOCAL_HOSTS = {"127.0.0.1", "localhost", "0.0.0.0", "::1"}
        _is_local = _host in _LOCAL_HOSTS or _host.startswith("10.") or _host.startswith("192.168.") or _host.startswith("172.")
        if not _is_local:
            conn.close()
            return jsonify({"error": "External webhooks disabled. Set NOC_ALLOW_EXTERNAL_WEBHOOKS=true to enable."}), 403

    status = "sent"
    response_text = ""
    try:
        if channel["channel_type"] in ("slack", "mattermost"):
            payload = {"text": f"*[{severity.upper()}] {title}*\n{message}"}
            resp = httpx.post(channel["webhook_url"], json=payload, timeout=10.0)
            response_text = resp.text
            status = "sent" if resp.status_code < 300 else "failed"
        elif channel["channel_type"] == "webhook":
            payload = {"title": title, "message": message, "severity": severity,
                       "timestamp": datetime.now().isoformat(), "source": "Junos AI NOC"}
            resp = httpx.post(channel["webhook_url"], json=payload, timeout=10.0)
            response_text = resp.text
            status = "sent" if resp.status_code < 300 else "failed"
        else:
            response_text = f"Unsupported channel type: {channel['channel_type']}"
            status = "failed"
    except Exception as e:
        response_text = str(e)
        status = "failed"
    conn.execute("INSERT INTO notification_history (channel_id, title, message, severity, status, response) VALUES (?,?,?,?,?,?)",
                 (channel_id, title, message, severity, status, response_text))
    conn.commit()
    conn.close()
    return jsonify({"status": status, "response": response_text})

@app.route("/api/notifications/history")
def api_notification_history():
    conn = sqlite3.connect(str(NOTIFICATIONS_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM notification_history ORDER BY sent_at DESC LIMIT 50").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/notifications/ai-summary", methods=["POST"])
def api_notification_ai_summary():
    """AI generates a smart alert summary from recent events."""
    data = request.json or {}
    events = data.get("events", "")
    if not events:
        return jsonify({"error": "events required"}), 400
    try:
        summary = run_async(ollama_analyze_async(
            "You are a Junos NOC alert summarizer. Create concise, actionable alert summaries.",
            json.dumps(events) if isinstance(events, (list, dict)) else str(events),
            "Summarize these network events into a clear alert notification. Include:\n"
            "1. Severity classification (critical/warning/info)\n"
            "2. Affected devices and services\n"
            "3. Root cause hypothesis\n"
            "4. Recommended immediate actions\n"
            "Keep it concise — suitable for a Slack/Teams notification."
        ))
        return jsonify({"summary": summary, "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 503


# ══════════════════════════════════════════════════════════════
#  CONFIG GIT EXPORT (Feature #11)
# ══════════════════════════════════════════════════════════════

GIT_EXPORT_DIR.mkdir(parents=True, exist_ok=True)

@app.route("/api/git-export/init", methods=["POST"])
def api_git_export_init():
    """Initialize git repo for config export."""
    try:
        if not (GIT_EXPORT_DIR / ".git").exists():
            subprocess.run(["git", "init"], cwd=str(GIT_EXPORT_DIR), capture_output=True, check=True)
        return jsonify({"status": "initialized", "path": str(GIT_EXPORT_DIR)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/git-export/export", methods=["POST"])
def api_git_export_configs():
    """Export all golden configs to git repository with AI-generated commit message."""
    data = request.json or {}
    custom_message = data.get("message", "")
    try:
        # Initialize git if needed
        if not (GIT_EXPORT_DIR / ".git").exists():
            subprocess.run(["git", "init"], cwd=str(GIT_EXPORT_DIR), capture_output=True, check=True)
        # Copy configs
        changes = []
        for fname in sorted(GOLDEN_CONFIG_DIR.iterdir()):
            if fname.name.endswith(".conf"):
                dest = GIT_EXPORT_DIR / fname.name
                old_content = dest.read_text() if dest.exists() else ""
                new_content = fname.read_text()
                if old_content != new_content:
                    changes.append(fname.name)
                shutil.copy2(fname, dest)
        # Git add
        subprocess.run(["git", "add", "-A"], cwd=str(GIT_EXPORT_DIR), capture_output=True)
        # Check if there are changes to commit
        status = subprocess.run(["git", "status", "--porcelain"], cwd=str(GIT_EXPORT_DIR),
                                capture_output=True, text=True)
        if not status.stdout.strip():
            return jsonify({"status": "no_changes", "message": "No config changes to commit"})
        # Generate AI commit message if not provided
        if not custom_message and changes:
            try:
                commit_msg = run_async(ollama_analyze_async(
                    "You are a git commit message generator for network configs. Be concise.",
                    f"Changed files: {', '.join(changes)}",
                    "Generate a clear, conventional git commit message (max 72 chars subject line) for these Junos config changes. "
                    "Format: type(scope): description. No markdown, just plain text."
                ))
                custom_message = commit_msg.strip().split('\n')[0][:72]
            except Exception:
                custom_message = f"config: update {len(changes)} golden configs"
        elif not custom_message:
            custom_message = f"config: export golden configs ({datetime.now().strftime('%Y-%m-%d %H:%M')})"
        # ── Security: Sanitize commit message ──
        custom_message = re.sub(r'[^\w\s\-_.:()/,#@]', '', custom_message)[:200]
        # Git commit
        subprocess.run(["git", "commit", "-m", custom_message], cwd=str(GIT_EXPORT_DIR),
                        capture_output=True, check=True)
        # Get log
        log = subprocess.run(["git", "log", "--oneline", "-5"], cwd=str(GIT_EXPORT_DIR),
                             capture_output=True, text=True)
        return jsonify({"status": "committed", "message": custom_message,
                        "changes": changes, "log": log.stdout.strip(),
                        "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/git-export/log")
def api_git_export_log():
    """Get git commit history."""
    try:
        result = subprocess.run(["git", "log", "--oneline", "-20"],
                                cwd=str(GIT_EXPORT_DIR), capture_output=True, text=True)
        lines = [l.strip() for l in result.stdout.strip().split('\n') if l.strip()]
        return jsonify({"log": lines})
    except Exception as e:
        return jsonify({"log": [], "error": str(e)})

@app.route("/api/git-export/diff/<commit>")
def api_git_export_diff(commit):
    """Show diff for a specific commit."""
    try:
        result = subprocess.run(["git", "show", "--stat", commit],
                                cwd=str(GIT_EXPORT_DIR), capture_output=True, text=True)
        return jsonify({"commit": commit, "diff": result.stdout})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ══════════════════════════════════════════════════════════════
#  CONFIG ROLLBACK SERVICE (Feature #12)
# ══════════════════════════════════════════════════════════════

@app.route("/api/rollback/diff/<router>")
def api_rollback_diff(router):
    """Get config diff against rollback version via MCP."""
    version = int(request.args.get("version", 1))
    try:
        result = run_async(mcp_execute_command(router, f"show system rollback compare {version}"))
        return jsonify({"router": router, "version": version, "diff": result,
                        "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/rollback/execute", methods=["POST"])
def api_rollback_execute():
    """Execute a rollback on a router with AI risk assessment."""
    data = request.json or {}
    router = data.get("router", "")
    version = data.get("version", 1)
    confirm = data.get("confirm", False)
    if not router:
        return jsonify({"error": "router required"}), 400
    # First, get the diff
    try:
        diff = run_async(mcp_execute_command(router, f"show system rollback compare {version}"))
    except Exception as e:
        return jsonify({"error": f"Failed to get rollback diff: {e}"}), 500
    if not confirm:
        # AI risk assessment
        try:
            risk = run_async(ollama_analyze_async(
                "You are a JNCIE-SP certified Junos engineer performing rollback risk assessment.",
                diff,
                "Analyze this Junos rollback diff and assess the risk:\n"
                "1. Risk level: LOW / MEDIUM / HIGH / CRITICAL\n"
                "2. What will change (protocols affected, interfaces, routing)\n"
                "3. Potential service impact\n"
                "4. Recommendation: PROCEED / CAUTION / ABORT\n"
                "Be specific about BGP, IS-IS, MPLS, LDP, VPN impacts."
            ))
        except Exception:
            risk = "AI risk assessment unavailable"
        return jsonify({"router": router, "version": version, "diff": diff,
                        "risk_assessment": risk, "requires_confirmation": True})
    # Execute rollback
    try:
        result = run_async(mcp_load_config(router,
            f"rollback {version}", f"NOC Rollback to version {version}"))
        return jsonify({"router": router, "version": version, "result": result,
                        "status": "rolled_back", "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ══════════════════════════════════════════════════════════════
#  RESULT COMPARISON SERVICE (Feature #13)
# ══════════════════════════════════════════════════════════════

RESULTS_DIR.mkdir(parents=True, exist_ok=True)

@app.route("/api/results/capture", methods=["POST"])
def api_capture_result():
    """Capture command output as a named result for later comparison."""
    data = request.json or {}
    name = data.get("name", f"result_{int(time.time())}")
    router = data.get("router", "")
    command = data.get("command", "")
    if not router or not command:
        return jsonify({"error": "router and command required"}), 400
    try:
        output = run_async(mcp_execute_command(router, command))
        result = {
            "name": name, "router": router, "command": command,
            "output": output, "captured_at": datetime.now().isoformat()
        }
        safe_name = re.sub(r'[^\w\-]', '_', name)
        path = RESULTS_DIR / f"{safe_name}.json"
        path.write_text(json.dumps(result, indent=2))
        return jsonify({"saved": name, "path": str(path), "lines": len(output.splitlines())})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/results")
def api_list_results():
    """List all captured results."""
    results = []
    for f in sorted(RESULTS_DIR.glob("*.json"), reverse=True):
        try:
            data = json.loads(f.read_text())
            results.append({
                "name": data.get("name", f.stem), "router": data.get("router", ""),
                "command": data.get("command", ""), "captured_at": data.get("captured_at", ""),
                "lines": len(data.get("output", "").splitlines())
            })
        except Exception:
            continue
    return jsonify(results)

@app.route("/api/results/<name>")
def api_get_result(name):
    safe = re.sub(r'[^\w\-]', '_', name)
    path = RESULTS_DIR / f"{safe}.json"
    if not path.exists():
        return jsonify({"error": "Not found"}), 404
    return jsonify(json.loads(path.read_text()))

@app.route("/api/results/compare", methods=["POST"])
def api_compare_results():
    """Compare two captured results side by side with AI diff analysis."""
    data = request.json or {}
    result_a = data.get("result_a", "")
    result_b = data.get("result_b", "")
    if not result_a or not result_b:
        return jsonify({"error": "result_a and result_b names required"}), 400
    # Load both results (iterate by name for safety)
    # Try to find by name
    data_a = data_b = None
    for f in RESULTS_DIR.glob("*.json"):
        try:
            d = json.loads(f.read_text())
            if d.get("name") == result_a:
                data_a = d
            if d.get("name") == result_b:
                data_b = d
        except Exception:
            continue
    if not data_a or not data_b:
        return jsonify({"error": "One or both results not found"}), 404
    # Generate diff
    lines_a = data_a.get("output", "").splitlines()
    lines_b = data_b.get("output", "").splitlines()
    diff = list(difflib.unified_diff(lines_a, lines_b,
                fromfile=f"{result_a} ({data_a.get('captured_at', '')})",
                tofile=f"{result_b} ({data_b.get('captured_at', '')})",
                lineterm=""))
    # AI analysis of diff
    ai_analysis = ""
    if diff:
        try:
            ai_analysis = run_async(ollama_analyze_async(
                "You are a Junos network engineer analyzing command output differences.",
                "\n".join(diff[:200]),
                "Analyze the differences between these two command outputs:\n"
                f"- Result A: '{result_a}' from {data_a.get('router','?')} ({data_a.get('command','')})\n"
                f"- Result B: '{result_b}' from {data_b.get('router','?')} ({data_b.get('command','')})\n\n"
                "Explain what changed, whether it indicates a problem, and any recommended actions."
            ))
        except Exception:
            ai_analysis = "AI analysis unavailable"
    return jsonify({
        "result_a": {"name": result_a, "router": data_a.get("router"), "command": data_a.get("command"),
                     "captured_at": data_a.get("captured_at"), "lines": len(lines_a)},
        "result_b": {"name": result_b, "router": data_b.get("router"), "command": data_b.get("command"),
                     "captured_at": data_b.get("captured_at"), "lines": len(lines_b)},
        "diff": "\n".join(diff), "additions": sum(1 for l in diff if l.startswith("+") and not l.startswith("+++")),
        "deletions": sum(1 for l in diff if l.startswith("-") and not l.startswith("---")),
        "ai_analysis": ai_analysis, "timestamp": datetime.now().isoformat()
    })

@app.route("/api/results/<name>", methods=["DELETE"])
def api_delete_result(name):
    for f in RESULTS_DIR.glob("*.json"):
        try:
            d = json.loads(f.read_text())
            if d.get("name") == name:
                f.unlink()
                return jsonify({"deleted": name})
        except Exception:
            continue
    return jsonify({"error": "Not found"}), 404


# ══════════════════════════════════════════════════════════════
#  CRON EXPRESSION SCHEDULING (Feature #2)
# ══════════════════════════════════════════════════════════════

def parse_cron_expression(cron_expr: str) -> str:
    """Parse simple cron expressions and return next run as ISO string.
    Supports: '*/5 * * * *' (every 5 min), '0 */2 * * *' (every 2 hours),
    '0 0 * * *' (daily), '30 8 * * 1-5' (weekdays 8:30am), etc.
    Also supports simple aliases: @hourly, @daily, @weekly
    """
    now = datetime.now()
    cron_expr = cron_expr.strip()
    # Aliases
    aliases = {
        "@hourly": "0 * * * *", "@daily": "0 0 * * *",
        "@weekly": "0 0 * * 0", "@midnight": "0 0 * * *",
        "@yearly": "0 0 1 1 *", "@monthly": "0 0 1 * *"
    }
    cron_expr = aliases.get(cron_expr.lower(), cron_expr)
    parts = cron_expr.split()
    if len(parts) != 5:
        return calculate_next_run("1h")  # Fallback
    minute_p, hour_p, dom_p, mon_p, dow_p = parts
    # Simple interval detection: */N
    if minute_p.startswith("*/"):
        interval = int(minute_p[2:])
        next_min = ((now.minute // interval) + 1) * interval
        if next_min >= 60:
            return (now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)).isoformat()
        return now.replace(minute=next_min, second=0, microsecond=0).isoformat()
    if hour_p.startswith("*/"):
        interval = int(hour_p[2:])
        next_hour = ((now.hour // interval) + 1) * interval
        if next_hour >= 24:
            return (now.replace(hour=0, minute=int(minute_p) if minute_p != "*" else 0,
                                second=0, microsecond=0) + timedelta(days=1)).isoformat()
        return now.replace(hour=next_hour, minute=int(minute_p) if minute_p != "*" else 0,
                           second=0, microsecond=0).isoformat()
    # Specific time cron: minute hour * * *
    try:
        target_min = int(minute_p) if minute_p != "*" else 0
        target_hour = int(hour_p) if hour_p != "*" else now.hour
        target = now.replace(hour=target_hour, minute=target_min, second=0, microsecond=0)
        if target <= now:
            target += timedelta(days=1)
        return target.isoformat()
    except (ValueError, TypeError):
        return (now + timedelta(hours=1)).isoformat()


# ══════════════════════════════════════════════════════════════
#  REST CALL & PYTHON SNIPPET WORKFLOW STEPS (Features #4, #5)
# ══════════════════════════════════════════════════════════════
# (Integrated into the existing execute_workflow function)
# See the enhanced workflow executor below

# We need to extend the workflow engine with new step types
_original_execute_workflow = execute_workflow

async def execute_workflow_v2(workflow: dict) -> list:
    """Enhanced workflow executor with REST call & Python snippet steps."""
    results = []
    variables = workflow.get("variables", {})

    for i, step in enumerate(workflow.get("steps", [])):
        step_result = {"step": i + 1, "name": step.get("name", f"Step {i+1}"),
                       "type": step.get("type", "command"), "status": "running"}
        start = time.time()

        try:
            step_type = step.get("type", "command")

            if step_type == "rest_call":
                # REST Call Service
                url = step.get("url", "")
                method = step.get("method", "GET").upper()
                headers = step.get("headers", {})
                body = step.get("body", "")
                # Variable substitution
                for k, v in variables.items():
                    url = url.replace(f"{{{{{k}}}}}", str(v))
                    body = body.replace(f"{{{{{k}}}}}", str(v))
                async with httpx.AsyncClient(timeout=30.0) as client:
                    if method == "POST":
                        resp = await client.post(url, json=json.loads(body) if body else {}, headers=headers)
                    elif method == "PUT":
                        resp = await client.put(url, json=json.loads(body) if body else {}, headers=headers)
                    elif method == "DELETE":
                        resp = await client.delete(url, headers=headers)
                    else:
                        resp = await client.get(url, headers=headers)
                    step_result["output"] = f"HTTP {resp.status_code}\n{resp.text[:3000]}"
                    step_result["status_code"] = resp.status_code
                    # AI analysis of REST response if requested
                    if step.get("ai_analyze_response"):
                        ai = await ollama_analyze_async(
                            "You are an API response analyst.",
                            resp.text[:2000],
                            step.get("ai_question", "Analyze this API response and summarize key findings.")
                        )
                        step_result["ai_analysis"] = ai

            elif step_type == "python_snippet":
                # Python Snippet Service (hardened sandbox)
                code = step.get("code", "")
                for k, v in variables.items():
                    code = code.replace(f"{{{{{k}}}}}", str(v))

                # ── Security: Block dangerous patterns before exec ──
                _BLOCKED_PATTERNS = [
                    r'__\w+__',          # Dunder attributes (bypass builtins)
                    r'import\s+',        # Import statements
                    r'eval\s*\(',        # eval()
                    r'exec\s*\(',        # Nested exec()
                    r'compile\s*\(',     # compile()
                    r'globals\s*\(',     # globals()
                    r'locals\s*\(',      # locals()
                    r'open\s*\(',        # File access
                    r'os\.',             # OS module
                    r'sys\.',            # Sys module
                    r'subprocess',       # Subprocess
                    r'shutil',           # File operations
                    r'pickle',           # Deserialization attacks
                    r'socket',           # Network access
                    r'requests\.',       # HTTP requests
                    r'httpx\.',          # HTTP requests
                    r'getattr\s*\(',     # Attribute access bypass
                    r'setattr\s*\(',     # Attribute modification
                    r'delattr\s*\(',     # Attribute deletion
                    r'breakpoint\s*\(',  # Debugger
                ]
                for pattern in _BLOCKED_PATTERNS:
                    if re.search(pattern, code, re.IGNORECASE):
                        step_result["status"] = "error"
                        step_result["output"] = f"Security: blocked pattern '{pattern}' detected in code snippet"
                        break
                else:
                    # Inject previous step results
                    local_vars = {"results": results, "variables": variables}
                    exec_globals = {"__builtins__": {"len": len, "str": str, "int": int, "float": float,
                                                     "list": list, "dict": dict, "set": set, "tuple": tuple,
                                                     "range": range, "enumerate": enumerate, "zip": zip,
                                                     "sorted": sorted, "filter": filter, "map": map,
                                                     "max": max, "min": min, "sum": sum, "abs": abs,
                                                     "round": round, "print": lambda *a: None,
                                                     "isinstance": isinstance, "type": type,
                                                     "True": True, "False": False, "None": None}}
                    import io
                    old_stdout = sys.stdout
                    sys.stdout = buffer = io.StringIO()
                    try:
                        exec(code, exec_globals, local_vars)
                        step_result["output"] = buffer.getvalue() or local_vars.get("output", "Executed OK")
                    finally:
                        sys.stdout = old_stdout

            elif step_type == "ping_sweep":
                # Ping sweep step
                routers = step.get("routers", [])
                if not routers:
                    routers = [n["id"] for n in build_topology_from_golden_configs().get("nodes", [])]
                result = await mcp_execute_batch("show system uptime", routers)
                step_result["output"] = result

            elif step_type == "validate":
                # Data validation step
                router = step.get("router", "")
                cmd = step.get("command", "")
                pattern = step.get("pattern", "")
                output = await mcp_execute_command(router, cmd)
                passed = bool(re.search(pattern, output, re.IGNORECASE)) if pattern else True
                step_result["output"] = f"{'PASS' if passed else 'FAIL'}: {output[:1000]}"
                step_result["validation_passed"] = passed

            elif step_type == "notify":
                # Send notification step
                channel_id = step.get("channel_id")
                title = step.get("title", "Workflow Alert")
                msg = step.get("message", "")
                # Substitute step references
                if msg.startswith("$step_"):
                    ref_idx = int(msg.split("_")[1]) - 1
                    if 0 <= ref_idx < len(results):
                        msg = results[ref_idx].get("output", "")[:1000]
                if channel_id:
                    conn = sqlite3.connect(str(NOTIFICATIONS_DB))
                    conn.row_factory = sqlite3.Row
                    ch = conn.execute("SELECT * FROM notification_channels WHERE id=?", (channel_id,)).fetchone()
                    if ch:
                        ch = dict(ch)
                        try:
                            payload = {"text": f"*[Workflow] {title}*\n{msg}"}
                            httpx.post(ch["webhook_url"], json=payload, timeout=10.0)
                        except Exception:
                            pass
                    conn.close()
                step_result["output"] = f"Notification sent: {title}"

            else:
                # Delegate to original workflow executor for existing types
                # Re-wrap as single-step workflow
                single = {"steps": [step], "variables": variables}
                sub_results = await _original_execute_workflow(single)
                if sub_results:
                    step_result = sub_results[0]
                    step_result["step"] = i + 1

            step_result["status"] = step_result.get("status", "success")

        except Exception as e:
            step_result["status"] = "error"
            step_result["output"] = str(e)
            if step.get("stop_on_error", False):
                results.append(step_result)
                break

        step_result["duration_ms"] = int((time.time() - start) * 1000)
        results.append(step_result)
        socketio.emit("workflow_progress", {
            "step": i + 1, "total": len(workflow.get("steps", [])),
            "name": step_result["name"], "status": step_result["status"]
        })

    return results


# ══════════════════════════════════════════════════════════════
#  CRON-AWARE SCHEDULER ENDPOINT (Feature #2)
# ══════════════════════════════════════════════════════════════

@app.route("/api/scheduled-tasks/cron", methods=["POST"])
def api_create_cron_task():
    """Create a task with CRON expression scheduling."""
    data = request.json or {}
    name = data.get("name", "")
    command = data.get("command", "")
    cron_expr = data.get("cron", "")
    routers = json.dumps(data.get("routers", []))
    if not name or not command or not cron_expr:
        return jsonify({"error": "name, command, and cron expression required"}), 400
    next_run = parse_cron_expression(cron_expr)
    conn = sqlite3.connect(str(SCHEDULED_DB))
    conn.execute(
        "INSERT INTO scheduled_tasks (name, task_type, schedule, target_routers, command, next_run) VALUES (?,?,?,?,?,?)",
        (name, "cron", cron_expr, routers, command, next_run)
    )
    conn.commit()
    tid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return jsonify({"id": tid, "name": name, "cron": cron_expr, "next_run": next_run})

@app.route("/api/scheduled-tasks/calendar")
def api_task_calendar():
    """Get scheduled tasks formatted for calendar view (Feature #3)."""
    conn = sqlite3.connect(str(SCHEDULED_DB))
    conn.row_factory = sqlite3.Row
    tasks = conn.execute("SELECT * FROM scheduled_tasks ORDER BY next_run").fetchall()
    history = conn.execute(
        "SELECT * FROM task_history ORDER BY run_at DESC LIMIT 100"
    ).fetchall()
    conn.close()
    # Format as calendar events
    events = []
    for t in tasks:
        t = dict(t)
        if t.get("next_run"):
            events.append({
                "id": t["id"], "title": t["name"], "start": t["next_run"],
                "type": "scheduled", "command": t["command"],
                "schedule": t["schedule"], "enabled": bool(t["enabled"])
            })
    for h in history:
        h = dict(h)
        events.append({
            "id": f"h_{h['id']}", "title": f"Ran: Task #{h['task_id']}",
            "start": h["run_at"], "type": "completed",
            "status": h["status"], "duration_ms": h.get("duration_ms", 0)
        })
    return jsonify(events)


# ══════════════════════════════════════════════════════════════
#  NETWORK DISCOVERY & INTERFACE ANALYSIS (Atlas-inspired)
#  Full device discovery, interface enumeration, OS fingerprint,
#  ARP/LLDP neighbor discovery, and infrastructure mapping
# ══════════════════════════════════════════════════════════════

@app.route("/api/discovery/interfaces/<router>")
def api_discovery_interfaces(router):
    """Discover all interfaces on a router with status, IPs, MACs, and traffic stats."""
    try:
        # Gather comprehensive interface data via MCP
        result = run_async(mcp_execute_command(router, "show interfaces terse"))
        detail = run_async(mcp_execute_command(router, "show interfaces descriptions"))
        return jsonify({"router": router, "interfaces": result, "descriptions": detail,
                        "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/discovery/interfaces/<router>/detail")
def api_discovery_interfaces_detail(router):
    """Get detailed interface statistics including errors, CRC, MTU, speed."""
    try:
        result = run_async(mcp_execute_command(router, "show interfaces extensive"))
        return jsonify({"router": router, "detail": result[:10000],
                        "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/discovery/neighbors/<router>")
def api_discovery_neighbors(router):
    """Discover directly connected neighbors via LLDP and ARP."""
    try:
        lldp = run_async(mcp_execute_command(router, "show lldp neighbors"))
        arp = run_async(mcp_execute_command(router, "show arp no-resolve"))
        return jsonify({"router": router, "lldp_neighbors": lldp, "arp_table": arp,
                        "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/discovery/full-scan", methods=["POST"])
def api_discovery_full_scan():
    """Full infrastructure scan across all routers — device inventory, interfaces, neighbors, protocols."""
    data = request.json or {}
    routers = data.get("routers", [])
    if not routers:
        devices = load_devices()
        routers = list(devices.keys())
    scan_results = {}
    for router in routers:
        try:
            facts = run_async(mcp_get_facts(router))
            interfaces = run_async(mcp_execute_command(router, "show interfaces terse"))
            lldp = run_async(mcp_execute_command(router, "show lldp neighbors"))
            version = run_async(mcp_execute_command(router, "show version"))
            scan_results[router] = {
                "facts": facts, "interfaces": interfaces,
                "lldp": lldp, "version": version, "status": "scanned"
            }
        except Exception as e:
            scan_results[router] = {"status": "error", "error": str(e)}
    return jsonify({"scan": scan_results, "total_scanned": len(scan_results),
                    "timestamp": datetime.now().isoformat()})

@app.route("/api/discovery/ai-map", methods=["POST"])
def api_discovery_ai_map():
    """AI analyzes discovery data and builds an infrastructure map with recommendations."""
    data = request.json or {}
    scan_data = data.get("scan_data", "")
    if not scan_data:
        return jsonify({"error": "scan_data required"}), 400
    try:
        analysis = run_async(ollama_analyze_async(
            "You are a senior network architect performing infrastructure discovery analysis.",
            json.dumps(scan_data) if isinstance(scan_data, (dict, list)) else str(scan_data),
            "Analyze this network infrastructure scan and provide:\n"
            "1. Complete device inventory with roles, OS versions, and capabilities\n"
            "2. Layer 2 neighbor map (who connects to whom via which interfaces)\n"
            "3. IP addressing scheme analysis (subnets, VLANs, overlap detection)\n"
            "4. Protocol deployment coverage (IS-IS, BGP, MPLS, LDP per device)\n"
            "5. Anomaly detection: unused interfaces, missing LLDP neighbors, version mismatches\n"
            "6. Infrastructure health score (1-10) with justification\n"
            "7. Recommendations for improvement"
        ))
        return jsonify({"analysis": analysis, "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 503


# ══════════════════════════════════════════════════════════════
#  PROTOCOL TRAFFIC ANALYSIS (mcpcap / Wireshark-MCP inspired)
#  Real-time protocol statistics, traffic flow analysis,
#  session tracking, and anomaly detection via Junos show commands
# ══════════════════════════════════════════════════════════════

@app.route("/api/traffic/protocol-stats/<router>")
def api_traffic_protocol_stats(router):
    """Get protocol hierarchy statistics — equivalent to Wireshark protocol stats."""
    try:
        # Gather protocol statistics from Junos
        isis = run_async(mcp_execute_command(router, "show isis statistics"))
        bgp_summary = run_async(mcp_execute_command(router, "show bgp summary"))
        ospf = run_async(mcp_execute_command(router, "show ospf statistics"))
        ldp = run_async(mcp_execute_command(router, "show ldp statistics"))
        mpls = run_async(mcp_execute_command(router, "show mpls statistics"))
        rsvp = run_async(mcp_execute_command(router, "show rsvp statistics"))
        return jsonify({
            "router": router,
            "protocols": {
                "isis": isis, "bgp": bgp_summary, "ospf": ospf,
                "ldp": ldp, "mpls": mpls, "rsvp": rsvp
            },
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/traffic/interface-counters/<router>")
def api_traffic_interface_counters(router):
    """Get real-time interface traffic counters — packet rates, errors, drops."""
    interface = request.args.get("interface", "")
    try:
        if interface:
            result = run_async(mcp_execute_command(router,
                f"show interfaces {interface} statistics"))
        else:
            result = run_async(mcp_execute_command(router,
                "show interfaces statistics"))
        return jsonify({"router": router, "interface": interface or "all",
                        "counters": result, "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/traffic/flow-analysis/<router>")
def api_traffic_flow_analysis(router):
    """Analyze traffic flows — BGP received/advertised routes, MPLS LSPs, L3VPN tables."""
    try:
        bgp_routes = run_async(mcp_execute_command(router, "show route summary"))
        mpls_lsp = run_async(mcp_execute_command(router, "show mpls lsp brief"))
        ldp_session = run_async(mcp_execute_command(router, "show ldp session"))
        firewall = run_async(mcp_execute_command(router, "show firewall"))
        return jsonify({
            "router": router,
            "flows": {
                "route_summary": bgp_routes, "mpls_lsps": mpls_lsp,
                "ldp_sessions": ldp_session, "firewall_counters": firewall
            },
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/traffic/session-table/<router>")
def api_traffic_session_table(router):
    """Get active sessions/connections — equivalent to TCP stream following."""
    try:
        bgp_neigh = run_async(mcp_execute_command(router, "show bgp neighbor"))
        isis_adj = run_async(mcp_execute_command(router, "show isis adjacency detail"))
        ldp_neigh = run_async(mcp_execute_command(router, "show ldp neighbor"))
        return jsonify({
            "router": router,
            "sessions": {
                "bgp_neighbors": bgp_neigh, "isis_adjacencies": isis_adj,
                "ldp_neighbors": ldp_neigh
            },
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/traffic/ai-analyze", methods=["POST"])
def api_traffic_ai_analyze():
    """AI-powered deep traffic analysis — equivalent to Wireshark expert analysis."""
    data = request.json or {}
    traffic_data = data.get("traffic_data", "")
    analysis_type = data.get("type", "general")  # general, security, performance, anomaly
    if not traffic_data:
        return jsonify({"error": "traffic_data required"}), 400

    type_prompts = {
        "general": "Provide comprehensive protocol traffic analysis: packet counts, session health, "
                   "error rates, and overall protocol stack assessment.",
        "security": "Perform security-focused traffic analysis: detect unauthorized sessions, "
                    "unusual traffic patterns, potential reconnaissance, BGP hijack indicators, "
                    "rogue LLDP neighbors, and cleartext protocol exposure.",
        "performance": "Analyze traffic performance: identify congestion points, high-error interfaces, "
                       "CRC errors, input/output drops, MTU mismatches, and bandwidth utilization issues.",
        "anomaly": "Detect traffic anomalies: sudden traffic spikes, unusual protocol behavior, "
                   "flapping sessions, route oscillation, MPLS label issues, and asymmetric routing."
    }
    try:
        analysis = run_async(ollama_analyze_async(
            "You are a JNCIE-SP certified network traffic analyst with expertise in "
            "packet-level analysis, protocol forensics, and security assessment.",
            json.dumps(traffic_data) if isinstance(traffic_data, (dict, list)) else str(traffic_data),
            type_prompts.get(analysis_type, type_prompts["general"])
        ))
        return jsonify({"analysis": analysis, "type": analysis_type,
                        "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 503


# ══════════════════════════════════════════════════════════════
#  DNS DIAGNOSTICS (dns-mcp-server inspired)
#  DNS resolution analysis, cache inspection, trace path,
#  and batch lookups via Junos DNS capabilities
# ══════════════════════════════════════════════════════════════

@app.route("/api/dns/lookup/<router>")
def api_dns_lookup(router):
    """Perform DNS lookup from a router — resolve hostnames and check DNS health."""
    domain = request.args.get("domain", "")
    record_type = request.args.get("type", "A")
    if not domain:
        return jsonify({"error": "domain parameter required"}), 400
    try:
        # Use Junos ping with count 1 to resolve, and check DNS config
        dns_config = run_async(mcp_execute_command(router, "show configuration system name-server"))
        resolve = run_async(mcp_execute_command(router,
            f"show route resolve {domain}"))
        return jsonify({
            "router": router, "domain": domain, "type": record_type,
            "dns_servers": dns_config, "resolution": resolve,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/dns/reverse/<router>")
def api_dns_reverse_lookup(router):
    """Reverse DNS lookup — convert IP to hostname."""
    ip_address = request.args.get("ip", "")
    if not ip_address:
        return jsonify({"error": "ip parameter required"}), 400
    try:
        result = run_async(mcp_execute_command(router,
            f"show route {ip_address}"))
        return jsonify({"router": router, "ip": ip_address, "result": result,
                        "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/dns/batch", methods=["POST"])
def api_dns_batch_lookup():
    """Batch DNS lookups across multiple domains from a router."""
    data = request.json or {}
    router = data.get("router", "")
    domains = data.get("domains", [])
    if not router or not domains:
        return jsonify({"error": "router and domains required"}), 400
    results = []
    for domain in domains[:20]:  # Limit to 20
        try:
            resolve = run_async(mcp_execute_command(router, f"show route resolve {domain}"))
            results.append({"domain": domain, "result": resolve, "status": "resolved"})
        except Exception as e:
            results.append({"domain": domain, "error": str(e), "status": "failed"})
    return jsonify({"router": router, "results": results, "total": len(results),
                    "timestamp": datetime.now().isoformat()})

@app.route("/api/dns/config-audit", methods=["POST"])
def api_dns_config_audit():
    """AI audit of DNS configuration across routers — detect misconfigs and inconsistencies."""
    data = request.json or {}
    routers = data.get("routers", [])
    if not routers:
        devices = load_devices()
        routers = list(devices.keys())
    dns_configs = {}
    for router in routers:
        try:
            cfg = run_async(mcp_execute_command(router, "show configuration system name-server"))
            dns_configs[router] = cfg
        except Exception as e:
            dns_configs[router] = f"Error: {e}"
    try:
        analysis = run_async(ollama_analyze_async(
            "You are a Junos DNS and naming infrastructure specialist.",
            json.dumps(dns_configs),
            "Audit DNS configuration across these routers:\n"
            "1. DNS server consistency — are all routers using the same name servers?\n"
            "2. Reachability — are the configured DNS servers reachable?\n"
            "3. Redundancy — does each router have at least 2 DNS servers?\n"
            "4. Best practices — NTP sync, DNS timeout settings, search domains\n"
            "5. Security — DNS over TLS/HTTPS availability, DNSSEC support\n"
            "6. Recommendations for improvement"
        ))
        return jsonify({"configs": dns_configs, "analysis": analysis,
                        "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 503


# ══════════════════════════════════════════════════════════════
#  SECURITY THREAT ANALYSIS (Wireshark-MCP inspired)
#  Security audit, threat detection, credential scanning,
#  firewall analysis, and hardening assessment
# ══════════════════════════════════════════════════════════════

@app.route("/api/security/audit/<router>")
def api_security_audit(router):
    """Comprehensive security audit of a router — equivalent to Wireshark security audit workflow."""
    try:
        # Gather security-relevant data via multiple MCP commands
        login = run_async(mcp_execute_command(router, "show system login"))
        ssh = run_async(mcp_execute_command(router, "show configuration system services ssh"))
        snmp = run_async(mcp_execute_command(router, "show configuration snmp"))
        firewall = run_async(mcp_execute_command(router, "show configuration firewall"))
        syslog = run_async(mcp_execute_command(router, "show configuration system syslog"))
        ntp = run_async(mcp_execute_command(router, "show configuration system ntp"))
        alarms = run_async(mcp_execute_command(router, "show system alarms"))
        lo0_filter = run_async(mcp_execute_command(router,
            "show configuration interfaces lo0 unit 0 family inet filter"))
        return jsonify({
            "router": router,
            "security_data": {
                "login_config": login, "ssh_config": ssh, "snmp_config": snmp,
                "firewall_rules": firewall, "syslog_config": syslog,
                "ntp_config": ntp, "alarms": alarms, "lo0_filter": lo0_filter
            },
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/security/threat-check", methods=["POST"])
def api_security_threat_check():
    """AI-powered threat detection — analyze logs and configs for security indicators."""
    data = request.json or {}
    router = data.get("router", "")
    if not router:
        return jsonify({"error": "router required"}), 400
    try:
        # Collect security telemetry
        syslog_msgs = run_async(mcp_execute_command(router, "show log messages | last 100"))
        auth_log = run_async(mcp_execute_command(router, "show log auth | last 50"))
        connections = run_async(mcp_execute_command(router, "show system connections"))
        commit_log = run_async(mcp_execute_command(router, "show system commit"))

        security_data = {
            "syslog": syslog_msgs, "auth_log": auth_log,
            "connections": connections, "commit_history": commit_log
        }
        # AI threat analysis
        analysis = run_async(ollama_analyze_async(
            "You are a senior network security analyst specializing in Junos threat detection.",
            json.dumps(security_data),
            "Perform comprehensive threat analysis:\n"
            "1. Authentication threats: failed logins, brute force indicators, unauthorized access\n"
            "2. Configuration changes: unauthorized commits, suspicious config modifications\n"
            "3. Network anomalies: unexpected connections, unusual traffic patterns\n"
            "4. System integrity: alarm conditions, license issues, hardware alerts\n"
            "5. Compliance violations: missing hardening, exposed services\n"
            "6. Severity classification for each finding (CRITICAL/HIGH/MEDIUM/LOW)\n"
            "7. Recommended incident response actions\n"
            "Present findings in a structured security report format."
        ))
        return jsonify({"router": router, "threat_analysis": analysis,
                        "raw_data": security_data, "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 503

@app.route("/api/security/credential-scan", methods=["POST"])
def api_security_credential_scan():
    """Scan configs for cleartext credentials, weak community strings, and insecure auth."""
    data = request.json or {}
    routers = data.get("routers", [])
    if not routers:
        devices = load_devices()
        routers = list(devices.keys())
    configs = {}
    for router in routers:
        config_path = GOLDEN_CONFIG_DIR / f"{router}.conf"
        if config_path.exists():
            configs[router] = config_path.read_text()
        else:
            # Fallback: pull live config via MCP
            try:
                live = run_async(mcp_get_config(router))
                if live and not live.startswith("Error:") and len(live) > 50:
                    configs[router] = live
            except Exception:
                pass
    if not configs:
        return jsonify({"error": "No configs available. Sync from MCP first."}), 404
    try:
        analysis = run_async(ollama_analyze_async(
            "You are a network security auditor specializing in credential exposure detection.",
            json.dumps({r: c[:3000] for r, c in configs.items()}),
            "Scan these Junos configurations for security credential issues:\n"
            "1. Cleartext passwords (any 'password' not starting with $9$)\n"
            "2. SNMP community strings (especially 'public' or 'private')\n"
            "3. BGP/IS-IS/OSPF authentication — is it MD5 or missing?\n"
            "4. SSH key strength and encryption algorithms\n"
            "5. RADIUS/TACACS+ shared secrets exposure\n"
            "6. Default credentials still present\n"
            "For each finding: device, location in config, severity, and remediation command."
        ))
        return jsonify({"analysis": analysis, "routers_scanned": list(configs.keys()),
                        "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 503

@app.route("/api/security/hardening-report", methods=["POST"])
def api_security_hardening_report():
    """Generate a full security hardening report with CIS benchmark-style scoring."""
    data = request.json or {}
    router = data.get("router", "")
    if not router:
        return jsonify({"error": "router required"}), 400
    config_path = GOLDEN_CONFIG_DIR / f"{router}.conf"
    if config_path.exists():
        config = config_path.read_text()
    else:
        config = run_async(mcp_get_config(router))
        if not config or config.startswith("Error:"):
            return jsonify({"error": f"No config available for {router}"}), 404
    try:
        report = run_async(ollama_analyze_async(
            "You are a JNCIE-SEC certified Junos security engineer conducting a CIS-style hardening assessment.",
            config,
            "Generate a security hardening report for this Junos router. Score each control:\n\n"
            "CONTROL CATEGORIES:\n"
            "1. Management Plane Security (SSH, console, SNMP, NTP, syslog) [20 pts]\n"
            "2. Control Plane Protection (lo0 filter, RE protection, DDoS prevention) [20 pts]\n"
            "3. Data Plane Security (firewall filters, policing, uRPF) [20 pts]\n"
            "4. Routing Protocol Security (IS-IS auth, BGP MD5, route filtering) [20 pts]\n"
            "5. Operational Security (commit confirm, rollback config, rescue config) [20 pts]\n\n"
            "For each category:\n"
            "- Score out of 20\n"
            "- List of checks: PASS / FAIL / WARNING\n"
            "- Specific remediation configs for failures\n"
            "- Overall score out of 100\n"
            "- Risk level: CRITICAL / HIGH / MEDIUM / LOW"
        ))
        return jsonify({"router": router, "hardening_report": report,
                        "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 503


# ══════════════════════════════════════════════════════════════
#  ADVANCED PATH ANALYSIS (PYORPS-inspired)
#  Multi-algorithm path computation, cost-weighted routing,
#  what-if failure analysis, and capacity planning
# ══════════════════════════════════════════════════════════════

@app.route("/api/path/multi-algorithm", methods=["POST"])
def api_path_multi_algorithm():
    """Compute paths using multiple algorithms and compare results."""
    data = request.json or {}
    source = data.get("source", "")
    target = data.get("target", "")
    if not source or not target:
        return jsonify({"error": "source and target required"}), 400
    topo = build_topology_from_golden_configs()
    stats = calculate_network_stats_v2(topo)
    # Build adjacency with costs
    adj = {}
    for link in topo.get("links", []):
        s, t = link["source"], link["target"]
        cost = link.get("metric", 10)
        adj.setdefault(s, []).append((t, cost))
        adj.setdefault(t, []).append((s, cost))
    # Dijkstra shortest path
    import heapq
    def dijkstra(src, dst):
        dist = {src: 0}
        prev = {src: None}
        heap = [(0, src)]
        while heap:
            d, u = heapq.heappop(heap)
            if u == dst:
                break
            if d > dist.get(u, float('inf')):
                continue
            for v, w in adj.get(u, []):
                nd = d + w
                if nd < dist.get(v, float('inf')):
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(heap, (nd, v))
        path = []
        node = dst
        while node is not None:
            path.append(node)
            node = prev.get(node)
        return list(reversed(path)), dist.get(dst, float('inf'))
    # K-shortest paths (Yen's algorithm simplified)
    def k_shortest(src, dst, k=3):
        paths = []
        first_path, first_cost = dijkstra(src, dst)
        if first_path and first_path[0] == src:
            paths.append({"path": first_path, "cost": first_cost})
        # Simple alternative: find paths avoiding intermediate nodes
        for i in range(1, min(k, len(first_path) - 1)):
            spur_node = first_path[i]
            # Remove edges used by existing paths
            temp_adj = {k: list(v) for k, v in adj.items()}
            for p in paths:
                for j in range(len(p["path"]) - 1):
                    ns, nt = p["path"][j], p["path"][j+1]
                    temp_adj[ns] = [(n, c) for n, c in temp_adj.get(ns, []) if n != nt]
            # Find path avoiding the spur
            alt_path, alt_cost = dijkstra(src, dst)
            if alt_path and alt_path not in [p["path"] for p in paths]:
                paths.append({"path": alt_path, "cost": alt_cost})
        return paths
    paths = k_shortest(source, target, k=3)
    return jsonify({
        "source": source, "target": target,
        "algorithms": {
            "dijkstra": {"path": paths[0]["path"] if paths else [], "cost": paths[0]["cost"] if paths else 0},
            "k_shortest": paths,
        },
        "topology_stats": {
            "nodes": len(topo.get("nodes", [])),
            "links": len(topo.get("links", [])),
            "spof": stats.get("single_points_of_failure", [])
        },
        "timestamp": datetime.now().isoformat()
    })

@app.route("/api/path/what-if", methods=["POST"])
def api_path_what_if():
    """What-if failure analysis — simulate node or link failure and compute impact."""
    data = request.json or {}
    failed_node = data.get("failed_node", "")
    failed_link = data.get("failed_link", {})  # {"source": "X", "target": "Y"}
    if not failed_node and not failed_link:
        return jsonify({"error": "failed_node or failed_link required"}), 400
    topo = build_topology_from_golden_configs()
    nodes = [n for n in topo.get("nodes", []) if n["id"] != failed_node]
    links = topo.get("links", [])
    if failed_node:
        links = [l for l in links if l["source"] != failed_node and l["target"] != failed_node]
    if failed_link:
        links = [l for l in links if not (
            (l["source"] == failed_link.get("source") and l["target"] == failed_link.get("target")) or
            (l["source"] == failed_link.get("target") and l["target"] == failed_link.get("source"))
        )]
    # Check connectivity after failure
    adj = {}
    for l in links:
        adj.setdefault(l["source"], set()).add(l["target"])
        adj.setdefault(l["target"], set()).add(l["source"])
    node_ids = [n["id"] for n in nodes]
    # BFS from first node
    if node_ids:
        visited = {node_ids[0]}
        queue = [node_ids[0]]
        while queue:
            current = queue.pop(0)
            for neighbor in adj.get(current, set()):
                if neighbor not in visited and neighbor in node_ids:
                    visited.add(neighbor)
                    queue.append(neighbor)
        connected = len(visited) == len(node_ids)
        isolated = [n for n in node_ids if n not in visited]
    else:
        connected = False
        isolated = []
    # AI impact analysis
    try:
        impact = run_async(ollama_analyze_async(
            "You are a network resilience engineer specializing in failure impact analysis.",
            json.dumps({
                "failed": failed_node or failed_link,
                "remaining_nodes": len(nodes), "remaining_links": len(links),
                "network_connected": connected, "isolated_nodes": isolated,
                "original_nodes": len(topo.get("nodes", [])),
                "original_links": len(topo.get("links", []))
            }),
            "Analyze the impact of this network failure:\n"
            "1. Affected services (VPN, MPLS LSPs, BGP sessions)\n"
            "2. Traffic rerouting paths\n"
            "3. Convergence time estimate\n"
            "4. Customer/service impact severity\n"
            "5. Recommended remediation steps\n"
            "6. Prevention recommendations"
        ))
    except Exception:
        impact = "AI analysis unavailable"
    return jsonify({
        "failure": {"node": failed_node, "link": failed_link},
        "impact": {
            "network_connected": connected, "isolated_nodes": isolated,
            "nodes_remaining": len(nodes), "links_remaining": len(links),
            "nodes_lost": len(topo.get("nodes", [])) - len(nodes),
            "links_lost": len(topo.get("links", [])) - len(links)
        },
        "ai_analysis": impact,
        "timestamp": datetime.now().isoformat()
    })

@app.route("/api/path/capacity-plan", methods=["POST"])
def api_path_capacity_plan():
    """AI-powered capacity planning — analyze topology and recommend where to add capacity."""
    topo = build_topology_from_golden_configs()
    stats = calculate_network_stats_v2(topo)
    try:
        analysis = run_async(ollama_analyze_async(
            "You are a network capacity planning engineer for an SP/ISP network.",
            json.dumps({
                "nodes": [{"id": n["id"], "role": n.get("role", "P"),
                           "interfaces": len(n.get("interfaces", [])),
                           "bgp_peers": len(n.get("bgp_neighbors", [])),
                           "isis_intfs": len(n.get("isis_interfaces", []))}
                          for n in topo.get("nodes", [])],
                "link_count": len(topo.get("links", [])),
                "spof": stats.get("single_points_of_failure", []),
                "redundancy": stats.get("redundancy_score", 0),
                "diameter": stats.get("diameter", 0)
            }),
            "Provide a capacity planning analysis:\n"
            "1. Current capacity utilization assessment per node\n"
            "2. Bottleneck identification (nodes with most traffic paths)\n"
            "3. Where to add new links for redundancy\n"
            "4. Interface capacity upgrades needed\n"
            "5. Growth projection recommendations\n"
            "6. Cost-benefit analysis of proposed changes\n"
            "7. Priority ranking of improvements"
        ))
        return jsonify({"capacity_plan": analysis, "stats": stats,
                        "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 503


# ══════════════════════════════════════════════════════════════
#  LIVE MONITORING & ALERTING (Atlas-inspired auto-scan)
# ══════════════════════════════════════════════════════════════

@app.route("/api/monitor/health-dashboard")
def api_monitor_health_dashboard():
    """Real-time health dashboard data — all protocols across all routers."""
    devices = load_devices()
    routers = list(devices.keys())[:15]  # Limit for performance
    health = {}
    for router in routers:
        try:
            uptime = run_async(mcp_execute_command(router, "show system uptime"))
            alarms = run_async(mcp_execute_command(router, "show system alarms"))
            health[router] = {
                "reachable": True, "uptime": uptime[:500],
                "alarms": alarms[:500],
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            health[router] = {
                "reachable": False, "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    reachable = sum(1 for h in health.values() if h.get("reachable"))
    return jsonify({
        "health": health, "total": len(routers), "reachable": reachable,
        "unreachable": len(routers) - reachable,
        "score": round(reachable / len(routers) * 100, 1) if routers else 0,
        "timestamp": datetime.now().isoformat()
    })

@app.route("/api/monitor/protocol-health")
def api_monitor_protocol_health():
    """Check health of all major protocols across the network."""
    devices = load_devices()
    routers = list(devices.keys())
    # Batch check key protocols
    try:
        isis_result = run_async(mcp_execute_batch("show isis adjacency", routers))
        bgp_result = run_async(mcp_execute_batch("show bgp summary", routers))
        ldp_result = run_async(mcp_execute_batch("show ldp session", routers))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({
        "isis": isis_result[:5000], "bgp": bgp_result[:5000], "ldp": ldp_result[:5000],
        "total_routers": len(routers), "timestamp": datetime.now().isoformat()
    })

@app.route("/api/monitor/ai-incident", methods=["POST"])
def api_monitor_ai_incident():
    """AI-powered incident detection and response recommendation."""
    data = request.json or {}
    symptoms = data.get("symptoms", "")
    if not symptoms:
        return jsonify({"error": "symptoms required"}), 400
    try:
        incident = run_async(ollama_analyze_async(
            "You are a Tier-3 Junos network incident response engineer.",
            str(symptoms),
            "Analyze these network symptoms and provide incident response:\n"
            "1. Incident classification (P1/P2/P3/P4)\n"
            "2. Root cause hypothesis (ranked by probability)\n"
            "3. Affected blast radius (devices, services, customers)\n"
            "4. Immediate triage commands to run on affected routers\n"
            "5. Remediation steps (ordered by priority)\n"
            "6. Escalation criteria\n"
            "7. Post-incident review checklist"
        ))
        return jsonify({"incident_response": incident,
                        "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 503


# ══════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    port = int(os.environ.get("NOC_PORT", 5555))
    # Start the background scheduler
    start_scheduler()
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║   Junos AI NOC — Web UI v22.0 (Full MCP + AI)               ║
║   ─────────────────────────────────────────────────────────  ║
║   URL:    http://localhost:{port}                            ║
║   MCP:    {MCP_SERVER_URL}           ║
║   Ollama: {OLLAMA_URL}                     ║
║   Mode:   {'Development' if os.environ.get('FLASK_DEBUG') else 'Production'}                                      ║
║   Configs: {len(list(GOLDEN_CONFIG_DIR.glob('*.conf')))} golden | Templates: {len(list(TEMPLATES_DIR.glob('*.j2')))}          ║
║   Scheduler: Active | Workflows: {len(list(WORKFLOWS_DIR.glob('*.json')))} saved              ║
╚══════════════════════════════════════════════════════════════╝
""")
    socketio.run(app, host=os.environ.get("NOC_HOST", "127.0.0.1"), port=port,
                 debug=bool(os.environ.get("FLASK_DEBUG")),
                 allow_unsafe_werkzeug=bool(os.environ.get("FLASK_DEBUG")))
