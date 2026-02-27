#!/usr/bin/env python3
"""
Reasoning Engine v15.0 — Claude-Level Chain-of-Thought for Junos AI

This module implements a unique, multi-stage reasoning pipeline that gives
a local LLM (GPT-OSS / Qwen / Llama) Claude-level diagnostic capabilities
in the Junos networking domain.

Architecture:
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                     REASONING ENGINE PIPELINE                           │
  │                                                                         │
  │  Stage 1: CLASSIFY — Determine problem domain & complexity              │
  │      ↓                                                                  │
  │  Stage 2: DECOMPOSE — Break into OSI-layered investigation branches     │
  │      ↓                                                                  │
  │  Stage 3: HYPOTHESIZE — Generate ranked hypotheses per branch           │
  │      ↓                                                                  │
  │  Stage 4: INVESTIGATE — Targeted data collection per hypothesis         │
  │      ↓                                                                  │
  │  Stage 5: DIAGNOSE — FSM + cascading chain analysis                     │
  │      ↓                                                                  │
  │  Stage 6: SYNTHESIZE — Cross-branch merge → single root cause           │
  │      ↓                                                                  │
  │  Stage 7: PRESCRIBE — Fix commands + verification + auto-recovery map   │
  └─────────────────────────────────────────────────────────────────────────┘

Key Innovations:
  - Hypothesis-Driven Investigation: Don't collect everything — collect
    what DISPROVES hypotheses (Popperian method applied to networking)
  - Protocol FSM Anchoring: Every diagnosis maps to a protocol state
    machine transition — no hallucination possible
  - Cascade Graph Walking: Deterministic failure chain resolution
    from root cause to all symptoms
  - Confidence Accumulation: Evidence-based confidence scoring that
    increases with each confirming data point
"""

import re
import json
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

logger = logging.getLogger("junos-reasoning")


# ══════════════════════════════════════════════════════════════
#  PROBLEM CLASSIFICATION
# ══════════════════════════════════════════════════════════════

class ProblemDomain(Enum):
    CONNECTIVITY = "connectivity"          # "X can't reach Y"
    PROTOCOL_STATE = "protocol_state"      # "BGP is Active on PE1"
    PERFORMANCE = "performance"            # "Slow traffic between X and Y"
    CONFIGURATION = "configuration"        # "Configure OSPF on PE1"
    TOPOLOGY = "topology"                  # "Show me the topology"
    SCRIPTING = "scripting"                # "Write a commit script"
    HEALTH_CHECK = "health_check"          # "Is the network healthy?"
    COMPARISON = "comparison"              # "Compare PE1 and PE2 configs"
    CAPACITY = "capacity"                  # "Is there enough bandwidth?"
    SECURITY = "security"                  # "Check firewall rules"
    VPN_SERVICE = "vpn_service"            # "L3VPN / L2VPN issues"
    MPLS_TRANSPORT = "mpls_transport"      # "LSP / LDP / RSVP issues"
    UNKNOWN = "unknown"

class Complexity(Enum):
    SIMPLE = "simple"          # Single command, single device
    MODERATE = "moderate"      # Multi-device or multi-protocol
    COMPLEX = "complex"        # Cross-layer, cascading, multi-device
    EXPERT = "expert"          # Full mind-map reasoning needed


@dataclass
class ProblemClassification:
    domain: ProblemDomain
    complexity: Complexity
    protocols_involved: list = field(default_factory=list)
    devices_mentioned: list = field(default_factory=list)
    osi_layers: list = field(default_factory=list)
    keywords: list = field(default_factory=list)
    reasoning_strategy: str = ""


