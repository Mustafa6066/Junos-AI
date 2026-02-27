#!/usr/bin/env python3
"""
Network Analysis Engine v16.0 — Advanced Packet, DNS, Security & Telemetry Intelligence

Capabilities adapted from:
  - mcpcap (PCAP protocol analysis — DNS/DHCP/ICMP/TCP)
  - Wireshark-MCP (TShark, Nmap, threat intel, stream following)
  - dns-mcp-server (DNS lookup/trace/batch/reverse)
  - Cisco DevNet AI (alert-driven troubleshooting, telemetry, collaborative analysis)
  - gNMIBuddy (structured network data collection, batch operations)
  - mistral-4-cisco (persistent agent memory, config auditing, vulnerability scanning)

All adapted for Junos MCP — using native Junos CLI commands via MCP instead of
external tools. No TShark/Nmap/Scapy required — everything runs through your
existing Junos MCP server.

Architecture:
  ┌──────────────────────────────────────────────────────────────────┐
  │                  NETWORK ANALYSIS ENGINE                         │
  │                                                                  │
  │  Module 1: PACKET CAPTURE — monitor traffic + flow analysis      │
  │  Module 2: DNS INTELLIGENCE — resolution verification & trace    │
  │  Module 3: SECURITY AUDIT — firewall, ACL, control plane check   │
  │  Module 4: FLOW ANALYSIS — J-Flow, interface counters, QoS       │
  │  Module 5: ALERT ENGINE — threshold monitoring & auto-trigger    │
  │  Module 6: FORENSICS — log correlation, event timeline           │
  │  Module 7: DEVICE PROFILER — health scoring & anomaly detection  │
  │  Module 8: COLLABORATIVE — persistent memory & reporting         │
  └──────────────────────────────────────────────────────────────────┘
"""

import re
import json
import time
import logging
import hashlib
import sqlite3
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from collections import defaultdict

logger = logging.getLogger("junos-network-analysis")


# ══════════════════════════════════════════════════════════════
#  MODULE 1: PACKET CAPTURE INTELLIGENCE
#  (Adapted from mcpcap — DNS/DHCP/ICMP/TCP analysis)
#  Uses Junos "monitor traffic" and "show firewall log" instead of Scapy
# ══════════════════════════════════════════════════════════════

class CaptureProtocol(Enum):
    DNS = "dns"
    DHCP = "dhcp"
    ICMP = "icmp"
    TCP = "tcp"
    BGP = "bgp"
    OSPF = "ospf"
    LDP = "ldp"
    BFD = "bfd"
    ALL = "all"


@dataclass
class CaptureRequest:
    """Request to capture/analyze traffic on a Junos router."""
    router: str
    interface: str = ""          # ge-0/0/0, lo0, etc. (empty = all)
    protocol: CaptureProtocol = CaptureProtocol.ALL
    count: int = 50              # Number of packets
    duration: int = 10           # Seconds
    filter_expression: str = ""  # Junos BPF-like filter
    detail_level: str = "brief"  # brief, detail, extensive


@dataclass
class CaptureResult:
    """Results from traffic capture analysis."""
    router: str
    protocol: str
    packets_captured: int = 0
    packets_analyzed: int = 0
    raw_output: str = ""
    analysis: dict = field(default_factory=dict)
    anomalies: list = field(default_factory=list)
    statistics: dict = field(default_factory=dict)
    timestamp: str = ""


def build_capture_command(request: CaptureRequest) -> str:
    """Build Junos 'monitor traffic' command from a CaptureRequest.
    
    Junos equivalent of Wireshark live capture — no TShark needed.
    """
    cmd = "monitor traffic"
    
    if request.interface:
        cmd += f" interface {request.interface}"
    
    cmd += f" count {request.count}"
    
    # Protocol-specific filters (Junos BPF syntax)
    proto_filters = {
        CaptureProtocol.DNS:  "port 53",
        CaptureProtocol.DHCP: "port 67 or port 68",
        CaptureProtocol.ICMP: "icmp",
        CaptureProtocol.TCP:  "tcp",
        CaptureProtocol.BGP:  "tcp port 179",
        CaptureProtocol.OSPF: "proto ospf",
        CaptureProtocol.LDP:  "tcp port 646 or udp port 646",
        CaptureProtocol.BFD:  "udp port 3784 or udp port 3785",
    }
    
    filter_parts = []
    if request.protocol != CaptureProtocol.ALL:
        filter_parts.append(proto_filters.get(request.protocol, ""))
    if request.filter_expression:
        filter_parts.append(request.filter_expression)
    
    if filter_parts:
        cmd += f" matching \"{' and '.join(f for f in filter_parts if f)}\""
    
    if request.detail_level == "detail":
        cmd += " detail"
    elif request.detail_level == "extensive":
        cmd += " extensive"
    else:
        cmd += " brief"
    
    cmd += " no-resolve"
    return cmd


def parse_capture_output(raw_output: str, protocol: CaptureProtocol) -> CaptureResult:
    """Parse Junos monitor traffic output into structured analysis.
    
    Adapted from mcpcap's protocol-specific analyzers.
    """
    result = CaptureResult(
        router="",
        protocol=protocol.value,
        raw_output=raw_output,
        timestamp=datetime.now().isoformat(),
    )
    
    lines = raw_output.strip().split("\n")
    packets = []
    current_packet = []
    
    for line in lines:
        # Junos monitor traffic packet separator
        if re.match(r'^\d{2}:\d{2}:\d{2}\.\d+', line):
            if current_packet:
                packets.append("\n".join(current_packet))
            current_packet = [line]
        else:
            current_packet.append(line)
    if current_packet:
        packets.append("\n".join(current_packet))
    
    result.packets_captured = len(packets)
    result.packets_analyzed = len(packets)
    
    # Protocol-specific analysis
    if protocol == CaptureProtocol.DNS:
        result.analysis = _analyze_dns_capture(packets)
    elif protocol == CaptureProtocol.ICMP:
        result.analysis = _analyze_icmp_capture(packets)
    elif protocol == CaptureProtocol.TCP:
        result.analysis = _analyze_tcp_capture(packets)
    elif protocol == CaptureProtocol.BGP:
        result.analysis = _analyze_bgp_capture(packets)
    elif protocol == CaptureProtocol.OSPF:
        result.analysis = _analyze_ospf_capture(packets)
    else:
        result.analysis = _analyze_generic_capture(packets)
    
    # Common statistics
    result.statistics = _generate_capture_stats(packets)
    
    return result


def _analyze_dns_capture(packets: list) -> dict:
    """Analyze DNS packets — adapted from mcpcap DNSModule."""
    queries = defaultdict(int)
    responses = defaultdict(int)
    query_types = defaultdict(int)
    nxdomain_count = 0
    servers = set()
    
    for pkt in packets:
        # Extract DNS query/response info from Junos monitor traffic output
        if "A?" in pkt or "AAAA?" in pkt or "MX?" in pkt:
            # DNS query
            m = re.search(r'(\S+)\.\s+(A|AAAA|MX|CNAME|TXT|NS|PTR|SOA|SRV)\?', pkt)
            if m:
                queries[m.group(1)] += 1
                query_types[m.group(2)] += 1
        if "NXDomain" in pkt:
            nxdomain_count += 1
        # Extract DNS server IPs
        m = re.search(r'>\s+(\d+\.\d+\.\d+\.\d+)\.53:', pkt)
        if m:
            servers.add(m.group(1))
    
    return {
        "total_queries": sum(queries.values()),
        "total_responses": sum(responses.values()),
        "unique_domains": len(queries),
        "top_queried_domains": dict(sorted(queries.items(), key=lambda x: -x[1])[:10]),
        "query_type_distribution": dict(query_types),
        "nxdomain_count": nxdomain_count,
        "dns_servers_contacted": list(servers),
        "potential_issues": _detect_dns_anomalies(queries, nxdomain_count),
    }


def _detect_dns_anomalies(queries: dict, nxdomain_count: int) -> list:
    """Detect DNS anomalies — adapted from mcpcap security_analysis prompt."""
    anomalies = []
    
    # DGA detection: lots of queries for random-looking domains
    random_domains = [d for d in queries if len(d) > 20 and sum(c.isdigit() for c in d) > 5]
    if random_domains:
        anomalies.append({
            "type": "potential_dga",
            "severity": "HIGH",
            "description": f"Found {len(random_domains)} domains with DGA-like patterns",
            "domains": random_domains[:5],
        })
    
    # High NXDOMAIN rate suggests reconnaissance or misconfiguration
    total_q = sum(queries.values())
    if total_q > 0 and nxdomain_count / total_q > 0.3:
        anomalies.append({
            "type": "high_nxdomain_rate",
            "severity": "MEDIUM",
            "description": f"NXDOMAIN rate is {nxdomain_count}/{total_q} ({100*nxdomain_count/total_q:.0f}%) — possible DNS tunneling or misconfiguration",
        })
    
    # Single domain queried excessively (possible DNS tunneling)
    for domain, count in queries.items():
        if count > 50:
            anomalies.append({
                "type": "excessive_queries",
                "severity": "MEDIUM",
                "description": f"Domain '{domain}' queried {count} times — possible DNS tunneling",
            })
    
    return anomalies


