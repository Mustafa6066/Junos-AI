"""
Topology Engine — v16.0

Re-exports topology building & visualization functions from ollama_mcp_client.

Functions:
  build_live_topology          — Build topology from live MCP data
  topology_to_mermaid          — Convert topology to Mermaid diagram
  topology_to_ascii            — Convert topology to ASCII art
  build_topology_from_golden_configs — Build from golden config files
  topology_to_prompt_string    — Convert topology for AI prompt context
  NetworkDependencyGraph       — Network dependency analysis class

Usage:
    from modules.topology import build_live_topology, topology_to_mermaid
"""

from ollama_mcp_client import (
    build_live_topology,
    topology_to_mermaid,
    topology_to_ascii,
    build_topology_from_golden_configs,
    topology_to_prompt_string,
    NetworkDependencyGraph,
)

__all__ = [
    "build_live_topology", "topology_to_mermaid", "topology_to_ascii",
    "build_topology_from_golden_configs", "topology_to_prompt_string",
    "NetworkDependencyGraph",
]
