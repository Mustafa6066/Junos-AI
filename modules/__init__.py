"""
Junos MCP Bridge — Modular Package v17.0

This package provides logical groupings of the Junos MCP Bridge functions.
Each sub-module re-exports functions from ollama_mcp_client.py so they can
be imported by logical domain:

  modules/
  ├── __init__.py          ← This file
  ├── constants.py         ← Pure data: FSM tables, trees, feature matrices
  ├── parsers.py           ← Junos CLI output parsers (pure functions)
  ├── mcp_comm.py          ← MCP server communication
  ├── specialists.py       ← AI specialist analysis functions
  ├── topology.py          ← Topology building & visualization
  ├── ui.py                ← Rich terminal UI helpers
  ├── audit.py             ← Full audit engine & inter-device analysis
  ├── config_mgmt.py       ← Golden configs, sessions, compliance
  └── intelligence.py      ← AI reasoning, query classification

  Standalone engines (imported directly, not via modules/):
  ├── reasoning_engine.py  ← v15.0 hypothesis-driven investigation
  ├── network_analysis.py  ← v16.0 packet capture, DNS, security audit
  └── hypered_brain.py     ← v17.0 multi-layer AI with self-validation

Usage:
    from modules.parsers import find_down_interfaces, find_bgp_issues
    from modules.constants import PROTOCOL_FSM
    from modules import parsers
    from hypered_brain import hypered_brain_analyze  # v17.0
"""

__version__ = "17.0"

# Import submodules for direct access via `from modules import parsers`
from . import (  # noqa: F401
    constants,
    parsers,
    mcp_comm,
    specialists,
    topology,
    ui,
    audit,
    config_mgmt,
    intelligence,
)

__all__ = [
    "constants",
    "parsers",
    "mcp_comm",
    "specialists",
    "topology",
    "ui",
    "audit",
    "config_mgmt",
    "intelligence",
]
