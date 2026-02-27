"""
MCP Bridge Communication Layer — v16.0

Handles all MCP server communication:
  - SSE response parsing
  - JSON-RPC posting (mcp_post)
  - Session initialization (mcp_initialize)
  - Tool listing & calling (mcp_list_tools, mcp_call_tool)
  - Batch & single command runners (run_batch, run_single)
  - Auto-reconnect (mcp_reconnect)
  - Batch JSON parsing (parse_batch_json)

Extracted from ollama_mcp_client.py for modular architecture.
"""

import asyncio
import json
import logging
import time

from rich.console import Console
from rich.theme import Theme

BRIDGE_THEME = Theme({
    "info": "cyan",
    "success": "bold green",
    "warning": "bold yellow",
    "error": "bold red",
    "critical": "bold white on red",
    "heading": "bold magenta",
    "device": "bold cyan",
    "protocol": "bold blue",
    "command": "dim italic",
    "metric": "bold white",
})

console = Console(theme=BRIDGE_THEME)
logger = logging.getLogger("junos-bridge")

# ── Module-level defaults (overwritten by init_mcp_bridge) ──
MCP_SERVER_URL = "http://127.0.0.1:30030/mcp/"
MCP_CALL_TIMEOUT = 120.0
MCP_BATCH_CONCURRENCY = 2
MCP_BATCH_RETRY = 1
MCP_BATCH_RETRY_DELAY = 3.0
MCP_MAX_RESPONSE_CHARS = 500_000

_mcp_semaphore: asyncio.Semaphore | None = None

# Imported from main module at runtime
_check_circuit_breaker = None
_record_circuit_failure = None
_record_circuit_success = None
_collection_status = None


def init_mcp_bridge(*, mcp_server_url: str, call_timeout: float,
                    batch_concurrency: int, batch_retry: int,
                    batch_retry_delay: float, max_response_chars: int,
                    check_circuit_breaker_fn, record_circuit_failure_fn,
                    record_circuit_success_fn, collection_status_ref: dict):
    """Initialize module globals from the main config.
    
    Called once from main module during startup to avoid circular imports.
    """
    global MCP_SERVER_URL, MCP_CALL_TIMEOUT, MCP_BATCH_CONCURRENCY
    global MCP_BATCH_RETRY, MCP_BATCH_RETRY_DELAY, MCP_MAX_RESPONSE_CHARS
    global _check_circuit_breaker, _record_circuit_failure, _record_circuit_success
    global _collection_status

    MCP_SERVER_URL = mcp_server_url
    MCP_CALL_TIMEOUT = call_timeout
    MCP_BATCH_CONCURRENCY = batch_concurrency
    MCP_BATCH_RETRY = batch_retry
    MCP_BATCH_RETRY_DELAY = batch_retry_delay
    MCP_MAX_RESPONSE_CHARS = max_response_chars
    _check_circuit_breaker = check_circuit_breaker_fn
    _record_circuit_failure = record_circuit_failure_fn
    _record_circuit_success = record_circuit_success_fn
    _collection_status = collection_status_ref


# ═══════════════════════════════════════════════════════════
#  SSE / JSON-RPC Parsing
# ═══════════════════════════════════════════════════════════

def parse_sse_response(text: str) -> dict:
    """Parse SSE event stream and extract the final JSON-RPC result."""
    parsed_messages = []
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("data: "):
            data_str = line[6:]
            try:
                msg = json.loads(data_str)
                parsed_messages.append(msg)
            except json.JSONDecodeError:
                continue
    for msg in reversed(parsed_messages):
        if "result" in msg:
            return msg
    if parsed_messages:
        return parsed_messages[-1]
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {}


# ═══════════════════════════════════════════════════════════
#  MCP POST / Initialize / List / Call
# ═══════════════════════════════════════════════════════════

async def mcp_post(client, session_id, payload, timeout=30.0):
    headers = {"Accept": "application/json, text/event-stream"}
    if session_id:
        headers["mcp-session-id"] = session_id
    resp = await client.post(MCP_SERVER_URL, json=payload, headers=headers, timeout=timeout)
    new_sid = resp.headers.get("mcp-session-id", session_id)
    ct = resp.headers.get("content-type", "")
    raw_text = resp.text
    if len(raw_text) > MCP_MAX_RESPONSE_CHARS:
        logger.warning(f"MCP response truncated: {len(raw_text)} → {MCP_MAX_RESPONSE_CHARS} chars")
        raw_text = raw_text[:MCP_MAX_RESPONSE_CHARS]
    data = parse_sse_response(raw_text) if "text/event-stream" in ct else resp.json()
    return data, new_sid