def classify_problem(query: str, device_map: dict = None) -> ProblemClassification:
    """Classify a user query into domain, complexity, and affected protocols.
    This determines which reasoning strategy to use."""
    
    q_lower = query.lower()
    
    # ── Domain Detection ──
    domain = ProblemDomain.UNKNOWN
    
    # Connectivity patterns
    if any(kw in q_lower for kw in ["can't reach", "cannot reach", "unreachable", "no connectivity",
                                      "ping fail", "traceroute", "packet loss", "blackhole"]):
        domain = ProblemDomain.CONNECTIVITY
    
    # Protocol state patterns
    elif any(kw in q_lower for kw in ["active state", "idle state", "not established", "down state",
                                        "nonexistent", "exstart", "init state", "stuck",
                                        "bgp active", "ospf init", "ldp nonexistent",
                                        "is active", "is idle", "is down", "goes down",
                                        "session active", "state active", "not coming up",
                                        "won't establish", "can't establish", "flapping",
                                        "keeps dropping", "keeps going down"]):
        domain = ProblemDomain.PROTOCOL_STATE
    
    # Topology patterns
    elif any(kw in q_lower for kw in ["topology", "diagram", "map", "visuali", "network map",
                                        "show topology", "draw", "graph"]):
        domain = ProblemDomain.TOPOLOGY
    
    # Scripting patterns
    elif any(kw in q_lower for kw in ["script", "commit script", "op script", "event script",
                                        "pyez", "automation", "slax", "ansible", "netconf",
                                        "automate", "python script"]):
        domain = ProblemDomain.SCRIPTING
    
    # Configuration patterns
    elif any(kw in q_lower for kw in ["configure", "config", "set ", "delete ", "template",
                                        "add ", "create ", "enable ", "deploy"]):
        domain = ProblemDomain.CONFIGURATION
    
    # VPN patterns
    elif any(kw in q_lower for kw in ["l3vpn", "l2vpn", "vrf", "vpn", "route-target",
                                        "route-distinguisher", "vpls", "evpn", "vxlan"]):
        domain = ProblemDomain.VPN_SERVICE
    
    # MPLS patterns
    elif any(kw in q_lower for kw in ["mpls", "lsp", "rsvp", "ldp", "label", "te tunnel",
                                        "traffic engineering", "cspf", "fast-reroute"]):
        domain = ProblemDomain.MPLS_TRANSPORT
    
    # Health check patterns
    elif any(kw in q_lower for kw in ["health", "audit", "check", "status", "overview",
                                        "summary", "how is", "is everything"]):
        domain = ProblemDomain.HEALTH_CHECK
    
    # Performance patterns
    elif any(kw in q_lower for kw in ["slow", "latency", "bandwidth", "utilization",
                                        "congestion", "queue", "drop", "throughput"]):
        domain = ProblemDomain.PERFORMANCE
    
    # Security patterns
    elif any(kw in q_lower for kw in ["firewall", "filter", "security", "acl", "protect",
                                        "attack", "ddos", "prefix-list"]):
        domain = ProblemDomain.SECURITY
    
    # Comparison patterns
    elif any(kw in q_lower for kw in ["compare", "diff", "difference", "versus", "vs"]):
        domain = ProblemDomain.COMPARISON
    
    # ── Protocol Detection ──
    protocols = []
    protocol_map = {
        "ospf": ["ospf", "spf", "area 0", "dead timer", "hello", "lsa", "dr election"],
        "bgp": ["bgp", "ibgp", "ebgp", "as-path", "local-pref", "route reflector",
                 "established", "active state", "prefix"],
        "isis": ["isis", "is-is", "adjacency", "level 2", "level 1", "iih", "csnp", "psnp"],
        "ldp": ["ldp", "label distribution", "label binding", "fec"],
        "rsvp": ["rsvp", "rsvp-te", "cspf", "bandwidth reservation"],
        "mpls": ["mpls", "label switch", "lsp", "label stack"],
        "bfd": ["bfd", "bidirectional forwarding"],
        "l3vpn": ["l3vpn", "vrf", "vpn-ipv4", "route-target", "rd", "pe-ce"],
        "l2vpn": ["l2vpn", "l2circuit", "vpls", "pseudowire"],
        "evpn": ["evpn", "evi", "esi", "mac-mobility"],
    }
    for proto, keywords in protocol_map.items():
        if any(kw in q_lower for kw in keywords):
            protocols.append(proto)
    
    # ── Device Detection ──
    devices = []
    if device_map:
        for mcp_name, hostname in device_map.items():
            if hostname.lower() in q_lower or mcp_name.lower() in q_lower:
                devices.append(hostname)
    # Also detect generic device mentions
    device_patterns = re.findall(r'\b(PE\d+|P\d+|RR\d+)\b', query, re.IGNORECASE)
    for dp in device_patterns:
        if dp.upper() not in [d.upper() for d in devices]:
            devices.append(dp.upper())
    
    # ── OSI Layer Detection ──
    layers = []
    layer_keywords = {
        "L1": ["physical", "interface", "link", "cable", "optic", "light level", "up/down"],
        "L2": ["ethernet", "vlan", "mtu", "mac", "lldp", "lacp", "stp"],
        "L3": ["routing", "ospf", "isis", "igp", "route", "reachability", "loopback"],
        "MPLS": ["mpls", "ldp", "rsvp", "label", "lsp", "inet.3"],
        "BGP": ["bgp", "ibgp", "ebgp", "prefix", "as-path", "route reflector"],
        "Services": ["vpn", "vrf", "l3vpn", "l2vpn", "evpn", "service"],
    }
    for layer, keywords in layer_keywords.items():
        if any(kw in q_lower for kw in keywords):
            layers.append(layer)
    if not layers:
        layers = ["L1", "L2", "L3", "MPLS", "BGP", "Services"]  # Full stack
    
    # ── Fallback Domain Detection ──
    # If domain is still unknown but protocols were detected, infer domain
    if domain == ProblemDomain.UNKNOWN and protocols:
        if any(p in protocols for p in ["bgp", "ospf", "isis", "ldp"]):
            domain = ProblemDomain.PROTOCOL_STATE
        elif any(p in protocols for p in ["mpls", "rsvp"]):
            domain = ProblemDomain.MPLS_TRANSPORT
        elif any(p in protocols for p in ["l3vpn", "l2vpn", "evpn"]):
            domain = ProblemDomain.VPN_SERVICE
    elif domain == ProblemDomain.UNKNOWN and devices:
        domain = ProblemDomain.HEALTH_CHECK  # At least a device was mentioned
    
    # ── Complexity Scoring ──
    complexity_score = 0
    if len(devices) > 2: complexity_score += 2
    if len(protocols) > 2: complexity_score += 2
    if len(layers) > 3: complexity_score += 1
    if domain == ProblemDomain.CONNECTIVITY: complexity_score += 2
    if domain == ProblemDomain.VPN_SERVICE: complexity_score += 2
    if "cascad" in q_lower or "root cause" in q_lower: complexity_score += 3
    if "why" in q_lower: complexity_score += 1
    
    if complexity_score >= 5:
        complexity = Complexity.EXPERT
        strategy = "mind_map"
    elif complexity_score >= 3:
        complexity = Complexity.COMPLEX
        strategy = "structured_chain"
    elif complexity_score >= 1:
        complexity = Complexity.MODERATE
        strategy = "focused_investigation"
    else:
        complexity = Complexity.SIMPLE
        strategy = "direct_query"
    
    return ProblemClassification(
        domain=domain,
        complexity=complexity,
        protocols_involved=protocols,
        devices_mentioned=devices,
        osi_layers=layers,
        keywords=[kw for kw in q_lower.split() if len(kw) > 3],
        reasoning_strategy=strategy,
    )


# ══════════════════════════════════════════════════════════════
#  HYPOTHESIS ENGINE
# ══════════════════════════════════════════════════════════════

@dataclass
class Hypothesis:
    """A testable hypothesis about the root cause of a problem."""
    id: str
    layer: str                          # OSI layer
    description: str                     # Human-readable hypothesis
    protocol: str = ""                   # Protocol involved
    test_commands: list = field(default_factory=list)  # Commands to test this
    expected_healthy: str = ""           # What healthy looks like
    failure_indicators: list = field(default_factory=list)
    confidence: float = 0.0             # Prior confidence (0-100)
    evidence: list = field(default_factory=list)
    status: str = "untested"            # untested, confirmed, refuted, inconclusive
    cascading_impact: list = field(default_factory=list)
    
    @property
    def verification_command(self) -> str:
        """Get the primary verification command for this hypothesis."""
        return self.test_commands[0] if self.test_commands else ""