def _analyze_icmp_capture(packets: list) -> dict:
    """Analyze ICMP packets — adapted from mcpcap ICMPModule."""
    echo_requests = 0
    echo_replies = 0
    unreachable = 0
    time_exceeded = 0
    ttl_values = []
    round_trips = []
    sources = defaultdict(int)
    
    for pkt in packets:
        if "echo request" in pkt.lower() or "icmp: echo" in pkt.lower():
            echo_requests += 1
        elif "echo reply" in pkt.lower():
            echo_replies += 1
        elif "unreachable" in pkt.lower():
            unreachable += 1
        elif "time exceeded" in pkt.lower():
            time_exceeded += 1
        
        # Extract TTL
        m = re.search(r'ttl\s*[=:]\s*(\d+)', pkt, re.IGNORECASE)
        if m:
            ttl_values.append(int(m.group(1)))
        
        # Extract source IPs
        m = re.match(r'\d{2}:\d{2}:\d{2}\.\d+\s+\S+\s+(\d+\.\d+\.\d+\.\d+)', pkt)
        if m:
            sources[m.group(1)] += 1
    
    return {
        "echo_requests": echo_requests,
        "echo_replies": echo_replies,
        "unreachable": unreachable,
        "time_exceeded": time_exceeded,
        "loss_rate": f"{100*(1 - echo_replies/max(echo_requests,1)):.1f}%" if echo_requests else "N/A",
        "avg_ttl": sum(ttl_values) / max(len(ttl_values), 1) if ttl_values else 0,
        "unique_sources": len(sources),
        "top_sources": dict(sorted(sources.items(), key=lambda x: -x[1])[:5]),
    }


def _analyze_tcp_capture(packets: list) -> dict:
    """Analyze TCP packets — adapted from mcpcap TCPModule."""
    syn_count = 0
    syn_ack_count = 0
    fin_count = 0
    rst_count = 0
    connections = defaultdict(list)
    
    for pkt in packets:
        flags = ""
        m = re.search(r'Flags\s+\[([^\]]+)\]', pkt)
        if m:
            flags = m.group(1)
        
        if "S" in flags and "." not in flags:
            syn_count += 1
        if "S" in flags and "." in flags:
            syn_ack_count += 1
        if "F" in flags:
            fin_count += 1
        if "R" in flags:
            rst_count += 1
        
        # Track connections by src:port → dst:port
        m = re.search(r'(\d+\.\d+\.\d+\.\d+)\.(\d+)\s+>\s+(\d+\.\d+\.\d+\.\d+)\.(\d+)', pkt)
        if m:
            key = f"{m.group(1)}:{m.group(2)}->{m.group(3)}:{m.group(4)}"
            connections[key].append(flags)
    
    anomalies = []
    if rst_count > syn_count * 0.3 and syn_count > 0:
        anomalies.append({
            "type": "high_rst_rate",
            "severity": "HIGH",
            "description": f"RST rate is {rst_count}/{syn_count} ({100*rst_count/syn_count:.0f}%) — possible firewall blocks or port scanning",
        })
    if syn_count > 0 and syn_ack_count / syn_count < 0.5:
        anomalies.append({
            "type": "low_syn_ack_ratio",
            "severity": "HIGH",
            "description": f"Only {syn_ack_count}/{syn_count} SYN-ACKs received — handshake failures",
        })
    
    return {
        "syn_count": syn_count,
        "syn_ack_count": syn_ack_count,
        "fin_count": fin_count,
        "rst_count": rst_count,
        "unique_connections": len(connections),
        "handshake_success_rate": f"{100*syn_ack_count/max(syn_count,1):.0f}%",
        "anomalies": anomalies,
    }


def _analyze_bgp_capture(packets: list) -> dict:
    """Analyze BGP control packets — unique to Junos MCP."""
    open_msgs = 0
    update_msgs = 0
    keepalive_msgs = 0
    notification_msgs = 0
    
    for pkt in packets:
        p_lower = pkt.lower()
        if "open" in p_lower:
            open_msgs += 1
        elif "update" in p_lower:
            update_msgs += 1
        elif "keepalive" in p_lower:
            keepalive_msgs += 1
        elif "notification" in p_lower:
            notification_msgs += 1
    
    return {
        "open_messages": open_msgs,
        "update_messages": update_msgs,
        "keepalive_messages": keepalive_msgs,
        "notification_messages": notification_msgs,
        "health": "healthy" if notification_msgs == 0 else "issues_detected",
    }


def _analyze_ospf_capture(packets: list) -> dict:
    """Analyze OSPF control packets — unique to Junos MCP."""
    hello_count = 0
    dbd_count = 0
    lsr_count = 0
    lsu_count = 0
    lsa_ack_count = 0
    
    for pkt in packets:
        p_lower = pkt.lower()
        if "hello" in p_lower:
            hello_count += 1
        elif "database description" in p_lower or "dbd" in p_lower:
            dbd_count += 1
        elif "ls request" in p_lower or "lsr" in p_lower:
            lsr_count += 1
        elif "ls update" in p_lower or "lsu" in p_lower:
            lsu_count += 1
        elif "ls ack" in p_lower:
            lsa_ack_count += 1
    
    return {
        "hello_packets": hello_count,
        "database_description": dbd_count,
        "ls_request": lsr_count,
        "ls_update": lsu_count,
        "ls_ack": lsa_ack_count,
        "convergence_activity": "active" if lsu_count > 0 else "stable",
    }


def _analyze_generic_capture(packets: list) -> dict:
    """Generic packet analysis for any protocol."""
    protocols = defaultdict(int)
    sources = defaultdict(int)
    destinations = defaultdict(int)
    
    for pkt in packets:
        m = re.match(r'\d{2}:\d{2}:\d{2}\.\d+\s+\S+\s+(\d+\.\d+\.\d+\.\d+)\S*\s+>\s+(\d+\.\d+\.\d+\.\d+)', pkt)
        if m:
            sources[m.group(1)] += 1
            destinations[m.group(2)] += 1
        
        # Detect protocol
        for proto in ["TCP", "UDP", "ICMP", "OSPF", "BGP", "LDP", "BFD"]:
            if proto.lower() in pkt.lower():
                protocols[proto] += 1
                break
    
    return {
        "protocol_distribution": dict(protocols),
        "top_sources": dict(sorted(sources.items(), key=lambda x: -x[1])[:5]),
        "top_destinations": dict(sorted(destinations.items(), key=lambda x: -x[1])[:5]),
    }


def _generate_capture_stats(packets: list) -> dict:
    """Generate summary statistics from capture — adapted from mcpcap CapInfos."""
    if not packets:
        return {"total_packets": 0}
    
    timestamps = []
    sizes = []
    for pkt in packets:
        m = re.match(r'(\d{2}):(\d{2}):(\d{2})\.(\d+)', pkt)
        if m:
            ts = int(m.group(1))*3600 + int(m.group(2))*60 + int(m.group(3)) + int(m.group(4))/1000000
            timestamps.append(ts)
        # Estimate packet size from length field
        m2 = re.search(r'length\s+(\d+)', pkt, re.IGNORECASE)
        if m2:
            sizes.append(int(m2.group(1)))
    
    duration = max(timestamps) - min(timestamps) if len(timestamps) > 1 else 0
    
    return {
        "total_packets": len(packets),
        "duration_seconds": round(duration, 3),
        "packets_per_second": round(len(packets) / max(duration, 0.001), 1),
        "avg_packet_size": round(sum(sizes) / max(len(sizes), 1)) if sizes else "unknown",
        "total_bytes": sum(sizes) if sizes else "unknown",
    }


# ══════════════════════════════════════════════════════════════
#  MODULE 2: DNS INTELLIGENCE
#  (Adapted from dns-mcp-server — lookup, reverse, batch, trace)
#  Uses Junos DNS commands instead of external DNS resolvers
# ══════════════════════════════════════════════════════════════

@dataclass
class DNSLookupResult:
    domain: str
    record_type: str
    results: list = field(default_factory=list)
    server_used: str = ""
    response_time_ms: float = 0.0
    status: str = "success"
    error: str = ""


def build_dns_commands(domain: str, record_types: Optional[list] = None,
                       dns_server: str = "") -> list:
    """Build Junos commands for DNS resolution verification.
    
    Unlike external DNS tools, this verifies DNS from the router's perspective —
    which is what matters for routing (BGP next-hop, OSPF FQDN, etc.)
    
    Adapted from dns-mcp-server's dns_lookup/reverse_dns/batch_dns tools.
    """
    if record_types is None:
        record_types = ["A"]
    
    commands = []
    
    for rtype in record_types:
        # Junos native DNS lookup
        if dns_server:
            commands.append(f"show system name-server | no-more")
        
        # Use operational mode DNS resolution
        if rtype in ["A", "AAAA"]:
            commands.append(f"show host {domain}")
        elif rtype == "PTR":
            # Reverse DNS — build in-addr.arpa from IP
            octets = domain.split(".")
            if len(octets) == 4:
                arpa = ".".join(reversed(octets)) + ".in-addr.arpa"
                commands.append(f"show host {arpa}")
            else:
                commands.append(f"show host {domain}")
        elif rtype == "MX":
            commands.append(f"show host {domain}")
        else:
            commands.append(f"show host {domain}")
    
    return commands


