"""
Rich Terminal UI Helpers — v16.0

Re-exports UI display functions from ollama_mcp_client.

Functions:
  print_welcome_banner       — Professional startup banner
  print_status_bar           — Status bar with health indicators
  print_command_help         — Command reference table
  print_layer_dashboard      — Layer-by-layer status dashboard
  build_severity_heatmap     — Severity distribution heatmap
  export_report_html         — Export audit report to HTML

Usage:
    from modules.ui import print_welcome_banner, print_command_help
"""

from ollama_mcp_client import (
    print_welcome_banner,
    print_status_bar,
    print_command_help,
    print_layer_dashboard,
    build_severity_heatmap,
    export_report_html,
)

__all__ = [
    "print_welcome_banner", "print_status_bar", "print_command_help",
    "print_layer_dashboard", "build_severity_heatmap", "export_report_html",
]
