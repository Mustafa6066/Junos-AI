"""
AI Specialist Functions — v16.0

Re-exports protocol-specific AI specialist functions from ollama_mcp_client.

Layer 1 specialists (protocol-specific):
  specialist_ospf, specialist_bgp, specialist_ldp_mpls,
  specialist_l2vpn_evpn, specialist_isis, specialist_system_health,
  specialist_rsvp_te, specialist_qos_cos, specialist_security,
  specialist_l3vpn, specialist_hardware_env

Layer 2 synthesizer:
  specialist_synthesizer

Orchestrators:
  run_layered_analysis, ollama_analyze

Helpers:
  _specialist_call, generate_executive_narrative, ai_guided_troubleshoot

Usage:
    from modules.specialists import run_layered_analysis, specialist_ospf
"""

from ollama_mcp_client import (
    # Core AI
    ollama_analyze,
    run_layered_analysis,
    # Layer 1 specialists
    specialist_ospf,
    specialist_bgp,
    specialist_ldp_mpls,
    specialist_l2vpn_evpn,
    specialist_isis,
    specialist_system_health,
    specialist_rsvp_te,
    specialist_qos_cos,
    specialist_security,
    specialist_l3vpn,
    specialist_hardware_env,
    # Layer 2
    specialist_synthesizer,
    # Helpers
    _specialist_call,
    generate_executive_narrative,
    ai_guided_troubleshoot,
)

__all__ = [
    "ollama_analyze", "run_layered_analysis",
    "specialist_ospf", "specialist_bgp", "specialist_ldp_mpls",
    "specialist_l2vpn_evpn", "specialist_isis", "specialist_system_health",
    "specialist_rsvp_te", "specialist_qos_cos", "specialist_security",
    "specialist_l3vpn", "specialist_hardware_env",
    "specialist_synthesizer",
    "_specialist_call",
    "generate_executive_narrative", "ai_guided_troubleshoot",
]