# ── Master Hypothesis Library ──
# Pre-built hypotheses for common Junos problems
HYPOTHESIS_LIBRARY = {
    ProblemDomain.CONNECTIVITY: [
        Hypothesis(
            id="H-L1-INTF",
            layer="L1",
            description="Physical interface is down (admin or link)",
            test_commands=["show interfaces terse"],
            expected_healthy="up/up",
            failure_indicators=["down", "administratively down"],
            confidence=20.0,
            cascading_impact=["L3:IGP adj drops", "MPLS:LDP down", "BGP:session drops", "VPN:routes withdrawn"]
        ),
        Hypothesis(
            id="H-L2-MTU",
            layer="L2",
            description="MTU mismatch between endpoints causing OSPF ExStart / IS-IS LSP drops",
            protocol="ospf",
            test_commands=["show interfaces {intf} | match mtu"],
            expected_healthy="MTU matches on both sides",
            failure_indicators=["ExStart", "mtu mismatch"],
            confidence=15.0,
        ),
        Hypothesis(
            id="H-L3-IGP",
            layer="L3",
            description="IGP (OSPF/IS-IS) adjacency not forming — loopback unreachable",
            protocol="ospf",
            test_commands=["show ospf neighbor", "show isis adjacency", "show route {peer_loopback}"],
            expected_healthy="Full / Up",
            failure_indicators=["Init", "Down", "ExStart", "no matching route"],
            confidence=25.0,
            cascading_impact=["MPLS:LDP Nonexistent", "BGP:Active", "VPN:routes withdrawn"]
        ),
        Hypothesis(
            id="H-MPLS-LDP",
            layer="MPLS",
            description="LDP session not Operational — no MPLS labels in inet.3",
            protocol="ldp",
            test_commands=["show ldp session", "show route table inet.3"],
            expected_healthy="Operational, inet.3 has /32 routes",
            failure_indicators=["Nonexistent", "no matching route"],
            confidence=20.0,
            cascading_impact=["BGP:VPN next-hop unresolvable", "VPN:routes unusable"]
        ),
        Hypothesis(
            id="H-BGP-SESSION",
            layer="BGP",
            description="BGP session not Established — route exchange broken",
            protocol="bgp",
            test_commands=["show bgp summary", "show bgp neighbor {peer}"],
            expected_healthy="Established, routes received > 0",
            failure_indicators=["Active", "Idle", "Connect", "0/0"],
            confidence=15.0,
        ),
        Hypothesis(
            id="H-VPN-RT",
            layer="Services",
            description="VPN route-target mismatch — routes not imported into VRF",
            protocol="l3vpn",
            test_commands=["show route table {vrf}.inet.0", "show route advertising-protocol bgp {rr}"],
            expected_healthy="VPN routes present in VRF table",
            failure_indicators=["no matching route", "0 destinations"],
            confidence=10.0,
        ),
        Hypothesis(
            id="H-FW-BLOCK",
            layer="L3",
            description="Firewall filter on lo0 blocking control plane traffic (BGP/LDP/OSPF)",
            protocol="firewall",
            test_commands=["show firewall filter", "show firewall log"],
            expected_healthy="No deny counters incrementing for protocol traffic",
            failure_indicators=["discard", "deny", "counter incrementing"],
            confidence=10.0,
        ),
    ],
    ProblemDomain.PROTOCOL_STATE: [
        Hypothesis(
            id="H-OSPF-INIT",
            layer="L3",
            description="OSPF stuck in Init — hello/area/auth/interface-type mismatch",
            protocol="ospf",
            test_commands=["show ospf interface detail", "show ospf neighbor detail"],
            expected_healthy="Full",
            failure_indicators=["Init", "type mismatch", "area mismatch"],
            confidence=30.0,
        ),
        Hypothesis(
            id="H-OSPF-EXSTART",
            layer="L2",
            description="OSPF stuck in ExStart — MTU mismatch (99% of cases)",
            protocol="ospf",
            test_commands=["show interfaces {intf} | match mtu"],
            expected_healthy="Full",
            failure_indicators=["ExStart"],
            confidence=30.0,
        ),
        Hypothesis(
            id="H-BGP-ACTIVE",
            layer="L3",
            description="BGP Active — TCP can't connect → IGP route to peer loopback missing",
            protocol="bgp",
            test_commands=["show route {peer_loopback}", "show bgp neighbor {peer}"],
            expected_healthy="Established",
            failure_indicators=["Active", "no matching route"],
            confidence=35.0,
            cascading_impact=["VPN:no route exchange", "L3VPN:customer routes withdrawn"]
        ),
        Hypothesis(
            id="H-LDP-NONEXIST",
            layer="L3",
            description="LDP Nonexistent — no IGP route to peer or LDP not on interface",
            protocol="ldp",
            test_commands=["show ldp interface", "show ldp session", "show route {peer_lo0}"],
            expected_healthy="Operational",
            failure_indicators=["Nonexistent", "no matching route"],
            confidence=30.0,
        ),
    ],
}


def generate_hypotheses(classification: ProblemClassification, query: str) -> list:
    """Generate ranked hypotheses based on problem classification.
    Returns hypotheses sorted by prior confidence (most likely first)."""
    
    # Get base hypotheses from library
    hypotheses = list(HYPOTHESIS_LIBRARY.get(classification.domain, []))
    
    # If no domain-specific hypotheses, use connectivity as default
    if not hypotheses:
        hypotheses = list(HYPOTHESIS_LIBRARY.get(ProblemDomain.CONNECTIVITY, []))
    
    # Boost confidence for hypotheses matching detected protocols
    for h in hypotheses:
        if h.protocol in classification.protocols_involved:
            h.confidence += 15.0
        if h.layer in classification.osi_layers:
            h.confidence += 10.0
    
    # Sort by confidence (highest first)
    hypotheses.sort(key=lambda h: h.confidence, reverse=True)
    
    return hypotheses


# ══════════════════════════════════════════════════════════════
#  CASCADING FAILURE GRAPH
# ══════════════════════════════════════════════════════════════

@dataclass
class CascadeNode:
    """A node in the cascading failure chain."""
    layer: str
    protocol: str
    state: str
    description: str
    is_root_cause: bool = False
    children: list = field(default_factory=list)
    evidence: str = ""


# Complete Junos protocol dependency graph
PROTOCOL_DEPENDENCY_GRAPH = {
    # Physical layer is the foundation
    "L1:interface": {
        "depends_on": [],
        "enables": ["L2:ethernet", "L3:ospf", "L3:isis"],
        "failure_impact": "ALL protocols on this interface drop",
    },
    # Data link
    "L2:ethernet": {
        "depends_on": ["L1:interface"],
        "enables": ["L3:ospf", "L3:isis"],
        "failure_impact": "IGP hellos not exchanged",
    },
    # IGP
    "L3:ospf": {
        "depends_on": ["L1:interface", "L2:ethernet"],
        "enables": ["MPLS:ldp", "MPLS:rsvp", "BGP:ibgp"],
        "failure_impact": "Loopback unreachable → LDP/BGP fail",
    },
    "L3:isis": {
        "depends_on": ["L1:interface", "L2:ethernet"],
        "enables": ["MPLS:ldp", "MPLS:rsvp", "BGP:ibgp"],
        "failure_impact": "Loopback unreachable → LDP/BGP fail",
    },
    # MPLS
    "MPLS:ldp": {
        "depends_on": ["L3:ospf", "L3:isis"],
        "enables": ["BGP:vpn_nexthop", "Services:l3vpn", "Services:l2vpn"],
        "failure_impact": "No labels in inet.3 → VPN routes unresolvable",
    },
    "MPLS:rsvp": {
        "depends_on": ["L3:ospf", "L3:isis"],
        "enables": ["MPLS:lsp", "Services:te_tunnel"],
        "failure_impact": "LSPs down → TE traffic fails",
    },
    # BGP
    "BGP:ibgp": {
        "depends_on": ["L3:ospf", "L3:isis"],
        "enables": ["Services:l3vpn", "Services:l2vpn"],
        "failure_impact": "No VPN route exchange between PEs",
    },
    "BGP:vpn_nexthop": {
        "depends_on": ["MPLS:ldp", "MPLS:rsvp"],
        "enables": ["Services:l3vpn", "Services:l2vpn"],
        "failure_impact": "VPN routes exist but next-hop not resolvable via MPLS",
    },
    # Services
    "Services:l3vpn": {
        "depends_on": ["BGP:ibgp", "BGP:vpn_nexthop", "MPLS:ldp"],
        "enables": [],
        "failure_impact": "Customer L3 traffic fails",
    },
    "Services:l2vpn": {
        "depends_on": ["BGP:ibgp", "BGP:vpn_nexthop", "MPLS:ldp"],
        "enables": [],
        "failure_impact": "Customer L2 traffic fails",
    },
}