def build_dns_trace_commands(domain: str) -> list:
    """Build commands to trace DNS resolution path.
    
    Adapted from dns-mcp-server's dns_trace tool.
    On Junos: traceroute + DNS config verification.
    """
    return [
        f"show host {domain}",
        "show system name-server",
        "show configuration system name-server",
        f"traceroute {domain} no-resolve",
        "show system statistics icmp | match \"echo|unreach\"",
    ]


def parse_dns_output(output: str, domain: str) -> DNSLookupResult:
    """Parse Junos 'show host' output into structured DNS result."""
    result = DNSLookupResult(domain=domain, record_type="A")
    
    lines = output.strip().split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # "hostname has address 1.2.3.4"
        m = re.search(r'has address\s+(\S+)', line)
        if m:
            result.results.append({"type": "A", "value": m.group(1)})
            continue
        
        # "hostname has IPv6 address ::1"
        m = re.search(r'has IPv6 address\s+(\S+)', line)
        if m:
            result.results.append({"type": "AAAA", "value": m.group(1)})
            continue
        
        # "hostname mail is handled by 10 mail.example.com."
        m = re.search(r'mail is handled by\s+(\d+)\s+(\S+)', line)
        if m:
            result.results.append({"type": "MX", "priority": int(m.group(1)), "value": m.group(2)})
            continue
        
        # "hostname is an alias for other.example.com."
        m = re.search(r'is an alias for\s+(\S+)', line)
        if m:
            result.results.append({"type": "CNAME", "value": m.group(1)})
            continue
        
        # "Host not found"
        if "not found" in line.lower() or "nxdomain" in line.lower():
            result.status = "NXDOMAIN"
            result.error = line
    
    if not result.results and result.status == "success":
        result.status = "no_records"
    
    return result


def build_batch_dns_commands(queries: list) -> list:
    """Build batch DNS resolution commands for multiple domains.
    
    Adapted from dns-mcp-server's batch_dns tool.
    Returns {router: [commands]} for parallel execution.
    """
    all_commands = []
    for q in queries:
        domain = q.get("domain", "")
        record_types = q.get("record_types", ["A"])
        all_commands.extend(build_dns_commands(domain, record_types))
    return all_commands


# ══════════════════════════════════════════════════════════════
#  MODULE 3: SECURITY AUDIT ENGINE
#  (Adapted from Wireshark-MCP threat intel + Cisco security agent)
#  Uses Junos firewall, prefix-list, and policy analysis
# ══════════════════════════════════════════════════════════════

class SecuritySeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class SecurityFinding:
    """A security finding from audit — adapted from Wireshark-MCP threat model."""
    category: str            # firewall, acl, control_plane, credentials, config
    severity: SecuritySeverity
    title: str
    description: str
    device: str = ""
    evidence: str = ""
    remediation: str = ""
    cve_reference: str = ""  # If applicable


# ── Security Audit Checks (adapted from Wireshark-MCP security_audit prompt
#    and mistral-4-cisco vulnerability scanning) ──

JUNOS_SECURITY_CHECKS = {
    "control_plane_protection": {
        "commands": [
            "show configuration firewall family inet filter protect-re",
            "show configuration firewall family inet filter lo0-filter",
            "show configuration interfaces lo0",
        ],
        "check": "verify_loopback_filter",
        "severity": SecuritySeverity.CRITICAL,
        "title": "Control Plane (lo0) Firewall Filter",
        "description": "Verify that a firewall filter is applied to lo0 to protect the RE",
        "remediation": "set interfaces lo0 unit 0 family inet filter input protect-re",
    },
    "ssh_security": {
        "commands": [
            "show configuration system services ssh",
            "show configuration system login",
        ],
        "check": "verify_ssh_config",
        "severity": SecuritySeverity.HIGH,
        "title": "SSH Security Configuration",
        "description": "Verify SSH uses v2 only, root-login disabled, rate-limit set",
        "remediation": "set system services ssh protocol-version v2; set system services ssh root-login deny; set system services ssh rate-limit 5",
    },
    "snmp_security": {
        "commands": [
            "show configuration snmp",
        ],
        "check": "verify_snmp_config",
        "severity": SecuritySeverity.HIGH,
        "title": "SNMP Community String Security",
        "description": "Check for default/weak SNMP community strings",
        "remediation": "set snmp community <complex-string> authorization read-only",
    },
    "ntp_authentication": {
        "commands": [
            "show configuration system ntp",
        ],
        "check": "verify_ntp_config",
        "severity": SecuritySeverity.MEDIUM,
        "title": "NTP Authentication",
        "description": "Verify NTP uses authentication to prevent time-based attacks",
        "remediation": "set system ntp authentication-key <id> type md5 value <key>",
    },
    "bgp_authentication": {
        "commands": [
            "show configuration protocols bgp",
        ],
        "check": "verify_bgp_auth",
        "severity": SecuritySeverity.CRITICAL,
        "title": "BGP Session Authentication",
        "description": "Verify all BGP peers use MD5 authentication",
        "remediation": "set protocols bgp group <name> authentication-key <key>",
    },
    "ospf_authentication": {
        "commands": [
            "show configuration protocols ospf",
        ],
        "check": "verify_ospf_auth",
        "severity": SecuritySeverity.HIGH,
        "title": "OSPF Area Authentication",
        "description": "Verify OSPF areas use authentication",
        "remediation": "set protocols ospf area 0 interface <intf> authentication md5 1 key <key>",
    },
    "isis_authentication": {
        "commands": [
            "show configuration protocols isis",
        ],
        "check": "verify_isis_auth",
        "severity": SecuritySeverity.HIGH,
        "title": "IS-IS Authentication",
        "description": "Verify IS-IS uses authentication",
        "remediation": "set protocols isis level 2 authentication-key <key> authentication-type md5",
    },
    "ldp_authentication": {
        "commands": [
            "show configuration protocols ldp",
        ],
        "check": "verify_ldp_auth",
        "severity": SecuritySeverity.MEDIUM,
        "title": "LDP Session Authentication",
        "description": "Verify LDP sessions use MD5 authentication",
        "remediation": "set protocols ldp session <peer> authentication-key <key>",
    },
    "prefix_list_protection": {
        "commands": [
            "show configuration policy-options prefix-list",
            "show configuration protocols bgp",
        ],
        "check": "verify_prefix_lists",
        "severity": SecuritySeverity.HIGH,
        "title": "BGP Prefix-List / Route Policy Protection",
        "description": "Verify BGP peers have import/export policies with prefix-list limits",
        "remediation": "set protocols bgp group <name> import <policy>",
    },
    "unused_interfaces": {
        "commands": [
            "show interfaces terse | match \"down.*down\"",
            "show configuration interfaces",
        ],
        "check": "verify_unused_intfs",
        "severity": SecuritySeverity.MEDIUM,
        "title": "Unused Interface Hardening",
        "description": "Verify unused interfaces are disabled (admin down)",
        "remediation": "set interfaces <intf> disable",
    },
    "syslog_config": {
        "commands": [
            "show configuration system syslog",
        ],
        "check": "verify_syslog",
        "severity": SecuritySeverity.MEDIUM,
        "title": "Syslog / Remote Logging",
        "description": "Verify syslog is configured for remote logging",
        "remediation": "set system syslog host <server> any warning; set system syslog host <server> authorization info",
    },
    "login_banner": {
        "commands": [
            "show configuration system login message",
            "show configuration system login announcement",
        ],
        "check": "verify_login_banner",
        "severity": SecuritySeverity.LOW,
        "title": "Login Banner / Legal Notice",
        "description": "Verify a login banner is configured for legal compliance",
        "remediation": 'set system login message "AUTHORIZED ACCESS ONLY"',
    },
}


