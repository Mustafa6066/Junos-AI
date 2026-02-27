"""
Junos CLI Output Parsers — v16.0

Re-exports all parser functions from ollama_mcp_client.
These are pure functions for parsing Junos CLI output — no side effects.

Usage:
    from modules.parsers import find_down_interfaces, find_bgp_issues
"""

from ollama_mcp_client import (
    find_down_interfaces,
    parse_interface_detail,
    find_interface_errors,
    find_mtu_mismatches,
    find_ospf_neighbors,
    parse_ospf_intf_types,
    find_ospf_type_mismatches,
    find_bgp_issues,
    find_ldp_issues,
    find_isis_issues,
    find_bfd_issues,
    find_mpls_lsp_issues,
    find_rsvp_issues,
    find_lldp_topology,
    build_loopback_reachability,
    build_reachability_matrix,
    find_alarm_issues,
    find_storage_issues,
    find_coredump_issues,
    find_firewall_issues,
    parse_route_summary,
    parse_commit_history,
    parse_batch_json,
)

__all__ = [
    # Interface parsers
    "find_down_interfaces", "parse_interface_detail",
    "find_interface_errors", "find_mtu_mismatches",
    # Routing protocol parsers
    "find_ospf_neighbors", "parse_ospf_intf_types", "find_ospf_type_mismatches",
    "find_bgp_issues", "find_ldp_issues", "find_isis_issues",
    "find_bfd_issues", "find_mpls_lsp_issues", "find_rsvp_issues",
    # Topology parsers
    "find_lldp_topology", "build_loopback_reachability", "build_reachability_matrix",
    # System parsers
    "find_alarm_issues", "find_storage_issues", "find_coredump_issues",
    "find_firewall_issues", "parse_route_summary", "parse_commit_history",
    "parse_batch_json",
]