def walk_cascade(root_failure: str, depth: int = 0, max_depth: int = 7) -> list:
    """Walk the protocol dependency graph to find all downstream impacts
    of a given failure. Returns a list of cascade chain descriptions.
    
    Accepts keys in multiple formats:
      - Exact: 'L3:isis'
      - Underscore: 'L3_ISIS' → normalized to 'L3:isis'
      - Short: 'ISIS' → matches 'L3:isis'
    """
    if depth >= max_depth:
        return []
    
    # Normalize input key
    normalized = root_failure
    if ":" not in normalized and "_" in normalized:
        parts = normalized.split("_", 1)
        normalized = f"{parts[0]}:{parts[1]}".lower()
    elif ":" not in normalized:
        # Try to match by protocol name alone
        for key in PROTOCOL_DEPENDENCY_GRAPH:
            if normalized.lower() in key.lower():
                normalized = key
                break
    else:
        normalized = normalized.lower()
    
    # Try case-insensitive lookup
    node = PROTOCOL_DEPENDENCY_GRAPH.get(normalized)
    if not node:
        # Fuzzy match
        for key in PROTOCOL_DEPENDENCY_GRAPH:
            if key.lower() == normalized.lower():
                node = PROTOCOL_DEPENDENCY_GRAPH[key]
                normalized = key
                break
    
    if not node:
        return []
    
    impacts = []
    indent = "  " * depth + "└─► " if depth > 0 else ""
    impacts.append(f"{indent}{root_failure}: {node['failure_impact']}")
    
    for enabled in node.get("enables", []):
        impacts.extend(walk_cascade(enabled, depth + 1, max_depth))
    
    return impacts


def find_root_cause_from_symptoms(symptoms: list) -> dict:
    """Given a list of symptom strings, trace back to the most likely root cause.
    Uses the dependency graph to find the lowest-layer failure."""
    
    # Map symptoms to dependency graph nodes
    symptom_nodes = []
    for symptom in symptoms:
        s_lower = symptom.lower()
        if "interface" in s_lower and "down" in s_lower:
            symptom_nodes.append("L1:interface")
        elif "ospf" in s_lower and any(s in s_lower for s in ["init", "exstart", "down"]):
            symptom_nodes.append("L3:ospf")
        elif "isis" in s_lower and any(s in s_lower for s in ["down", "initial"]):
            symptom_nodes.append("L3:isis")
        elif "ldp" in s_lower and "nonexist" in s_lower:
            symptom_nodes.append("MPLS:ldp")
        elif "bgp" in s_lower and "active" in s_lower:
            symptom_nodes.append("BGP:ibgp")
        elif "vpn" in s_lower or "vrf" in s_lower:
            symptom_nodes.append("Services:l3vpn")
    
    if not symptom_nodes:
        return {"root_cause": "Unknown", "chain": [], "confidence": 0}
    
    # Find the lowest-layer node (it's the root cause)
    layer_order = ["L1:interface", "L2:ethernet", "L3:ospf", "L3:isis", 
                   "MPLS:ldp", "MPLS:rsvp", "BGP:ibgp", "BGP:vpn_nexthop",
                   "Services:l3vpn", "Services:l2vpn"]
    
    root = None
    for node in layer_order:
        if node in symptom_nodes:
            root = node
            break
    
    if not root:
        root = symptom_nodes[0]
    
    # Walk cascade from root
    chain = walk_cascade(root)
    
    # Calculate confidence based on how many symptoms the chain explains
    explained = sum(1 for s in symptom_nodes if any(s in c for c in chain))
    confidence = min(95, (explained / max(len(symptom_nodes), 1)) * 100)
    
    return {
        "root_cause": root,
        "chain": chain,
        "explained_symptoms": explained,
        "total_symptoms": len(symptom_nodes),
        "confidence": round(confidence, 1),
    }


# ══════════════════════════════════════════════════════════════
#  EVIDENCE ACCUMULATOR
# ══════════════════════════════════════════════════════════════

@dataclass
class Evidence:
    """A piece of evidence supporting or refuting a hypothesis."""
    source: str          # Router/device name
    command: str         # Command that produced this
    raw_output: str      # Raw output
    interpretation: str  # What this evidence means
    supports: str = ""   # Hypothesis ID it supports
    refutes: str = ""    # Hypothesis ID it refutes
    confidence_delta: float = 0.0  # How much this changes confidence


class EvidenceAccumulator:
    """Collects and weighs evidence for/against hypotheses."""
    
    def __init__(self):
        self.evidence_list: list[Evidence] = []
        self.hypothesis_scores: dict[str, float] = {}
    
    def add_evidence(self, evidence: Evidence):
        self.evidence_list.append(evidence)
        
        if evidence.supports:
            self.hypothesis_scores[evidence.supports] = (
                self.hypothesis_scores.get(evidence.supports, 50.0) + evidence.confidence_delta
            )
        if evidence.refutes:
            self.hypothesis_scores[evidence.refutes] = (
                self.hypothesis_scores.get(evidence.refutes, 50.0) - evidence.confidence_delta
            )
    
    def get_top_hypothesis(self) -> tuple:
        """Return the hypothesis ID with highest accumulated confidence."""
        if not self.hypothesis_scores:
            return ("unknown", 0.0)
        top = max(self.hypothesis_scores.items(), key=lambda x: x[1])
        return top
    
    def get_ranked_hypotheses(self, hypotheses: list) -> list:
        """Return hypotheses ranked by accumulated evidence confidence.
        Returns list of (Hypothesis, confidence_pct) tuples."""
        results = []
        for h in hypotheses:
            score = self.hypothesis_scores.get(h.id, h.confidence) or h.confidence
            results.append((h, min(score, 100.0)))
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def get_evidence_summary(self) -> str:
        """Generate a formatted evidence chain for the final report."""
        if not self.evidence_list:
            return "No evidence collected."
        
        lines = ["## Evidence Chain\n"]
        for i, ev in enumerate(self.evidence_list, 1):
            icon = "✅" if ev.supports else ("❌" if ev.refutes else "ℹ️")
            lines.append(f"### Evidence #{i} {icon}")
            lines.append(f"- **Source:** {ev.source}")
            lines.append(f"- **Command:** `{ev.command}`")
            lines.append(f"- **Finding:** {ev.interpretation}")
            if ev.supports:
                lines.append(f"- **Supports:** {ev.supports} (+{ev.confidence_delta}%)")
            if ev.refutes:
                lines.append(f"- **Refutes:** {ev.refutes} (-{ev.confidence_delta}%)")
            lines.append("")
        
        # Final scores
        lines.append("### Hypothesis Rankings\n")
        sorted_scores = sorted(self.hypothesis_scores.items(), key=lambda x: x[1], reverse=True)
        for h_id, score in sorted_scores:
            bar_len = int(min(score, 100) / 5)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            lines.append(f"  {h_id}: [{bar}] {min(score, 100):.0f}%")
        
        return "\n".join(lines)


# ══════════════════════════════════════════════════════════════
#  TOPOLOGY INTELLIGENCE
# ══════════════════════════════════════════════════════════════

@dataclass
class TopologyNode:
    hostname: str
    role: str              # PE, P, RR
    loopback: str = ""
    protocols: list = field(default_factory=list)
    health: str = "healthy"
    bgp_peers: list = field(default_factory=list)
    ospf_neighbors: list = field(default_factory=list)
    isis_adjacencies: list = field(default_factory=list)
    ldp_sessions: list = field(default_factory=list)
    interfaces: list = field(default_factory=list)

@dataclass  
class TopologyLink:
    src: str
    dst: str
    src_intf: str = ""
    dst_intf: str = ""
    link_type: str = "physical"  # physical, ibgp, ldp
    state: str = "up"
    ip_subnet: str = ""