def analyze_security_output(check_name: str, outputs: dict) -> SecurityFinding:
    """Analyze the output from security check commands.
    
    Adapted from Wireshark-MCP threat_intel + mistral-4-cisco audit logic.
    """
    check = JUNOS_SECURITY_CHECKS.get(check_name)
    if not check:
        return SecurityFinding(
            category="unknown", severity=SecuritySeverity.INFO,
            title="Unknown Check", description=f"No check definition for {check_name}"
        )
    
    combined_output = "\n".join(str(v) for v in outputs.values()).lower()
    
    finding = SecurityFinding(
        category=check_name,
        severity=check["severity"],
        title=check["title"],
        description=check["description"],
        remediation=check["remediation"],
    )
    
    # Check-specific analysis
    if check_name == "control_plane_protection":
        if "filter" not in combined_output or "lo0" not in combined_output:
            finding.evidence = "No firewall filter found on lo0 — RE is unprotected"
        else:
            finding.severity = SecuritySeverity.INFO
            finding.evidence = "lo0 filter is applied ●"
    
    elif check_name == "ssh_security":
        issues = []
        if "root-login" not in combined_output or "deny" not in combined_output:
            issues.append("root-login not denied")
        if "protocol-version v2" not in combined_output and "v2" not in combined_output:
            issues.append("SSH v2 not enforced")
        if "rate-limit" not in combined_output:
            issues.append("No rate-limit on SSH")
        if issues:
            finding.evidence = "; ".join(issues)
        else:
            finding.severity = SecuritySeverity.INFO
            finding.evidence = "SSH configuration looks secure ●"
    
    elif check_name == "snmp_security":
        weak_communities = ["public", "private", "community", "test", "default"]
        found_weak = [c for c in weak_communities if c in combined_output]
        if found_weak:
            finding.evidence = f"Weak SNMP community strings found: {', '.join(found_weak)}"
        elif "snmp" not in combined_output:
            finding.severity = SecuritySeverity.INFO
            finding.evidence = "SNMP not configured (may be intentional)"
        else:
            finding.severity = SecuritySeverity.INFO
            finding.evidence = "SNMP community strings appear non-default ●"
    
    elif check_name == "bgp_authentication":
        if "authentication-key" not in combined_output and "authentication-algorithm" not in combined_output:
            finding.evidence = "No BGP authentication configured — sessions vulnerable to spoofing"
        else:
            finding.severity = SecuritySeverity.INFO
            finding.evidence = "BGP authentication is configured ●"
    
    elif check_name == "ospf_authentication":
        if "authentication" not in combined_output:
            finding.evidence = "No OSPF authentication — neighbors could be spoofed"
        else:
            finding.severity = SecuritySeverity.INFO
            finding.evidence = "OSPF authentication is configured ●"
    
    elif check_name == "isis_authentication":
        if "authentication" not in combined_output:
            finding.evidence = "No IS-IS authentication — adjacencies could be spoofed"
        else:
            finding.severity = SecuritySeverity.INFO
            finding.evidence = "IS-IS authentication is configured ●"
    
    elif check_name == "ldp_authentication":
        if "authentication" not in combined_output:
            finding.evidence = "No LDP authentication — sessions vulnerable to hijacking"
        else:
            finding.severity = SecuritySeverity.INFO
            finding.evidence = "LDP authentication is configured ●"
    
    elif check_name == "prefix_list_protection":
        if "import" not in combined_output and "export" not in combined_output:
            finding.evidence = "No import/export policies on BGP — route leaking risk"
        else:
            finding.severity = SecuritySeverity.INFO
            finding.evidence = "BGP policies are configured ●"
    
    elif check_name == "syslog_config":
        if "host" not in combined_output:
            finding.evidence = "No remote syslog configured — events may be lost"
        else:
            finding.severity = SecuritySeverity.INFO
            finding.evidence = "Remote syslog is configured ●"
    
    elif check_name == "ntp_authentication":
        if "authentication" not in combined_output:
            finding.evidence = "NTP without authentication — time spoofing possible"
        else:
            finding.severity = SecuritySeverity.INFO
            finding.evidence = "NTP authentication is configured ●"
    
    elif check_name == "login_banner":
        if "message" not in combined_output and "announcement" not in combined_output:
            finding.evidence = "No login banner configured"
        else:
            finding.severity = SecuritySeverity.INFO
            finding.evidence = "Login banner is configured ●"
    
    elif check_name == "unused_interfaces":
        down_intfs = re.findall(r'(ge-\S+|xe-\S+|et-\S+)\s+\S+\s+down\s+down', combined_output)
        if down_intfs:
            finding.evidence = f"Found {len(down_intfs)} down interfaces that should be admin-disabled: {', '.join(down_intfs[:5])}"
        else:
            finding.severity = SecuritySeverity.INFO
            finding.evidence = "No unmanaged down interfaces found ●"
    
    return finding


def generate_security_report(findings: list) -> str:
    """Generate a formatted security audit report.
    
    Adapted from Wireshark-MCP security_audit prompt + mistral-4-cisco report format.
    """
    lines = []
    lines.append("# ⊘ Junos Security Audit Report")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    
    # Summary counters
    by_severity = defaultdict(list)
    for f in findings:
        by_severity[f.severity.value].append(f)
    
    lines.append("## Executive Summary")
    lines.append(f"- [red]●[/red] **Critical:** {len(by_severity.get('critical', []))}")
    lines.append(f"- [#ff8700]●[/#ff8700] **High:** {len(by_severity.get('high', []))}")
    lines.append(f"- [yellow]●[/yellow] **Medium:** {len(by_severity.get('medium', []))}")
    lines.append(f"- [blue]●[/blue] **Low:** {len(by_severity.get('low', []))}")
    lines.append(f"- [green]●[/green] **Passed:** {len(by_severity.get('info', []))}")
    lines.append("")
    
    # Score
    total_checks = len(findings)
    passed = len(by_severity.get("info", []))
    score = int(100 * passed / max(total_checks, 1))
    bar_len = score // 5
    bar = "█" * bar_len + "░" * (20 - bar_len)
    lines.append(f"## Security Score: [{bar}] {score}%")
    lines.append("")
    
    # Detailed findings (non-passing first)
    severity_order = ["critical", "high", "medium", "low", "info"]
    severity_icons = {"critical": "[red]●[/red]", "high": "[#ff8700]●[/#ff8700]", "medium": "[yellow]●[/yellow]", "low": "[blue]●[/blue]", "info": "[green]●[/green]"}
    
    for sev in severity_order:
        sev_findings = by_severity.get(sev, [])
        if not sev_findings:
            continue
        
        lines.append(f"## {severity_icons[sev]} {sev.upper()} Findings")
        for f in sev_findings:
            lines.append(f"### {f.title}")
            lines.append(f"- **Category:** {f.category}")
            if f.device:
                lines.append(f"- **Device:** {f.device}")
            lines.append(f"- **Evidence:** {f.evidence}")
            if f.remediation and sev != "info":
                lines.append(f"- **Remediation:** `{f.remediation}`")
            lines.append("")
    
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════
#  MODULE 4: FLOW & PERFORMANCE ANALYSIS
#  (Adapted from mcpcap traffic_flow + Wireshark-MCP protocol stats)
#  Uses Junos J-Flow, interface counters, CoS
# ══════════════════════════════════════════════════════════════

@dataclass
class FlowAnalysisResult:
    """Traffic flow analysis result — adapted from mcpcap analyze_traffic_flow."""
    interface: str
    direction: str            # inbound, outbound, bidirectional
    total_bytes: int = 0
    total_packets: int = 0
    rate_bps: float = 0.0
    rate_pps: float = 0.0
    utilization_pct: float = 0.0
    top_protocols: dict = field(default_factory=dict)
    error_counters: dict = field(default_factory=dict)
    qos_stats: dict = field(default_factory=dict)


FLOW_ANALYSIS_COMMANDS = {
    "interface_counters": "show interfaces {intf} extensive | no-more",
    "interface_errors": "show interfaces {intf} extensive | match \"error|drop|discard|overflow\"",
    "cos_counters": "show class-of-service interface {intf} | no-more",
    "queue_stats": "show interfaces queue {intf} | no-more",
    "traffic_stats": "show interfaces {intf} statistics detail | no-more",
    "policer_stats": "show firewall filter {filter} | no-more",
    "flow_table": "show services flow-monitoring version-ipfix template | no-more",
}


def build_flow_commands(interface: str) -> list:
    """Build Junos commands for interface flow analysis."""
    commands = []
    for name, cmd_template in FLOW_ANALYSIS_COMMANDS.items():
        if "{intf}" in cmd_template:
            commands.append(cmd_template.replace("{intf}", interface))
        elif "{filter}" not in cmd_template:
            commands.append(cmd_template)
    return commands


def parse_interface_counters(output: str) -> FlowAnalysisResult:
    """Parse Junos interface extensive output into flow analysis.
    
    Adapted from mcpcap analyze_traffic_flow + Wireshark-MCP get_protocol_statistics.
    """
    result = FlowAnalysisResult(interface="", direction="bidirectional")
    
    # Input/output bytes
    m = re.search(r'Input\s+bytes\s*:\s*(\d+)', output)
    if m:
        result.total_bytes += int(m.group(1))
    m = re.search(r'Output\s+bytes\s*:\s*(\d+)', output)
    if m:
        result.total_bytes += int(m.group(1))
    
    # Input/output packets
    m = re.search(r'Input\s+packets\s*:\s*(\d+)', output)
    if m:
        result.total_packets += int(m.group(1))
    m = re.search(r'Output\s+packets\s*:\s*(\d+)', output)
    if m:
        result.total_packets += int(m.group(1))
    
    # Input/output rate
    m = re.search(r'Input\s+rate\s*:\s*(\d+)\s*bps', output)
    if m:
        result.rate_bps = int(m.group(1))
    
    # Speed for utilization calculation
    m = re.search(r'Speed:\s*(\d+)(?:Gbps|mbps)', output, re.IGNORECASE)
    if m:
        speed = int(m.group(1))
        if "gbps" in output.lower():
            speed *= 1_000_000_000
        elif "mbps" in output.lower():
            speed *= 1_000_000
        if speed > 0:
            result.utilization_pct = round(100.0 * result.rate_bps / speed, 2)
    
    # Error counters
    error_patterns = {
        "input_errors": r'Input\s+errors\s*:\s*(\d+)',
        "output_errors": r'Output\s+errors\s*:\s*(\d+)',
        "input_drops": r'Input\s+drops\s*:\s*(\d+)',
        "output_drops": r'Output\s+drops\s*:\s*(\d+)',
        "crc_errors": r'CRC/Align\s+errors\s*:\s*(\d+)',
        "fifo_errors": r'FIFO\s+errors\s*:\s*(\d+)',
        "framing_errors": r'Framing\s+errors\s*:\s*(\d+)',
    }
    for name, pattern in error_patterns.items():
        m = re.search(pattern, output, re.IGNORECASE)
        if m:
            result.error_counters[name] = int(m.group(1))
    
    return result