async def mcp_initialize(client):
    data, sid = await mcp_post(client, None, {
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-03-26", "capabilities": {},
                   "clientInfo": {"name": "ollama-mcp-bridge", "version": "3.0.0"}}
    })
    await client.post(MCP_SERVER_URL,
        json={"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
        headers={"Accept": "application/json, text/event-stream", "mcp-session-id": sid},
        timeout=10.0)
    return sid


async def mcp_list_tools(client, sid):
    data, _ = await mcp_post(client, sid, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    return data.get("result", {}).get("tools", [])


async def mcp_call_tool(client, sid, tool_name, arguments):
    data, _ = await mcp_post(client, sid, {
        "jsonrpc": "2.0", "id": 3, "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments}
    }, timeout=MCP_CALL_TIMEOUT)
    content = data.get("result", {}).get("content", [])
    text = "\n".join(c.get("text", "") for c in content if c.get("type") == "text")
    if not text and data:
        return json.dumps(data)[:2000]
    return text


# ═══════════════════════════════════════════════════════════
#  Batch & Single Command Runners
# ═══════════════════════════════════════════════════════════

async def run_batch(client, sid, command, router_names, label):
    """Run a batch command with concurrency throttling, retry logic, and circuit breaker."""
    global _mcp_semaphore
    if _mcp_semaphore is None:
        _mcp_semaphore = asyncio.Semaphore(MCP_BATCH_CONCURRENCY)

    if _check_circuit_breaker and _check_circuit_breaker(label):
        console.print(f"      [warning]▲ {label}: circuit breaker OPEN (too many recent failures), skipping[/warning]")
        if _collection_status is not None:
            _collection_status[label] = "circuit-breaker-open"
        return ""

    async with _mcp_semaphore:
        console.print(f"   [info]◇ {label}:[/info] [command]{command}[/command]")
        logger.info(f"Batch command: {label} → {command} on {len(router_names)} routers")
        batch_start = time.time()
        last_error = None
        for attempt in range(1, MCP_BATCH_RETRY + 2):
            try:
                result = await asyncio.wait_for(
                    mcp_call_tool(client, sid, "execute_junos_command_batch",
                                  {"command": command, "router_names": router_names}),
                    timeout=MCP_CALL_TIMEOUT
                )
                elapsed = round(time.time() - batch_start, 1)
                result_len = len(result) if result else 0
                console.print(f"      [success]● {result_len} chars ({elapsed}s)[/success]")
                if _collection_status is not None:
                    _collection_status[label] = "success"
                logger.info(f"Batch {label}: success ({result_len} chars, {elapsed}s)")
                if _record_circuit_success:
                    _record_circuit_success(label)
                return result
            except asyncio.TimeoutError:
                last_error = f"Timeout after {MCP_CALL_TIMEOUT}s"
                elapsed = round(time.time() - batch_start, 1)
                if attempt <= MCP_BATCH_RETRY:
                    logger.warning(f"Batch {label}: attempt {attempt} timed out ({elapsed}s), retrying in {MCP_BATCH_RETRY_DELAY}s...")
                    console.print(f"      [warning]▲ {label} attempt {attempt} timed out ({elapsed}s), retrying...[/warning]")
                    await asyncio.sleep(MCP_BATCH_RETRY_DELAY)
                else:
                    console.print(f"      [error]✗ {label}: {last_error}[/error]")
                    if _collection_status is not None:
                        _collection_status[label] = f"failed: {last_error}"
                    logger.error(f"Batch {label}: FAILED after {MCP_BATCH_RETRY} retries ({last_error})")
                    if _record_circuit_failure:
                        _record_circuit_failure(label)
                    return ""
            except Exception as e:
                last_error = e
                elapsed = round(time.time() - batch_start, 1)
                if attempt <= MCP_BATCH_RETRY:
                    logger.warning(f"Batch {label}: attempt {attempt} failed ({e}, {elapsed}s), retrying in {MCP_BATCH_RETRY_DELAY}s...")
                    console.print(f"      [warning]▲ {label} attempt {attempt} failed, retrying...[/warning]")
                    await asyncio.sleep(MCP_BATCH_RETRY_DELAY)
                else:
                    console.print(f"      [error]✗ {label}: {last_error}[/error]")
                    if _collection_status is not None:
                        _collection_status[label] = f"failed: {last_error}"
                    logger.error(f"Batch {label}: FAILED after {MCP_BATCH_RETRY} retries ({last_error})")
                    if _record_circuit_failure:
                        _record_circuit_failure(label)
                    return ""
        return ""


async def run_single(client, sid, command, router_name, label):
    console.print(f"   [info]◇ {label}:[/info] [command]{command} on {router_name}[/command]")
    logger.info(f"Single command: {label} → {command} on {router_name}")
    try:
        result = await asyncio.wait_for(
            mcp_call_tool(client, sid, "execute_junos_command",
                          {"command": command, "router_name": router_name}),
            timeout=MCP_CALL_TIMEOUT
        )
        console.print(f"      [success]● {len(result)} chars[/success]")
        logger.info(f"Single {label}: success ({len(result)} chars)")
        return result
    except asyncio.TimeoutError:
        console.print(f"      [error]✗ Timeout ({MCP_CALL_TIMEOUT}s)[/error]")
        logger.error(f"Single {label}: TIMEOUT after {MCP_CALL_TIMEOUT}s")
        return ""
    except Exception as e:
        console.print(f"      [error]✗ Error: {e}[/error]")
        logger.error(f"Single {label}: FAILED ({e})")
        return ""


async def mcp_reconnect(client) -> str:
    """Re-initialize MCP session after connection loss."""
    print("   ↻ MCP connection lost — attempting reconnect...")
    for attempt in range(3):
        try:
            sid = await mcp_initialize(client)
            print(f"   ● MCP reconnected (attempt {attempt + 1}): {sid}")
            return sid
        except Exception as e:
            wait = 2 ** attempt
            print(f"   ▲ Reconnect attempt {attempt + 1}/3 failed: {e} (retry in {wait}s)")
            await asyncio.sleep(wait)
    raise ConnectionError("MCP server reconnection failed after 3 attempts")


# ═══════════════════════════════════════════════════════════
#  Batch JSON Parser
# ═══════════════════════════════════════════════════════════

def parse_batch_json(raw: str) -> dict:
    """Parse batch command JSON → {router_name: output_text}."""
    result = {}
    try:
        data = json.loads(raw)
        for r in data.get("results", []):
            result[r.get("router_name", "unknown")] = r.get("output", "")
    except (json.JSONDecodeError, KeyError, TypeError):
        pass
    return result