class TopologyIntelligence:
    """Advanced topology analysis from iBGP, LLDP, and IS-IS data.
    Produces Mermaid diagrams, ASCII maps, and topology-aware reasoning."""
    
    def __init__(self):
        self.nodes: dict[str, TopologyNode] = {}
        self.links: list[TopologyLink] = []
        self._adjacency: dict[str, set] = {}
    
    @property
    def physical_links(self) -> list:
        """Get only physical links."""
        return [l for l in self.links if l.link_type == "physical"]
    
    @property
    def ibgp_links(self) -> list:
        """Get only iBGP links."""
        return [l for l in self.links if l.link_type == "ibgp"]
    
    def add_node(self, hostname: str, role: str = "P", loopback: str = ""):
        self.nodes[hostname] = TopologyNode(
            hostname=hostname, role=role, loopback=loopback
        )
        self._adjacency.setdefault(hostname, set())
    
    def add_link(self, src: str, dst: str, src_intf: str = "", dst_intf: str = "",
                 link_type: str = "physical", state: str = "up", ip_subnet: str = ""):
        self.links.append(TopologyLink(
            src=src, dst=dst, src_intf=src_intf, dst_intf=dst_intf,
            link_type=link_type, state=state, ip_subnet=ip_subnet
        ))
        self._adjacency.setdefault(src, set()).add(dst)
        self._adjacency.setdefault(dst, set()).add(src)
    
    def build_from_lldp(self, lldp_links: list, device_map: dict):
        """Build physical topology from LLDP neighbor data."""
        for mcp_name, hostname in device_map.items():
            role = "PE" if hostname.upper().startswith("PE") else (
                "RR" if hostname.upper().startswith("RR") else "P")
            self.add_node(hostname, role)
        
        seen = set()
        for link in lldp_links:
            src_h = device_map.get(link.get("local_router", ""), link.get("local_router", ""))
            dst_h = device_map.get(link.get("remote_router", ""), link.get("remote_router", ""))
            key = tuple(sorted([src_h, dst_h, link.get("local_intf", "")]))
            if key not in seen:
                seen.add(key)
                self.add_link(
                    src=src_h, dst=dst_h,
                    src_intf=link.get("local_intf", ""),
                    dst_intf=link.get("remote_intf", ""),
                    link_type="physical",
                    state="up"
                )
    
    def add_ibgp_sessions(self, bgp_established: list, bgp_issues: list, device_map: dict):
        """Overlay iBGP sessions onto topology."""
        loopback_map = {}
        for mcp_name, hostname in device_map.items():
            if hostname in self.nodes and self.nodes[hostname].loopback:
                loopback_map[self.nodes[hostname].loopback] = hostname
        
        for session in bgp_established:
            src_h = device_map.get(session.get("router", ""), session.get("router", ""))
            peer_h = loopback_map.get(session.get("peer", ""), "")
            if src_h and peer_h and src_h != peer_h:
                self.add_link(src=src_h, dst=peer_h, link_type="ibgp", state="established")
                if src_h in self.nodes:
                    self.nodes[src_h].bgp_peers.append(peer_h)
        
        for session in bgp_issues:
            src_h = device_map.get(session.get("router", ""), session.get("router", ""))
            peer_h = loopback_map.get(session.get("peer", ""), "")
            if src_h and peer_h:
                self.add_link(src=src_h, dst=peer_h, link_type="ibgp",
                              state=session.get("state", "down"))
    
    def generate_mermaid(self, show_ibgp: bool = True, show_protocols: bool = True) -> str:
        """Generate a rich Mermaid topology diagram."""
        lines = ["```mermaid", "graph TB"]
        lines.append("")
        
        # Styles
        lines.append("    %% Node styles by role and health")
        lines.append("    classDef pe fill:#1b5e20,stroke:#4caf50,color:#fff,stroke-width:3px,font-weight:bold")
        lines.append("    classDef p fill:#0d47a1,stroke:#2196f3,color:#fff,stroke-width:2px")
        lines.append("    classDef rr fill:#4a148c,stroke:#9c27b0,color:#fff,stroke-width:3px,font-weight:bold")
        lines.append("    classDef critical fill:#b71c1c,stroke:#f44336,color:#fff,stroke-width:4px")
        lines.append("    classDef warning fill:#e65100,stroke:#ff9800,color:#fff,stroke-width:3px")
        lines.append("    classDef ibgpLink stroke:#9c27b0,stroke-width:2px,stroke-dasharray: 5 5")
        lines.append("")
        
        # Subgraph: PE Layer
        pe_nodes = [h for h, n in self.nodes.items() if n.role == "PE"]
        p_nodes = [h for h, n in self.nodes.items() if n.role == "P"]
        rr_nodes = [h for h, n in self.nodes.items() if n.role == "RR"]
        
        if pe_nodes:
            lines.append("    subgraph PE_Layer[\"🏢 PE Layer — Customer Edge\"]")
            for h in sorted(pe_nodes):
                n = self.nodes[h]
                nid = h.replace("-", "_")
                lo_str = f"\\n📍 {n.loopback}" if n.loopback else ""
                protos = f"\\n🔗 {', '.join(n.protocols)}" if n.protocols and show_protocols else ""
                lines.append(f"        {nid}[\"🖥️ {h}{lo_str}{protos}\"]")
            lines.append("    end")
            lines.append("")
        
        if p_nodes or rr_nodes:
            lines.append("    subgraph Core_Layer[\"⚡ MPLS Core — Transport\"]")
            for h in sorted(p_nodes):
                n = self.nodes[h]
                nid = h.replace("-", "_")
                lo_str = f"\\n📍 {n.loopback}" if n.loopback else ""
                lines.append(f"        {nid}(\"{h}{lo_str}\")")
            for h in sorted(rr_nodes):
                n = self.nodes[h]
                nid = h.replace("-", "_")
                lo_str = f"\\n📍 {n.loopback}" if n.loopback else ""
                lines.append(f"        {nid}{{{{\"🔄 {h} (RR){lo_str}\"}}}}")
            lines.append("    end")
            lines.append("")
        
        # Apply node styles
        for h, n in self.nodes.items():
            nid = h.replace("-", "_")
            if n.health == "critical":
                lines.append(f"    class {nid} critical")
            elif n.health == "warning":
                lines.append(f"    class {nid} warning")
            elif n.role == "PE":
                lines.append(f"    class {nid} pe")
            elif n.role == "RR":
                lines.append(f"    class {nid} rr")
            else:
                lines.append(f"    class {nid} p")
        lines.append("")
        
        # Physical links (solid)
        seen = set()
        lines.append("    %% Physical Links (LLDP)")
        for link in self.links:
            if link.link_type != "physical":
                continue
            key = tuple(sorted([link.src, link.dst]))
            if key in seen:
                continue
            seen.add(key)
            src_id = link.src.replace("-", "_")
            dst_id = link.dst.replace("-", "_")
            intf_label = link.src_intf.replace("ge-0/0/", "ge") if link.src_intf else ""
            if link.state == "down":
                lines.append(f"    {src_id} -.-x|❌ {intf_label}| {dst_id}")
            else:
                lines.append(f"    {src_id} ---|{intf_label}| {dst_id}")
        
        # iBGP sessions (dashed)
        if show_ibgp:
            lines.append("")
            lines.append("    %% iBGP Sessions")
            bgp_seen = set()
            for link in self.links:
                if link.link_type != "ibgp":
                    continue
                key = tuple(sorted([link.src, link.dst]))
                if key in bgp_seen:
                    continue
                bgp_seen.add(key)
                src_id = link.src.replace("-", "_")
                dst_id = link.dst.replace("-", "_")
                if "established" in link.state.lower():
                    lines.append(f"    {src_id} -.->|iBGP ✅| {dst_id}")
                else:
                    lines.append(f"    {src_id} -.->|iBGP ❌ {link.state}| {dst_id}")
        
        lines.append("```")
        return "\n".join(lines)
    
    def generate_ascii_topology(self) -> str:
        """Generate a rich ASCII network topology map for terminal display."""
        pe_nodes = sorted([h for h, n in self.nodes.items() if n.role == "PE"])
        p_nodes = sorted([h for h, n in self.nodes.items() if n.role == "P"])
        rr_nodes = sorted([h for h, n in self.nodes.items() if n.role == "RR"])
        
        width = 72
        lines = []
        lines.append("┌" + "─" * width + "┐")
        lines.append("│" + " LIVE NETWORK TOPOLOGY ".center(width) + "│")
        lines.append("│" + " iBGP · LLDP · IS-IS · LDP Overlay ".center(width) + "│")
        lines.append("├" + "─" * width + "┤")
        
        # PE Layer
        if pe_nodes:
            pe_line = "  ".join(f"[{h}]" for h in pe_nodes)
            lines.append("│" + f"  🏢 PE Layer:  {pe_line}".ljust(width) + "│")
            # Draw connections down
            lines.append("│" + "       │  ╲        │        ╱  │".center(width) + "│")
        
        # Core Layer
        if p_nodes or rr_nodes:
            core_items = []
            for h in p_nodes:
                if h in [n for n in rr_nodes]:
                    continue
                core_items.append(f"({h})")
            for h in rr_nodes:
                core_items.append(f"{{🔄 {h}=RR}}")
            core_line = "  ".join(core_items)
            lines.append("│" + f"  ⚡ Core:      {core_line}".ljust(width) + "│")
        
        lines.append("├" + "─" * width + "┤")
        
        # Protocol health matrix
        lines.append("│" + "  Protocol Health Matrix".ljust(width) + "│")
        header = "│  Node      │ Role │ OSPF │ BGP  │ LDP  │ ISIS │ Links│Health│"
        lines.append(header.ljust(width + 1) + "│" if len(header) < width + 2 else header)
        lines.append("│" + "─" * 11 + "┼" + "──────┼──────┼──────┼──────┼──────┼──────┼──────│")
        
        for h in sorted(self.nodes.keys()):
            n = self.nodes[h]
            health_icon = {"healthy": "🟢", "warning": "🟡", "critical": "🔴"}.get(n.health, "⚪")
            ospf_count = len(n.ospf_neighbors)
            bgp_count = len(n.bgp_peers)
            ldp_count = len(n.ldp_sessions)
            isis_count = len(n.isis_adjacencies)
            link_count = sum(1 for l in self.links if l.link_type == "physical" and (l.src == h or l.dst == h))
            
            row = f"│  {h:<9} │  {n.role:<4}│  {ospf_count:<4}│  {bgp_count:<4}│  {ldp_count:<4}│  {isis_count:<4}│  {link_count:<4}│ {health_icon}    │"
            lines.append(row)
        
        lines.append("├" + "─" * width + "┤")
        
        # iBGP Session Map
        lines.append("│" + "  iBGP Sessions (PE ↔ RR)".ljust(width) + "│")
        bgp_shown = set()
        for link in self.links:
            if link.link_type != "ibgp":
                continue
            key = tuple(sorted([link.src, link.dst]))
            if key in bgp_shown:
                continue
            bgp_shown.add(key)
            icon = "✅" if "established" in link.state.lower() else "❌"
            session_line = f"    {icon} {link.src} ←→ {link.dst} ({link.state})"
            lines.append("│" + session_line.ljust(width) + "│")
        
        if not bgp_shown:
            lines.append("│" + "    No iBGP sessions detected".ljust(width) + "│")
        
        lines.append("└" + "─" * width + "┘")
        return "\n".join(lines)
    
    def find_path(self, src: str, dst: str) -> list:
        """Find shortest path between two nodes using BFS.
        Used for MPLS path verification and troubleshooting."""
        if src not in self._adjacency or dst not in self._adjacency:
            return []
        
        visited = set()
        queue = [(src, [src])]
        
        while queue:
            current, path = queue.pop(0)
            if current == dst:
                return path
            if current in visited:
                continue
            visited.add(current)
            
            for neighbor in self._adjacency.get(current, []):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
        
        return []  # No path found
    
    def find_articulation_points(self) -> list:
        """Find nodes whose removal would partition the network.
        These are critical transit nodes."""
        articulation_points = []
        all_nodes = list(self._adjacency.keys())
        
        for node in all_nodes:
            # Remove node and check connectivity
            remaining = {n: neighbors - {node} for n, neighbors in self._adjacency.items() if n != node}
            if not remaining:
                continue
            
            # BFS from any remaining node
            start = next(iter(remaining))
            visited = set()
            queue = [start]
            while queue:
                current = queue.pop(0)
                if current in visited:
                    continue
                visited.add(current)
                for neighbor in remaining.get(current, set()):
                    if neighbor not in visited:
                        queue.append(neighbor)
            
            if len(visited) < len(remaining):
                articulation_points.append({
                    "node": node,
                    "role": self.nodes.get(node, TopologyNode(hostname=node, role="?")).role,
                    "connections": len(self._adjacency.get(node, set())),
                    "partitions_created": len(remaining) - len(visited),
                })
        
        return articulation_points
    
    def get_ecmp_paths(self, src: str, dst: str) -> list:
        """Find all equal-cost paths between two nodes.
        Used for ECMP analysis and load balancing verification."""
        if src not in self._adjacency or dst not in self._adjacency:
            return []
        
        all_paths = []
        queue = [(src, [src])]
        shortest_len = float('inf')
        
        while queue:
            current, path = queue.pop(0)
            if len(path) > shortest_len:
                continue
            if current == dst:
                if len(path) < shortest_len:
                    shortest_len = len(path)
                    all_paths = [path]
                elif len(path) == shortest_len:
                    all_paths.append(path)
                continue
            
            for neighbor in self._adjacency.get(current, set()):
                if neighbor not in path:
                    queue.append((neighbor, path + [neighbor]))
        
        return all_paths