# ══════════════════════════════════════════════════════════════
#  MODULE 5: ALERT & THRESHOLD ENGINE
#  (Adapted from Cisco AI-Network-Troubleshooting-PoC)
#  Grafana webhook → LLM analysis pattern, adapted for Junos
# ══════════════════════════════════════════════════════════════

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class AlertRule:
    """An alert rule — adapted from Cisco Grafana alarm pattern."""
    name: str
    description: str
    protocol: str
    metric: str                    # What to check (neighbor_count, session_state, etc.)
    condition: str                 # Comparison operator (lt, gt, eq, ne, contains)
    threshold: str                 # Value to compare against
    severity: AlertSeverity = AlertSeverity.WARNING
    commands: list = field(default_factory=list)  # Junos commands to gather metric
    auto_investigate: bool = True  # Trigger hypothesis engine on alert


# ── Pre-built Junos Alert Rules ──
# Adapted from Cisco AI PoC Grafana alarm:
#   "if avgNeighbors(30sec) < avgNeighbors(30min) : send Alarm"
# Translated to Junos-native checks

JUNOS_ALERT_RULES = [
    AlertRule(
        name="isis_neighbor_loss",
        description="IS-IS adjacency count dropped",
        protocol="isis",
        metric="adjacency_count",
        condition="lt",
        threshold="previous",
        severity=AlertSeverity.CRITICAL,
        commands=["show isis adjacency | count"],
        auto_investigate=True,
    ),
    AlertRule(
        name="bgp_session_down",
        description="BGP peer in non-Established state",
        protocol="bgp",
        metric="session_state",
        condition="ne",
        threshold="Establ",
        severity=AlertSeverity.CRITICAL,
        commands=["show bgp summary"],
        auto_investigate=True,
    ),
    AlertRule(
        name="ldp_session_loss",
        description="LDP session not Operational",
        protocol="ldp",
        metric="session_state",
        condition="ne",
        threshold="Operational",
        severity=AlertSeverity.ERROR,
        commands=["show ldp session"],
        auto_investigate=True,
    ),
    AlertRule(
        name="ospf_neighbor_not_full",
        description="OSPF neighbor stuck in non-Full state",
        protocol="ospf",
        metric="neighbor_state",
        condition="ne",
        threshold="Full",
        severity=AlertSeverity.CRITICAL,
        commands=["show ospf neighbor"],
        auto_investigate=True,
    ),
    AlertRule(
        name="interface_errors",
        description="Interface error counters incrementing",
        protocol="physical",
        metric="error_count",
        condition="gt",
        threshold="0",
        severity=AlertSeverity.WARNING,
        commands=["show interfaces extensive | match error"],
        auto_investigate=False,
    ),
    AlertRule(
        name="high_cpu",
        description="RE CPU utilization above 80%",
        protocol="system",
        metric="cpu_utilization",
        condition="gt",
        threshold="80",
        severity=AlertSeverity.ERROR,
        commands=["show chassis routing-engine | match \"CPU utilization\""],
        auto_investigate=True,
    ),
    AlertRule(
        name="memory_pressure",
        description="RE memory utilization above 85%",
        protocol="system",
        metric="memory_utilization",
        condition="gt",
        threshold="85",
        severity=AlertSeverity.ERROR,
        commands=["show chassis routing-engine | match \"Memory\""],
        auto_investigate=True,
    ),
    AlertRule(
        name="route_table_change",
        description="Significant routing table size change (±10%)",
        protocol="routing",
        metric="route_count",
        condition="change_pct",
        threshold="10",
        severity=AlertSeverity.WARNING,
        commands=["show route summary | match \"inet.0\""],
        auto_investigate=True,
    ),
    AlertRule(
        name="bfd_session_down",
        description="BFD session went down",
        protocol="bfd",
        metric="session_state",
        condition="ne",
        threshold="Up",
        severity=AlertSeverity.CRITICAL,
        commands=["show bfd session"],
        auto_investigate=True,
    ),
]


@dataclass
class AlertEvent:
    """A triggered alert event."""
    rule_name: str
    severity: AlertSeverity
    device: str
    protocol: str
    message: str
    metric_value: str
    threshold: str
    timestamp: str = ""
    auto_investigate: bool = True
    investigation_result: str = ""


class AlertEngine:
    """Alert engine that monitors Junos metrics and triggers investigations.
    
    Adapted from Cisco AI-Network-Troubleshooting-PoC Grafana webhook pattern.
    Instead of external telemetry (Telegraf→InfluxDB→Grafana), this uses
    direct Junos CLI polling via MCP.
    """
    
    def __init__(self):
        self.rules = {r.name: r for r in JUNOS_ALERT_RULES}
        self.history: list[AlertEvent] = []
        self._previous_metrics: dict = {}  # For trend-based alerts
    
    def check_metric(self, rule_name: str, device: str, current_value: str) -> Optional[AlertEvent]:
        """Check a metric against an alert rule and return AlertEvent if triggered."""
        rule = self.rules.get(rule_name)
        if not rule:
            return None
        
        triggered = False
        
        if rule.condition == "lt":
            try:
                if rule.threshold == "previous":
                    prev = self._previous_metrics.get(f"{device}:{rule_name}", current_value)
                    triggered = float(current_value) < float(prev)
                else:
                    triggered = float(current_value) < float(rule.threshold)
            except ValueError:
                pass
        
        elif rule.condition == "gt":
            try:
                triggered = float(current_value) > float(rule.threshold)
            except ValueError:
                pass
        
        elif rule.condition == "ne":
            triggered = current_value.strip().lower() != rule.threshold.strip().lower()
        
        elif rule.condition == "eq":
            triggered = current_value.strip().lower() == rule.threshold.strip().lower()
        
        elif rule.condition == "contains":
            triggered = rule.threshold.lower() in current_value.lower()
        
        elif rule.condition == "change_pct":
            try:
                prev = float(self._previous_metrics.get(f"{device}:{rule_name}", current_value))
                curr = float(current_value)
                if prev > 0:
                    change_pct = abs(curr - prev) / prev * 100
                    triggered = change_pct > float(rule.threshold)
            except ValueError:
                pass
        
        # Update previous value
        self._previous_metrics[f"{device}:{rule_name}"] = current_value
        
        if triggered:
            event = AlertEvent(
                rule_name=rule_name,
                severity=rule.severity,
                device=device,
                protocol=rule.protocol,
                message=f"{rule.description}: {current_value} (threshold: {rule.threshold})",
                metric_value=current_value,
                threshold=rule.threshold,
                timestamp=datetime.now().isoformat(),
                auto_investigate=rule.auto_investigate,
            )
            self.history.append(event)
            return event
        
        return None
    
    def get_active_alerts(self, since_minutes: int = 60) -> list:
        """Get alerts from the last N minutes."""
        cutoff = datetime.now() - timedelta(minutes=since_minutes)
        return [
            a for a in self.history
            if datetime.fromisoformat(a.timestamp) > cutoff
        ]
    
    def generate_alert_summary(self) -> str:
        """Generate a formatted alert summary."""
        recent = self.get_active_alerts(60)
        if not recent:
            return "● No alerts in the last 60 minutes."
        
        lines = ["# ⊗ Active Alerts", ""]
        severity_icons = {
            AlertSeverity.CRITICAL: "[red]●[/red]",
            AlertSeverity.ERROR: "[#ff8700]●[/#ff8700]",
            AlertSeverity.WARNING: "[yellow]●[/yellow]",
            AlertSeverity.INFO: "[blue]●[/blue]",
        }
        for alert in sorted(recent, key=lambda a: a.severity.value):
            icon = severity_icons.get(alert.severity, "⚪")
            lines.append(f"{icon} **{alert.device}** — {alert.message}")
            lines.append(f"   Protocol: {alert.protocol} | Time: {alert.timestamp}")
            if alert.investigation_result:
                lines.append(f"   Investigation: {alert.investigation_result[:200]}")
            lines.append("")
        
        return "\n".join(lines)


# ══════════════════════════════════════════════════════════════
#  MODULE 6: LOG FORENSICS & TIMELINE
#  (Adapted from Wireshark-MCP forensic_investigation prompt
#   + gNMIBuddy ops.logs + Cisco telemetry correlation)
# ══════════════════════════════════════════════════════════════

@dataclass
class LogEntry:
    """Parsed Junos syslog entry."""
    timestamp: str
    device: str
    facility: str
    severity: str
    process: str
    message: str
    raw_line: str = ""


@dataclass
class ForensicTimeline:
    """Timeline of correlated events — adapted from Wireshark-MCP forensic prompt."""
    events: list = field(default_factory=list)  # list of LogEntry
    time_window: str = ""
    correlation_chains: list = field(default_factory=list)
    root_cause_events: list = field(default_factory=list)


LOG_FORENSIC_COMMANDS = {
    "recent_messages": "show log messages | last 100",
    "recent_errors": "show log messages | match \"error|warning|critical|alert\" | last 50",
    "interface_events": "show log messages | match \"SNMP_TRAP_LINK|IF_DOWN|IF_UP\" | last 50",
    "routing_events": "show log messages | match \"RPD_OSPF|RPD_BGP|RPD_ISIS|RPD_LDP\" | last 50",
    "chassis_events": "show log messages | match \"CHASSISD|ALARM|FPC|PIC\" | last 50",
    "security_events": "show log messages | match \"LOGIN|SSH|SNMP|FIREWALL\" | last 50",
    "commit_history": "show system commit",
    "uptime": "show system uptime",
}


