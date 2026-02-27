"""
Shared Constants — v16.0

Re-exports pure data structures from ollama_mcp_client.
These are protocol FSM tables, troubleshooting trees, feature matrices,
compliance checks, severity weights, change templates, and runbooks.

Usage:
    from modules.constants import PROTOCOL_FSM, TROUBLESHOOT_TREES
"""

import ollama_mcp_client as _main

# ── Protocol & Network Constants ─────────────────────────────
PROTOCOL_FSM = _main.PROTOCOL_FSM
JUNOS_FEATURE_MATRIX = _main.JUNOS_FEATURE_MATRIX
COMPLIANCE_CHECKS = _main.COMPLIANCE_CHECKS
SEVERITY_WEIGHTS = _main.SEVERITY_WEIGHTS

# ── Troubleshooting Trees ────────────────────────────────────
TROUBLESHOOT_TREES = _main.TROUBLESHOOT_TREES
EXTENDED_TROUBLESHOOT_TREES = _main.EXTENDED_TROUBLESHOOT_TREES

# ── Operational References ───────────────────────────────────
RUNBOOKS = _main.RUNBOOKS
VENDOR_TRANSLATIONS = _main.VENDOR_TRANSLATIONS

# ── Change Management ────────────────────────────────────────
CHANGE_TEMPLATES = _main.CHANGE_TEMPLATES

# ── v16.0 Network Analysis Constants ─────────────────────────
ANALYSIS_PROMPTS = _main.ANALYSIS_PROMPTS
JUNOS_SCRIPT_TEMPLATES = _main.JUNOS_SCRIPT_TEMPLATES
JUNOS_SECURITY_CHECKS = _main.JUNOS_SECURITY_CHECKS
PROTOCOL_DEPENDENCY_GRAPH = _main.PROTOCOL_DEPENDENCY_GRAPH

# ── v16.0 Additional Constants ───────────────────────────────
CASCADING_PATTERNS = _main.CASCADING_PATTERNS
DEVICE_PROFILE_COMMANDS = _main.DEVICE_PROFILE_COMMANDS
JUNOS_ALERT_RULES = _main.JUNOS_ALERT_RULES

# ── Structured Phase Results ─────────────────────────────────
PhaseResult = _main.PhaseResult

__all__ = [
    "PROTOCOL_FSM", "JUNOS_FEATURE_MATRIX", "COMPLIANCE_CHECKS",
    "SEVERITY_WEIGHTS", "TROUBLESHOOT_TREES", "EXTENDED_TROUBLESHOOT_TREES",
    "RUNBOOKS", "VENDOR_TRANSLATIONS", "CHANGE_TEMPLATES",
    "ANALYSIS_PROMPTS", "JUNOS_SCRIPT_TEMPLATES", "JUNOS_SECURITY_CHECKS",
    "PROTOCOL_DEPENDENCY_GRAPH", "CASCADING_PATTERNS",
    "DEVICE_PROFILE_COMMANDS", "JUNOS_ALERT_RULES",
    "PhaseResult",
]
