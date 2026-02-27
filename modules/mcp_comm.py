"""
MCP Communication Layer — v16.0

Re-exports MCP server interaction functions from ollama_mcp_client.

Usage:
    from modules.mcp_comm import run_batch, run_single, mcp_initialize
"""

from ollama_mcp_client import (
    parse_sse_response,
    mcp_post,
    mcp_initialize,
    mcp_list_tools,
    mcp_call_tool,
    run_batch,
    run_single,
    mcp_reconnect,
    parse_batch_json,
)

__all__ = [
    "parse_sse_response", "mcp_post", "mcp_initialize",
    "mcp_list_tools", "mcp_call_tool",
    "run_batch", "run_single", "mcp_reconnect",
    "parse_batch_json",
]