def build_forensic_commands(scope: str = "all", time_window: str = "",
                            keyword: str = "") -> list:
    """Build Junos log forensic commands.
    
    Adapted from gNMIBuddy's ops.logs (filtered device logs with keyword search).
    """
    commands = []
    
    if scope == "all" or scope == "recent":
        commands.append(LOG_FORENSIC_COMMANDS["recent_messages"])
    if scope == "all" or scope == "errors":
        commands.append(LOG_FORENSIC_COMMANDS["recent_errors"])
    if scope == "all" or scope == "interface":
        commands.append(LOG_FORENSIC_COMMANDS["interface_events"])
    if scope == "all" or scope == "routing":
        commands.append(LOG_FORENSIC_COMMANDS["routing_events"])
    if scope == "all" or scope == "chassis":
        commands.append(LOG_FORENSIC_COMMANDS["chassis_events"])
    if scope == "all" or scope == "security":
        commands.append(LOG_FORENSIC_COMMANDS["security_events"])
    if scope == "all" or scope == "commits":
        commands.append(LOG_FORENSIC_COMMANDS["commit_history"])
    
    if keyword:
        commands.append(f'show log messages | match "{keyword}" | last 50')
    
    commands.append(LOG_FORENSIC_COMMANDS["uptime"])
    
    return commands


def parse_syslog_line(line: str, device: str = "") -> Optional[LogEntry]:
    """Parse a single Junos syslog line into structured LogEntry."""
    # Format: "Jun 20 14:23:45 hostname process[pid]: message"
    m = re.match(
        r'(\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2})\s+'  # timestamp
        r'(\S+)\s+'                                  # hostname
        r'(\S+?)(?:\[(\d+)\])?:\s+'                  # process[pid]
        r'(.*)',                                      # message
        line.strip()
    )
    if not m:
        return None
    
    # Determine severity from message content
    msg = m.group(5)
    severity = "info"
    for sev_kw in [("CRIT", "critical"), ("ALERT", "critical"), ("EMERG", "critical"),
                   ("ERR", "error"), ("WARN", "warning"), ("NOTICE", "notice")]:
        if sev_kw[0] in msg.upper():
            severity = sev_kw[1]
            break
    
    # Extract facility from process name
    process = m.group(3)
    facility = "system"
    facility_map = {
        "rpd": "routing", "bgp": "routing", "ospf": "routing", "isis": "routing",
        "chassisd": "chassis", "alarmd": "chassis", "fpc": "chassis",
        "sshd": "security", "login": "security", "mgd": "security",
        "snmpd": "snmp", "mib2d": "snmp",
        "kernel": "kernel", "ifinfo": "interface", "lacpd": "interface",
        "ldpd": "routing", "rsvpd": "routing", "bfdd": "routing",
    }
    for proc_prefix, fac in facility_map.items():
        if process.lower().startswith(proc_prefix):
            facility = fac
            break
    
    return LogEntry(
        timestamp=m.group(1),
        device=device or m.group(2),
        facility=facility,
        severity=severity,
        process=process,
        message=msg,
        raw_line=line.strip(),
    )


def correlate_events(entries: list, window_seconds: int = 300) -> ForensicTimeline:
    """Correlate log events to find causal chains.
    
    Adapted from Wireshark-MCP forensic_investigation prompt:
    "Timeline Reconstruction: Create chronological sequence of events"
    """
    timeline = ForensicTimeline()
    timeline.events = sorted(entries, key=lambda e: e.timestamp)
    
    # Find correlation chains — events that happen within window_seconds of each other
    chains = []
    used = set()
    
    for i, event in enumerate(timeline.events):
        if i in used:
            continue
        chain = [event]
        used.add(i)
        
        for j in range(i + 1, len(timeline.events)):
            if j in used:
                continue
            # Check if events are related (same device/facility or cause-effect)
            if (timeline.events[j].device == event.device and
                timeline.events[j].facility == event.facility):
                chain.append(timeline.events[j])
                used.add(j)
        
        if len(chain) > 1:
            chains.append(chain)
    
    timeline.correlation_chains = chains
    
    # Identify root cause events (earliest critical/error events)
    timeline.root_cause_events = [
        e for e in timeline.events[:10]
        if e.severity in ("critical", "error")
    ]
    
    return timeline


def format_forensic_timeline(timeline: ForensicTimeline) -> str:
    """Format forensic timeline for display."""
    lines = ["# ⊕ Forensic Event Timeline", ""]
    
    if timeline.root_cause_events:
        lines.append("## ◎ Potential Root Cause Events")
        for e in timeline.root_cause_events:
            icon = "[red]●[/red]" if e.severity == "critical" else "[#ff8700]●[/#ff8700]"
            lines.append(f"  {icon} [{e.timestamp}] {e.device}/{e.process}: {e.message}")
        lines.append("")
    
    if timeline.correlation_chains:
        lines.append(f"## ⊶ Correlated Event Chains ({len(timeline.correlation_chains)} found)")
        for i, chain in enumerate(timeline.correlation_chains[:5], 1):
            lines.append(f"### Chain #{i} ({len(chain)} events)")
            for e in chain:
                sev_icon = {"critical": "[red]●[/red]", "error": "[#ff8700]●[/#ff8700]", "warning": "[yellow]●[/yellow]"}.get(e.severity, "⚪")
                lines.append(f"  {sev_icon} [{e.timestamp}] {e.process}: {e.message}")
            lines.append("")
    
    lines.append(f"## ◫ Event Statistics")
    by_severity = defaultdict(int)
    by_facility = defaultdict(int)
    for e in timeline.events:
        by_severity[e.severity] += 1
        by_facility[e.facility] += 1
    
    lines.append(f"  Total events: {len(timeline.events)}")
    for sev, count in sorted(by_severity.items()):
        lines.append(f"  - {sev}: {count}")
    lines.append("")
    for fac, count in sorted(by_facility.items(), key=lambda x: -x[1]):
        lines.append(f"  - {fac}: {count}")
    
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════
#  MODULE 7: DEVICE PROFILER & ANOMALY DETECTION
#  (Adapted from mistral-4-cisco profiler + gNMIBuddy device info)
# ══════════════════════════════════════════════════════════════

@dataclass
class DeviceProfile:
    """Device health profile — adapted from gNMIBuddy NetworkOperationResult
    and mistral-4-cisco YAML summary format."""
    hostname: str
    role: str = ""
    model: str = ""
    junos_version: str = ""
    uptime: str = ""
    cpu_utilization: float = 0.0
    memory_utilization: float = 0.0
    temperature: float = 0.0
    alarm_count: int = 0
    interface_count: int = 0
    interfaces_up: int = 0
    interfaces_down: int = 0
    ospf_neighbors: int = 0
    bgp_peers_established: int = 0
    bgp_peers_total: int = 0
    isis_adjacencies: int = 0
    ldp_sessions: int = 0
    route_count: int = 0
    health_score: float = 100.0
    anomalies: list = field(default_factory=list)
    last_commit: str = ""
    last_reboot: str = ""


DEVICE_PROFILE_COMMANDS = [
    "show chassis hardware | match \"Chassis|Model\"",
    "show version | match \"Junos:|Model:\"",
    "show system uptime | match \"System booted|Current time|uptime\"",
    "show chassis routing-engine | match \"CPU|Memory|Temperature\"",
    "show chassis alarms",
    "show interfaces terse | count",
    "show interfaces terse | match \" up \" | count",
    "show interfaces terse | match \" down \" | count",
    "show ospf neighbor | count",
    "show bgp summary | match \"Establ\" | count",
    "show bgp summary | count",
    "show isis adjacency | count",
    "show ldp session | match \"Operational\" | count",
    "show route summary | match \"inet.0\"",
    "show system commit | match \"^0 \"",
]