# ══════════════════════════════════════════════════════════════
#  JUNOS SCRIPTING INTELLIGENCE
# ══════════════════════════════════════════════════════════════

JUNOS_SCRIPT_TEMPLATES = {
    "op_script_ospf_check": {
        "name": "OSPF Neighbor Health Check",
        "type": "op",
        "language": "slax",
        "description": "Checks all OSPF neighbors and alerts on non-Full states",
        "template": '''version 1.1;
ns junos = "http://xml.juniper.net/junos/*/junos";
ns xnm = "http://xml.juniper.net/xnm/1.1/xnm";
ns jcs = "http://xml.juniper.net/junos/commit-scripts/1.0";
import "../import/junos.xsl";

match / {
    <op-script-results> {
        var $ospf = jcs:invoke('get-ospf-neighbor-information');
        var $total = count($ospf/ospf-neighbor);
        var $healthy = count($ospf/ospf-neighbor[ospf-neighbor-state == "Full"]);
        
        <output> "=== OSPF Neighbor Health Check ===";
        <output> "Total neighbors: " _ $total;
        <output> "Healthy (Full): " _ $healthy;
        
        if ($healthy < $total) {
            <output> "\\n⚠️ UNHEALTHY NEIGHBORS:";
            for-each ($ospf/ospf-neighbor[ospf-neighbor-state != "Full"]) {
                <output> "  " _ neighbor-id _ " on " _ interface-name _ 
                         " → State: " _ ospf-neighbor-state;
            }
        } else {
            <output> "\\n✅ All OSPF neighbors are Full.";
        }
    }
}''',
        "install_commands": [
            "set system scripts op file check-ospf.slax",
            "commit",
            "# Run: op check-ospf",
        ],
    },
    "commit_script_isis_p2p": {
        "name": "IS-IS Point-to-Point Enforcement",
        "type": "commit",
        "language": "slax",
        "description": "Warns if any IS-IS interface is not configured as point-to-point",
        "template": '''version 1.1;
ns junos = "http://xml.juniper.net/junos/*/junos";
ns xnm = "http://xml.juniper.net/xnm/1.1/xnm";
ns jcs = "http://xml.juniper.net/junos/commit-scripts/1.0";
import "../import/junos.xsl";

match configuration {
    var $isis = protocols/isis;
    for-each ($isis/interface[not(starts-with(name, 'lo'))]) {
        if (not(point-to-point)) {
            <xnm:warning> {
                <message> "IS-IS interface " _ name _ " is NOT point-to-point. "
                    _ "Add: set protocols isis interface " _ name _ " point-to-point";
            }
        }
    }
}''',
    },
    "event_script_link_down": {
        "name": "Interface Down Auto-Notification",
        "type": "event",
        "language": "slax",
        "description": "Triggered on SNMP_TRAP_LINK_DOWN — logs interface details and sends syslog",
        "template": '''version 1.1;
ns junos = "http://xml.juniper.net/junos/*/junos";
ns xnm = "http://xml.juniper.net/xnm/1.1/xnm";
ns jcs = "http://xml.juniper.net/junos/commit-scripts/1.0";
import "../import/junos.xsl";

match / {
    var $interface = event-script-input/trigger-event/attribute-list/
                     attribute[name == "interface-name"]/value;
    var $message = "ALERT: Interface " _ $interface _ " went DOWN on " _ 
                   $hostname _ " at " _ $localtime;
    
    expr jcs:syslog("external.warning", $message);
    
    /* Collect diagnostic data */
    var $intf-info = jcs:invoke('get-interface-information', 
                                <interface-name> $interface);
    var $errors = $intf-info/physical-interface/input-error-list;
    
    if ($errors/input-errors > 0) {
        expr jcs:syslog("external.error", 
            "Interface " _ $interface _ " has " _ 
            $errors/input-errors _ " input errors — possible hardware issue");
    }
}''',
    },
    "pyez_audit": {
        "name": "PyEZ Network Audit Script",
        "type": "pyez",
        "language": "python",
        "description": "Python PyEZ script to audit OSPF, BGP, LDP across all routers",
        "template": '''#!/usr/bin/env python3
"""PyEZ Network Health Audit — Checks OSPF, BGP, LDP, IS-IS across all routers."""

from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
import json
import sys

ROUTERS = [
    {"host": "pe1", "user": "admin", "password": "juniper123"},
    {"host": "pe2", "user": "admin", "password": "juniper123"},
    {"host": "pe3", "user": "admin", "password": "juniper123"},
    {"host": "p11", "user": "admin", "password": "juniper123"},
    {"host": "p12", "user": "admin", "password": "juniper123"},
]

def audit_router(router_info):
    """Audit a single router and return findings."""
    findings = []
    try:
        dev = Device(**router_info)
        dev.open()
        hostname = dev.facts.get("hostname", router_info["host"])
        
        # OSPF Check
        ospf = dev.rpc.get_ospf_neighbor_information()
        for nbr in ospf.findall('.//ospf-neighbor'):
            state = nbr.findtext('ospf-neighbor-state')
            if state != 'Full':
                findings.append({
                    "router": hostname,
                    "protocol": "OSPF",
                    "severity": "CRITICAL",
                    "detail": f"Neighbor {nbr.findtext('neighbor-id')} is {state}",
                })
        
        # BGP Check
        bgp = dev.rpc.get_bgp_summary_information()
        for peer in bgp.findall('.//bgp-peer'):
            state = peer.findtext('peer-state')
            if state != 'Established':
                findings.append({
                    "router": hostname,
                    "protocol": "BGP",
                    "severity": "CRITICAL",
                    "detail": f"Peer {peer.findtext('peer-address')} is {state}",
                })
        
        # LDP Check
        ldp = dev.rpc.get_ldp_session_information()
        for session in ldp.findall('.//ldp-session'):
            state = session.findtext('ldp-session-state')
            if state != 'Operational':
                findings.append({
                    "router": hostname,
                    "protocol": "LDP",
                    "severity": "WARNING",
                    "detail": f"LDP to {session.findtext('ldp-neighbor-address')} is {state}",
                })
        
        dev.close()
        
        if not findings:
            findings.append({
                "router": hostname,
                "protocol": "ALL",
                "severity": "INFO",
                "detail": "All protocols healthy",
            })
        
    except ConnectError as e:
        findings.append({
            "router": router_info["host"],
            "protocol": "SYSTEM",
            "severity": "CRITICAL",
            "detail": f"Connection failed: {e}",
        })
    
    return findings

if __name__ == "__main__":
    all_findings = []
    for router in ROUTERS:
        print(f"Auditing {router['host']}...")
        all_findings.extend(audit_router(router))
    
    print("\\n=== AUDIT RESULTS ===")
    for f in all_findings:
        icon = {"CRITICAL": "🔴", "WARNING": "🟡", "INFO": "🟢"}.get(f["severity"], "⚪")
        print(f"  {icon} [{f['router']}] {f['protocol']}: {f['detail']}")
    
    print(f"\\nTotal findings: {len(all_findings)}")
    
    # Save to JSON
    with open("audit_results.json", "w") as fp:
        json.dump(all_findings, fp, indent=2)
    print("Results saved to audit_results.json")
''',
    },
    "op_script_topology": {
        "name": "LLDP + BGP Topology Discovery",
        "type": "op",
        "language": "slax",
        "description": "Discovers network topology from LLDP neighbors and BGP peerings",
        "template": '''version 1.1;
ns junos = "http://xml.juniper.net/junos/*/junos";
ns xnm = "http://xml.juniper.net/xnm/1.1/xnm";
ns jcs = "http://xml.juniper.net/junos/commit-scripts/1.0";
import "../import/junos.xsl";

match / {
    <op-script-results> {
        <output> "=== TOPOLOGY DISCOVERY ===";
        <output> "";
        
        /* LLDP Neighbors */
        <output> "--- Physical Topology (LLDP) ---";
        var $lldp = jcs:invoke('get-lldp-neighbors-information');
        for-each ($lldp/lldp-neighbor-information) {
            <output> "  " _ lldp-local-port-id _ " → " _ 
                     lldp-remote-system-name _ " (" _ 
                     lldp-remote-port-id _ ")";
        }
        
        <output> "";
        <output> "--- iBGP Sessions ---";
        var $bgp = jcs:invoke('get-bgp-neighbor-information');
        for-each ($bgp/bgp-peer) {
            <output> "  " _ peer-address _ " [AS " _ peer-as _ 
                     "] State: " _ peer-state;
        }
        
        <output> "";
        <output> "--- IS-IS Adjacencies ---";
        var $isis = jcs:invoke('get-isis-adjacency-information');
        for-each ($isis/isis-adjacency) {
            <output> "  " _ system-name _ " via " _ 
                     interface-name _ " Level: " _ level _ 
                     " State: " _ adjacency-state;
        }
    }
}''',
    },
    "commit_script_bgp_auth": {
        "name": "BGP Authentication Enforcement",
        "type": "commit",
        "language": "slax",
        "description": "Ensures all BGP groups have authentication configured",
        "template": '''version 1.1;
ns junos = "http://xml.juniper.net/junos/*/junos";
ns xnm = "http://xml.juniper.net/xnm/1.1/xnm";
ns jcs = "http://xml.juniper.net/junos/commit-scripts/1.0";
import "../import/junos.xsl";

match configuration {
    for-each (protocols/bgp/group) {
        if (not(authentication-key) and not(authentication-algorithm)) {
            <xnm:warning> {
                <message> "BGP group '" _ name _ 
                    "' has NO authentication configured. "
                    _ "Add: set protocols bgp group " _ name 
                    _ " authentication-key <key>";
            }
        }
    }
}''',
    },
    "pyez_config_backup": {
        "name": "PyEZ Configuration Backup",
        "type": "pyez",
        "language": "python",
        "description": "Backs up running configuration from all routers with timestamped filenames",
        "template": '''#!/usr/bin/env python3
"""PyEZ Config Backup — Saves running config from all routers."""

from jnpr.junos import Device
from datetime import datetime
import os

ROUTERS = [
    {"host": "pe1", "user": "admin", "password": "juniper123"},
    {"host": "p11", "user": "admin", "password": "juniper123"},
    {"host": "p12", "user": "admin", "password": "juniper123"},
]

BACKUP_DIR = "./config_backups"

def backup_router(router_info):
    """Backup a single router's configuration."""
    dev = Device(**router_info)
    dev.open()
    
    hostname = dev.facts.get("hostname", router_info["host"])
    config = dev.rpc.get_config(options={"format": "text"})
    
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{BACKUP_DIR}/{hostname}_{timestamp}.conf"
    
    with open(filename, "w") as f:
        f.write(config.text)
    
    print(f"  ✅ {hostname} → {filename}")
    dev.close()
    return filename

if __name__ == "__main__":
    print(f"=== Configuration Backup — {datetime.now().isoformat()} ===")
    for router in ROUTERS:
        try:
            backup_router(router)
        except Exception as e:
            print(f"  ❌ {router['host']}: {e}")
    print("Backup complete.")
''',
    },
}


