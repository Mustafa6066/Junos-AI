"""
Audit Engine — v16.0

Re-exports the main audit functions from ollama_mcp_client.

Functions:
  run_full_audit        — Full network audit (2,292 lines — the main engine)
  run_between_devices   — Targeted audit between two specific devices

Usage:
    from modules.audit import run_full_audit, run_between_devices
"""

from ollama_mcp_client import (
    run_full_audit,
    run_between_devices,
)

__all__ = [
    "run_full_audit",
    "run_between_devices",
]