def parse_device_profile(outputs: dict, hostname: str) -> DeviceProfile:
    """Parse device profiling command outputs into a DeviceProfile.
    
    Adapted from gNMIBuddy's device.info + mistral-4-cisco YAML output format.
    """
    profile = DeviceProfile(hostname=hostname)
    combined = "\n".join(str(v) for v in outputs.values())
    
    # Parse specific fields
    m = re.search(r'Junos:\s*(\S+)', combined)
    if m:
        profile.junos_version = m.group(1)
    
    m = re.search(r'Model:\s*(\S+)', combined)
    if m:
        profile.model = m.group(1)
    
    m = re.search(r'System booted:\s*(.*)', combined)
    if m:
        profile.last_reboot = m.group(1).strip()
    
    m = re.search(r'CPU utilization.*?(\d+)\s*percent', combined, re.IGNORECASE)
    if m:
        profile.cpu_utilization = float(m.group(1))
    
    m = re.search(r'Memory utilization.*?(\d+)\s*percent', combined, re.IGNORECASE)
    if m:
        profile.memory_utilization = float(m.group(1))
    
    m = re.search(r'Temperature.*?(\d+)\s*degrees', combined, re.IGNORECASE)
    if m:
        profile.temperature = float(m.group(1))
    
    # Count-based parsing
    def extract_count(pattern):
        m = re.search(pattern + r'.*?Count:\s*(\d+)', combined, re.IGNORECASE | re.DOTALL)
        if m:
            return int(m.group(1))
        # Try just the count line directly after
        m = re.search(r'Count:\s*(\d+)\s+lines', combined)
        return 0
    
    # Calculate health score
    score = 100.0
    
    if profile.cpu_utilization > 80:
        score -= 20
        profile.anomalies.append(f"High CPU: {profile.cpu_utilization}%")
    elif profile.cpu_utilization > 60:
        score -= 10
    
    if profile.memory_utilization > 85:
        score -= 20
        profile.anomalies.append(f"High memory: {profile.memory_utilization}%")
    elif profile.memory_utilization > 70:
        score -= 10
    
    if profile.temperature > 65:
        score -= 15
        profile.anomalies.append(f"High temperature: {profile.temperature}°C")
    
    if profile.alarm_count > 0:
        score -= 15 * profile.alarm_count
        profile.anomalies.append(f"{profile.alarm_count} chassis alarms active")
    
    profile.health_score = max(0, score)
    
    # Determine role
    if hostname.upper().startswith("PE"):
        profile.role = "PE"
    elif hostname.upper().startswith("RR"):
        profile.role = "RR"
    elif hostname.upper().startswith("P"):
        profile.role = "P"
    else:
        profile.role = "Unknown"
    
    return profile


def generate_device_comparison(profiles: list) -> str:
    """Generate a comparative device report.
    
    Adapted from mistral-4-cisco's combined analysis:
    "Common Configurations, Deviations, and Potential Vulnerabilities"
    """
    lines = ["# ◫ Device Comparison Report", ""]
    
    # Health score summary
    lines.append("## Health Scores")
    for p in sorted(profiles, key=lambda x: x.health_score):
        bar_len = int(p.health_score / 5)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        icon = "[green]●[/green]" if p.health_score >= 80 else ("[yellow]●[/yellow]" if p.health_score >= 50 else "[red]●[/red]")
        lines.append(f"  {icon} {p.hostname:<10} [{bar}] {p.health_score:.0f}%")
    lines.append("")
    
    # Version consistency
    versions = {p.junos_version for p in profiles if p.junos_version}
    if len(versions) > 1:
        lines.append("## ▲ Version Inconsistency")
        lines.append(f"  Found {len(versions)} different Junos versions: {', '.join(versions)}")
        for p in profiles:
            lines.append(f"  - {p.hostname}: {p.junos_version or 'unknown'}")
        lines.append("")
    
    # Anomalies across devices
    all_anomalies = []
    for p in profiles:
        for a in p.anomalies:
            all_anomalies.append(f"  - {p.hostname}: {a}")
    
    if all_anomalies:
        lines.append("## ⊗ Anomalies Detected")
        for a in all_anomalies:
            lines.append(a)
        lines.append("")
    
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════
#  MODULE 8: COLLABORATIVE ANALYSIS & PERSISTENT MEMORY
#  (Adapted from mistral-4-cisco persistent agent + Cisco Webex reporting)
# ══════════════════════════════════════════════════════════════