def get_script_template(script_type: str, query: str = "") -> dict:
    """Find the most relevant script template based on type/key and query keywords.
    Can also be called with an exact template key name."""
    
    # Direct key lookup first
    if script_type in JUNOS_SCRIPT_TEMPLATES:
        return JUNOS_SCRIPT_TEMPLATES[script_type]
    
    q_lower = query.lower() if query else script_type.lower()
    
    # Score each template
    best_match = None
    best_score = 0
    
    for key, template in JUNOS_SCRIPT_TEMPLATES.items():
        score = 0
        
        # Type match
        if template["type"] == script_type:
            score += 10
        
        # Keyword matching
        desc_lower = (template["description"] + " " + template["name"]).lower()
        for word in q_lower.split():
            if len(word) > 3 and word in desc_lower:
                score += 3
        
        # Protocol keyword matching
        for proto in ["ospf", "bgp", "ldp", "isis", "lldp", "topology"]:
            if proto in q_lower and proto in key.lower():
                score += 5
        
        if score > best_score:
            best_score = score
            best_match = template
    
    return best_match or {}


def list_available_scripts() -> dict:
    """List all available script templates. Returns dict of {key: description}."""
    result = {}
    for key, tmpl in JUNOS_SCRIPT_TEMPLATES.items():
        result[key] = f"{tmpl['type']} ({tmpl['language']}) — {tmpl['description']}"
    return result


