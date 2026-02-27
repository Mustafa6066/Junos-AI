"""
Configuration & State Management — v16.0

Re-exports config, golden config, session, compliance, baseline,
change management, and lessons learned functions from ollama_mcp_client.

Usage:
    from modules.config_mgmt import save_golden_config, load_golden_config
    from modules.config_mgmt import run_compliance_audit
"""

from ollama_mcp_client import (
    # Golden configs
    save_golden_config,
    load_golden_config,
    diff_configs,
    summarize_drift,
    # Session persistence
    save_session_history,
    load_session_history,
    # Compliance
    run_compliance_audit,
    format_compliance_report,
    check_version_compatibility,
    # Baselines
    load_baselines,
    save_baselines,
    detect_baseline_anomalies,
    update_baselines,
    # Change management
    capture_device_state,
    compare_device_states,
    check_change_window,
    simulate_config_impact,
    # Resolution DB
    save_resolution,
    lookup_resolution,
    # Lessons learned
    save_lesson,
    get_top_lessons,
    load_workflow_lessons,
    save_workflow_lesson,
    detect_user_correction,
    generate_lesson_from_correction,
    # Audit DB
    init_audit_db,
    save_audit_to_db,
    get_health_trend,
    get_audit_trends,
    # Device facts
    load_facts_cache,
    save_facts_cache,
    _ensure_golden_dir,
    get_role_commands,
    find_previous_audit,
)

__all__ = [
    # Golden configs
    "save_golden_config", "load_golden_config", "diff_configs", "summarize_drift",
    # Session
    "save_session_history", "load_session_history",
    # Compliance
    "run_compliance_audit", "format_compliance_report", "check_version_compatibility",
    # Baselines
    "load_baselines", "save_baselines", "detect_baseline_anomalies", "update_baselines",
    # Change management
    "capture_device_state", "compare_device_states", "check_change_window",
    "simulate_config_impact",
    # Resolution DB
    "save_resolution", "lookup_resolution",
    # Lessons
    "save_lesson", "get_top_lessons", "load_workflow_lessons",
    "save_workflow_lesson", "detect_user_correction", "generate_lesson_from_correction",
    # Audit DB
    "init_audit_db", "save_audit_to_db", "get_health_trend", "get_audit_trends",
    # Device & config utilities
    "load_facts_cache", "save_facts_cache", "_ensure_golden_dir",
    "get_role_commands", "find_previous_audit",
]
