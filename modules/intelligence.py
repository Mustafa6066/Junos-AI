"""
AI Intelligence & Reasoning — v16.0

Re-exports AI reasoning, query classification, validation, and
diagnostic analysis functions from ollama_mcp_client.

Usage:
    from modules.intelligence import mind_map_reasoning, classify_query
    from modules.intelligence import calculate_health_score
"""

from ollama_mcp_client import (
    # Core AI communication
    ollama_chat,
    mcp_tools_to_ollama_tools,
    smart_truncate_tool_result,
    # Reasoning engines
    mind_map_reasoning,
    structured_reasoning_chain,
    classify_query,
    generate_conversation_summary,
    # Validation & verification
    validate_junos_commands,
    verify_ai_output,
    confidence_gated_specialist,
    _extract_confidence_score,
    _extract_kb_section,
    _extract_kb_subsection,
    _get_relevant_expert_examples,
    # Knowledge loading
    load_knowledge_base,
    load_ecosystem_context,
    get_junos_scripting_context,
    # Health & diagnostics
    calculate_health_score,
    get_fsm_diagnosis,
    identify_cascading_chain,
    save_issue_fingerprints,
    load_issue_fingerprints,
    find_recurring_issues,
    analyze_error_acceleration,
    # Correlation engines
    build_cross_router_correlation,
    build_temporal_correlation,
    build_coverage_matrix,
    validate_fsm_states,
    build_blast_radius,
    build_root_cause_chain,
    estimate_sla_impact,
    # Vendor tools
    translate_command,
    get_vendor_translation_table,
    # Runbooks & proactive
    format_runbook_preview,
    get_runbook_commands,
    check_for_proactive_alerts,
    add_proactive_alert,
    get_last_root_cause_chain,
    # Health polling
    background_health_poll,
    get_health_state_prompt,
    stop_health_poll,
    # Internal utilities
    calculate_confidence_score,
    calculate_risk_score,
    analyze_change_impact,
    assign_itil_priority,
    estimate_tokens,
    trim_messages_by_tokens,
    calculate_budgets,
    validate_ai_references,
    compare_audit_reports,
    format_confidence,
    load_config,
    check_circuit_breaker,
    record_circuit_failure,
    record_circuit_success,
)

__all__ = [
    # Core AI
    "ollama_chat", "mcp_tools_to_ollama_tools", "smart_truncate_tool_result",
    # Reasoning
    "mind_map_reasoning", "structured_reasoning_chain",
    "classify_query", "generate_conversation_summary",
    # Validation
    "validate_junos_commands", "verify_ai_output", "confidence_gated_specialist",
    "_extract_confidence_score", "_extract_kb_section", "_extract_kb_subsection",
    "_get_relevant_expert_examples",
    # Knowledge
    "load_knowledge_base", "load_ecosystem_context", "get_junos_scripting_context",
    # Health & diagnostics
    "calculate_health_score", "get_fsm_diagnosis", "identify_cascading_chain",
    "save_issue_fingerprints", "load_issue_fingerprints", "find_recurring_issues",
    "analyze_error_acceleration",
    # Correlation
    "build_cross_router_correlation", "build_temporal_correlation",
    "build_coverage_matrix", "validate_fsm_states", "build_blast_radius",
    "build_root_cause_chain", "estimate_sla_impact",
    # Vendor
    "translate_command", "get_vendor_translation_table",
    # Runbooks & proactive
    "format_runbook_preview", "get_runbook_commands",
    "check_for_proactive_alerts", "add_proactive_alert", "get_last_root_cause_chain",
    # Health polling
    "background_health_poll", "get_health_state_prompt", "stop_health_poll",
    # Utilities
    "calculate_confidence_score", "calculate_risk_score", "analyze_change_impact",
    "assign_itil_priority", "estimate_tokens", "trim_messages_by_tokens",
    "calculate_budgets", "validate_ai_references", "compare_audit_reports",
    "format_confidence", "load_config",
    "check_circuit_breaker", "record_circuit_failure", "record_circuit_success",
]