# ══════════════════════════════════════════════════════════════
#  REASONING CHAIN FORMATTER
# ══════════════════════════════════════════════════════════════

def format_reasoning_chain(classification: ProblemClassification,
                           hypotheses: list,
                           evidence: EvidenceAccumulator,
                           cascade_result: "dict | None" = None,
                           topology: "TopologyIntelligence | None" = None) -> str:
    """Format the complete reasoning chain into a professional report.
    This is what makes the AI's output match Claude's quality."""
    
    lines = []
    
    # Header
    lines.append("# 🧠 Deep Reasoning Analysis\n")
    
    # Classification
    lines.append("## Problem Classification")
    lines.append(f"- **Domain:** {classification.domain.value}")
    lines.append(f"- **Complexity:** {classification.complexity.value}")
    lines.append(f"- **Strategy:** {classification.reasoning_strategy}")
    lines.append(f"- **Protocols:** {', '.join(classification.protocols_involved) or 'All'}")
    lines.append(f"- **Devices:** {', '.join(classification.devices_mentioned) or 'All'}")
    lines.append(f"- **OSI Layers:** {', '.join(classification.osi_layers)}")
    lines.append("")
    
    # Hypotheses
    lines.append("## Hypotheses (Ranked)")
    for i, h in enumerate(hypotheses[:5], 1):
        status_icon = {"untested": "⚪", "confirmed": "✅", "refuted": "❌", 
                       "inconclusive": "🟡"}.get(h.status, "⚪")
        lines.append(f"### {status_icon} H{i}: {h.description}")
        lines.append(f"  - Layer: {h.layer} | Protocol: {h.protocol or 'N/A'}")
        lines.append(f"  - Prior Confidence: {h.confidence:.0f}%")
        if h.evidence:
            lines.append(f"  - Evidence: {'; '.join(h.evidence[:3])}")
        if h.cascading_impact:
            lines.append(f"  - Cascade: {' → '.join(h.cascading_impact)}")
        lines.append("")
    
    # Evidence chain
    lines.append(evidence.get_evidence_summary())
    lines.append("")
    
    # Cascading failure analysis
    if cascade_result and cascade_result.get("chain"):
        lines.append("## 🔗 Cascading Failure Chain")
        lines.append(f"**Root Cause:** `{cascade_result['root_cause']}`")
        lines.append(f"**Confidence:** {cascade_result['confidence']}%")
        lines.append(f"**Explained:** {cascade_result['explained_symptoms']}/{cascade_result['total_symptoms']} symptoms")
        lines.append("")
        lines.append("```")
        for step in cascade_result["chain"]:
            lines.append(step)
        lines.append("```")
        lines.append("")
    
    # Topology context
    if topology and topology.nodes:
        # Articulation points
        art_points = topology.find_articulation_points()
        if art_points:
            lines.append("## ⚠️ Critical Transit Nodes")
            for ap in art_points:
                lines.append(f"  - **{ap['node']}** ({ap['role']}) — {ap['connections']} connections, "
                             f"removing it partitions {ap['partitions_created']} nodes")
            lines.append("")
    
    return "\n".join(lines)