class AnalysisMemory:
    """Persistent analysis memory — adapted from mistral-4-cisco's
    agent_id.txt/conversation_id.txt pattern for persistent context.
    
    Stores investigation history in SQLite for cross-session continuity.
    """
    
    def __init__(self, db_path: str = "analysis_memory.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS investigations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    query TEXT NOT NULL,
                    domain TEXT,
                    devices TEXT,
                    findings TEXT,
                    root_cause TEXT,
                    resolution TEXT,
                    confidence REAL DEFAULT 0.0,
                    tags TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS device_baselines (
                    hostname TEXT PRIMARY KEY,
                    profile_json TEXT,
                    last_updated TEXT,
                    baseline_score REAL DEFAULT 100.0
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS alert_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    device TEXT,
                    rule_name TEXT,
                    severity TEXT,
                    message TEXT,
                    resolved INTEGER DEFAULT 0
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to initialize analysis memory DB: {e}")
    
    def record_investigation(self, query: str, domain: str, devices: list,
                              findings: str, root_cause: str = "",
                              resolution: str = "", confidence: float = 0.0,
                              tags: Optional[list] = None):
        """Record a completed investigation for future reference."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute(
                """INSERT INTO investigations 
                   (timestamp, query, domain, devices, findings, root_cause, resolution, confidence, tags)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    datetime.now().isoformat(),
                    query,
                    domain,
                    json.dumps(devices),
                    findings,
                    root_cause,
                    resolution,
                    confidence,
                    json.dumps(tags or []),
                )
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to record investigation: {e}")
    
    def find_similar_investigations(self, query: str, limit: int = 5) -> list:
        """Find past investigations similar to current query.
        
        Adapted from mistral-4-cisco's persistent Agent memory.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            keywords = [w.lower() for w in query.split() if len(w) > 3]
            if not keywords:
                return []
            
            # Simple keyword matching (could be upgraded to vector search)
            conditions = " OR ".join(
                f"LOWER(query) LIKE '%{kw}%' OR LOWER(findings) LIKE '%{kw}%' OR LOWER(root_cause) LIKE '%{kw}%'"
                for kw in keywords[:5]
            )
            
            rows = conn.execute(
                f"""SELECT timestamp, query, domain, findings, root_cause, resolution, confidence
                    FROM investigations
                    WHERE {conditions}
                    ORDER BY timestamp DESC
                    LIMIT ?""",
                (limit,)
            ).fetchall()
            conn.close()
            
            return [
                {
                    "timestamp": r[0],
                    "query": r[1],
                    "domain": r[2],
                    "findings": r[3][:300],
                    "root_cause": r[4],
                    "resolution": r[5],
                    "confidence": r[6],
                }
                for r in rows
            ]
        except Exception as e:
            logger.error(f"Failed to search investigations: {e}")
            return []
    
    def update_device_baseline(self, hostname: str, profile: DeviceProfile):
        """Store device baseline for anomaly detection across sessions."""
        try:
            conn = sqlite3.connect(self.db_path)
            profile_json = json.dumps({
                "hostname": profile.hostname,
                "role": profile.role,
                "model": profile.model,
                "junos_version": profile.junos_version,
                "cpu_utilization": profile.cpu_utilization,
                "memory_utilization": profile.memory_utilization,
                "health_score": profile.health_score,
                "ospf_neighbors": profile.ospf_neighbors,
                "bgp_peers_established": profile.bgp_peers_established,
                "isis_adjacencies": profile.isis_adjacencies,
                "ldp_sessions": profile.ldp_sessions,
                "route_count": profile.route_count,
            })
            conn.execute(
                """INSERT OR REPLACE INTO device_baselines 
                   (hostname, profile_json, last_updated, baseline_score)
                   VALUES (?, ?, ?, ?)""",
                (hostname, profile_json, datetime.now().isoformat(), profile.health_score)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to update device baseline: {e}")
    
    def get_device_baseline(self, hostname: str) -> Optional[dict]:
        """Get previous baseline for a device to detect drift."""
        try:
            conn = sqlite3.connect(self.db_path)
            row = conn.execute(
                "SELECT profile_json, last_updated FROM device_baselines WHERE hostname = ?",
                (hostname,)
            ).fetchone()
            conn.close()
            if row:
                return {"profile": json.loads(row[0]), "last_updated": row[1]}
            return None
        except Exception as e:
            logger.error(f"Failed to get device baseline: {e}")
            return None
    
    def record_alert(self, event: AlertEvent):
        """Record an alert event."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute(
                """INSERT INTO alert_log 
                   (timestamp, device, rule_name, severity, message)
                   VALUES (?, ?, ?, ?, ?)""",
                (event.timestamp, event.device, event.rule_name,
                 event.severity.value, event.message)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to record alert: {e}")
    
    def get_investigation_context(self, query: str) -> str:
        """Get relevant past context for a new investigation.
        
        This is the "persistent memory" feature from mistral-4-cisco,
        where the AI agent retains context across conversations.
        """
        similar = self.find_similar_investigations(query, limit=3)
        if not similar:
            return ""
        
        lines = ["## ⊞ Relevant Past Investigations", ""]
        for s in similar:
            lines.append(f"### [{s['timestamp'][:10]}] {s['query'][:100]}")
            if s['root_cause']:
                lines.append(f"  Root Cause: {s['root_cause']}")
            if s['resolution']:
                lines.append(f"  Resolution: {s['resolution']}")
            lines.append(f"  Confidence: {s['confidence']:.0f}%")
            lines.append("")
        
        return "\n".join(lines)


# ══════════════════════════════════════════════════════════════
#  ANALYSIS PROMPT LIBRARY
#  (Adapted from mcpcap analysis prompts + Wireshark-MCP guided workflows)
# ══════════════════════════════════════════════════════════════

ANALYSIS_PROMPTS = {
    "security_audit": {
        "name": "Security Audit Workflow",
        "description": "Guided Junos security analysis — adapted from Wireshark-MCP security_audit",
        "steps": [
            "1. Collect firewall filter configurations from all routers",
            "2. Check lo0 RE protection filter on every device",
            "3. Verify BGP/OSPF/IS-IS/LDP authentication",
            "4. Check SSH and SNMP security settings",
            "5. Scan for default credentials and weak community strings",
            "6. Review prefix-list and policy protections",
            "7. Check unused interface hardening",
            "8. Verify syslog and NTP configuration",
            "9. Generate security score and remediation report",
        ],
    },
    "network_troubleshooting": {
        "name": "Network Troubleshooting Workflow",
        "description": "Guided Junos troubleshooting — adapted from Wireshark-MCP + Cisco AI PoC",
        "steps": [
            "1. Identify the problem domain (connectivity/protocol/performance)",
            "2. Generate hypotheses ranked by likelihood",
            "3. Collect evidence from affected and adjacent devices",
            "4. Analyze protocol FSM states (OSPF/BGP/IS-IS/LDP)",
            "5. Trace the cascading failure chain from root cause",
            "6. Correlate with recent log events and config changes",
            "7. Check past investigations for similar patterns",
            "8. Generate root cause analysis with remediation steps",
        ],
    },
    "incident_response": {
        "name": "Incident Response Workflow",
        "description": "Network incident investigation — adapted from Wireshark-MCP incident_response",
        "steps": [
            "1. Capture current state: all protocol neighbors, routes, interfaces",
            "2. Review logs for the incident time window",
            "3. Build event correlation timeline",
            "4. Identify configuration changes (show system commit)",
            "5. Compare current state against golden config baselines",
            "6. Analyze traffic flows on affected interfaces",
            "7. Check for security indicators (unauthorized access, anomalies)",
            "8. Generate incident report with timeline and root cause",
        ],
    },
    "capacity_planning": {
        "name": "Capacity Planning Analysis",
        "description": "Traffic and capacity analysis — adapted from mcpcap CapInfos + flow analysis",
        "steps": [
            "1. Collect interface utilization across all links",
            "2. Identify links above 70% utilization",
            "3. Analyze traffic flow patterns and top talkers",
            "4. Check ECMP load balancing effectiveness",
            "5. Review QoS/CoS queue statistics",
            "6. Project growth based on historical trends",
            "7. Identify bottleneck links for capacity upgrades",
            "8. Generate capacity planning recommendations",
        ],
    },
    "dns_forensics": {
        "name": "DNS Forensic Analysis",
        "description": "DNS traffic investigation — adapted from mcpcap DNS + dns-mcp-server",
        "steps": [
            "1. Capture DNS traffic on router interfaces",
            "2. Analyze query patterns and frequency",
            "3. Detect DGA domains and DNS tunneling indicators",
            "4. Verify DNS resolver configuration on all routers",
            "5. Check for NXDOMAIN floods and cache poisoning",
            "6. Correlate DNS anomalies with security events",
            "7. Generate DNS health and security report",
        ],
    },
}


def get_analysis_prompt(prompt_name: str) -> dict:
    """Get a guided analysis workflow prompt."""
    return ANALYSIS_PROMPTS.get(prompt_name, {})


def list_analysis_prompts() -> dict:
    """List all available analysis prompts."""
    return {
        name: {"name": p["name"], "description": p["description"]}
        for name, p in ANALYSIS_PROMPTS.items()
    }


# ══════════════════════════════════════════════════════════════
#  MASTER INTEGRATION — All modules accessible via single interface
# ══════════════════════════════════════════════════════════════

class NetworkAnalysisEngine:
    """Master engine combining all network analysis capabilities.
    
    Integrates:
    - mcpcap packet capture analysis (Junos monitor traffic)
    - Wireshark-MCP security audit & threat detection (Junos firewall)
    - dns-mcp-server DNS intelligence (Junos show host)
    - Cisco AI alert-driven investigation (threshold monitoring)
    - gNMIBuddy device profiling (Junos show commands)
    - mistral-4-cisco persistent memory (SQLite investigation history)
    """
    
    def __init__(self, db_path: str = "analysis_memory.db"):
        self.alert_engine = AlertEngine()
        self.memory = AnalysisMemory(db_path)
        self.device_profiles: dict[str, DeviceProfile] = {}
    
    def get_capture_commands(self, router: str, protocol: str = "all",
                              interface: str = "", count: int = 50) -> str:
        """Get packet capture command for a router."""
        try:
            proto = CaptureProtocol(protocol.lower())
        except ValueError:
            proto = CaptureProtocol.ALL
        
        request = CaptureRequest(
            router=router,
            interface=interface,
            protocol=proto,
            count=count,
        )
        return build_capture_command(request)
    
    def analyze_capture(self, raw_output: str, protocol: str = "all") -> dict:
        """Analyze captured packet output."""
        try:
            proto = CaptureProtocol(protocol.lower())
        except ValueError:
            proto = CaptureProtocol.ALL
        
        result = parse_capture_output(raw_output, proto)
        return {
            "protocol": result.protocol,
            "packets_captured": result.packets_captured,
            "analysis": result.analysis,
            "statistics": result.statistics,
            "anomalies": result.anomalies,
        }
    
    def get_dns_commands(self, domain: str, record_types: Optional[list] = None) -> list:
        """Get DNS resolution commands."""
        return build_dns_commands(domain, record_types)
    
    def get_dns_trace_commands(self, domain: str) -> list:
        """Get DNS trace commands."""
        return build_dns_trace_commands(domain)
    
    def parse_dns(self, output: str, domain: str) -> dict:
        """Parse DNS output."""
        result = parse_dns_output(output, domain)
        return {
            "domain": result.domain,
            "status": result.status,
            "records": result.results,
            "error": result.error,
        }
    
    def get_security_checks(self) -> dict:
        """Get all security check definitions."""
        return {
            name: {
                "title": check["title"],
                "severity": check["severity"].value,
                "commands": check["commands"],
                "description": check["description"],
            }
            for name, check in JUNOS_SECURITY_CHECKS.items()
        }
    
    def run_security_check(self, check_name: str, outputs: dict,
                            device: str = "") -> SecurityFinding:
        """Run a specific security check."""
        finding = analyze_security_output(check_name, outputs)
        finding.device = device
        return finding
    
    def generate_security_report(self, findings: list) -> str:
        """Generate formatted security report."""
        return generate_security_report(findings)
    
    def get_flow_commands(self, interface: str) -> list:
        """Get flow analysis commands."""
        return build_flow_commands(interface)
    
    def analyze_flow(self, output: str) -> FlowAnalysisResult:
        """Analyze interface flow data."""
        return parse_interface_counters(output)
    
    def check_alert(self, rule_name: str, device: str, value: str) -> Optional[AlertEvent]:
        """Check an alert rule."""
        event = self.alert_engine.check_metric(rule_name, device, value)
        if event:
            self.memory.record_alert(event)
        return event
    
    def get_alert_summary(self) -> str:
        """Get active alert summary."""
        return self.alert_engine.generate_alert_summary()
    
    def get_alert_rules(self) -> dict:
        """Get all alert rule definitions."""
        return {
            name: {
                "description": rule.description,
                "protocol": rule.protocol,
                "severity": rule.severity.value,
                "commands": rule.commands,
            }
            for name, rule in self.alert_engine.rules.items()
        }
    
    def get_forensic_commands(self, scope: str = "all", keyword: str = "") -> list:
        """Get log forensic commands."""
        return build_forensic_commands(scope, keyword=keyword)
    
    def analyze_logs(self, output: str, device: str = "") -> ForensicTimeline:
        """Parse and correlate log output."""
        entries = []
        for line in output.split("\n"):
            entry = parse_syslog_line(line.strip(), device)
            if entry:
                entries.append(entry)
        return correlate_events(entries)
    
    def format_forensics(self, timeline: ForensicTimeline) -> str:
        """Format forensic timeline."""
        return format_forensic_timeline(timeline)
    
    def get_profile_commands(self) -> list:
        """Get device profiling commands."""
        return list(DEVICE_PROFILE_COMMANDS)
    
    def build_profile(self, outputs: dict, hostname: str) -> DeviceProfile:
        """Build device profile from command outputs."""
        profile = parse_device_profile(outputs, hostname)
        self.device_profiles[hostname] = profile
        
        # Check for drift from baseline
        baseline = self.memory.get_device_baseline(hostname)
        if baseline:
            prev = baseline["profile"]
            if profile.health_score < prev.get("health_score", 100) - 15:
                profile.anomalies.append(
                    f"Health score dropped: {prev['health_score']:.0f} → {profile.health_score:.0f}"
                )
        
        # Update baseline
        self.memory.update_device_baseline(hostname, profile)
        return profile
    
    def compare_devices(self) -> str:
        """Compare all profiled devices."""
        return generate_device_comparison(list(self.device_profiles.values()))
    
    def get_investigation_context(self, query: str) -> str:
        """Get past investigation context for a query."""
        return self.memory.get_investigation_context(query)
    
    def record_investigation(self, query: str, domain: str, devices: list,
                              findings: str, root_cause: str = "",
                              resolution: str = "", confidence: float = 0.0):
        """Record completed investigation."""
        self.memory.record_investigation(
            query, domain, devices, findings, root_cause, resolution, confidence
        )
    
    def get_workflow(self, name: str) -> dict:
        """Get a guided analysis workflow."""
        return get_analysis_prompt(name)
    
    def list_workflows(self) -> dict:
        """List available analysis workflows."""
        return list_analysis_prompts()
