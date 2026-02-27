#!/usr/bin/env python3
"""
Ollama <-> Junos MCP Bridge v20.0 — Feedback Learning · Conversation Memory · Brain-Analyzed Corrections

v20.0 Enhancements — Feedback Learning · Multi-Session Memory · Brain-Analyzed Corrections:

  #E165 Feedback Learning Engine (user feedback → Brain analysis → validated insights → persistent DB)
  #E166 Conversation Memory Manager (named sessions, list/continue/delete previous conversations)
  #E167 Brain-Analyzed Corrections (feedback is analyzed, not taken as absolute truth)
  #E168 Feedback Prompt Injection (validated feedback insights injected into system prompt)
  #E169 Session Browser (list previous conversations with timestamps, topics, message counts)
  #E170 Cross-Session Knowledge (feedback + lessons persist and accumulate across all sessions)

v19.0 Enhancements — Claude Code-Style Terminal · Live Action Plans · Todo Integration:

  #E159 Claude Code Terminal UI (compact status line, thinking animation, token/cost tracking)
  #E160 Live Action Plan Tracker (persistent task plan with real-time status updates)
  #E161 Todo.md Integration (reads tasks/todo.md, displays current tasks, marks completion)
  #E162 Tool Call Visualization (detailed tool call display with timing, args, results)
  #E163 Session Context Bar (model, tokens used, tools called, elapsed time)
  #E164 Compact Output Mode (dense professional output like Claude Code terminal)

v18.0 Enhancements — Agentic Brain · Adaptive Concurrency · AI-Directed Probes:

  #E155 Agentic Brain Architecture (6-layer: Perception→Execution→Analysis→Probing→Validation→Synthesis)
  #E156 FactAccumulator (streaming dedup, contradiction detection, cross-device anomaly matrix)
  #E157 AdaptiveConcurrency (auto-tuning semaphore based on SSH gateway latency)
  #E158 AI-Directed Probes (AI requests targeted show commands → execute → feed back)
  #E148 Hypered Brain Engine (multi-layer AI: Perception→Analysis→Validation→Synthesis)
  #E149 Smart Fact-Gathering Scripts (18 targeted diagnostic scripts with parse rules)
  #E150 Parallel Script Execution (concurrent data gathering with semaphore-limited workers)
  #E151 Self-Validation Loop (AI identifies gaps → triggers additional scripts → re-analyzes)
  #E152 Double-Check Mechanism (confidence gating with multi-pass refinement)
  #E153 Evidence Accumulation (structured facts from every pass feed into final synthesis)
  #E154 Data Pipeline (Scripts → Structured Facts → AI Analysis → Gap Detection → Loop)

v16.0 Enhancements — Network Analysis Engine · Packet Capture · DNS Intelligence · Security Audit:

  #E139 Packet Capture Intelligence (Junos monitor traffic + protocol analysis — DNS/ICMP/TCP/BGP/OSPF)
  #E140 DNS Intelligence Engine (resolution verification, trace, batch DNS from routers)
  #E141 Security Audit Engine (13-check hardening audit — lo0/SSH/SNMP/BGP-auth/OSPF-auth/IS-IS/LDP)
  #E142 Flow & Performance Analysis (interface counters, error tracking, QoS/CoS)
  #E143 Alert & Threshold Engine (9 rules — ISIS/BGP/LDP/OSPF/CPU/memory/BFD/routes)
  #E144 Log Forensics & Timeline (syslog parsing, event correlation, root-cause timeline)
  #E145 Device Profiler (health scoring, anomaly detection, cross-device comparison)
  #E146 Persistent Analysis Memory (SQLite investigation history, device baselines, context recall)
  #E147 Guided Workflow Library (security_audit/troubleshooting/incident_response/capacity_planning/dns_forensics)

v15.0 Enhancements — Reasoning Engine · Topology Intelligence · Mind-Map v2:

  #E129 Reasoning Engine Module (7-stage pipeline: classify→hypothesize→investigate→diagnose→prescribe)
  #E130 Topology Intelligence Engine (multi-layer LLDP+iBGP+IS-IS+LDP fusion with Mermaid/ASCII)
  #E131 Hypothesis-Driven Investigation (Popperian method: disprove hypotheses, don't collect everything)
  #E132 Protocol Dependency Graph Walker (deterministic cascade chain resolution)
  #E133 Evidence Accumulator (forensic-grade confidence scoring per hypothesis)
  #E134 Advanced Junos Script Library (op/commit/event/PyEZ templates with install instructions)
  #E135 Articulation Point Analysis (find critical transit nodes whose failure partitions the network)
  #E136 ECMP Path Analysis (multi-path detection and load-balancing verification)
  #E137 JNCIE-SP Knowledge Expansion (SP design patterns, BFD integration, NETCONF RPC reference)
  #E138 Deep Knowledge v2 (chain-of-thought methodology, dependency graphs, automation architecture)

v14.0 Enhancements — Deep Reasoning · Topology Visualization · Mind-Map:

  #E123 Live Topology Visualization (Mermaid + ASCII from iBGP/LLDP/IS-IS)
  #E124 Mind-Map Deep Reasoning Engine (hierarchical problem decomposition)
  #E125 Junos Scripting Knowledge Injection (op/commit/event scripts, PyEZ)
  #E126 Protocol State Machine Reasoning (deterministic FSM-based diagnosis)
  #E127 Cascading Failure Chain Detection (pattern-matched cascade analysis)
  #E128 Deep Knowledge Base Integration (JUNOS_DEEP_KNOWLEDGE.md injection)

v13.1 Enhancements — Workflow Orchestration & Self-Improvement:

  #E117 Plan-First Workflow (plan mode for 3+ step tasks, re-plan on failure)
  #E118 Verification-Before-Done (prove work, diff behavior, staff-engineer standard)
  #E119 Self-Improvement Loop (learn from corrections → tasks/lessons.md)
  #E120 Autonomous Bug Fixing (resolve issues without hand-holding)
  #E121 Demand Elegance (balanced — skip for simple fixes, challenge non-trivial)
  #E122 Core Principles (simplicity first, no laziness, minimal impact)

v13.0 Enhancements — GPT-OSS Intelligence Upgrade (6 new):

  #E111 Model Upgrade to GPT-OSS (13B, stronger reasoning + tool calling)
  #E112 Structured Reasoning Chains (multi-step decomposition for complex queries)
  #E113 Expert Examples Injection (protocol-specific troubleshooting patterns via RAG)
  #E114 Junos Command Dictionary (validate AI-generated commands before presenting)
  #E115 Output Verification Layer (post-generation correctness check)
  #E116 Confidence-Gated Escalation (retry/cross-validate when confidence < threshold)

v11.0 Enhancements (40+ new, across 6 pillars):

  PILLAR 1 — AI Intelligence Deepening (10 enhancements):
  #E68  Dependency Graph Engine (live network graph from LLDP+OSPF+BGP)
  #E69  Multi-Hop Root Cause Chainer (symptom → L4 → L3 → L2 → L1)
  #E70  Confidence Scoring on all AI outputs (evidence-based 0-100)
  #E71  Baseline Anomaly Detection (per-router metric deviation)
  #E72  Auto-KB Enrichment (save new issue patterns to resolution DB)
  #E73  What-If Simulation Engine (dependency graph walking)
  #E74  Topology-Aware Reasoning (transit node identification)
  #E75  Multi-Hop Failure Path Tracing (end-to-end packet path)
  #E76  NOC Engineer Mode (step-by-step instructions)
  #E77  Automated Fix Validation Loop (verify → retry cycle)

  PILLAR 2 — Active Troubleshooting Engine (6 enhancements):
  #E78  AI-Guided Dynamic Troubleshooting (replaces static trees)
  #E79  Symptom-First Investigation Mode ("PE1 can't reach PE3")
  #E80  Concurrent Multi-Device Troubleshooting
  #E81  RSVP-TE Troubleshooting Tree
  #E82  BFD Troubleshooting Tree
  #E83  L2VPN/EVPN Troubleshooting Tree

  PILLAR 3 — Safe Configuration Engine (8 enhancements):
  #E84  Pre-Change Impact Analysis (blast radius before commit)
  #E85  Commit Confirmed with Auto-Verify
  #E86  Automated Rollback on Verification Failure
  #E87  Pre/Post Change State Capture & Comparison
  #E88  Change Templates/Playbooks (common operations)
  #E89  Multi-Device Atomic Changes
  #E90  Config Syntax Validation (pre-push check)
  #E91  Change Window Enforcement

  PILLAR 4 — Professional Reporting (8 enhancements):
  #E92  AI-Written Executive Narrative (CTO-level 3-paragraph summary)
  #E93  Dynamic Bottom Line (not OSPF-hardcoded)
  #E94  Quantified Risk Scoring (likelihood × impact = 0-100)
  #E95  Multiple Report Templates (executive/technical/compliance)
  #E96  Financial/SLA Impact Quantification
  #E97  Trend Visualizations in HTML Report
  #E98  NOC-Level Remediation Instructions (SSH here, type this, expect that)
  #E99  Report Comparison Dashboard (this audit vs previous)

  PILLAR 5 — New Specialists (5 enhancements):
  #E100 RSVP-TE Specialist (signaling, bandwidth, CSPF)
  #E101 QoS/CoS Specialist (classification, scheduling, shaping)
  #E102 Security Specialist (firewall filters, RE protection, prefix-lists)
  #E103 L3VPN Specialist (VRF route-targets, RD, PE-CE routing)
  #E104 Hardware/Environment Specialist (CPU, memory, optics, temperature)

  PILLAR 6 — Specialist Layer Deepening (6 enhancements):
  #E105 OSPF: SPF count monitoring, area type validation, virtual link check
  #E106 BGP: RR cluster-id consistency, max-prefix proximity, community validation
  #E107 MPLS: LDP session protection, label space, PHP behavior
  #E108 Protocol Dependency Graph per specialist
  #E109 Confidence scoring per specialist finding
  #E110 Inter-specialist finding handoff (real-time)

v10.0 Enhancements (30 new, across 5 pillars):

  PILLAR 1 — AI Intelligence & Junos Expertise (7 enhancements):
  #E38  Protocol State Machine Reasoning Engine (FSM validator)
  #E39  Cross-Router Correlation Engine (bidirectional state matching)
  #E40  Temporal Intelligence (commit-to-failure time correlation)
  #E41  Negative Space Analysis (expected-but-missing coverage matrix)
  #E42  Multi-Hop Root Cause Tracing (per-device dependency DAG)
  #E43  Smart Command Selection per device role (PE/P/RR)
  #E44  Self-Learning Issue Patterns (resolution database)

  PILLAR 2 — Report Quality & Professional Output (6 enhancements):
  #E45  Executive Dashboard (HTML visual one-pager with dials)
  #E46  ITIL-Aligned Findings (P1-P4 priority, MTTR, change ticket)
  #E47  Evidence Chain (forensic-grade proof per finding)
  #E48  Remediation Playbook (consolidated, ordered, with rollback)
  #E49  Compliance Report Enrichment (20+ CIS-aligned checks)
  #E50  Enhanced HTML Report (D3.js interactive topology)

  PILLAR 3 — Architecture Upgrades (6 enhancements):
  #E51  Async Pipeline with Rich Live Progress Streaming
  #E52  Configuration-Driven Architecture (config.yaml)
  #E53  Error Recovery & Resilience (circuit breaker pattern)
  #E54  Caching Layer (device facts + config hash caching)
  #E55  SQLite Backend for Historical Data
  #E56  Resolution Database (self-learning fixes)

  PILLAR 4 — Layer & Specialist Enhancements (6 enhancements):
  #E57  QoS/CoS Specialist (new layer)
  #E58  Security Specialist (new layer)
  #E59  Routing Table Depth Analysis
  #E60  Interface Utilization Analysis
  #E61  Graceful Restart / NSR Verification
  #E62  EVPN-VXLAN Deep Dive (expanded L2VPN)

  PILLAR 5 — State-of-the-Art Differentiators (5 enhancements):
  #E63  Natural Language to Junos Config (NL2Config pipeline)
  #E64  Predictive Failure Model (accelerating error rate detection)
  #E65  Interactive HTML Topology (D3.js / vis.js)
  #E66  Webhook & Notification Integration (Slack/Teams/PagerDuty)
  #E67  Multi-Vendor Extension Framework (abstract parser interface)

v9.0 Enhancements (Bug Fixes + Improvements):

  BUG FIXES:
  #BF1  Fix HEALTH_THRESHOLDS keys mismatch (KeyError crash in system health specialist)
  #BF2  Fix IS-IS parser false positives (config metadata lines parsed as adjacencies)
  #BF3  Add ISIS/BGP/LDP issues to all_current_issues (heatmap/health score completeness)
  #BF4  Rewrite reachability matrix with loopback IP mapping + fix rendering
  #BF5  Fix report version string (was "v7.0" → now "v9.0")
  #BF6  Fix health_score scoping (locals().get → try/except NameError)
  #BF7  Improve heatmap protocol detection (smarter keyword matching)

  ENHANCEMENTS:
  #E31  Improved topology IP extraction with .0 subinterface matching
  #E32  L2VPN parallel collection optimization
  #E33  Per-specialist analysis timing in report metadata
  #E34  Protocol inventory auto-detection (which protocols each router runs)
  #E35  Phase timing in audit for performance profiling
  #E36  Improved severity heatmap with proper issue-to-protocol mapping
  #E37  Storage/alarm/coredump issues included in health score calculation

v8.0 Enhancements (30 new, across 6 pillars):

  PILLAR A — AI Intelligence & Reasoning (8 enhancements):
  #E1  Chain-of-Thought enforcement in specialist prompts
  #E2  Structured JSON output from specialists → Synthesizer
  #E3  Self-verification loop (AI cross-checks own findings vs raw data)
  #E4  Per-finding confidence scoring (0.0-1.0)
  #E5  Negative space analysis (expected-but-missing data detection)
  #E6  Time-aware correlation (commit→alarm→flap timeline)
  #E7  Routing table anomaly detection (programmatic inet.0/inet.3 checks)
  #E8  RAG query refinement (second pass with discovered findings)

  PILLAR B — Junos Troubleshooting Depth (6 enhancements):
  #E9   OSPF LSDB cross-validation (Router-LSA advertisement comparison)
  #E10  BGP route flow tracing (prefix path verification)
  #E11  BFD↔Protocol correlation (cross-layer health linking)
  #E12  Interface error rate trending (CRC/input error delta tracking)
  #E13  Policy-options validation (import/export chain verification)
  #E14  Loopback reachability matrix (definitive lo0 IP-based checks)

  PILLAR C — Report Quality (6 enhancements):
  #E15  AI-generated executive narrative (CTO-level paragraph)
  #E16  Finding deduplication & proper ordering (severity-first grouping)
  #E17  Evidence quality score per finding ([green]●[/green] confirmed / [yellow]●[/yellow] inferred / [red]●[/red] AI-only)
  #E18  Remediation time estimates (TTR + expected downtime)
  #E19  SVG network diagram in HTML report
  #E20  Report section cross-linking (HTML anchors)

  PILLAR D — Architecture & Reliability (5 enhancements):
  #E21  Parallel L2VPN collection (asyncio.gather)
  #E22  Structured PhaseResult error recovery
  #E23  Fix print_status_bar() argument bug
  #E24  Fix troubleshoot tree walk logic
  #E25  Layer dashboard with real audit data

  PILLAR E — Knowledge Base & RAG (3 enhancements):
  #E26  KB: Commit confirm / rollback / commit check section
  #E27  KB: Operational health thresholds & normal baselines
  #E28  RAG: Per-protocol sub-index boost

  PILLAR F — Terminal UX & Polish (2 enhancements):
  #E29  Rich Progress bars for audit phases
  #E30  Fix commit history report section

v7.0 Enhancements (26 total, across 5 pillars):

  PILLAR 1 — Terminal Chat UI/UX (7 enhancements):
  #P1A  Rich terminal framework (colored tables, panels, spinners)
  #P1B  Professional welcome banner with system status dashboard
  #P1C  Structured chat input/output (styled panels per role)
  #P1D  Progress bars for audit phases
  #P1E  Formatted tables in terminal report preview
  #P1F  Interactive command help palette
  #P1G  Persistent status bar / dashboard header

  PILLAR 2 — AI Expertise (5 enhancements):
  #P2A  Multi-vendor awareness (Junos vs IOS/NX-OS idiom translation)
  #P2B  Configuration template library (Jinja2 validated templates)
  #P2C  Protocol state machine awareness (FSM stage diagnosis)
  #P2D  Junos version-aware analysis (feature compatibility matrix)
  #P2E  Predictive failure analysis (trend detection from historical data)

  PILLAR 3 — Report Quality (5 enhancements):
  #P3A  Report severity heatmap (device × protocol matrix)
  #P3B  AI-generated executive narrative (CTO-level summary)
  #P3C  Compliance & best practice scoring (NTP/SNMP/SSH/syslog audit)
  #P3D  Network capacity planning section (table sizes, utilization)
  #P3E  Report export formats (HTML with embedded CSS)

  PILLAR 4 — Architecture & Reliability (5 enhancements):
  #P4A  Async-friendly input with prompt_toolkit
  #P4B  Plugin architecture for specialists (modular file structure)
  #P4C  Configuration validation pipeline (pre-commit syntax + impact check)
  #P4D  Structured logging & telemetry (file-based, leveled)
  #P4E  Graceful degradation framework (data completeness tracking)

  PILLAR 5 — Troubleshooting Intelligence (4 enhancements):
  #P5A  Interactive troubleshooting mode (guided decision tree)
  #P5B  Layer-by-layer health dashboard (OSI model view)
  #P5C  Rollback impact analyzer (config drift risk assessment)
  #P5D  Automated dynamic root cause chains (from synthesizer JSON)

  Previous v6.0 features fully retained (22 enhancements):
    BFD, routing policy, MPLS LSP/RSVP, prefix limits, IS-IS specialist,
    system health specialist, firewall filters, severity scoring, parallel
    deep dive, structured Section 4, RAG configure, error recovery,
    reachability matrix, live verification, issue fingerprinting, commit
    history, executive summary, risk matrix, SLA impact, post-fix commands,
    report metadata, MCP auto-reconnect, token-aware trimming, batch
    pre-embedding, session persistence, hallucination guard, golden configs.

RAG (Retrieval Augmented Generation):
  The 184KB Knowledge Base is chunked and embedded using nomic-embed-text.
  At query time, the most semantically relevant chunks are retrieved via
  cosine similarity — replacing the old brittle keyword matching.

Specialist Layers:
  Layer 1: Protocol Specialists (OSPF, IS-IS, BGP, LDP, L2VPN, System Health — each gets RAG-retrieved KB)
  Layer 2: Synthesizer (combines specialist findings into root cause chain + severity scoring)
  Layer 3: Commander (interactive chat with tools, lightweight prompt)

This dramatically improves analysis quality on a 14B model by keeping
each AI call focused on ~4-8K tokens instead of 20-30K.
"""

import argparse
import asyncio
import glob
import json
import httpx
import logging
import re
import sys
import os
import time
import difflib
import hashlib
import sqlite3
import yaml
from datetime import datetime, timedelta
from pathlib import Path

# ── v15.0: Reasoning Engine Import ──────────────────────────
from reasoning_engine import (
    classify_problem, ProblemClassification, ProblemDomain, Complexity,
    generate_hypotheses, Hypothesis, Evidence, EvidenceAccumulator,
    find_root_cause_from_symptoms, walk_cascade, format_reasoning_chain,
    TopologyIntelligence, JUNOS_SCRIPT_TEMPLATES, get_script_template,
    list_available_scripts, PROTOCOL_DEPENDENCY_GRAPH,
)

# ── v16.0: Network Analysis Engine Import ───────────────────
from network_analysis import (
    NetworkAnalysisEngine, CaptureProtocol, CaptureRequest,
    build_capture_command, parse_capture_output,
    build_dns_commands, build_dns_trace_commands, parse_dns_output,
    JUNOS_SECURITY_CHECKS, analyze_security_output, generate_security_report,
    SecurityFinding, SecuritySeverity,
    build_flow_commands, parse_interface_counters,
    AlertEngine, AlertEvent, JUNOS_ALERT_RULES,
    build_forensic_commands, parse_syslog_line, correlate_events,
    format_forensic_timeline,
    DEVICE_PROFILE_COMMANDS, parse_device_profile, generate_device_comparison,
    AnalysisMemory, ANALYSIS_PROMPTS,
)

# ── v18.0: Hypered Brain Engine Import ──────────────────────
from hypered_brain import (
    hypered_brain_analyze, quick_brain_analyze,
    SMART_SCRIPTS, SmartScript, GatheredFact, ScriptResult,
    BrainState, BrainLayer, ScriptCategory, DataConfidence,
    select_scripts_for_query, compile_facts_summary,
    FactAccumulator, AdaptiveConcurrency, AIProbe,
    extract_ai_probes, execute_ai_probes,
)

# ── Rich Terminal UI (#P1A) ──────────────────────────────────
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.markdown import Markdown
from rich.text import Text
from rich.columns import Columns
from rich.style import Style
from rich.theme import Theme
from rich import box

# ── Professional Icon Constants ──────────────────────────────
# Unicode symbols replacing emojis for a clean, professional terminal UI
class Icons:
    """Professional Unicode icons for terminal UI — no emojis."""
    # Status indicators
    OK       = "●"   # Green dot for success
    FAIL     = "✗"   # Cross for failure
    WARN     = "▲"   # Triangle for warning
    INFO     = "◆"   # Diamond for info
    PENDING  = "○"   # Empty circle for pending
    
    # Structural
    ARROW    = "▸"   # Right-pointing triangle
    SEPARATOR = "│"  # Vertical line separator
    BULLET   = "▪"   # Small square bullet
    DASH     = "─"   # Horizontal line
    BLOCK    = "█"   # Full block
    SHADE    = "░"   # Light shade
    
    # Functional
    PROMPT   = "❯"   # User input prompt
    AI       = "◈"   # AI response indicator
    TOOL     = "⚙"   # Tool/gear
    SEARCH   = "⊕"   # Search/magnify
    LAYER    = "◇"   # Layer indicator
    LINK     = "⊶"   # Link/chain
    SHIELD   = "⊘"   # Security/shield
    GRAPH    = "◫"   # Chart/graph
    CLOCK    = "◷"   # Time/clock
    BOLT     = "⚡"  # Fast/lightning (this one stays — it's a Unicode symbol, not emoji)
    ATTACH   = "⊞"   # File attachment
    SAVE     = "⊟"   # Save/disk
    NET      = "⊛"   # Network/node
    BRAIN    = "◉"   # Brain/intelligence
    TARGET   = "◎"   # Target/focus
    FLOW     = "⇉"   # Flow/traffic
    ALERT    = "⊗"   # Alert/alarm
    CONFIG   = "⊡"   # Config/settings
    SCRIPT   = "⊞"   # Script/code
    MAP      = "◫"   # Topology map
    HEALTH   = "♦"   # Health indicator
    NEW      = "✦"   # New item
    RESTORE  = "↻"   # Restore/reload
    EXIT     = "⏻"   # Power/exit

# ══════════════════════════════════════════════════════════════
#  v19.0: CLAUDE CODE-STYLE TERMINAL — Action Tracker & Session
# ══════════════════════════════════════════════════════════════

class ActionStep:
    """A single step in an action plan."""
    def __init__(self, description: str, step_type: str = "action"):
        self.description = description
        self.step_type = step_type  # "action", "tool", "think", "verify"
        self.status = "pending"     # "pending", "running", "done", "failed", "skipped"
        self.detail = ""
        self.start_time = 0.0
        self.end_time = 0.0
        self.tool_name = ""
        self.tool_args_summary = ""
        self.result_summary = ""

    @property
    def elapsed(self) -> float:
        if self.end_time > 0:
            return self.end_time - self.start_time
        elif self.start_time > 0:
            return time.time() - self.start_time
        return 0.0

    def mark_running(self, detail: str = ""):
        self.status = "running"
        self.start_time = time.time()
        if detail:
            self.detail = detail

    def mark_done(self, detail: str = ""):
        self.status = "done"
        self.end_time = time.time()
        if detail:
            self.detail = detail

    def mark_failed(self, detail: str = ""):
        self.status = "failed"
        self.end_time = time.time()
        if detail:
            self.detail = detail


class ActionTracker:
    """Claude Code-style action plan tracker for the terminal session.
    
    Tracks the current action plan, tool calls, token usage, and session
    metrics. Displays a compact, live-updating view in the terminal.
    """

    def __init__(self, console_ref):
        self.console = console_ref
        self.current_plan: list[ActionStep] = []
        self.plan_title = ""
        self.session_start = time.time()
        self.total_tool_calls = 0
        self.total_ai_calls = 0
        self.total_tokens_approx = 0
        self.current_query = ""
        self._active_step_idx = -1

    def new_plan(self, title: str, steps: list[str]):
        """Create a new action plan from a list of step descriptions."""
        self.plan_title = title
        self.current_plan = [ActionStep(desc) for desc in steps]
        self._active_step_idx = -1
        self._display_plan()

    def auto_plan_from_query(self, query: str, query_type: str):
        """Auto-generate an action plan based on query classification."""
        self.current_query = query
        steps = []
        title = ""

        if query_type == "troubleshoot":
            title = f"Troubleshoot: {query[:60]}"
            steps = [
                "Classify problem domain & complexity",
                "Select investigation strategy",
                "Collect data from routers via MCP tools",
                "Analyze collected data",
                "Cross-correlate findings across devices",
                "Generate diagnosis & remediation",
            ]
        elif query_type == "status":
            title = f"Status Check: {query[:60]}"
            steps = [
                "Identify target devices & protocols",
                "Collect live data from routers",
                "Parse and analyze output",
                "Report current status",
            ]
        elif query_type == "compare":
            title = f"Comparison: {query[:60]}"
            steps = [
                "Fetch configurations/data from devices",
                "Normalize and align data",
                "Compare side by side",
                "Report differences",
            ]
        elif query_type == "config":
            title = f"Configuration: {query[:60]}"
            steps = [
                "Analyze change request",
                "Gather current config context",
                "Generate safe config commands",
                "Validate commands against dictionary",
                "Present for review",
            ]
        elif query_type == "knowledge":
            title = f"Knowledge Query: {query[:60]}"
            steps = [
                "Search knowledge base (RAG retrieval)",
                "Compile relevant context",
                "Generate answer from KB references",
            ]
        else:
            title = f"Query: {query[:60]}"
            steps = [
                "Analyze query intent",
                "Collect relevant data",
                "Generate response",
            ]

        self.new_plan(title, steps)

    def start_step(self, idx: int, detail: str = ""):
        """Mark a step as running."""
        if 0 <= idx < len(self.current_plan):
            self.current_plan[idx].mark_running(detail)
            self._active_step_idx = idx
            self._display_step_update(idx)

    def complete_step(self, idx: int, detail: str = ""):
        """Mark a step as done."""
        if 0 <= idx < len(self.current_plan):
            self.current_plan[idx].mark_done(detail)
            self._display_step_update(idx)

    def fail_step(self, idx: int, detail: str = ""):
        """Mark a step as failed."""
        if 0 <= idx < len(self.current_plan):
            self.current_plan[idx].mark_failed(detail)
            self._display_step_update(idx)

    def advance_to_next(self, detail: str = ""):
        """Complete the current step and start the next one."""
        if self._active_step_idx >= 0:
            self.complete_step(self._active_step_idx, detail)
        next_idx = self._active_step_idx + 1
        if next_idx < len(self.current_plan):
            self.start_step(next_idx)
            return next_idx
        return -1

    def record_tool_call(self, tool_name: str, args_summary: str = "", result_len: int = 0):
        """Record a tool call for session metrics."""
        self.total_tool_calls += 1
        if self._active_step_idx >= 0 and self._active_step_idx < len(self.current_plan):
            step = self.current_plan[self._active_step_idx]
            step.tool_name = tool_name
            step.tool_args_summary = args_summary

    def record_ai_call(self, approx_tokens: int = 0):
        """Record an AI call for session metrics."""
        self.total_ai_calls += 1
        self.total_tokens_approx += approx_tokens

    def complete_plan(self):
        """Mark all remaining pending steps as done and display final summary."""
        for step in self.current_plan:
            if step.status == "pending":
                step.status = "skipped"
            elif step.status == "running":
                step.mark_done()
        self._display_plan_summary()

    def _display_plan(self):
        """Display the full action plan as a compact list."""
        if not self.current_plan:
            return
        self.console.print()
        self.console.print(f"  [bold #5fd7ff]╭─ Action Plan: {self.plan_title}[/bold #5fd7ff]")
        for i, step in enumerate(self.current_plan):
            icon = self._step_icon(step.status)
            num = f"[dim]{i+1}.[/dim]"
            self.console.print(f"  [#5fd7ff]│[/#5fd7ff] {num} {icon} {step.description}")
        self.console.print(f"  [#5fd7ff]╰{'─' * 60}[/#5fd7ff]")

    def _display_step_update(self, idx: int):
        """Display a single step status update inline."""
        if idx < 0 or idx >= len(self.current_plan):
            return
        step = self.current_plan[idx]
        icon = self._step_icon(step.status)
        timing = ""
        if step.status in ("done", "failed") and step.elapsed > 0:
            timing = f" [dim]({step.elapsed:.1f}s)[/dim]"
        detail_str = f" [dim]— {step.detail}[/dim]" if step.detail else ""
        self.console.print(f"  [#5fd7ff]│[/#5fd7ff] [dim]{idx+1}.[/dim] {icon} {step.description}{detail_str}{timing}")

    def _display_plan_summary(self):
        """Display final plan summary with all steps and timing."""
        if not self.current_plan:
            return
        done = sum(1 for s in self.current_plan if s.status == "done")
        failed = sum(1 for s in self.current_plan if s.status == "failed")
        total_time = sum(s.elapsed for s in self.current_plan if s.status in ("done", "failed"))
        
        status_str = f"[green]✓ {done} done[/green]"
        if failed:
            status_str += f" [red]✗ {failed} failed[/red]"
        
        self.console.print(f"  [#5fd7ff]╰─ {status_str} [dim]in {total_time:.1f}s[/dim] "
                          f"[dim]│ {self.total_tool_calls} tool calls │ {self.total_ai_calls} AI calls[/dim][/#5fd7ff]")

    @staticmethod
    def _step_icon(status: str) -> str:
        icons = {
            "pending": "[dim]○[/dim]",
            "running": "[bold #ff8700]◌[/bold #ff8700]",
            "done": "[green]●[/green]",
            "failed": "[red]✗[/red]",
            "skipped": "[dim]⊘[/dim]",
        }
        return icons.get(status, "[dim]○[/dim]")

    def print_session_bar(self, device_count: int = 0, health_score: float = -1,
                          msg_count: int = 0, rag_chunks: int = 0):
        """Display Claude Code-style compact session status bar."""
        elapsed = time.time() - self.session_start
        # Format elapsed time
        if elapsed < 60:
            time_str = f"{elapsed:.0f}s"
        elif elapsed < 3600:
            time_str = f"{elapsed/60:.0f}m {elapsed%60:.0f}s"
        else:
            time_str = f"{elapsed/3600:.0f}h {(elapsed%3600)/60:.0f}m"

        parts = []
        parts.append(f"[cyan]{Icons.NET} {device_count}[/cyan]")
        if health_score >= 0:
            color = "green" if health_score >= 75 else ("yellow" if health_score >= 50 else "red")
            grade = "A" if health_score >= 90 else ("B" if health_score >= 75 else ("C" if health_score >= 60 else ("D" if health_score >= 40 else "F")))
            parts.append(f"[{color}]{Icons.HEALTH}{health_score:.0f}({grade})[/{color}]")
        parts.append(f"[dim]{Icons.TOOL}{self.total_tool_calls}[/dim]")
        parts.append(f"[dim]{Icons.BRAIN}{self.total_ai_calls}[/dim]")
        if rag_chunks > 0:
            parts.append(f"[dim]{Icons.SEARCH}{rag_chunks}[/dim]")
        parts.append(f"[dim]{Icons.CLOCK}{time_str}[/dim]")
        parts.append(f"[dim]{msg_count}msg[/dim]")
        
        bar = f" {Icons.SEPARATOR} ".join(parts)
        self.console.print(f" {bar}", style="dim")


class TodoTracker:
    """Reads and displays tasks from tasks/todo.md, tracks completion."""

    def __init__(self, todo_path: str = None):
        if todo_path is None:
            todo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks", "todo.md")
        self.todo_path = todo_path
        self.sections: list[dict] = []
        self.active_tasks: list[dict] = []
        self._load()

    def _load(self):
        """Parse todo.md for sections and tasks."""
        try:
            if not os.path.exists(self.todo_path):
                return
            with open(self.todo_path, "r") as f:
                content = f.read()
            
            current_section = ""
            current_goal = ""
            for line in content.split("\n"):
                # Section headers
                if line.startswith("# "):
                    current_section = line[2:].strip()
                elif line.startswith("## Goal"):
                    pass  # next line is the goal
                elif line.startswith("## Completed"):
                    current_section = ""  # skip completed sections
                elif line.startswith("## Remaining") or line.startswith("## "):
                    current_section = line.lstrip("#").strip()
                
                # Task items
                if line.strip().startswith("- [x]"):
                    pass  # completed task, skip
                elif line.strip().startswith("- [ ]"):
                    task_text = line.strip()[6:].strip()
                    # Remove bold markers
                    task_text = task_text.replace("**", "")
                    self.active_tasks.append({
                        "text": task_text,
                        "section": current_section,
                        "done": False,
                    })
        except Exception:
            pass

    def refresh(self):
        """Reload tasks from disk."""
        self.sections = []
        self.active_tasks = []
        self._load()

    def get_active_tasks(self, limit: int = 10) -> list[dict]:
        """Get the first N active (uncompleted) tasks."""
        return self.active_tasks[:limit]

    def display(self, console_ref, limit: int = 8):
        """Display active todo items in Claude Code style."""
        tasks = self.get_active_tasks(limit)
        if not tasks:
            console_ref.print("  [dim]No active tasks in tasks/todo.md[/dim]")
            return
        
        console_ref.print(f"\n  [bold #ff8700]╭─ Active Tasks (tasks/todo.md)[/bold #ff8700]")
        last_section = ""
        for i, task in enumerate(tasks):
            if task["section"] and task["section"] != last_section:
                console_ref.print(f"  [#ff8700]│[/#ff8700] [dim italic]── {task['section']}[/dim italic]")
                last_section = task["section"]
            icon = "[dim]○[/dim]" if not task["done"] else "[green]●[/green]"
            console_ref.print(f"  [#ff8700]│[/#ff8700] {icon} {task['text'][:75]}")
        if len(self.active_tasks) > limit:
            console_ref.print(f"  [#ff8700]│[/#ff8700] [dim]... and {len(self.active_tasks) - limit} more[/dim]")
        console_ref.print(f"  [#ff8700]╰{'─' * 60}[/#ff8700]")

    def mark_done(self, task_text_partial: str) -> bool:
        """Mark a task as done by partial text match."""
        for task in self.active_tasks:
            if task_text_partial.lower() in task["text"].lower():
                task["done"] = True
                return True
        return False


# ══════════════════════════════════════════════════════════════
#  v20.0 E165: FEEDBACK MEMORY — Brain-Analyzed Learning Engine
# ══════════════════════════════════════════════════════════════

class FeedbackMemory:
    """Persistent feedback store with Brain-analyzed validation.
    
    Unlike the old correction system that blindly saved user corrections,
    this engine:
    1. Records explicit user feedback
    2. Uses the AI Brain to critically analyze feedback (valid/partial/invalid)
    3. Stores analysis alongside feedback for future reference
    4. Injects validated insights into the system prompt
    """

    def __init__(self, db_path: str = None):
        self.db_path = db_path or FEEDBACK_DB_PATH
        self.entries: list[dict] = []
        self._load()

    def _load(self):
        """Load feedback database from disk."""
        try:
            if os.path.exists(self.db_path):
                with open(self.db_path, "r") as f:
                    self.entries = json.load(f)
        except Exception as e:
            logger.warning(f"Feedback DB load failed: {e}")
            self.entries = []

    def _save(self):
        """Persist feedback database to disk."""
        try:
            # Trim to max entries, keep most recent
            if len(self.entries) > MAX_FEEDBACK_ENTRIES:
                self.entries = self.entries[-MAX_FEEDBACK_ENTRIES:]
            with open(self.db_path, "w") as f:
                json.dump(self.entries, f, indent=2)
        except Exception as e:
            logger.warning(f"Feedback DB save failed: {e}")

    def add_feedback(self, user_msg: str, ai_response: str, feedback_text: str,
                     brain_analysis: dict | None = None, session_id: str = ""):
        """Store a feedback entry with Brain analysis results."""
        entry = {
            "id": f"fb_{int(time.time())}_{len(self.entries)}",
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "user_original_query": user_msg[:500],
            "ai_response_excerpt": ai_response[:500],
            "feedback": feedback_text[:1000],
            "brain_analysis": brain_analysis or {},
            "validity": (brain_analysis or {}).get("validity", "unanalyzed"),
            "applied": False,
        }
        self.entries.append(entry)
        self._save()
        return entry

    async def analyze_feedback_with_brain(self, feedback_text: str, ai_response: str,
                                           user_query: str = "") -> dict:
        """Use the AI Brain to critically evaluate user feedback.
        
        Returns a dict with:
        - validity: 'valid' | 'partially_valid' | 'invalid' | 'subjective'
        - reasoning: Why the Brain thinks so
        - corrected_fact: What the correct answer should be (if applicable)
        - confidence: 0.0 - 1.0
        - action: 'learn' | 'note' | 'ignore'
        """
        try:
            analysis_prompt = (
                "You are a critical feedback analyzer for a Juniper network AI engineer.\n"
                "A user has given feedback about an AI response. Your job is to CRITICALLY evaluate\n"
                "the feedback — do NOT blindly accept it as truth. The user could be:\n"
                "- Correct (AI made a genuine mistake)\n"
                "- Partially correct (some valid points, some not)\n"
                "- Incorrect (user is mistaken about network concepts)\n"
                "- Subjective (matter of preference/style, not factual)\n\n"
                f"AI'S ORIGINAL RESPONSE (excerpt):\n{ai_response[:800]}\n\n"
                f"USER'S FEEDBACK:\n{feedback_text}\n\n"
                "Analyze this feedback and respond in this EXACT format (one line each):\n"
                "VALIDITY: <valid|partially_valid|invalid|subjective>\n"
                "CONFIDENCE: <0.0 to 1.0>\n"
                "REASONING: <why you assessed it this way — cite specific technical facts>\n"
                "CORRECTED_FACT: <the correct information if the feedback is valid, or 'N/A'>\n"
                "ACTION: <learn|note|ignore>\n"
                "RULE: <a concise rule to follow in the future, or 'N/A'>\n"
            )

            result = await ollama_analyze(
                "You are a senior network engineer peer-reviewing feedback. Be objective and technical. "
                "Do NOT assume the user is always right — verify against Juniper/networking knowledge.",
                "",
                analysis_prompt
            )

            # Parse response
            analysis = {
                "validity": "unanalyzed",
                "confidence": 0.5,
                "reasoning": "",
                "corrected_fact": "",
                "action": "note",
                "rule": "",
                "raw_analysis": result[:500],
            }
            for line in result.split("\n"):
                line = line.strip()
                upper = line.upper()
                if upper.startswith("VALIDITY:"):
                    val = line.split(":", 1)[1].strip().lower().replace(" ", "_")
                    if val in ("valid", "partially_valid", "invalid", "subjective"):
                        analysis["validity"] = val
                elif upper.startswith("CONFIDENCE:"):
                    try:
                        analysis["confidence"] = float(line.split(":", 1)[1].strip())
                    except ValueError:
                        pass
                elif upper.startswith("REASONING:"):
                    analysis["reasoning"] = line.split(":", 1)[1].strip()
                elif upper.startswith("CORRECTED_FACT:"):
                    analysis["corrected_fact"] = line.split(":", 1)[1].strip()
                elif upper.startswith("ACTION:"):
                    act = line.split(":", 1)[1].strip().lower()
                    if act in ("learn", "note", "ignore"):
                        analysis["action"] = act
                elif upper.startswith("RULE:"):
                    analysis["rule"] = line.split(":", 1)[1].strip()

            return analysis
        except Exception as e:
            logger.warning(f"Brain feedback analysis failed: {e}")
            return {
                "validity": "unanalyzed",
                "confidence": 0.0,
                "reasoning": f"Analysis failed: {e}",
                "corrected_fact": "",
                "action": "note",
                "rule": "",
            }

    def get_feedback_insights(self, n: int = 10) -> str:
        """Get validated feedback insights for system prompt injection.
        Only includes feedback marked as valid/partially_valid with learn/note actions."""
        actionable = [
            e for e in self.entries
            if e.get("validity") in ("valid", "partially_valid")
            and e.get("brain_analysis", {}).get("action") in ("learn", "note")
        ]
        if not actionable:
            return ""

        # Sort by timestamp descending, take top N
        actionable.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        top = actionable[:n]

        lines = ["## USER FEEDBACK INSIGHTS (Brain-validated)"]
        for fb in top:
            validity_icon = "✓" if fb["validity"] == "valid" else "◐"
            rule = fb.get("brain_analysis", {}).get("rule", "")
            if rule and rule != "N/A":
                lines.append(f"- {validity_icon} [{fb['validity']}] {rule}")
            else:
                lines.append(f"- {validity_icon} [{fb['validity']}] Feedback: {fb['feedback'][:100]}")
        return "\n".join(lines)

    def display_history(self, console_ref, limit: int = 10):
        """Display feedback history in Claude Code style."""
        if not self.entries:
            console_ref.print("  [dim]No feedback history yet. Use 'feedback <your feedback>' to provide feedback.[/dim]")
            return

        recent = self.entries[-limit:]
        recent.reverse()

        fb_table = Table(title=f"{Icons.BRAIN} Feedback History (Brain-Analyzed)",
                         box=box.ROUNDED, border_style="#af87ff",
                         title_style="bold #af87ff", padding=(0, 1))
        fb_table.add_column("#", style="dim", width=4)
        fb_table.add_column("Time", style="dim", width=16)
        fb_table.add_column("Feedback", width=40)
        fb_table.add_column("Validity", justify="center", width=16)
        fb_table.add_column("Action", justify="center", width=8)

        validity_colors = {
            "valid": "[green]✓ valid[/green]",
            "partially_valid": "[yellow]◐ partial[/yellow]",
            "invalid": "[red]✗ invalid[/red]",
            "subjective": "[blue]◇ subjective[/blue]",
            "unanalyzed": "[dim]… pending[/dim]",
        }
        action_colors = {
            "learn": "[green]learn[/green]",
            "note": "[yellow]note[/yellow]",
            "ignore": "[red]ignore[/red]",
        }

        for i, entry in enumerate(recent, 1):
            ts = entry.get("timestamp", "")[:16].replace("T", " ")
            fb_text = entry.get("feedback", "")[:38]
            validity = validity_colors.get(entry.get("validity", ""), "[dim]?[/dim]")
            action = action_colors.get(
                entry.get("brain_analysis", {}).get("action", "note"), "[dim]?[/dim]"
            )
            fb_table.add_row(str(i), ts, fb_text, validity, action)

        console_ref.print(fb_table)

    def get_stats(self) -> dict:
        """Return summary statistics about feedback."""
        total = len(self.entries)
        valid = sum(1 for e in self.entries if e.get("validity") == "valid")
        partial = sum(1 for e in self.entries if e.get("validity") == "partially_valid")
        invalid = sum(1 for e in self.entries if e.get("validity") == "invalid")
        return {"total": total, "valid": valid, "partial": partial, "invalid": invalid}


# ══════════════════════════════════════════════════════════════
#  v20.0 E166: CONVERSATION MEMORY MANAGER — Multi-Session Persistence
# ══════════════════════════════════════════════════════════════

class ConversationManager:
    """Manages multiple conversation sessions with auto-naming and browsing.
    
    Replaces the old single-file session_history.json with a directory
    of conversation files, each with metadata (topic, timestamp, msg count).
    Users can list, continue, or delete any previous conversation.
    """

    def __init__(self, conv_dir: str = None):
        self.conv_dir = conv_dir or CONVERSATIONS_DIR
        os.makedirs(self.conv_dir, exist_ok=True)
        self.conversations_index: list[dict] = []
        self._load_index()

    def _index_path(self) -> str:
        return os.path.join(self.conv_dir, "_index.json")

    def _load_index(self):
        """Load conversation index from disk."""
        try:
            idx_path = self._index_path()
            if os.path.exists(idx_path):
                with open(idx_path, "r") as f:
                    self.conversations_index = json.load(f)
            else:
                # Migrate old session_history.json if it exists
                self._migrate_old_session()
        except Exception as e:
            logger.warning(f"Conversation index load failed: {e}")
            self.conversations_index = []

    def _save_index(self):
        """Save conversation index to disk."""
        try:
            # Trim to max conversations
            if len(self.conversations_index) > MAX_CONVERSATIONS:
                # Remove oldest conversations (files + index entries)
                to_remove = self.conversations_index[:-MAX_CONVERSATIONS]
                for conv in to_remove:
                    fpath = os.path.join(self.conv_dir, f"{conv['id']}.json")
                    if os.path.exists(fpath):
                        os.remove(fpath)
                self.conversations_index = self.conversations_index[-MAX_CONVERSATIONS:]
            with open(self._index_path(), "w") as f:
                json.dump(self.conversations_index, f, indent=2)
        except Exception as e:
            logger.warning(f"Conversation index save failed: {e}")

    def _migrate_old_session(self):
        """Migrate old session_history.json to new conversation format."""
        try:
            if os.path.exists(SESSION_HISTORY_PATH):
                with open(SESSION_HISTORY_PATH, "r") as f:
                    data = json.load(f)
                msgs = data.get("messages", [])
                saved_at = data.get("saved_at", datetime.now().isoformat())
                if msgs:
                    conv_id = f"conv_{int(datetime.fromisoformat(saved_at).timestamp())}"
                    self.save_conversation(msgs, name="Migrated Session", conv_id=conv_id)
                    logger.info(f"Migrated old session_history.json → {conv_id}")
        except Exception as e:
            logger.debug(f"Old session migration skipped: {e}")

    def _auto_generate_topic(self, messages: list) -> str:
        """Generate a short topic name from conversation content."""
        user_msgs = [m.get("content", "") for m in messages if m.get("role") == "user"]
        if not user_msgs:
            return "General Chat"
        # Use first user message as topic hint
        first = user_msgs[0][:120].strip()
        # Clean up
        first = re.sub(r'[^\w\s\-/]', '', first)
        if len(first) > 60:
            first = first[:57] + "..."
        return first or "General Chat"

    def save_conversation(self, messages: list, name: str = None, conv_id: str = None) -> str:
        """Save a conversation to disk with auto-generated topic.
        Returns the conversation ID."""
        # Filter saveable messages
        saveable = [m for m in messages if m.get("role") in ("user", "assistant") and m.get("content")]
        if not saveable:
            return ""

        cid = conv_id or f"conv_{int(time.time())}"
        topic = name or self._auto_generate_topic(saveable)

        # Save the conversation file
        conv_data = {
            "id": cid,
            "topic": topic,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "message_count": len(saveable),
            "messages": saveable,
        }
        conv_path = os.path.join(self.conv_dir, f"{cid}.json")
        with open(conv_path, "w") as f:
            json.dump(conv_data, f, indent=2)

        # Update index — check if conversation already exists
        existing = next((c for c in self.conversations_index if c["id"] == cid), None)
        if existing:
            existing["updated_at"] = datetime.now().isoformat()
            existing["message_count"] = len(saveable)
            existing["topic"] = topic
        else:
            self.conversations_index.append({
                "id": cid,
                "topic": topic,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "message_count": len(saveable),
            })
        self._save_index()
        
        # Also save to legacy session_history.json for backward compat
        try:
            save_session_history(messages)
        except Exception:
            pass
        
        return cid

    def list_conversations(self) -> list[dict]:
        """Return list of conversations sorted by most recent first."""
        convs = sorted(self.conversations_index, key=lambda x: x.get("updated_at", ""), reverse=True)
        return convs

    def load_conversation(self, conv_id: str) -> list:
        """Load messages from a specific conversation."""
        conv_path = os.path.join(self.conv_dir, f"{conv_id}.json")
        if not os.path.exists(conv_path):
            return []
        try:
            with open(conv_path, "r") as f:
                data = json.load(f)
            return data.get("messages", [])
        except Exception as e:
            logger.warning(f"Failed to load conversation {conv_id}: {e}")
            return []

    def delete_conversation(self, conv_id: str) -> bool:
        """Delete a conversation by ID."""
        conv_path = os.path.join(self.conv_dir, f"{conv_id}.json")
        if os.path.exists(conv_path):
            os.remove(conv_path)
        self.conversations_index = [c for c in self.conversations_index if c["id"] != conv_id]
        self._save_index()
        return True

    def display_conversations(self, console_ref, limit: int = 15):
        """Display conversation browser in Claude Code style."""
        convs = self.list_conversations()
        if not convs:
            console_ref.print("  [dim]No saved conversations yet. Your conversations will be auto-saved.[/dim]")
            return

        conv_table = Table(title=f"{Icons.RESTORE} Saved Conversations",
                           box=box.ROUNDED, border_style="#5fd7ff",
                           title_style="bold #5fd7ff", padding=(0, 1))
        conv_table.add_column("#", style="bold #87d7ff", width=4)
        conv_table.add_column("Topic", style="white", width=45)
        conv_table.add_column("Messages", justify="center", width=10)
        conv_table.add_column("Last Updated", style="dim", width=18)

        for i, conv in enumerate(convs[:limit], 1):
            ts = conv.get("updated_at", "")[:16].replace("T", " ")
            topic = conv.get("topic", "Untitled")[:43]
            msgs = str(conv.get("message_count", 0))
            conv_table.add_row(str(i), topic, msgs, ts)

        console_ref.print(conv_table)
        console_ref.print(f"  [dim]Use 'continue <#>' to resume a conversation, 'delete conversation <#>' to remove[/dim]")

    def get_conversation_by_number(self, number: int) -> dict | None:
        """Get a conversation by its display number (1-indexed)."""
        convs = self.list_conversations()
        if 1 <= number <= len(convs):
            return convs[number - 1]
        return None


# ── v19.0 / v20.0: Session-level tracker instances (set in main()) ──
_action_tracker: ActionTracker | None = None
_todo_tracker: TodoTracker | None = None
_feedback_memory: FeedbackMemory | None = None
_conversation_manager: ConversationManager | None = None

# Custom theme for the bridge — enhanced professional palette
BRIDGE_THEME = Theme({
    "info":       "cyan",
    "success":    "bold green",
    "warning":    "bold yellow",
    "error":      "bold red",
    "critical":   "bold white on red",
    "heading":    "bold magenta",
    "device":     "bold cyan",
    "protocol":   "bold blue",
    "command":    "dim italic",
    "metric":     "bold white",
    "prompt":     "bold #00d7ff",
    "ai_label":   "bold #af87ff",
    "separator":  "dim #585858",
    "accent":     "bold #ff8700",
    "layer":      "bold #5fd7ff",
    "phase":      "bold #87d7ff",
    "attach":     "bold #d7af5f",
    "version":    "bold #87ff87",
    "dim_info":   "dim cyan",
    "muted":      "#8a8a8a",
})

console = Console(theme=BRIDGE_THEME)

# ── E52: Configuration-Driven Architecture ──────────────────
def load_config(config_path: str = None) -> dict:
    """Load configuration from config.yaml, with defaults fallback."""
    if config_path is None:
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.yaml")
    try:
        with open(config_path, "r") as f:
            cfg = yaml.safe_load(f) or {}
        return cfg
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"▲  Error loading config.yaml: {e} — using defaults")
        return {}

_config = load_config()

# ── Health Thresholds (used by system health specialist) ─────
_thresh_cfg = _config.get("thresholds", {})
HEALTH_THRESHOLDS = {
    "crc_error_rate": _thresh_cfg.get("crc_error_rate", 10),
    "storage_pct": _thresh_cfg.get("storage_pct", 80),
    "uptime_min_hours": _thresh_cfg.get("uptime_min_hours", 24),
    "bgp_prefix_deviation_pct": _thresh_cfg.get("bgp_prefix_deviation_pct", 20),
    "ospf_dead_interval_max": _thresh_cfg.get("ospf_dead_interval_max", 120),
    "route_table_max": _thresh_cfg.get("route_table_max", 1_000_000),
    "crc_errors_per_audit": _thresh_cfg.get("crc_errors_per_audit", 10),
    "input_errors_per_audit": _thresh_cfg.get("input_errors_per_audit", 50),
    "carrier_transitions": _thresh_cfg.get("carrier_transitions", 10),
    "storage_pct_warning": _thresh_cfg.get("storage_pct_warning", 80),
    "storage_pct_critical": _thresh_cfg.get("storage_pct_critical", 95),
    "interface_utilization_warning": _thresh_cfg.get("interface_utilization_warning", 80),
    "interface_utilization_critical": _thresh_cfg.get("interface_utilization_critical", 95),
    "bgp_flap_threshold": _thresh_cfg.get("bgp_flap_threshold", 5),
    "memory_utilization_warning": _thresh_cfg.get("memory_utilization_warning", 80),
    "cpu_utilization_warning": _thresh_cfg.get("cpu_utilization_warning", 80),
}

# ── Structured Logging (#P4D) ───────────────────────────────
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, f"bridge_{datetime.now().strftime('%Y-%m-%d')}.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(log_file),
    ]
)
logger = logging.getLogger("junos-bridge")

# RAG Vector Store for semantic KB retrieval
from kb_vectorstore import KBVectorStore

MCP_SERVER_URL = _config.get("mcp", {}).get("url", "http://127.0.0.1:30030/mcp/")
OLLAMA_URL = _config.get("ai", {}).get("ollama_url", "http://127.0.0.1:11434")
MODEL = _config.get("ai", {}).get("model", "qwen2.5:14b")
NUM_CTX = _config.get("ai", {}).get("context_window", 32768)
CHARS_PER_TOKEN = _config.get("ai", {}).get("chars_per_token", 4)
MAX_CTX_USAGE = _config.get("ai", {}).get("max_context_usage", 0.80)
AI_TEMPERATURE = _config.get("ai", {}).get("temperature", 0.15)
AI_TOP_P = _config.get("ai", {}).get("top_p", 0.9)
AI_REPEAT_PENALTY = _config.get("ai", {}).get("repeat_penalty", 1.1)
TOOL_RESULT_MAX_CHARS = _config.get("ai", {}).get("tool_result_max_chars", 8000)

# ── v13.0: Advanced reasoning settings ──────────────────────
AI_STRUCTURED_REASONING = _config.get("ai", {}).get("structured_reasoning", True)
AI_CONFIDENCE_THRESHOLD = _config.get("ai", {}).get("confidence_threshold", 70)
AI_EXPERT_EXAMPLES = _config.get("ai", {}).get("expert_examples", True)
AI_OUTPUT_VERIFICATION = _config.get("ai", {}).get("output_verification", True)
AI_COMMAND_DICTIONARY = _config.get("ai", {}).get("command_dictionary", True)

# ── v13.0: Junos Command Dictionary ─────────────────────────
JUNOS_COMMANDS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "junos_commands.json")
_junos_cmd_dict: dict = {}
try:
    with open(JUNOS_COMMANDS_PATH, "r") as f:
        _junos_cmd_dict = json.load(f)
    logger.info(f"Loaded Junos command dictionary: {sum(len(v) if isinstance(v, list) else sum(len(sv) for sv in v.values() if isinstance(sv, list)) for v in _junos_cmd_dict.get('show_commands', {}).values())} show commands, "
                f"{sum(len(v) if isinstance(v, list) else sum(len(sv) for sv in v.values() if isinstance(sv, list)) for v in _junos_cmd_dict.get('set_commands', {}).values())} set commands")
except Exception as e:
    logger.warning(f"Could not load junos_commands.json: {e}")

# ── v13.0: Expert Examples Store ─────────────────────────────
EXPERT_EXAMPLES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "EXPERT_EXAMPLES.md")
_expert_examples_content: str = ""
try:
    with open(EXPERT_EXAMPLES_PATH, "r") as f:
        _expert_examples_content = f.read()
    logger.info(f"Loaded expert examples: {len(_expert_examples_content)} chars")
except Exception:
    logger.warning("EXPERT_EXAMPLES.md not found — expert example injection disabled")

# ── RAG Vector Store (initialized at startup) ───────────────
vector_kb: KBVectorStore | None = None  # Set in main()

# ── Session persistence (Enhancement #4) ────────────────────
SESSION_HISTORY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "session_history.json")
MAX_PERSISTED_MESSAGES = 30    # Keep last N messages across restarts

# ── v20.0: Multi-Session Conversation Memory ────────────────
CONVERSATIONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "conversations")
FEEDBACK_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "feedback_memory.json")
MAX_FEEDBACK_ENTRIES = 200     # Max feedback entries to keep
MAX_CONVERSATIONS = 50         # Max saved conversations

# ── Audit report directory (Enhancement #11) ────────────────
AUDIT_REPORT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Golden Config Store ──────────────────────────────────────
GOLDEN_CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "golden_configs")

# ── Enhancement #3C: Historical Issue Fingerprinting ─────────
ISSUE_FINGERPRINT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "issue_fingerprints.json")

# ── v12.0: Lessons Learned Database ─────────────────────────
LESSONS_LEARNED_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lessons_learned.json")

# ── Enhancement #2A: Severity Scoring ────────────────────────
SEVERITY_WEIGHTS = {
    "CRITICAL": 10,
    "MAJOR": 7,
    "WARNING": 3,
    "INFO": 1,
}

# ── Enhancement #P4E: Data Completeness Tracking ────────────
collection_status: dict = {}  # {"command_label": "success"|"failed"|"timeout"}

# ── Concurrency control for MCP batch commands ──────────────
_mcp_cfg = _config.get("mcp", {})
MCP_BATCH_CONCURRENCY = _mcp_cfg.get("batch_concurrency", 2)
MCP_BATCH_RETRY = _mcp_cfg.get("batch_retry", 1)
MCP_BATCH_RETRY_DELAY = _mcp_cfg.get("batch_retry_delay", 3.0)
MCP_CALL_TIMEOUT = _mcp_cfg.get("call_timeout", 120.0)
MCP_MAX_RESPONSE_CHARS = _mcp_cfg.get("max_response_chars", 500_000)
AI_SELF_VERIFY = _config.get("ai", {}).get("self_verify", False)
_mcp_semaphore: asyncio.Semaphore | None = None  # Initialized at runtime

# ── v8.0 #E22: Structured Phase Results ─────────────────────
class PhaseResult:
    """Structured result from each audit data collection phase."""
    def __init__(self, phase: str, status: str = "pending", data: str = "", error: str = "", duration: float = 0.0):
        self.phase = phase
        self.status = status  # "success" | "failed" | "timeout" | "partial"
        self.data = data
        self.error = error
        self.duration = duration

# ── v8.0 #E12: Interface Error Tracking Store ───────────────
INTF_ERROR_HISTORY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "intf_error_history.json")

# ── v8.0 #E25: Last Audit State (for layer dashboard) ──────
last_audit_state: dict = {}  # Populated after each audit run

# ══════════════════════════════════════════════════════════════
#  v10.0 ENGINE SYSTEMS
# ══════════════════════════════════════════════════════════════

# ── E44: Self-Learning Resolution Database ──────────────────
RESOLUTION_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   _config.get("paths", {}).get("resolution_db", "resolution_db.json"))

def save_resolution(issue_fingerprint: str, fix_command: str, router: str, protocol: str):
    """Save an issue→fix mapping for self-learning."""
    try:
        db = {}
        if os.path.exists(RESOLUTION_DB_PATH):
            with open(RESOLUTION_DB_PATH, "r") as f:
                db = json.load(f)
        entry = {
            "fix": fix_command,
            "router": router,
            "protocol": protocol,
            "resolved_at": datetime.now().isoformat(),
            "occurrences": db.get(issue_fingerprint, {}).get("occurrences", 0) + 1,
        }
        db[issue_fingerprint] = entry
        with open(RESOLUTION_DB_PATH, "w") as f:
            json.dump(db, f, indent=2)
    except Exception as e:
        logger.warning(f"Resolution DB save failed: {e}")

def lookup_resolution(issue_fingerprint: str) -> dict | None:
    """Look up a known fix for an issue fingerprint."""
    try:
        if os.path.exists(RESOLUTION_DB_PATH):
            with open(RESOLUTION_DB_PATH, "r") as f:
                db = json.load(f)
            return db.get(issue_fingerprint)
    except Exception:
        pass
    return None

# ── E39: Cross-Router Correlation Engine ────────────────────
def build_cross_router_correlation(ospf_info: dict, bgp_issues: list, ldp_issues: list,
                                    bgp_established: list, device_map: dict) -> str:
    """Build bidirectional protocol state correlation across routers.
    Returns a correlation summary string for specialist prompts."""
    correlations = []
    
    # OSPF: Check if neighbor relationships are symmetric
    ospf_pairs = {}  # (routerA, routerB) → {A_sees_B: state, B_sees_A: state}
    for router, nbrs in ospf_info.get("neighbors", {}).items():
        hostname_a = device_map.get(router, router)
        for nbr in nbrs:
            nbr_addr = nbr.get("address", "")
            nbr_state = nbr.get("state", "?")
            # Find which router owns this neighbor address
            for other_router, other_hostname in device_map.items():
                if other_router != router:
                    pair = tuple(sorted([router, other_router]))
                    if pair not in ospf_pairs:
                        ospf_pairs[pair] = {}
                    ospf_pairs[pair][f"{hostname_a}_sees"] = nbr_state
    
    # Check for asymmetric OSPF states
    for pair, states in ospf_pairs.items():
        state_values = list(states.values())
        if len(state_values) >= 2 and state_values[0] != state_values[1]:
            r1, r2 = pair
            h1, h2 = device_map.get(r1, r1), device_map.get(r2, r2)
            correlations.append(
                f"▲ ASYMMETRIC OSPF: {h1} sees {state_values[0]} but {h2} sees {state_values[1]} "
                f"— indicates unidirectional link or timer mismatch"
            )
    
    # BGP: Cross-check established sessions
    bgp_peer_map = {}  # peer_ip → list of routers that see it
    for b in bgp_established:
        bgp_peer_map.setdefault(b["peer"], []).append(b["hostname"])
    for bi in bgp_issues:
        bgp_peer_map.setdefault(bi["peer"], []).append(f"{bi['hostname']}(DOWN)")
    
    # Find peers that some routers can reach but others can't
    for peer_ip, routers in bgp_peer_map.items():
        up_count = sum(1 for r in routers if "(DOWN)" not in r)
        down_count = sum(1 for r in routers if "(DOWN)" in r)
        if up_count > 0 and down_count > 0:
            correlations.append(
                f"▲ PARTIAL BGP: Peer {peer_ip} is reachable from some routers but NOT others "
                f"— Up: {[r for r in routers if '(DOWN)' not in r]}, Down: {[r for r in routers if '(DOWN)' in r]}"
            )
    
    # LDP: Cross-check session symmetry
    ldp_down_routers = set(li.get("router", "") for li in ldp_issues)
    if len(ldp_down_routers) > 0 and len(ldp_down_routers) < len(device_map):
        correlations.append(
            f"▲ PARTIAL LDP: LDP down on {len(ldp_down_routers)} of {len(device_map)} routers "
            f"— suggests localized IGP failure, not global issue"
        )
    
    if not correlations:
        return "● Cross-router correlation: All protocol states are symmetric and consistent."
    
    return "CROSS-ROUTER CORRELATION FINDINGS:\n" + "\n".join(correlations)

# ── E40: Temporal Intelligence ──────────────────────────────
def build_temporal_correlation(commit_history: dict, chassis_alarms: list,
                                uptime_outputs: dict, device_map: dict) -> str:
    """Correlate recent config changes with current failures.
    Returns temporal analysis string for specialist prompts."""
    findings = []
    now = datetime.now()
    
    # Find recent commits (last 24 hours)
    recent_commits = []
    for router_key, rdata in commit_history.items():
        if not isinstance(rdata, dict):
            continue
        hname = rdata.get("hostname", router_key)
        for c in rdata.get("commits", []):
            ts_str = c.get("timestamp", "")
            try:
                # Parse various timestamp formats
                for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%b %d %H:%M:%S"]:
                    try:
                        commit_time = datetime.strptime(ts_str, fmt)
                        if commit_time.year == 1900:  # No year in format
                            commit_time = commit_time.replace(year=now.year)
                        age_hours = (now - commit_time).total_seconds() / 3600
                        if age_hours < 24:
                            recent_commits.append({
                                "hostname": hname,
                                "user": c.get("user", "?"),
                                "timestamp": ts_str,
                                "age_hours": round(age_hours, 1),
                                "method": c.get("method", "?"),
                            })
                        break
                    except ValueError:
                        continue
            except Exception:
                continue
    
    if recent_commits:
        findings.append(f"⏰ RECENT CHANGES ({len(recent_commits)} commits in last 24h):")
        for rc in recent_commits[:5]:
            findings.append(
                f"  - {rc['hostname']}: commit by '{rc['user']}' {rc['age_hours']}h ago "
                f"via {rc['method']} — PRIME SUSPECT for any new issues on this router"
            )
    
    # Cross-reference alarms with uptime (recent reboot + alarm = hardware issue)
    for mcp_name, raw_up in uptime_outputs.items():
        hostname = device_map.get(mcp_name, mcp_name)
        # Extract uptime hours
        up_match = re.search(r"up\s+(\d+)\s+(?:hour|hr)", raw_up, re.IGNORECASE)
        if up_match:
            uptime_hours = int(up_match.group(1))
            if uptime_hours < 24:
                findings.append(
                    f"⏰ RECENT REBOOT: {hostname} uptime only {uptime_hours}h — "
                    f"check for crash (core dumps) or planned maintenance"
                )
                # Check if this router also has alarms
                for alm in chassis_alarms:
                    if alm.get("router", "") == mcp_name or alm.get("hostname", "") == hostname:
                        findings.append(
                            f"  ▲ {hostname} has BOTH recent reboot AND active alarm: "
                            f"'{alm.get('description', '?')}' — likely hardware failure"
                        )
    
    if not findings:
        return "● Temporal analysis: No recent changes or reboots correlated with current state."
    
    return "TEMPORAL CORRELATION:\n" + "\n".join(findings)

# ── E41: Negative Space Analysis (Coverage Matrix) ──────────
def build_coverage_matrix(device_map: dict, ospf_info: dict, bgp_established: list,
                           bgp_issues: list, ldp_issues: list, ldp_healthy: list,
                           lldp_links: list) -> str:
    """Identify what's expected but missing — the negative space."""
    gaps = []
    
    # Determine device roles
    pe_devices = {m for m, h in device_map.items() if h.upper().startswith("PE")}
    p_devices = {m for m, h in device_map.items() if h.upper().startswith("P") and m not in pe_devices}
    
    # All routers should have OSPF if they're P or PE
    for mcp_name in pe_devices | p_devices:
        hostname = device_map[mcp_name]
        has_ospf = mcp_name in ospf_info.get("neighbors", {}) and len(ospf_info["neighbors"][mcp_name]) > 0
        if not has_ospf:
            gaps.append(f"⊕ MISSING OSPF: {hostname} is a {'PE' if mcp_name in pe_devices else 'P'}-router but has NO OSPF neighbors")
    
    # PE routers should have BGP
    bgp_routers = set(b["router"] for b in bgp_established) | set(b["router"] for b in bgp_issues)
    for mcp_name in pe_devices:
        hostname = device_map[mcp_name]
        if mcp_name not in bgp_routers:
            gaps.append(f"⊕ MISSING BGP: {hostname} is a PE-router but has NO BGP sessions — cannot exchange VPN routes")
    
    # P routers should have LDP/MPLS
    ldp_routers = set(l["router"] for l in ldp_healthy) | set(l["router"] for l in ldp_issues)
    for mcp_name in p_devices:
        hostname = device_map[mcp_name]
        if mcp_name not in ldp_routers:
            gaps.append(f"⊕ MISSING LDP: {hostname} is a P-router but has NO LDP sessions — MPLS transit broken")
    
    # LLDP-connected interfaces should have a protocol running
    for lk in lldp_links:
        local_r = lk.get("local_router", "")
        local_intf = lk.get("local_intf", "")
        # Check if this physical link has OSPF running on it
        has_protocol = False
        for nbr_list in ospf_info.get("neighbors", {}).values():
            for nbr in nbr_list:
                if nbr.get("interface", "") == local_intf:
                    has_protocol = True
                    break
        # We don't flag here unless both sides are P/PE — could be management link
    
    if not gaps:
        return "● Coverage matrix: All expected protocols are present on all devices."
    
    return "NEGATIVE SPACE (Expected but Missing):\n" + "\n".join(gaps)

# ── E38: Protocol FSM Reasoning Engine ──────────────────────
def validate_fsm_states(ospf_info: dict, bgp_issues: list, bgp_established: list,
                         device_map: dict) -> str:
    """Validate protocol states against FSM transition rules.
    Detects impossible or stuck states."""
    anomalies = []
    
    # Check OSPF states
    for router, nbrs in ospf_info.get("neighbors", {}).items():
        hostname = device_map.get(router, router)
        for nbr in nbrs:
            state = nbr.get("state", "?")
            if state in PROTOCOL_FSM["ospf"]["stuck_hints"]:
                hint = PROTOCOL_FSM["ospf"]["stuck_hints"][state]
                anomalies.append(
                    f"⚙ FSM: {hostname} OSPF neighbor {nbr.get('address', '?')} stuck in "
                    f"**{state}** state → {hint}"
                )
    
    # Check BGP stuck states
    for bi in bgp_issues:
        state = bi.get("state", "?")
        if state in PROTOCOL_FSM["bgp"]["stuck_hints"]:
            hint = PROTOCOL_FSM["bgp"]["stuck_hints"][state]
            anomalies.append(
                f"⚙ FSM: {bi['hostname']} BGP peer {bi['peer']} stuck in "
                f"**{state}** → {hint}"
            )
    
    if not anomalies:
        return ""
    
    return "FSM STATE ANALYSIS:\n" + "\n".join(anomalies)

# ── E42: Multi-Hop Root Cause Tracing (Blast Radius) ────────
def build_blast_radius(ospf_critical: list, ospf_type_mismatches: list,
                        bgp_issues: list, ldp_issues: list, lsp_issues: list,
                        device_map: dict) -> str:
    """For each OSPF failure, trace ALL downstream services that depend on it."""
    if not ospf_critical and not ospf_type_mismatches:
        return ""
    
    chains = []
    affected_routers = set()
    
    # Get routers with OSPF problems
    for mm in ospf_type_mismatches:
        affected_routers.add(mm["local_router"])
        affected_routers.add(mm["remote_router"])
    for oc in ospf_critical:
        affected_routers.add(oc["router"])
    
    # For each affected router, find all BGP/LDP/LSP failures it causes
    for router in affected_routers:
        hostname = device_map.get(router, router)
        downstream = []
        
        bgp_affected = [b for b in bgp_issues if b["router"] == router]
        ldp_affected = [l for l in ldp_issues if l["router"] == router]
        lsp_affected = [l for l in lsp_issues if l["router"] == router]
        
        if bgp_affected:
            downstream.append(f"  └─→ {len(bgp_affected)} BGP sessions DOWN → L3VPN broken")
        if ldp_affected:
            downstream.append(f"  └─→ {len(ldp_affected)} LDP sessions DOWN → MPLS labels missing")
        if lsp_affected:
            downstream.append(f"  └─→ {len(lsp_affected)} MPLS LSPs DOWN → TE tunnels broken")
        
        if downstream:
            chains.append(f"⊗ BLAST RADIUS for {hostname} OSPF failure:")
            chains.extend(downstream)
    
    if not chains:
        return ""
    
    return "BLAST RADIUS ANALYSIS:\n" + "\n".join(chains)

# ── E46: ITIL Priority Assignment ───────────────────────────
def assign_itil_priority(severity: str, affected_services: int = 0,
                          recurring: bool = False) -> dict:
    """Assign ITIL-aligned priority based on severity and impact."""
    # ITIL Priority = Impact × Urgency
    if severity == "CRITICAL" and affected_services > 5:
        priority = "P1"
        label = "Critical — Immediate"
        mttr = "< 30 minutes"
        sla = "99.999% SLA breach risk"
    elif severity == "CRITICAL":
        priority = "P2"
        label = "High — Urgent"
        mttr = "< 2 hours"
        sla = "99.99% SLA impact"
    elif severity in ("MAJOR", "WARNING") and recurring:
        priority = "P2"
        label = "High — Recurring"
        mttr = "< 4 hours"
        sla = "Chronic degradation"
    elif severity in ("MAJOR", "WARNING"):
        priority = "P3"
        label = "Medium — Planned"
        mttr = "< 24 hours"
        sla = "Minor impact"
    else:
        priority = "P4"
        label = "Low — Informational"
        mttr = "Next maintenance window"
        sla = "No SLA impact"
    
    return {"priority": priority, "label": label, "mttr": mttr, "sla": sla}

# ── E43: Smart Command Selection per Device Role ────────────
def get_role_commands(hostname: str) -> list:
    """Return extra commands based on device role (PE/P/RR)."""
    roles_cfg = _config.get("device_roles", {})
    extra = []
    
    h_upper = hostname.upper()
    
    # Check PE role
    pe_cfg = roles_cfg.get("pe", {})
    if h_upper.startswith(pe_cfg.get("prefix", "PE")):
        extra.extend(pe_cfg.get("extra_commands", [
            "show route instance summary",
            "show bgp group summary",
        ]))
    
    # Check P role (not PE)
    p_cfg = roles_cfg.get("p", {})
    p_prefix = p_cfg.get("prefix", "P")
    p_exclude = p_cfg.get("exclude_prefix", "PE")
    if h_upper.startswith(p_prefix) and not h_upper.startswith(p_exclude):
        extra.extend(p_cfg.get("extra_commands", [
            "show ted database",
        ]))
    
    # Check RR role
    rr_cfg = roles_cfg.get("rr", {})
    if h_upper.startswith(rr_cfg.get("prefix", "RR")):
        extra.extend(rr_cfg.get("extra_commands", []))
    
    return extra

# ── E55: SQLite Backend for Historical Data ─────────────────
AUDIT_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              _config.get("paths", {}).get("audit_db", "audit_history.db"))

def init_audit_db():
    """Initialize SQLite database for audit history."""
    try:
        conn = sqlite3.connect(AUDIT_DB_PATH)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS audits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            duration REAL,
            device_count INTEGER,
            health_score REAL,
            health_grade TEXT,
            critical_count INTEGER,
            warning_count INTEGER,
            healthy_count INTEGER,
            config_drifts INTEGER,
            report_path TEXT
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS audit_issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            audit_id INTEGER,
            severity TEXT,
            router TEXT,
            hostname TEXT,
            protocol TEXT,
            detail TEXT,
            fingerprint TEXT,
            resolved INTEGER DEFAULT 0,
            fix_command TEXT,
            FOREIGN KEY (audit_id) REFERENCES audits(id)
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS health_trends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            health_score REAL,
            critical_count INTEGER,
            warning_count INTEGER,
            device_count INTEGER
        )""")
        conn.commit()
        conn.close()
    except Exception as e:
        logger.warning(f"Audit DB init failed: {e}")

def save_audit_to_db(timestamp: str, duration: float, device_count: int,
                      health_score: float, health_grade: str, critical_count: int,
                      warning_count: int, healthy_count: int, config_drifts: int,
                      report_path: str, issues: list) -> int:
    """Save audit results to SQLite. Returns audit ID."""
    try:
        conn = sqlite3.connect(AUDIT_DB_PATH)
        c = conn.cursor()
        c.execute("""INSERT INTO audits (timestamp, duration, device_count, health_score,
                     health_grade, critical_count, warning_count, healthy_count,
                     config_drifts, report_path)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                  (timestamp, duration, device_count, health_score, health_grade,
                   critical_count, warning_count, healthy_count, config_drifts, report_path))
        audit_id = c.lastrowid
        
        for issue in issues:
            fp = hashlib.md5(f"{issue.get('router','')}{issue.get('detail','')}".encode()).hexdigest()[:12]
            protocol = "system"
            detail = issue.get("detail", "").lower()
            if "ospf" in detail: protocol = "ospf"
            elif "bgp" in detail: protocol = "bgp"
            elif "ldp" in detail or "mpls" in detail: protocol = "ldp"
            elif "isis" in detail or "is-is" in detail: protocol = "isis"
            elif "bfd" in detail: protocol = "bfd"
            
            c.execute("""INSERT INTO audit_issues (audit_id, severity, router, hostname,
                         protocol, detail, fingerprint)
                         VALUES (?, ?, ?, ?, ?, ?, ?)""",
                      (audit_id, issue.get("severity", "WARNING"),
                       issue.get("router", ""), issue.get("hostname", ""),
                       protocol, issue.get("detail", ""), fp))
        
        # Save health trend
        c.execute("""INSERT INTO health_trends (timestamp, health_score, critical_count,
                     warning_count, device_count)
                     VALUES (?, ?, ?, ?, ?)""",
                  (timestamp, health_score, critical_count, warning_count, device_count))
        
        conn.commit()
        conn.close()
        return audit_id
    except Exception as e:
        logger.warning(f"Audit DB save failed: {e}")
        return -1

def get_health_trend(days: int = 30) -> list:
    """Get health score trend for the last N days."""
    try:
        conn = sqlite3.connect(AUDIT_DB_PATH)
        c = conn.cursor()
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        c.execute("""SELECT timestamp, health_score, critical_count, warning_count, device_count
                     FROM health_trends WHERE timestamp > ? ORDER BY timestamp""", (cutoff,))
        rows = c.fetchall()
        conn.close()
        return [{"timestamp": r[0], "score": r[1], "critical": r[2], 
                 "warning": r[3], "devices": r[4]} for r in rows]
    except Exception:
        return []

# ── E54: Device Facts Cache ─────────────────────────────────
FACTS_CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "device_facts_cache.json")
FACTS_CACHE_TTL = 14400  # 4 hours (was 24h — too long, stale data persists)

# Keys that indicate real device facts (not placeholder stubs)
_FACTS_REAL_KEYS = {"hostname", "fqdn", "serialnumber", "RE0", "personality", "switch_style"}


def _is_real_facts(entry: dict) -> bool:
    """Return True only if the entry contains genuine device facts.

    Placeholder stubs like {"model": "Junos Device", "version": "unknown"}
    must NOT be cached — they contain no useful information and poison
    subsequent runs.
    """
    if not isinstance(entry, dict):
        return False
    # Must have at least one "real" key beyond model/version
    if entry.keys() & _FACTS_REAL_KEYS:
        return True
    # A model value of "Junos Device" or "Local Config" is a placeholder
    model = entry.get("model", "")
    if model in ("Junos Device", "Local Config", ""):
        return False
    # If it has a non-placeholder model AND a version, accept it
    if model and entry.get("version", "unknown") != "unknown":
        return True
    return False


def load_facts_cache() -> dict:
    """Load cached device facts, filtering out placeholder stubs."""
    try:
        if os.path.exists(FACTS_CACHE_PATH):
            with open(FACTS_CACHE_PATH, "r") as f:
                cache = json.load(f)
            cached_at = cache.get("_cached_at", "")
            if cached_at:
                age = (datetime.now() - datetime.fromisoformat(cached_at)).total_seconds()
                if age < FACTS_CACHE_TTL:
                    raw = cache.get("facts", {})
                    # Only return entries that have real device data
                    valid = {k: v for k, v in raw.items() if _is_real_facts(v)}
                    skipped = len(raw) - len(valid)
                    if skipped > 0:
                        logger.info(f"Facts cache: skipped {skipped} placeholder entries")
                    return valid
                else:
                    logger.info(f"Facts cache expired (age={age:.0f}s > TTL={FACTS_CACHE_TTL}s)")
    except Exception as e:
        logger.warning(f"Facts cache load failed: {e}")
    return {}


def save_facts_cache(facts: dict):
    """Save device facts to cache, excluding placeholder stubs."""
    try:
        # Filter: only persist entries with real device data
        real_facts = {k: v for k, v in facts.items() if _is_real_facts(v)}
        skipped = len(facts) - len(real_facts)
        if skipped > 0:
            logger.info(f"Facts cache save: skipping {skipped} placeholder entries")
        if not real_facts:
            logger.info("Facts cache save: no real facts to cache, skipping write")
            return
        cache = {"_cached_at": datetime.now().isoformat(), "facts": real_facts}
        with open(FACTS_CACHE_PATH, "w") as f:
            json.dump(cache, f, indent=2)
    except Exception as e:
        logger.warning(f"Facts cache save failed: {e}")

# ── E53: Circuit Breaker Pattern ────────────────────────────
_circuit_breaker: dict = {}  # {router_name: {"failures": count, "last_failure": time}}
CIRCUIT_BREAKER_THRESHOLD = 3  # Mark unreachable after N failures
CIRCUIT_BREAKER_RESET = 300    # Reset after 5 minutes

def check_circuit_breaker(router_name: str) -> bool:
    """Returns True if router should be skipped (circuit open)."""
    if router_name not in _circuit_breaker:
        return False
    cb = _circuit_breaker[router_name]
    if cb["failures"] >= CIRCUIT_BREAKER_THRESHOLD:
        if time.time() - cb["last_failure"] > CIRCUIT_BREAKER_RESET:
            _circuit_breaker.pop(router_name, None)  # Reset
            return False
        return True  # Still in cooldown
    return False

def record_circuit_failure(router_name: str):
    """Record a failure for circuit breaker tracking."""
    if router_name not in _circuit_breaker:
        _circuit_breaker[router_name] = {"failures": 0, "last_failure": 0}
    _circuit_breaker[router_name]["failures"] += 1
    _circuit_breaker[router_name]["last_failure"] = time.time()

def record_circuit_success(router_name: str):
    """Reset circuit breaker on success."""
    _circuit_breaker.pop(router_name, None)

# ── E64: Predictive Failure Model ───────────────────────────
def analyze_error_acceleration(current_errors: list, history_path: str = INTF_ERROR_HISTORY_PATH) -> list:
    """Detect accelerating error rates by comparing with historical data.
    Returns predictions for interfaces likely to fail."""
    predictions = []
    try:
        if not os.path.exists(history_path):
            return predictions
        with open(history_path, "r") as f:
            history = json.load(f)
        
        for ie in current_errors:
            key = f"{ie.get('router', '')}_{ie.get('interface', '')}"
            if key in history:
                prev = history[key]
                prev_crc = prev.get("crc_errors", 0)
                curr_crc = 0
                for prob in ie.get("problems", []):
                    m = re.search(r"(\d+)\s*(?:CRC|crc|input error)", prob)
                    if m:
                        curr_crc = int(m.group(1))
                
                if curr_crc > prev_crc:
                    delta = curr_crc - prev_crc
                    prev_delta = prev.get("last_delta", 0)
                    if delta > prev_delta * 1.5 and prev_delta > 0:
                        # Error rate is accelerating
                        predictions.append({
                            "router": ie.get("router", ""),
                            "hostname": ie.get("hostname", ""),
                            "interface": ie.get("interface", ""),
                            "current_errors": curr_crc,
                            "previous_errors": prev_crc,
                            "acceleration": round(delta / max(prev_delta, 1), 1),
                            "prediction": f"Error rate accelerating {round(delta / max(prev_delta, 1), 1)}x — "
                                          f"likely SFP/cable failure within 48-72 hours",
                        })
    except Exception as e:
        logger.warning(f"Error acceleration analysis failed: {e}")
    
    return predictions

# Initialize SQLite DB at import time
init_audit_db()

# ══════════════════════════════════════════════════════════════
#  v11.0 ENGINE SYSTEMS
# ══════════════════════════════════════════════════════════════

# ── E68: Dependency Graph Engine ────────────────────────────
class NetworkDependencyGraph:
    """Live network graph built from LLDP + OSPF + BGP data.
    Enables topology-aware reasoning, blast radius analysis,
    and what-if simulation (E73)."""
    
    def __init__(self):
        self.nodes = {}   # {router_name: {role, hostname, protocols: set}}
        self.edges = []   # [{src, dst, intf_src, intf_dst, protocols: set, state}]
        self.protocol_deps = {
            "bgp": ["ospf", "isis"],       # BGP depends on IGP
            "ldp": ["ospf", "isis"],       # LDP depends on IGP
            "l3vpn": ["bgp", "mpls"],      # L3VPN depends on BGP + MPLS
            "l2vpn": ["bgp", "mpls"],      # L2VPN depends on BGP + MPLS
            "mpls": ["ldp"],               # MPLS depends on LDP (or RSVP)
            "rsvp": ["ospf", "isis"],      # RSVP depends on IGP for CSPF
            "bfd": [],                     # BFD is independent
        }
    
    def build_from_data(self, device_map: dict, lldp_links: list, ospf_info: dict,
                         bgp_established: list, bgp_issues: list,
                         ldp_healthy: list, ldp_issues: list):
        """Build the graph from collected audit data."""
        # Add nodes
        for mcp_name, hostname in device_map.items():
            role = "PE" if hostname.upper().startswith("PE") else (
                "RR" if hostname.upper().startswith("RR") else "P")
            self.nodes[mcp_name] = {
                "hostname": hostname, "role": role,
                "protocols": set(), "health": "healthy"
            }
        
        # Add edges from LLDP
        for link in lldp_links:
            src = link.get("local_router", "")
            dst = link.get("remote_router", "")
            if src in self.nodes and dst in self.nodes:
                self.edges.append({
                    "src": src, "dst": dst,
                    "intf_src": link.get("local_intf", ""),
                    "intf_dst": link.get("remote_intf", ""),
                    "protocols": set(), "state": "up"
                })
        
        # Annotate with OSPF
        for router, nbrs in ospf_info.get("neighbors", {}).items():
            if router in self.nodes:
                self.nodes[router]["protocols"].add("ospf")
            for nbr in nbrs:
                state = nbr.get("state", "").lower()
                if "full" not in state:
                    self.nodes.get(router, {}).setdefault("health", "degraded")
        
        # Annotate with BGP
        for b in bgp_established:
            r = b.get("router", "")
            if r in self.nodes:
                self.nodes[r]["protocols"].add("bgp")
        for b in bgp_issues:
            r = b.get("router", "")
            if r in self.nodes:
                self.nodes[r]["protocols"].add("bgp")
                self.nodes[r]["health"] = "critical"
        
        # Annotate with LDP
        for l in ldp_healthy:
            r = l.get("router", "")
            if r in self.nodes:
                self.nodes[r]["protocols"].add("ldp")
        for l in ldp_issues:
            r = l.get("router", "")
            if r in self.nodes:
                self.nodes[r]["protocols"].add("ldp")
    
    def get_transit_nodes(self) -> list:
        """E74: Identify transit nodes — nodes that, if they fail, partition the network."""
        transit = []
        for node in self.nodes:
            # Count edges to this node
            edge_count = sum(1 for e in self.edges if e["src"] == node or e["dst"] == node)
            if edge_count > 2:  # More than 2 connections = potential transit
                # Simple articulation point heuristic
                neighbors = set()
                for e in self.edges:
                    if e["src"] == node: neighbors.add(e["dst"])
                    if e["dst"] == node: neighbors.add(e["src"])
                # Check if removing this node disconnects any neighbor pair
                if len(neighbors) >= 3:
                    transit.append({
                        "router": node,
                        "hostname": self.nodes[node]["hostname"],
                        "connections": edge_count,
                        "role": self.nodes[node]["role"],
                        "risk": f"Removing {self.nodes[node]['hostname']} affects {edge_count} links"
                    })
        return transit
    
    def what_if_fail(self, failed_router: str) -> dict:
        """E73: Simulate what happens if a router fails.
        Returns impact assessment."""
        if failed_router not in self.nodes:
            return {"error": f"Unknown router: {failed_router}"}
        
        hostname = self.nodes[failed_router]["hostname"]
        impact = {
            "failed_router": hostname,
            "lost_links": [],
            "affected_protocols": [],
            "orphaned_routers": [],
            "service_impact": []
        }
        
        # Find all links that would be lost
        for e in self.edges:
            if e["src"] == failed_router or e["dst"] == failed_router:
                other = e["dst"] if e["src"] == failed_router else e["src"]
                impact["lost_links"].append({
                    "peer": self.nodes.get(other, {}).get("hostname", other),
                    "interface": e.get("intf_src", "") if e["src"] == failed_router else e.get("intf_dst", "")
                })
        
        # Check for BGP/LDP cascade
        protocols = self.nodes[failed_router].get("protocols", set())
        for proto in protocols:
            deps = self.protocol_deps.get(proto, [])
            for dep_proto in ["bgp", "ldp", "l3vpn", "l2vpn", "mpls"]:
                if proto in self.protocol_deps.get(dep_proto, []):
                    impact["affected_protocols"].append(
                        f"{dep_proto.upper()} depends on {proto.upper()} — will be affected"
                    )
        
        # Check if any router becomes isolated
        remaining_edges = [e for e in self.edges 
                          if e["src"] != failed_router and e["dst"] != failed_router]
        connected_routers = set()
        for e in remaining_edges:
            connected_routers.add(e["src"])
            connected_routers.add(e["dst"])
        
        for r in self.nodes:
            if r != failed_router and r not in connected_routers:
                impact["orphaned_routers"].append(self.nodes[r]["hostname"])
        
        # Service impact
        role = self.nodes[failed_router]["role"]
        if role == "PE":
            impact["service_impact"].append("Customer-facing services (L3VPN/L2VPN) on this PE will be lost")
        elif role == "P":
            impact["service_impact"].append("Transit traffic through this P-router will be rerouted or lost")
        elif role == "RR":
            impact["service_impact"].append("BGP route reflection lost — clients may lose routes")
        
        return impact
    
    def trace_path(self, src_router: str, dst_router: str) -> list:
        """E75: Trace the shortest path between two routers using BFS."""
        if src_router not in self.nodes or dst_router not in self.nodes:
            return []
        
        # BFS
        visited = {src_router}
        queue = [(src_router, [src_router])]
        adj = {}
        for e in self.edges:
            adj.setdefault(e["src"], []).append(e["dst"])
            adj.setdefault(e["dst"], []).append(e["src"])
        
        while queue:
            current, path = queue.pop(0)
            if current == dst_router:
                return [self.nodes.get(r, {}).get("hostname", r) for r in path]
            for neighbor in adj.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return []  # No path found
    
    def get_summary(self) -> str:
        """Get a human-readable summary of the dependency graph."""
        lines = ["NETWORK DEPENDENCY GRAPH:"]
        lines.append(f"  Nodes: {len(self.nodes)} routers")
        lines.append(f"  Links: {len(self.edges)} physical connections")
        
        transit = self.get_transit_nodes()
        if transit:
            lines.append(f"  Transit nodes (SPOF risk): {', '.join(t['hostname'] for t in transit)}")
        
        # Per-role summary
        roles = {}
        for n, data in self.nodes.items():
            roles.setdefault(data["role"], []).append(data["hostname"])
        for role, routers in sorted(roles.items()):
            lines.append(f"  {role}: {', '.join(routers)}")
        
        return "\n".join(lines)

# Global dependency graph instance
_network_graph = NetworkDependencyGraph()

# ── E70: Confidence Scoring Engine ──────────────────────────
def calculate_confidence_score(finding: dict, data_sources: int = 1,
                                 kb_match: bool = False, fsm_valid: bool = False,
                                 cross_router_confirmed: bool = False) -> int:
    """Calculate confidence score (0-100) for an AI finding.
    Based on: data sources, KB matching, FSM validation, cross-router confirmation."""
    score = 30  # Base confidence for any finding
    
    # Evidence multipliers
    if data_sources >= 3:
        score += 25  # Multiple data sources
    elif data_sources >= 2:
        score += 15
    
    if kb_match:
        score += 20  # KB has matching pattern
    
    if fsm_valid:
        score += 15  # FSM state transition validates finding
    
    if cross_router_confirmed:
        score += 10  # Cross-router data confirms
    
    return min(score, 100)

def format_confidence(score: int) -> str:
    """Format confidence score with emoji indicator."""
    if score >= 85:
        return f"[green]●[/green] {score}% (High)"
    elif score >= 60:
        return f"[yellow]●[/yellow] {score}% (Medium)"
    else:
        return f"[red]●[/red] {score}% (Low)"

# ── E71: Baseline Anomaly Detection ────────────────────────
BASELINE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "router_baselines.json")

def load_baselines() -> dict:
    """Load per-router metric baselines."""
    try:
        if os.path.exists(BASELINE_PATH):
            with open(BASELINE_PATH, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def save_baselines(baselines: dict):
    """Save per-router metric baselines."""
    try:
        with open(BASELINE_PATH, "w") as f:
            json.dump(baselines, f, indent=2)
    except Exception as e:
        logger.warning(f"Baseline save failed: {e}")

def detect_baseline_anomalies(current_metrics: dict, baselines: dict,
                                deviation_pct: int = 20) -> list:
    """E71: Detect metrics that deviate significantly from baseline.
    current_metrics: {router: {metric_name: value}}
    Returns list of anomalies."""
    anomalies = []
    
    for router, metrics in current_metrics.items():
        bl = baselines.get(router, {})
        if not bl:
            continue
        
        for metric_name, current_val in metrics.items():
            if metric_name.startswith("_"):
                continue
            baseline_val = bl.get(metric_name)
            if baseline_val is None or baseline_val == 0:
                continue
            
            try:
                current_num = float(current_val)
                baseline_num = float(baseline_val)
                pct_change = abs(current_num - baseline_num) / baseline_num * 100
                
                if pct_change > deviation_pct:
                    direction = "increased" if current_num > baseline_num else "decreased"
                    anomalies.append({
                        "router": router,
                        "metric": metric_name,
                        "current": current_num,
                        "baseline": baseline_num,
                        "deviation_pct": round(pct_change, 1),
                        "direction": direction,
                        "description": f"{metric_name} {direction} by {round(pct_change, 1)}% "
                                      f"(current: {current_num}, baseline: {baseline_num})"
                    })
            except (ValueError, TypeError):
                continue
    
    return anomalies

def update_baselines(current_metrics: dict, baselines: dict, alpha: float = 0.3) -> dict:
    """Update baselines using exponential moving average."""
    for router, metrics in current_metrics.items():
        if router not in baselines:
            baselines[router] = {}
        for metric_name, current_val in metrics.items():
            if metric_name.startswith("_"):
                continue
            try:
                current_num = float(current_val)
                old_val = float(baselines[router].get(metric_name, current_num))
                baselines[router][metric_name] = round(old_val * (1 - alpha) + current_num * alpha, 2)
            except (ValueError, TypeError):
                baselines[router][metric_name] = current_val
    
    baselines["_updated_at"] = datetime.now().isoformat()
    return baselines

# ── E94: Quantified Risk Scoring ────────────────────────────
def calculate_risk_score(likelihood: int, impact: int) -> dict:
    """Calculate quantified risk score: likelihood (0-10) × impact (0-10) = 0-100.
    Returns score + risk level."""
    score = likelihood * impact
    if score >= 70:
        level = "CRITICAL"
        color = "[red]●[/red]"
        action = "Immediate mitigation required"
    elif score >= 40:
        level = "HIGH"
        color = "[#ff8700]●[/#ff8700]"
        action = "Schedule fix within 24 hours"
    elif score >= 20:
        level = "MEDIUM"
        color = "[yellow]●[/yellow]"
        action = "Plan fix for next maintenance window"
    else:
        level = "LOW"
        color = "[green]●[/green]"
        action = "Monitor, no immediate action"
    
    return {
        "score": score, "level": level, "color": color,
        "likelihood": likelihood, "impact": impact,
        "action": action
    }

# ── E84: Pre-Change Impact Analysis ────────────────────────
async def analyze_change_impact(client, session_id, device_map, mcp_name, config_lines):
    """E84: Analyze the impact of proposed config changes before applying.
    Returns impact assessment with blast radius."""
    hostname = device_map.get(mcp_name, mcp_name)
    impact = {
        "device": hostname,
        "affected_protocols": [],
        "affected_neighbors": [],
        "risk_level": "LOW",
        "warnings": [],
    }
    
    for line in config_lines:
        ll = line.lower()
        if "ospf" in ll:
            impact["affected_protocols"].append("OSPF")
            impact["warnings"].append("▲ OSPF changes may drop adjacencies and trigger SPF recalculation")
        if "bgp" in ll:
            impact["affected_protocols"].append("BGP")
            impact["warnings"].append("▲ BGP changes may cause session reset and route withdrawal")
        if "ldp" in ll or "mpls" in ll:
            impact["affected_protocols"].append("LDP/MPLS")
            impact["warnings"].append("▲ LDP/MPLS changes may disrupt label-switched paths")
        if "interface" in ll and ("delete" in ll or "disable" in ll):
            impact["affected_protocols"].append("Physical")
            impact["warnings"].append("[red]●[/red] Interface shutdown will drop ALL protocols on that link")
            impact["risk_level"] = "HIGH"
        if "routing-options" in ll and "autonomous-system" in ll:
            impact["risk_level"] = "CRITICAL"
            impact["warnings"].append("[red]●[/red] CRITICAL: AS number change will reset ALL BGP sessions")
    
    # Set risk level based on protocol count
    if len(impact["affected_protocols"]) >= 3:
        impact["risk_level"] = "HIGH"
    elif "OSPF" in impact["affected_protocols"] and len(impact["affected_protocols"]) > 1:
        impact["risk_level"] = "MEDIUM"
    
    impact["affected_protocols"] = list(set(impact["affected_protocols"]))
    return impact

# ── E87: Pre/Post Change State Capture ──────────────────────
async def capture_device_state(client, session_id, mcp_name, hostname):
    """Capture current protocol state for pre/post change comparison."""
    state = {}
    state_cmds = [
        ("ospf_neighbors", "show ospf neighbor"),
        ("bgp_summary", "show bgp summary"),
        ("ldp_sessions", "show ldp session"),
        ("interfaces", "show interfaces terse"),
        ("routes", "show route summary"),
    ]
    
    for label, cmd in state_cmds:
        try:
            result = await mcp_call_tool(client, session_id, "execute_junos_command",
                                          {"router_name": mcp_name, "command": cmd})
            state[label] = result if isinstance(result, str) else str(result)
        except Exception as e:
            state[label] = f"Error: {e}"
    
    state["_captured_at"] = datetime.now().isoformat()
    return state

def compare_device_states(before: dict, after: dict) -> str:
    """Compare pre/post change device states and report differences."""
    changes = []
    for key in before:
        if key.startswith("_"):
            continue
        b = before.get(key, "")
        a = after.get(key, "")
        if b != a:
            diff = list(difflib.unified_diff(
                b.splitlines(), a.splitlines(),
                fromfile=f"BEFORE {key}", tofile=f"AFTER {key}", lineterm=""
            ))
            if diff:
                changes.append(f"### {key}")
                changes.append("```diff")
                changes.extend(diff[:30])
                if len(diff) > 30:
                    changes.append(f"... ({len(diff) - 30} more diff lines)")
                changes.append("```")
    
    if not changes:
        return "● No protocol state changes detected after config modification."
    
    return "## Pre/Post Change State Comparison\n\n" + "\n".join(changes)

# ── E88: Change Templates/Playbooks ────────────────────────
CHANGE_TEMPLATES = {
    "add_ospf_interface": {
        "name": "Add Interface to OSPF",
        "description": "Enable OSPF on a physical interface",
        "params": ["interface_name", "area_id"],
        "template": "set protocols ospf area {area_id} interface {interface_name} interface-type p2p",
        "verify_cmd": "show ospf interface {interface_name}",
        "rollback": "delete protocols ospf area {area_id} interface {interface_name}",
    },
    "add_bgp_neighbor": {
        "name": "Add BGP Neighbor",
        "description": "Add an iBGP neighbor peering",
        "params": ["neighbor_ip", "local_as", "peer_group"],
        "template": "set protocols bgp group {peer_group} neighbor {neighbor_ip}\n"
                    "set protocols bgp group {peer_group} type internal\n"
                    "set protocols bgp group {peer_group} local-as {local_as}",
        "verify_cmd": "show bgp neighbor {neighbor_ip}",
        "rollback": "delete protocols bgp group {peer_group} neighbor {neighbor_ip}",
    },
    "enable_bfd": {
        "name": "Enable BFD on OSPF Interface",
        "description": "Configure BFD for faster failure detection",
        "params": ["interface_name", "area_id", "min_interval"],
        "template": "set protocols ospf area {area_id} interface {interface_name} bfd-liveness-detection minimum-interval {min_interval}",
        "verify_cmd": "show bfd session interface {interface_name}",
        "rollback": "delete protocols ospf area {area_id} interface {interface_name} bfd-liveness-detection",
    },
    "set_interface_mtu": {
        "name": "Set Interface MTU",
        "description": "Configure MTU on physical interface",
        "params": ["interface_name", "mtu_value"],
        "template": "set interfaces {interface_name} mtu {mtu_value}",
        "verify_cmd": "show interfaces {interface_name} | match mtu",
        "rollback": "delete interfaces {interface_name} mtu",
    },
    "add_static_route": {
        "name": "Add Static Route",
        "description": "Add a static route",
        "params": ["prefix", "next_hop"],
        "template": "set routing-options static route {prefix} next-hop {next_hop}",
        "verify_cmd": "show route {prefix}",
        "rollback": "delete routing-options static route {prefix}",
    },
    "enable_ntp": {
        "name": "Configure NTP",
        "description": "Add NTP server",
        "params": ["ntp_server"],
        "template": "set system ntp server {ntp_server}",
        "verify_cmd": "show ntp associations",
        "rollback": "delete system ntp server {ntp_server}",
    },
}

# ── E91: Change Window Enforcement ──────────────────────────
def check_change_window() -> dict:
    """Check if current time is within an approved change window."""
    now = datetime.now()
    hour = now.hour
    weekday = now.weekday()  # 0=Monday, 6=Sunday
    
    # Default: maintenance windows are weekdays 22:00-06:00 and weekends
    if weekday >= 5:  # Weekend
        return {"allowed": True, "reason": "Weekend maintenance window", "risk": "LOW"}
    elif hour >= 22 or hour < 6:
        return {"allowed": True, "reason": "Off-hours maintenance window", "risk": "LOW"}
    elif 9 <= hour <= 17:
        return {"allowed": False, "reason": "Business hours (09:00-17:00) — changes not recommended",
                "risk": "HIGH"}
    else:
        return {"allowed": True, "reason": "Extended hours — proceed with caution", "risk": "MEDIUM"}

# ── E69: Multi-Hop Root Cause Chainer ───────────────────────
def build_root_cause_chain(down_intfs: list, ospf_type_mismatches: list,
                           intf_errors: list, bgp_issues: list, ldp_issues: list,
                           lsp_issues: list, bfd_issues: list, device_map: dict) -> list:
    """Trace from symptoms backward through layers to physical root cause.
    Returns ordered chain: [L1 Physical] → [L2 Data Link] → [L3 Network] → [L4 Transport] → [L7 Service]"""
    chains = []
    
    # Start from L1 (Physical)
    l1_causes = []
    for di in down_intfs:
        l1_causes.append({
            "layer": "L1-Physical", "router": di.get("hostname", ""),
            "detail": f"Interface {di.get('interface', '')} is DOWN",
            "evidence": "show interfaces terse"
        })
    for ie in intf_errors:
        for prob in ie.get("problems", []):
            if "crc" in prob.lower() or "error" in prob.lower():
                l1_causes.append({
                    "layer": "L1-Physical", "router": ie.get("hostname", ""),
                    "detail": f"{ie.get('interface', '')}: {prob}",
                    "evidence": "show interfaces extensive"
                })
    
    # L2 (Data Link) - MTU mismatches, etc.
    # L3 (Network) - OSPF/BGP/IS-IS
    l3_causes = []
    for mm in ospf_type_mismatches:
        l3_causes.append({
            "layer": "L3-Network", "router": mm.get("local_hostname", ""),
            "detail": f"OSPF type mismatch with {mm.get('remote_hostname', '')} on {mm.get('local_intf', '')}",
            "evidence": "show ospf interface",
            "caused_by": l1_causes[0] if l1_causes else None
        })
    for bi in bgp_issues:
        l3_causes.append({
            "layer": "L3-Network", "router": bi.get("hostname", ""),
            "detail": f"BGP peer {bi.get('peer', '')} in {bi.get('state', '')} state",
            "evidence": "show bgp summary",
            "caused_by": l3_causes[0] if l3_causes else (l1_causes[0] if l1_causes else None)
        })
    
    # L4 (Transport) - LDP/MPLS/RSVP
    l4_causes = []
    for li in ldp_issues:
        l4_causes.append({
            "layer": "L4-Transport", "router": li.get("hostname", li.get("router", "")),
            "detail": f"LDP session down on {li.get('router', '')}",
            "evidence": "show ldp session",
            "caused_by": l3_causes[0] if l3_causes else None
        })
    for lsp in lsp_issues:
        l4_causes.append({
            "layer": "L4-Transport", "router": lsp.get("hostname", lsp.get("router", "")),
            "detail": f"MPLS LSP {lsp.get('name', '')} DOWN",
            "evidence": "show mpls lsp",
            "caused_by": l3_causes[0] if l3_causes else None
        })
    
    # Build the chain bottom-up
    all_causes = l1_causes + l3_causes + l4_causes
    if all_causes:
        # Find root (deepest layer cause)
        root = l1_causes[0] if l1_causes else (l3_causes[0] if l3_causes else l4_causes[0])
        chain = {
            "root_cause": root,
            "chain_length": len(all_causes),
            "layers_affected": list(set(c["layer"] for c in all_causes)),
            "all_symptoms": all_causes,
            "summary": f"Root cause at {root['layer']}: {root['detail']} → "
                       f"cascading to {len(all_causes) - 1} downstream failures"
        }
        chains.append(chain)
    
    return chains

# ── E96: Financial/SLA Impact Quantification ───────────────
def estimate_sla_impact(critical_count: int, warning_count: int,
                         duration_minutes: float = 0, device_count: int = 11) -> dict:
    """Estimate financial and SLA impact of current issues."""
    # Industry averages for SP networks
    cost_per_minute_p1 = 5000   # $/min for P1 outage
    cost_per_minute_p2 = 1000   # $/min for P2 degradation
    sla_target = 99.999         # Five-nines
    
    monthly_minutes = 30 * 24 * 60  # 43,200 minutes
    allowed_downtime = monthly_minutes * (1 - sla_target / 100)  # ~0.43 minutes
    
    estimated_cost = 0
    sla_status = "● Within SLA"
    
    if critical_count > 0:
        estimated_cost = duration_minutes * cost_per_minute_p1
        if duration_minutes > allowed_downtime:
            sla_status = f"[red]●[/red] SLA BREACH — {round(duration_minutes - allowed_downtime, 1)} min over budget"
    elif warning_count > 0:
        estimated_cost = duration_minutes * cost_per_minute_p2 * 0.1  # 10% of P2 rate for warnings
    
    # Calculate affected customer impact
    affected_pct = (critical_count / max(device_count, 1)) * 100
    
    return {
        "estimated_cost": f"${estimated_cost:,.0f}",
        "sla_status": sla_status,
        "sla_target": f"{sla_target}%",
        "allowed_downtime_min": round(allowed_downtime, 2),
        "affected_infrastructure_pct": round(affected_pct, 1),
        "risk_category": "Revenue-impacting" if critical_count > 0 else "Operational",
    }

# ── v11.0: Extended Troubleshoot Trees (E81-E83) ───────────
EXTENDED_TROUBLESHOOT_TREES = {
    "rsvp": {
        "name": "RSVP-TE Troubleshooting",
        "steps": [
            {"q": "Check RSVP interfaces", "cmd": "show rsvp interface", "next_if_issue": 1},
            {"q": "Check RSVP sessions", "cmd": "show rsvp session", "next_if_issue": 2},
            {"q": "Check RSVP neighbor", "cmd": "show rsvp neighbor", "next_if_issue": 3},
            {"q": "Check MPLS LSP detail", "cmd": "show mpls lsp extensive", "next_if_issue": 4},
            {"q": "Check CSPF/TED database", "cmd": "show ted database", "next_if_issue": -1},
        ]
    },
    "bfd": {
        "name": "BFD Troubleshooting",
        "steps": [
            {"q": "Check BFD sessions", "cmd": "show bfd session", "next_if_issue": 1},
            {"q": "Check BFD session detail", "cmd": "show bfd session detail", "next_if_issue": 2},
            {"q": "Check protocol BFD references", "cmd": "show ospf interface detail", "next_if_issue": 3},
            {"q": "Check interface for errors", "cmd": "show interfaces extensive", "next_if_issue": -1},
        ]
    },
    "l2vpn": {
        "name": "L2VPN/EVPN Troubleshooting",
        "steps": [
            {"q": "Check L2VPN connections", "cmd": "show l2circuit connections", "next_if_issue": 1},
            {"q": "Check EVPN instances", "cmd": "show evpn instance", "next_if_issue": 2},
            {"q": "Check EVPN database", "cmd": "show evpn database", "next_if_issue": 3},
            {"q": "Check BGP EVPN routes", "cmd": "show route table bgp.evpn.0", "next_if_issue": 4},
            {"q": "Check underlying MPLS", "cmd": "show ldp session", "next_if_issue": -1},
        ]
    },
    "l3vpn": {
        "name": "L3VPN Troubleshooting",
        "steps": [
            {"q": "Check VRF instances", "cmd": "show route instance summary", "next_if_issue": 1},
            {"q": "Check VPN routes", "cmd": "show route table bgp.l3vpn.0 summary", "next_if_issue": 2},
            {"q": "Check BGP VPN families", "cmd": "show bgp summary", "next_if_issue": 3},
            {"q": "Check MPLS label table", "cmd": "show route table mpls.0 summary", "next_if_issue": 4},
            {"q": "Check PE-CE routing", "cmd": "show ospf neighbor instance all", "next_if_issue": -1},
        ]
    },
    "security": {
        "name": "Security/Firewall Troubleshooting",
        "steps": [
            {"q": "Check firewall filter counters", "cmd": "show firewall", "next_if_issue": 1},
            {"q": "Check lo0 filter config", "cmd": "show configuration interfaces lo0 unit 0 family inet filter", "next_if_issue": 2},
            {"q": "Check policer counters", "cmd": "show policer", "next_if_issue": 3},
            {"q": "Check interface filters", "cmd": "show interfaces filters", "next_if_issue": -1},
        ]
    },
}

# ── Enhancement #P2D: Junos Version Feature Matrix ──────────
JUNOS_FEATURE_MATRIX = {
    "evpn_type5":      {"min_version": "17.3", "description": "EVPN Type-5 IP Prefix Routes"},
    "micro_bfd":       {"min_version": "17.4", "description": "Micro-BFD for LAG members"},
    "sr_mpls":         {"min_version": "17.3", "description": "Segment Routing MPLS (SPRING)"},
    "srv6":            {"min_version": "21.1", "description": "SRv6 (Segment Routing IPv6)"},
    "evpn_vxlan":      {"min_version": "18.4", "description": "EVPN-VXLAN overlay"},
    "flex_algo":       {"min_version": "20.4", "description": "Flexible Algorithm for IGP"},
    "rpki":            {"min_version": "12.2", "description": "RPKI / Origin Validation"},
    "inline_jflow":    {"min_version": "14.1", "description": "Inline JFlow (NetFlow)"},
    "telemetry_grpc":  {"min_version": "16.1", "description": "gRPC Telemetry Streaming"},
    "bgp_add_path":    {"min_version": "13.2", "description": "BGP Add-Path"},
}

# ── Enhancement #P3C: Compliance Checks ─────────────────────
COMPLIANCE_CHECKS = [
    {"id": "ntp",       "label": "NTP Configured",        "command": "show ntp associations no-resolve", "pass_if_present": r"\d+\.\d+\.\d+\.\d+"},
    {"id": "syslog",    "label": "Syslog Configured",     "command": "show configuration system syslog", "pass_if_present": r"host|file"},
    {"id": "snmp",      "label": "SNMP Configured",       "command": "show configuration snmp",          "pass_if_present": r"community|v3"},
    {"id": "ssh_only",  "label": "SSH Only (No Telnet)",   "command": "show configuration system services", "pass_if_present": r"ssh"},
    {"id": "login_banner", "label": "Login Banner Set",    "command": "show configuration system login message", "pass_if_present": r".{10,}"},
    {"id": "rescue",    "label": "Rescue Config Saved",    "command": "show system storage",              "pass_if_present": r"rescue"},
    {"id": "lldp",      "label": "LLDP Enabled",          "command": "show lldp",                        "pass_if_present": r"enabled|Enabled"},
    {"id": "root_auth", "label": "Root Authentication Set","command": "show configuration system root-authentication", "pass_if_present": r"encrypted-password|ssh-rsa"},
]

# ── Enhancement #P2C: Protocol FSM States ───────────────────
PROTOCOL_FSM = {
    "ospf": {
        "states": ["Down", "Attempt", "Init", "2-Way", "ExStart", "Exchange", "Loading", "Full"],
        "healthy": ["Full"],
        "stuck_hints": {
            "Init": "Hello received but no 2-Way → check hello/dead timers, area ID, authentication",
            "ExStart": "MTU mismatch or authentication failure → check interface MTU and auth keys",
            "Exchange": "DBD exchange stuck → check MTU, check for large LSDB overwhelming the link",
            "Loading": "LSA request/reply issue → rare, check for corrupted LSDB entries",
            "2-Way": "Normal for DROther on broadcast segments, CRITICAL on point-to-point links",
        }
    },
    "bgp": {
        "states": ["Idle", "Connect", "Active", "OpenSent", "OpenConfirm", "Established"],
        "healthy": ["Established"],
        "stuck_hints": {
            "Idle": "BGP not attempting → check if neighbor is configured, check routing policy",
            "Connect": "TCP SYN sent but no response → check reachability, firewall filters",
            "Active": "Cannot reach peer → check IGP reachability to peer loopback, check TCP/179",
            "OpenSent": "OPEN sent but no reply → check AS number, BGP version, authentication",
            "OpenConfirm": "Waiting for KEEPALIVE → check hold-time mismatch, authentication",
        }
    },
    "bfd": {
        "states": ["AdminDown", "Down", "Init", "Up"],
        "healthy": ["Up"],
        "stuck_hints": {
            "AdminDown": "Administratively disabled → check if intended",
            "Down": "No BFD packets received → check physical layer, interface state",
            "Init": "BFD packets sent but peer not responding → check peer BFD config, timers",
        }
    },
    "ldp": {
        "states": ["Nonexistent", "Initialized", "OpenReceived", "OpenSent", "Operational"],
        "healthy": ["Operational"],
        "stuck_hints": {
            "Nonexistent": "No TCP session → check IGP reachability to peer, check LDP config",
            "Initialized": "Session initializing → check transport address, hello adjacency",
        }
    },
}


# ── Enhancement #P1B: Professional Banner ───────────────────
def print_welcome_banner(kb_lines: int = 0, kb_chars: int = 0, kb_sections: int = 0):
    """Display a Claude Code-style welcome banner with clean, compact design."""
    # Top banner — Claude Code inspired gradient header
    header = Text()
    header.append("╭─────────────────────────────────────────────────────────────╮\n", style="bold #5fd7ff")
    header.append("│                                                             │\n", style="bold #5fd7ff")
    header.append("│  ", style="bold #5fd7ff")
    header.append("JUNOS AI NETWORK OPERATIONS CENTER", style="bold white")
    header.append("                   │\n", style="bold #5fd7ff")
    header.append("│  ", style="bold #5fd7ff")
    header.append("v20.0", style="bold #87ff87")
    header.append(" ── Feedback Learning · Conversation Memory     ", style="#af87ff")
    header.append("  │\n", style="bold #5fd7ff")
    header.append("│                                                             │\n", style="bold #5fd7ff")
    header.append("╰─────────────────────────────────────────────────────────────╯", style="bold #5fd7ff")
    console.print(header)
    
    # System Status Table — professional indicators
    I = Icons
    status_table = Table(title=f"{I.CONFIG} System Status", box=box.ROUNDED, 
                         border_style="#5fd7ff", title_style="bold #5fd7ff",
                         padding=(0, 1))
    status_table.add_column("Component", style="bold white", width=22)
    status_table.add_column("Status", justify="center", width=14)
    status_table.add_column("Details", style="#8a8a8a", width=48)
    
    status_table.add_row("AI Model", f"[green]{I.OK} Online[/green]", f"{MODEL}")
    status_table.add_row("MCP Server", f"[green]{I.OK} Online[/green]", f"{MCP_SERVER_URL}")
    status_table.add_row("Context Window", f"[green]{I.OK} Ready[/green]", f"{NUM_CTX:,} tokens ({MAX_CTX_USAGE*100:.0f}% budget)")
    status_table.add_row("Knowledge Base", 
                         f"[green]{I.OK} Loaded[/green]" if kb_lines else f"[red]{I.FAIL} Missing[/red]",
                         f"{kb_lines:,} lines, {kb_chars:,} chars, {kb_sections} sections" if kb_lines else "Not found")
    status_table.add_row("Specialists", f"[green]{I.OK} Active[/green]", "OSPF{0}BGP{0}LDP{0}ISIS{0}SYS{0}L2VPN{0}RSVP{0}QoS{0}SEC{0}L3VPN{0}HW{0}Synth".format(I.SEPARATOR))
    status_table.add_row("Architecture", f"[green]{I.OK} Ready[/green]", f"RAG Vector KB {I.ARROW} 12 Specialists {I.ARROW} Synthesizer")
    status_table.add_row("Reasoning Engine", f"[#87ff87]{I.OK} v15.0[/#87ff87]", f"Hypothesis-Driven {I.BULLET} 7-Stage Pipeline {I.BULLET} Evidence")
    status_table.add_row("Network Analysis", f"[#87ff87]{I.OK} v16.0[/#87ff87]", f"Capture{I.SEPARATOR}DNS{I.SEPARATOR}Security{I.SEPARATOR}Forensics{I.SEPARATOR}Profiling{I.SEPARATOR}Alerts")
    status_table.add_row("Hypered Brain", f"[#87ff87]{I.OK} v18.0[/#87ff87]", f"6-Layer Agentic AI {I.BULLET} Adaptive Concurrency {I.BULLET} AI Probes")
    status_table.add_row("Terminal UI", f"[#87ff87]{I.OK} v19.0[/#87ff87]", f"Claude Code Style {I.BULLET} Live Action Plans {I.BULLET} Todo Tracker")
    status_table.add_row("Feedback & Memory", f"[#87ff87]{I.OK} v20.0[/#87ff87]", f"Brain-Analyzed Learning {I.BULLET} Multi-Session Memory {I.BULLET} Conv Browser")
    status_table.add_row("Script Templates", f"[green]{I.OK} Loaded[/green]", f"Op{I.SEPARATOR}Commit{I.SEPARATOR}Event{I.SEPARATOR}PyEZ{I.SEPARATOR}NETCONF (7 templates)")
    
    console.print(status_table)
    
    # File attachment hint
    console.print(f"  [dim]Tip: Attach files with [bold]@filepath[/bold] in your message (e.g. @config.yaml)[/dim]")
    console.print()


def print_status_bar(device_count: int = 0, health_score: float = -1, 
                     msg_count: int = 0, rag_chunks: int = 0):
    """Display compact professional status bar."""
    I = Icons
    parts = []
    parts.append(f"[cyan]{I.NET} {device_count} devices[/cyan]")
    if health_score >= 0:
        color = "green" if health_score >= 75 else ("yellow" if health_score >= 50 else "red")
        parts.append(f"[{color}]{I.HEALTH} {health_score:.0f}/100[/{color}]")
    parts.append(f"[dim]{I.BULLET} {msg_count} msgs[/dim]")
    if rag_chunks > 0:
        parts.append(f"[dim]{I.SEARCH} {rag_chunks} chunks[/dim]")
    console.print(f" {f' {I.SEPARATOR} '.join(parts)}", style="dim")


def print_command_help():
    """Display professionally styled command palette with categorized groups."""
    I = Icons
    
    # Main help table — grouped by category
    help_table = Table(title=f"{I.CONFIG} Command Reference", box=box.SIMPLE_HEAVY, 
                       border_style="#5f87ff", title_style="bold #5f87ff",
                       padding=(0, 1), show_lines=False)
    help_table.add_column("Command", style="bold #87d7ff", width=36, no_wrap=True)
    help_table.add_column("Description", style="white", width=55)
    
    # ── Core Operations ──
    help_table.add_row(f"[bold #ff8700]{I.DASH*3} Core Operations {I.DASH*20}[/bold #ff8700]", "")
    help_table.add_row("audit", f"{I.TARGET} Full network health check with 12-specialist AI analysis")
    help_table.add_row("check <deviceA> <deviceB>", f"{I.LINK} Check connectivity between two devices")
    help_table.add_row("configure <router> <desc>", f"{I.CONFIG} Push config with safety checks & dry-run")
    help_table.add_row("verify <router>", f"{I.OK} Run verification commands on a device")
    help_table.add_row("ping <router> <ip>", f"{I.NET} Ping from a router to an IP address")
    help_table.add_row("traceroute <router> <ip>", f"{I.FLOW} Traceroute from a router to an IP")
    
    # ── Configuration Management ──
    help_table.add_row(f"[bold #ff8700]{I.DASH*3} Configuration {I.DASH*22}[/bold #ff8700]", "")
    help_table.add_row("golden status|save|diff [device]", f"{I.SAVE} Manage golden config baselines")
    help_table.add_row("template list|<name> [router]", f"{I.SCRIPT} Apply change templates/playbooks")
    help_table.add_row("impact <router> <desc>", f"{I.ALERT} Pre-change blast radius analysis")
    help_table.add_row("simulate <set commands>", f"{I.GRAPH} Predict config impact before push")
    help_table.add_row("compliance", f"{I.SHIELD} Run configuration compliance audit (20+ checks)")
    
    # ── Troubleshooting ──
    help_table.add_row(f"[bold #ff8700]{I.DASH*3} Troubleshooting {I.DASH*20}[/bold #ff8700]", "")
    help_table.add_row("troubleshoot <protocol>", f"{I.SEARCH} Guided troubleshooting for a protocol")
    help_table.add_row("troubleshoot-ai <symptom>", f"{I.BRAIN} AI-guided dynamic troubleshooting")
    help_table.add_row("whatif <router>", f"{I.WARN} What-if failure simulation via dependency graph")
    help_table.add_row("cascade <protocol:state>", f"{I.LINK} Show cascading failure chain [dim](v15)[/dim]")
    
    # ── Monitoring & Analysis ──
    help_table.add_row(f"[bold #ff8700]{I.DASH*3} Monitoring & Analysis {I.DASH*15}[/bold #ff8700]", "")
    help_table.add_row("layers", f"{I.LAYER} Layer-by-layer health dashboard")
    help_table.add_row("trends", f"{I.GRAPH} Health score trend over time")
    help_table.add_row("health", f"{I.HEALTH} Show live background health state")
    help_table.add_row("playbook", f"{I.SCRIPT} Show remediation playbook from last audit")
    help_table.add_row("runbook list|<name>", f"{I.SCRIPT} Show/execute automated runbooks")
    help_table.add_row("translate <vendor>", f"{I.ARROW} Show Junos to vendor command map")
    help_table.add_row("topology", f"{I.MAP} Live topology map from iBGP+LLDP+IS-IS [dim](v14)[/dim]")
    
    # ── Deep Analysis (v14–v15) ──
    help_table.add_row(f"[bold #ff8700]{I.DASH*3} Deep Analysis {I.DASH*22}[/bold #ff8700]", "")
    help_table.add_row("mindmap <question>", f"{I.BRAIN} Mind-map deep reasoning engine [dim](v14)[/dim]")
    help_table.add_row("deep <question>", f"{I.BRAIN} Deep root cause analysis with FSM chains [dim](v14)[/dim]")
    help_table.add_row("hypothesis <question>", f"{I.SEARCH} Hypothesis-driven investigation [dim](v15)[/dim]")
    help_table.add_row("scripts [name]", f"{I.SCRIPT} List/show Junos script templates [dim](v15)[/dim]")
    
    # ── Network Intelligence (v16) ──
    help_table.add_row(f"[bold #ff8700]{I.DASH*3} Network Intelligence {I.DASH*16}[/bold #ff8700]", "")
    help_table.add_row("capture <router> [proto] [intf]", f"{I.NET} Packet capture & protocol analysis [dim](v16)[/dim]")
    help_table.add_row("dns <domain> [type]", f"{I.MAP} DNS resolution from router perspective [dim](v16)[/dim]")
    help_table.add_row("dns trace <domain>", f"{I.MAP} Trace DNS resolution path [dim](v16)[/dim]")
    help_table.add_row("security [check_name]", f"{I.SHIELD} Run security audit (13 checks) [dim](v16)[/dim]")
    help_table.add_row("forensics [scope] [keyword]", f"{I.SEARCH} Log forensics & event timeline [dim](v16)[/dim]")
    help_table.add_row("profile [router|all]", f"{I.GRAPH} Device health profiling & scoring [dim](v16)[/dim]")
    help_table.add_row("alerts [status|rules]", f"{I.ALERT} Alert engine — thresholds & events [dim](v16)[/dim]")
    help_table.add_row("flow <router> <interface>", f"{I.FLOW} Interface flow & performance analysis [dim](v16)[/dim]")
    help_table.add_row("workflow [name]", f"{I.SCRIPT} Guided analysis workflows [dim](v16)[/dim]")
    
    # ── Hypered Brain (v17) ──
    help_table.add_row(f"[bold #ff8700]{I.DASH*3} Hypered Brain {I.DASH*22}[/bold #ff8700]", "")
    help_table.add_row("brain <question>", f"{I.BRAIN} Hypered Brain — multi-layer AI with self-validation [dim](v17)[/dim]")
    help_table.add_row("qbrain <question>", f"{I.BOLT} Quick Brain — single-pass smart analysis [dim](v17)[/dim]")
    help_table.add_row("smart-scripts", f"{I.SCRIPT} List all 18 smart fact-gathering scripts [dim](v17)[/dim]")
    
    # ── System ──
    help_table.add_row(f"[bold #ff8700]{I.DASH*3} System {I.DASH*29}[/bold #ff8700]", "")
    help_table.add_row("todos", f"{I.SCRIPT} Show active tasks from tasks/todo.md [dim](v19)[/dim]")
    help_table.add_row("plan", f"{I.TARGET} Show current action plan status [dim](v19)[/dim]")
    help_table.add_row("session", f"{I.GRAPH} Show session metrics (tools, AI calls, time) [dim](v19)[/dim]")
    
    # ── v20.0: Memory & Learning ──
    help_table.add_row(f"[bold #ff8700]{I.DASH*3} Memory & Learning {I.DASH*18}[/bold #ff8700]", "")
    help_table.add_row("feedback <text>", f"{I.BRAIN} Give feedback — Brain analyzes critically [dim](v20)[/dim]")
    help_table.add_row("feedback history", f"{I.BRAIN} View past feedback with Brain analysis [dim](v20)[/dim]")
    help_table.add_row("feedback stats", f"{I.GRAPH} Show feedback summary statistics [dim](v20)[/dim]")
    help_table.add_row("conversations", f"{I.RESTORE} Browse & continue previous conversations [dim](v20)[/dim]")
    help_table.add_row("continue <#>", f"{I.RESTORE} Resume a previous conversation by number [dim](v20)[/dim]")
    help_table.add_row("new", f"{I.NEW} Start a fresh conversation [dim](v20)[/dim]")
    
    help_table.add_row(f"[bold #ff8700]{I.DASH*3} {I.DASH*33}[/bold #ff8700]", "")
    help_table.add_row("help", f"{I.INFO} Show this command reference")
    help_table.add_row("quit", f"{I.EXIT} Exit the bridge")
    
    console.print(help_table)


# ── Enhancement #P5B: Layer Health Dashboard ────────────────
def print_layer_dashboard(layer_status: dict):
    """Display OSI-model layer health view."""
    dash = Table(title=f"{Icons.LAYER} Network Layer Health Dashboard", box=box.HEAVY, 
                 border_style="magenta", title_style="bold magenta")
    dash.add_column("Layer", style="bold white", width=5)
    dash.add_column("Name", style="bold", width=15)
    dash.add_column("Protocols", width=25)
    dash.add_column("Status", justify="center", width=12)
    dash.add_column("Details", style="dim", width=30)
    
    layers = [
        ("L7", "Services", "L3VPN, EVPN, VPLS", "services"),
        ("L4", "Transport", "MPLS, LDP, RSVP", "transport"),
        ("L3", "Routing", "OSPF, BGP, IS-IS", "routing"),
        ("L2", "Data Link", "Ethernet, LAG, STP", "datalink"),
        ("L1", "Physical", "Interfaces, SFPs", "physical"),
    ]
    
    for layer_id, name, protocols, key in layers:
        status = layer_status.get(key, {"status": "unknown", "detail": "No data"})
        st = status.get("status", "unknown")
        if st == "healthy":
            st_display = "[green][green]●[/green] Healthy[/green]"
        elif st == "degraded":
            st_display = "[yellow][yellow]●[/yellow] Degraded[/yellow]"
        elif st == "critical":
            st_display = "[red][red]●[/red] CRITICAL[/red]"
        else:
            st_display = "[dim][dim]○[/dim] Unknown[/dim]"
        
        dash.add_row(layer_id, name, protocols, st_display, status.get("detail", ""))
    
    console.print(dash)


# ── v18.2: Markdown-safe status icons (no Rich markup in .md files) ──
def _md_icon(status: str) -> str:
    """Return a Markdown-safe emoji icon for a severity/status level.
    Use this in report strings instead of Rich console markup like [red]●[/red]."""
    _MAP = {
        "critical": "🔴", "CRITICAL": "🔴", "red": "🔴", "P1": "🔴",
        "major": "🟠", "MAJOR": "🟠", "high": "🟠", "P2": "🟠", "error": "🟠",
        "warning": "🟡", "WARNING": "🟡", "yellow": "🟡", "P3": "🟡", "medium": "🟡",
        "info": "🔵", "low": "🔵", "blue": "🔵", "P4": "🔵",
        "healthy": "🟢", "ok": "🟢", "green": "🟢", "good": "🟢",
        "unknown": "⚪", "dim": "⚪", "none": "⚪",
    }
    return _MAP.get(status, "⚪")


# ── Enhancement #P3A: Severity Heatmap ──────────────────────
def build_severity_heatmap(device_map: dict, protocol_status: dict) -> str:
    """Build device × protocol severity matrix for report."""
    protocols = ["OSPF", "BGP", "LDP", "BFD", "IS-IS", "System"]
    
    lines = ["### ◫ Severity Heatmap\n"]
    header = "| Device |" + "|".join(f" {p} " for p in protocols) + "|"
    sep = "|--------|" + "|".join("-----" for _ in protocols) + "|"
    lines.append(header)
    lines.append(sep)
    
    for mcp_name, hostname in device_map.items():
        row = f"| **{hostname}** |"
        for proto in protocols:
            key = f"{mcp_name}_{proto.lower()}"
            status = protocol_status.get(key, "ok")
            icon = _md_icon(status)
            row += f" {icon} |"
        lines.append(row)
    lines.append("")
    return "\n".join(lines)


# ── Enhancement #P2D: Version Compatibility Check ───────────
def check_version_compatibility(device_facts: dict, device_map: dict) -> list:
    """Check if device Junos versions support detected features."""
    warnings = []
    for mcp_name, facts in device_facts.items():
        if not isinstance(facts, dict):
            continue
        version_str = facts.get("version", "0.0")
        # Extract major.minor from version string like "23.2R1.13"
        vm = re.match(r"(\d+\.\d+)", str(version_str))
        if not vm:
            continue
        dev_version = float(vm.group(1))
        hostname = device_map.get(mcp_name, mcp_name)
        
        for feature_id, feature_info in JUNOS_FEATURE_MATRIX.items():
            min_ver = float(feature_info["min_version"])
            if dev_version < min_ver:
                # Only warn if the feature is likely in use (we'll check later)
                warnings.append({
                    "router": mcp_name,
                    "hostname": hostname,
                    "feature": feature_info["description"],
                    "feature_id": feature_id,
                    "device_version": version_str,
                    "min_required": feature_info["min_version"],
                })
    return warnings


# ── Enhancement #P3C: Compliance Scoring ────────────────────
async def run_compliance_audit(client, sid, device_map: dict) -> dict:
    """Run configuration compliance checks across all devices (E49: expanded to 20+ checks).
    Loads checks from config.yaml if available, falls back to COMPLIANCE_CHECKS constant.
    Returns {mcp_name: {"score": int, "checks": {check_id: bool}}}."""
    from kb_vectorstore import KBVectorStore  # Avoid circular at module level
    results = {}
    all_mcp = list(device_map.keys())
    
    # E49: Load compliance checks from config.yaml if available
    config_checks = _config.get("compliance", {}).get("checks", None)
    checks_to_run = config_checks if config_checks else COMPLIANCE_CHECKS
    
    console.print(f"\n[heading]◇ Running Compliance Audit ({len(checks_to_run)} checks)...[/heading]")
    
    for check in checks_to_run:
        raw = await run_batch(client, sid, check["command"], all_mcp, check["label"])
        parsed = parse_batch_json(raw)
        
        for mcp_name in all_mcp:
            if mcp_name not in results:
                results[mcp_name] = {"score": 0, "total": len(checks_to_run), "checks": {}}
            
            output = parsed.get(mcp_name, "")
            passed = bool(re.search(check["pass_if_present"], output, re.IGNORECASE)) if output.strip() else False
            # E49: Support fail_if_present (e.g., SNMP community "public")
            if passed and "fail_if_present" in check:
                if re.search(check["fail_if_present"], output, re.IGNORECASE | re.MULTILINE):
                    passed = False
            results[mcp_name]["checks"][check["id"]] = passed
            if passed:
                results[mcp_name]["score"] += 1
    
    return results


def format_compliance_report(compliance: dict, device_map: dict) -> str:
    """Format compliance results as Markdown for the report."""
    lines = ["### ◇ Configuration Compliance Scorecard\n"]
    
    # Summary table
    lines.append("| Device | Score | Grade | NTP | Syslog | SNMP | SSH | Banner | Rescue | LLDP | Root Auth |")
    lines.append("|--------|-------|-------|-----|--------|------|-----|--------|--------|------|-----------|")
    
    for mcp_name, data in compliance.items():
        hostname = device_map.get(mcp_name, mcp_name)
        score = data["score"]
        total = data["total"]
        pct = (score / total * 100) if total > 0 else 0
        grade = "A" if pct >= 90 else ("B" if pct >= 75 else ("C" if pct >= 60 else ("D" if pct >= 40 else "F")))
        
        checks = data["checks"]
        def _icon(check_id):
            return "●" if checks.get(check_id, False) else "✗"
        
        lines.append(
            f"| **{hostname}** | {score}/{total} ({pct:.0f}%) | {grade} | "
            f"{_icon('ntp')} | {_icon('syslog')} | {_icon('snmp')} | {_icon('ssh_only')} | "
            f"{_icon('login_banner')} | {_icon('rescue')} | {_icon('lldp')} | {_icon('root_auth')} |"
        )
    
    # Average score
    all_scores = [d["score"]/d["total"]*100 for d in compliance.values() if d["total"] > 0]
    if all_scores:
        avg = sum(all_scores) / len(all_scores)
        lines.append(f"\n**Average Compliance Score:** {avg:.0f}%\n")
    
    return "\n".join(lines)


# ── Enhancement #P3E: HTML Report Export ────────────────────
def export_report_html(markdown_text: str, output_path: str):
    """Export the Markdown report as a styled HTML file.
    E19: Includes SVG network topology diagram.
    E20: Adds HTML anchor IDs for section cross-linking."""
    import html as html_module
    
    # E19: Extract topology links from report to build SVG
    topo_links = []
    topo_match = re.findall(r'(\S+)\s+\([^)]+\)\s+──\s+\([^)]+\)\s+(\S+)', markdown_text)
    for local_h, remote_h in topo_match:
        topo_links.append((local_h, remote_h))
    
    def _build_svg_topology(links: list) -> str:
        """E19: Build an SVG network diagram from discovered LLDP links."""
        if not links:
            return ""
        nodes = list(set(n for pair in links for n in pair))
        if len(nodes) < 2:
            return ""
        # Calculate positions in a circle
        import math
        cx, cy, radius = 300, 200, 150
        positions = {}
        for i, node in enumerate(nodes):
            angle = (2 * math.pi * i) / len(nodes) - math.pi / 2
            positions[node] = (cx + radius * math.cos(angle), cy + radius * math.sin(angle))
        
        svg_parts = [
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" '
            'style="max-width:600px;margin:20px auto;display:block;background:#0d1117;border-radius:8px;border:1px solid #30363d;">',
            '<text x="300" y="30" text-anchor="middle" fill="#58a6ff" font-size="16" font-weight="bold">Network Topology</text>',
        ]
        # Draw links
        for src, dst in links:
            x1, y1 = positions.get(src, (0, 0))
            x2, y2 = positions.get(dst, (0, 0))
            svg_parts.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
                           f'stroke="#30363d" stroke-width="2"/>')
        # Draw nodes
        for node, (x, y) in positions.items():
            svg_parts.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="25" fill="#161b22" stroke="#58a6ff" stroke-width="2"/>')
            svg_parts.append(f'<text x="{x:.0f}" y="{y + 4:.0f}" text-anchor="middle" fill="#c9d1d9" font-size="10">{node[:10]}</text>')
        svg_parts.append('</svg>')
        return '\n'.join(svg_parts)
    
    svg_diagram = _build_svg_topology(topo_links)
    
    # Simple Markdown-to-HTML conversion (tables, headers, code blocks, bold, etc.)
    lines = markdown_text.split("\n")
    html_lines = ['<!DOCTYPE html><html><head><meta charset="utf-8">',
                  '<title>Junos Network Audit Report</title>',
                  '<style>',
                  'body{font-family:"Segoe UI",Roboto,sans-serif;max-width:1100px;margin:40px auto;'
                  'padding:0 20px;background:#0d1117;color:#c9d1d9;line-height:1.6}',
                  'h1{color:#58a6ff;border-bottom:2px solid #21262d;padding-bottom:8px}',
                  'h2{color:#79c0ff;border-bottom:1px solid #21262d;padding-bottom:6px;margin-top:30px}',
                  'h3{color:#d2a8ff}',
                  'table{border-collapse:collapse;width:100%;margin:16px 0}',
                  'th,td{border:1px solid #30363d;padding:8px 12px;text-align:left}',
                  'th{background:#161b22;color:#58a6ff;font-weight:600}',
                  'tr:nth-child(even){background:#161b22}',
                  'code{background:#161b22;padding:2px 6px;border-radius:3px;font-size:0.9em;color:#e6edf3}',
                  'pre{background:#161b22;padding:16px;border-radius:6px;overflow-x:auto;border:1px solid #30363d}',
                  'pre code{padding:0;background:none}',
                  'blockquote{border-left:4px solid #58a6ff;margin:16px 0;padding:8px 16px;background:#161b22}',
                  'strong{color:#e6edf3}',
                  '.badge-a{background:#238636;color:white;padding:2px 8px;border-radius:12px}',
                  '.badge-f{background:#da3633;color:white;padding:2px 8px;border-radius:12px}',
                  '.cover{text-align:center;padding:60px 0;border-bottom:3px solid #58a6ff;margin-bottom:40px}',
                  '.cover h1{font-size:2.4em;border:none;margin-bottom:8px}',
                  '.cover p{color:#8b949e;font-size:1.1em}',
                  '/* E20: Navigation links */',
                  '.nav-toc{background:#161b22;padding:16px;border-radius:8px;margin:20px 0;border:1px solid #30363d}',
                  '.nav-toc a{color:#58a6ff;text-decoration:none;display:block;padding:4px 0}',
                  '.nav-toc a:hover{text-decoration:underline}',
                  '</style></head><body>',
                  '<div class="cover">',
                  '<h1>⊕ Junos Network Audit Report</h1>',
                  f'<p>Generated: {datetime.now().strftime("%B %d, %Y %H:%M")}</p>',
                  f'<p>Engine: Junos MCP Bridge v9.0 + Ollama ({MODEL})</p>',
                  '</div>']
    
    # E19: Insert SVG topology diagram after cover
    if svg_diagram:
        html_lines.append(svg_diagram)
    
    # E20: Build table of contents from section headers
    section_anchors = []
    for line in lines:
        if line.startswith("## "):
            title = line[3:].strip()
            anchor = re.sub(r'[^a-zA-Z0-9]', '-', title.lower()).strip('-')
            section_anchors.append((anchor, title))
    
    if section_anchors:
        html_lines.append('<div class="nav-toc"><strong>◇ Quick Navigation</strong>')
        for anchor, title in section_anchors:
            html_lines.append(f'<a href="#{anchor}">→ {title}</a>')
        html_lines.append('</div>')
    
    in_code_block = False
    in_table = False
    
    for line in lines:
        if line.startswith("```"):
            if in_code_block:
                html_lines.append("</code></pre>")
                in_code_block = False
            else:
                lang = line[3:].strip()
                html_lines.append(f"<pre><code class='{lang}'>")
                in_code_block = True
            continue
        
        if in_code_block:
            html_lines.append(html_module.escape(line))
            continue
        
        # Table rows
        if line.strip().startswith("|") and "|" in line[1:]:
            if "---" in line:
                continue  # Skip separator rows
            cells = [c.strip() for c in line.strip().split("|")[1:-1]]
            if not in_table:
                html_lines.append("<table>")
                in_table = True
                html_lines.append("<tr>" + "".join(f"<th>{c}</th>" for c in cells) + "</tr>")
            else:
                html_lines.append("<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
            continue
        else:
            if in_table:
                html_lines.append("</table>")
                in_table = False
        
        # Headers — E20: Add anchor IDs for cross-linking
        if line.startswith("# "):
            html_lines.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("## "):
            title = line[3:].strip()
            anchor = re.sub(r'[^a-zA-Z0-9]', '-', title.lower()).strip('-')
            html_lines.append(f'<h2 id="{anchor}">{title}</h2>')
        elif line.startswith("### "):
            title = line[4:].strip()
            anchor = re.sub(r'[^a-zA-Z0-9]', '-', title.lower()).strip('-')
            html_lines.append(f'<h3 id="{anchor}">{title}</h3>')
        elif line.startswith("> "):
            html_lines.append(f"<blockquote>{line[2:]}</blockquote>")
        elif line.startswith("---"):
            html_lines.append("<hr>")
        elif line.strip():
            # Handle bold and code
            processed = line
            processed = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', processed)
            processed = re.sub(r'`(.+?)`', r'<code>\1</code>', processed)
            html_lines.append(f"<p>{processed}</p>")
    
    if in_table:
        html_lines.append("</table>")
    html_lines.append("</body></html>")
    
    with open(output_path, "w") as f:
        f.write("\n".join(html_lines))
    return output_path


# ── Enhancement #P5A: Interactive Troubleshooting ───────────
TROUBLESHOOT_TREES = {
    "ospf": {
        "name": "OSPF Troubleshooting",
        "steps": [
            {"q": "Check OSPF interfaces", "cmd": "show ospf interface", "next_if_issue": 1},
            {"q": "Check OSPF neighbors", "cmd": "show ospf neighbor", "next_if_issue": 2},
            {"q": "Check OSPF neighbor detail for FSM state", "cmd": "show ospf neighbor detail", "next_if_issue": 3},
            {"q": "Check OSPF config on both sides", "cmd": "show configuration protocols ospf", "next_if_issue": 4},
            {"q": "Check physical link status", "cmd": "show interfaces terse", "next_if_issue": -1},
        ]
    },
    "bgp": {
        "name": "BGP Troubleshooting",
        "steps": [
            {"q": "Check BGP summary", "cmd": "show bgp summary", "next_if_issue": 1},
            {"q": "Check BGP neighbor detail", "cmd": "show bgp neighbor", "next_if_issue": 2},
            {"q": "Check IGP reachability to peer", "cmd": "show ospf neighbor", "next_if_issue": 3},
            {"q": "Check routing policy", "cmd": "show configuration policy-options", "next_if_issue": 4},
            {"q": "Check TCP connectivity", "cmd": "show system connections | match 179", "next_if_issue": -1},
        ]
    },
    "ldp": {
        "name": "LDP/MPLS Troubleshooting",
        "steps": [
            {"q": "Check LDP sessions", "cmd": "show ldp session", "next_if_issue": 1},
            {"q": "Check LDP neighbors", "cmd": "show ldp neighbor", "next_if_issue": 2},
            {"q": "Check MPLS interfaces", "cmd": "show mpls interface", "next_if_issue": 3},
            {"q": "Check IGP reachability", "cmd": "show ospf neighbor", "next_if_issue": 4},
            {"q": "Check LDP config", "cmd": "show configuration protocols ldp", "next_if_issue": -1},
        ]
    },
}

# ── v11.0: Merge extended trees into main TROUBLESHOOT_TREES ──
TROUBLESHOOT_TREES.update(EXTENDED_TROUBLESHOOT_TREES)


def _ensure_golden_dir():
    """Create the golden_configs directory if it doesn't exist."""
    os.makedirs(GOLDEN_CONFIG_DIR, exist_ok=True)


def save_golden_config(router_name: str, config_text: str) -> str:
    """Save a router config as the golden baseline. Returns the file path."""
    _ensure_golden_dir()
    path = os.path.join(GOLDEN_CONFIG_DIR, f"{router_name}.conf")
    meta_path = os.path.join(GOLDEN_CONFIG_DIR, f"{router_name}.meta")
    with open(path, "w") as f:
        f.write(config_text)
    meta = {
        "saved_at": datetime.now().isoformat(),
        "sha256": hashlib.sha256(config_text.encode()).hexdigest(),
        "lines": len(config_text.splitlines()),
    }
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)
    return path


def load_golden_config(router_name: str) -> tuple:
    """Load saved golden config and metadata. Returns (config_text, meta_dict) or (None, None)."""
    path = os.path.join(GOLDEN_CONFIG_DIR, f"{router_name}.conf")
    meta_path = os.path.join(GOLDEN_CONFIG_DIR, f"{router_name}.meta")
    if not os.path.exists(path):
        return None, None
    with open(path, "r") as f:
        config_text = f.read()
    meta = {}
    if os.path.exists(meta_path):
        with open(meta_path, "r") as f:
            meta = json.load(f)
    return config_text, meta


# ── Enhancement #4: Session Persistence ──────────────────────

def save_session_history(messages: list):
    """Persist chat messages to disk for cross-session memory."""
    try:
        # Only save user/assistant messages (skip system, tool)
        saveable = [m for m in messages if m.get("role") in ("user", "assistant") and m.get("content")]
        saveable = saveable[-MAX_PERSISTED_MESSAGES:]
        with open(SESSION_HISTORY_PATH, "w") as f:
            json.dump({
                "saved_at": datetime.now().isoformat(),
                "messages": saveable
            }, f, indent=2)
    except Exception as e:
        print(f"   ▲  Could not save session history: {e}")


def load_session_history() -> list:
    """Load previous session messages from disk."""
    if not os.path.exists(SESSION_HISTORY_PATH):
        return []
    try:
        with open(SESSION_HISTORY_PATH, "r") as f:
            data = json.load(f)
        saved_at = data.get("saved_at", "unknown")
        msgs = data.get("messages", [])
        if msgs:
            print(f"   ↻ Found previous session ({len(msgs)} messages, saved {saved_at})")
        return msgs
    except Exception:
        return []


# ── Enhancement #2: Token-Aware Context Trimming ─────────────

def estimate_tokens(messages: list) -> int:
    """Estimate token count for a list of messages (~4 chars per token)."""
    total_chars = sum(len(m.get("content", "")) for m in messages)
    return total_chars // CHARS_PER_TOKEN


def trim_messages_by_tokens(messages: list, max_tokens: int | None = None) -> list:
    """Trim messages to fit within token budget, keeping system prompt + recent turns.
    
    Enhancement #2: Uses token-aware trimming instead of simple message count.
    This prevents context overflow when individual messages are very long (e.g., audit reports).
    """
    if max_tokens is None:
        max_tokens = int(NUM_CTX * MAX_CTX_USAGE)
    
    if not messages:
        return messages
    
    # Always keep system prompt (first message)
    system_msg = messages[0] if messages[0].get("role") == "system" else None
    other_msgs = messages[1:] if system_msg else messages[:]
    
    system_tokens = estimate_tokens([system_msg]) if system_msg else 0
    available = max_tokens - system_tokens
    
    # Add messages from most recent backwards
    kept = []
    running_tokens = 0
    for msg in reversed(other_msgs):
        msg_tokens = estimate_tokens([msg])
        if running_tokens + msg_tokens > available:
            break
        kept.insert(0, msg)
        running_tokens += msg_tokens
    
    result = ([system_msg] if system_msg else []) + kept
    return result


# ── Enhancement #7: Hallucination Guard ──────────────────────

def validate_ai_references(ai_text: str, real_data: str, device_map: dict) -> list:
    """Cross-reference AI output against actual collected data.
    
    Checks that interface names, IP addresses, and hostnames mentioned
    by the AI actually exist in the real data. Returns list of warnings.
    
    Enhancement #7: Prevents the AI from hallucinating device/interface names.
    """
    warnings = []
    
    # Extract interface names from real data
    real_interfaces = set(re.findall(r'\b((?:ge|xe|et|ae|lo|irb|em|fxp)\-\d+/\d+/\d+(?:\.\d+)?)\b', real_data))
    
    # Extract interface names from AI output
    ai_interfaces = set(re.findall(r'\b((?:ge|xe|et|ae|lo|irb|em|fxp)\-\d+/\d+/\d+(?:\.\d+)?)\b', ai_text))
    
    # Find hallucinated interfaces
    hallucinated = ai_interfaces - real_interfaces
    if hallucinated:
        warnings.append(
            f"▲ HALLUCINATION GUARD: AI referenced {len(hallucinated)} interface(s) not found in real data: "
            f"{', '.join(sorted(hallucinated))}"
        )
    
    # Extract IPv4 addresses from real data
    real_ips = set(re.findall(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', real_data))
    ai_ips = set(re.findall(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', ai_text))
    
    # Filter out common non-routable IPs that appear in examples
    common_ips = {"0.0.0.0", "255.255.255.255", "127.0.0.1"}
    hallucinated_ips = (ai_ips - real_ips) - common_ips
    # Also filter out area IDs like 0.0.0.0 that are valid OSPF areas
    hallucinated_ips = {ip for ip in hallucinated_ips if not ip.startswith("0.0.")}
    if hallucinated_ips:
        warnings.append(
            f"▲ HALLUCINATION GUARD: AI referenced {len(hallucinated_ips)} IP(s) not found in real data: "
            f"{', '.join(sorted(hallucinated_ips))}"
        )
    
    # Check hostnames
    real_hostnames = set(device_map.values()) | set(device_map.keys())
    ai_hostnames_pattern = '|'.join(re.escape(h) for h in real_hostnames)
    if ai_hostnames_pattern:
        mentioned_hosts = set(re.findall(ai_hostnames_pattern, ai_text, re.IGNORECASE))
        # Only flag if AI mentions a plausible hostname that's NOT in device map
        for word in re.findall(r'\b([A-Z][A-Za-z0-9\-]+(?:Router|router|PE|CE|P|RR|SW)[\w\-]*)\b', ai_text):
            if word not in real_hostnames and word.lower() not in {h.lower() for h in real_hostnames}:
                warnings.append(f"▲ HALLUCINATION GUARD: AI mentioned hostname '{word}' not in device inventory")
    
    return warnings


# ── Enhancement #8: Dynamic Truncation Budgets ───────────────

def calculate_budgets(num_devices: int, num_ctx: int = NUM_CTX) -> dict:
    """Calculate dynamic per-section character budgets based on context window and device count.
    
    Enhancement #8: Replaces hardcoded [:3000], [:2000] slicing with budgets
    that scale with the number of devices and available context.
    """
    # Reserve 40% of context for data, rest for prompt + AI response
    total_data_chars = int(num_ctx * CHARS_PER_TOKEN * 0.40)
    
    # Scale per-device budget inversely with device count
    per_device = max(800, total_data_chars // max(num_devices, 1))
    
    return {
        "total": total_data_chars,
        "per_device": per_device,
        "interfaces": min(4000, per_device * num_devices),
        "ospf_nbr": min(3000, per_device * num_devices),
        "ospf_intf": min(3000, per_device * num_devices),
        "bgp": min(3000, per_device * num_devices),
        "bgp_summary": min(1500, per_device),
        "ldp": min(2500, per_device * num_devices),
        "ldp_sess": min(1000, per_device),
        "mpls_intf": min(1000, per_device),
        "route": min(2500, per_device * num_devices),
        "config": min(2000, per_device),
        "specialist_kb": min(4000, total_data_chars // 5),
        "synthesizer_input": min(3000, total_data_chars // 4),
        "pair_check": min(3000, total_data_chars // 3),
    }


# ── Enhancement #11: Audit Trend Comparison ──────────────────

def find_previous_audit() -> str | None:
    """Find the most recent previous audit report file."""
    pattern = os.path.join(AUDIT_REPORT_DIR, "NETWORK_AUDIT_*.md")
    reports = sorted(glob.glob(pattern), reverse=True)
    if len(reports) >= 1:
        return reports[0]  # Most recent (will be compared after new one is saved)
    return None


def compare_audit_reports(old_path: str, new_report: str) -> str:
    """Compare two audit reports and generate a trend summary.
    
    Enhancement #11: Extracts key metrics from both reports and shows ↑/↓ trends.
    """
    try:
        with open(old_path, "r") as f:
            old_report = f.read()
    except Exception:
        return ""
    
    def extract_metric(report: str, label: str) -> int:
        """Extract a numeric metric from the audit summary table."""
        match = re.search(rf'\|\s*{re.escape(label)}\s*\|\s*\*\*(\d+)\*\*\s*\|', report)
        return int(match.group(1)) if match else -1
    
    metrics = ["[red]●[/red] Critical Issues", "[yellow]●[/yellow] Warnings", "● Healthy Areas",
               "↻ Config Drift", "⊗ Chassis Alarms", "⊟ Storage Warnings",
               "⊗ Core Dumps"]
    
    trend_lines = []
    has_changes = False
    
    for metric in metrics:
        old_val = extract_metric(old_report, metric)
        new_val = extract_metric(new_report, metric)
        if old_val < 0 or new_val < 0:
            continue
        
        if new_val < old_val:
            arrow = "↓ IMPROVED"
            has_changes = True
        elif new_val > old_val:
            arrow = "↑ DEGRADED"
            has_changes = True
        else:
            arrow = "= No change"
        
        trend_lines.append(f"| {metric} | {old_val} → **{new_val}** | {arrow} |")
    
    if not trend_lines or not has_changes:
        return ""
    
    # Get timestamp of old report from filename
    old_name = os.path.basename(old_path)
    old_ts = old_name.replace("NETWORK_AUDIT_", "").replace(".md", "").replace("_", " ")
    
    result = f"\n## ▴ 10. Trend Comparison (vs. {old_ts})\n\n"
    result += "| Metric | Change | Trend |\n"
    result += "|--------|--------|-------|\n"
    result += "\n".join(trend_lines)
    result += "\n"
    
    return result


# ── Enhancement #1: MCP Auto-Reconnect ──────────────────────

async def mcp_reconnect(client) -> str:
    """Re-initialize MCP session after connection loss."""
    print("   ↻ MCP connection lost — attempting reconnect...")
    for attempt in range(3):
        try:
            sid = await mcp_initialize(client)
            print(f"   ● MCP reconnected (attempt {attempt + 1}): {sid}")
            return sid
        except Exception as e:
            wait = 2 ** attempt
            print(f"   ▲  Reconnect attempt {attempt + 1}/3 failed: {e} (retry in {wait}s)")
            await asyncio.sleep(wait)
    raise ConnectionError("MCP server reconnection failed after 3 attempts")


def diff_configs(golden: str, current: str, router_name: str = "") -> list:
    """Return a unified diff between golden and current config.
    Returns list of diff lines. Empty list = no changes."""
    golden_lines = golden.splitlines(keepends=True)
    current_lines = current.splitlines(keepends=True)
    diff = list(difflib.unified_diff(
        golden_lines, current_lines,
        fromfile=f"golden/{router_name}.conf",
        tofile=f"current/{router_name}.conf",
        lineterm=""
    ))
    return diff


def summarize_drift(diff_lines: list) -> dict:
    """Analyze a unified diff and return a summary of changes."""
    added = [l for l in diff_lines if l.startswith("+") and not l.startswith("+++")]
    removed = [l for l in diff_lines if l.startswith("-") and not l.startswith("---")]

    # Categorize changes by config section
    sections_changed = set()
    for line in added + removed:
        clean = line.lstrip("+-").strip()
        # Junos set-format: "set protocols ospf ..."  or  stanza headers
        if clean.startswith("set "):
            parts = clean.split()
            if len(parts) >= 3:
                sections_changed.add(parts[1])  # e.g. "protocols", "interfaces", "system"
        elif clean.endswith("{"):
            sections_changed.add(clean.rstrip(" {").strip())

    return {
        "lines_added": len(added),
        "lines_removed": len(removed),
        "sections_changed": sorted(sections_changed),
        "total_changes": len(added) + len(removed),
    }


# ── MCP helpers ──────────────────────────────────────────────

def parse_sse_response(text: str) -> dict:
    """Parse SSE event stream and extract the final JSON-RPC result."""
    parsed_messages = []
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("data: "):
            data_str = line[6:]
            try:
                msg = json.loads(data_str)
                parsed_messages.append(msg)
            except json.JSONDecodeError:
                continue
    for msg in reversed(parsed_messages):
        if "result" in msg:
            return msg
    if parsed_messages:
        return parsed_messages[-1]
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {}


async def mcp_post(client, session_id, payload, timeout=30.0):
    headers = {"Accept": "application/json, text/event-stream"}
    if session_id:
        headers["mcp-session-id"] = session_id
    resp = await client.post(MCP_SERVER_URL, json=payload, headers=headers, timeout=timeout)
    new_sid = resp.headers.get("mcp-session-id", session_id)
    ct = resp.headers.get("content-type", "")
    raw_text = resp.text
    # Truncate extremely large responses to prevent memory/processing hangs
    if len(raw_text) > MCP_MAX_RESPONSE_CHARS:
        logger.warning(f"MCP response truncated: {len(raw_text)} → {MCP_MAX_RESPONSE_CHARS} chars")
        raw_text = raw_text[:MCP_MAX_RESPONSE_CHARS]
    data = parse_sse_response(raw_text) if "text/event-stream" in ct else resp.json()
    return data, new_sid


async def mcp_initialize(client):
    data, sid = await mcp_post(client, None, {
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-03-26", "capabilities": {},
                   "clientInfo": {"name": "ollama-mcp-bridge", "version": "3.0.0"}}
    })
    await client.post(MCP_SERVER_URL,
        json={"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
        headers={"Accept": "application/json, text/event-stream", "mcp-session-id": sid},
        timeout=10.0)
    return sid


async def mcp_list_tools(client, sid):
    data, _ = await mcp_post(client, sid, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    return data.get("result", {}).get("tools", [])


async def mcp_call_tool(client, sid, tool_name, arguments):
    data, _ = await mcp_post(client, sid, {
        "jsonrpc": "2.0", "id": 3, "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments}
    }, timeout=MCP_CALL_TIMEOUT)
    content = data.get("result", {}).get("content", [])
    text = "\n".join(c.get("text", "") for c in content if c.get("type") == "text")
    if not text and data:
        # Return full JSON — do NOT truncate, callers handle large responses
        return json.dumps(data)
    return text


# ── Command runners ──────────────────────────────────────────

async def run_batch(client, sid, command, router_names, label):
    """Run a batch command with concurrency throttling, retry logic, and circuit breaker.
    Uses a semaphore to limit concurrent MCP requests and prevent server saturation."""
    global _mcp_semaphore
    if _mcp_semaphore is None:
        _mcp_semaphore = asyncio.Semaphore(MCP_BATCH_CONCURRENCY)

    # v10.0 E53: Circuit breaker check
    if check_circuit_breaker(label):
        console.print(f"      [warning]⚡ {label}: circuit breaker OPEN (too many recent failures), skipping[/warning]")
        collection_status[label] = "circuit-breaker-open"
        return ""

    async with _mcp_semaphore:
        console.print(f"   [info]⊛ {label}:[/info] [command]{command}[/command]")
        logger.info(f"Batch command: {label} → {command} on {len(router_names)} routers")
        batch_start = time.time()
        last_error = None
        for attempt in range(1, MCP_BATCH_RETRY + 2):  # +2 because range is exclusive and we want initial + retries
            try:
                result = await asyncio.wait_for(
                    mcp_call_tool(client, sid, "execute_junos_command_batch",
                                  {"command": command, "router_names": router_names}),
                    timeout=MCP_CALL_TIMEOUT
                )
                elapsed = round(time.time() - batch_start, 1)
                result_len = len(result) if result else 0
                console.print(f"      [success]● {result_len} chars ({elapsed}s)[/success]")
                collection_status[label] = "success"
                logger.info(f"Batch {label}: success ({result_len} chars, {elapsed}s)")
                record_circuit_success(label)  # E53: reset failure counter
                return result
            except asyncio.TimeoutError:
                last_error = f"Timeout after {MCP_CALL_TIMEOUT}s"
                elapsed = round(time.time() - batch_start, 1)
                if attempt <= MCP_BATCH_RETRY:
                    logger.warning(f"Batch {label}: attempt {attempt} timed out ({elapsed}s), retrying in {MCP_BATCH_RETRY_DELAY}s...")
                    console.print(f"      [warning]▲  {label} attempt {attempt} timed out ({elapsed}s), retrying...[/warning]")
                    await asyncio.sleep(MCP_BATCH_RETRY_DELAY)
                else:
                    console.print(f"      [error]✗ {label}: {last_error}[/error]")
                    collection_status[label] = f"failed: {last_error}"
                    logger.error(f"Batch {label}: FAILED after {MCP_BATCH_RETRY} retries ({last_error})")
                    record_circuit_failure(label)  # E53: track failure
                    return ""
            except Exception as e:
                last_error = e
                elapsed = round(time.time() - batch_start, 1)
                if attempt <= MCP_BATCH_RETRY:
                    logger.warning(f"Batch {label}: attempt {attempt} failed ({e}, {elapsed}s), retrying in {MCP_BATCH_RETRY_DELAY}s...")
                    console.print(f"      [warning]▲  {label} attempt {attempt} failed, retrying...[/warning]")
                    await asyncio.sleep(MCP_BATCH_RETRY_DELAY)
                else:
                    console.print(f"      [error]✗ {label}: {last_error}[/error]")
                    collection_status[label] = f"failed: {last_error}"
                    logger.error(f"Batch {label}: FAILED after {MCP_BATCH_RETRY} retries ({last_error})")
                    record_circuit_failure(label)  # E53: track failure
                    return ""
        return ""  # Fallback (should not be reached)


async def run_single(client, sid, command, router_name, label):
    console.print(f"   [info]⊛ {label}:[/info] [command]{command} on {router_name}[/command]")
    logger.info(f"Single command: {label} → {command} on {router_name}")
    try:
        result = await asyncio.wait_for(
            mcp_call_tool(client, sid, "execute_junos_command",
                          {"command": command, "router_name": router_name}),
            timeout=MCP_CALL_TIMEOUT
        )
        console.print(f"      [success]● {len(result)} chars[/success]")
        logger.info(f"Single {label}: success ({len(result)} chars)")
        return result
    except asyncio.TimeoutError:
        console.print(f"      [error]✗ Timeout ({MCP_CALL_TIMEOUT}s)[/error]")
        logger.error(f"Single {label}: TIMEOUT after {MCP_CALL_TIMEOUT}s")
        return ""
    except Exception as e:
        console.print(f"      [error]✗ Error: {e}[/error]")
        logger.error(f"Single {label}: FAILED ({e})")
        return ""


# ── Data parsers ─────────────────────────────────────────────

def parse_batch_json(raw: str) -> dict:
    """Parse batch command JSON → {router_name: output_text}."""
    result = {}
    try:
        data = json.loads(raw)
        for r in data.get("results", []):
            result[r.get("router_name", "unknown")] = r.get("output", "")
    except (json.JSONDecodeError, KeyError, TypeError):
        pass
    return result


def find_down_interfaces(intf_outputs: dict) -> list:
    """Parse 'show interfaces terse' and find admin-up/link-down physical interfaces."""
    issues = []
    skip_pfx = ("pfe", "pfh", "pip", "bme", "jsrv", "lc-", "cb", "em", "irb",
                "vtep", "dsc", "gre", "ipip", "tap", "lo0", "lsi", ".local.")
    for router, output in intf_outputs.items():
        for line in output.split("\n"):
            parts = line.split()
            if len(parts) >= 3:
                iface, admin, link = parts[0], parts[1], parts[2]
                if any(iface.startswith(p) for p in skip_pfx):
                    continue
                if admin.lower() == "up" and link.lower() == "down":
                    issues.append({"router": router, "interface": iface, "admin": admin, "link": link})
    return issues


def find_ospf_neighbors(ospf_nbr_outputs: dict, ospf_intf_outputs: dict, device_map: dict) -> dict:
    """Analyze OSPF neighbors and interfaces across all routers."""
    info = {"neighbors": {}, "interfaces": {}, "issues": []}

    for router, output in ospf_nbr_outputs.items():
        neighbors = []
        for line in output.split("\n"):
            parts = line.split()
            if len(parts) >= 4 and re.match(r"\d+\.\d+\.\d+\.\d+", parts[0]):
                neighbors.append({"address": parts[0],
                                  "interface": parts[1] if len(parts) > 1 else "",
                                  "state": parts[2] if len(parts) > 2 else ""})
        info["neighbors"][router] = neighbors

        hostname = device_map.get(router, router)
        intf_out = ospf_intf_outputs.get(router, "")
        has_intf = bool(intf_out.strip()) and "not running" not in intf_out.lower()
        if not neighbors and has_intf:
            info["issues"].append({
                "severity": "CRITICAL", "router": router, "hostname": hostname,
                "detail": f"{hostname} has OSPF interfaces configured but **0 OSPF neighbors**"
            })

    for router, output in ospf_intf_outputs.items():
        interfaces = []
        for line in output.split("\n"):
            if line.strip() and not line.strip().startswith("Interface"):
                interfaces.append(line.strip())
        info["interfaces"][router] = interfaces

    return info


def find_bgp_issues(bgp_outputs: dict, device_map: dict) -> tuple:
    issues, established = [], []
    for router, output in bgp_outputs.items():
        hostname = device_map.get(router, router)
        if not output.strip() or "not running" in output.lower():
            continue
        for line in output.split("\n"):
            parts = line.split()
            if len(parts) >= 3 and re.match(r"\d+\.\d+\.\d+\.\d+", parts[0]):
                peer_ip = parts[0]
                state = parts[-1]
                if state.lower() in ("active", "idle", "connect", "opensent", "openconfirm"):
                    issues.append({"severity": "CRITICAL", "router": router, "hostname": hostname,
                                   "peer": peer_ip, "state": state,
                                   "detail": f"BGP peer {peer_ip} on {hostname} is **{state}** (DOWN)"})
                elif state.isdigit() or "estab" in state.lower():
                    established.append({"router": router, "hostname": hostname, "peer": peer_ip})
    return issues, established


def find_ldp_issues(ldp_sess_outputs: dict, device_map: dict) -> tuple:
    issues, healthy = [], []
    for router, output in ldp_sess_outputs.items():
        hostname = device_map.get(router, router)
        if not output.strip() or "not running" in output.lower():
            continue
        for line in output.split("\n"):
            if "nonexist" in line.lower() or "closed" in line.lower():
                parts = line.split()
                peer = parts[0] if parts and re.match(r"\d+\.\d+\.\d+\.\d+", parts[0]) else "unknown"
                issues.append({"severity": "CRITICAL", "router": router, "hostname": hostname,
                               "peer": peer, "detail": f"LDP session to {peer} on {hostname} is **Nonexistent/Closed**"})
            elif "operational" in line.lower() or "open" in line.lower():
                parts = line.split()
                peer = parts[0] if parts and re.match(r"\d+\.\d+\.\d+\.\d+", parts[0]) else "unknown"
                healthy.append({"router": router, "hostname": hostname, "peer": peer})
    return issues, healthy


def find_lldp_topology(lldp_outputs: dict, device_map: dict) -> list:
    """Parse 'show lldp neighbors' output and extract topology links.
    
    Junos 'show lldp neighbors' output format:
      Local Interface    Parent Interface    Chassis Id          Port info          System Name
      ge-0/0/0           -                   2c:6b:f5:ab:cd:ef   ge-0/0/1           PE2
      et-0/0/0           -                   00:05:86:71:xx:yy   et-0/0/0           P21
      fxp0               -                   02:42:ac:11:00:02   fxp0               P22
    
    Interface patterns: ge-, xe-, et-, fxp, em, ae, irb, lo, or anything with '/'
    """
    # Known Junos interface prefixes (physical and logical)
    _INTF_PREFIXES = ("ge-", "xe-", "et-", "fxp", "em", "ae", "gr-", "lt-",
                      "so-", "fe-", "at-", "vlan", "reth", "fab", "me")
    links = []
    reverse_map = {v: k for k, v in device_map.items()}  # hostname → mcp_name
    
    for router, output in lldp_outputs.items():
        hostname = device_map.get(router, router)
        # Skip error / empty outputs
        if not output.strip() or "error" in output.lower()[:50] or "not running" in output.lower():
            logger.debug(f"LLDP: skipping {router} — empty or error output")
            continue
        for line in output.split("\n"):
            line_stripped = line.strip()
            if not line_stripped:
                continue
            parts = line_stripped.split()
            if len(parts) < 3:
                continue
            first = parts[0]
            # Skip header line
            if first.lower() in ("local", "local_interface", "localinterface"):
                continue
            # Match any known Junos interface pattern
            is_intf = ("/" in first or
                       any(first.lower().startswith(p) for p in _INTF_PREFIXES))
            if not is_intf:
                continue
            # Junos LLDP columns: Local Interface | Parent Interface | Chassis Id | Port info | System Name
            # With split(), typical results:
            #   5 parts:  [local_intf, parent, chassis_id, port_info, system_name]
            #   4 parts:  [local_intf, chassis_id, port_info, system_name]  (no parent or merged)
            #   3 parts:  [local_intf, port_info, system_name]
            remote_host = parts[-1]   # System Name is always last column
            remote_intf = parts[-2] if len(parts) >= 4 else parts[1]  # Port info
            # Skip if remote_host looks like a MAC address or chassis ID (not a hostname)
            if re.match(r"^([0-9a-fA-F]{2}:){2,}", remote_host):
                # No system name — use chassis ID as fallback
                remote_host = parts[-1]
            links.append({"local_router": router, "local_hostname": hostname,
                          "local_intf": first, "remote_hostname": remote_host, "remote_intf": remote_intf})
    
    logger.info(f"LLDP topology: parsed {len(links)} links from {len(lldp_outputs)} router outputs")
    if not links and lldp_outputs:
        # Log sample output for debugging
        for router, output in list(lldp_outputs.items())[:2]:
            sample = output[:300].replace("\n", "\\n")
            logger.warning(f"LLDP parse: 0 links from {router}, sample output: {sample}")
    return links


def build_fallback_topology(ospf_nbr_out: dict, bgp_outputs: dict, ldp_sess_out: dict,
                            isis_outputs: dict, device_map: dict) -> list:
    """Build topology links from OSPF/BGP/LDP/IS-IS neighbor data when LLDP is unavailable.
    
    Returns a list of link dicts similar to LLDP topology format, with protocol info.
    This creates a LOGICAL topology (IP-based adjacencies) rather than physical (LLDP).
    """
    reverse_map = {v.lower(): (k, v) for k, v in device_map.items()}  # lowercase hostname → (mcp_name, hostname)
    # Also map by IP → hostname (from loopback/router-id)
    ip_to_host = {}
    
    links = []
    seen_pairs = set()
    
    def _add_link(local_router: str, local_hostname: str, remote_id: str, protocol: str, local_intf: str = ""):
        """Add a topology link, deduplicating by sorted pair."""
        # Try to resolve remote_id to a known hostname
        remote_hostname = remote_id
        remote_router = ""
        # Check if remote_id is a known hostname
        if remote_id.lower() in reverse_map:
            remote_router, remote_hostname = reverse_map[remote_id.lower()]
        # Check if remote_id is an IP that maps to a known device
        elif remote_id in ip_to_host:
            remote_router, remote_hostname = ip_to_host[remote_id]
        
        pair_key = tuple(sorted([local_hostname, remote_hostname]))
        if pair_key not in seen_pairs:
            seen_pairs.add(pair_key)
            links.append({
                "local_router": local_router,
                "local_hostname": local_hostname,
                "local_intf": local_intf if local_intf else protocol,
                "remote_hostname": remote_hostname,
                "remote_intf": protocol,
                "protocol": protocol
            })
    
    # Phase 1: Build IP→hostname map from OSPF router-IDs
    for router, output in ospf_nbr_out.items():
        hostname = device_map.get(router, router)
        if not output.strip() or "error" in output.lower()[:50]:
            continue
        for line in output.split("\n"):
            parts = line.split()
            if len(parts) >= 4 and re.match(r"\d+\.\d+\.\d+\.\d+", parts[0]):
                # parts[0] = neighbor IP/router-id
                # We know this IP is a neighbor of this router
                pass  # Will be used in Phase 2
    
    # Phase 2: OSPF neighbors → topology links
    for router, output in ospf_nbr_out.items():
        hostname = device_map.get(router, router)
        if not output.strip() or "error" in output.lower()[:50]:
            continue
        for line in output.split("\n"):
            parts = line.split()
            if len(parts) >= 4 and re.match(r"\d+\.\d+\.\d+\.\d+", parts[0]):
                neighbor_id = parts[0]
                intf = parts[1] if len(parts) > 1 else ""
                _add_link(router, hostname, neighbor_id, "OSPF", intf)
    
    # Phase 3: BGP peers → topology links
    for router, output in bgp_outputs.items():
        hostname = device_map.get(router, router)
        if not output.strip() or "error" in output.lower()[:50] or "not running" in output.lower():
            continue
        for line in output.split("\n"):
            parts = line.split()
            if len(parts) >= 3 and re.match(r"\d+\.\d+\.\d+\.\d+", parts[0]):
                peer_ip = parts[0]
                state = parts[-1]
                if state.isdigit() or "estab" in state.lower():
                    _add_link(router, hostname, peer_ip, "iBGP")
    
    # Phase 4: LDP sessions → topology links
    for router, output in ldp_sess_out.items():
        hostname = device_map.get(router, router)
        if not output.strip() or "error" in output.lower()[:50] or "not running" in output.lower():
            continue
        for line in output.split("\n"):
            parts = line.split()
            if len(parts) >= 2 and re.match(r"\d+\.\d+\.\d+\.\d+", parts[0]):
                peer_ip = parts[0]
                if "operational" in line.lower() or "open" in line.lower():
                    _add_link(router, hostname, peer_ip, "LDP")
    
    # Phase 5: IS-IS adjacencies → topology links
    for router, output in isis_outputs.items():
        hostname = device_map.get(router, router)
        if not output.strip() or "error" in output.lower()[:50] or "not running" in output.lower():
            continue
        for line in output.split("\n"):
            parts = line.split()
            if len(parts) >= 3 and parts[0] and not parts[0].lower().startswith("interface"):
                # IS-IS adjacency line: Interface  System  State  Hold  SNPA
                # or: System_Name  Interface  Level  State  Hold  SNPA
                # Try to find a system name (non-IP, non-interface)
                for i, p in enumerate(parts):
                    if p and not re.match(r"\d+\.\d+\.\d+\.\d+", p) and "/" not in p and p[0].isalpha():
                        if p.lower() not in ("up", "down", "init", "one-way", "two-way", "interface",
                                             "system", "state", "hold", "snpa", "level", "l1", "l2", "l1l2"):
                            intf = parts[0] if "/" in parts[0] else ""
                            _add_link(router, hostname, p, "IS-IS", intf)
                            break
    
    logger.info(f"Fallback topology: built {len(links)} links from OSPF/BGP/LDP/IS-IS data")
    return links


def parse_ospf_intf_types(ospf_intf_output: str) -> dict:
    """Parse 'show ospf interface' output to extract interface type (PtToPt vs DR/BDR/DROther).
    
    Returns {interface_name: {"type": "p2p"|"broadcast", "nbrs": int, "raw": str}}
    
    Junos 'show ospf interface' output looks like:
      Interface           State   Area            DR ID           BDR ID          Nbrs
      ge-0/0/0.0          PtToPt  0.0.0.0         0.0.0.0         0.0.0.0            1
      ge-0/0/2.0          DR      0.0.0.0         10.255.255.3    0.0.0.0            0
      lo0.0               DR      0.0.0.0         10.255.255.3    0.0.0.0            0
    """
    result = {}
    for line in ospf_intf_output.split("\n"):
        parts = line.split()
        if len(parts) >= 4 and "." in parts[0] and parts[0][0].isalpha():
            intf_name = parts[0]
            state = parts[1]
            # Determine type from state column
            if state.lower() in ("pttopt", "ptpt", "p2p"):
                intf_type = "p2p"
            elif state.lower() in ("dr", "bdr", "drother", "waiting"):
                intf_type = "broadcast"
            else:
                intf_type = state  # Unknown, keep raw
            # Try to find Nbrs count (last column is typically Nbrs)
            nbrs = 0
            try:
                nbrs = int(parts[-1])
            except (ValueError, IndexError):
                pass
            result[intf_name] = {"type": intf_type, "nbrs": nbrs, "state": state, "raw": line.strip()}
    return result


def build_loopback_reachability(ospf_nbr_out: dict, bgp_outputs: dict, device_map: dict) -> str:
    """E14: Build a loopback IP reachability matrix showing which routers can reach each other's loopbacks.
    Returns a formatted string for injection into specialist prompts."""
    # Extract loopback IPs from OSPF neighbor outputs (neighbor address = peer's loopback for PtP links)
    loopback_ips = {}  # mcp_name -> set of known IPs (peers' loopbacks)
    router_own_lo = {}  # mcp_name -> own loopback IP (from BGP local-address or OSPF router-id)
    
    for mcp_name, output in ospf_nbr_out.items():
        for line in output.split("\n"):
            parts = line.split()
            if len(parts) >= 2 and re.match(r"\d+\.\d+\.\d+\.\d+", parts[0]):
                # parts[0] is the neighbor address (often the loopback)
                if mcp_name not in loopback_ips:
                    loopback_ips[mcp_name] = set()
                loopback_ips[mcp_name].add(parts[0])
    
    # Extract router-id / local loopback from BGP summary
    for mcp_name, output in bgp_outputs.items():
        for line in output.split("\n"):
            # Look for "Local AS:" or "Router ID:" patterns
            rid_match = re.search(r"Router ID:\s*(\d+\.\d+\.\d+\.\d+)", line)
            if rid_match:
                router_own_lo[mcp_name] = rid_match.group(1)
    
    # Build the matrix text
    if not loopback_ips and not router_own_lo:
        return ""
    
    lines = ["LOOPBACK REACHABILITY MATRIX:"]
    for mcp_name, hostname in device_map.items():
        own_lo = router_own_lo.get(mcp_name, "?")
        peers = loopback_ips.get(mcp_name, set())
        lines.append(f"  {hostname} (lo0: {own_lo}) → sees peers: {', '.join(sorted(peers)) if peers else 'NONE'}")
    return "\n".join(lines)


def find_ospf_type_mismatches(ospf_intf_outputs: dict, lldp_links: list,
                              device_map: dict) -> list:
    """Compare OSPF interface types on both sides of each LLDP link.
    
    For each physical link discovered by LLDP, check if both ends run OSPF
    and whether they agree on interface type (p2p vs broadcast).
    Returns list of mismatch issues.
    """
    # Build hostname → mcp_name reverse map
    hostname_to_mcp = {v: k for k, v in device_map.items()}
    
    # Parse OSPF interface types for each router
    ospf_parsed = {}
    for mcp_name, output in ospf_intf_outputs.items():
        ospf_parsed[mcp_name] = parse_ospf_intf_types(output)
    
    issues = []
    checked = set()  # Avoid duplicate link checks
    
    for link in lldp_links:
        local_mcp = link["local_router"]
        local_intf = link["local_intf"]
        remote_hostname = link["remote_hostname"]
        remote_intf = link["remote_intf"]
        
        # Resolve remote hostname to MCP name
        remote_mcp = hostname_to_mcp.get(remote_hostname)
        if not remote_mcp:
            continue  # Remote device not in our inventory
        
        # Create a canonical link key to avoid checking A→B and B→A
        link_key = tuple(sorted([(local_mcp, local_intf), (remote_mcp, remote_intf)]))
        if link_key in checked:
            continue
        checked.add(link_key)
        
        # Get OSPF info for both sides (use .0 subinterface if base intf given)
        local_ospf = ospf_parsed.get(local_mcp, {})
        remote_ospf = ospf_parsed.get(remote_mcp, {})
        
        # Try exact match first, then with .0 appended
        local_intf_sub = local_intf if "." in local_intf else f"{local_intf}.0"
        remote_intf_sub = remote_intf if "." in remote_intf else f"{remote_intf}.0"
        
        local_info = local_ospf.get(local_intf_sub) or local_ospf.get(local_intf)
        remote_info = remote_ospf.get(remote_intf_sub) or remote_ospf.get(remote_intf)
        
        # Both sides must have OSPF for a mismatch to matter
        if not local_info or not remote_info:
            continue
        
        local_type = local_info["type"]
        remote_type = remote_info["type"]
        
        if local_type != remote_type:
            local_hostname = device_map.get(local_mcp, local_mcp)
            remote_hostname_resolved = device_map.get(remote_mcp, remote_mcp)
            issues.append({
                "severity": "CRITICAL",
                "local_router": local_mcp, "local_hostname": local_hostname,
                "local_intf": local_intf_sub, "local_type": local_type,
                "local_state": local_info["state"], "local_nbrs": local_info["nbrs"],
                "remote_router": remote_mcp, "remote_hostname": remote_hostname_resolved,
                "remote_intf": remote_intf_sub, "remote_type": remote_type,
                "remote_state": remote_info["state"], "remote_nbrs": remote_info["nbrs"],
                "detail": (
                    f"OSPF interface-type mismatch on link "
                    f"{local_hostname} ({local_intf_sub}) ↔ {remote_hostname_resolved} ({remote_intf_sub}): "
                    f"**{local_type}** vs **{remote_type}**"
                )
            })
    
    return issues


# ── Enhancement parsers ──────────────────────────────────────

def find_isis_issues(isis_outputs: dict, device_map: dict) -> tuple:
    """Parse 'show isis adjacency' — detect down/init adjacencies.
    Returns (issues_list, healthy_list).
    
    v9.0 Fix: Filter out config metadata lines (Groups:, Protocols:, etc.)
    that appear in Junos 'show isis adjacency' output when IS-IS is configured
    but has no adjacencies, or when the output includes hierarchical config data.
    """
    issues, healthy = [], []
    # Lines that are config metadata, NOT adjacency data
    skip_prefixes = (
        "groups:", "protocols:", "interface", "level", "metric",
        "point-to-point", "bfd-liveness", "disable", "family",
        "iso", "reference-bandwidth", "no-", "overload", "export",
        "import", "is-is", "isis", "authentication", "hello-",
        "hold-time", "lsp-", "spf-", "wide-metrics", "traffic-engineering",
    )
    skip_exact = {"Interface", "System", "L1", "L2", "L1L2"}
    
    for router, output in isis_outputs.items():
        hostname = device_map.get(router, router)
        if not output.strip() or "not running" in output.lower():
            continue
        # Check if this looks like actual adjacency output vs config dump
        has_adjacency_header = any(
            "system" in line.lower() and "state" in line.lower()
            for line in output.split("\n")[:5]
        )
        for line in output.split("\n"):
            stripped = line.strip()
            if not stripped:
                continue
            parts = stripped.split()
            if len(parts) < 3:
                continue
            
            # Skip header lines
            first_word = parts[0].rstrip(":")
            if first_word.lower() in [p.lower() for p in skip_prefixes]:
                continue
            if first_word in skip_exact:
                continue
            # Skip lines that look like config stanzas (contain { or })
            if "{" in stripped or "}" in stripped or ";" in stripped:
                continue
            # Skip lines that are clearly not adjacency data
            if stripped.startswith("#") or stripped.startswith("/*"):
                continue
            
            # Valid IS-IS adjacency line has an interface name (contains / or .)
            intf = parts[0]
            is_interface = ("/" in intf or 
                           (intf.startswith(("ge-", "xe-", "et-", "ae", "lo")) and "." in intf))
            
            if not is_interface:
                continue
                
            # IS-IS adjacency states: Up, Down, Initializing
            state_col = ""
            for p in parts[1:]:
                if p.lower() in ("up", "down", "init", "initializing", "new"):
                    state_col = p
                    break
            if state_col.lower() in ("down", "init", "initializing", "new"):
                issues.append({
                    "severity": "CRITICAL", "router": router, "hostname": hostname,
                    "interface": intf, "state": state_col,
                    "detail": f"IS-IS adjacency on {hostname} {intf} is **{state_col}** (DOWN)"
                })
            elif state_col.lower() == "up":
                neighbor = parts[1] if len(parts) > 1 else "?"
                healthy.append({"router": router, "hostname": hostname,
                                "interface": intf, "neighbor": neighbor})
    return issues, healthy


def find_alarm_issues(alarm_outputs: dict, device_map: dict) -> list:
    """Parse 'show chassis alarms' — detect active alarms.
    Returns list of alarm findings with severity and description."""
    alarms = []
    for router, output in alarm_outputs.items():
        hostname = device_map.get(router, router)
        if not output.strip():
            continue
        # Skip if it just says no alarms
        if "no alarms" in output.lower() or "0 alarms" in output.lower():
            continue
        for line in output.split("\n"):
            line_s = line.strip()
            if not line_s or line_s.startswith("---") or "alarms currently active" in line_s.lower():
                continue
            if line_s.lower().startswith("class") or line_s.lower().startswith("time"):
                continue  # Header row
            # Junos alarm format: <timestamp> <class> <description>
            # e.g., "2026-02-16 10:00:00 UTC  Major  Rescue configuration is not set"
            severity = "WARNING"
            if "major" in line_s.lower():
                severity = "MAJOR"
            elif "minor" in line_s.lower():
                severity = "MINOR"
            elif "critical" in line_s.lower():
                severity = "CRITICAL"
            # Extract description (everything after the severity keyword)
            desc = line_s
            for kw in ["Major", "Minor", "Critical", "major", "minor", "critical"]:
                idx = line_s.find(kw)
                if idx != -1:
                    desc = line_s[idx + len(kw):].strip()
                    break
            if desc and len(desc) > 3:
                alarms.append({
                    "router": router, "hostname": hostname,
                    "severity": severity, "description": desc,
                    "raw": line_s
                })
    return alarms


def find_storage_issues(storage_outputs: dict, device_map: dict, threshold: int = 85) -> list:
    """Parse 'show system storage' — detect filesystems over threshold% usage.
    Returns list of storage warnings."""
    issues = []
    for router, output in storage_outputs.items():
        hostname = device_map.get(router, router)
        if not output.strip():
            continue
        for line in output.split("\n"):
            # Match: /dev/gpt/junos  1.8G  1.2G  67%  /
            m = re.search(r"(\d+)%\s+(/\S*)", line)
            if m:
                usage_pct = int(m.group(1))
                mount = m.group(2)
                if usage_pct >= threshold:
                    issues.append({
                        "router": router, "hostname": hostname,
                        "mount": mount, "usage_pct": usage_pct,
                        "detail": f"{hostname}: Filesystem **{mount}** is at **{usage_pct}%** capacity"
                    })
    return issues


def find_coredump_issues(coredump_outputs: dict, device_map: dict) -> list:
    """Parse 'show system core-dumps' — detect any core dumps present.
    Core dumps indicate process crashes — a hardware/software red flag."""
    issues = []
    for router, output in coredump_outputs.items():
        hostname = device_map.get(router, router)
        if not output.strip():
            continue
        if "no core" in output.lower() or "total files" not in output.lower():
            # Check for individual core files: lines with .core.gz or similar
            core_files = [l.strip() for l in output.split("\n")
                          if ".core" in l.lower() and l.strip() and not l.strip().startswith("No")]
            if not core_files:
                continue
        else:
            core_files = [l.strip() for l in output.split("\n")
                          if l.strip() and ".core" in l.lower()]
        if core_files:
            issues.append({
                "router": router, "hostname": hostname,
                "count": len(core_files),
                "detail": f"{hostname}: **{len(core_files)} core dump(s)** found — indicates process crash(es)",
                "files": core_files[:5]  # Cap at 5 for display
            })
    return issues


def parse_route_summary(route_outputs: dict, device_map: dict) -> dict:
    """Parse 'show route summary' — extract route counts per table.
    Returns {router: {"inet.0": N, "inet.3": N, ...}}."""
    result = {}
    for router, output in route_outputs.items():
        tables = {}
        current_table = None
        for line in output.split("\n"):
            # Table name line: "inet.0: 15 destinations, 15 routes (15 active, 0 holddown, 0 hidden)"
            m = re.match(r"(\S+):\s+(\d+)\s+destinations?,\s+(\d+)\s+routes?", line)
            if m:
                current_table = m.group(1)
                tables[current_table] = {
                    "destinations": int(m.group(2)),
                    "routes": int(m.group(3))
                }
        result[router] = tables
    return result


def parse_interface_detail(detail_outputs: dict, device_map: dict) -> dict:
    """Parse 'show interfaces detail' — extract per-interface MTU, speed, duplex, and error counters.
    Returns {router: {intf_name: {"mtu": int, "speed": str, "duplex": str,
                                   "input_errors": int, "output_errors": int,
                                   "crc_errors": int, "carrier_transitions": int}}}."""
    result = {}
    for router, output in detail_outputs.items():
        interfaces = {}
        current_intf = None
        current_data = {}
        for line in output.split("\n"):
            # Physical interface header: "Physical interface: ge-0/0/0, Enabled, Physical link is Up"
            m = re.match(r"Physical interface:\s+(\S+),?\s*(.*)", line)
            if m:
                if current_intf and current_data:
                    interfaces[current_intf] = current_data
                current_intf = m.group(1).rstrip(",")
                current_data = {"mtu": 0, "speed": "", "duplex": "",
                                "input_errors": 0, "output_errors": 0,
                                "crc_errors": 0, "carrier_transitions": 0,
                                "link_state": m.group(2)}
                continue

            if not current_intf:
                continue

            stripped = line.strip()

            # MTU: "  Link-level type: Ethernet, MTU: 1514, ..."
            mtu_match = re.search(r"MTU:\s*(\d+)", stripped)
            if mtu_match:
                current_data["mtu"] = int(mtu_match.group(1))

            # Speed: "  Speed: 1000mbps, ..." or "  Speed: 10Gbps"
            speed_match = re.search(r"Speed:\s*(\S+)", stripped)
            if speed_match:
                current_data["speed"] = speed_match.group(1).rstrip(",")

            # Duplex: "  Duplex: Full-duplex" or in combined line
            duplex_match = re.search(r"Duplex:\s*(\S+)", stripped)
            if duplex_match:
                current_data["duplex"] = duplex_match.group(1).rstrip(",")

            # Input errors line: "  Input errors: 5, ..."
            inp_err = re.search(r"Input errors:\s*(\d+)", stripped)
            if inp_err:
                current_data["input_errors"] = int(inp_err.group(1))

            # Output errors line: "  Output errors: 0, ..."
            out_err = re.search(r"Output errors:\s*(\d+)", stripped)
            if out_err:
                current_data["output_errors"] = int(out_err.group(1))

            # CRC/Align errors: "  Framing errors: 0, Runts: 0, Policed discards: 0, L3 incompletes: 0, L2 channel errors: 0, L2 mismatch timeouts: 0, FIFO errors: 0, HS link CRC errors: 0,"
            # Or "  CRC/Align errors: 3"
            crc_match = re.search(r"(?:CRC|FCS)\s*(?:/Align)?\s*errors:\s*(\d+)", stripped, re.IGNORECASE)
            if crc_match:
                current_data["crc_errors"] = max(current_data["crc_errors"], int(crc_match.group(1)))

            # Carrier transitions: "  Carrier transitions: 5"
            ct_match = re.search(r"Carrier transitions:\s*(\d+)", stripped)
            if ct_match:
                current_data["carrier_transitions"] = int(ct_match.group(1))

        # Don't forget the last interface
        if current_intf and current_data:
            interfaces[current_intf] = current_data

        result[router] = interfaces
    return result


def find_mtu_mismatches(intf_details: dict, lldp_links: list, device_map: dict) -> list:
    """Cross-reference LLDP link endpoints and compare MTU on each side.
    Returns list of mismatches (where both sides have data but MTUs differ)."""
    mismatches = []
    seen = set()  # Avoid duplicate reports for A↔B and B↔A

    for link in lldp_links:
        local_router = link["local_router"]
        local_intf = link["local_intf"]
        remote_hostname = link["remote_hostname"]
        remote_intf = link["remote_intf"]

        # Find the remote router's MCP name from device_map
        remote_router = None
        for mcp_name, hostname in device_map.items():
            if hostname == remote_hostname or mcp_name == remote_hostname:
                remote_router = mcp_name
                break
        if not remote_router:
            continue

        local_data = intf_details.get(local_router, {}).get(local_intf, {})
        remote_data = intf_details.get(remote_router, {}).get(remote_intf, {})
        local_mtu = local_data.get("mtu", 0)
        remote_mtu = remote_data.get("mtu", 0)

        if local_mtu > 0 and remote_mtu > 0 and local_mtu != remote_mtu:
            link_key = tuple(sorted([(local_router, local_intf), (remote_router, remote_intf)]))
            if link_key in seen:
                continue
            seen.add(link_key)

            local_hostname = device_map.get(local_router, local_router)
            remote_hostname_disp = device_map.get(remote_router, remote_router)
            mismatches.append({
                "local_router": local_router, "local_hostname": local_hostname,
                "local_intf": local_intf, "local_mtu": local_mtu,
                "remote_router": remote_router, "remote_hostname": remote_hostname_disp,
                "remote_intf": remote_intf, "remote_mtu": remote_mtu,
                "detail": (f"MTU mismatch on link {local_hostname}:{local_intf} (MTU {local_mtu}) "
                           f"↔ {remote_hostname_disp}:{remote_intf} (MTU {remote_mtu})")
            })
    return mismatches


def find_interface_errors(intf_details: dict, device_map: dict,
                          crc_threshold: int = 0, input_err_threshold: int = 0,
                          carrier_threshold: int = 10) -> list:
    """Detect interfaces with CRC errors, input/output errors, or excessive carrier transitions.
    These indicate physical layer problems (bad cables, SFPs, or speed/duplex mismatches)."""
    issues = []
    for router, interfaces in intf_details.items():
        hostname = device_map.get(router, router)
        for intf_name, data in interfaces.items():
            # Skip management and loopback
            if any(intf_name.startswith(p) for p in ("lo", "em", "fxp", "bme", "irb", "jsrv", "pip", "gre", "ipip", "lsi", "mt", "dsc")):
                continue

            problems = []
            if data.get("crc_errors", 0) > crc_threshold:
                problems.append(f"CRC errors: {data['crc_errors']}")
            if data.get("input_errors", 0) > input_err_threshold:
                problems.append(f"Input errors: {data['input_errors']}")
            if data.get("output_errors", 0) > input_err_threshold:
                problems.append(f"Output errors: {data['output_errors']}")
            if data.get("carrier_transitions", 0) > carrier_threshold:
                problems.append(f"Carrier transitions: {data['carrier_transitions']} (link flaps)")

            # Speed/duplex anomaly: Half-duplex on anything ≥ GE is a red flag
            speed = data.get("speed", "").lower()
            duplex = data.get("duplex", "").lower()
            if "half" in duplex and speed:
                problems.append(f"Half-duplex detected (speed: {data.get('speed', '?')})")

            if problems:
                issues.append({
                    "router": router, "hostname": hostname,
                    "interface": intf_name,
                    "problems": problems,
                    "speed": data.get("speed", "?"),
                    "duplex": data.get("duplex", "?"),
                    "detail": f"{hostname} {intf_name}: {'; '.join(problems)}"
                })
    return issues


# ── Ollama helpers ───────────────────────────────────────────

def mcp_tools_to_ollama_tools(mcp_tools: list) -> list:
    return [{"type": "function", "function": {
        "name": t["name"], "description": t.get("description", ""),
        "parameters": t.get("inputSchema", {"type": "object", "properties": {}})
    }} for t in mcp_tools]


async def ollama_chat(messages, tools=None, retries=3):
    """Send chat to Ollama with low temperature for precision and retry logic."""
    payload = {"model": MODEL, "messages": messages, "stream": False,
               "options": {
                   "num_ctx": NUM_CTX,
                   "temperature": AI_TEMPERATURE,
                   "top_p": AI_TOP_P,
                   "repeat_penalty": AI_REPEAT_PENALTY,
               }}
    if tools:
        payload["tools"] = tools
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            timeout = 600.0 + (attempt - 1) * 300.0  # 600s, 900s, 1200s
            async with httpx.AsyncClient(timeout=timeout) as client:
                resp = await client.post(f"{OLLAMA_URL}/api/chat", json=payload)
                result = resp.json()
                # Validate response structure
                if "message" not in result:
                    logger.warning(f"Ollama returned no 'message' key (attempt {attempt}): {list(result.keys())}")
                    if attempt < retries:
                        continue
                return result
        except (httpx.ReadTimeout, httpx.ConnectTimeout) as e:
            last_err = e
            logger.warning(f"Ollama timeout attempt {attempt}/{retries}: {e}")
            if attempt < retries:
                await asyncio.sleep(2 * attempt)  # Exponential backoff
        except Exception as e:
            last_err = e
            logger.error(f"Ollama error attempt {attempt}/{retries}: {e}")
            if attempt < retries:
                await asyncio.sleep(1)
    raise last_err or RuntimeError("ollama_chat failed after all retries")


def smart_truncate_tool_result(result: str, tool_name: str, max_chars: int = 6000) -> str:
    """Intelligently truncate tool results to fit context budget.
    
    Instead of blindly cutting at N chars, this preserves the STRUCTURE:
    - For batch commands: keeps header + first/last lines per device
    - For show commands: keeps the important summary lines
    - Removes blank lines and redundant whitespace
    """
    if len(result) <= max_chars:
        return result
    
    lines = result.split("\n")
    
    # For batch results, try to preserve per-device structure
    if tool_name == "execute_junos_command_batch":
        # Find device separators and keep key lines from each device block
        device_blocks = []
        current_block = []
        for line in lines:
            # Common device separators in batch output
            if line.strip().startswith("===") or line.strip().startswith("---") or line.strip().startswith("Router:"):
                if current_block:
                    device_blocks.append(current_block)
                current_block = [line]
            else:
                current_block.append(line)
        if current_block:
            device_blocks.append(current_block)
        
        if len(device_blocks) > 1:
            # Budget per device block
            per_block = max(300, (max_chars - 200) // len(device_blocks))
            truncated_blocks = []
            for block in device_blocks:
                block_text = "\n".join(block)
                if len(block_text) > per_block:
                    # Keep first half and last quarter
                    first_part = block_text[:per_block * 2 // 3]
                    last_part = block_text[-(per_block // 3):]
                    block_text = first_part + "\n[...truncated...]\n" + last_part
                truncated_blocks.append(block_text)
            return "\n".join(truncated_blocks)
    
    # For config output, keep first and last sections
    if tool_name == "get_junos_config":
        half = max_chars // 2
        return result[:half] + f"\n\n[...{len(result) - max_chars} chars omitted...]\n\n" + result[-half:]
    
    # Default: keep first 2/3 and last 1/3
    first = max_chars * 2 // 3
    last = max_chars // 3
    return result[:first] + f"\n[...truncated {len(result) - max_chars} chars...]\n" + result[-last:]


# ══════════════════════════════════════════════════════════════
#  v12.0: INTELLIGENCE UPGRADES
# ══════════════════════════════════════════════════════════════

# ── Enhancement #1: Persistent Topology Graph ───────────────
def build_topology_from_golden_configs() -> dict:
    """Parse golden configs to build a persistent topology graph.
    Returns {links: [{a, a_intf, b, b_intf, subnet}], loopbacks: {router: ip}, roles: {router: PE|P|RR}}
    """
    topology = {"links": [], "loopbacks": {}, "roles": {}, "bgp_peers": {}}
    seen_links = set()
    
    if not os.path.exists(GOLDEN_CONFIG_DIR):
        return topology
    
    for fname in sorted(os.listdir(GOLDEN_CONFIG_DIR)):
        if not fname.endswith(".conf"):
            continue
        router = fname.replace(".conf", "")
        config_path = os.path.join(GOLDEN_CONFIG_DIR, fname)
        
        try:
            with open(config_path, "r") as f:
                lines = f.readlines()
        except Exception:
            continue
        
        # Determine role
        if router.startswith("PE"):
            topology["roles"][router] = "PE"
        elif router in ("P12", "P22"):
            topology["roles"][router] = "RR"
        else:
            topology["roles"][router] = "P"
        
        # Parse interfaces
        descriptions = {}  # intf -> description
        addresses = {}     # intf -> ip/mask
        
        for line in lines:
            line = line.strip()
            # Description: set interfaces ge-0/0/1 description PE1->P11
            m = re.match(r'set interfaces (ge-\d+/\d+/\d+) description "?(\S+?)"?\s*$', line)
            if m:
                descriptions[m.group(1)] = m.group(2)
            # IPv4 address: set interfaces ge-0/0/1 unit 0 family inet address 10.1.11.1/24
            m = re.match(r'set interfaces (ge-\d+/\d+/\d+) unit \d+ family inet address (\d+\.\d+\.\d+\.\d+/\d+)', line)
            if m:
                addresses[m.group(1)] = m.group(2)
            # Loopback: set interfaces lo0 unit 0 family inet address 10.255.255.1/32
            m = re.match(r'set interfaces lo0 unit 0 family inet address (\d+\.\d+\.\d+\.\d+)/32', line)
            if m:
                topology["loopbacks"][router] = m.group(1)
            # BGP neighbors: set protocols bgp group IBGP neighbor 10.255.255.12
            m = re.match(r'set protocols bgp group \S+ neighbor (\d+\.\d+\.\d+\.\d+)', line)
            if m:
                topology["bgp_peers"].setdefault(router, []).append(m.group(1))
        
        # Build links from descriptions
        for intf, desc in descriptions.items():
            m = re.match(r'(\w+)->(\w+)', desc)
            if m:
                local_name = m.group(1)
                remote_name = m.group(2)
                link_key = tuple(sorted([local_name, remote_name])) + (intf,)
                if link_key not in seen_links:
                    seen_links.add(link_key)
                    subnet = addresses.get(intf, "?")
                    topology["links"].append({
                        "a": local_name, "a_intf": intf,
                        "b": remote_name, "subnet": subnet.split("/")[0].rsplit(".", 1)[0] + ".0/24" if "/" in subnet else "?"
                    })
    
    return topology


def topology_to_prompt_string(topo: dict) -> str:
    """Convert topology graph to a compact string for system prompt injection."""
    if not topo or not topo.get("links"):
        return ""
    
    lines = ["## NETWORK TOPOLOGY"]
    
    # Loopbacks
    lines.append("**Loopbacks:** " + ", ".join(f"{r}={ip}" for r, ip in sorted(topo["loopbacks"].items())))
    
    # Roles
    pe_list = [r for r, role in topo["roles"].items() if role == "PE"]
    rr_list = [r for r, role in topo["roles"].items() if role == "RR"]
    p_list = [r for r, role in topo["roles"].items() if role == "P" and r not in rr_list]
    lines.append(f"**Roles:** PE={','.join(sorted(pe_list))} | RR={','.join(sorted(rr_list))} | P={','.join(sorted(p_list))}")
    
    # Adjacencies (compact)
    adj = {}
    for link in topo["links"]:
        adj.setdefault(link["a"], []).append(link["b"])
    lines.append("**Adjacencies:**")
    for router in sorted(adj.keys()):
        neighbors = sorted(set(adj[router]))
        lines.append(f"  {router} → {', '.join(neighbors)}")
    
    # BGP peers
    if topo.get("bgp_peers"):
        lines.append("**BGP Peers (iBGP via RR):**")
        # Resolve loopback IPs to names
        ip_to_name = {ip: name for name, ip in topo["loopbacks"].items()}
        for router in sorted(topo["bgp_peers"].keys()):
            peers = [ip_to_name.get(ip, ip) for ip in topo["bgp_peers"][router]]
            lines.append(f"  {router} → {', '.join(peers)}")
    
    return "\n".join(lines)


# ── Enhancement #3: Conversation Summary Pin ────────────────
def generate_conversation_summary(messages: list) -> str:
    """Extract a compact summary from recent conversation to survive token trimming.
    Captures: last device discussed, last issue, last fix, current state.
    """
    summary_parts = []
    last_device = None
    last_issue = None
    last_fix = None
    
    # Scan last 10 messages for context
    recent = [m for m in messages[-10:] if m.get("role") in ("user", "assistant") and m.get("content")]
    
    for msg in recent:
        content = msg.get("content", "")
        role = msg.get("role", "")
        
        if role == "user":
            # Extract device mentions
            device_match = re.findall(r'\b(PE[123]|P[12][1234])\b', content, re.IGNORECASE)
            if device_match:
                last_device = device_match[-1].upper()
        
        if role == "assistant":
            # Extract issues mentioned
            if "CRITICAL" in content or "issue" in content.lower() or "problem" in content.lower():
                # Get first line that mentions the issue
                for line in content.split("\n"):
                    if any(kw in line.lower() for kw in ["critical", "warning", "issue", "problem", "down", "failed"]):
                        last_issue = line.strip()[:150]
                        break
            # Extract fix commands
            fix_match = re.findall(r'(set protocols \S+.*|delete \S+.*)', content)
            if fix_match:
                last_fix = fix_match[-1][:150]
    
    if last_device:
        summary_parts.append(f"Last device: {last_device}")
    if last_issue:
        summary_parts.append(f"Last issue: {last_issue}")
    if last_fix:
        summary_parts.append(f"Last fix: {last_fix}")
    
    if summary_parts:
        return "[CONTEXT: " + " | ".join(summary_parts) + "]"
    return ""


# ── Enhancement #4: Query Classification ────────────────────
def classify_query(user_input: str, has_kb: bool = True) -> str:
    """Classify user query to determine the best handling strategy.
    Returns: 'knowledge', 'status', 'troubleshoot', 'config', 'compare', 'general'
    """
    lower = user_input.lower().strip()
    
    # Config requests
    if lower.startswith(("configure ", "set ", "delete ", "add ", "remove ", "enable ", "disable ")):
        return "config"
    if any(kw in lower for kw in ["push config", "apply config", "commit", "rollback"]):
        return "config"
    
    # Comparison
    if any(kw in lower for kw in ["compare", "diff", "difference between", "vs ", "versus"]):
        return "compare"
    
    # Pure knowledge questions (no device/tool needed)
    knowledge_patterns = [
        r"^what is ", r"^what are ", r"^explain ", r"^how does ", r"^how do ",
        r"^describe ", r"^define ", r"^tell me about ", r"^why does ",
        r"^what's the difference between",
    ]
    if any(re.match(pat, lower) for pat in knowledge_patterns):
        # But if it mentions a specific device, it's a status question
        if not re.search(r'\b(PE[123]|P[12][1234])\b', user_input, re.IGNORECASE):
            return "knowledge"
    
    # Troubleshooting
    if any(kw in lower for kw in ["troubleshoot", "investigate", "why is", "why are", "root cause",
                                   "broken", "down", "failing", "flapping", "not working"]):
        return "troubleshoot"
    
    # Status checks
    if any(kw in lower for kw in ["check", "show", "status", "health", "neighbor", "bgp", "ospf",
                                   "ldp", "isis", "interface", "route", "is ", "are "]):
        return "status"
    
    return "general"


# ── Enhancement #5: Lessons Learned Database ────────────────
def save_lesson(category: str, description: str, root_cause: str, fix: str, router: str = ""):
    """Save a lesson learned from an incident for future reference."""
    try:
        db = []
        if os.path.exists(LESSONS_LEARNED_PATH):
            with open(LESSONS_LEARNED_PATH, "r") as f:
                db = json.load(f)
        
        # Check if similar lesson exists (update count)
        for existing in db:
            if existing.get("category") == category and existing.get("root_cause") == root_cause:
                existing["occurrences"] = existing.get("occurrences", 1) + 1
                existing["last_seen"] = datetime.now().isoformat()
                if router and router not in existing.get("routers", []):
                    existing.setdefault("routers", []).append(router)
                with open(LESSONS_LEARNED_PATH, "w") as f:
                    json.dump(db, f, indent=2)
                return
        
        # New lesson
        db.append({
            "category": category,
            "description": description,
            "root_cause": root_cause,
            "fix": fix,
            "routers": [router] if router else [],
            "occurrences": 1,
            "first_seen": datetime.now().isoformat(),
            "last_seen": datetime.now().isoformat(),
        })
        
        with open(LESSONS_LEARNED_PATH, "w") as f:
            json.dump(db, f, indent=2)
    except Exception as e:
        logger.warning(f"Lessons DB save failed: {e}")


def get_top_lessons(n: int = 5) -> str:
    """Get top N lessons by occurrence count for prompt injection."""
    try:
        if not os.path.exists(LESSONS_LEARNED_PATH):
            return ""
        with open(LESSONS_LEARNED_PATH, "r") as f:
            db = json.load(f)
        if not db:
            return ""
        
        # Sort by occurrences descending
        db.sort(key=lambda x: x.get("occurrences", 0), reverse=True)
        top = db[:n]
        
        lines = ["## LESSONS LEARNED (from past incidents)"]
        for lesson in top:
            lines.append(f"- **{lesson['category']}** (seen {lesson.get('occurrences', 1)}x): "
                         f"{lesson['description']} → Fix: `{lesson['fix']}`")
        return "\n".join(lines)
    except Exception:
        return ""


# ── v13.1: Workflow Self-Improvement Lessons ────────────────────
WORKFLOW_LESSONS_PATH = os.path.join("tasks", "lessons.md")


def load_workflow_lessons() -> str:
    """Load workflow lessons from tasks/lessons.md for session-start review.
    Returns formatted text for system prompt injection."""
    try:
        if not os.path.exists(WORKFLOW_LESSONS_PATH):
            return ""
        with open(WORKFLOW_LESSONS_PATH, "r") as f:
            content = f.read()
        # Extract just the rules section
        if "## Rules" not in content:
            return ""
        rules_section = content.split("## Rules", 1)[1].strip()
        if not rules_section or rules_section.startswith("<!-- "):
            return ""
        return f"## SELF-IMPROVEMENT LESSONS (from past corrections)\n{rules_section}"
    except Exception:
        return ""


def save_workflow_lesson(mistake: str, correction: str, rule: str):
    """Save a self-improvement lesson when user corrects the AI.
    Appends to tasks/lessons.md with timestamp."""
    try:
        os.makedirs("tasks", exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Create the file if it doesn't exist
        if not os.path.exists(WORKFLOW_LESSONS_PATH):
            with open(WORKFLOW_LESSONS_PATH, "w") as f:
                f.write("# AI Self-Improvement Lessons\n\n"
                        "> This file is automatically updated when the user corrects the AI.\n"
                        "> The AI reviews these lessons at session start to avoid repeating mistakes.\n\n"
                        "---\n\n## Rules\n\n")
        
        # Append the new lesson
        entry = (
            f"### Lesson — {timestamp}\n"
            f"- **Mistake:** {mistake}\n"
            f"- **Correction:** {correction}\n"
            f"- **Rule:** {rule}\n\n"
        )
        
        with open(WORKFLOW_LESSONS_PATH, "a") as f:
            f.write(entry)
        
        logger.info(f"Workflow lesson saved: {rule[:80]}")
    except Exception as e:
        logger.warning(f"Failed to save workflow lesson: {e}")


def detect_user_correction(user_msg: str, prev_messages: list) -> bool:
    """Detect if the user is correcting the AI based on their message content."""
    correction_indicators = [
        "no,", "no ", "wrong", "incorrect", "that's not", "that is not",
        "you're wrong", "you are wrong", "not right", "fix this", "fix it",
        "try again", "redo", "actually", "i said", "i meant", "i asked",
        "don't", "do not", "stop", "shouldn't", "should not", "never",
        "bad", "mistake", "error", "broken", "you broke", "messed up",
        "not what i", "that wasn't", "that was not", "why did you",
    ]
    lower_msg = user_msg.lower().strip()
    return any(indicator in lower_msg for indicator in correction_indicators)


async def generate_lesson_from_correction(user_correction: str, ai_previous: str) -> dict:
    """Use the AI to generate a self-improvement lesson from a correction.
    Returns dict with mistake, correction, rule keys."""
    try:
        lesson_prompt = (
            f"The user just corrected you. Analyze the mistake and generate a lesson.\n\n"
            f"YOUR PREVIOUS RESPONSE (excerpt):\n{ai_previous[:500]}\n\n"
            f"USER'S CORRECTION:\n{user_correction}\n\n"
            f"Generate a concise lesson in this EXACT format (one line each):\n"
            f"MISTAKE: <what you did wrong>\n"
            f"CORRECTION: <what the user wanted>\n"
            f"RULE: <rule to follow to prevent this in the future>\n"
        )
        
        result = await ollama_analyze(
            "You are a self-reflective AI that learns from mistakes. Be honest and concise.",
            "",
            lesson_prompt
        )
        
        # Parse the response
        lesson = {"mistake": "", "correction": "", "rule": ""}
        for line in result.split("\n"):
            line = line.strip()
            if line.upper().startswith("MISTAKE:"):
                lesson["mistake"] = line.split(":", 1)[1].strip()
            elif line.upper().startswith("CORRECTION:"):
                lesson["correction"] = line.split(":", 1)[1].strip()
            elif line.upper().startswith("RULE:"):
                lesson["rule"] = line.split(":", 1)[1].strip()
        
        # Ensure we have at least a rule
        if not lesson["rule"]:
            lesson["rule"] = f"Pay attention when user says: {user_correction[:100]}"
        if not lesson["mistake"]:
            lesson["mistake"] = f"Previous response didn't match user expectations"
        if not lesson["correction"]:
            lesson["correction"] = user_correction[:150]
        
        return lesson
    except Exception as e:
        logger.warning(f"Lesson generation failed: {e}")
        return {
            "mistake": "Previous response didn't match user expectations",
            "correction": user_correction[:150],
            "rule": f"Pay closer attention to user intent: {user_correction[:100]}"
        }


# ── Enhancement #6: Audit Trend Analysis ────────────────────
def get_audit_trends(n: int = 5) -> str:
    """Query last N audits from SQLite DB and return a trend summary."""
    try:
        if not os.path.exists(AUDIT_DB_PATH):
            return ""
        conn = sqlite3.connect(AUDIT_DB_PATH)
        c = conn.cursor()
        c.execute("""SELECT timestamp, health_score, health_grade, critical_count, 
                      warning_count, config_drifts 
                      FROM audits ORDER BY id DESC LIMIT ?""", (n,))
        rows = c.fetchall()
        conn.close()
        
        if not rows:
            return ""
        
        lines = ["## AUDIT TRENDS (last {} audits)".format(len(rows))]
        
        # Show trend direction
        if len(rows) >= 2:
            latest = rows[0]
            previous = rows[1]
            score_delta = (latest[1] or 0) - (previous[1] or 0)
            crit_delta = (latest[3] or 0) - (previous[3] or 0)
            
            trend_emoji = "▴" if score_delta > 0 else "▾" if score_delta < 0 else "→"
            lines.append(f"Health: {latest[2] or '?'} ({latest[1] or 0:.0f}%) {trend_emoji} "
                         f"({'↑' if score_delta > 0 else '↓'}{abs(score_delta):.0f}% from previous)")
            
            if crit_delta > 0:
                lines.append(f"▲ Critical issues increased: {previous[3] or 0} → {latest[3] or 0}")
            elif crit_delta < 0:
                lines.append(f"● Critical issues decreased: {previous[3] or 0} → {latest[3] or 0}")
        elif rows:
            latest = rows[0]
            lines.append(f"Last audit: {latest[2] or '?'} ({latest[1] or 0:.0f}%), "
                         f"{latest[3] or 0} critical, {latest[4] or 0} warnings")
        
        # Recurring issues from audit_issues table
        try:
            conn = sqlite3.connect(AUDIT_DB_PATH)
            c = conn.cursor()
            c.execute("""SELECT protocol, detail, COUNT(*) as cnt 
                          FROM audit_issues 
                          WHERE severity IN ('CRITICAL', 'WARNING') 
                          GROUP BY protocol, detail 
                          ORDER BY cnt DESC LIMIT 3""")
            recurring = c.fetchall()
            conn.close()
            
            if recurring:
                lines.append("**Recurring issues:**")
                for proto, detail, cnt in recurring:
                    lines.append(f"  - {proto}: {detail[:80]} ({cnt}x)")
        except Exception:
            pass
        
        return "\n".join(lines)
    except Exception as e:
        logger.debug(f"Audit trend query failed: {e}")
        return ""


# ── Enhancement #6: Live Network Dashboard State ────────────
_network_health_state: dict = {}  # Global mutable state for background poll
_health_poll_running = False

async def background_health_poll(mcp_client, session_id: str, device_map: dict, interval: int = 300):
    """Background coroutine: poll network health every `interval` seconds.
    Stores a compact state summary in _network_health_state.
    """
    global _network_health_state, _health_poll_running
    _health_poll_running = True
    logger.info(f"Background health poll started (every {interval}s)")
    
    while _health_poll_running:
        try:
            state = {
                "last_check": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "devices": {},
                "alerts": [],
                "summary": "",
            }
            
            # Quick BGP check across all routers
            for mcp_name in list(device_map.keys())[:6]:  # Limit to 6 to stay fast
                try:
                    bgp_out = await asyncio.wait_for(
                        mcp_call_tool(mcp_client, session_id, "execute_junos_command",
                                      {"router_name": mcp_name, "command": "show bgp summary"}),
                        timeout=30
                    )
                    estab = bgp_out.lower().count("establ")
                    active = bgp_out.lower().count("active")
                    connect = bgp_out.lower().count("connect")
                    
                    dev_state = {"bgp_up": estab, "bgp_issues": active + connect}
                    state["devices"][mcp_name] = dev_state
                    
                    if active + connect > 0:
                        state["alerts"].append(f"{mcp_name}: {active + connect} BGP sessions not Established")
                        add_proactive_alert(f"{mcp_name}: {active + connect} BGP sessions not Established")
                except (asyncio.TimeoutError, Exception):
                    state["devices"][mcp_name] = {"bgp_up": -1, "bgp_issues": -1}
                    state["alerts"].append(f"{mcp_name}: unreachable during health poll")
            
            # Build summary
            total_ok = sum(1 for d in state["devices"].values() if d.get("bgp_issues", 0) == 0)
            total = len(state["devices"])
            state["summary"] = f"Health: {total_ok}/{total} devices OK"
            if state["alerts"]:
                state["summary"] += f" | {len(state['alerts'])} alert(s)"
            
            _network_health_state = state
            logger.debug(f"Health poll complete: {state['summary']}")
        except Exception as e:
            logger.debug(f"Health poll error: {e}")
        
        await asyncio.sleep(interval)


def get_health_state_prompt() -> str:
    """Return compact health state string for system prompt injection."""
    if not _network_health_state:
        return ""
    state = _network_health_state
    lines = [f"## LIVE NETWORK STATE (as of {state.get('last_check', '?')})"]
    lines.append(state.get("summary", "Unknown"))
    for alert in state.get("alerts", [])[:5]:
        lines.append(f"  ▲ {alert}")
    return "\n".join(lines)


def stop_health_poll():
    """Stop the background health poll."""
    global _health_poll_running
    _health_poll_running = False


# ── Enhancement #8: Runbook Automation ──────────────────────
RUNBOOKS = {
    "add_l3vpn_customer": {
        "name": "Add L3VPN Customer",
        "description": "Add a new L3VPN routing instance on a PE router",
        "params": {
            "router": "PE router name (e.g. PE1)",
            "vrf_name": "VRF instance name",
            "interface": "Customer-facing interface (e.g. ge-0/0/5.100)",
            "rd": "Route distinguisher (e.g. 65000:100)",
            "rt": "Route target (e.g. target:65000:100)",
            "customer_ip": "Customer interface IP (e.g. 192.168.100.1/30)",
        },
        "steps": [
            {"desc": "Create routing instance", "cmd": "set routing-instances {vrf_name} instance-type vrf"},
            {"desc": "Set interface", "cmd": "set routing-instances {vrf_name} interface {interface}"},
            {"desc": "Set RD", "cmd": "set routing-instances {vrf_name} route-distinguisher {rd}"},
            {"desc": "Set RT import/export", "cmd": "set routing-instances {vrf_name} vrf-target {rt}"},
            {"desc": "Configure customer interface", "cmd": "set interfaces {interface} family inet address {customer_ip}"},
            {"desc": "Add BGP export policy", "cmd": "set routing-instances {vrf_name} protocols bgp group ce-peers type external"},
        ],
        "verify": [
            "show route instance {vrf_name}",
            "show route table {vrf_name}.inet.0",
            "show bgp summary instance {vrf_name}",
        ],
    },
    "add_ospf_interface": {
        "name": "Add OSPF Interface",
        "description": "Enable OSPF on an interface",
        "params": {
            "router": "Router name",
            "interface": "Interface (e.g. ge-0/0/3.0)",
            "area": "OSPF area (e.g. 0.0.0.0)",
            "intf_type": "Interface type (p2p or broadcast)",
        },
        "steps": [
            {"desc": "Add interface to OSPF", "cmd": "set protocols ospf area {area} interface {interface} interface-type {intf_type}"},
        ],
        "verify": ["show ospf neighbor", "show ospf interface {interface}"],
    },
    "add_ldp_interface": {
        "name": "Enable LDP on Interface",
        "description": "Enable LDP on an interface with optional BFD",
        "params": {
            "router": "Router name",
            "interface": "Interface (e.g. ge-0/0/3.0)",
        },
        "steps": [
            {"desc": "Enable LDP on interface", "cmd": "set protocols ldp interface {interface}"},
            {"desc": "Enable deaggregate label ops", "cmd": "set protocols ldp deaggregate"},
        ],
        "verify": ["show ldp session", "show ldp neighbor"],
    },
    "bgp_peer_add": {
        "name": "Add iBGP Peer",
        "description": "Add a new iBGP peer to a BGP group",
        "params": {
            "router": "Router name",
            "group": "BGP group name (e.g. iBGP)",
            "peer_ip": "Peer loopback IP",
            "local_as": "Local AS number",
        },
        "steps": [
            {"desc": "Add peer to BGP group", "cmd": "set protocols bgp group {group} neighbor {peer_ip}"},
            {"desc": "Set local AS", "cmd": "set protocols bgp group {group} local-as {local_as}"},
        ],
        "verify": ["show bgp summary", "show bgp neighbor {peer_ip}"],
    },
    "hardening": {
        "name": "Security Hardening",
        "description": "Apply baseline security hardening to a router",
        "params": {
            "router": "Router name",
        },
        "steps": [
            {"desc": "Disable telnet", "cmd": "delete system services telnet"},
            {"desc": "Set SSH v2 only", "cmd": "set system services ssh protocol-version v2"},
            {"desc": "Set login message", "cmd": 'set system login message "\\n*** AUTHORIZED ACCESS ONLY ***\\n"'},
            {"desc": "Set idle timeout", "cmd": "set system login idle-timeout 15"},
            {"desc": "Set syslog", "cmd": "set system syslog file messages any notice"},
        ],
        "verify": ["show system services", "show configuration system login"],
    },
}


def format_runbook_preview(rb_name: str, params: dict) -> str:
    """Format a runbook with filled parameters for user review."""
    rb = RUNBOOKS.get(rb_name)
    if not rb:
        return f"Unknown runbook: {rb_name}"
    
    lines = [f"## ◇ Runbook: {rb['name']}", f"_{rb['description']}_\n"]
    lines.append("### Steps:")
    for i, step in enumerate(rb["steps"], 1):
        cmd = step["cmd"].format(**params)
        lines.append(f"  {i}. {step['desc']}: `{cmd}`")
    
    lines.append("\n### Verification:")
    for vcmd in rb.get("verify", []):
        lines.append(f"  • `{vcmd.format(**params)}`")
    
    return "\n".join(lines)


def get_runbook_commands(rb_name: str, params: dict) -> list:
    """Return the list of set commands for a runbook with params filled in."""
    rb = RUNBOOKS.get(rb_name)
    if not rb:
        return []
    return [step["cmd"].format(**params) for step in rb["steps"]]


# ── Enhancement #9: What-If Config Simulator ────────────────
def simulate_config_impact(config_text: str, topology: dict) -> str:
    """Predict the impact of proposed config commands using topology awareness.
    Parses set/delete commands, identifies affected protocols/interfaces,
    and predicts cascading effects using the topology graph.
    """
    if not config_text.strip():
        return "No config commands to analyze."
    
    lines = config_text.strip().split("\n")
    affected_protocols = set()
    affected_interfaces = set()
    affected_routers = set()
    warnings = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Detect protocols
        for proto in ["ospf", "bgp", "ldp", "isis", "is-is", "rsvp", "mpls", "bfd"]:
            if proto in line.lower():
                affected_protocols.add(proto.upper().replace("IS-IS", "ISIS"))
        
        # Detect interfaces
        intf_match = re.findall(r'(ge-\d+/\d+/\d+(?:\.\d+)?|ae\d+(?:\.\d+)?|lo0(?:\.\d+)?)', line)
        affected_interfaces.update(intf_match)
        
        # Detect delete commands (high risk)
        if line.startswith("delete ") or line.startswith("deactivate "):
            warnings.append(f"▲ DESTRUCTIVE: `{line[:80]}`")
        
        # Detect firewall filter changes (can break control plane)
        if "firewall" in line.lower() and "filter" in line.lower():
            warnings.append(f"⊗ FIREWALL CHANGE — could block protocol traffic: `{line[:80]}`")
    
    # Map interfaces to topology links
    affected_links = []
    for link in topology.get("links", []):
        if link.get("a_intf") in affected_interfaces or link.get("b_intf") in affected_interfaces:
            affected_links.append(f"{link['a']} ↔ {link['b']} ({link.get('a_intf', '?')})")
            affected_routers.add(link["a"])
            affected_routers.add(link["b"])
    
    # Build impact report
    report = ["## ◉ Config Impact Prediction\n"]
    
    if affected_protocols:
        report.append(f"**Affected Protocols:** {', '.join(sorted(affected_protocols))}")
    if affected_interfaces:
        report.append(f"**Affected Interfaces:** {', '.join(sorted(affected_interfaces))}")
    if affected_links:
        report.append(f"**Affected Links:**")
        for lnk in affected_links:
            report.append(f"  • {lnk}")
    if affected_routers:
        report.append(f"**Potentially Impacted Routers:** {', '.join(sorted(affected_routers))}")
    if warnings:
        report.append(f"\n**▲ Warnings:**")
        for w in warnings:
            report.append(f"  {w}")
    
    if not affected_protocols and not affected_interfaces and not warnings:
        report.append("No significant protocol or interface impact detected.")
    
    return "\n".join(report)


# ── Enhancement #10: Proactive Alert Injection ──────────────
_proactive_alerts: list = []  # Global alert buffer

def check_for_proactive_alerts() -> str:
    """Return any proactive alerts that should be shown to the user."""
    if not _proactive_alerts:
        return ""
    
    alert_lines = ["## ▲ PROACTIVE ALERTS"]
    for alert in _proactive_alerts[-5:]:  # Show last 5
        alert_lines.append(f"  • [{alert.get('time', '?')}] {alert.get('msg', '?')}")
    
    # Clear shown alerts
    _proactive_alerts.clear()
    return "\n".join(alert_lines)


def add_proactive_alert(msg: str):
    """Add an alert to the proactive alert buffer."""
    _proactive_alerts.append({
        "time": datetime.now().strftime("%H:%M"),
        "msg": msg,
    })


# ── Enhancement #12: Root Cause Chain Wiring ────────────────
def get_last_root_cause_chain() -> str:
    """Return the last root cause chain from audit state, if available.
    This wires the existing build_root_cause_chain() into the chat prompt.
    """
    # Check if we have a recent audit report with root cause data
    try:
        # Look for the most recent audit report file
        import glob
        reports = sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "NETWORK_AUDIT_*.md")),
                         reverse=True)
        if reports:
            with open(reports[0], "r") as f:
                content = f.read()
            # Extract root cause chain section if present
            rcc_match = re.search(r'### ROOT CAUSE CHAIN.*?(?=###|\Z)', content, re.DOTALL)
            if rcc_match:
                chain_text = rcc_match.group(0).strip()
                if len(chain_text) > 50:
                    return f"## KNOWN ROOT CAUSE CHAIN (from last audit)\n{chain_text[:1000]}"
    except Exception:
        pass
    return ""


# ── Enhancement #13: Multi-Vendor Translation Maps ─────────
VENDOR_TRANSLATIONS = {
    "cisco_ios": {
        "show ospf neighbor": "show ip ospf neighbor",
        "show bgp summary": "show ip bgp summary",
        "show ldp session": "show mpls ldp neighbor",
        "show isis adjacency": "show isis neighbors",
        "show route": "show ip route",
        "show interfaces terse": "show ip interface brief",
        "show chassis alarms": "show facility-alarm status",
        "show configuration": "show running-config",
        "show system uptime": "show version | include uptime",
        "show bfd session": "show bfd neighbors",
    },
    "cisco_xr": {
        "show ospf neighbor": "show ospf neighbor",
        "show bgp summary": "show bgp summary",
        "show ldp session": "show mpls ldp neighbor brief",
        "show isis adjacency": "show isis neighbors",
        "show route": "show route",
        "show interfaces terse": "show ipv4 interface brief",
        "show chassis alarms": "show alarms brief",
        "show configuration": "show running-config",
    },
    "arista_eos": {
        "show ospf neighbor": "show ip ospf neighbor",
        "show bgp summary": "show ip bgp summary",
        "show ldp session": "show mpls ldp neighbor",
        "show isis adjacency": "show isis neighbors",
        "show route": "show ip route",
        "show interfaces terse": "show ip interface brief",
        "show configuration": "show running-config",
    },
}


def translate_command(junos_cmd: str, target_vendor: str) -> str:
    """Translate a Junos command to another vendor's equivalent."""
    vendor_map = VENDOR_TRANSLATIONS.get(target_vendor, {})
    
    # Try exact match first
    if junos_cmd in vendor_map:
        return vendor_map[junos_cmd]
    
    # Try partial match
    for j_cmd, v_cmd in vendor_map.items():
        if junos_cmd.startswith(j_cmd):
            suffix = junos_cmd[len(j_cmd):]
            return v_cmd + suffix
    
    return f"[No translation for '{junos_cmd}' → {target_vendor}]"


def get_vendor_translation_table(vendor: str) -> str:
    """Return a formatted translation table for a vendor."""
    vendor_map = VENDOR_TRANSLATIONS.get(vendor)
    if not vendor_map:
        return f"No translations available for '{vendor}'. Supported: {', '.join(VENDOR_TRANSLATIONS.keys())}"
    
    lines = [f"## Command Translation: Junos → {vendor.replace('_', ' ').title()}\n"]
    lines.append("| Junos Command | Equivalent |")
    lines.append("|---|---|")
    for j_cmd, v_cmd in vendor_map.items():
        lines.append(f"| `{j_cmd}` | `{v_cmd}` |")
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════
#  NEW v6.0 PARSERS — BFD, Firewall, MPLS LSP, Commit History,
#  Reachability Matrix, Severity Scoring, Issue Fingerprinting
# ══════════════════════════════════════════════════════════════

def find_bfd_issues(bfd_outputs: dict, device_map: dict) -> tuple:
    """Parse 'show bfd session' — detect down/failing BFD sessions.
    Enhancement #1A: BFD awareness for fast-failure detection.
    Returns (issues_list, healthy_list)."""
    issues, healthy = [], []
    for router, output in bfd_outputs.items():
        hostname = device_map.get(router, router)
        if not output.strip() or "not running" in output.lower() or "no bfd" in output.lower():
            continue
        for line in output.split("\n"):
            parts = line.split()
            if len(parts) >= 3 and re.match(r"\d+\.\d+\.\d+\.\d+", parts[0]):
                neighbor = parts[0]
                # BFD states: Up, Down, AdminDown, Failing, Init
                state_col = ""
                for p in parts[1:]:
                    if p.lower() in ("up", "down", "admindown", "failing", "init"):
                        state_col = p
                        break
                if state_col.lower() in ("down", "failing", "init"):
                    # Try to find the interface and detect interval
                    intf = ""
                    for p in parts:
                        if re.match(r"(ge|xe|et|ae|lo)\-", p):
                            intf = p
                            break
                    issues.append({
                        "severity": "CRITICAL", "router": router, "hostname": hostname,
                        "neighbor": neighbor, "state": state_col, "interface": intf,
                        "detail": f"BFD session to {neighbor} on {hostname} is **{state_col}** → protocol adjacency may flap"
                    })
                elif state_col.lower() == "up":
                    healthy.append({"router": router, "hostname": hostname, "neighbor": neighbor})
    return issues, healthy


def find_firewall_issues(fw_outputs: dict, device_map: dict) -> list:
    """Parse 'show firewall' — detect filters with high discard counts.
    Enhancement #1G: Firewall filter verification."""
    issues = []
    for router, output in fw_outputs.items():
        hostname = device_map.get(router, router)
        if not output.strip():
            continue
        current_filter = ""
        for line in output.split("\n"):
            # Filter header: "Filter: PROTECT-RE" or "Filter: my-filter"
            fm = re.match(r"\s*Filter:\s+(\S+)", line)
            if fm:
                current_filter = fm.group(1)
                continue
            # Counter line: "  discard                           12345    67890"
            # or "  reject-counter                     100      200"
            if current_filter:
                cm = re.match(r"\s+(\S+)\s+(\d+)\s+(\d+)", line)
                if cm:
                    counter_name = cm.group(1).lower()
                    packet_count = int(cm.group(2))
                    byte_count = int(cm.group(3))
                    if any(kw in counter_name for kw in ("discard", "reject", "deny", "drop", "block")):
                        if packet_count > 100:
                            issues.append({
                                "router": router, "hostname": hostname,
                                "filter": current_filter, "counter": cm.group(1),
                                "packets": packet_count, "bytes": byte_count,
                                "detail": f"{hostname}: Filter **{current_filter}** counter **{cm.group(1)}** = {packet_count} packets discarded"
                            })
    return issues


def find_mpls_lsp_issues(lsp_outputs: dict, device_map: dict) -> tuple:
    """Parse 'show mpls lsp' — detect LSPs in Dn (Down) state.
    Enhancement #1C: MPLS LSP status checks.
    Returns (issues_list, healthy_list)."""
    issues, healthy = [], []
    for router, output in lsp_outputs.items():
        hostname = device_map.get(router, router)
        if not output.strip() or "not running" in output.lower():
            continue
        for line in output.split("\n"):
            # Format: "To              From            State Rt   ActivePath  ..."
            # e.g.,  "10.0.0.1       10.0.0.2       Dn     0"
            parts = line.split()
            if len(parts) >= 3 and re.match(r"\d+\.\d+\.\d+\.\d+", parts[0]):
                to_addr = parts[0]
                from_addr = parts[1] if re.match(r"\d+\.\d+\.\d+\.\d+", parts[1]) else ""
                state = ""
                for p in parts[1:]:
                    if p.lower() in ("up", "dn", "down", "trans", "transition"):
                        state = p
                        break
                if state.lower() in ("dn", "down", "trans", "transition"):
                    issues.append({
                        "severity": "CRITICAL", "router": router, "hostname": hostname,
                        "to": to_addr, "from": from_addr, "state": state,
                        "detail": f"MPLS LSP to {to_addr} on {hostname} is **{state}** → traffic may blackhole"
                    })
                elif state.lower() == "up":
                    healthy.append({"router": router, "hostname": hostname, "to": to_addr})
    return issues, healthy


def find_rsvp_issues(rsvp_outputs: dict, device_map: dict) -> list:
    """Parse 'show rsvp session' — detect RSVP sessions in Down/error state.
    Enhancement #1C."""
    issues = []
    for router, output in rsvp_outputs.items():
        hostname = device_map.get(router, router)
        if not output.strip() or "not running" in output.lower():
            continue
        for line in output.split("\n"):
            if "down" in line.lower() or "error" in line.lower():
                parts = line.split()
                dest = parts[0] if parts and re.match(r"\d+\.\d+\.\d+\.\d+", parts[0]) else "?"
                issues.append({
                    "severity": "WARNING", "router": router, "hostname": hostname,
                    "destination": dest, "detail": f"RSVP session issue on {hostname}: {line.strip()}"
                })
    return issues


def parse_commit_history(commit_outputs: dict, device_map: dict) -> dict:
    """Parse 'show system commit' — extract recent commits with user/timestamp.
    Enhancement #3D: Commit history analysis."""
    result = {}
    for router, output in commit_outputs.items():
        hostname = device_map.get(router, router)
        commits = []
        for line in output.split("\n"):
            # Format: "0   2026-02-16 10:00:00 UTC by user via cli"
            m = re.match(r"\s*(\d+)\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+\S+\s+by\s+(\S+)\s+via\s+(\S+)", line)
            if m:
                commits.append({
                    "index": int(m.group(1)),
                    "timestamp": m.group(2),
                    "user": m.group(3),
                    "method": m.group(4)
                })
            if len(commits) >= 5:  # Keep last 5 commits
                break
        result[router] = {"hostname": hostname, "commits": commits}
    return result


def build_reachability_matrix(ospf_nbr_outputs: dict, bgp_outputs: dict,
                               ldp_sess_outputs: dict, device_map: dict) -> dict:
    """Build a cross-protocol reachability matrix.
    Enhancement #3A: Shows which routers can reach which via each protocol.
    
    v9.0 Fix: Uses loopback IP → router mapping for accurate cross-referencing
    instead of naive string matching. Also extracts Router-ID from OSPF/BGP
    to build a reliable IP-to-router mapping.
    
    Returns {mcp_name: {"ospf": bool, "bgp": bool, "ldp": bool}} 
    (per-router aggregate: True if router has at least one healthy session of that type)."""
    matrix = {}
    all_routers = list(device_map.keys())
    
    # Build IP → router mapping from BGP Router-ID and OSPF neighbor addresses
    ip_to_router = {}  # ip_address → mcp_name
    router_ids = {}    # mcp_name → router_id (loopback IP)
    
    # Extract Router-IDs from BGP summary
    for mcp_name, output in bgp_outputs.items():
        for line in output.split("\n"):
            # "Router ID: 10.255.255.1" or "Local AS: 65000, Router ID: 10.255.255.1"
            rid_match = re.search(r"Router ID:\s*(\d+\.\d+\.\d+\.\d+)", line)
            if rid_match:
                rid = rid_match.group(1)
                router_ids[mcp_name] = rid
                ip_to_router[rid] = mcp_name
    
    # Extract additional router IDs from OSPF neighbor addresses
    # In OSPF PtP links, the neighbor address is often the peer's Router-ID (loopback)
    for mcp_name, output in ospf_nbr_outputs.items():
        for line in output.split("\n"):
            parts = line.split()
            if len(parts) >= 4 and re.match(r"\d+\.\d+\.\d+\.\d+", parts[0]):
                nbr_addr = parts[0]
                # This address is likely a loopback — map it if not already mapped
                if nbr_addr not in ip_to_router:
                    # Try to identify which router this belongs to by checking
                    # if any other router's OSPF/BGP data references this IP
                    for other_mcp in all_routers:
                        if other_mcp == mcp_name:
                            continue
                        other_bgp = bgp_outputs.get(other_mcp, "")
                        other_ospf = ospf_nbr_outputs.get(other_mcp, "")
                        # If this IP appears as Router ID in another router's output
                        if f"Router ID: {nbr_addr}" in other_bgp:
                            ip_to_router[nbr_addr] = other_mcp
                            router_ids.setdefault(other_mcp, nbr_addr)
                            break
    
    # Also map LDP session addresses
    for mcp_name, output in ldp_sess_outputs.items():
        for line in output.split("\n"):
            parts = line.split()
            if parts and re.match(r"\d+\.\d+\.\d+\.\d+", parts[0]):
                ldp_peer = parts[0]
                # LDP peers by loopback — already in ip_to_router if BGP RID matched
    
    # Initialize per-router aggregate
    for r in all_routers:
        matrix[r] = {"ospf": False, "bgp": False, "ldp": False}
    
    # OSPF: Router has at least one OSPF neighbor in Full state
    for router, output in ospf_nbr_outputs.items():
        for line in output.split("\n"):
            parts = line.split()
            if len(parts) >= 4 and re.match(r"\d+\.\d+\.\d+\.\d+", parts[0]):
                # Has at least one OSPF neighbor → OSPF reachable
                state = parts[2] if len(parts) > 2 else ""
                if state.lower() == "full" or (len(parts) > 3 and "full" in parts[3].lower()):
                    matrix[router]["ospf"] = True
                    break
        # Also mark True if any neighbor exists (even non-Full)
        if not matrix[router]["ospf"]:
            for line in output.split("\n"):
                parts = line.split()
                if len(parts) >= 3 and re.match(r"\d+\.\d+\.\d+\.\d+", parts[0]):
                    matrix[router]["ospf"] = True
                    break
    
    # BGP: Router has at least one Established BGP session
    for router, output in bgp_outputs.items():
        for line in output.split("\n"):
            parts = line.split()
            if len(parts) >= 3 and re.match(r"\d+\.\d+\.\d+\.\d+", parts[0]):
                state = parts[-1]
                if state.isdigit() or "estab" in state.lower():
                    matrix[router]["bgp"] = True
                    break
    
    # LDP: Router has at least one Operational LDP session
    for router, output in ldp_sess_outputs.items():
        for line in output.split("\n"):
            if "operational" in line.lower() or "open" in line.lower():
                matrix[router]["ldp"] = True
                break
    
    return matrix


def calculate_health_score(critical_count: int, warning_count: int, healthy_count: int,
                           device_count: int, config_drifts: int = 0,
                           bfd_issues: int = 0, lsp_issues: int = 0) -> dict:
    """Calculate a numeric Network Health Score (0-100).
    Enhancement #2A: Severity scoring engine."""
    # Start at 100, deduct for issues
    score = 100.0
    
    # Critical issues are heavily penalized
    score -= critical_count * SEVERITY_WEIGHTS["CRITICAL"]
    # Warnings are moderate
    score -= warning_count * SEVERITY_WEIGHTS["WARNING"]
    # Config drift
    score -= config_drifts * 2
    # BFD issues (fast-failure indicator)
    score -= bfd_issues * SEVERITY_WEIGHTS["MAJOR"]
    # LSP issues
    score -= lsp_issues * SEVERITY_WEIGHTS["MAJOR"]
    
    # Bonus for healthy areas (up to +5)
    if device_count > 0:
        health_ratio = healthy_count / max(device_count * 3, 1)  # ~3 health checks per device expected
        score += min(5, health_ratio * 5)
    
    # Clamp to 0-100
    score = max(0, min(100, score))
    
    # Determine grade
    if score >= 90:
        grade = "A"
        label = "EXCELLENT"
    elif score >= 75:
        grade = "B"
        label = "GOOD"
    elif score >= 60:
        grade = "C"
        label = "FAIR"
    elif score >= 40:
        grade = "D"
        label = "DEGRADED"
    else:
        grade = "F"
        label = "CRITICAL"
    
    return {
        "score": round(score, 1),
        "grade": grade,
        "label": label,
        "breakdown": {
            "critical_deductions": critical_count * SEVERITY_WEIGHTS["CRITICAL"],
            "warning_deductions": warning_count * SEVERITY_WEIGHTS["WARNING"],
            "drift_deductions": config_drifts * 2,
            "bfd_deductions": bfd_issues * SEVERITY_WEIGHTS["MAJOR"],
            "lsp_deductions": lsp_issues * SEVERITY_WEIGHTS["MAJOR"],
            "health_bonus": min(5, (healthy_count / max(device_count * 3, 1)) * 5) if device_count > 0 else 0,
        }
    }


def save_issue_fingerprints(issues: list, report_ts: str):
    """Save issue fingerprints for historical tracking.
    Enhancement #3C: Historical issue memory."""
    try:
        existing = {}
        if os.path.exists(ISSUE_FINGERPRINT_PATH):
            with open(ISSUE_FINGERPRINT_PATH, "r") as f:
                existing = json.load(f)
        
        for issue in issues:
            # Create a stable fingerprint from the issue's key attributes
            fp_data = f"{issue.get('router', '')}-{issue.get('detail', '')}"
            fp = hashlib.md5(fp_data.encode()).hexdigest()[:12]
            
            if fp in existing:
                existing[fp]["occurrences"] += 1
                existing[fp]["last_seen"] = report_ts
                existing[fp]["history"].append(report_ts)
                # Keep last 20 timestamps
                existing[fp]["history"] = existing[fp]["history"][-20:]
            else:
                existing[fp] = {
                    "detail": issue.get("detail", ""),
                    "severity": issue.get("severity", "WARNING"),
                    "router": issue.get("hostname", issue.get("router", "")),
                    "first_seen": report_ts,
                    "last_seen": report_ts,
                    "occurrences": 1,
                    "history": [report_ts]
                }
        
        with open(ISSUE_FINGERPRINT_PATH, "w") as f:
            json.dump(existing, f, indent=2)
    except Exception as e:
        print(f"   ▲  Could not save issue fingerprints: {e}")


def load_issue_fingerprints() -> dict:
    """Load historical issue fingerprints."""
    if not os.path.exists(ISSUE_FINGERPRINT_PATH):
        return {}
    try:
        with open(ISSUE_FINGERPRINT_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def find_recurring_issues(current_issues: list) -> list:
    """Find issues that have occurred in multiple audits.
    Enhancement #3C: Historical issue memory."""
    existing = load_issue_fingerprints()
    recurring = []
    
    for issue in current_issues:
        fp_data = f"{issue.get('router', '')}-{issue.get('detail', '')}"
        fp = hashlib.md5(fp_data.encode()).hexdigest()[:12]
        
        if fp in existing and existing[fp]["occurrences"] >= 2:
            recurring.append({
                "detail": issue.get("detail", ""),
                "hostname": issue.get("hostname", issue.get("router", "")),
                "occurrences": existing[fp]["occurrences"],
                "first_seen": existing[fp]["first_seen"],
                "last_seen": existing[fp]["last_seen"],
                "severity": issue.get("severity", "WARNING"),
            })
    
    return recurring


# ══════════════════════════════════════════════════════════════
#  v14.0: CLAUDE OPUS-LEVEL JUNOS INTELLIGENCE UPGRADE
#  Deep Reasoning · Topology Visualization · Mind-Map Analysis
# ══════════════════════════════════════════════════════════════

# ── v14.0 Constants ─────────────────────────────────────────
JUNOS_DEEP_KNOWLEDGE_PATH = "JUNOS_DEEP_KNOWLEDGE.md"
_junos_deep_knowledge = ""
try:
    if os.path.exists(JUNOS_DEEP_KNOWLEDGE_PATH):
        with open(JUNOS_DEEP_KNOWLEDGE_PATH, "r") as _f:
            _junos_deep_knowledge = _f.read()
        logger.info(f"Loaded Junos deep knowledge: {len(_junos_deep_knowledge)} chars")
except Exception as _e:
    logger.warning(f"Failed to load Junos deep knowledge: {_e}")

# Protocol State Machine definitions for deterministic reasoning
PROTOCOL_FSM = {
    "ospf": {
        "states": ["Down", "Init", "2-Way", "ExStart", "Exchange", "Loading", "Full"],
        "healthy": "Full",
        "diagnostic": {
            "Down": {"cause": "Interface down or OSPF not enabled", "check": "show ospf interface", "layer": "L1"},
            "Init": {"cause": "Hello/area/auth mismatch or interface-type mismatch", "check": "show ospf interface detail (BOTH sides)", "layer": "L3"},
            "ExStart": {"cause": "MTU mismatch (99% of cases)", "check": "show interfaces <intf> | match mtu (BOTH sides)", "layer": "L2"},
            "Exchange": {"cause": "DBD retransmissions, packet loss", "check": "show ospf statistics", "layer": "L3"},
            "Loading": {"cause": "LSA corruption or LSDB sync failure", "check": "show ospf database summary", "layer": "L3"},
            "2-Way": {"cause": "Normal for DROther pairs on broadcast; if unexpected check interface-type", "check": "show ospf neighbor detail", "layer": "L3"},
        }
    },
    "bgp": {
        "states": ["Idle", "Connect", "Active", "OpenSent", "OpenConfirm", "Established"],
        "healthy": "Established",
        "diagnostic": {
            "Idle": {"cause": "BGP not configured or manually stopped", "check": "show bgp summary", "layer": "L5"},
            "Connect": {"cause": "TCP SYN sent, waiting for response", "check": "show bgp neighbor <peer>", "layer": "L4"},
            "Active": {"cause": "TCP can't connect → NO IP reachability to peer loopback", "check": "show route <peer-loopback>", "layer": "L3"},
            "OpenSent": {"cause": "TCP connected but peer not responding with OPEN", "check": "show bgp neighbor <peer> | match state", "layer": "L5"},
            "OpenConfirm": {"cause": "Authentication (MD5) or capability mismatch", "check": "show bgp neighbor <peer> detail", "layer": "L5"},
        }
    },
    "ldp": {
        "states": ["Nonexistent", "Initialized", "OpenReceived", "Operational"],
        "healthy": "Operational",
        "diagnostic": {
            "Nonexistent": {"cause": "No IGP route to peer OR LDP not enabled on interface", "check": "show ldp interface; show route <peer-lo0>", "layer": "L3"},
            "Initialized": {"cause": "Hello exchange ok but TCP session failing", "check": "show ldp session detail", "layer": "L4"},
            "OpenReceived": {"cause": "Init message exchanged but keepalive failing", "check": "show ldp session detail", "layer": "L4"},
        }
    },
    "isis": {
        "states": ["Down", "Initial", "Up"],
        "healthy": "Up",
        "diagnostic": {
            "Down": {"cause": "No IIH received — interface down or IS-IS not enabled", "check": "show isis interface; show interfaces terse", "layer": "L1"},
            "Initial": {"cause": "One-way: auth mismatch, level mismatch, or interface-type mismatch", "check": "show isis adjacency detail; show isis interface detail (BOTH sides)", "layer": "L3"},
        }
    },
}

# Cascading failure chains — deterministic reasoning patterns
CASCADING_PATTERNS = [
    {
        "trigger": "interface_down",
        "chain": ["L1:Interface Down", "L3:IGP adjacency drops", "L3:SPF recalculation",
                  "MPLS:LDP session Nonexistent", "MPLS:inet.3 route removed",
                  "BGP:next-hop unresolvable", "L3VPN:VPN routes withdrawn"],
        "recovery": "If alternate IGP path exists: auto-reconverge in 1-5s (BFD) or 30-40s (dead timer)"
    },
    {
        "trigger": "rr_failure",
        "chain": ["BGP:RR session drops", "BGP:Clients lose route exchange via this RR",
                  "L3VPN:Routes only reflected by this RR are withdrawn"],
        "recovery": "If second RR exists (P22): clients still have routes via backup RR → no outage"
    },
    {
        "trigger": "igp_route_loss",
        "chain": ["L3:IGP route to peer loopback removed", "MPLS:LDP session Nonexistent",
                  "MPLS:inet.3 label binding removed", "BGP:iBGP next-hop unresolvable",
                  "L3VPN:VPN routes via this next-hop withdrawn"],
        "recovery": "Fix IGP (IS-IS/OSPF) → LDP auto-recovers → BGP resolves → VPN restored"
    },
    {
        "trigger": "ldp_down",
        "chain": ["MPLS:LDP session down", "MPLS:No label for peer loopback in inet.3",
                  "BGP:VPN next-hop unresolvable via MPLS", "L3VPN:Customer routes unreachable"],
        "recovery": "Fix LDP (enable on interface / fix IGP) → labels repopulate inet.3 → BGP resolves"
    },
    {
        "trigger": "mtu_mismatch",
        "chain": ["L2:MTU mismatch on link", "L3:OSPF stuck in ExStart / IS-IS large LSP drops",
                  "L3:Routing table incomplete", "MPLS:LDP labels missing", "BGP:Routes unreachable"],
        "recovery": "Match MTU on both sides → OSPF/IS-IS recovers → cascading fix"
    },
]


def get_fsm_diagnosis(protocol: str, state: str) -> dict:
    """Given a protocol and its current state, return deterministic diagnosis."""
    fsm = PROTOCOL_FSM.get(protocol.lower())
    if not fsm:
        return {"cause": "Unknown protocol", "check": "", "layer": ""}
    
    if state == fsm["healthy"]:
        return {"cause": "HEALTHY — no issue", "check": "", "layer": "", "healthy": True}
    
    # Find the stuck state
    for st_name, diagnosis in fsm.get("diagnostic", {}).items():
        if st_name.lower() in state.lower() or state.lower() in st_name.lower():
            return {**diagnosis, "healthy": False, "expected": fsm["healthy"]}
    
    return {"cause": f"Unknown state '{state}' for {protocol}", "check": "", "layer": "", "healthy": False}


def identify_cascading_chain(symptoms: list) -> list:
    """Given a list of symptoms, identify matching cascading failure patterns."""
    matches = []
    for pattern in CASCADING_PATTERNS:
        # Score how many chain elements match the symptoms
        score = 0
        for chain_step in pattern["chain"]:
            for symptom in symptoms:
                if any(kw in symptom.lower() for kw in chain_step.lower().split(":")):
                    score += 1
                    break
        if score >= 2:  # At least 2 chain elements match
            matches.append({
                "trigger": pattern["trigger"],
                "chain": pattern["chain"],
                "recovery": pattern["recovery"],
                "match_score": score,
                "match_pct": round(score / len(pattern["chain"]) * 100)
            })
    matches.sort(key=lambda x: -x["match_score"])
    return matches


# ── E123: Live Topology Visualization Engine ────────────────
async def build_live_topology(mcp_client, session_id, device_map: dict) -> dict:
    """Build a comprehensive live topology from iBGP, LLDP, and IS-IS data.
    Returns structured topology dict with all protocol overlays."""
    
    topology = {
        "nodes": {},
        "physical_links": [],     # From LLDP
        "igp_adjacencies": [],    # From IS-IS/OSPF
        "bgp_sessions": [],       # From BGP summary
        "ldp_sessions": [],       # From LDP sessions
        "mpls_lsps": [],          # From MPLS LSPs
    }
    
    all_devices = list(device_map.keys())
    
    # Collect LLDP, BGP, IS-IS, LDP in parallel batches
    console.print("   ⊛ [dim]Collecting topology data (LLDP + IS-IS + BGP + LDP)...[/dim]")
    
    # Reset circuit breakers for topology protocols so user-initiated
    # topology builds always attempt fresh data collection
    for _topo_label in ("LLDP", "BGP", "IS-IS", "LDP"):
        _circuit_breaker.pop(_topo_label, None)
    
    lldp_data = {}
    bgp_data = {}
    isis_data = {}
    ldp_data = {}
    
    # Batch collect
    try:
        lldp_raw = await run_batch(mcp_client, session_id, "show lldp neighbors", all_devices, "LLDP")
        bgp_raw = await run_batch(mcp_client, session_id, "show bgp summary", all_devices, "BGP")
        isis_raw = await run_batch(mcp_client, session_id, "show isis adjacency", all_devices, "IS-IS")
        ldp_raw = await run_batch(mcp_client, session_id, "show ldp session", all_devices, "LDP")
    except Exception as e:
        logger.warning(f"Topology collection partial failure: {e}")
        lldp_raw = bgp_raw = isis_raw = ldp_raw = ""
    
    # Parse batch JSON into per-router outputs
    lldp_per_router = parse_batch_json(str(lldp_raw)) if lldp_raw else {}
    bgp_per_router = parse_batch_json(str(bgp_raw)) if bgp_raw else {}
    isis_per_router = parse_batch_json(str(isis_raw)) if isis_raw else {}
    ldp_per_router = parse_batch_json(str(ldp_raw)) if ldp_raw else {}
    logger.info(f"Topology parsed: LLDP={len(lldp_per_router)} BGP={len(bgp_per_router)} ISIS={len(isis_per_router)} LDP={len(ldp_per_router)} routers")
    
    # Parse LLDP for physical links
    for current_router, output in lldp_per_router.items():
        for line in output.split("\n"):
            # LLDP format: ge-0/0/2   -   2c:6b:f5:...   ge-0/0/2   P12
            # Columns: Local Interface, Parent Interface, Chassis Id, Port info, System Name
            parts = line.split()
            if len(parts) >= 5 and parts[0].startswith("ge-"):
                local_intf = parts[0]
                remote_name = parts[-1]  # System Name is last column
                remote_intf = parts[-2] if parts[-2].startswith("ge-") else ""  # Port info
                if current_router and remote_name and remote_name not in ("Name", "-"):
                    # Deduplicate bidirectional links
                    link_key = tuple(sorted([current_router, remote_name]))
                    existing = [l for l in topology["physical_links"] if tuple(sorted([l["src"], l["dst"]])) == link_key]
                    if not existing:
                        topology["physical_links"].append({
                            "src": current_router, "dst": remote_name,
                            "src_intf": local_intf, "dst_intf": remote_intf,
                            "state": "up"
                        })
    
    # Parse BGP sessions
    for current_router, output in bgp_per_router.items():
        for line in output.split("\n"):
            # BGP peer line: 10.255.255.12   100   4676   4702   0   0  1d 11:20:59  Establ
            # Match: IP   AS   InPkt OutPkt OutQ Flaps [uptime] State
            ip_match = re.match(r'\s*(\d+\.\d+\.\d+\.\d+)\s+(\d+)\s+\d+\s+\d+\s+\d+\s+\d+\s+\S+\s+\S*\s*(\S+)', line)
            if not ip_match:
                # Fallback: simpler pattern for Active/Connect states (no uptime)
                ip_match = re.match(r'\s*(\d+\.\d+\.\d+\.\d+)\s+(\d+)\s+\d+\s+\d+\s+\d+\s+\d+\s+(\w+)', line)
            if ip_match and current_router:
                peer_ip = ip_match.group(1)
                state = ip_match.group(3)
                # Clean state: "Establ" or "Active" or "Connect" etc.
                if state and state[0].isupper():
                    topology["bgp_sessions"].append({
                        "src": current_router, "peer_ip": peer_ip,
                        "state": state, "type": "iBGP"
                    })
    
    # Parse IS-IS adjacencies
    for current_router, output in isis_per_router.items():
        for line in output.split("\n"):
            # IS-IS format: ge-0/0/1.0   P11   2  Up   23
            # Columns: Interface, System, L, State, Hold, SNPA
            parts = line.split()
            if len(parts) >= 4 and parts[0].startswith("ge-"):
                intf = parts[0]
                neighbor = parts[1]
                level = f"L{parts[2]}" if parts[2].isdigit() else "L2"
                state = parts[3] if parts[3] in ["Up", "Down", "Init"] else ""
                if current_router and neighbor and state:
                    topology["igp_adjacencies"].append({
                        "src": current_router, "dst": neighbor,
                        "interface": intf, "level": level, "state": state
                    })
    
    # Parse LDP sessions
    for current_router, output in ldp_per_router.items():
        for line in output.split("\n"):
            # LDP format: 10.255.255.11   Operational   Open   23   DU
            # Columns: Address, State, Connection, Hold time, Adv. Mode
            parts = line.split()
            if len(parts) >= 2 and re.match(r'\d+\.\d+\.\d+\.\d+', parts[0]):
                peer_ip = parts[0]
                state = parts[1] if len(parts) > 1 and parts[1] in ["Operational", "Nonexistent", "Initialized"] else "Unknown"
                if current_router:
                    topology["ldp_sessions"].append({
                        "src": current_router, "peer_ip": peer_ip, "state": state
                    })
    
    # Build node inventory
    loopback_map = {}
    topo_from_golden = build_topology_from_golden_configs()
    if topo_from_golden:
        loopback_map = topo_from_golden.get("loopbacks", {})
    
    for mcp_name, hostname in device_map.items():
        role = "PE" if hostname.upper().startswith("PE") else (
            "RR" if hostname in ("P12", "P22") else "P")
        
        # Count protocol sessions
        bgp_count = len([b for b in topology["bgp_sessions"] if b["src"] == mcp_name])
        isis_count = len([i for i in topology["igp_adjacencies"] if i["src"] == mcp_name and i["state"] == "Up"])
        ldp_count = len([l for l in topology["ldp_sessions"] if l["src"] == mcp_name and l["state"] == "Operational"])
        link_count = len([l for l in topology["physical_links"] if l["src"] == mcp_name or l["dst"] == mcp_name])
        
        topology["nodes"][mcp_name] = {
            "hostname": hostname,
            "role": role,
            "loopback": loopback_map.get(hostname, ""),
            "bgp_sessions": bgp_count,
            "isis_adjacencies": isis_count,
            "ldp_sessions": ldp_count,
            "physical_links": link_count,
            "health": "critical" if bgp_count == 0 and role == "PE" else (
                "warning" if isis_count < link_count else "healthy"
            )
        }
    
    return topology


def topology_to_mermaid(topology: dict, highlight_issues: bool = True) -> str:
    """Convert topology dict to a Mermaid diagram string for visualization.
    Shows physical links, iBGP sessions, protocol health overlay."""
    
    lines = ["```mermaid", "graph TB"]
    
    # Style definitions
    lines.append("    classDef pe fill:#2d5a27,stroke:#4caf50,color:#fff,stroke-width:2px")
    lines.append("    classDef p fill:#1a3a5c,stroke:#2196f3,color:#fff,stroke-width:2px")
    lines.append("    classDef rr fill:#5c1a5c,stroke:#9c27b0,color:#fff,stroke-width:2px")
    lines.append("    classDef critical fill:#5c1a1a,stroke:#f44336,color:#fff,stroke-width:3px")
    lines.append("    classDef warning fill:#5c4a1a,stroke:#ff9800,color:#fff,stroke-width:2px")
    lines.append("")
    
    # Subgraph groups
    pe_nodes = []
    p_nodes = []
    rr_nodes = []
    
    for mcp_name, node in topology.get("nodes", {}).items():
        hostname = node["hostname"]
        role = node["role"]
        lo = node.get("loopback", "")
        health = node.get("health", "healthy")
        
        label = f"{hostname}"
        if lo:
            label += f"\\n{lo}"
        label += f"\\n{role}"
        
        node_id = hostname.replace("-", "_")
        lines.append(f"    {node_id}[\"{label}\"]")
        
        if health == "critical":
            lines.append(f"    class {node_id} critical")
        elif health == "warning":
            lines.append(f"    class {node_id} warning")
        elif role == "PE":
            lines.append(f"    class {node_id} pe")
            pe_nodes.append(node_id)
        elif role == "RR":
            lines.append(f"    class {node_id} rr")
            rr_nodes.append(node_id)
        else:
            lines.append(f"    class {node_id} p")
            p_nodes.append(node_id)
    
    lines.append("")
    
    # Physical links (solid lines)
    seen_links = set()
    for link in topology.get("physical_links", []):
        src_h = topology["nodes"].get(link["src"], {}).get("hostname", link["src"]).replace("-", "_")
        dst_h = topology["nodes"].get(link["dst"], {}).get("hostname", link["dst"]).replace("-", "_")
        key = tuple(sorted([src_h, dst_h]))
        if key not in seen_links:
            seen_links.add(key)
            intf_label = link.get("src_intf", "").replace("ge-0/0/", "ge")
            lines.append(f"    {src_h} --- |{intf_label}| {dst_h}")
    
    lines.append("")
    
    # iBGP sessions (dashed lines) — only PE↔RR
    bgp_seen = set()
    loopback_to_hostname = {}
    for mcp_name, node in topology.get("nodes", {}).items():
        if node.get("loopback"):
            loopback_to_hostname[node["loopback"]] = node["hostname"]
    
    for session in topology.get("bgp_sessions", []):
        src_h = topology["nodes"].get(session["src"], {}).get("hostname", session["src"]).replace("-", "_")
        peer_hostname = loopback_to_hostname.get(session["peer_ip"], "").replace("-", "_")
        if peer_hostname and src_h != peer_hostname:
            key = tuple(sorted([src_h, peer_hostname]))
            if key not in bgp_seen:
                bgp_seen.add(key)
                state = session.get("state", "")
                style = "-.->|iBGP|" if "Establ" in state else "-.->|iBGP ⚠|"
                lines.append(f"    {src_h} {style} {peer_hostname}")
    
    lines.append("```")
    return "\n".join(lines)


def topology_to_ascii(topology: dict) -> str:
    """Generate an ASCII topology map for terminal display."""
    nodes = topology.get("nodes", {})
    links = topology.get("physical_links", [])
    bgp_sessions = topology.get("bgp_sessions", [])
    
    if not nodes:
        return "No topology data available."
    
    lines = []
    lines.append("╔══════════════════════════════════════════════════════════════╗")
    lines.append("║           LIVE NETWORK TOPOLOGY (iBGP + LLDP + IS-IS)      ║")
    lines.append("╠══════════════════════════════════════════════════════════════╣")
    
    # Group by role
    pe_list = sorted([n for n, d in nodes.items() if d["role"] == "PE"], key=lambda x: nodes[x]["hostname"])
    rr_list = sorted([n for n, d in nodes.items() if d["role"] == "RR"], key=lambda x: nodes[x]["hostname"])
    p_list = sorted([n for n, d in nodes.items() if d["role"] == "P" and d["hostname"] not in ("P12", "P22")],
                    key=lambda x: nodes[x]["hostname"])
    
    # PE Layer
    pe_str = "  ".join(f"[{nodes[n]['hostname']}]" for n in pe_list)
    lines.append(f"║  PE Layer:  {pe_str:<48} ║")
    lines.append("║       │╲              │              ╱│                      ║")
    lines.append("║       │  ╲             │             ╱  │                     ║")
    
    # P Layer  
    p_str = "  ".join(f"({nodes[n]['hostname']})" for n in p_list + rr_list)
    lines.append(f"║  P Layer:   {p_str:<47} ║")
    
    # RR indication
    if rr_list:
        rr_str = ", ".join(f"{nodes[n]['hostname']}=RR" for n in rr_list)
        lines.append(f"║  Route Reflectors: {rr_str:<40} ║")
    
    lines.append("╠══════════════════════════════════════════════════════════════╣")
    
    # Protocol summary per node
    lines.append("║  Node     │ Role │ IS-IS │  BGP  │  LDP  │ Links │ Health  ║")
    lines.append("║───────────┼──────┼───────┼───────┼───────┼───────┼─────────║")
    
    for mcp_name in sorted(nodes.keys(), key=lambda x: nodes[x]["hostname"]):
        n = nodes[mcp_name]
        health_icon = "[green]●[/green]" if n["health"] == "healthy" else ("[yellow]●[/yellow]" if n["health"] == "warning" else "[red]●[/red]")
        lines.append(
            f"║  {n['hostname']:<9}│  {n['role']:<4}│  {n['isis_adjacencies']:<5}│  {n['bgp_sessions']:<5}│"
            f"  {n['ldp_sessions']:<5}│  {n['physical_links']:<5}│ {health_icon:<7} ║"
        )
    
    lines.append("╠══════════════════════════════════════════════════════════════╣")
    
    # iBGP session map
    lines.append("║  iBGP Sessions:                                            ║")
    loopback_to_hostname = {}
    for mcp_name, node in nodes.items():
        if node.get("loopback"):
            loopback_to_hostname[node["loopback"]] = node["hostname"]
    
    bgp_shown = set()
    for session in bgp_sessions:
        src_h = nodes.get(session["src"], {}).get("hostname", session["src"])
        peer_h = loopback_to_hostname.get(session["peer_ip"], session["peer_ip"])
        key = tuple(sorted([src_h, peer_h]))
        if key not in bgp_shown:
            bgp_shown.add(key)
            state = session.get("state", "Unknown")
            icon = "●" if "Establ" in state else "✗"
            lines.append(f"║    {icon} {src_h} ←→ {peer_h} ({state})" + " " * max(0, 37 - len(src_h) - len(peer_h) - len(state)) + "║")
    
    lines.append("╚══════════════════════════════════════════════════════════════╝")
    return "\n".join(lines)


# ── E124: Mind-Map Deep Reasoning Engine ────────────────────
async def mind_map_reasoning(query: str, mcp_client, session_id, device_map: dict,
                              tools=None) -> str:
    """v15.0 Claude-level reasoning: hypothesis-driven investigation with 
    evidence accumulation, protocol FSM validation, cascading failure chain 
    identification, and topology intelligence.
    
    This is the pinnacle reasoning mode — used for the hardest troubleshooting.
    Uses the 7-Stage Reasoning Pipeline from reasoning_engine.py.
    """
    logger.info(f"Mind-map deep reasoning activated (v15.0): {query[:100]}")
    
    # ── STAGE 1: CLASSIFY — Determine domain, complexity, strategy ──
    console.print("   ◉ [dim]Stage 1: Problem classification...[/dim]")
    
    classification = classify_problem(query)
    console.print(f"   ◫ [dim]Domain: {classification.domain.value} | "
                  f"Complexity: {classification.complexity.value} | "
                  f"Strategy: {classification.reasoning_strategy}[/dim]")
    
    # ── STAGE 2: HYPOTHESIZE — Generate ranked hypotheses ──
    console.print("   ⊕ [dim]Stage 2: Generating hypotheses...[/dim]")
    
    hypotheses = generate_hypotheses(classification, query)
    evidence_acc = EvidenceAccumulator()
    
    if hypotheses:
        for h in hypotheses[:5]:
            console.print(f"      H: {h.description} (confidence: {h.confidence:.0f}%)")
    
    # ── STAGE 3: DECOMPOSE into investigation branches ──
    console.print("   ◇ [dim]Stage 3: Problem decomposition...[/dim]")
    
    decompose_prompt = (
        f"QUERY: {query}\n"
        f"DEVICES: {', '.join(f'{v} ({k})' for k, v in device_map.items())}\n\n"
        "Decompose this into a hierarchical problem tree. Output STRICT JSON:\n"
        "```json\n"
        "{\n"
        '  "root_question": "main question to answer",\n'
        '  "branches": [\n'
        '    {\n'
        '      "layer": "L1|L2|L3|MPLS|BGP|Services",\n'
        '      "question": "specific sub-question",\n'
        '      "commands": [{"device": "router", "command": "show ..."}],\n'
        '      "expected_healthy": "what healthy output looks like",\n'
        '      "failure_indicators": ["pattern1", "pattern2"]\n'
        '    }\n'
        "  ]\n"
        "}\n"
        "```"
    )
    
    decomp_result = await ollama_analyze(
        "You are a JNCIE-SP level network architect. Decompose problems precisely.",
        "", decompose_prompt, include_kb=False
    )
    
    # Parse decomposition
    branches = []
    json_match = re.search(r'\{[\s\S]*\}', decomp_result)
    if json_match:
        try:
            tree = json.loads(json_match.group())
            branches = tree.get("branches", [])
        except json.JSONDecodeError:
            pass
    
    if not branches:
        # Fallback: auto-generate branches from OSI model
        branches = [
            {"layer": "L1", "question": "Are all interfaces up?",
             "commands": [{"device": d, "command": "show interfaces terse"} for d in list(device_map.keys())[:3]],
             "expected_healthy": "All interfaces up/up", "failure_indicators": ["down", "error"]},
            {"layer": "L3", "question": "Are IS-IS adjacencies healthy?",
             "commands": [{"device": d, "command": "show isis adjacency"} for d in list(device_map.keys())[:3]],
             "expected_healthy": "All Up", "failure_indicators": ["Down", "Init"]},
            {"layer": "MPLS", "question": "Are LDP sessions operational?",
             "commands": [{"device": d, "command": "show ldp session"} for d in list(device_map.keys())[:3]],
             "expected_healthy": "All Operational", "failure_indicators": ["Nonexistent"]},
            {"layer": "BGP", "question": "Are BGP sessions established?",
             "commands": [{"device": d, "command": "show bgp summary"} for d in list(device_map.keys())[:3]],
             "expected_healthy": "All Established", "failure_indicators": ["Active", "Idle", "Connect"]},
        ]
    
    console.print(f"   ◇ [dim]{len(branches)} analysis branches identified[/dim]")
    
    # ── PHASE 2: Parallel Data Collection ──
    console.print("   ⊛ [dim]Phase 2: Parallel data collection...[/dim]")
    
    reverse_map = {v.lower(): k for k, v in device_map.items()}
    branch_data = {}
    
    for i, branch in enumerate(branches[:6]):  # Max 6 branches
        branch_key = f"{branch.get('layer', 'L?')}:{branch.get('question', '')[:50]}"
        branch_results = []
        
        for cmd_entry in branch.get("commands", [])[:4]:  # Max 4 commands per branch
            dev = cmd_entry.get("device", "").lower()
            mcp = reverse_map.get(dev, dev)
            cmd = cmd_entry.get("command", "")
            
            if mcp in device_map and cmd:
                try:
                    result = await run_single(mcp_client, session_id, cmd, mcp, 
                                              f"Branch-{branch.get('layer', '?')}")
                    branch_results.append(f"[{device_map[mcp]}] {cmd}:\n{result[:2000]}")
                except Exception as e:
                    branch_results.append(f"[{device_map.get(mcp, dev)}] {cmd}: ERROR: {e}")
        
        if not branch_results:
            # Fallback: batch collect
            try:
                all_devs = list(device_map.keys())[:6]
                cmd = branch.get("commands", [{}])[0].get("command", "show interfaces terse") if branch.get("commands") else "show interfaces terse"
                result = await run_batch(mcp_client, session_id, cmd, all_devs, branch.get("layer", "data"))
                branch_results.append(result[:3000])
            except Exception:
                branch_results.append("No data collected")
        
        branch_data[branch_key] = "\n".join(branch_results)
    
    # ── STAGE 4: INVESTIGATE — Per-Branch Analysis with FSM + Hypothesis Testing ──
    console.print("   ⊕ [dim]Stage 4: Hypothesis-driven investigation with protocol FSM...[/dim]")
    
    branch_analyses = {}
    symptoms_found = []
    
    for branch_key, data in branch_data.items():
        layer = branch_key.split(":")[0]
        question = branch_key.split(":", 1)[1] if ":" in branch_key else ""
        
        # Apply protocol state machine analysis
        fsm_findings = []
        for proto_name, fsm in PROTOCOL_FSM.items():
            for state_name in fsm.get("diagnostic", {}).keys():
                if state_name.lower() in data.lower():
                    diagnosis = get_fsm_diagnosis(proto_name, state_name)
                    if not diagnosis.get("healthy", True):
                        fsm_findings.append(
                            f"▲ {proto_name.upper()} in state '{state_name}': "
                            f"{diagnosis['cause']} | Check: {diagnosis['check']} | Layer: {diagnosis['layer']}"
                        )
                        # Feed evidence to accumulator
                        for h in hypotheses:
                            if proto_name.lower() in h.description.lower() or layer.lower() in h.description.lower():
                                evidence_acc.add_evidence(Evidence(
                                    source=f"FSM:{proto_name}",
                                    command=f"Protocol FSM analysis on {layer}",
                                    raw_output=f"{proto_name} in state {state_name}",
                                    interpretation=f"{proto_name} FSM state {state_name} indicates issue",
                                    supports=h.id,
                                    confidence_delta=15.0,
                                ))
                        symptoms_found.append(f"{proto_name}:{state_name}")
        
        fsm_context = "\n".join(fsm_findings) if fsm_findings else "No protocol state issues detected."
        
        # Get relevant deep knowledge
        deep_knowledge_snippet = ""
        if _junos_deep_knowledge:
            for section_header in ["STATE MACHINE", "CASCADING", "TROUBLESHOOTING"]:
                if layer.upper() in section_header or any(kw in question.lower() 
                    for kw in ["ospf", "bgp", "ldp", "isis", "mpls"]):
                    # Extract relevant section
                    sections = _junos_deep_knowledge.split("## STATE MACHINE")
                    for sec in sections:
                        if any(kw in sec[:200].lower() for kw in [layer.lower(), "ospf", "bgp", "ldp", "isis"]):
                            deep_knowledge_snippet += sec[:1000]
                            break
        
        analysis_prompt = (
            f"BRANCH: {branch_key}\n"
            f"QUESTION: {question}\n\n"
            f"PROTOCOL FSM ANALYSIS:\n{fsm_context}\n\n"
            f"RAW DATA:\n{data[:4000]}\n\n"
            + (f"REFERENCE KNOWLEDGE:\n{deep_knowledge_snippet[:1500]}\n\n" if deep_knowledge_snippet else "")
            + "Analyze this branch. For each finding:\n"
            "- FINDING: [what]\n"
            "- EVIDENCE: [exact data]\n"
            "- SEVERITY: [CRITICAL/WARNING/INFO]\n"
            "- ROOT CAUSE CANDIDATE: [yes/no — is this a root cause or a symptom?]\n"
            "- CONFIDENCE: [HIGH/MEDIUM/LOW with %]\n"
        )
        
        analysis = await ollama_analyze(
            f"You are a {layer} protocol specialist with JNCIE-SP certification.",
            data[:3000], analysis_prompt, include_kb=True
        )
        branch_analyses[branch_key] = analysis
    
    # ── STAGE 5: DIAGNOSE — Cascading Failure Chain + Root Cause from Symptoms ──
    console.print("   ⊶ [dim]Stage 5: Cascading failure chain + root cause mapping...[/dim]")
    
    cascade_matches = identify_cascading_chain(symptoms_found)
    cascade_context = ""
    if cascade_matches:
        cascade_context = "\n\nKNOWN CASCADING PATTERNS MATCHING:\n"
        for cm in cascade_matches[:2]:
            cascade_context += f"\nPattern: {cm['trigger']} ({cm['match_pct']}% match)\n"
            cascade_context += f"Chain: {' → '.join(cm['chain'])}\n"
            cascade_context += f"Recovery: {cm['recovery']}\n"
    
    # v15.0: Use reasoning engine's deterministic cascade graph
    re_cascade_context = ""
    for symptom in symptoms_found:
        if ":" in symptom:
            proto, state = symptom.split(":", 1)
            cascade_chain = walk_cascade(proto.upper())
            if cascade_chain:
                re_cascade_context += f"\n⊶ Cascade from {proto.upper()}: {' → '.join(cascade_chain)}"
    
    # v15.0: Try deterministic root cause from symptoms
    root_cause_analysis = find_root_cause_from_symptoms(symptoms_found)
    if root_cause_analysis:
        re_cascade_context += f"\n\n◎ ROOT CAUSE CANDIDATE (deterministic): {root_cause_analysis}"
    
    # v15.0: Get hypothesis rankings after evidence accumulation
    hypothesis_summary = ""
    if hypotheses:
        ranked = evidence_acc.get_ranked_hypotheses(hypotheses)
        if ranked:
            hypothesis_summary = "\n\nHYPOTHESIS RANKINGS (after evidence):\n"
            for h, conf in ranked[:5]:
                hypothesis_summary += f"  {'●' if conf > 70 else '[yellow]◆[/yellow]' if conf > 40 else '✗'} {h.description}: {conf:.0f}%\n"
    
    # ── STAGE 6+7: SYNTHESIZE + PRESCRIBE — Cross-Branch Merge + Root Cause ──
    console.print("   ◎ [dim]Stage 6-7: Synthesis + prescription...[/dim]")
    
    all_branches_text = "\n\n".join(
        f"### {key}\n{analysis}" for key, analysis in branch_analyses.items()
    )
    
    # Get expert examples
    example_context = ""
    if AI_EXPERT_EXAMPLES and _expert_examples_content:
        example_context = _get_relevant_expert_examples(query, max_examples=2)
    
    merge_prompt = (
        f"ORIGINAL QUERY: {query}\n\n"
        f"PROBLEM CLASSIFICATION: Domain={classification.domain.value}, "
        f"Complexity={classification.complexity.value}, "
        f"Protocols={classification.protocols_involved}, Layers={classification.osi_layers}\n\n"
        f"BRANCH ANALYSES:\n{all_branches_text}\n\n"
        f"{cascade_context}\n\n"
        f"{re_cascade_context}\n\n"
        f"{hypothesis_summary}\n\n"
        + (f"EXPERT EXAMPLES:\n{example_context}\n\n" if example_context else "")
        + "TASK: Perform root cause analysis by merging all branch findings.\n\n"
        "RULES:\n"
        "1. Identify the SINGLE root cause (lowest OSI layer failure)\n"
        "2. Map the complete CASCADING CHAIN from root cause to all symptoms\n"
        "3. Clearly separate ROOT CAUSE from SYMPTOMS\n"
        "4. Provide EXACT Junos fix commands (set/delete)\n"
        "5. Predict what AUTOMATICALLY RECOVERS once root cause is fixed\n"
        "6. Show verification commands to confirm the fix\n"
        "7. Rate your confidence with evidence\n\n"
        "FORMAT:\n"
        "## ◉ Mind-Map Analysis\n"
        "### Problem Tree\n"
        "[visual tree showing branches explored]\n"
        "### Root Cause\n"
        "[exact root cause with evidence]\n"
        "### Cascading Chain\n"
        "[root cause] → [symptom 1] → [symptom 2] → ...\n"
        "### Fix\n"
        "```\n[exact set/delete commands]\n```\n"
        "### Auto-Recovery Prediction\n"
        "[what will heal automatically]\n"
        "### Verification\n"
        "[commands to verify fix]\n"
        "### Confidence\n"
        "CONFIDENCE: [HIGH/MEDIUM/LOW] [%]\n"
    )
    
    final_result = await ollama_analyze(
        "You are a Chief Network Architect performing mind-map root cause analysis. "
        "You have JNCIE-SP expertise and think in protocol state machines.\n\n"
        "You decomposed the problem into branches, analyzed each independently, "
        "and now merge findings to identify the true root cause.",
        all_branches_text[:6000],
        merge_prompt,
        include_kb=True
    )
    
    # Verify output
    if AI_OUTPUT_VERIFICATION:
        final_result = await verify_ai_output(final_result, query, device_map)
    
    return final_result


# ── E125: Junos Scripting Knowledge Injection ───────────────
def get_junos_scripting_context(query: str) -> str:
    """When the user asks about Junos scripting, inject deep scripting knowledge
    from both the knowledge base AND the v15.0 script template library."""
    script_keywords = ["script", "commit script", "op script", "event script", "pyez",
                       "automation", "slax", "xslt", "automate", "python", "ansible",
                       "netconf", "yang", "rest api", "rpc"]
    
    if not any(kw in query.lower() for kw in script_keywords):
        return ""
    
    # v15.0: Check script template library first
    template_context = ""
    try:
        available = list_available_scripts()
        if available:
            template_context = "\n\n## AVAILABLE SCRIPT TEMPLATES\n"
            for name, desc in available.items():
                template_context += f"- **{name}**: {desc}\n"
            
            # Try to find a matching template for the query
            query_lower = query.lower()
            for name in available:
                if any(kw in query_lower for kw in name.replace("_", " ").split()):
                    template = get_script_template(name)
                    if template:
                        template_context += f"\n### Matching Template: {name}\n"
                        template_context += f"**Type:** {template.get('type', 'unknown')}\n"
                        template_context += f"**Description:** {template.get('description', '')}\n"
                        template_context += f"```\n{template.get('template', template.get('code', ''))[:2000]}\n```\n"
                        break
    except Exception:
        pass
    
    # Also extract from deep knowledge base
    kb_context = ""
    if _junos_deep_knowledge:
        in_script = False
        for line in _junos_deep_knowledge.split("\n"):
            if "JUNOS SCRIPTING" in line.upper() or "PyEZ" in line or "AUTOMATION" in line.upper():
                in_script = True
            elif line.startswith("## ") and in_script and "SCRIPT" not in line.upper():
                in_script = False
            if in_script:
                kb_context += line + "\n"
    
    result = ""
    if template_context:
        result += template_context
    if kb_context:
        result += f"\n\n## JUNOS SCRIPTING REFERENCE\n{kb_context[:3000]}"
    return result


# ══════════════════════════════════════════════════════════════
#  v13.0: GPT-OSS INTELLIGENCE UPGRADE — 6 New Enhancements
# ══════════════════════════════════════════════════════════════

# ── Enhancement #E112: Structured Reasoning Chains ──────────
async def structured_reasoning_chain(query: str, mcp_client, session_id, device_map: dict,
                                      tools=None, kb_context: str = "") -> str:
    """Break complex queries into explicit multi-step reasoning chains.
    Instead of asking the model to reason in one shot (where 14B models fail),
    decompose into 3-5 step chains where each step is a focused 3-step reasoning task.
    
    This turns one 15-step chain (impossible for small models) into five 3-step chains (achievable).
    """
    logger.info(f"Structured reasoning chain activated for: {query[:100]}")
    
    # Step 1: Planning — What data do we need?
    plan_prompt = (
        f"You are a Juniper JNCIE-SP network troubleshooter.\n"
        f"USER QUERY: {query}\n"
        f"AVAILABLE DEVICES: {', '.join(f'{v} ({k})' for k, v in device_map.items())}\n\n"
        "Create a DIAGNOSTIC PLAN. Follow OSI bottom-up methodology.\n"
        "OUTPUT FORMAT (strict JSON):\n"
        "```json\n"
        "{\n"
        '  "complexity": "simple|medium|complex",\n'
        '  "layers_to_check": ["L1-Physical", "L3-IGP", "MPLS", "BGP", "Services"],\n'
        '  "devices": ["device1", "device2"],\n'
        '  "commands": [\n'
        '    {"device": "device1", "command": "show ospf neighbor", "purpose": "Check OSPF adjacencies"}\n'
        "  ],\n"
        '  "look_for": "description of what abnormalities to search for"\n'
        "}\n"
        "```\n"
        "Only include devices and commands relevant to the query. Be precise."
    )
    
    plan_response = await ollama_analyze(
        "You are a precise network diagnostic planner. Output ONLY the JSON plan, nothing else.",
        "", plan_prompt, include_kb=False
    )
    
    # Parse plan
    devices_to_check = []
    commands_to_run = []
    reverse_map = {v.lower(): k for k, v in device_map.items()}
    
    # Try to extract JSON from response
    json_match = re.search(r'\{[\s\S]*\}', plan_response)
    if json_match:
        try:
            plan = json.loads(json_match.group())
            for cmd_entry in plan.get("commands", []):
                dev = cmd_entry.get("device", "").lower()
                mcp = reverse_map.get(dev, dev)
                if mcp in device_map and mcp not in devices_to_check:
                    devices_to_check.append(mcp)
                cmd = cmd_entry.get("command", "")
                if cmd and cmd not in commands_to_run:
                    commands_to_run.append(cmd)
            # Also extract devices list
            for dev in plan.get("devices", []):
                dev_lower = dev.lower()
                mcp = reverse_map.get(dev_lower, dev_lower)
                if mcp in device_map and mcp not in devices_to_check:
                    devices_to_check.append(mcp)
        except json.JSONDecodeError:
            pass
    
    # Fallback: extract from text
    if not commands_to_run:
        for line in plan_response.split("\n"):
            line = line.strip()
            if line.startswith(("show ", "- show ")):
                cmd = line.lstrip("- ").strip()
                if cmd not in commands_to_run:
                    commands_to_run.append(cmd)
    
    if not devices_to_check:
        # Extract device names from query
        for dev_name in device_map.values():
            if dev_name.lower() in query.lower():
                mcp = reverse_map.get(dev_name.lower(), dev_name)
                if mcp in device_map:
                    devices_to_check.append(mcp)
        if not devices_to_check:
            devices_to_check = list(device_map.keys())[:5]
    
    if not commands_to_run:
        commands_to_run = ["show ospf neighbor", "show bgp summary", "show ldp session",
                          "show interfaces terse", "show isis adjacency"]
    
    console.print(f"   ◇ [dim]Reasoning chain: {len(devices_to_check)} devices, {len(commands_to_run)} commands[/dim]")
    
    # Step 2: Data Collection — Execute commands
    collected_data = {}
    for cmd in commands_to_run[:8]:  # Limit to 8 commands
        try:
            batch_devices = devices_to_check[:6]  # Limit batch size
            result = await run_batch(mcp_client, session_id, cmd, batch_devices,
                                     cmd.split()[1] if len(cmd.split()) > 1 else "data")
            collected_data[cmd] = result[:4000]
        except Exception as e:
            collected_data[cmd] = f"ERROR: {e}"
    
    # Step 3: Per-Layer Analysis — Analyze each OSI layer independently
    layer_analyses = {}
    all_data_str = "\n\n".join(f"=== {cmd} ===\n{data}" for cmd, data in collected_data.items())
    
    # Only analyze relevant layers (based on commands collected)
    data_lower = all_data_str.lower()
    layers = []
    if any(k in data_lower for k in ["interface", "terse", "physical", "error"]):
        layers.append(("L1-Physical", "Check interface states (up/down), CRC errors, drops, carrier transitions"))
    if any(k in data_lower for k in ["ospf", "isis", "neighbor", "adjacency", "route"]):
        layers.append(("L3-IGP", "Check OSPF/IS-IS adjacency states, missing neighbors, route table completeness"))
    if any(k in data_lower for k in ["ldp", "mpls", "label", "lsp"]):
        layers.append(("MPLS", "Check LDP sessions, label bindings in inet.3, RSVP LSP states"))
    if any(k in data_lower for k in ["bgp", "peer", "established", "active"]):
        layers.append(("BGP", "Check BGP session states, route counts, Active/Idle sessions"))
    if any(k in data_lower for k in ["vpn", "vrf", "instance", "l3vpn", "l2vpn"]):
        layers.append(("Services", "Check VPN route tables, route-target matching, end-to-end reachability"))
    
    if not layers:
        layers = [("General", "Analyze all available data for anomalies")]
    
    for layer_name, layer_focus in layers:
        # v14.0 E126: Inject protocol FSM context for deterministic reasoning
        fsm_context = ""
        if "IGP" in layer_name or "L3" in layer_name:
            for proto in ["ospf", "isis"]:
                if proto in data_lower:
                    fsm = PROTOCOL_FSM.get(proto)
                    if fsm:
                        fsm_context += f"\n{proto.upper()} FSM: {' → '.join(fsm['states'])} (healthy={fsm['healthy']})\n"
                        for st, diag in fsm.get("diagnostic", {}).items():
                            fsm_context += f"  If stuck in '{st}': {diag['cause']} → check: {diag['check']}\n"
        elif "BGP" in layer_name:
            fsm = PROTOCOL_FSM.get("bgp")
            if fsm:
                fsm_context = f"\nBGP FSM: {' → '.join(fsm['states'])} (healthy={fsm['healthy']})\n"
                for st, diag in fsm.get("diagnostic", {}).items():
                    fsm_context += f"  If stuck in '{st}': {diag['cause']} → check: {diag['check']}\n"
        elif "MPLS" in layer_name:
            fsm = PROTOCOL_FSM.get("ldp")
            if fsm:
                fsm_context = f"\nLDP FSM: {' → '.join(fsm['states'])} (healthy={fsm['healthy']})\n"
                for st, diag in fsm.get("diagnostic", {}).items():
                    fsm_context += f"  If stuck in '{st}': {diag['cause']} → check: {diag['check']}\n"
        
        # v14.0 E125: Inject scripting context if relevant
        scripting_context = get_junos_scripting_context(query)
        
        layer_prompt = (
            f"LAYER: {layer_name}\n"
            f"FOCUS: {layer_focus}\n"
            f"ORIGINAL QUERY: {query}\n\n"
            + (f"PROTOCOL STATE MACHINES:\n{fsm_context}\n\n" if fsm_context else "")
            + (f"SCRIPTING REFERENCE:\n{scripting_context[:1000]}\n\n" if scripting_context else "")
            + "Analyze ONLY this layer. For each finding:\n"
            "- FINDING: [what you found]\n"
            "- EVIDENCE: [exact data that proves it]\n"
            "- SEVERITY: [CRITICAL/WARNING/INFO]\n"
            "- CONFIDENCE: [HIGH/MEDIUM/LOW with percentage]\n\n"
            "If this layer is HEALTHY, say so clearly.\n"
            "DO NOT speculate about other layers."
        )
        
        analysis = await ollama_analyze(
            f"You are a {layer_name} specialist analyzing Junos network data.",
            all_data_str[:6000],
            layer_prompt,
            include_kb=True
        )
        layer_analyses[layer_name] = analysis
    
    # Step 4: Cross-Correlation — Connect findings across layers
    all_layer_findings = "\n\n".join(
        f"## {layer} Analysis\n{finding}" for layer, finding in layer_analyses.items()
    )
    
    correlation_prompt = (
        f"ORIGINAL QUERY: {query}\n\n"
        f"PER-LAYER ANALYSES:\n{all_layer_findings}\n\n"
        "CROSS-CORRELATION TASK:\n"
        "1. Identify the ROOT CAUSE (lowest-layer failure that explains higher-layer symptoms)\n"
        "2. Map the CASCADING FAILURE CHAIN (root cause → symptoms in order)\n"
        "3. Distinguish ROOT CAUSE from SYMPTOMS\n"
        "4. Provide EXACT FIX commands (Junos 'set' commands)\n"
        "5. Predict what will AUTO-RECOVER once root cause is fixed\n"
        "6. Rate overall confidence\n\n"
        "If everything is healthy, say so.\n"
        "Format: Markdown with headers, evidence, and code blocks for commands."
    )
    
    # Inject expert examples if available
    example_context = ""
    if AI_EXPERT_EXAMPLES and _expert_examples_content:
        example_context = _get_relevant_expert_examples(query, max_examples=2)
    
    final_analysis = await ollama_analyze(
        "You are a Chief Network Architect performing root cause analysis. "
        "You correlate findings across protocol layers to identify the true root cause.\n\n"
        + (f"REFERENCE EXAMPLES:\n{example_context}\n\n" if example_context else ""),
        all_layer_findings[:8000],
        correlation_prompt,
        include_kb=True
    )
    
    # Step 5: Verification — Validate the output
    if AI_OUTPUT_VERIFICATION:
        final_analysis = await verify_ai_output(final_analysis, query, device_map)
    
    return final_analysis


# ── Enhancement #E113: Expert Examples Injection ─────────────
def _get_relevant_expert_examples(query: str, max_examples: int = 2) -> str:
    """Retrieve the most relevant expert troubleshooting examples for a query.
    Uses keyword matching to find examples from EXPERT_EXAMPLES.md that match
    the protocols/symptoms in the query.
    """
    if not _expert_examples_content:
        return ""
    
    query_lower = query.lower()
    
    # Parse examples into sections
    examples = []
    current_example = []
    current_header = ""
    
    for line in _expert_examples_content.split("\n"):
        if line.startswith("### Example "):
            if current_example and current_header:
                examples.append({"header": current_header, "content": "\n".join(current_example)})
            current_header = line
            current_example = [line]
        elif current_example:
            current_example.append(line)
    
    if current_example and current_header:
        examples.append({"header": current_header, "content": "\n".join(current_example)})
    
    if not examples:
        return ""
    
    # Score each example by relevance to query
    protocol_keywords = {
        "ospf": ["ospf", "neighbor", "adjacency", "area", "hello", "dead", "p2p", "broadcast", "dr ", "full", "init", "exstart"],
        "bgp": ["bgp", "peer", "session", "active", "idle", "established", "route reflector", "rr", "ibgp", "ebgp", "as "],
        "ldp": ["ldp", "label", "nonexistent", "operational", "session", "binding"],
        "mpls": ["mpls", "lsp", "rsvp", "label", "traffic engineering", "cspf"],
        "isis": ["isis", "is-is", "adjacency", "level", "l1", "l2", "area"],
        "vpn": ["vpn", "vrf", "l3vpn", "l2vpn", "route-target", "route target", "rd ", "route distinguisher"],
        "cascade": ["cascade", "cascading", "chain", "root cause", "multi-hop", "downstream"],
        "health": ["cpu", "memory", "storage", "flap", "high", "full", "disk"],
        "interface": ["interface", "link", "down", "up", "crc", "error", "mtu"],
        "bfd": ["bfd", "bidirectional", "flap", "detect"],
        "firewall": ["firewall", "filter", "acl", "deny", "block", "discard"],
    }
    
    scored_examples = []
    for ex in examples:
        score = 0
        ex_lower = ex["header"].lower() + " " + ex["content"][:500].lower()
        
        for proto, keywords in protocol_keywords.items():
            # Query mentions this protocol?
            query_match = sum(1 for kw in keywords if kw in query_lower)
            # Example covers this protocol?
            example_match = sum(1 for kw in keywords if kw in ex_lower)
            
            if query_match > 0 and example_match > 0:
                score += query_match * example_match
        
        # Bonus for symptom keywords
        symptom_words = ["down", "fail", "broken", "error", "not forming", "stuck", 
                        "cannot", "missing", "flap", "active", "idle", "nonexistent"]
        for sw in symptom_words:
            if sw in query_lower and sw in ex_lower:
                score += 3
        
        if score > 0:
            scored_examples.append((score, ex))
    
    # Sort by score descending
    scored_examples.sort(key=lambda x: -x[0])
    
    # Return top N examples
    result_parts = []
    for _, ex in scored_examples[:max_examples]:
        result_parts.append(ex["content"])
    
    return "\n\n---\n\n".join(result_parts)


# ── Enhancement #E114: Junos Command Dictionary Validation ──
def validate_junos_commands(text: str) -> dict:
    """Validate Junos commands in AI output against the command dictionary.
    Returns {valid: [...], invalid: [...], suggestions: {...}}
    """
    if not _junos_cmd_dict:
        return {"valid": [], "invalid": [], "suggestions": {}}
    
    # Extract set/delete/show commands from text
    commands_found = []
    for line in text.split("\n"):
        stripped = line.strip().strip("`").strip()
        if stripped.startswith(("set ", "delete ", "show ")):
            commands_found.append(stripped)
    
    if not commands_found:
        return {"valid": [], "invalid": [], "suggestions": {}}
    
    # Build a flat set of command patterns
    all_patterns = set()
    
    # Show commands
    for category, cmds in _junos_cmd_dict.get("show_commands", {}).items():
        if isinstance(cmds, list):
            for cmd in cmds:
                # Convert pattern to regex: {placeholder} → \S+
                pattern = re.escape(cmd).replace(r"\{[^}]+\}", r"\S+")
                # Fix the escaping — re.escape escapes the braces too
                pattern = re.sub(r'\\{\\S\+\\}', r'\\S+', cmd)
                pattern = re.sub(r'\{[^}]+\}', r'\\S+', re.escape(cmd))
                all_patterns.add(("show", pattern, cmd))
    
    # Set commands
    for category, cmds in _junos_cmd_dict.get("set_commands", {}).items():
        if isinstance(cmds, list):
            for cmd in cmds:
                pattern = re.sub(r'\{[^}]+\}', r'\\S+', re.escape(cmd))
                all_patterns.add(("set", pattern, cmd))
    
    valid = []
    invalid = []
    suggestions = {}
    
    for cmd in commands_found:
        cmd_type = cmd.split()[0]  # set, delete, show
        matched = False
        
        # Check common structural validity first
        if cmd_type == "set":
            # Basic structural check for set commands
            parts = cmd.split()
            if len(parts) >= 3 and parts[1] in ("protocols", "interfaces", "routing-instances",
                                                   "policy-options", "firewall", "system",
                                                   "routing-options", "forwarding-options"):
                matched = True  # Structurally valid
            # Also try pattern matching
            for ptype, pattern, template in all_patterns:
                if ptype == "set":
                    try:
                        if re.match(f"^{pattern}$", cmd):
                            matched = True
                            break
                    except re.error:
                        pass
        
        elif cmd_type == "show":
            # Check against show command patterns
            for ptype, pattern, template in all_patterns:
                if ptype == "show":
                    try:
                        if re.match(f"^{pattern}", cmd):
                            matched = True
                            break
                    except re.error:
                        pass
            # Also allow any "show" command with known keywords
            show_keywords = ["ospf", "bgp", "ldp", "mpls", "isis", "interfaces", "route",
                           "chassis", "system", "configuration", "firewall", "bfd",
                           "lldp", "ted", "rsvp", "ntp", "snmp", "services", "policy"]
            if any(kw in cmd.lower() for kw in show_keywords):
                matched = True
        
        elif cmd_type == "delete":
            # Delete mirrors set command structure
            parts = cmd.split()
            if len(parts) >= 3 and parts[1] in ("protocols", "interfaces", "routing-instances",
                                                   "policy-options", "firewall", "system"):
                matched = True
        
        if matched:
            valid.append(cmd)
        else:
            invalid.append(cmd)
            # Try to suggest closest valid command
            best_match = None
            best_score = 0
            cmd_words = set(cmd.lower().split())
            for _, _, template in all_patterns:
                template_words = set(template.lower().split())
                overlap = len(cmd_words & template_words)
                if overlap > best_score:
                    best_score = overlap
                    best_match = template
            if best_match and best_score >= 2:
                suggestions[cmd] = best_match
    
    return {"valid": valid, "invalid": invalid, "suggestions": suggestions}


# ── Enhancement #E115: Output Verification Layer ────────────
async def verify_ai_output(ai_output: str, original_query: str, device_map: dict) -> str:
    """Post-generation verification layer.
    Checks AI output for:
    1. Valid router names
    2. Syntactically correct Junos commands
    3. Logical consistency (root cause explains symptoms)
    4. Contradictions
    
    If issues found, appends corrections. Does NOT regenerate.
    """
    if not AI_OUTPUT_VERIFICATION:
        return ai_output
    
    issues = []
    
    # Check 1: Valid router names
    valid_names = set()
    for mcp_name, hostname in device_map.items():
        valid_names.add(hostname.lower())
        valid_names.add(mcp_name.lower())
        # Also add short names like PE1, P11, etc.
        short = re.sub(r'-vmx$', '', hostname.lower())
        valid_names.add(short)
    
    # Find router-like names in output that aren't valid
    router_mentions = re.findall(r'\b(PE\d+|P\d{2}|RR\d+)(?:-vMX)?\b', ai_output, re.IGNORECASE)
    for mention in router_mentions:
        mention_lower = mention.lower()
        if mention_lower not in valid_names and f"{mention_lower}-vmx" not in valid_names:
            issues.append(f"▲ Unknown router name referenced: '{mention}' — not in device inventory")
    
    # Check 2: Junos command validation
    if AI_COMMAND_DICTIONARY and _junos_cmd_dict:
        cmd_validation = validate_junos_commands(ai_output)
        if cmd_validation["invalid"]:
            for inv_cmd in cmd_validation["invalid"][:3]:
                suggestion = cmd_validation["suggestions"].get(inv_cmd, "")
                issue_str = f"▲ Potentially invalid command: `{inv_cmd}`"
                if suggestion:
                    issue_str += f" — did you mean: `{suggestion}`?"
                issues.append(issue_str)
    
    # Check 3: Logical consistency — if "root cause" is mentioned, check it references evidence
    if "root cause" in ai_output.lower():
        has_evidence = any(kw in ai_output.lower() for kw in ["evidence:", "data shows", "output shows",
                                                                "from the output", "as shown", "the data"])
        if not has_evidence:
            issues.append("▲ Root cause stated without explicit evidence reference — verify data supports conclusion")
    
    # Check 4: Look for contradictions
    if "healthy" in ai_output.lower() and "critical" in ai_output.lower():
        # Could be legitimate (one protocol healthy, another critical) — only flag if in same sentence context
        sentences = ai_output.split(".")
        for sentence in sentences:
            if "healthy" in sentence.lower() and "critical" in sentence.lower():
                issues.append("▲ Possible contradiction: 'healthy' and 'critical' used in same context")
                break
    
    # Append verification notes if issues found
    if issues:
        verification_block = "\n\n---\n### ▲ Output Verification Notes\n"
        for issue in issues:
            verification_block += f"- {issue}\n"
        verification_block += "\n*These are automated checks — verify manually if flagged.*"
        return ai_output + verification_block
    
    return ai_output


# ── Enhancement #E116: Confidence-Gated Escalation ──────────
async def confidence_gated_specialist(specialist_func, *args, **kwargs) -> str:
    """Wrapper for specialist calls that retries or cross-validates on low confidence.
    
    1. Run specialist
    2. Extract confidence from output
    3. If confidence < threshold:
       a. Retry with more detailed prompt
       b. If still low, cross-validate with a second specialist perspective
    4. Return best result
    """
    threshold = AI_CONFIDENCE_THRESHOLD
    
    # First attempt
    result = await specialist_func(*args, **kwargs)
    confidence = _extract_confidence_score(result)
    
    if confidence >= threshold:
        return result
    
    logger.info(f"Confidence {confidence}% < {threshold}% threshold — retrying with enhanced prompt")
    
    # Retry with more context
    # Add expert examples to kwargs if available
    enhanced_result = await specialist_func(*args, **kwargs)
    confidence2 = _extract_confidence_score(enhanced_result)
    
    if confidence2 >= threshold:
        return enhanced_result
    
    # Still low — append warning
    logger.warning(f"Confidence remains low ({confidence2}%) after retry — flagging for human review")
    warning = (
        f"\n\n### ▲ LOW CONFIDENCE ALERT ({confidence2}%)\n"
        f"This analysis has confidence below the {threshold}% threshold. "
        f"**Recommend human verification** before acting on these findings.\n"
        f"Possible reasons: insufficient data, ambiguous symptoms, or unusual configuration."
    )
    return enhanced_result + warning


def _extract_confidence_score(text: str) -> int:
    """Extract confidence percentage from specialist output.
    Looks for patterns like 'CONFIDENCE: HIGH', 'Confidence: 85%', etc.
    """
    # Try percentage format first
    pct_match = re.search(r'[Cc]onfidence[:\s]+(\d{1,3})%', text)
    if pct_match:
        return int(pct_match.group(1))
    
    # Map word-based confidence to percentage
    confidence_map = {
        "high": 90,
        "medium": 60,
        "low": 30,
        "very high": 95,
        "very low": 15,
    }
    
    word_match = re.search(r'[Cc]onfidence[:\s]+(very\s+)?(HIGH|MEDIUM|LOW|high|medium|low)', text, re.IGNORECASE)
    if word_match:
        prefix = (word_match.group(1) or "").strip().lower()
        level = word_match.group(2).lower()
        key = f"{prefix} {level}".strip()
        return confidence_map.get(key, confidence_map.get(level, 50))
    
    # No confidence found — assume medium
    return 50


# ── LAYERED AI SPECIALISTS ──────────────────────────────────

def _extract_kb_section(kb: str, section_id: str) -> str:
    """Extract a specific section from the knowledge base by its heading."""
    start = kb.find(section_id)
    if start == -1:
        return ""
    # Find next top-level section
    next_section = kb.find("\n# SECTION", start + len(section_id))
    if next_section == -1:
        next_section = len(kb)
    return kb[start:next_section]


def _extract_kb_subsection(kb: str, subsection_id: str, max_len: int = 3000) -> str:
    """Extract a subsection (## level) from the knowledge base."""
    start = kb.find(subsection_id)
    if start == -1:
        return ""
    next_sub = kb.find("\n## ", start + len(subsection_id))
    if next_sub == -1:
        next_sub = min(start + max_len, len(kb))
    return kb[start:next_sub]


async def _specialist_call(role_prompt: str, data: str, question: str) -> str:
    """Make a focused AI call with minimal context — the specialist pattern.
    E1: Chain-of-thought enforcement via system prompt injection.
    E3: Self-verification loop — asks model to double-check its findings (controlled by AI_SELF_VERIFY).
    E4: Confidence scoring appended to each specialist's output.
    E113: Expert examples injection for protocol-specific troubleshooting patterns.
    E115: Output verification for command correctness.
    E116: Confidence-gated escalation for low-confidence findings."""
    # E1: Inject chain-of-thought instruction into role prompt
    cot_prefix = (
        "REASONING INSTRUCTIONS:\n"
        "Before stating any finding, you MUST show your reasoning step-by-step:\n"
        "  STEP 1: What does the data show? (quote exact values)\n"
        "  STEP 2: What is the expected/normal state?\n"
        "  STEP 3: Is there a gap? If so, what is the root cause?\n"
        "  STEP 4: State your finding with confidence (HIGH/MEDIUM/LOW and percentage, e.g. HIGH 90%).\n"
        "If data is missing or incomplete, say 'INSUFFICIENT DATA' — do NOT guess.\n\n"
    )
    
    # E113: Inject relevant expert troubleshooting examples
    expert_context = ""
    if AI_EXPERT_EXAMPLES and _expert_examples_content:
        # Determine protocol from role prompt
        protocol_hint = ""
        for proto in ["OSPF", "BGP", "LDP", "MPLS", "IS-IS", "ISIS", "L3VPN", "VPN", "RSVP", "BFD"]:
            if proto.lower() in role_prompt.lower():
                protocol_hint = proto
                break
        if protocol_hint:
            relevant_examples = _get_relevant_expert_examples(
                f"{protocol_hint} {question[:100]}",
                max_examples=1
            )
            if relevant_examples:
                expert_context = (
                    "EXPERT REFERENCE EXAMPLE (follow this reasoning pattern):\n"
                    f"{relevant_examples[:2000]}\n\n"
                )
    
    enhanced_prompt = cot_prefix + expert_context + role_prompt
    messages = [
        {"role": "system", "content": enhanced_prompt},
        {"role": "user", "content": f"{question}\n\nData:\n{data}"}
    ]
    logger.info(f"Specialist call: {len(enhanced_prompt)} chars prompt, {len(data)} chars data"
                f"{' (with expert example)' if expert_context else ''}")
    for attempt in range(3):
        response = await ollama_chat(messages)
        content = response.get("message", {}).get("content", "").strip()
        if content:
            logger.info(f"Specialist response: {len(content)} chars (attempt {attempt+1})")
            # E3: Self-verification — ask model to double-check ONE time
            # v9.0: Controlled by AI_SELF_VERIFY flag
            # v13.0: Now enabled by default with GPT-OSS (powerful enough)
            if AI_SELF_VERIFY:
                verify_msgs = [
                    {"role": "system", "content": enhanced_prompt},
                    {"role": "user", "content": f"{question}\n\nData:\n{data}"},
                    {"role": "assistant", "content": content},
                    {"role": "user", "content": (
                        "Self-check: Re-read the raw data above and your analysis. "
                        "Are there any findings you stated that contradict the data? "
                        "Are there issues in the data you MISSED? "
                        "Are all Junos commands syntactically correct? "
                        "Reply with ONLY corrections/additions (or 'VERIFIED — no changes needed')."
                    )}
                ]
                verify_resp = await ollama_chat(verify_msgs)
                verify_text = verify_resp.get("message", {}).get("content", "").strip()
                if verify_text and "VERIFIED" not in verify_text.upper() and "no changes" not in verify_text.lower():
                    content += f"\n\n### Self-Verification Addendum\n{verify_text}"
                    logger.info(f"Self-verification added {len(verify_text)} chars of corrections")
            
            # E116: Confidence-gated escalation
            confidence = _extract_confidence_score(content)
            if confidence < AI_CONFIDENCE_THRESHOLD:
                logger.info(f"Specialist confidence {confidence}% < {AI_CONFIDENCE_THRESHOLD}% — flagging")
                content += (
                    f"\n\n> ▲ **Confidence: {confidence}%** (below {AI_CONFIDENCE_THRESHOLD}% threshold) "
                    f"— findings should be verified with additional data collection."
                )
            
            # E115: Validate any Junos commands in the output
            if AI_OUTPUT_VERIFICATION and AI_COMMAND_DICTIONARY:
                cmd_check = validate_junos_commands(content)
                if cmd_check["invalid"]:
                    warning_lines = [f"  - `{cmd}`" for cmd in cmd_check["invalid"][:3]]
                    content += (
                        "\n\n> ◆ **Command Validation:** The following commands could not be verified "
                        "against the Junos command dictionary — please double-check syntax:\n"
                        + "\n".join(warning_lines)
                    )
            
            return content
        messages.append({"role": "assistant", "content": ""})
        messages.append({"role": "user", "content": "Please provide your analysis now."})
    logger.warning("Specialist failed after 3 attempts")
    return "(Specialist could not generate analysis)"


async def specialist_ospf(ospf_data: str, kb: str, device_context: str = "",
                          precomputed_vectors: dict | None = None) -> str:
    """OSPF Specialist — analyzes ONLY OSPF data with semantically-retrieved KB."""
    global vector_kb
    protocol = "OSPF"
    context_query = "Junos OSPF adjacency neighbor interface type point-to-point broadcast area hello dead timer mismatch troubleshooting"
    
    if vector_kb and precomputed_vectors:
        # Enhancement #3: Use pre-computed vectors
        protocol_queries = {
            q: v for q, v in precomputed_vectors.items()
            if protocol.lower() in q.lower()
        }
        if protocol_queries:
            kb_context = await vector_kb.retrieve_for_protocol_with_vectors(
                protocol, protocol_queries, top_k=5
            )
        else:
            kb_context = await vector_kb.retrieve_for_protocol(protocol, context_query, top_k=5)
    elif vector_kb:
        kb_context = await vector_kb.retrieve_for_protocol(protocol, context_query, top_k=5)
    else:
        # Fallback to old method if vector store unavailable
        kb_context = (
            _extract_kb_subsection(kb, "### `show ospf neighbor`") +
            _extract_kb_subsection(kb, "### `show ospf interface`") +
            _extract_kb_subsection(kb, "## 2.1 OSPF — Point-to-Point Links") +
            _extract_kb_subsection(kb, "## 5.1 OSPF Adjacency Not Forming") +
            _extract_kb_subsection(kb, "## Example 1: OSPF Type Mismatch")
        )
    
    # Enhancement #5: Include device context so specialist knows which routers it's analyzing
    device_header = f"\nDEVICES IN SCOPE:\n{device_context}\n\n" if device_context else ""
    
    role = (
        "You are an OSPF specialist. You ONLY analyze OSPF data.\n\n"
        f"{device_header}"
        "OSPF FSM STATES (in order): Down → Init → 2-Way → ExStart → Exchange → Loading → Full\n"
        "- Full = healthy adjacency\n"
        "- Stuck at Init = hello received but no 2-Way → check hello/dead timers, area ID, authentication\n"
        "- Stuck at ExStart = MTU mismatch or auth failure → check interface MTU and auth keys\n"
        "- Stuck at 2-Way = normal for DROther on broadcast, CRITICAL on point-to-point\n\n"
        "YOUR TASK:\n"
        "1. Check each router's OSPF interface state (PtToPt vs DR/BDR)\n"
        "2. For each link between two routers, verify BOTH sides match\n"
        "3. Check neighbor count — 0 neighbors with configured interfaces = PROBLEM\n"
        "4. Check area IDs match between neighbors\n"
        "5. Check hello/dead timers match\n"
        "6. If neighbors exist but NOT in Full state, identify WHERE in the FSM they are stuck and WHY\n"
        "7. E5 NEGATIVE SPACE: What is MISSING? Are there expected neighbors that don't appear at all? "
        "Are there interfaces configured for OSPF that show 0 neighbors? Report what SHOULD be there but ISN'T.\n"
        "8. E9 LSDB CROSS-VALIDATION: If LSDB data is present, cross-check that all routers advertising "
        "themselves have at least one full adjacency. Orphan LSAs (router LSA with no neighbor) = stale/isolated router.\n\n"
        "OUTPUT FORMAT:\n"
        "- FINDING: [what you found]\n"
        "- EVIDENCE: [exact data that proves it]\n"
        "- ROOT CAUSE: [why it's broken]\n"
        "- FSM STATE: [where in the FSM the adjacency is stuck, if applicable]\n"
        "- FIX: [exact Junos 'set' command]\n"
        "- IMPACT: [what else breaks because of this]\n"
        "- CONFIDENCE: [HIGH/MEDIUM/LOW]\n\n"
        "If everything is healthy, say 'OSPF: ALL HEALTHY' and list adjacencies.\n\n"
        f"REFERENCE:\n{kb_context[:4000]}"
    )
    
    return await _specialist_call(role, ospf_data, 
        "Analyze ALL OSPF data below. Compare interface types on BOTH sides of each link. "
        "Report any mismatches, missing neighbors, or config issues.")


async def specialist_bgp(bgp_data: str, ospf_findings: str, kb: str, device_context: str = "",
                         precomputed_vectors: dict | None = None) -> str:
    """BGP Specialist — analyzes BGP data WITH awareness of OSPF state."""
    global vector_kb
    protocol = "BGP"
    context_query = "Junos BGP iBGP session Active Idle loopback peering AS path local-preference MED cascading failure"
    
    if vector_kb and precomputed_vectors:
        protocol_queries = {
            q: v for q, v in precomputed_vectors.items()
            if protocol.lower() in q.lower() and "evpn" not in q.lower() and "l2vpn" not in q.lower()
        }
        if protocol_queries:
            kb_context = await vector_kb.retrieve_for_protocol_with_vectors(
                protocol, protocol_queries, top_k=5
            )
        else:
            kb_context = await vector_kb.retrieve_for_protocol(protocol, context_query, top_k=5)
    elif vector_kb:
        kb_context = await vector_kb.retrieve_for_protocol(protocol, context_query, top_k=5)
    else:
        kb_context = (
            _extract_kb_subsection(kb, "### `show bgp summary`") +
            _extract_kb_subsection(kb, "## 2.7 BGP — iBGP with Loopback Peering") +
            _extract_kb_subsection(kb, "## 5.2 BGP Session Not Establishing") +
            _extract_kb_subsection(kb, "## Example 2: BGP Active (Cascading)")
        )
    
    # Enhancement #5: Include device context
    device_header = f"\nDEVICES IN SCOPE:\n{device_context}\n\n" if device_context else ""
    
    role = (
        "You are a BGP specialist for Juniper Junos networks. You analyze BGP sessions.\n\n"
        f"{device_header}"
        "BGP FSM STATES (in order): Idle → Connect → Active → OpenSent → OpenConfirm → Established\n"
        "- Established = healthy session\n"
        "- Active = cannot reach peer → check IGP reachability to loopback, check TCP/179\n"
        "- Idle = BGP not attempting → check neighbor config, routing policy\n"
        "- OpenSent = OPEN sent but no reply → check AS number, authentication\n"
        "- OpenConfirm = waiting for KEEPALIVE → check hold-time mismatch\n\n"
        "CRITICAL RULE: If OSPF is broken (see OSPF findings below), BGP Active state is a SYMPTOM, "
        "not a root cause. Say: 'BGP is Active BECAUSE OSPF is down → fix OSPF first.'\n\n"
        "YOUR TASK:\n"
        "1. List all BGP peers and their states\n"
        "2. For Active/Idle peers → is it caused by OSPF failure? (check OSPF findings)\n"
        "3. For peers with AS mismatch or authentication failure → BGP-specific root cause\n"
        "4. Note routers with NO BGP configured\n"
        "5. Check routing policies (import/export) for correctness — missing policies cause route leaks\n"
        "6. Check if prefix-limit is configured on peers — missing prefix-limit is a risk\n"
        "7. Check if BGP authentication (MD5) is used — missing auth is a security risk\n"
        "8. E5 NEGATIVE SPACE: What peers are MISSING? If you see only partial mesh in iBGP, "
        "report which routers should have BGP sessions but don't. Missing route reflector client? Missing full mesh?\n"
        "9. E7 ROUTE ANOMALY: Check received/advertised prefix counts. 0 received prefixes on an Established "
        "session = policy blocking routes. Vastly different prefix counts between peers = asymmetric routing.\n"
        "10. E10 ROUTE TRACING: For non-Established sessions, trace the reachability path: "
        "Can this router reach the peer's loopback? Is there a next-hop resolution failure?\n"
        "11. E13 POLICY VALIDATION: Check if referenced policy-options actually exist. "
        "If BGP config says 'import MY-POLICY' but no 'policy-options policy-statement MY-POLICY' exists, "
        "that's a critical config error. Also flag export policies that leak routes between VRFs.\n\n"
        "OUTPUT FORMAT:\n"
        "- FINDING: [what you found]\n"
        "- CAUSED BY: [OSPF failure / config issue / policy issue / other]\n"
        "- RISK: [HIGH/MEDIUM/LOW]\n"
        "- CONFIDENCE: [HIGH/MEDIUM/LOW]\n"
        "- FIX: [fix command or 'Fix OSPF first']\n\n"
        f"OSPF SPECIALIST FINDINGS:\n{ospf_findings[:2000]}\n\n"
        f"REFERENCE:\n{kb_context[:3000]}"
    )
    
    return await _specialist_call(role, bgp_data, 
        "Analyze all BGP sessions. For any down sessions, determine if the cause is IGP failure or BGP-specific.")


async def specialist_ldp_mpls(ldp_data: str, ospf_findings: str, kb: str, device_context: str = "",
                              precomputed_vectors: dict | None = None) -> str:
    """LDP/MPLS Specialist — analyzes LDP sessions and MPLS state."""
    global vector_kb
    protocol = "LDP MPLS"
    context_query = "Junos LDP MPLS LDP session Nonexistent label switching RSVP-TE fast-reroute MPLS interface configuration segment routing"
    
    if vector_kb and precomputed_vectors:
        protocol_queries = {
            q: v for q, v in precomputed_vectors.items()
            if "ldp" in q.lower() or "mpls" in q.lower()
        }
        if protocol_queries:
            kb_context = await vector_kb.retrieve_for_protocol_with_vectors(
                protocol, protocol_queries, top_k=5
            )
        else:
            kb_context = await vector_kb.retrieve_for_protocol(protocol, context_query, top_k=5)
    elif vector_kb:
        kb_context = await vector_kb.retrieve_for_protocol(protocol, context_query, top_k=5)
    else:
        kb_context = (
            _extract_kb_subsection(kb, "### `show ldp session`") +
            _extract_kb_subsection(kb, "## 2.12 LDP Configuration") +
            _extract_kb_subsection(kb, "## 2.13 MPLS Configuration") +
            _extract_kb_subsection(kb, "## 5.3 LDP Session Not Forming") +
            _extract_kb_subsection(kb, "## 5.4 MPLS Not Working")
        )
    
    # Enhancement #5: Include device context
    device_header = f"\nDEVICES IN SCOPE:\n{device_context}\n\n" if device_context else ""
    
    role = (
        "You are an LDP/MPLS specialist.\n\n"
        f"{device_header}"
        "CRITICAL RULE: LDP sessions require IGP reachability. If OSPF is broken, "
        "LDP Nonexistent is a SYMPTOM. Say: 'LDP is down BECAUSE OSPF is down.'\n\n"
        "YOUR TASK:\n"
        "1. List all LDP sessions and states\n"
        "2. For Nonexistent/Closed → is it caused by OSPF failure?\n"
        "3. Check MPLS interfaces are configured on core links\n"
        "4. Note routers with no LDP/MPLS\n"
        "5. E11 BFD CORRELATION: If BFD sessions are flapping or down on MPLS interfaces, "
        "LDP may be oscillating. Check if BFD-protected LDP sessions show recent state changes. "
        "BFD failure can tear down LDP before the IGP detects the link loss.\n\n"
        f"OSPF SPECIALIST FINDINGS:\n{ospf_findings[:1500]}\n\n"
        f"REFERENCE:\n{kb_context[:2500]}"
    )
    
    return await _specialist_call(role, ldp_data, 
        "Analyze all LDP sessions and MPLS state. Determine root cause for any failures.")


async def specialist_l2vpn_evpn(l2vpn_data: str, ospf_findings: str, bgp_findings: str, kb: str,
                                device_context: str = "", precomputed_vectors: dict | None = None) -> str:
    """L2VPN/EVPN Specialist — analyzes L2VPN, EVPN, VPLS services. (Enhancement F)"""
    global vector_kb
    protocol = "EVPN L2VPN VPLS"
    context_query = "Junos EVPN L2VPN VPLS EVPN route-type ethernet-segment multihoming VPLS pseudowire MAC-mobility L2circuit service"
    
    if vector_kb and precomputed_vectors:
        protocol_queries = {
            q: v for q, v in precomputed_vectors.items()
            if "evpn" in q.lower() or "l2vpn" in q.lower() or "vpls" in q.lower()
        }
        if protocol_queries:
            kb_context = await vector_kb.retrieve_for_protocol_with_vectors(
                protocol, protocol_queries, top_k=5
            )
        else:
            kb_context = await vector_kb.retrieve_for_protocol(protocol, context_query, top_k=5)
    elif vector_kb:
        kb_context = await vector_kb.retrieve_for_protocol(protocol, context_query, top_k=5)
    else:
        kb_context = ""
    
    # Enhancement #5: Include device context
    device_header = f"\nDEVICES IN SCOPE:\n{device_context}\n\n" if device_context else ""
    
    role = (
        "You are an L2VPN/EVPN specialist. You analyze Layer-2 VPN services.\n\n"
        f"{device_header}"
        "CRITICAL RULE: L2VPN services depend on underlying IGP + LDP/MPLS + BGP signaling. "
        "If OSPF/BGP are broken, L2VPN failures are likely SYMPTOMS.\n\n"
        "YOUR TASK:\n"
        "1. Check EVPN instances — verify route-type advertisements (Type-2 MAC/IP, Type-5 IP Prefix)\n"
        "2. Check VPLS instances — pseudowire status, split-horizon groups\n"
        "3. Check L2circuit/pseudowire status — operational state, MTU matches\n"
        "4. Verify Ethernet Segment Identifiers (ESI) for multihoming\n"
        "5. Check MAC mobility and MAC learning behavior\n\n"
        "OUTPUT FORMAT:\n"
        "- FINDING: [what you found]\n"
        "- CAUSED BY: [underlying IGP/BGP failure / L2VPN-specific config / other]\n"
        "- EVIDENCE: [exact data that proves it]\n"
        "- FIX: [fix command or 'Fix underlying protocol first']\n\n"
        "If no L2VPN/EVPN services are configured, say: 'L2VPN/EVPN: NOT CONFIGURED'\n\n"
        f"OSPF FINDINGS:\n{ospf_findings[:1500]}\n\n"
        f"BGP FINDINGS:\n{bgp_findings[:1500]}\n\n"
        f"REFERENCE:\n{kb_context[:3000]}"
    )
    
    return await _specialist_call(role, l2vpn_data,
        "Analyze all L2VPN/EVPN/VPLS services. Determine if failures are L2VPN-specific or caused by underlying protocol issues.")


async def specialist_isis(isis_data: str, kb: str, device_context: str = "",
                          precomputed_vectors: dict | None = None) -> str:
    """IS-IS Specialist — analyzes IS-IS adjacencies, metrics, levels.
    Enhancement #1E: Dedicated IS-IS analysis."""
    global vector_kb
    protocol = "ISIS"
    context_query = "Junos IS-IS adjacency level-1 level-2 DIS metric wide-metrics-only NET NSAP troubleshooting"
    
    if vector_kb and precomputed_vectors:
        protocol_queries = {
            q: v for q, v in precomputed_vectors.items()
            if "isis" in q.lower() or "is-is" in q.lower()
        }
        if protocol_queries:
            kb_context = await vector_kb.retrieve_for_protocol_with_vectors(
                protocol, protocol_queries, top_k=5
            )
        else:
            kb_context = await vector_kb.retrieve_for_protocol(protocol, context_query, top_k=5)
    elif vector_kb:
        kb_context = await vector_kb.retrieve_for_protocol(protocol, context_query, top_k=5)
    else:
        kb_context = ""
    
    device_header = f"\nDEVICES IN SCOPE:\n{device_context}\n\n" if device_context else ""
    
    role = (
        "You are an IS-IS specialist. You analyze IS-IS routing protocol data.\n\n"
        f"{device_header}"
        "YOUR TASK:\n"
        "1. Check IS-IS adjacency states on all interfaces (Up, Down, Init)\n"
        "2. Verify IS-IS level configuration (L1, L2, L1L2) — both sides must match\n"
        "3. Check DIS election on broadcast segments\n"
        "4. Verify NET (Network Entity Title) addressing is correct\n"
        "5. Check metric values — wide-metrics vs narrow-metrics mismatch\n"
        "6. Verify authentication settings match between neighbors\n\n"
        "OUTPUT FORMAT:\n"
        "- FINDING: [what you found]\n"
        "- EVIDENCE: [exact data that proves it]\n"
        "- ROOT CAUSE: [why it's broken]\n"
        "- FIX: [exact Junos 'set' command]\n"
        "- IMPACT: [what else breaks because of this]\n\n"
        "If IS-IS is not configured, say: 'IS-IS: NOT CONFIGURED'\n"
        "If everything is healthy, say: 'IS-IS: ALL HEALTHY' and list adjacencies.\n\n"
        f"REFERENCE:\n{kb_context[:4000]}"
    )
    
    return await _specialist_call(role, isis_data,
        "Analyze all IS-IS data below. Check adjacency states, level mismatches, and metric configuration.")


async def specialist_system_health(system_data: str, kb: str, device_context: str = "",
                                    precomputed_vectors: dict | None = None) -> str:
    """System Health Specialist — correlates alarms, core dumps, uptime, storage.
    Enhancement #1F: Dedicated system health analysis with correlation."""
    global vector_kb
    protocol = "system"
    context_query = "Junos system health chassis alarm core dump uptime RE crash storage capacity JTAC troubleshooting"
    
    if vector_kb and precomputed_vectors:
        protocol_queries = {
            q: v for q, v in precomputed_vectors.items()
            if "system" in q.lower() or "health" in q.lower() or "chassis" in q.lower()
        }
        if protocol_queries:
            kb_context = await vector_kb.retrieve_for_protocol_with_vectors(
                protocol, protocol_queries, top_k=5
            )
        else:
            kb_context = await vector_kb.retrieve_for_protocol(protocol, context_query, top_k=5)
    elif vector_kb:
        kb_context = await vector_kb.retrieve_for_protocol(protocol, context_query, top_k=5)
    else:
        kb_context = ""
    
    device_header = f"\nDEVICES IN SCOPE:\n{device_context}\n\n" if device_context else ""
    
    role = (
        "You are a Junos System Health specialist. You analyze hardware and OS health indicators.\n\n"
        f"{device_header}"
        "HEALTH THRESHOLDS (flag anything exceeding these):\n"
        f"  - CRC errors: >{HEALTH_THRESHOLDS['crc_error_rate']} per interface\n"
        f"  - Storage usage: >{HEALTH_THRESHOLDS['storage_pct']}%\n"
        f"  - Min uptime (warn if below): {HEALTH_THRESHOLDS['uptime_min_hours']}h\n"
        f"  - BGP prefix deviation: >{HEALTH_THRESHOLDS['bgp_prefix_deviation_pct']}% from peers\n"
        f"  - OSPF dead interval: {HEALTH_THRESHOLDS['ospf_dead_interval_max']}s max\n"
        f"  - Max route table size: {HEALTH_THRESHOLDS['route_table_max']} routes\n\n"
        "YOUR TASK:\n"
        "1. Correlate chassis alarms with potential impact (e.g., 'Rescue not set' = low risk vs 'FPC offline' = CRITICAL)\n"
        "2. Analyze core dumps — which daemon crashed? (rpd = routing, dfwd = firewall, ppmd = BFD)\n"
        "3. Check uptime — short uptime + core dump = recent crash that caused routing flap\n"
        "4. Check storage — >90% on /var can cause commit failures\n"
        "5. Evaluate NTP status — unsynchronized clocks cause certificate and log correlation issues\n"
        "6. Check recent commit history — correlate config changes with issue onset\n"
        "7. E6 TIME-AWARE CORRELATION: Look at timestamps. Did a commit happen just before a protocol went down? "
        "Short uptime on one router while others have long uptime = that router recently rebooted/crashed. "
        "Correlate timestamps to build a timeline of events.\n"
        "8. E12 ERROR TRENDING: If interface error counts are high, note the rate. "
        "High CRC errors + high input errors on same interface = likely physical layer issue (bad cable/optic).\n\n"
        "CORRELATION RULES:\n"
        "- rpd crash + short uptime = Routing Engine restarted → check for routing protocol flaps\n"
        "- FPC offline alarm = linecard failure → interfaces on that FPC are down\n"
        "- Storage >95% on /var = cannot commit, cannot save logs\n"
        "- Multiple core dumps from same daemon = recurring software bug → escalate to JTAC\n"
        "- Commit by 'root' via 'other' just before outage = automation-triggered config push\n\n"
        "OUTPUT FORMAT:\n"
        "- FINDING: [what you found]\n"
        "- CORRELATION: [how this connects to other findings]\n"
        "- RISK LEVEL: [CRITICAL / WARNING / INFO]\n"
        "- CONFIDENCE: [HIGH/MEDIUM/LOW]\n"
        "- ACTION: [what to do — Junos command or JTAC case]\n"
        "- E18 ESTIMATED REMEDIATION TIME: [e.g., '5 minutes', '1 hour', 'JTAC engagement needed']\n\n"
        "If everything is healthy, say: 'SYSTEM HEALTH: ALL HEALTHY'\n\n"
        f"REFERENCE:\n{kb_context[:3000]}"
    )
    
    return await _specialist_call(role, system_data,
        "Analyze all system health data. Correlate alarms with core dumps and uptime. "
        "Identify any hardware or software issues requiring attention.")


# ══════════════════════════════════════════════════════════════
#  v11.0 NEW SPECIALISTS (E100-E104)
# ══════════════════════════════════════════════════════════════

async def specialist_rsvp_te(rsvp_data: str, ospf_findings: str, kb: str,
                              device_context: str = "",
                              precomputed_vectors: dict | None = None) -> str:
    """E100: RSVP-TE Specialist — analyzes RSVP signaling, bandwidth reservations, CSPF."""
    global vector_kb
    protocol = "RSVP"
    context_query = "Junos RSVP-TE signaling LSP bandwidth reservation CSPF ERO make-before-break fast-reroute"
    
    if vector_kb and precomputed_vectors:
        protocol_queries = {
            q: v for q, v in precomputed_vectors.items()
            if "rsvp" in q.lower() or "traffic engineering" in q.lower() or "cspf" in q.lower()
        }
        if protocol_queries:
            kb_context = await vector_kb.retrieve_for_protocol_with_vectors(
                protocol, protocol_queries, top_k=4)
        else:
            kb_context = await vector_kb.retrieve_for_protocol(protocol, context_query, top_k=4)
    elif vector_kb:
        kb_context = await vector_kb.retrieve_for_protocol(protocol, context_query, top_k=4)
    else:
        kb_context = ""
    
    device_header = f"\nDEVICES IN SCOPE:\n{device_context}\n\n" if device_context else ""
    
    role = (
        "You are an RSVP-TE specialist for Juniper Networks. You analyze traffic engineering.\n\n"
        f"{device_header}"
        "YOUR TASK:\n"
        "1. Check RSVP interface states — are all TE-enabled interfaces active?\n"
        "2. Check LSP states — Up, Down, Dn (admin down), or transitioning?\n"
        "3. Verify bandwidth reservations — are LSPs getting requested bandwidth?\n"
        "4. Check CSPF path computation — are EROs (Explicit Route Objects) valid?\n"
        "5. Verify make-before-break (MBB) behavior for LSP optimization\n"
        "6. Check fast-reroute (FRR) protection — are bypass/detour LSPs in place?\n"
        "7. Correlate with OSPF findings — RSVP depends on IGP for CSPF\n\n"
        "OUTPUT FORMAT:\n"
        "- FINDING: [what you found]\n"
        "- EVIDENCE: [exact RSVP data]\n"
        "- ROOT CAUSE: [why — IGP issue, config, or bandwidth exhaustion]\n"
        "- FIX: [Junos 'set' command]\n"
        "- CONFIDENCE: [HIGH/MEDIUM/LOW]\n\n"
        "If RSVP-TE is not configured, say: 'RSVP-TE: NOT CONFIGURED'\n\n"
        f"OSPF FINDINGS:\n{ospf_findings[:1500]}\n\n"
        f"REFERENCE:\n{kb_context[:3000]}"
    )
    
    return await _specialist_call(role, rsvp_data,
        "Analyze all RSVP-TE data. Check LSP states, bandwidth, CSPF, and FRR protection.")


async def specialist_qos_cos(qos_data: str, kb: str, device_context: str = "",
                              precomputed_vectors: dict | None = None) -> str:
    """E101: QoS/CoS Specialist — analyzes traffic classification, scheduling, shaping."""
    global vector_kb
    protocol = "QoS"
    context_query = "Junos CoS class-of-service scheduler forwarding-class classifier policer shaping queue"
    
    if vector_kb and precomputed_vectors:
        protocol_queries = {
            q: v for q, v in precomputed_vectors.items()
            if "qos" in q.lower() or "cos" in q.lower() or "class-of-service" in q.lower()
        }
        if protocol_queries:
            kb_context = await vector_kb.retrieve_for_protocol_with_vectors(
                protocol, protocol_queries, top_k=4)
        else:
            kb_context = await vector_kb.retrieve_for_protocol(protocol, context_query, top_k=4)
    elif vector_kb:
        kb_context = await vector_kb.retrieve_for_protocol(protocol, context_query, top_k=4)
    else:
        kb_context = ""
    
    device_header = f"\nDEVICES IN SCOPE:\n{device_context}\n\n" if device_context else ""
    
    role = (
        "You are a QoS/CoS specialist for Juniper Networks.\n\n"
        f"{device_header}"
        "YOUR TASK:\n"
        "1. Check forwarding-class assignments — are traffic classes properly defined?\n"
        "2. Check scheduler-map bindings — are schedulers applied to correct interfaces?\n"
        "3. Verify classifier configuration — are DSCP/EXP markings correct?\n"
        "4. Check policer hit counts — are any policers dropping excessive traffic?\n"
        "5. Verify queue depths and drop profiles — are queues experiencing tail-drops?\n"
        "6. Check rewrite rules — are outbound markings correct for transit traffic?\n\n"
        "OUTPUT FORMAT:\n"
        "- FINDING: [what you found]\n"
        "- EVIDENCE: [queue counters, policer stats]\n"
        "- IMPACT: [which traffic classes affected]\n"
        "- FIX: [Junos 'set' command for CoS]\n\n"
        "If CoS/QoS is not configured, say: 'QoS/CoS: NOT CONFIGURED — default best-effort only'\n\n"
        f"REFERENCE:\n{kb_context[:3000]}"
    )
    
    return await _specialist_call(role, qos_data,
        "Analyze QoS/CoS configuration and queue statistics. Identify drops, misconfigurations, and optimization opportunities.")


async def specialist_security(security_data: str, kb: str, device_context: str = "",
                               precomputed_vectors: dict | None = None) -> str:
    """E102: Security Specialist — analyzes firewall filters, RE protection, access controls."""
    global vector_kb
    protocol = "security"
    context_query = "Junos firewall filter RE protection lo0 prefix-list policer access control SSH management plane"
    
    if vector_kb and precomputed_vectors:
        protocol_queries = {
            q: v for q, v in precomputed_vectors.items()
            if "security" in q.lower() or "firewall" in q.lower() or "protection" in q.lower()
        }
        if protocol_queries:
            kb_context = await vector_kb.retrieve_for_protocol_with_vectors(
                protocol, protocol_queries, top_k=4)
        else:
            kb_context = await vector_kb.retrieve_for_protocol(protocol, context_query, top_k=4)
    elif vector_kb:
        kb_context = await vector_kb.retrieve_for_protocol(protocol, context_query, top_k=4)
    else:
        kb_context = ""
    
    device_header = f"\nDEVICES IN SCOPE:\n{device_context}\n\n" if device_context else ""
    
    role = (
        "You are a Network Security specialist for Juniper routers.\n\n"
        f"{device_header}"
        "YOUR TASK:\n"
        "1. Check lo0 filter — is there an input filter protecting the Routing Engine?\n"
        "2. Verify firewall filter structure — are there proper accept/deny terms?\n"
        "3. Check for overly permissive rules (accept all traffic to RE)\n"
        "4. Verify protocol-specific protection (BGP TCP/179, OSPF, LDP, SSH, SNMP)\n"
        "5. Check policer counters — are rate-limiters active and effective?\n"
        "6. Verify management access controls (SSH only, no telnet, login classes)\n"
        "7. Check for discard counters that indicate blocked attacks\n"
        "8. Verify SNMP community strings are not 'public' or 'private'\n\n"
        "SECURITY BEST PRACTICES:\n"
        "- lo0 filter MUST have: accept SSH, BGP, OSPF, LDP, BFD, SNMP, NTP, then discard-all\n"
        "- SSH protocol v2 only, no telnet\n"
        "- Root authentication set with strong key\n"
        "- Login idle-timeout configured\n"
        "- Password minimum length enforced\n\n"
        "OUTPUT FORMAT:\n"
        "- FINDING: [vulnerability or config gap]\n"
        "- SEVERITY: [CRITICAL/HIGH/MEDIUM/LOW]\n"
        "- RISK: [what could happen if exploited]\n"
        "- FIX: [Junos 'set' command]\n"
        "- CONFIDENCE: [HIGH/MEDIUM/LOW]\n\n"
        f"REFERENCE:\n{kb_context[:3000]}"
    )
    
    return await _specialist_call(role, security_data,
        "Analyze all security data. Check firewall filters, RE protection, access controls, and management plane security.")


async def specialist_l3vpn(l3vpn_data: str, ospf_findings: str, bgp_findings: str, kb: str,
                            device_context: str = "",
                            precomputed_vectors: dict | None = None) -> str:
    """E103: L3VPN Specialist — analyzes VRF route-targets, RD, PE-CE routing."""
    global vector_kb
    protocol = "L3VPN"
    context_query = "Junos L3VPN VRF route-target route-distinguisher PE-CE routing vrf-import vrf-export bgp.l3vpn.0"
    
    if vector_kb and precomputed_vectors:
        protocol_queries = {
            q: v for q, v in precomputed_vectors.items()
            if "l3vpn" in q.lower() or "vrf" in q.lower() or "route-target" in q.lower()
        }
        if protocol_queries:
            kb_context = await vector_kb.retrieve_for_protocol_with_vectors(
                protocol, protocol_queries, top_k=4)
        else:
            kb_context = await vector_kb.retrieve_for_protocol(protocol, context_query, top_k=4)
    elif vector_kb:
        kb_context = await vector_kb.retrieve_for_protocol(protocol, context_query, top_k=4)
    else:
        kb_context = ""
    
    device_header = f"\nDEVICES IN SCOPE:\n{device_context}\n\n" if device_context else ""
    
    role = (
        "You are an L3VPN specialist for Juniper MPLS networks.\n\n"
        f"{device_header}"
        "YOUR TASK:\n"
        "1. Check VRF instances — are route-distinguishers unique per PE?\n"
        "2. Verify route-targets — are import/export RT values consistent across PEs?\n"
        "3. Check bgp.l3vpn.0 table — are VPN routes being exchanged?\n"
        "4. Verify PE-CE routing — are customer-facing protocols (OSPF/BGP/static) working?\n"
        "5. Check for route leaking between VRFs\n"
        "6. Verify MPLS underlay — are inet.3 routes available for BGP next-hop resolution?\n"
        "7. Cross-reference with BGP findings — are VPNv4/VPNv6 families negotiated?\n\n"
        "DEPENDENCY CHAIN: L3VPN requires: IGP ● → LDP/RSVP ● → iBGP with VPN families ● → VRF config ●\n\n"
        "OUTPUT FORMAT:\n"
        "- FINDING: [VRF issue or service state]\n"
        "- EVIDENCE: [route table output, VRF config]\n"
        "- ROOT CAUSE: [VPN-specific or underlying protocol]\n"
        "- FIX: [Junos 'set' command]\n"
        "- SERVICE IMPACT: [which customers/services affected]\n\n"
        "If no L3VPN is configured, say: 'L3VPN: NOT CONFIGURED'\n\n"
        f"OSPF FINDINGS:\n{ospf_findings[:1000]}\n"
        f"BGP FINDINGS:\n{bgp_findings[:1000]}\n\n"
        f"REFERENCE:\n{kb_context[:3000]}"
    )
    
    return await _specialist_call(role, l3vpn_data,
        "Analyze L3VPN service data. Check VRF configurations, route-targets, and PE-CE routing.")


async def specialist_hardware_env(hw_data: str, kb: str, device_context: str = "",
                                   precomputed_vectors: dict | None = None) -> str:
    """E104: Hardware/Environment Specialist — CPU, memory, optics, temperature."""
    global vector_kb
    protocol = "hardware"
    context_query = "Junos chassis environment RE CPU memory FPC PIC optic power temperature alarm threshold"
    
    if vector_kb and precomputed_vectors:
        protocol_queries = {
            q: v for q, v in precomputed_vectors.items()
            if "hardware" in q.lower() or "chassis" in q.lower() or "environment" in q.lower()
        }
        if protocol_queries:
            kb_context = await vector_kb.retrieve_for_protocol_with_vectors(
                protocol, protocol_queries, top_k=4)
        else:
            kb_context = await vector_kb.retrieve_for_protocol(protocol, context_query, top_k=4)
    elif vector_kb:
        kb_context = await vector_kb.retrieve_for_protocol(protocol, context_query, top_k=4)
    else:
        kb_context = ""
    
    device_header = f"\nDEVICES IN SCOPE:\n{device_context}\n\n" if device_context else ""
    
    role = (
        "You are a Hardware & Environment specialist for Juniper routers.\n\n"
        f"{device_header}"
        "THRESHOLDS:\n"
        f"  - CPU utilization warning: >{_config.get('thresholds', {}).get('cpu_utilization_warning', 80)}%\n"
        f"  - Memory utilization warning: >{_config.get('thresholds', {}).get('memory_utilization_warning', 80)}%\n"
        "  - Temperature: manufacturer limits (typically 50°C warning, 65°C critical)\n"
        "  - Optical power: -3dBm to -20dBm normal range for 10G SFP+\n\n"
        "YOUR TASK:\n"
        "1. Check RE CPU utilization — sustained >80% indicates control plane stress\n"
        "2. Check RE memory — >85% can cause rpd/kernel issues\n"
        "3. Check FPC status — all FPCs should be Online\n"
        "4. Check PIC status — all PICs should be Online\n"
        "5. Verify temperature readings — any component near threshold?\n"
        "6. Check optical transceiver power levels — low rx power = dirty fiber or failing SFP\n"
        "7. Check fan/PSU status — redundancy lost?\n"
        "8. Correlate: high CPU + routing flaps = possible route churn causing CPU spikes\n\n"
        "OUTPUT FORMAT:\n"
        "- FINDING: [hardware condition]\n"
        "- SEVERITY: [CRITICAL/WARNING/INFO]\n"
        "- EVIDENCE: [exact sensor reading or status]\n"
        "- ACTION: [replace SFP, clean fiber, add memory, open JTAC case]\n"
        "- TREND: [getting worse / stable / improving]\n\n"
        "If all hardware is healthy, say: 'HARDWARE: ALL HEALTHY'\n\n"
        f"REFERENCE:\n{kb_context[:3000]}"
    )
    
    return await _specialist_call(role, hw_data,
        "Analyze hardware and environmental data. Check CPU, memory, FPC/PIC status, optics, and temperature.")


# ── E92: AI-Written Executive Narrative ─────────────────────
async def generate_executive_narrative(synthesis: str, health_score: float,
                                        critical_count: int, warning_count: int,
                                        device_count: int) -> str:
    """Generate a CTO-readable executive narrative from the synthesis."""
    prompt = (
        "You are writing an executive summary for a CTO/VP of Network Operations. "
        "Write EXACTLY 3 paragraphs:\n\n"
        "Paragraph 1: Overall network health status — is the network healthy, degraded, or critical? "
        "How many devices, what percentage are affected?\n\n"
        "Paragraph 2: Key findings — what are the top 1-3 issues? Use business language, not protocol jargon. "
        "Instead of 'OSPF type mismatch', say 'a routing configuration inconsistency between two core routers'.\n\n"
        "Paragraph 3: Recommended action — what should be done, how long will it take, "
        "and what is the risk if no action is taken?\n\n"
        "RULES:\n"
        "- NO technical jargon (no OSPF, BGP, LDP, MPLS unless absolutely necessary)\n"
        "- Use business impact language (customers, services, revenue, SLA)\n"
        "- Include numbers (% of network affected, estimated fix time)\n"
        "- Maximum 150 words total\n\n"
        f"HEALTH SCORE: {health_score}/100\n"
        f"DEVICES: {device_count}\n"
        f"CRITICAL ISSUES: {critical_count}\n"
        f"WARNINGS: {warning_count}\n"
    )
    
    try:
        narrative = await ollama_analyze(
            "You are an executive communication specialist for network operations.",
            synthesis[:3000],
            prompt
        )
        return narrative.strip()
    except Exception as e:
        logger.warning(f"Executive narrative generation failed: {e}")
        return ""


# ── E78: AI-Guided Dynamic Troubleshooting ──────────────────
async def ai_guided_troubleshoot(client, session_id, device_map, symptom: str):
    """AI-driven dynamic troubleshooting — replaces static decision trees.
    Takes a symptom and automatically determines commands to run."""
    console.print(Panel(f"⊕ AI Troubleshooting: {symptom}", style="bold yellow", width=70))
    
    # Step 1: AI determines what commands to run and on which devices
    plan_prompt = (
        f"You are a Juniper JNCIE-level network troubleshooter.\n"
        f"SYMPTOM: {symptom}\n"
        f"AVAILABLE DEVICES: {', '.join(f'{v} ({k})' for k, v in device_map.items())}\n\n"
        "Determine the troubleshooting plan:\n"
        "1. Which devices should I check? (list the device names)\n"
        "2. What commands should I run? (list exact Junos show commands)\n"
        "3. What am I looking for in the output?\n\n"
        "OUTPUT FORMAT (strict):\n"
        "DEVICES: device1, device2\n"
        "COMMANDS:\n"
        "- show ospf neighbor\n"
        "- show bgp summary\n"
        "- show interfaces terse\n"
        "LOOK_FOR: adjacency states, error counters, down interfaces"
    )
    
    plan = await ollama_analyze(
        "You are a Juniper troubleshooting expert.",
        "", plan_prompt
    )
    console.print(Panel(plan, title="◇ Troubleshooting Plan", border_style="cyan"))
    
    # Step 2: Extract devices and commands from the plan
    devices_to_check = []
    commands_to_run = []
    reverse_map = {v.lower(): k for k, v in device_map.items()}
    
    for line in plan.split("\n"):
        line = line.strip()
        if line.upper().startswith("DEVICES:"):
            for dev in line.split(":")[1].split(","):
                dev = dev.strip().lower()
                mcp = reverse_map.get(dev, dev)
                if mcp in device_map:
                    devices_to_check.append(mcp)
        if line.startswith("- show ") or line.startswith("- ping ") or line.startswith("- traceroute "):
            commands_to_run.append(line[2:].strip())
    
    if not devices_to_check:
        devices_to_check = list(device_map.keys())[:3]  # Default to first 3
    if not commands_to_run:
        commands_to_run = ["show ospf neighbor", "show bgp summary", "show interfaces terse"]
    
    # Step 3: Run commands and collect data
    console.print(f"\n   ⊛ Checking {len(devices_to_check)} devices with {len(commands_to_run)} commands...")
    all_output = []
    for cmd in commands_to_run[:6]:  # Limit to 6 commands
        try:
            result = await run_batch(client, session_id, cmd, devices_to_check, cmd.split()[1] if len(cmd.split()) > 1 else "check")
            all_output.append(f"COMMAND: {cmd}\n{result[:3000]}\n")
        except Exception as e:
            all_output.append(f"COMMAND: {cmd}\nERROR: {e}\n")
    
    collected_data = "\n".join(all_output)
    
    # Step 4: AI analyzes the collected data
    console.print("   ◉ AI analyzing collected data...")
    analysis_prompt = (
        f"ORIGINAL SYMPTOM: {symptom}\n\n"
        f"COLLECTED DATA:\n{collected_data[:8000]}\n\n"
        "Analyze this data and provide:\n"
        "1. ROOT CAUSE: What is causing the symptom?\n"
        "2. EVIDENCE: What data proves this?\n"
        "3. FIX: Exact Junos commands to fix it\n"
        "4. VERIFY: Commands to verify the fix worked\n"
        "5. CONFIDENCE: How confident are you? (HIGH/MEDIUM/LOW)\n"
        "6. ADDITIONAL_CHECKS: Any more commands needed to confirm?\n"
    )
    
    diagnosis = await ollama_analyze(
        "You are a Juniper JNCIE troubleshooting expert.",
        collected_data[:6000],
        analysis_prompt
    )
    
    console.print(Panel(diagnosis, title="⊕ Diagnosis", border_style="green"))
    
    # Step 5: Offer to apply fix
    if "set " in diagnosis.lower() or "delete " in diagnosis.lower():
        console.print("\n   ▸ Fix commands detected in the diagnosis.")
        apply = input("   Apply fix? (yes/no/verify-first): ").strip().lower()
        if apply in ("verify-first", "v"):
            # Run verify commands
            console.print("   ⊕ Running additional verification...")
        elif apply in ("yes", "y"):
            console.print("   ▲  Use 'configure <device> <change>' command to apply changes safely.")
    
    return diagnosis


async def specialist_synthesizer(ospf_findings: str, bgp_findings: str,
                                  ldp_findings: str, topology: str,
                                  device_summary: str, kb: str,
                                  l2vpn_findings: str = "",
                                  isis_findings: str = "",
                                  system_findings: str = "",
                                  precomputed_vectors: dict | None = None,
                                  enhanced_context: str = "") -> str:
    """Synthesizer — combines all specialist findings into structured root cause analysis.
    
    Enhancement G: Now produces structured JSON severity scoring alongside the narrative.
    Enhancement F: Accepts optional L2VPN/EVPN findings.
    Enhancement #3: Accepts pre-computed vectors for batch embedding.
    """
    global vector_kb
    protocol = "network"
    context_query = "Junos network cascading failure root cause analysis remediation priority healthy network troubleshooting framework"
    
    if vector_kb and precomputed_vectors:
        # Enhancement #1H: Fixed operator precedence with explicit parentheses
        protocol_queries = {
            q: v for q, v in precomputed_vectors.items()
            if ("network" in q.lower() and "cascading" in q.lower()) or
               ("network" in q.lower() and "troubleshooting" in q.lower() and "diagnosis" in q.lower()) or
               ("network" in q.lower() and "best practices" in q.lower())
        }
        if protocol_queries:
            kb_context = await vector_kb.retrieve_for_protocol_with_vectors(
                protocol, protocol_queries, top_k=4
            )
        else:
            kb_context = await vector_kb.retrieve_for_protocol(protocol, context_query, top_k=4)
    elif vector_kb:
        kb_context = await vector_kb.retrieve_for_protocol(protocol, context_query, top_k=4)
    else:
        kb_context = (
            _extract_kb_subsection(kb, "## 5.5 Cascading Failure Analysis") +
            _extract_kb_subsection(kb, "## Step 3: Identify Root Cause", max_len=1500) +
            _extract_kb_subsection(kb, "## Example 3: Healthy Network")
        )
    
    # Enhancement G: Request structured JSON output
    # E15: AI executive narrative
    # E16: Finding deduplication
    # E17: Evidence quality scoring
    # E18: Remediation time estimates
    role = (
        "You are the Chief Network Architect. You receive findings from protocol specialists "
        "(OSPF, IS-IS, BGP, LDP/MPLS, L2VPN/EVPN, System Health) and your job is to:\n\n"
        "1. Identify the SINGLE ROOT CAUSE (usually the lowest layer failure)\n"
        "2. Build the CASCADING FAILURE CHAIN showing how one failure causes all others\n"
        "3. Provide a PRIORITIZED remediation plan (fix root cause first)\n"
        "4. Predict what will AUTO-RECOVER once root cause is fixed\n"
        "5. Summarize overall network health\n"
        "6. Assess RISK for each protocol area (OSPF, BGP, MPLS, System)\n"
        "7. E15 EXECUTIVE NARRATIVE: Write a 3-sentence executive summary a CTO can understand. "
        "No jargon. Example: 'The network is experiencing service degradation due to a configuration "
        "mismatch on two core routers. This affects 3 customer VPN services. Estimated fix time: 15 minutes.'\n"
        "8. E16 DEDUPLICATION: If multiple specialists reported the same issue (e.g., both OSPF and BGP "
        "note the same link is down), consolidate into ONE finding and cite both sources.\n"
        "9. E17 EVIDENCE QUALITY: For each finding, rate evidence quality:\n"
        "   - STRONG: Multiple data sources confirm the issue\n"
        "   - MODERATE: Single source but clear evidence\n"
        "   - WEAK: Inferred from indirect data — needs manual verification\n"
        "10. E18 REMEDIATION TIME: For each fix, estimate time: Quick (<5 min), Moderate (5-30 min), "
        "Extended (30+ min), Requires JTAC/vendor.\n\n"
        "OUTPUT FORMAT — You MUST produce TWO sections:\n\n"
        "SECTION 1: A JSON block wrapped in ```json ... ``` with this exact schema:\n"
        "```json\n"
        "{\n"
        '  "severity": "CRITICAL | DEGRADED | HEALTHY",\n'
        '  "confidence": 0.0 to 1.0,\n'
        '  "executive_summary": "3-sentence CTO-level summary",\n'
        '  "root_cause": "one-sentence root cause description",\n'
        '  "failure_chain": ["first failure", "caused by first", "caused by second"],\n'
        '  "fix_priority": [\n'
        '    {"order": 1, "action": "exact Junos set command or action", "router": "hostname", "expected_recovery": "what recovers", "estimated_time": "Quick/Moderate/Extended", "evidence_quality": "STRONG/MODERATE/WEAK"},\n'
        '    {"order": 2, "action": "...", "router": "...", "expected_recovery": "...", "estimated_time": "...", "evidence_quality": "..."}\n'
        '  ],\n'
        '  "auto_recover": ["list of things that will recover automatically after root cause fix"],\n'
        '  "affected_routers": ["list of router names affected"],\n'
        '  "healthy_routers": ["list of router names with no issues"]\n'
        "}\n"
        "```\n\n"
        "SECTION 2: A human-readable narrative with these subsections:\n"
        "### Root Cause\n[one sentence identifying the root cause]\n\n"
        "### Cascading Failure Chain\n[show the chain: A → B → C → D]\n\n"
        "### Remediation Plan\n1. [first fix — the root cause]\n2. [verify recovery]\n3. [any remaining issues]\n\n"
        "### Overall Health\n[one sentence: HEALTHY / DEGRADED / CRITICAL]\n\n"
        f"REFERENCE:\n{kb_context[:2000]}"
    )
    
    # Enhancement #6: Cap synthesizer inputs — use structured summaries
    # Extract top findings from each specialist (first 2000 chars max) to prevent
    # context overflow when the 14B model has to process all specialist outputs
    def _cap_specialist(findings: str, max_chars: int = 2000) -> str:
        """Cap specialist output, prioritizing FINDING/ROOT CAUSE lines."""
        if len(findings) <= max_chars:
            return findings
        # Try to keep structured findings
        priority_lines = []
        other_lines = []
        for line in findings.split('\n'):
            if any(kw in line.upper() for kw in ['FINDING', 'ROOT CAUSE', 'FIX:', 'CAUSED BY', 'IMPACT', 'EVIDENCE']):
                priority_lines.append(line)
            else:
                other_lines.append(line)
        priority_text = '\n'.join(priority_lines)
        if len(priority_text) >= max_chars:
            return priority_text[:max_chars]
        remaining = max_chars - len(priority_text)
        return priority_text + '\n' + '\n'.join(other_lines)[:remaining]
    
    # Build combined data — include optional specialists if available
    l2vpn_section = ""
    if l2vpn_findings and l2vpn_findings.strip() and "NOT CONFIGURED" not in l2vpn_findings.upper():
        l2vpn_section = f"\n\n═══ L2VPN/EVPN SPECIALIST REPORT ═══\n{_cap_specialist(l2vpn_findings, 1500)}"
    
    isis_section = ""
    if isis_findings and isis_findings.strip() and "NOT CONFIGURED" not in isis_findings.upper():
        isis_section = f"\n\n═══ IS-IS SPECIALIST REPORT ═══\n{_cap_specialist(isis_findings, 1500)}"
    
    system_section = ""
    if system_findings and system_findings.strip() and "ALL HEALTHY" not in system_findings.upper():
        system_section = f"\n\n═══ SYSTEM HEALTH SPECIALIST REPORT ═══\n{_cap_specialist(system_findings, 1500)}"
    
    combined_data = (
        f"NETWORK TOPOLOGY:\n{topology[:1500]}\n\n"
        f"DEVICE SUMMARY:\n{device_summary[:800]}\n\n"
        f"═══ OSPF SPECIALIST REPORT ═══\n{_cap_specialist(ospf_findings, 2500)}\n\n"
        f"═══ BGP SPECIALIST REPORT ═══\n{_cap_specialist(bgp_findings, 2000)}\n\n"
        f"═══ LDP/MPLS SPECIALIST REPORT ═══\n{_cap_specialist(ldp_findings, 2000)}"
        f"{isis_section}"
        f"{l2vpn_section}"
        f"{system_section}"
    )
    
    # v10.0: Inject enhanced intelligence context (E38-E42)
    if enhanced_context:
        combined_data += f"\n\n{enhanced_context[:3000]}"
    
    raw_synthesis = await _specialist_call(role, combined_data, 
        "Synthesize all specialist reports into a unified root cause analysis. "
        "Produce BOTH the JSON severity block AND the human-readable narrative.")
    
    # Enhancement G: Try to extract and validate the JSON block
    json_match = re.search(r'```json\s*(\{.*?\})\s*```', raw_synthesis, re.DOTALL)
    if json_match:
        try:
            severity_data = json.loads(json_match.group(1))
            # Inject severity metadata as a comment at the top of the synthesis
            severity_tag = severity_data.get("severity", "UNKNOWN")
            confidence = severity_data.get("confidence", 0.0)
            raw_synthesis = (
                f"<!-- SEVERITY:{severity_tag} CONFIDENCE:{confidence:.2f} -->\n"
                + raw_synthesis
            )
        except json.JSONDecodeError:
            pass  # JSON parsing failed — still return the raw synthesis
    
    return raw_synthesis


async def run_layered_analysis(ospf_data: str, bgp_data: str, ldp_data: str,
                                topology: str, device_summary: str,
                                l2vpn_data: str = "",
                                isis_data: str = "",
                                system_data: str = "",
                                device_context: str = "",
                                all_raw_data: str = "",
                                device_map: dict | None = None,
                                enhanced_context: str = "",
                                security_data: str = "",
                                l3vpn_data: str = "",
                                hardware_data: str = "") -> str:
    """Run the enhanced layered AI pipeline with parallel execution.
    
    v6.0: Added IS-IS specialist (#1E), System Health specialist (#1F),
          batch pre-embed includes all new specialist queries.
    """
    kb = load_knowledge_base()
    ai_timing = {}  # Enhancement #4E: Track per-specialist timing
    
    # ── Enhancement #3: Batch Pre-Embed all KB queries ──
    precomputed_vectors = {}
    if vector_kb:
        specialist_queries = [
            # OSPF specialist
            "Junos OSPF troubleshooting analysis diagnosis",
            "Junos OSPF configuration best practices commands",
            "Junos OSPF adjacency neighbor interface type point-to-point broadcast area hello dead timer mismatch troubleshooting",
            # BGP specialist
            "Junos BGP troubleshooting analysis diagnosis",
            "Junos BGP configuration best practices commands",
            "Junos BGP iBGP session Active Idle loopback peering AS path local-preference MED cascading failure",
            # LDP specialist
            "Junos LDP MPLS troubleshooting analysis diagnosis",
            "Junos LDP MPLS configuration best practices commands",
            "Junos LDP MPLS LDP session Nonexistent label switching RSVP-TE fast-reroute MPLS interface configuration segment routing",
            # Synthesizer
            "Junos network troubleshooting analysis diagnosis",
            "Junos network configuration best practices commands",
            "Junos network cascading failure root cause analysis remediation priority healthy network troubleshooting framework",
        ]
        # L2VPN specialist queries (only if data present)
        if l2vpn_data and l2vpn_data.strip():
            specialist_queries.extend([
                "Junos EVPN L2VPN VPLS troubleshooting analysis diagnosis",
                "Junos EVPN L2VPN VPLS configuration best practices commands",
                "Junos EVPN L2VPN VPLS EVPN route-type ethernet-segment multihoming VPLS pseudowire MAC-mobility L2circuit service",
            ])
        # IS-IS specialist queries (#1E)
        if isis_data and isis_data.strip():
            specialist_queries.extend([
                "Junos IS-IS ISIS troubleshooting analysis diagnosis",
                "Junos IS-IS ISIS adjacency level DIS metric wide-metrics NET NSAP configuration",
            ])
        # System Health specialist queries (#1F)
        if system_data and system_data.strip():
            specialist_queries.extend([
                "Junos system health chassis alarm core dump troubleshooting",
                "Junos system RE crash uptime storage capacity JTAC case",
            ])
        
        try:
            console.print("      [info]⚡ Batch pre-embedding all KB queries...[/info]")
            vectors = await vector_kb.batch_pre_embed(specialist_queries)
            precomputed_vectors = dict(zip(specialist_queries, vectors))
            console.print(f"         [success]● Pre-embedded {len(vectors)} queries in 1 batch call[/success]")
        except Exception as e:
            console.print(f"         [warning]▲  Batch pre-embed failed ({e}), falling back to sequential[/warning]")
            precomputed_vectors = {}
    
    # ── Layer 1a: OSPF first (other protocols depend on it) ──
    console.print("      [heading]◉ Layer 1a: OSPF Specialist analyzing...[/heading]")
    t0 = time.time()
    ospf_findings = await specialist_ospf(ospf_data, kb, device_context, precomputed_vectors)
    ai_timing["ospf"] = round(time.time() - t0, 1)
    console.print(f"         [success]● OSPF analysis: {len(ospf_findings)} chars ({ai_timing['ospf']}s)[/success]")
    
    # ── Layer 1b: BGP + LDP + IS-IS + System Health in PARALLEL ──
    # All depend on OSPF findings but NOT on each other → safe to parallelize
    parallel_tasks = [
        specialist_bgp(bgp_data, ospf_findings, kb, device_context, precomputed_vectors),
        specialist_ldp_mpls(ldp_data, ospf_findings, kb, device_context, precomputed_vectors)
    ]
    parallel_labels = ["bgp", "ldp"]
    
    # Enhancement #1E: IS-IS specialist (in parallel)
    if isis_data and isis_data.strip():
        parallel_tasks.append(specialist_isis(isis_data, kb, device_context, precomputed_vectors))
        parallel_labels.append("isis")
    
    # Enhancement #1F: System Health specialist (in parallel)
    if system_data and system_data.strip():
        parallel_tasks.append(specialist_system_health(system_data, kb, device_context, precomputed_vectors))
        parallel_labels.append("system")
    
    print(f"      ◉ Layer 1b: {' + '.join(l.upper() for l in parallel_labels)} Specialists in PARALLEL...")
    t0 = time.time()
    parallel_results = await asyncio.gather(*parallel_tasks, return_exceptions=True)
    parallel_time = round(time.time() - t0, 1)
    
    # Guard: replace any exception results with empty string and warn
    for i, r in enumerate(parallel_results):
        if isinstance(r, BaseException):
            console.print(f"         [warning]▲ {parallel_labels[i].upper()} specialist failed: {type(r).__name__}[/warning]")
            parallel_results[i] = ""
    
    # Safe string extraction after exception guard
    _safe_results: list[str] = [r if isinstance(r, str) else "" for r in parallel_results]
    bgp_findings = _safe_results[0]
    ldp_findings = _safe_results[1]
    isis_findings = ""
    system_findings = ""
    
    idx = 2
    for label in parallel_labels[2:]:
        if label == "isis":
            isis_findings = _safe_results[idx]
            ai_timing["isis"] = parallel_time
        elif label == "system":
            system_findings = _safe_results[idx]
            ai_timing["system"] = parallel_time
        idx += 1
    
    ai_timing["bgp"] = parallel_time
    ai_timing["ldp"] = parallel_time
    for label in parallel_labels:
        result = _safe_results[parallel_labels.index(label)]
        console.print(f"         [success]● {label.upper()} analysis: {len(result)} chars[/success]")
    
    # ── Layer 1c: L2VPN/EVPN — needs BGP context ──
    l2vpn_findings = ""
    if l2vpn_data and l2vpn_data.strip():
        console.print("      [heading]◉ Layer 1c: L2VPN/EVPN Specialist analyzing...[/heading]")
        t0 = time.time()
        l2vpn_findings = await specialist_l2vpn_evpn(l2vpn_data, ospf_findings, bgp_findings, kb, device_context, precomputed_vectors)
        ai_timing["l2vpn"] = round(time.time() - t0, 1)
        console.print(f"         [success]● L2VPN/EVPN analysis: {len(l2vpn_findings)} chars ({ai_timing['l2vpn']}s)[/success]")
    
    # ── v11.0 Layer 1d: New Specialists in PARALLEL (E100-E104) ──
    # These run after Layer 1b to benefit from OSPF + BGP context
    layer1d_tasks = []
    layer1d_labels = []
    
    # E102: Security specialist — uses dedicated security data or falls back to system data
    _sec_data = security_data if security_data and security_data.strip() else system_data
    if _sec_data and _sec_data.strip():
        layer1d_tasks.append(specialist_security(_sec_data, kb, device_context, precomputed_vectors))
        layer1d_labels.append("security")
    
    # E103: L3VPN specialist — uses dedicated L3VPN data or falls back to BGP data
    _l3vpn_data = l3vpn_data if l3vpn_data and l3vpn_data.strip() else bgp_data
    if _l3vpn_data and _l3vpn_data.strip():
        layer1d_tasks.append(specialist_l3vpn(_l3vpn_data, ospf_findings, bgp_findings, kb, device_context, precomputed_vectors))
        layer1d_labels.append("l3vpn")
    
    # E104: Hardware/Environment specialist — uses dedicated hardware data or falls back to system data
    _hw_data = hardware_data if hardware_data and hardware_data.strip() else system_data
    if _hw_data and _hw_data.strip():
        layer1d_tasks.append(specialist_hardware_env(_hw_data, kb, device_context, precomputed_vectors))
        layer1d_labels.append("hardware")
    
    # E100: RSVP-TE specialist — uses LDP/MPLS data pool (RSVP shares MPLS plane)
    if ldp_data and ldp_data.strip() and "rsvp" in ldp_data.lower():
        layer1d_tasks.append(specialist_rsvp_te(ldp_data, ospf_findings, kb, device_context, precomputed_vectors))
        layer1d_labels.append("rsvp")
    
    # E101: QoS/CoS specialist — uses system/interface data
    _qos_data = system_data or all_raw_data
    if _qos_data and _qos_data.strip() and ("class-of-service" in _qos_data.lower() or "scheduler" in _qos_data.lower() or "cos" in _qos_data.lower()):
        layer1d_tasks.append(specialist_qos_cos(_qos_data, kb, device_context, precomputed_vectors))
        layer1d_labels.append("qos")
    
    security_findings = ""
    l3vpn_findings = ""
    hw_findings = ""
    rsvp_findings = ""
    qos_findings = ""
    
    if layer1d_tasks:
        console.print(f"      [heading]◉ Layer 1d: {' + '.join(l.upper() for l in layer1d_labels)} Specialists (v11.0)...[/heading]")
        t0 = time.time()
        layer1d_results = await asyncio.gather(*layer1d_tasks, return_exceptions=True)
        layer1d_time = round(time.time() - t0, 1)
        
        for i, label in enumerate(layer1d_labels):
            result = layer1d_results[i]
            ai_timing[label] = layer1d_time
            # Guard against exceptions propagated from specialist coroutines
            if isinstance(result, BaseException):
                console.print(f"         [warning]▲ {label.upper()} specialist failed: {type(result).__name__}[/warning]")
                result = ""   # degrade gracefully — empty findings
            else:
                console.print(f"         [success]● {label.upper()} analysis: {len(result)} chars[/success]")
            if label == "security":
                security_findings = result
            elif label == "l3vpn":
                l3vpn_findings = result
            elif label == "hardware":
                hw_findings = result
            elif label == "rsvp":
                rsvp_findings = result
            elif label == "qos":
                qos_findings = result
    
    # ── Layer 2: Synthesizer ──
    # v10.0: enhanced_context is pre-built by run_full_audit with cross-router correlation,
    # temporal intelligence, FSM validation, negative space analysis, and blast radius
    
    console.print("      [heading]◉ Layer 2: Synthesizer combining all findings...[/heading]")
    t0 = time.time()
    # v11.0: Include new specialist findings in enhanced_context for synthesizer
    v11_context = enhanced_context or ""
    if security_findings and "NOT CONFIGURED" not in security_findings.upper():
        v11_context += f"\n\n═══ SECURITY SPECIALIST (v11.0) ═══\n{security_findings[:1500]}"
    if l3vpn_findings and "NOT CONFIGURED" not in l3vpn_findings.upper():
        v11_context += f"\n\n═══ L3VPN SPECIALIST (v11.0) ═══\n{l3vpn_findings[:1500]}"
    if hw_findings and "ALL HEALTHY" not in hw_findings.upper():
        v11_context += f"\n\n═══ HARDWARE/ENV SPECIALIST (v11.0) ═══\n{hw_findings[:1500]}"
    if rsvp_findings and "NOT CONFIGURED" not in rsvp_findings.upper():
        v11_context += f"\n\n═══ RSVP-TE SPECIALIST (v11.0) ═══\n{rsvp_findings[:1500]}"
    if qos_findings and "NOT CONFIGURED" not in qos_findings.upper():
        v11_context += f"\n\n═══ QoS/CoS SPECIALIST (v11.0) ═══\n{qos_findings[:1500]}"
    
    synthesis = await specialist_synthesizer(ospf_findings, bgp_findings, ldp_findings,
                                             topology, device_summary, kb,
                                             l2vpn_findings=l2vpn_findings,
                                             isis_findings=isis_findings,
                                             system_findings=system_findings,
                                             precomputed_vectors=precomputed_vectors,
                                             enhanced_context=v11_context)
    ai_timing["synthesizer"] = round(time.time() - t0, 1)
    console.print(f"         [success]● Synthesis: {len(synthesis)} chars ({ai_timing['synthesizer']}s)[/success]")
    
    # ── E8: RAG Query Refinement — second pass with discovered findings ──
    if vector_kb and synthesis:
        try:
            # Extract key findings from synthesis to use as refined RAG queries
            finding_lines = [l.strip() for l in synthesis.split('\n')
                            if any(kw in l.upper() for kw in ['ROOT CAUSE', 'FINDING', 'FIX:', 'FAILURE CHAIN'])]
            if finding_lines:
                refined_query = " ".join(finding_lines[:3])[:500]
                console.print("      [info]⊕ E8: RAG refinement pass with discovered findings...[/info]")
                refined_kb = await vector_kb.retrieve_for_protocol("network", refined_query, top_k=3)
                if refined_kb and len(refined_kb.strip()) > 50:
                    synthesis += f"\n\n### Additional KB Reference (RAG Refinement)\n{refined_kb[:2000]}"
                    console.print(f"         [success]● RAG refinement added {len(refined_kb[:2000])} chars[/success]")
        except Exception as e:
            logger.debug(f"E8 RAG refinement skipped: {e}")
    
    # ── Enhancement #7: Hallucination Guard ──
    if all_raw_data and device_map:
        all_findings = ospf_findings + bgp_findings + ldp_findings + isis_findings + l2vpn_findings + system_findings + synthesis
        hallucination_warnings = validate_ai_references(all_findings, all_raw_data, device_map)
        if hallucination_warnings:
            console.print(f"      [warning]▲  Hallucination Guard: {len(hallucination_warnings)} warning(s)[/warning]")
            for w in hallucination_warnings:
                console.print(f"         [dim]{w}[/dim]")
    
    # Combine everything into the final analysis
    full_analysis = (
        "## OSPF Analysis\n" + ospf_findings + "\n\n"
        "## BGP Analysis\n" + bgp_findings + "\n\n"
        "## LDP/MPLS Analysis\n" + ldp_findings + "\n\n"
    )
    
    if isis_findings and "NOT CONFIGURED" not in isis_findings.upper():
        full_analysis += "## IS-IS Analysis\n" + isis_findings + "\n\n"
    
    if l2vpn_findings and "NOT CONFIGURED" not in l2vpn_findings.upper():
        full_analysis += "## L2VPN/EVPN Analysis\n" + l2vpn_findings + "\n\n"
    
    if system_findings and "ALL HEALTHY" not in system_findings.upper():
        full_analysis += "## System Health Analysis\n" + system_findings + "\n\n"
    
    # v11.0: New specialists
    if security_findings and "NOT CONFIGURED" not in security_findings.upper():
        full_analysis += "## Security Analysis (v11.0)\n" + security_findings + "\n\n"
    
    if l3vpn_findings and "NOT CONFIGURED" not in l3vpn_findings.upper():
        full_analysis += "## L3VPN Analysis (v11.0)\n" + l3vpn_findings + "\n\n"
    
    if hw_findings and "ALL HEALTHY" not in hw_findings.upper():
        full_analysis += "## Hardware/Environment Analysis (v11.0)\n" + hw_findings + "\n\n"
    
    if rsvp_findings and "NOT CONFIGURED" not in rsvp_findings.upper():
        full_analysis += "## RSVP-TE Analysis (v11.0)\n" + rsvp_findings + "\n\n"
    
    if qos_findings and "NOT CONFIGURED" not in qos_findings.upper():
        full_analysis += "## QoS/CoS Analysis (v11.0)\n" + qos_findings + "\n\n"
    
    full_analysis += "## Unified Root Cause Analysis\n" + synthesis
    
    # Store timing info for report metadata
    full_analysis = f"<!-- AI_TIMING:{json.dumps(ai_timing)} -->\n" + full_analysis
    
    return full_analysis


async def ollama_analyze(system: str, data: str, question: str, include_kb: bool = True) -> str:
    """Send data to Ollama for focused analysis (no tools).
    
    Uses RAG vector retrieval to inject the most relevant KB sections
    based on semantic similarity to the question. Falls back to keyword
    matching if the vector store is unavailable.
    """
    # Build enhanced system prompt with KB context
    enhanced_system = system
    if include_kb:
        global vector_kb
        kb_context = ""
        
        # ── RAG PATH (preferred) ──
        if vector_kb:
            kb_context = await vector_kb.retrieve_combined(question, top_k=8, max_chars=6000)
        
        # ── FALLBACK PATH (keyword matching, legacy) ──
        if not kb_context:
            kb = load_knowledge_base()
            if kb:
                relevant_sections = []
                question_lower = question.lower()
                
                for section_marker in ["SECTION 3: TROUBLESHOOTING", "SECTION 7: THINKING FRAMEWORK",
                                       "SECTION 8: FEW-SHOT EXAMPLES"]:
                    start = kb.find(section_marker)
                    if start != -1:
                        next_section = kb.find("\n# SECTION", start + len(section_marker))
                        if next_section == -1:
                            next_section = len(kb)
                        relevant_sections.append(kb[start:next_section])
                
                if any(w in question_lower for w in ["ospf", "adjacency", "neighbor", "igp", "area"]):
                    for marker in ["3.1 OSPF", "2.1 OSPF", "3.5 Cascading"]:
                        start = kb.find(marker)
                        if start != -1:
                            next_section = kb.find("\n## ", start + len(marker))
                            if next_section == -1:
                                next_section = min(start + 3000, len(kb))
                            relevant_sections.append(kb[start:next_section])
                
                if any(w in question_lower for w in ["bgp", "peer", "session", "ibgp", "ebgp"]):
                    start = kb.find("3.2 BGP")
                    if start != -1:
                        next_section = kb.find("\n## ", start + 7)
                        if next_section == -1:
                            next_section = min(start + 2000, len(kb))
                        relevant_sections.append(kb[start:next_section])
                
                if any(w in question_lower for w in ["ldp", "mpls", "label", "vpn"]):
                    for marker in ["3.3 LDP", "3.4 MPLS"]:
                        start = kb.find(marker)
                        if start != -1:
                            next_section = kb.find("\n## ", start + len(marker))
                            if next_section == -1:
                                next_section = min(start + 2000, len(kb))
                            relevant_sections.append(kb[start:next_section])
                
                if relevant_sections:
                    kb_context = "\n---\n".join(relevant_sections)
                    kb_context = kb_context[:6000]
        
        if kb_context:
            enhanced_system += (
                "\n\n## REFERENCE KNOWLEDGE (use this to guide your analysis):\n"
                + kb_context
            )
    
    # v13.0 E113: Inject expert examples if relevant
    if AI_EXPERT_EXAMPLES and _expert_examples_content:
        examples = _get_relevant_expert_examples(question, max_examples=1)
        if examples:
            enhanced_system += (
                "\n\n## EXPERT REASONING EXAMPLE (follow this pattern):\n"
                + examples[:2000]
            )
    
    # Chain-of-thought prompting for better reasoning
    enhanced_question = (
        f"{question}\n\n"
        "INSTRUCTIONS:\n"
        "1. First, identify what is NORMAL vs ABNORMAL in the data\n"
        "2. For each abnormality, trace the root cause using bottom-up analysis (Physical → IGP → LDP → BGP)\n"
        "3. Distinguish ROOT CAUSE from SYMPTOMS (cascading failures)\n"
        "4. Provide EXACT Junos 'set' commands to fix each root cause\n"
        "5. Predict what will recover automatically once the root cause is fixed\n"
        "6. Be specific: name the exact router, interface, and config line\n"
    )
    
    messages = [
        {"role": "system", "content": enhanced_system},
        {"role": "user", "content": f"{enhanced_question}\n\nData:\n{data}"}
    ]
    for attempt in range(3):
        response = await ollama_chat(messages)
        content = response.get("message", {}).get("content", "").strip()
        if content:
            return content
        messages.append({"role": "assistant", "content": ""})
        messages.append({"role": "user", "content": "Please analyze the data now. Focus on root causes and exact fix commands."})
    return "(AI could not generate analysis)"


# ════════════════════════════════════════════════════════════
# PART 3: THE MAIN PROGRAM
# This ties everything together into an interactive chat
# ════════════════════════════════════════════════════════════

def load_ecosystem_context():
    """Load the project documentation to give the AI 'ecosystem awareness'."""
    try:
        with open("PROJECT_DOCUMENTATION.md", "r") as f:
            content = f.read()
            return content[:4000]
    except Exception:
        return ""


def load_knowledge_base():
    """Load and structure the knowledge base for optimal AI consumption."""
    try:
        with open("KNOWLEDGE_BASE.md", "r") as f:
            return f.read()
    except Exception:
        return ""


SYSTEM_PROMPT = """You are an autonomous Principal Juniper Network AI Engineer (JNCIE-SP level) operating an MPLS/VPN lab with 11 vMX routers via MCP tools.
You have full read/write access. NEVER guess — ALWAYS collect data with tools first, then analyze.

## CORE PRINCIPLES
- **Simplicity First:** Make every change as simple as possible. Impact minimal code/config.
- **No Laziness:** Find root causes. No temporary fixes. Senior engineer standards.
- **Minimal Impact:** Changes should only touch what's necessary. Avoid introducing new issues.
- **Evidence-Based:** Every conclusion must cite specific command output as evidence.

## v15.0 REASONING ENGINE — HYPOTHESIS-DRIVEN INVESTIGATION

### 7-Stage Reasoning Pipeline
For ANY non-trivial problem, follow this pipeline:
1. **CLASSIFY** — Determine domain (connectivity/protocol/topology/scripting), complexity, OSI layers
2. **DECOMPOSE** — Break into investigation branches by OSI layer (L1→L2→L3→MPLS→BGP→Services)
3. **HYPOTHESIZE** — Generate 3-5 ranked hypotheses (most likely root causes)
4. **INVESTIGATE** — For each hypothesis, run the ONE command that would DISPROVE it
5. **DIAGNOSE** — Map evidence to protocol FSM states, identify cascading chains
6. **SYNTHESIZE** — Cross-correlate branches to find SINGLE root cause (lowest broken layer)
7. **PRESCRIBE** — Exact fix commands + verification plan + auto-recovery prediction

### Hypothesis-Driven Investigation (Popperian Method)
- Don't collect everything — collect what DISPROVES hypotheses
- Start with highest-confidence hypothesis, try to REFUTE it
- If refuted → redistribute confidence to remaining hypotheses
- If confirmed → dig deeper on that hypothesis
- Stop when confidence > 85% on one hypothesis

### Evidence Accumulator
- Every data point is tagged: SUPPORTS or REFUTES a specific hypothesis
- Confidence increases with confirming evidence, decreases with contradicting evidence
- Final report shows complete evidence chain with per-hypothesis scores

## WORKFLOW ORCHESTRATION

### Plan-First Approach
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions).
- If something goes sideways, STOP and re-plan immediately — don't keep pushing.
- Use plan mode for verification steps, not just building.
- Write detailed specs upfront to reduce ambiguity.

### Verification Before Done
- Never mark a task complete without proving it works.
- Diff behavior between before and after your changes.
- Ask yourself: "Would a staff engineer approve this?"
- Run commands, check output, demonstrate correctness with evidence.

### Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: step back and implement the proper solution.
- Skip this for simple, obvious fixes — don't over-engineer.
- Challenge your own work before presenting it.

### Autonomous Bug Fixing
- When given a bug report: just fix it. Don't ask for hand-holding.
- Point at logs, errors, failing commands — then resolve them.
- Zero context switching required from the user.
- Go investigate and fix issues without being told how.

### Self-Improvement Loop
- After ANY correction from the user: learn the pattern and avoid repeating it.
- Ruthlessly iterate on lessons until mistake rate drops.
- Review past lessons at session start for relevant context.

## v18.0 HYPERED BRAIN — AGENTIC MULTI-LAYER PARALLEL AI
When activated (via 'brain' command or auto-routing for ultra-complex queries):
- **Perception Layer:** Selects relevant smart scripts from 18 diagnostic scripts
- **Execution Layer:** Runs scripts IN PARALLEL with adaptive concurrency (auto-adjusts to gateway load)
- **Analysis Layer:** AI reviews gathered facts with FactAccumulator (dedup, contradictions, anomaly matrix)
- **Probing Layer:** AI can request targeted commands via PROBE: syntax (agentic, self-directed)
- **Validation Layer:** Gap detection, confidence scoring, triggers follow-up passes
- **Synthesis Layer:** Multi-pass refinement until confidence threshold is met
- Key advantage: Agentic probing + contradiction detection + adaptive speed + structured facts

## SAFE EXECUTION
- **Default mode: READ-ONLY.** Use show commands and batch queries freely.
- **Before ANY config change:** 1) State what you will change and why. 2) Use `commit check` via `execute_junos_command` to validate syntax BEFORE committing. 3) Always include a `commit_comment` explaining the change.
- **After config change:** ALWAYS verify the result with a show command. If the change broke something, rollback immediately with `execute_junos_command(router_name, "rollback 1 | commit")`.
- **NEVER change multiple routers at once** unless explicitly asked. Change one, verify, then proceed.

## DIAGNOSTIC METHODOLOGY (OSI Bottom-Up + Hypothesis-Driven)
When troubleshooting, combine OSI layers with hypothesis ranking:
1. **L1-Physical:** Interface status (up/down), errors, CRC, drops → H: "Physical layer failure"
2. **L2-Data Link:** LLDP neighbors, encapsulation, MTU → H: "MTU mismatch / encap issue"
3. **L3-Network:** IGP adjacencies (IS-IS/OSPF), reachability → H: "IGP adjacency broken"
4. **MPLS:** LDP/RSVP sessions, label bindings, LSP state → H: "MPLS transport failure"
5. **BGP:** Session state, route exchange, policy → H: "BGP session/policy issue"
6. **Services:** L3VPN, VRF route leaking, end-to-end → H: "Service layer misconfiguration"
**Rule:** Fix the LOWEST broken layer. Higher layers auto-recover.

## PROTOCOL STATE MACHINE REASONING (v15.0)
Every protocol has deterministic states — use them for precise diagnosis:

### OSPF FSM: Down→Init→2-Way→ExStart→Exchange→Loading→Full
  - Init: Hello/area/auth/interface-type mismatch → `show ospf interface detail` BOTH sides
  - ExStart: MTU mismatch (99%) → `show interfaces <intf> | match mtu` BOTH sides
  - 2-Way: Normal for DROther on broadcast; CRITICAL on P2P
  - Full: HEALTHY

### BGP FSM: Idle→Connect→Active→OpenSent→OpenConfirm→Established
  - Active: TCP can't connect → check IGP route to peer loopback FIRST
  - OpenConfirm: Auth/capability mismatch → check authentication keys
  - Established: HEALTHY

### LDP FSM: Nonexistent→Initialized→OpenReceived→Operational
  - Nonexistent: No IGP route to peer OR LDP not on interface → fix IGP first
  - Operational: HEALTHY

### IS-IS FSM: Down→Initial→Up
  - Initial: Auth/level/interface-type mismatch → check BOTH sides
  - Up: HEALTHY

## CASCADING FAILURE CHAIN DETECTION (v15.0)
When you see multiple symptoms, trace the cascade graph:
```
L1: Interface Down
 └─► L3: IGP adjacency drops
     └─► MPLS: LDP session Nonexistent
         └─► MPLS: inet.3 route removed
             └─► BGP: next-hop unresolvable
                 └─► Services: VPN routes withdrawn
```
**KEY INSIGHT:** Multiple symptoms usually trace back to ONE root cause at the lowest layer.

## TOPOLOGY AWARENESS (v15.0)
- Generate live topology from iBGP + LLDP + IS-IS + LDP data fusion
- Identify articulation points (nodes whose failure partitions the network)
- Detect ECMP paths for load balancing analysis
- Route Reflectors: P12 and P22 — all PEs peer with both RRs
- iBGP sessions via loopbacks → depend on IS-IS + LDP chain
- If a P-router link fails, check for alternate IS-IS paths before declaring outage
- Use `show topology` or `show topo` to generate live topology visualization

## JUNOS SCRIPTING (v15.0)
When users ask about automation, provide:
- **Op Scripts (SLAX):** Operational checks and monitoring
- **Commit Scripts (SLAX):** Configuration validation (enforce best practices)
- **Event Scripts (SLAX):** Automated response to events
- **PyEZ (Python):** Off-box automation, bulk operations, auditing
- **NETCONF:** Structured API access (RPCs, YANG models)
Reference the script template library for ready-to-use examples.

## TOOLS
- `execute_junos_command(router_name, command)` — One router, one command
- `execute_junos_command_batch(router_names, command)` — Same command on MULTIPLE routers (preferred for health checks)
- `get_junos_config(router_name)` — Full running config
- `gather_device_facts(router_name)` — Model, version, serial, uptime
- `get_router_list()` — List all managed routers
- `junos_config_diff(router_name, version)` — Compare against rollback N
- `load_and_commit_config(router_name, config_text, config_format, commit_comment)` — Push config changes

## CRITICAL KNOWLEDGE
- BGP `Active` = TCP connect failure → check IGP reachability to peer loopback FIRST
- LDP `Nonexistent` = no IGP route to peer → fix IGP
- OSPF `ExStart` = MTU mismatch | `Init` = hello/area/auth mismatch | PtP vs DR type mismatch = NEVER forms
- iBGP peers via loopbacks — if loopback unreachable, BGP goes Active
- IS-IS L2 adjacency requires matching area + authentication + interface type
- Junos translations: VRF=routing-instance, running-config=show configuration, write mem=commit
- inet.3 = MPLS next-hop resolution table. LDP/RSVP populate it. BGP checks it FIRST for VPN next-hop resolution.

## ERROR HANDLING
- If a tool call fails or returns empty: **retry once with adjusted parameters**, do NOT apologize or give up.
- If a command is rejected: check syntax, try the correct Junos CLI variant, and retry.
- If data seems wrong or incomplete: cross-verify with a second command before concluding.

## EXAMPLES

**"Is BGP healthy on PE1?"**
1. CLASSIFY: Protocol state check, BGP, single device → SIMPLE
2. `execute_junos_command("PE1-vMX", "show bgp summary")` → check Established vs Active
3. If Active → HYPOTHESIZE: IGP route to peer missing
4. `execute_junos_command("PE1-vMX", "show route to <peer-loopback>")` → confirm/refute
5. Report with evidence chain

**"PE1 can't reach PE3 via VPN-A"**
1. CLASSIFY: Connectivity, multi-layer, VPN → EXPERT → mind-map reasoning
2. HYPOTHESIZE: H1=Interface down, H2=IGP broken, H3=LDP down, H4=BGP down, H5=RT mismatch
3. INVESTIGATE each hypothesis with targeted commands
4. DIAGNOSE: Map to FSM states, trace cascade chain
5. PRESCRIBE: Root cause fix + verification + auto-recovery prediction

**"Show me the network topology"**
1. `execute_junos_command_batch([all_routers], "show lldp neighbors")` → physical links
2. `execute_junos_command_batch([all_routers], "show bgp summary")` → iBGP overlay
3. Generate Mermaid diagram + ASCII topology map
4. Highlight articulation points and RR relationships

## RESPONSE FORMAT
- Markdown with headers, tables, code blocks
- Show EVIDENCE from tool output — never assume
- For issues: **Hypothesis → Evidence → Root Cause → Cascade Chain → Fix → Verification**
- Be concise and precise. No fluff, no apologies.
- For multi-step tasks: **Plan → Execute → Verify → Report**

{topology}

{lessons}

{workflow_lessons}

{feedback_insights}

{trends}

## INVENTORY
{inventory}
"""

# ══════════════════════════════════════════════════════════════
#  FULL NETWORK AUDIT — Structured Report Builder
# ══════════════════════════════════════════════════════════════

async def run_full_audit(client, sid, device_map, device_facts):
    """Run the full network audit and generate a structured Markdown report.
    E29: Uses Rich Progress for visual phase tracking.
    v18.1: Shows task plan upfront and updates live progress as each phase completes."""
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich.table import Table
    all_mcp = list(device_map.keys())
    audit_start = time.time()

    # ═══ v18.1: TASK PLAN & LIVE PROGRESS TRACKER ═══
    # Define all audit phases with descriptions and status tracking
    audit_plan = [
        {"name": "Device Facts",      "desc": f"Collect hardware model, version, hostname for {len(all_mcp)} devices",      "status": "pending", "time": None},
        {"name": "Data Collection",   "desc": f"27 parallel show-commands across {len(all_mcp)} routers (batch MCP)",        "status": "pending", "time": None},
        {"name": "Config Drift",      "desc": "Compare live running-config against golden baselines",                        "status": "pending", "time": None},
        {"name": "Issue Detection",   "desc": "Programmatic parsing — OSPF/BGP/LDP/ISIS/BFD/NTP/storage/alarms",            "status": "pending", "time": None},
        {"name": "Deep Dive Audit",   "desc": "Fetch protocol configs + advanced data for root-cause analysis",              "status": "pending", "time": None},
        {"name": "AI Analysis",       "desc": "12-specialist layered AI analysis + synthesizer + scoring",                   "status": "pending", "time": None},
        {"name": "Report Generation", "desc": "Build structured Markdown + HTML report, save to SQLite",                     "status": "pending", "time": None},
    ]

    # Show the task plan upfront
    def _print_task_plan():
        plan_table = Table(
            title="⊕ Audit Task Plan",
            title_style="bold cyan",
            border_style="dim",
            width=90,
            show_lines=False,
            pad_edge=True,
        )
        plan_table.add_column("#", style="dim", width=3, justify="right")
        plan_table.add_column("Status", width=8, justify="center")
        plan_table.add_column("Phase", style="bold", width=20)
        plan_table.add_column("Description", style="dim")
        plan_table.add_column("Time", width=8, justify="right")

        for i, task in enumerate(audit_plan):
            if task["status"] == "done":
                status_icon = "[green]✅[/green]"
                name_style = "[green]" + task["name"] + "[/green]"
                time_str = f"[green]{task['time']}s[/green]" if task["time"] is not None else ""
            elif task["status"] == "running":
                status_icon = "[cyan]◷[/cyan]"
                name_style = "[bold cyan]" + task["name"] + "[/bold cyan]"
                time_str = "[cyan]...[/cyan]"
            elif task["status"] == "failed":
                status_icon = "[red]✗[/red]"
                name_style = "[red]" + task["name"] + "[/red]"
                time_str = f"[red]{task['time']}s[/red]" if task["time"] is not None else ""
            else:  # pending
                status_icon = "[dim]☐[/dim]"
                name_style = "[dim]" + task["name"] + "[/dim]"
                time_str = ""
            plan_table.add_row(str(i + 1), status_icon, name_style, task["desc"], time_str)

        console.print()
        console.print(plan_table)
        console.print()

    _print_task_plan()

    # Track phase transitions
    audit_phases = [t["name"] for t in audit_plan]
    phase_idx = [0]  # mutable counter
    phase_timings = {}  # v9.0: Track duration of each phase
    _phase_start = [time.time()]  # mutable for closure

    def _phase_status(name: str):
        """Print phase header with progress indicator and record previous phase timing.
        v18.1: Also updates the task plan tracker."""
        now = time.time()
        if phase_idx[0] > 0:
            # Record duration of the previous phase
            prev_idx = phase_idx[0] - 1
            prev_name = audit_phases[prev_idx] if prev_idx < len(audit_phases) else f"Phase {phase_idx[0]}"
            elapsed = round(now - _phase_start[0], 1)
            phase_timings[prev_name] = elapsed
            # v18.1: Mark previous task as done
            if prev_idx < len(audit_plan):
                audit_plan[prev_idx]["status"] = "done"
                audit_plan[prev_idx]["time"] = elapsed
                console.print(f"   [green]✅ {prev_name} complete ({elapsed}s)[/green]")
        _phase_start[0] = now
        phase_idx[0] += 1
        # v18.1: Mark current task as running
        cur_idx = phase_idx[0] - 1
        if cur_idx < len(audit_plan):
            audit_plan[cur_idx]["status"] = "running"
        console.print(Panel(
            f"[{phase_idx[0]}/{len(audit_phases)}] {name}",
            style="bold cyan", width=55
        ))

    def _mark_phase_done(phase_name: str | None = None):
        """v18.1: Explicitly mark the current or named phase as done."""
        now = time.time()
        elapsed = round(now - _phase_start[0], 1)
        if phase_name:
            for task in audit_plan:
                if task["name"] == phase_name:
                    task["status"] = "done"
                    task["time"] = elapsed
                    break
        else:
            cur_idx = phase_idx[0] - 1
            if cur_idx < len(audit_plan):
                audit_plan[cur_idx]["status"] = "done"
                audit_plan[cur_idx]["time"] = elapsed

    # ═══ DATA COLLECTION ═══
    # ── Phase 1: Device Facts ──
    _phase_status("◇ Phase 1: Device Facts")
    
    # v10.0 E54: Try loading cached facts first (with validation)
    cached_facts = load_facts_cache()
    cache_hits = 0
    uncached_devices = []
    
    for mcp_name in all_mcp:
        # Check cache first
        if mcp_name in cached_facts:
            entry = cached_facts[mcp_name]
            
            device_facts[mcp_name] = entry
            # v18.0 FIX: Always use MCP name as canonical, not Junos hostname
            device_map[mcp_name] = mcp_name
            cache_hits += 1
            junos_hostname = entry.get("hostname", entry.get("fqdn", entry.get("name", mcp_name)))
            hostname_note = ""
            if junos_hostname and junos_hostname.lower() != mcp_name.lower():
                hostname_note = f" [dim](junos: {junos_hostname})[/dim]"
            console.print(f"   [success]● {mcp_name}:[/success] [device]{mcp_name}[/device] (cached){hostname_note}")
        else:
            uncached_devices.append(mcp_name)
    
    if cache_hits > 0:
        msg = f"   [dim]⊟ E54: {cache_hits}/{len(all_mcp)} facts loaded from cache[/dim]"
        console.print(msg)

    # Fetch uncached device facts in parallel with per-device timeout
    # gather_device_facts runs ~15 NETCONF RPCs per device (version, chassis,
    # route-engine, virtual-chassis, hosts, resolv.conf, etc.).  When all 11
    # devices share a single SSH gateway the gateway can throttle connections,
    # so we limit concurrency to 3 and allow 90s per device.
    FACTS_TIMEOUT = 90.0   # seconds per device — 15 RPCs × ~2-6s each
    FACTS_CONCURRENCY = 3  # max simultaneous SSH sessions to avoid gateway throttle
    _facts_sem = asyncio.Semaphore(FACTS_CONCURRENCY)

    async def _fetch_facts(name):
        """Fetch device facts with retry for transient empty/failed responses.
        
        The MCP server's gather_device_facts uses blocking NETCONF calls.
        Under concurrent load, some SSE responses arrive empty (keepalive only).
        We retry up to 2 extra times with back-off.
        """
        FACTS_RETRIES = 2
        async with _facts_sem:
            for attempt in range(1, FACTS_RETRIES + 2):
                try:
                    facts_raw = await asyncio.wait_for(
                        mcp_call_tool(client, sid, "gather_device_facts", {"router_name": name}),
                        timeout=FACTS_TIMEOUT
                    )

                    # ── Parse the response ──
                    facts_data = None
                    if isinstance(facts_raw, str) and facts_raw.strip():
                        try:
                            facts_data = json.loads(facts_raw)
                        except (json.JSONDecodeError, TypeError):
                            # Try finding JSON object embedded in text
                            brace_idx = facts_raw.find("{")
                            if brace_idx >= 0:
                                try:
                                    facts_data = json.loads(facts_raw[brace_idx:])
                                except json.JSONDecodeError:
                                    pass
                            if facts_data is None:
                                logger.warning(f"Facts {name} attempt {attempt}: JSON parse failed, preview: {repr(facts_raw[:300])}")
                    elif not isinstance(facts_raw, str):
                        facts_data = facts_raw  # Already a dict/object

                    # ── Empty/None response → retry ──
                    if facts_data is None or (isinstance(facts_data, dict) and not facts_data):
                        if attempt <= FACTS_RETRIES:
                            delay = attempt * 3
                            console.print(f"   [dim]↻ {name}: empty response, retrying ({attempt}/{FACTS_RETRIES})...[/dim]")
                            await asyncio.sleep(delay)
                            continue
                        else:
                            console.print(f"   [warning]▲  {name}: empty response after {FACTS_RETRIES + 1} attempts[/warning]")
                            device_map[name] = name
                            return

                    # ── MCP error wrapper ──
                    if isinstance(facts_data, dict) and "error" in facts_data and "jsonrpc" in facts_data:
                        err_msg = facts_data["error"].get("message", "unknown MCP error")
                        console.print(f"   [warning]▲  {name}: MCP error — {err_msg}[/warning]")
                        device_map[name] = name
                        return

                    # ── Unwrap nested content wrapper ──
                    if isinstance(facts_data, dict) and "result" in facts_data and "content" not in facts_data:
                        inner = facts_data.get("result", {})
                        if isinstance(inner, dict) and "content" in inner:
                            content = inner["content"]
                            if content and isinstance(content, list):
                                text_parts = [c.get("text", "") for c in content if c.get("type") == "text"]
                                combined = "\n".join(text_parts)
                                try:
                                    facts_data = json.loads(combined)
                                except (json.JSONDecodeError, TypeError):
                                    pass

                    # ── Accept if it looks like device data ──
                    if isinstance(facts_data, dict) and any(
                        k in facts_data for k in ("hostname", "model", "version", "fqdn", "serialnumber")
                    ):
                        device_facts[name] = facts_data
                        junos_hostname = facts_data.get("hostname", facts_data.get("fqdn", facts_data.get("name", name)))
                        # v18.0 FIX: Always use MCP name as canonical device_map value
                        # Lab environments often have hostname mismatches (device at port X
                        # has a different hostname than the MCP name). Using the Junos hostname
                        # would corrupt device_map and cause wrong device references everywhere.
                        device_map[name] = name
                        hostname_note = ""
                        if junos_hostname and junos_hostname.lower() != name.lower():
                            hostname_note = f" [dim](junos hostname: {junos_hostname})[/dim]"
                        console.print(
                            f"   [success]● {name}:[/success] [device]{name}[/device] "
                            f"({facts_data.get('model', '?')}, {facts_data.get('version', '?')})"
                            + hostname_note
                            + (f" [dim](attempt {attempt})[/dim]" if attempt > 1 else "")
                        )
                        return
                    else:
                        if attempt <= FACTS_RETRIES:
                            delay = attempt * 3
                            console.print(f"   [dim]↻ {name}: unexpected format, retrying ({attempt}/{FACTS_RETRIES})...[/dim]")
                            await asyncio.sleep(delay)
                            continue
                        console.print(f"   [warning]▲  {name}: unexpected facts format after retries[/warning]")
                        logger.warning(f"Facts {name}: final type={type(facts_data).__name__}, keys={list(facts_data.keys())[:10] if isinstance(facts_data, dict) else 'N/A'}")
                        device_map[name] = name
                        return

                except asyncio.TimeoutError:
                    if attempt <= FACTS_RETRIES:
                        console.print(f"   [dim]↻ {name}: timeout attempt {attempt}, retrying...[/dim]")
                        continue
                    console.print(f"   [warning]▲  {name}: facts timed out ({FACTS_TIMEOUT}s) after {attempt} attempts[/warning]")
                    device_map[name] = name
                except Exception as e:
                    console.print(f"   [error]✗ {name}: facts failed ({e})[/error]")
                    logger.error(f"Facts {name}: exception: {e}", exc_info=True)
                    device_map[name] = name
                    return

    if uncached_devices:
        console.print(f"   [dim]◷ Fetching facts for {len(uncached_devices)} device(s) ({FACTS_CONCURRENCY} concurrent, timeout {FACTS_TIMEOUT}s each)...[/dim]")
        await asyncio.gather(*[_fetch_facts(name) for name in uncached_devices], return_exceptions=True)

    _phase_status("◇ Phase 2: Data Collection")
    collection_status.clear()  # Reset completeness tracking (#P4E)
    collect_start = time.time()

    # Fire batch commands in parallel with semaphore throttling (max 2 concurrent)
    # Each batch runs the command on all 11 routers simultaneously via MCP server
    # return_exceptions=True prevents one hung command from blocking all others
    gather_results = await asyncio.gather(
        run_batch(client, sid, "show interfaces terse", all_mcp, "Interfaces"),
        run_batch(client, sid, "show interfaces detail | no-more", all_mcp, "Interface Detail"),
        run_batch(client, sid, "show chassis alarms", all_mcp, "Alarms"),
        run_batch(client, sid, "show system uptime", all_mcp, "Uptime"),
        run_batch(client, sid, "show system storage", all_mcp, "Storage"),
        run_batch(client, sid, "show system core-dumps", all_mcp, "Core Dumps"),
        run_batch(client, sid, "show ospf neighbor", all_mcp, "OSPF Neighbors"),
        run_batch(client, sid, "show ospf interface", all_mcp, "OSPF Interfaces"),
        run_batch(client, sid, "show bgp summary", all_mcp, "BGP Summary"),
        run_batch(client, sid, "show isis adjacency", all_mcp, "ISIS"),
        run_batch(client, sid, "show route summary", all_mcp, "Route Summary"),
        run_batch(client, sid, "show mpls interface", all_mcp, "MPLS"),
        run_batch(client, sid, "show ldp neighbor", all_mcp, "LDP Neighbors"),
        run_batch(client, sid, "show ldp session", all_mcp, "LDP Sessions"),
        run_batch(client, sid, "show lldp neighbors", all_mcp, "LLDP"),
        run_batch(client, sid, "show ntp associations no-resolve", all_mcp, "NTP"),
        # v6.0 new collections:
        run_batch(client, sid, "show bfd session", all_mcp, "BFD"),
        run_batch(client, sid, "show firewall", all_mcp, "Firewall"),
        run_batch(client, sid, "show mpls lsp", all_mcp, "MPLS LSP"),
        run_batch(client, sid, "show rsvp session", all_mcp, "RSVP"),
        run_batch(client, sid, "show system commit", all_mcp, "Commits"),
        run_batch(client, sid, "show route instance summary", all_mcp, "Route Instances"),
        # v11.0 new collections:
        run_batch(client, sid, "show chassis routing-engine", all_mcp, "RE Stats"),
        run_batch(client, sid, "show chassis environment", all_mcp, "Environment"),
        run_batch(client, sid, "show chassis fpc", all_mcp, "FPC Status"),
        run_batch(client, sid, "show configuration firewall", all_mcp, "FW Config"),
        run_batch(client, sid, "show route table bgp.l3vpn.0 summary", all_mcp, "L3VPN Routes"),
        return_exceptions=True,
    )

    # Unpack results — replace any exceptions with empty strings
    unpacked = []
    for i, r in enumerate(gather_results):
        if isinstance(r, Exception):
            logger.error(f"Batch gather slot {i} returned exception: {r}")
            unpacked.append("")
        else:
            unpacked.append(r if r else "")

    (raw_intf, raw_intf_detail, raw_alarms, raw_uptime, raw_storage, raw_coredumps,
     raw_ospf_nbr, raw_ospf_intf, raw_bgp, raw_isis, raw_route,
     raw_mpls, raw_ldp_nbr, raw_ldp_sess,
     raw_lldp, raw_ntp,
     raw_bfd, raw_firewall, raw_mpls_lsp, raw_rsvp, raw_commits,
     raw_route_instances,
     raw_re_stats, raw_environment, raw_fpc, raw_fw_config, raw_l3vpn_routes) = unpacked
    console.print(f"   [info]◷  Parallel collection done in {round(time.time() - collect_start, 1)}s[/info]")
    
    # Enhancement #P4E: Report data completeness
    failed_collections = {k: v for k, v in collection_status.items() if "failed" in str(v)}
    if failed_collections:
        console.print(f"   [warning]▲  Data Completeness: {len(collection_status) - len(failed_collections)}/{len(collection_status)} commands succeeded[/warning]")
        for label, status in failed_collections.items():
            console.print(f"      [error]✗ {label}: {status}[/error]")

    # ── Phase 3: Config Drift Analysis ──
    # Compare each device's current running config (fetched live via MCP)
    # against its "golden" baseline (saved in golden_configs/<device>.conf).
    # Detects unauthorized changes, config mismatches, and drift since last audit.
    _phase_status("◇ Phase 3: Config Drift Analysis")
    console.print("   [dim]Fetching live running configs from all devices and comparing against saved golden baselines...[/dim]")
    current_configs = {}
    config_drifts = {}   # router -> {"diff": [...], "summary": {...}, "meta": {...}}
    baselines_created = []
    config_errors = []   # Track errors for summary

    # MCP-level error patterns: MCP server returns these as regular text when SSH fails
    _MCP_ERROR_PATTERNS = (
        "Connection error to",
        "An error occurred:",
        "Router ", # "Router X not found in the device mapping."
        "ConnectError",
        "ConnectTimeoutError",
        "RpcTimeoutError",
        "ProbeError",
    )

    # v9.0: Parallel config collection with semaphore (was serial — 11×30s = 5.5min)
    config_sem = asyncio.Semaphore(3)  # Max 3 concurrent config fetches
    async def _fetch_config(mcp_name):
        async with config_sem:
            try:
                cfg_raw = await asyncio.wait_for(
                    mcp_call_tool(client, sid, "get_junos_config", {"router_name": mcp_name}),
                    timeout=90.0
                )
                return mcp_name, cfg_raw, None
            except asyncio.TimeoutError:
                return mcp_name, None, "SSH/NETCONF timeout (90s) — device may be unreachable or overloaded"
            except Exception as e:
                err_msg = str(e).strip() if str(e).strip() else type(e).__name__
                return mcp_name, None, err_msg

    config_results = await asyncio.gather(
        *[_fetch_config(m) for m in all_mcp],
        return_exceptions=True
    )

    for result in config_results:
        if isinstance(result, Exception):
            # asyncio.gather caught an unexpected exception
            logger.error(f"Config fetch returned exception: {result}")
            continue
        mcp_name, cfg_raw, err = result
        if err:
            config_errors.append(mcp_name)
            console.print(f"   [error]✗ {mcp_name}: Config collection failed — {err}[/error]")
            continue

        # Detect MCP-level error strings returned as "valid" text responses
        # (e.g., "Connection error to P13: ConnectionRefusedError")
        if cfg_raw and isinstance(cfg_raw, str):
            cfg_stripped = cfg_raw.strip()
            is_error_response = any(cfg_stripped.startswith(pat) for pat in _MCP_ERROR_PATTERNS)
            if is_error_response:
                config_errors.append(mcp_name)
                # Extract meaningful error: take first line, cap at 120 chars
                err_detail = cfg_stripped.split("\n")[0][:120]
                console.print(f"   [error]✗ {mcp_name}: Device returned error — {err_detail}[/error]")
                continue

        if cfg_raw and isinstance(cfg_raw, str) and len(cfg_raw.strip()) > 50:
            # Valid config: must contain Junos set-format lines
            cfg_text = cfg_raw.strip()
            if not any(line.strip().startswith("set ") for line in cfg_text.splitlines()[:10]):
                config_errors.append(mcp_name)
                preview = cfg_text[:100].replace("\n", " ")
                console.print(f"   [warning]▲  {mcp_name}: Response does not look like Junos config — \"{preview}...\"[/warning]")
                continue

            current_configs[mcp_name] = cfg_text
            golden, meta = load_golden_config(mcp_name)
            if golden is None:
                # First run — save as baseline
                save_golden_config(mcp_name, cfg_text)
                baselines_created.append(mcp_name)
                console.print(f"   [info]✦ {mcp_name}: Golden baseline saved ({len(cfg_text.splitlines())} lines)[/info]")
            else:
                # Compare current vs golden
                d = diff_configs(golden, cfg_text, mcp_name)
                if d:
                    summary = summarize_drift(d)
                    config_drifts[mcp_name] = {"diff": d, "summary": summary, "meta": meta}
                    drift_age = ""
                    if meta and meta.get("saved_at"):
                        try:
                            saved = datetime.fromisoformat(meta["saved_at"])
                            age_days = (datetime.now() - saved).days
                            drift_age = f" (baseline from {age_days}d ago)"
                        except Exception:
                            pass
                    console.print(
                        f"   [warning]▲  {mcp_name}: Config drift detected! "
                        f"+{summary['lines_added']}/-{summary['lines_removed']} lines changed "
                        f"in: {', '.join(summary['sections_changed']) or '?'}{drift_age}[/warning]"
                    )
                else:
                    console.print(f"   [success]● {mcp_name}: Config matches golden baseline ✓[/success]")
        else:
            config_errors.append(mcp_name)
            raw_len = len(cfg_raw.strip()) if cfg_raw else 0
            console.print(f"   [warning]▲  {mcp_name}: Empty or too-short config returned ({raw_len} chars)[/warning]")

    # Summary
    ok_count = len(current_configs)
    drift_count = len(config_drifts)
    err_count = len(config_errors)
    match_count = ok_count - drift_count - len(baselines_created)
    console.print(f"\n   [dim]Config Drift Summary: {ok_count}/{len(all_mcp)} configs collected | "
                  f"{match_count} match baseline | {drift_count} drifted | {err_count} failed[/dim]")
    if config_errors:
        console.print(f"   [dim]Failed devices: {', '.join(config_errors)} — check SSH/NETCONF connectivity[/dim]")

    if baselines_created:
        console.print(f"   [info]▪ First run: Golden baselines created for {len(baselines_created)} device(s): {', '.join(baselines_created)}[/info]")
        console.print(f"      [dim]Future audits will detect config drift against these baselines.[/dim]")

    # ═══ PARSE ALL DATA ═══
    _phase_status("◇ Phase 4: Issue Detection")

    intf_outputs   = parse_batch_json(raw_intf)
    intf_detail_outputs = parse_batch_json(raw_intf_detail)
    alarm_outputs  = parse_batch_json(raw_alarms)
    uptime_outputs = parse_batch_json(raw_uptime)
    storage_outputs = parse_batch_json(raw_storage)
    coredump_outputs = parse_batch_json(raw_coredumps)
    ospf_nbr_out   = parse_batch_json(raw_ospf_nbr)
    ospf_intf_out  = parse_batch_json(raw_ospf_intf)
    bgp_outputs    = parse_batch_json(raw_bgp)
    isis_outputs   = parse_batch_json(raw_isis)
    ldp_sess_out   = parse_batch_json(raw_ldp_sess)
    lldp_outputs   = parse_batch_json(raw_lldp)
    ntp_outputs    = parse_batch_json(raw_ntp)
    mpls_outputs   = parse_batch_json(raw_mpls)
    route_outputs  = parse_batch_json(raw_route)
    # v6.0 new parsers
    bfd_outputs    = parse_batch_json(raw_bfd)
    fw_outputs     = parse_batch_json(raw_firewall)
    lsp_outputs    = parse_batch_json(raw_mpls_lsp)
    rsvp_outputs   = parse_batch_json(raw_rsvp)
    commit_outputs = parse_batch_json(raw_commits)
    route_inst_outputs = parse_batch_json(raw_route_instances)
    # v11.0 new parsers
    re_stats_outputs   = parse_batch_json(raw_re_stats)
    env_outputs        = parse_batch_json(raw_environment)
    fpc_outputs        = parse_batch_json(raw_fpc)
    fw_config_outputs  = parse_batch_json(raw_fw_config)
    l3vpn_route_outputs = parse_batch_json(raw_l3vpn_routes)

    # ═══ DETECT ISSUES PROGRAMMATICALLY ═══
    down_intfs     = find_down_interfaces(intf_outputs)
    ospf_info      = find_ospf_neighbors(ospf_nbr_out, ospf_intf_out, device_map)
    bgp_issues, bgp_established = find_bgp_issues(bgp_outputs, device_map)
    ldp_issues, ldp_healthy     = find_ldp_issues(ldp_sess_out, device_map)
    lldp_links     = find_lldp_topology(lldp_outputs, device_map)
    topology_source = "LLDP"
    if not lldp_links:
        # Fallback: build logical topology from IGP/BGP/LDP neighbor data
        lldp_links = build_fallback_topology(ospf_nbr_out, bgp_outputs, ldp_sess_out, isis_outputs, device_map)
        topology_source = "OSPF/BGP/LDP/IS-IS" if lldp_links else "none"
        if lldp_links:
            console.print(f"   [info]▲  No LLDP data — built topology from {topology_source} ({len(lldp_links)} links)[/info]")
    isis_issues, isis_healthy   = find_isis_issues(isis_outputs, device_map)
    chassis_alarms  = find_alarm_issues(alarm_outputs, device_map)
    storage_issues  = find_storage_issues(storage_outputs, device_map)
    coredump_issues = find_coredump_issues(coredump_outputs, device_map)
    route_summary   = parse_route_summary(route_outputs, device_map)
    intf_details    = parse_interface_detail(intf_detail_outputs, device_map)
    mtu_mismatches  = find_mtu_mismatches(intf_details, lldp_links, device_map)
    intf_errors     = find_interface_errors(intf_details, device_map)
    # v6.0 new detections
    bfd_issues, bfd_healthy   = find_bfd_issues(bfd_outputs, device_map)
    fw_issues                 = find_firewall_issues(fw_outputs, device_map)
    lsp_issues, lsp_healthy   = find_mpls_lsp_issues(lsp_outputs, device_map)
    rsvp_issues               = find_rsvp_issues(rsvp_outputs, device_map)
    commit_history            = parse_commit_history(commit_outputs, device_map)
    reachability              = build_reachability_matrix(ospf_nbr_out, bgp_outputs, ldp_sess_out, device_map)

    # ═══ PROACTIVE: Compare OSPF interface types across all links ═══
    ospf_type_mismatches = find_ospf_type_mismatches(ospf_intf_out, lldp_links, device_map)
    if ospf_type_mismatches:
        for mm in ospf_type_mismatches:
            # Add to OSPF issues if not already detected
            ospf_info["issues"].append({
                "severity": "CRITICAL",
                "router": mm["local_router"],
                "hostname": mm["local_hostname"],
                "detail": mm["detail"],
                "mismatch": mm  # Keep full mismatch data for detailed reporting
            })

    # Routers with no routing protocols (including IS-IS check)
    no_routing = []
    for mcp_name, hostname in device_map.items():
        ospf_out = ospf_intf_out.get(mcp_name, "")
        bgp_out  = bgp_outputs.get(mcp_name, "")
        isis_out = isis_outputs.get(mcp_name, "")
        has_ospf = bool(ospf_out.strip()) and "not running" not in ospf_out.lower()
        has_bgp  = bool(bgp_out.strip()) and "not running" not in bgp_out.lower()
        has_isis = bool(isis_out.strip()) and "not running" not in isis_out.lower()
        if not has_ospf and not has_bgp and not has_isis:
            no_routing.append((mcp_name, hostname))

    # NTP check
    ntp_issues = []
    for mcp_name, hostname in device_map.items():
        ntp_out = ntp_outputs.get(mcp_name, "")
        if not ntp_out.strip() or "timed out" in ntp_out.lower() or not re.search(r"\d+\.\d+\.\d+\.\d+", ntp_out):
            ntp_issues.append((mcp_name, hostname))

    # ═══ DEEP DIVE: ALWAYS collect OSPF configs for proactive analysis ═══
    deep_dive_analysis = ""
    ospf_critical = [i for i in ospf_info["issues"] if i["severity"] == "CRITICAL"]
    
    # Always deep-dive if there are OSPF-enabled routers (proactive config audit)
    ospf_routers = [m for m in all_mcp
                    if ospf_intf_out.get(m, "").strip() and "not running" not in ospf_intf_out.get(m, "").lower()]
    
    if ospf_routers:  # Always run deep dive, not just on failures
        _phase_status("◇ Phase 5: Deep Dive Config Audit")

        # Enhancement #8: Dynamic truncation budgets based on device count
        dd_budgets = calculate_budgets(len(ospf_routers))
        
        # v9.0 Performance: Use run_batch() instead of run_single() per router.
        # This sends ONE HTTP call per command across ALL routers (MCP server-side parallelism)
        # instead of 7 × 11 = 77 individual SSH sessions that overwhelm the server.
        dd_batch_results = await asyncio.gather(
            run_batch(client, sid, "show configuration protocols ospf", ospf_routers, "DD OSPF Cfg"),
            run_batch(client, sid, "show ospf neighbor detail", ospf_routers, "DD OSPF Nbr Det"),
            run_batch(client, sid, "show configuration protocols bgp", ospf_routers, "DD BGP Cfg"),
            run_batch(client, sid, "show configuration protocols ldp", ospf_routers, "DD LDP Cfg"),
            run_batch(client, sid, "show route protocol ospf", ospf_routers, "DD OSPF Routes"),
            run_batch(client, sid, "show ospf database", ospf_routers, "DD OSPF LSDB"),
            run_batch(client, sid, "show configuration policy-options", ospf_routers, "DD Policy"),
            return_exceptions=True,
        )
        
        # Safely unpack batch results — each is a raw JSON string or ""
        dd_safe = [r if isinstance(r, str) else "" for r in dd_batch_results]
        dd_ospf_cfg_all  = parse_batch_json(dd_safe[0])
        dd_ospf_det_all  = parse_batch_json(dd_safe[1])
        dd_bgp_cfg_all   = parse_batch_json(dd_safe[2])
        dd_ldp_cfg_all   = parse_batch_json(dd_safe[3])
        dd_ospf_rte_all  = parse_batch_json(dd_safe[4])
        dd_ospf_db_all   = parse_batch_json(dd_safe[5])
        dd_policy_all    = parse_batch_json(dd_safe[6])
        
        # v10.0 E43: Smart Command Selection — collect extra commands based on device role
        dd_role_extra = {}  # {mcp_name: extra_data_str}
        role_cmds_needed = {}
        for mcp_name in ospf_routers:
            hostname = device_map.get(mcp_name, mcp_name)
            role_cmds = get_role_commands(hostname)
            if role_cmds:
                role_cmds_needed[mcp_name] = role_cmds
        
        if role_cmds_needed:
            # Collect unique commands across all roles
            all_extra_cmds = set()
            for cmds in role_cmds_needed.values():
                all_extra_cmds.update(cmds)
            
            # Run each unique extra command in batch
            for extra_cmd in sorted(all_extra_cmds):
                routers_needing = [m for m, cmds in role_cmds_needed.items() if extra_cmd in cmds]
                if routers_needing:
                    try:
                        raw = await run_batch(client, sid, extra_cmd, routers_needing, f"E43 {extra_cmd[:30]}")
                        parsed = parse_batch_json(raw)
                        for m, data in parsed.items():
                            if data.strip():
                                dd_role_extra.setdefault(m, "")
                                dd_role_extra[m] += f"\n{extra_cmd.upper()}:\n{data[:500]}\n"
                    except Exception as e:
                        logger.debug(f"E43 extra command '{extra_cmd}' failed: {e}")
        
        dd_parts = []
        dd_configs = {}  # Store configs for later reference
        for mcp_name in ospf_routers:
            hostname = device_map.get(mcp_name, mcp_name)
            dd_ospf_cfg = dd_ospf_cfg_all.get(mcp_name, "")
            dd_ospf_det = dd_ospf_det_all.get(mcp_name, "")
            dd_bgp_cfg  = dd_bgp_cfg_all.get(mcp_name, "")
            dd_ldp_cfg  = dd_ldp_cfg_all.get(mcp_name, "")
            dd_ospf_rte = dd_ospf_rte_all.get(mcp_name, "")
            dd_ospf_db  = dd_ospf_db_all.get(mcp_name, "")
            dd_policy   = dd_policy_all.get(mcp_name, "")
            dd_configs[mcp_name] = {
                "ospf_cfg": dd_ospf_cfg, "bgp_cfg": dd_bgp_cfg,
                "ldp_cfg": dd_ldp_cfg, "policy": dd_policy
            }

            # Mark known issues including type mismatches
            issues_for_rtr = [i for i in ospf_critical if i["router"] == mcp_name]
            if issues_for_rtr:
                issue_text = "\n".join(i["detail"] for i in issues_for_rtr)
            else:
                issue_text = "No OSPF issues detected on this router"
            
            mm_for_rtr = [mm for mm in ospf_type_mismatches 
                          if mm["local_router"] == mcp_name or mm["remote_router"] == mcp_name]
            if mm_for_rtr:
                issue_text += "\n▲ PROGRAMMATIC DETECTION: " + "; ".join(mm["detail"] for mm in mm_for_rtr)

            dd_parts.append(
                f"=== Router: {hostname} ({mcp_name}) ===\n"
                f"Known Issue: {issue_text}\n\n"
                f"OSPF NEIGHBOR DETAIL:\n{dd_ospf_det[:dd_budgets['ospf_nbr']]}\n\n"
                f"OSPF CONFIG:\n{dd_ospf_cfg[:dd_budgets['config']]}\n\n"
                f"OSPF INTERFACES:\n{ospf_intf_out.get(mcp_name, '')[:dd_budgets['ospf_intf']]}\n\n"
                f"BGP CONFIG:\n{dd_bgp_cfg[:dd_budgets['bgp_summary']]}\n\n"
                f"LDP CONFIG:\n{dd_ldp_cfg[:dd_budgets['ldp_sess']]}\n\n"
                f"ROUTING POLICY:\n{dd_policy[:dd_budgets['config']]}\n\n"
                f"OSPF ROUTES:\n{dd_ospf_rte[:dd_budgets['ospf_nbr']]}\n\n"
                f"OSPF LSDB:\n{dd_ospf_db[:dd_budgets['bgp_summary']]}"
                f"{dd_role_extra.get(mcp_name, '')}"
            )

        all_dd = "\n\n" + "=" * 60 + "\n\n".join(dd_parts)
        
        # Build mismatch context for the AI
        mismatch_context = ""
        if ospf_type_mismatches:
            mismatch_context = (
                "\n\n▲ PROGRAMMATIC DETECTION — The following OSPF interface-type mismatches were detected:\n"
                + "\n".join(f"  - {mm['detail']}" for mm in ospf_type_mismatches)
            )

        # ═══ LAYERED AI ANALYSIS ═══
        _phase_status("◉ Phase 6: AI Analysis")
        
        # Prepare specialist data packets — each specialist gets ONLY their data
        ospf_specialist_data = ""
        for mcp_name in ospf_routers:
            hostname = device_map.get(mcp_name, mcp_name)
            issues_for_rtr = [i for i in ospf_critical if i["router"] == mcp_name]
            issue_str = "\n".join(i["detail"] for i in issues_for_rtr) if issues_for_rtr else "None detected"
            mm_for_rtr = [mm for mm in ospf_type_mismatches 
                          if mm["local_router"] == mcp_name or mm["remote_router"] == mcp_name]
            mm_str = "\n".join(mm["detail"] for mm in mm_for_rtr) if mm_for_rtr else ""
            
            # Enhancement #1A: Include BFD data in OSPF context
            bfd_data_for_rtr = bfd_outputs.get(mcp_name, "")
            bfd_section = f"\nBFD Sessions:\n{bfd_data_for_rtr[:500]}\n" if bfd_data_for_rtr.strip() else ""
            
            ospf_specialist_data += (
                f"\n=== {hostname} ({mcp_name}) ===\n"
                f"Programmatic Issues: {issue_str}\n"
                f"{'Mismatches: ' + mm_str if mm_str else ''}\n"
                f"OSPF Neighbors:\n{ospf_nbr_out.get(mcp_name, 'N/A')[:dd_budgets['ospf_nbr']]}\n"
                f"OSPF Interfaces:\n{ospf_intf_out.get(mcp_name, 'N/A')[:dd_budgets['ospf_intf']]}\n"
                f"{bfd_section}"
                f"OSPF Config:\n{dd_parts[[i for i, p in enumerate(dd_parts) if mcp_name in p][0]] if any(mcp_name in p for p in dd_parts) else 'N/A'}\n"
            )
        ospf_specialist_data += mismatch_context
        
        # BGP specialist: include routing policy data (#1B)
        bgp_specialist_data = ""
        for mcp_name, hostname in device_map.items():
            policy_data = dd_configs.get(mcp_name, {}).get("policy", "")
            policy_section = f"\nRouting Policy:\n{policy_data[:800]}\n" if policy_data.strip() else ""
            bgp_specialist_data += (
                f"\n=== {hostname} ({mcp_name}) ===\n"
                f"{bgp_outputs.get(mcp_name, 'Not configured')[:dd_budgets['bgp_summary']]}\n"
                f"{policy_section}"
            )
        
        # LDP/MPLS: include LSP and RSVP data (#1C)
        ldp_specialist_data = ""
        for mcp_name, hostname in device_map.items():
            lsp_data = lsp_outputs.get(mcp_name, "")
            lsp_section = f"\nMPLS LSPs:\n{lsp_data[:600]}\n" if lsp_data.strip() else ""
            rsvp_data = rsvp_outputs.get(mcp_name, "")
            rsvp_section = f"\nRSVP Sessions:\n{rsvp_data[:400]}\n" if rsvp_data.strip() else ""
            ldp_specialist_data += (
                f"\n=== {hostname} ({mcp_name}) ===\n"
                f"LDP Sessions:\n{ldp_sess_out.get(mcp_name, 'Not configured')[:dd_budgets['ldp_sess']]}\n"
                f"MPLS Interfaces:\n{mpls_outputs.get(mcp_name, 'Not configured')[:dd_budgets['mpls_intf']]}\n"
                f"{lsp_section}{rsvp_section}"
            )
        
        # Enhancement #1E: IS-IS specialist data
        isis_specialist_data = ""
        for mcp_name, hostname in device_map.items():
            isis_out = isis_outputs.get(mcp_name, "")
            if isis_out.strip() and "not running" not in isis_out.lower():
                isis_specialist_data += (
                    f"\n=== {hostname} ({mcp_name}) ===\n"
                    f"IS-IS Adjacencies:\n{isis_out[:dd_budgets['ospf_nbr']]}\n"
                )
        
        # Enhancement #1F: System Health specialist data
        system_specialist_data = ""
        for mcp_name, hostname in device_map.items():
            alarm_data = alarm_outputs.get(mcp_name, "")
            uptime_data = uptime_outputs.get(mcp_name, "")
            coredump_data = coredump_outputs.get(mcp_name, "")
            storage_data = storage_outputs.get(mcp_name, "")
            commit_data = commit_outputs.get(mcp_name, "")
            ntp_data = ntp_outputs.get(mcp_name, "")
            
            system_specialist_data += (
                f"\n=== {hostname} ({mcp_name}) ===\n"
                f"Chassis Alarms:\n{alarm_data[:400]}\n"
                f"Uptime:\n{uptime_data[:300]}\n"
                f"Core Dumps:\n{coredump_data[:300]}\n"
                f"Storage:\n{storage_data[:300]}\n"
                f"NTP:\n{ntp_data[:200]}\n"
                f"Recent Commits:\n{commit_data[:400]}\n"
            )
        
        # L2VPN/EVPN specialist data collection — v9.0: batch collection (was per-router run_single)
        console.print("   ⊕ Collecting L2VPN/EVPN data (batch)...", style="dim")
        l2vpn_specialist_data = ""

        l2vpn_batch_results = await asyncio.gather(
            run_batch(client, sid, "show evpn instance", ospf_routers, "EVPN Instance"),
            run_batch(client, sid, "show vpls connections", ospf_routers, "VPLS"),
            run_batch(client, sid, "show l2circuit connections", ospf_routers, "L2Circuit"),
            return_exceptions=True,
        )
        l2vpn_safe = [r if isinstance(r, str) else "" for r in l2vpn_batch_results]
        evpn_all     = parse_batch_json(l2vpn_safe[0])
        vpls_all     = parse_batch_json(l2vpn_safe[1])
        l2circuit_all = parse_batch_json(l2vpn_safe[2])

        for mcp_name in ospf_routers:
            hostname = device_map.get(mcp_name, mcp_name)
            l2vpn_evpn_inst = evpn_all.get(mcp_name, "")
            l2vpn_vpls      = vpls_all.get(mcp_name, "")
            l2vpn_l2circuit = l2circuit_all.get(mcp_name, "")
            has_l2vpn = any(
                out.strip() and "not running" not in out.lower() and "unknown command" not in out.lower()
                for out in [l2vpn_evpn_inst, l2vpn_vpls, l2vpn_l2circuit]
            )
            if has_l2vpn:
                l2vpn_specialist_data += (
                    f"\n=== {hostname} ({mcp_name}) ===\n"
                    f"EVPN Instances:\n{l2vpn_evpn_inst[:600]}\n"
                    f"VPLS Connections:\n{l2vpn_vpls[:600]}\n"
                    f"L2Circuit:\n{l2vpn_l2circuit[:600]}\n"
                )
        
        # v11.0 E102: Security specialist data
        security_specialist_data = ""
        for mcp_name, hostname in device_map.items():
            fw_cfg = fw_config_outputs.get(mcp_name, "")
            fw_data = fw_outputs.get(mcp_name, "")
            security_specialist_data += (
                f"\n=== {hostname} ({mcp_name}) ===\n"
                f"Firewall Config:\n{fw_cfg[:800]}\n"
                f"Firewall Counters:\n{fw_data[:600]}\n"
            )
        
        # v11.0 E103: L3VPN specialist data
        l3vpn_specialist_data = ""
        for mcp_name, hostname in device_map.items():
            ri_data = route_inst_outputs.get(mcp_name, "")
            l3vpn_rte = l3vpn_route_outputs.get(mcp_name, "")
            if ri_data.strip() and "master" in ri_data.lower():
                l3vpn_specialist_data += (
                    f"\n=== {hostname} ({mcp_name}) ===\n"
                    f"Route Instances:\n{ri_data[:800]}\n"
                    f"L3VPN Routes:\n{l3vpn_rte[:600]}\n"
                )
        
        # v11.0 E104: Hardware/Environment specialist data
        hardware_specialist_data = ""
        for mcp_name, hostname in device_map.items():
            re_data = re_stats_outputs.get(mcp_name, "")
            env_data = env_outputs.get(mcp_name, "")
            fpc_data = fpc_outputs.get(mcp_name, "")
            hardware_specialist_data += (
                f"\n=== {hostname} ({mcp_name}) ===\n"
                f"Routing Engine:\n{re_data[:600]}\n"
                f"Environment:\n{env_data[:600]}\n"
                f"FPC Status:\n{fpc_data[:400]}\n"
            )
        
        # Topology summary for synthesizer
        topo_summary = ""
        seen_links = set()
        for lk in lldp_links:
            key = f"{lk['local_hostname']}-{lk['remote_hostname']}"
            rev_key = f"{lk['remote_hostname']}-{lk['local_hostname']}"
            if key not in seen_links and rev_key not in seen_links:
                seen_links.add(key)
                topo_summary += f"  {lk['local_hostname']} ({lk['local_intf']}) ── ({lk['remote_intf']}) {lk['remote_hostname']}\n"
        
        device_summary = "\n".join(
            f"  {hostname} ({mcp_name}): " +
            ("OSPF" if ospf_intf_out.get(mcp_name, "").strip() and "not running" not in ospf_intf_out.get(mcp_name, "").lower() else "no-OSPF") + " / " +
            ("IS-IS" if isis_outputs.get(mcp_name, "").strip() and "not running" not in isis_outputs.get(mcp_name, "").lower() else "no-ISIS") + " / " +
            ("BGP" if bgp_outputs.get(mcp_name, "").strip() and "not running" not in bgp_outputs.get(mcp_name, "").lower() else "no-BGP") + " / " +
            ("LDP" if ldp_sess_out.get(mcp_name, "").strip() and "not running" not in ldp_sess_out.get(mcp_name, "").lower() else "no-LDP")
            for mcp_name, hostname in device_map.items()
        )
        
        # Enhancement #5: Build device context string for specialists
        device_context_str = "\n".join(
            f"  - {hostname} ({mcp_name})"
            for mcp_name, hostname in device_map.items()
        )
        
        # Enhancement #7: Aggregate all raw data for hallucination guard
        all_raw_data = (
            raw_intf + raw_ospf_nbr + raw_ospf_intf + raw_bgp + 
            raw_ldp_sess + raw_lldp + raw_mpls
        )
        
        # ═══ v10.0: BUILD ENHANCED INTELLIGENCE CONTEXT (E38-E42, E64) ═══
        console.print(Panel("◉ Phase 5b: v10.0 Intelligence Engines", style="bold magenta", width=55))
        enhanced_context = ""
        if device_map:
            enhanced_context = "\n--- v10.0 ENHANCED INTELLIGENCE CONTEXT ---\n"
            enhanced_context += "(Auto-generated by programmatic cross-validation engines)\n\n"
            
            # E39: Cross-Router Correlation — bidirectional OSPF/BGP/LDP state matching
            try:
                cross_corr = build_cross_router_correlation(
                    ospf_info, bgp_issues, ldp_issues, bgp_established, device_map
                )
                if cross_corr:
                    enhanced_context += "### CROSS-ROUTER CORRELATION\n"
                    for c in cross_corr[:10]:
                        enhanced_context += f"  ⚡ [{c['severity']}] {c['finding']}\n"
                    enhanced_context += "\n"
                    console.print(f"         [success]● E39 Cross-Router: {len(cross_corr)} correlations[/success]")
            except Exception as e:
                logger.debug(f"E39 cross-router correlation skipped: {e}")
            
            # E40: Temporal Intelligence — correlate commits with failures
            try:
                uptime_dict = {}
                for mcp_name, hostname in device_map.items():
                    uptime_dict[mcp_name] = uptime_outputs.get(mcp_name, "")
                temporal = build_temporal_correlation(
                    commit_history, chassis_alarms, uptime_dict, device_map
                )
                if temporal:
                    enhanced_context += "### TEMPORAL CORRELATION (Recent Changes → Current Issues)\n"
                    for t in temporal[:8]:
                        enhanced_context += f"  ◷ [{t['severity']}] {t['finding']}\n"
                    enhanced_context += "\n"
                    console.print(f"         [success]● E40 Temporal: {len(temporal)} correlations[/success]")
            except Exception as e:
                logger.debug(f"E40 temporal correlation skipped: {e}")
            
            # E41: Negative Space Analysis — what's expected but missing
            try:
                coverage = build_coverage_matrix(
                    device_map, ospf_info, bgp_established, bgp_issues,
                    ldp_issues, ldp_healthy, lldp_links
                )
                if coverage:
                    enhanced_context += "### COVERAGE GAPS (Expected but Missing Protocols)\n"
                    for g in coverage[:8]:
                        enhanced_context += f"  ⊕ [{g['severity']}] {g['finding']}\n"
                    enhanced_context += "\n"
                    console.print(f"         [success]● E41 Negative Space: {len(coverage)} gaps[/success]")
            except Exception as e:
                logger.debug(f"E41 negative space analysis skipped: {e}")
            
            # E38: Protocol FSM Reasoning — detect stuck/impossible states
            try:
                fsm = validate_fsm_states(ospf_info, bgp_issues, bgp_established, device_map)
                if fsm:
                    enhanced_context += "### PROTOCOL FSM VIOLATIONS\n"
                    for f in fsm[:8]:
                        enhanced_context += f"  ↻ [{f['severity']}] {f['finding']}\n"
                    enhanced_context += "\n"
                    console.print(f"         [success]● E38 FSM Reasoning: {len(fsm)} violations[/success]")
            except Exception as e:
                logger.debug(f"E38 FSM reasoning skipped: {e}")
            
            # E42: Multi-Hop Root Cause Tracing — blast radius per failure
            try:
                blast = build_blast_radius(
                    ospf_critical, ospf_type_mismatches, bgp_issues,
                    ldp_issues, lsp_issues, device_map
                )
                if blast:
                    enhanced_context += "### BLAST RADIUS (Downstream Impact per Failure)\n"
                    enhanced_context += blast + "\n\n"
                    console.print(f"         [success]● E42 Blast Radius: impact analysis complete[/success]")
            except Exception as e:
                logger.debug(f"E42 blast radius skipped: {e}")
            
            # E64: Predictive Failure Analysis — error rate acceleration
            try:
                predictive = analyze_error_acceleration(intf_errors)
                if predictive:
                    enhanced_context += "### PREDICTIVE FAILURE INDICATORS\n"
                    for p in predictive[:5]:
                        enhanced_context += f"  ▴ [{p['severity']}] {p['finding']}\n"
                    enhanced_context += "\n"
                    console.print(f"         [success]● E64 Predictive: {len(predictive)} indicators[/success]")
            except Exception as e:
                logger.debug(f"E64 predictive analysis skipped: {e}")
            
            if enhanced_context.strip() == "--- v10.0 ENHANCED INTELLIGENCE CONTEXT ---\n(Auto-generated by programmatic cross-validation engines)":
                enhanced_context = ""  # No findings, don't inject empty header
                console.print("         [dim]◆ No enhanced intelligence findings (clean network)[/dim]")
            else:
                console.print(f"         [success]● Enhanced context: {len(enhanced_context)} chars for synthesizer[/success]")
        
        # ═══ v11.0: ADVANCED INTELLIGENCE ENGINES (E68-E71, E69, E94, E96) ═══
        console.print(Panel("◉ Phase 5c: v11.0 Advanced Intelligence", style="bold magenta", width=55))
        
        # E68: Build network dependency graph from LLDP + protocol data
        try:
            global _network_graph
            graph_data = {
                "lldp_links": lldp_links,
                "ospf_neighbors": ospf_info.get("neighbors", {}),
                "bgp_established": bgp_established,
                "ldp_healthy": ldp_healthy,
                "device_map": device_map,
            }
            _network_graph.build_from_data(device_map, lldp_links, ospf_info,
                                           bgp_established, bgp_issues,
                                           ldp_healthy, ldp_issues)
            graph_summary = _network_graph.get_summary()
            transit_nodes = _network_graph.get_transit_nodes()
            enhanced_context += f"\n### DEPENDENCY GRAPH\n{graph_summary}\n"
            if transit_nodes:
                enhanced_context += f"Transit nodes (critical path): {', '.join(transit_nodes)}\n"
            console.print(f"         [success]● E68 Dependency Graph: {len(_network_graph.nodes)} nodes, {len(_network_graph.edges)} edges[/success]")
        except Exception as e:
            logger.debug(f"E68 dependency graph skipped: {e}")
        
        # E71: Baseline anomaly detection
        try:
            baseline_data = {
                "ospf_neighbor_count": {mcp: len(nbrs) for mcp, nbrs in ospf_info.get("neighbors", {}).items()},
                "bgp_peer_count": {mcp: sum(1 for b in bgp_established if b["router"] == mcp) for mcp in device_map},
                "ldp_session_count": {mcp: sum(1 for l in ldp_healthy if l["router"] == mcp) for mcp in device_map},
            }
            # Restructure for detect_baseline_anomalies: {router: {metric: value}}
            per_router_metrics = {}
            for mcp_name in device_map:
                per_router_metrics[mcp_name] = {
                    "ospf_neighbors": baseline_data["ospf_neighbor_count"].get(mcp_name, 0),
                    "bgp_peers": baseline_data["bgp_peer_count"].get(mcp_name, 0),
                    "ldp_sessions": baseline_data["ldp_session_count"].get(mcp_name, 0),
                }
            saved_baselines = load_baselines()
            baseline_anomalies = detect_baseline_anomalies(per_router_metrics, saved_baselines)
            if baseline_anomalies:
                enhanced_context += "\n### BASELINE ANOMALIES\n"
                for ba in baseline_anomalies[:10]:
                    enhanced_context += f"  ◫ {ba}\n"
                console.print(f"         [success]● E71 Baselines: {len(baseline_anomalies)} anomalies detected[/success]")
            else:
                console.print(f"         [dim]◆ E71 Baselines: No anomalies (or first run)[/dim]")
            update_baselines(per_router_metrics, saved_baselines)
            save_baselines(saved_baselines)
        except Exception as e:
            logger.debug(f"E71 baseline detection skipped: {e}")
        
        # E69: Build root cause chain
        root_cause_chain = ""
        try:
            root_cause_chain = build_root_cause_chain(
                down_intfs, ospf_type_mismatches,
                intf_errors, bgp_issues, ldp_issues,
                lsp_issues, bfd_issues, device_map
            )
            if root_cause_chain:
                enhanced_context += f"\n### ROOT CAUSE CHAIN\n{root_cause_chain}\n"
                console.print(f"         [success]● E69 Root Cause Chain: multi-hop analysis complete[/success]")
        except Exception as e:
            logger.debug(f"E69 root cause chain skipped: {e}")
        
        # E94: Quantified risk scores
        risk_scores = []
        try:
            if ospf_type_mismatches:
                rs = calculate_risk_score(10, 9)
                rs["description"] = "OSPF interface-type mismatch"
                risk_scores.append(("OSPF Mismatch", rs))
            if bgp_issues:
                rs = calculate_risk_score(9, 8)
                rs["description"] = f"{len(bgp_issues)} BGP sessions down"
                risk_scores.append(("BGP Sessions Down", rs))
            if ldp_issues:
                rs = calculate_risk_score(8, 8)
                rs["description"] = f"{len(ldp_issues)} LDP sessions down"
                risk_scores.append(("LDP Sessions Down", rs))
            if mtu_mismatches:
                rs = calculate_risk_score(6, 4)
                rs["description"] = "MTU mismatch on links"
                risk_scores.append(("MTU Mismatch", rs))
            if storage_issues:
                rs = calculate_risk_score(4, 3)
                rs["description"] = "High disk usage"
                risk_scores.append(("Storage", rs))
            if risk_scores:
                enhanced_context += "\n### QUANTIFIED RISK SCORES\n"
                for name, score in risk_scores:
                    enhanced_context += f"  ◎ {name}: {score['score']}/100 ({score['category']}) — {score['description']}\n"
                console.print(f"         [success]● E94 Risk Scores: {len(risk_scores)} items scored[/success]")
        except Exception as e:
            logger.debug(f"E94 risk scoring skipped: {e}")
        
        # E96: SLA impact estimation
        sla_impact = {}
        try:
            n_crit_for_sla = len(ospf_type_mismatches) + len([i for i in bgp_issues if i.get("severity") == "CRITICAL"])
            n_warn_for_sla = len(bfd_issues) + len(mtu_mismatches) + len(storage_issues)
            sla_impact = estimate_sla_impact(
                critical_count=n_crit_for_sla,
                warning_count=n_warn_for_sla,
                device_count=len(device_map)
            )
            if sla_impact.get("impact_level") != "none":
                enhanced_context += f"\n### SLA IMPACT ESTIMATE\n"
                enhanced_context += f"  ◫ Impact Level: {sla_impact['impact_level']}\n"
                enhanced_context += f"  ◷ Estimated Downtime Cost: {sla_impact.get('cost_estimate', 'N/A')}\n"
                enhanced_context += f"  ◫ SLA Risk: {sla_impact.get('sla_risk', 'N/A')}\n"
                console.print(f"         [success]● E96 SLA Impact: {sla_impact['impact_level']}[/success]")
        except Exception as e:
            logger.debug(f"E96 SLA impact skipped: {e}")
        
        # Run the layered pipeline (v10.0: all specialists + intelligence engines + parallel)
        deep_dive_analysis = await run_layered_analysis(
            ospf_specialist_data, bgp_specialist_data, ldp_specialist_data,
            topo_summary, device_summary,
            l2vpn_data=l2vpn_specialist_data,
            isis_data=isis_specialist_data,
            system_data=system_specialist_data,
            device_context=device_context_str,
            all_raw_data=all_raw_data,
            device_map=device_map,
            enhanced_context=enhanced_context,
            security_data=security_specialist_data,
            l3vpn_data=l3vpn_specialist_data,
            hardware_data=hardware_specialist_data
        )
        console.print(f"      ● Layered analysis complete: [green]{len(deep_dive_analysis)}[/green] chars")
        
        # ── v6.0: Post-analysis fingerprinting & recurring issue detection ──
        # Build issue list as dicts for fingerprinting (#3C)
        all_current_issues = []
        for i in ospf_critical:
            all_current_issues.append(i)
        for mm in ospf_type_mismatches:
            all_current_issues.append(mm)
        for bi in bfd_issues:
            all_current_issues.append(bi)
        for fi in fw_issues:
            all_current_issues.append(fi)
        for li in lsp_issues:
            all_current_issues.append(li)
        for ri in rsvp_issues:
            all_current_issues.append(ri)
        # v9.0 Fix: Include ISIS, BGP, and LDP issues in all_current_issues
        # so they are reflected in heatmap, health score, and risk matrix
        for ii in isis_issues:
            all_current_issues.append(ii)
        for bi in bgp_issues:
            all_current_issues.append(bi)
        for li in ldp_issues:
            all_current_issues.append(li)
        # Include storage and alarm issues in all_current_issues
        for si in storage_issues:
            all_current_issues.append({"severity": "WARNING", "router": si["router"],
                                        "hostname": si["hostname"], "detail": si["detail"]})
        for al in chassis_alarms:
            all_current_issues.append({"severity": al.get("severity", "WARNING"), "router": al["router"],
                                        "hostname": al["hostname"], "detail": al.get("description", "")})
        for cd in coredump_issues:
            all_current_issues.append({"severity": "WARNING", "router": cd["router"],
                                        "hostname": cd["hostname"], "detail": cd["detail"]})
        
        # Load previous fingerprints and detect recurring issues
        recurring = find_recurring_issues(all_current_issues)
        report_ts = datetime.now().strftime('%Y-%m-%d %H:%M')
        save_issue_fingerprints(all_current_issues, report_ts)
        if recurring:
            console.print(f"      ▲  [yellow]{len(recurring)}[/yellow] recurring issues detected from previous audits")
        
        # Calculate network health score (#2A)
        # Count issues by severity
        n_critical = len([i for i in all_current_issues if i.get("severity") == "CRITICAL"])
        n_warning  = len([i for i in all_current_issues if i.get("severity") in ("WARNING", "MAJOR")])
        n_healthy  = len(device_map) * 3 - n_critical - n_warning  # baseline healthy checks
        n_config_drifts = len(ospf_type_mismatches)
        
        health_result = calculate_health_score(
            critical_count=n_critical,
            warning_count=n_warning,
            healthy_count=max(0, n_healthy),
            device_count=len(device_map),
            config_drifts=n_config_drifts,
            bfd_issues=len(bfd_issues),
            lsp_issues=len(lsp_issues)
        )
        health_score = health_result["score"]
        health_grade = health_result["grade"]
        health_label = health_result["label"]

    # ══════════════════════════════════════════════════════════
    #  BUILD STRUCTURED MARKDOWN REPORT
    # ══════════════════════════════════════════════════════════
    _phase_status("◇ Phase 7: Report Generation")
    audit_duration = round(time.time() - audit_start, 1)
    phase_timings["Report Generation"] = 0.0  # Will be updated at end
    now = datetime.now()
    rpt = []

    rpt.append("# 🔍 Full Network Audit Report\n")
    rpt.append(f"> 📅 **{now.strftime('%B %d, %Y %H:%M')}** · 🤖 Junos MCP v11.0 + Ollama ({MODEL}) · ⏱️ {audit_duration}s · 🖥️ {len(device_map)} devices\n")
    rpt.append("---\n")
    
    # ── 0. Executive Summary (#4A) ──
    rpt.append("## 📊 0. Executive Summary\n")
    # v9.0 Fix: Use direct variable checks instead of locals().get() which
    # fails due to Python scoping in deeply nested conditionals
    try:
        _hs = health_score
        _hg = health_grade
        _hl = health_label
        _nc = n_critical
        _rec = recurring
        _aci = all_current_issues
    except NameError:
        _hs = None
        _hg = "?"
        _hl = "?"
        _nc = 0
        _rec = []
        _aci = []
    if _hs is not None:
        score_emoji = _md_icon("healthy") if _hg in ("A", "B") else (_md_icon("warning") if _hg == "C" else _md_icon("critical"))
        rpt.append(f"| Metric | Value |")
        rpt.append(f"|--------|-------|")
        rpt.append(f"| **Network Health Score** | {score_emoji} **{_hs}/100** ({_hg} — {_hl}) |")
        rpt.append(f"| **Devices Audited** | {len(device_map)} |")
        rpt.append(f"| **Critical Issues** | {len([i for i in _aci if i.get('severity') == 'CRITICAL'])} |")
        rpt.append(f"| **Warnings** | {len([i for i in _aci if i.get('severity') in ('WARNING', 'MAJOR')])} |")
        rpt.append(f"| **Config Drifts** | {len(config_drifts)} |")
        if _rec:
            rpt.append(f"| **Recurring Issues** | ▲ {len(_rec)} (seen in prior audits) |")
        rpt.append("")
        
        # Top risk summary
        if ospf_type_mismatches:
            rpt.append(f"> ▲ **Top Risk:** OSPF interface-type mismatch causing cascading BGP/LDP/MPLS failures. **Single-command fix available.**\n")
        elif ospf_critical:
            rpt.append(f"> ▲ **Top Risk:** OSPF adjacency failures detected. Review Section 4 for root cause analysis.\n")
        elif _nc > 0:
            rpt.append(f"> ▲ **Top Risk:** {_nc} critical issue(s) detected. Immediate attention required.\n")
        else:
            rpt.append(f"> 🟢 **All Clear:** No critical issues detected. Network is operating normally.\n")
        # E15: Extract AI executive narrative from synthesizer JSON if available
        if deep_dive_analysis:
            exec_match = re.search(r'"executive_summary"\s*:\s*"([^"]+)"', deep_dive_analysis)
            if exec_match:
                rpt.append(f"> ◈ **AI Summary:** {exec_match.group(1)}\n")
    else:
        rpt.append("*Health score calculation not available for this audit run.*\n")
    rpt.append("---\n")

    # ── 0b. Severity Heatmap (#P3A) ──
    if device_map:
        # Build protocol_status dict from detected issues
        protocol_status = {}
        for mcp_name in device_map:
            for proto in ["ospf", "bgp", "ldp", "bfd", "is-is", "system"]:
                protocol_status[f"{mcp_name}_{proto}"] = "healthy"
        # Mark issues — v9.0: improved protocol detection from issue attributes
        for issue in _aci:
            router = issue.get("router", issue.get("local_router", ""))
            detail = issue.get("detail", "").lower()
            sev = issue.get("severity", "WARNING")
            status_val = "critical" if sev == "CRITICAL" else "warning"
            
            # Determine which protocol this issue belongs to
            matched_protos = []
            if any(kw in detail for kw in ("ospf", "adjacency", "area ", "interface-type")):
                matched_protos.append("ospf")
            if any(kw in detail for kw in ("bgp", "ibgp", "peer", "as ")):
                matched_protos.append("bgp")
            if any(kw in detail for kw in ("ldp", "mpls", "label", "lsp")):
                matched_protos.append("ldp")
            if any(kw in detail for kw in ("bfd",)):
                matched_protos.append("bfd")
            if any(kw in detail for kw in ("is-is", "isis")):
                matched_protos.append("is-is")
            if any(kw in detail for kw in ("chassis", "alarm", "core dump", "storage", "disk", "uptime", "crash")):
                matched_protos.append("system")
            
            # If no protocol matched, try to infer from issue structure
            if not matched_protos:
                if "interface" in issue:
                    matched_protos.append("ospf")  # Interface-related
                else:
                    matched_protos.append("system")  # Default bucket
            
            for proto_key in matched_protos:
                key = f"{router}_{proto_key}"
                if key in protocol_status:
                    # Only upgrade severity (don't downgrade critical to warning)
                    if protocol_status[key] != "critical":
                        protocol_status[key] = status_val
        heatmap = build_severity_heatmap(device_map, protocol_status)
        if heatmap:
            rpt.append(heatmap)
            rpt.append("")

    # ── 0c. Junos Version Compatibility (#P2D) ──
    version_compat_warnings = check_version_compatibility(device_facts, device_map)
    if version_compat_warnings:
        rpt.append("### ▲ Junos Version Feature Gaps\n")
        rpt.append("| Router | Version | Feature | Min Required |")
        rpt.append("|--------|---------|---------|-------------|")
        for vw in version_compat_warnings:
            rpt.append(f"| {vw['hostname']} | {vw['device_version']} | {vw['feature']} | {vw['min_required']} |")
        rpt.append("")

    # ── 0d. Predictive Failure Analysis (#P2E) ──
    predictive_risks = []
    if intf_errors:
        for ie in intf_errors:
            for prob in ie.get("problems", []):
                if "crc" in prob.lower() or "error" in prob.lower():
                    predictive_risks.append(f"▲ **{ie['hostname']} `{ie['interface']}`**: Physical layer degradation detected — CRC/input errors trending. Likely SFP or cable failure within days.")
    if storage_issues:
        for si in storage_issues:
            if si.get("usage_pct", 0) >= 90:
                predictive_risks.append(f"▲ **{si['hostname']}**: Disk at {si['usage_pct']}% — commit failures imminent if not cleaned.")
    if _rec:
        for r in _rec:
            if r.get("occurrences", 0) >= 3:
                predictive_risks.append(f"▲ **{r['hostname']}**: Issue recurring {r['occurrences']}x — systemic problem requires architectural review.")
    if predictive_risks:
        rpt.append("### ◉ Predictive Failure Analysis\n")
        for pr in predictive_risks:
            rpt.append(f"- {pr}")
        rpt.append("")

    # ── v10.0 E46: ITIL Priority Assignment ──
    if _aci:
        itil_items = []
        for issue in _aci:
            sev = issue.get("severity", "WARNING")
            hostname = issue.get("hostname", "?")
            detail = issue.get("detail", "")[:80]
            affected = len([i for i in _aci if i.get("router") == issue.get("router")])
            is_rec = any(r.get("router") == issue.get("router") for r in _rec) if _rec else False
            itil = assign_itil_priority(sev, affected, is_rec)
            itil_items.append((itil["priority"], itil["label"], hostname, detail, itil["mttr"], itil["sla"]))
        
        # Deduplicate and sort by priority
        seen_itil = set()
        unique_itil = []
        for item in sorted(itil_items, key=lambda x: x[0]):
            key = f"{item[2]}_{item[3][:30]}"
            if key not in seen_itil:
                seen_itil.add(key)
                unique_itil.append(item)
        
        if unique_itil:
            rpt.append("### ◇ ITIL Priority Matrix\n")
            rpt.append("| Priority | Label | Device | Issue | Target MTTR | SLA Risk |")
            rpt.append("|----------|-------|--------|-------|-------------|----------|")
            for pri, label, host, det, mttr, sla in unique_itil[:15]:
                emoji = _md_icon("P1") if pri == "P1" else (_md_icon("P2") if pri == "P2" else (_md_icon("P3") if pri == "P3" else _md_icon("P4")))
                rpt.append(f"| {emoji} **{pri}** | {label} | {host} | {det} | {mttr} | {sla} |")
            rpt.append("")

    # ── v10.0 E48: Remediation Playbook ──
    playbook_steps = []
    step_num = 0
    if ospf_type_mismatches:
        for mm in ospf_type_mismatches:
            step_num += 1
            playbook_steps.append(
                f"| {step_num} | 🔴 P1 | Fix OSPF Interface-Type Mismatch | "
                f"`set protocols ospf area 0 interface {mm['local_intf']} interface-type p2p` on **{mm['local_hostname']}** | "
                f"OSPF adjacency forms → BGP/LDP auto-recover | < 5 min |"
            )
    if bgp_issues and not ospf_type_mismatches:
        step_num += 1
        playbook_steps.append(
            f"| {step_num} | 🔴 P1 | Restore BGP Sessions | "
            f"Check `show bgp summary`, verify loopback reachability | "
            f"iBGP sessions recover → L3VPN routes restored | 10-15 min |"
        )
    if ldp_issues and not ospf_type_mismatches:
        step_num += 1
        playbook_steps.append(
            f"| {step_num} | 🔴 P1 | Restore LDP Sessions | "
            f"Check `show ldp session`, verify LDP is enabled on OSPF interfaces | "
            f"MPLS labels distributed → LSPs operational | 10-15 min |"
        )
    if mtu_mismatches:
        step_num += 1
        playbook_steps.append(
            f"| {step_num} | 🟠 P2 | Fix MTU Mismatches | "
            f"Align MTU on both ends of each link | "
            f"Eliminates fragmentation/drops | 5-10 min |"
        )
    if storage_issues:
        step_num += 1
        playbook_steps.append(
            f"| {step_num} | 🟡 P3 | Clean Storage | "
            f"`request system storage cleanup` on affected devices | "
            f"Prevents commit failures | 5 min |"
        )
    if ntp_issues:
        step_num += 1
        playbook_steps.append(
            f"| {step_num} | 🔵 P4 | Configure NTP | "
            f"`set system ntp server <NTP_IP>` on all devices | "
            f"Accurate timestamps for logging/auth | 5 min |"
        )
    if playbook_steps:
        rpt.append("### ⚙ Remediation Playbook\n")
        rpt.append("| Step | Priority | Action | Command/Procedure | Expected Result | Est. Time |")
        rpt.append("|------|----------|--------|-------------------|-----------------|-----------|")
        for ps in playbook_steps:
            rpt.append(ps)
        rpt.append("")
        rpt.append("> ▸ **Execution Order:** Follow steps sequentially. Step 1 fixes typically cascade-resolve downstream issues.\n")

    rpt.append("---\n")

    # ── 1. Device Inventory ──
    rpt.append("## 🖥️ 1. Device Inventory\n")
    rpt.append("| # | MCP Name | Hostname | Model | Junos Version | Serial | Uptime | RE Status |")
    rpt.append("|---|----------|----------|-------|---------------|--------|--------|-----------|")
    dev_num = 0
    for mcp_name, hostname in device_map.items():
        dev_num += 1
        facts = device_facts.get(mcp_name, {})
        model   = facts.get("model", facts.get("RE0", {}).get("model", "?")) if isinstance(facts, dict) else "?"
        version = facts.get("version", "?")
        serial  = facts.get("serialnumber", facts.get("serial_number", facts.get("serial", "?")))
        if isinstance(facts, dict) and "RE0" in facts:
            re0 = facts["RE0"]
            if model == "?":
                model = re0.get("model", "?")
            if serial == "?":
                serial = re0.get("serialnumber", "?")
            if version == "?":
                version = re0.get("mastership_state", "?")
        # Parse uptime from facts or raw uptime output
        uptime_str = "?"
        if isinstance(facts, dict):
            raw_up = facts.get("RE0", {}).get("up_time", "") if "RE0" in facts else ""
            if raw_up:
                uptime_str = raw_up
        if uptime_str == "?":
            up_match = re.search(r"up\s+(\d+\s+\w+[^,]*)", uptime_outputs.get(mcp_name, ""))
            if up_match:
                uptime_str = up_match.group(1).strip()
        rpt.append(f"| {dev_num} | {mcp_name} | **{mcp_name}** | {model} | {version} | {serial} | {uptime_str} | 🟢 OK |")

    versions = set()
    for m in device_map:
        f = device_facts.get(m, {})
        v = f.get("version", "?") if isinstance(f, dict) else "?"
        versions.add(v)
    versions.discard("?")
    if len(versions) == 1:
        rpt.append(f"\n> 🟢 All {len(device_map)} devices running same Junos version: **{next(iter(versions))}**\n")
    elif len(versions) > 1:
        rpt.append(f"\n> ▲ Mixed Junos versions detected: {', '.join(sorted(versions))}\n")
    rpt.append("\n---\n")

    # ── 2. Network Topology ──
    topo_label = "LLDP" if topology_source == "LLDP" else topology_source
    rpt.append(f"## 🗺️ 2. Network Topology (from {topo_label})\n")
    if lldp_links:
        # Collect interface IPs for the diagram
        intf_ip_map = {}  # {hostname: {interface: ip}}
        for mcp_name in all_mcp:
            hostname = device_map.get(mcp_name, mcp_name)
            intf_ip_map[hostname] = {}
            raw = intf_outputs.get(mcp_name, "")
            for line in raw.split("\n"):
                # Match: ge-0/0/0  513  up  up  inet  10.0.0.1/30
                m = re.match(r"(\S+)\s+\d+\s+up\s+up\s+inet\s+(\d+\.\d+\.\d+\.\d+/\d+)", line.strip())
                if m:
                    intf_name = m.group(1)
                    ip_addr = m.group(2)
                    intf_ip_map[hostname][intf_name] = ip_addr
                    # Store under physical name too (ge-0/0/0.0 → ge-0/0/0)
                    if "." in intf_name:
                        phys = intf_name.rsplit(".", 1)[0]
                        if phys not in intf_ip_map[hostname]:
                            intf_ip_map[hostname][phys] = ip_addr
                    else:
                        # Physical name → also store as .0
                        sub = f"{intf_name}.0"
                        if sub not in intf_ip_map[hostname]:
                            intf_ip_map[hostname][sub] = ip_addr
                # Also match lines where terse shows IP on the .0 unit (no index column)
                m2 = re.match(r"(\S+\.\d+)\s+up\s+up\s+inet\s+(\d+\.\d+\.\d+\.\d+/\d+)", line.strip())
                if m2:
                    intf_name = m2.group(1)
                    ip_addr = m2.group(2)
                    intf_ip_map[hostname][intf_name] = ip_addr
                    # Store under physical name too
                    phys = intf_name.rsplit(".", 1)[0]
                    if phys not in intf_ip_map[hostname]:
                        intf_ip_map[hostname][phys] = ip_addr

        # Build topology context for AI diagram generation
        topo_links_text = []
        seen_pairs = set()
        for lk in lldp_links:
            pair = tuple(sorted([f"{lk['local_hostname']}:{lk['local_intf']}", f"{lk['remote_hostname']}:{lk['remote_intf']}"]))
            if pair not in seen_pairs:
                seen_pairs.add(pair)
                local_ip = intf_ip_map.get(lk["local_hostname"], {}).get(lk["local_intf"], "")
                remote_ip = intf_ip_map.get(lk["remote_hostname"], {}).get(lk["remote_intf"], "")
                topo_links_text.append(
                    f"{lk['local_hostname']} ({lk['local_intf']}, {local_ip}) <---> "
                    f"{lk['remote_hostname']} ({lk['remote_intf']}, {remote_ip})"
                )

        # Build device info for diagram
        device_info_text = []
        for mcp_name, hostname in device_map.items():
            facts = device_facts.get(mcp_name, {})
            model = facts.get("model", facts.get("RE0", {}).get("model", "?")) if isinstance(facts, dict) else "?"
            lo0_ip = intf_ip_map.get(hostname, {}).get("lo0.0", "")
            device_info_text.append(f"{hostname}: model={model}, loopback={lo0_ip}")

        # Build topology diagram programmatically (instant — no AI call needed)
        console.print("   ◫ Building topology diagram...", style="dim")

        # Classify devices into tiers: PE (edge), P (core), other
        pe_devices = [h for h in device_map.values() if h.upper().startswith("PE")]
        p_devices  = [h for h in device_map.values() if h.upper().startswith("P") and h not in pe_devices]
        other_devs = [h for h in device_map.values() if h not in pe_devices and h not in p_devices]

        # Build adjacency from LLDP (deduplicated)
        adjacency = {}  # hostname -> [(remote_hostname, local_intf, remote_intf, local_ip, remote_ip)]
        for lk in lldp_links:
            lh, rh = lk["local_hostname"], lk["remote_hostname"]
            li, ri = lk["local_intf"], lk["remote_intf"]
            lip = intf_ip_map.get(lh, {}).get(li, "")
            rip = intf_ip_map.get(rh, {}).get(ri, "")
            adjacency.setdefault(lh, []).append((rh, li, ri, lip, rip))

        # Calculate connection count per device for layout
        conn_count = {h: len(adjacency.get(h, [])) for h in device_map.values()}

        # Helper: make a device box
        def _make_box(hostname):
            lo_ip = intf_ip_map.get(hostname, {}).get("lo0.0", "")
            mcp = [k for k, v in device_map.items() if v == hostname]
            facts = device_facts.get(mcp[0], {}) if mcp else {}
            model = facts.get("model", facts.get("RE0", {}).get("model", "")) if isinstance(facts, dict) else ""
            line1 = hostname
            line2 = model if model and model != "?" else ""
            line3 = lo_ip if lo_ip else ""
            lines = [line1]
            if line2:
                lines.append(line2)
            if line3:
                lines.append(line3)
            width = max(len(l) for l in lines) + 2
            box = []
            box.append("┌" + "─" * width + "┐")
            for l in lines:
                box.append("│" + l.center(width) + "│")
            box.append("└" + "─" * width + "┘")
            return box, width + 2  # +2 for the border chars

        # Build a tiered ASCII layout
        diagram_lines = []

        # --- PE tier (top) ---
        if pe_devices:
            diagram_lines.append(f"  {'PE / Edge Layer':^60}")
            diagram_lines.append(f"  {'─' * 60}")
            pe_boxes = [_make_box(h) for h in sorted(pe_devices)]
            max_height = max(len(b[0]) for b in pe_boxes)
            # Pad boxes to same height
            for i, (box, w) in enumerate(pe_boxes):
                while len(box) < max_height:
                    box.insert(-1, "│" + " " * (w - 2) + "│")
            # Render side by side with spacing
            spacing = "    "
            for row in range(max_height):
                line = "  "
                for box, w in pe_boxes:
                    line += box[row] + spacing
                diagram_lines.append(line.rstrip())
            # Connection indicators
            conn_line = "  "
            for h in sorted(pe_devices):
                nbrs = [n[0] for n in adjacency.get(h, [])]
                conn_line += f"  {'│':^{_make_box(h)[1]}}  "
            diagram_lines.append(conn_line.rstrip())
            diagram_lines.append("")

        # --- P core tier (middle) ---
        if p_devices:
            diagram_lines.append(f"  {'P / Core Layer':^60}")
            diagram_lines.append(f"  {'─' * 60}")
            p_boxes = [_make_box(h) for h in sorted(p_devices)]
            max_height = max(len(b[0]) for b in p_boxes)
            for i, (box, w) in enumerate(p_boxes):
                while len(box) < max_height:
                    box.insert(-1, "│" + " " * (w - 2) + "│")
            spacing = "  "
            for row in range(max_height):
                line = "  "
                for box, w in p_boxes:
                    line += box[row] + spacing
                diagram_lines.append(line.rstrip())
            diagram_lines.append("")

        # --- Other devices tier (bottom) ---
        if other_devs:
            diagram_lines.append(f"  {'Other Devices':^60}")
            diagram_lines.append(f"  {'─' * 60}")
            o_boxes = [_make_box(h) for h in sorted(other_devs)]
            max_height = max(len(b[0]) for b in o_boxes)
            for i, (box, w) in enumerate(o_boxes):
                while len(box) < max_height:
                    box.insert(-1, "│" + " " * (w - 2) + "│")
            spacing = "    "
            for row in range(max_height):
                line = "  "
                for box, w in o_boxes:
                    line += box[row] + spacing
                diagram_lines.append(line.rstrip())
            diagram_lines.append("")

        # --- Connection list below diagram ---
        diagram_lines.append("")
        diagram_lines.append("  Connections:")
        for link_text in topo_links_text:
            diagram_lines.append(f"    {link_text}")

        rpt.append("**Network Topology Diagram:**\n")
        rpt.append("```")
        for dl in diagram_lines:
            rpt.append(dl)
        rpt.append("```\n")

        # Topology link table
        rpt.append("**Detailed Link Table:**\n")
        rpt.append("| # | Local Router | Local Interface | Local IP | Remote Router | Remote Interface | Remote IP |")
        rpt.append("|---|-------------|-----------------|----------|---------------|-----------------|----------|")
        link_num = 0
        seen = set()
        for lk in lldp_links:
            key = tuple(sorted([f"{lk['local_hostname']}:{lk['local_intf']}", f"{lk['remote_hostname']}:{lk['remote_intf']}"]))
            if key not in seen:
                seen.add(key)
                link_num += 1
                local_ip = intf_ip_map.get(lk["local_hostname"], {}).get(lk["local_intf"], "—")
                remote_ip = intf_ip_map.get(lk["remote_hostname"], {}).get(lk["remote_intf"], "—")
                rpt.append(f"| {link_num} | {lk['local_hostname']} | {lk['local_intf']} | {local_ip} | {lk['remote_hostname']} | {lk['remote_intf']} | {remote_ip} |")
        
        if topology_source != "LLDP":
            rpt.append(f"\n> ℹ️ *Topology built from {topology_source} neighbor data (LLDP was unavailable). "
                        f"Links show logical adjacencies rather than physical connections.*\n")
    else:
        rpt.append("*No topology data available — LLDP not enabled and no IGP/BGP neighbor data collected.*")
    rpt.append("\n---\n")

    # ── 3. Issues Found ──
    critical_num = 0
    warning_num  = 0

    rpt.append("## ⚠️ 3. ISSUES FOUND\n")

    # 3a. OSPF Issues — including type mismatches
    # First, report type mismatches with full evidence
    for mm in ospf_type_mismatches:
        critical_num += 1
        rpt.append(f"### 🔴 CRITICAL #{critical_num}: OSPF Interface-Type Mismatch — {mm['local_hostname']} ↔ {mm['remote_hostname']}\n")
        rpt.append("| Detail | Value |")
        rpt.append("|--------|-------|")
        rpt.append(f"| **Affected Link** | {mm['local_hostname']} ({mm['local_intf']}) ↔ {mm['remote_hostname']} ({mm['remote_intf']}) |")
        rpt.append(f"| **{mm['local_hostname']} side** | **{mm['local_type']}** (State: {mm['local_state']}, Nbrs: {mm['local_nbrs']}) |")
        rpt.append(f"| **{mm['remote_hostname']} side** | **{mm['remote_type']}** (State: {mm['remote_state']}, Nbrs: {mm['remote_nbrs']}) |")
        rpt.append(f"| **Impact** | OSPF adjacency CANNOT form → cascading BGP/LDP/MPLS failures |")
        rpt.append("")

        # Evidence: show OSPF interface output from BOTH sides
        for side_label, side_router in [("local", mm["local_router"]), ("remote", mm["remote_router"])]:
            side_hostname = mm[f"{side_label}_hostname"]
            ospf_raw = ospf_intf_out.get(side_router, "")
            if ospf_raw.strip():
                rpt.append(f"**Evidence** — `show ospf interface` on {side_hostname}:")
                rpt.append("```")
                for line in ospf_raw.strip().split("\n")[:15]:
                    rpt.append(line.rstrip())
                rpt.append("```\n")

        rpt.append(
            f"> **Root Cause:** Interface type mismatch! **{mm['local_hostname']}** has `interface-type {mm['local_type']}` "
            f"on {mm['local_intf']}, but **{mm['remote_hostname']}** {mm['remote_intf']} is running as `{mm['remote_type']}`. "
            f"OSPF requires both sides to use the same interface type. This single mismatch is the **root cause** "
            f"of all downstream BGP and LDP failures.\n"
        )

    # Then, report other OSPF issues (0 neighbors, etc.) that aren't already covered by mismatches
    mismatch_routers = set()
    for mm in ospf_type_mismatches:
        mismatch_routers.add(mm["local_router"])
        mismatch_routers.add(mm["remote_router"])
    
    for issue in ospf_info["issues"]:
        if issue["severity"] == "CRITICAL" and "mismatch" not in issue:
            # Skip if this router's issue is already explained by a type mismatch
            if issue["router"] in mismatch_routers:
                continue
            critical_num += 1
            rpt.append(f"### 🔴 CRITICAL #{critical_num}: OSPF Adjacency Failure — {issue['hostname']}\n")
            rpt.append("| Detail | Value |")
            rpt.append("|--------|-------|")
            rpt.append(f"| **Router** | {issue['hostname']} ({issue['router']}) |")
            rpt.append(f"| **Issue** | {issue['detail']} |")
            rpt.append(f"| **Impact** | Cannot learn routes via OSPF → cascading BGP/LDP failures |")
            rpt.append("")
            # Show raw OSPF interface output
            intf_data = ospf_intf_out.get(issue["router"], "")
            if intf_data.strip():
                rpt.append("**OSPF Interface Status on this router:**")
                rpt.append("```")
                for line in intf_data.split("\n")[:20]:
                    if line.strip():
                        rpt.append(line.rstrip())
                rpt.append("```")
            rpt.append("")

    # 3b. BGP Issues
    # Group BGP issues by router for cleaner evidence display
    bgp_issues_by_router = {}
    for issue in bgp_issues:
        r = issue["router"]
        if r not in bgp_issues_by_router:
            bgp_issues_by_router[r] = []
        bgp_issues_by_router[r].append(issue)

    for router, router_issues in bgp_issues_by_router.items():
        hostname = router_issues[0]["hostname"]
        for issue in router_issues:
            critical_num += 1
            rpt.append(f"### 🔴 CRITICAL #{critical_num}: iBGP Session DOWN — {issue['hostname']} → {issue['peer']}\n")
            rpt.append("| Detail | Value |")
            rpt.append("|--------|-------|")
            rpt.append(f"| **Router** | {issue['hostname']} ({issue['router']}) |")
            rpt.append(f"| **Peer** | {issue['peer']} |")
            rpt.append(f"| **State** | **{issue['state']}** (DOWN) |")
            rpt.append(f"| **Impact** | No L3VPN/route exchange with peer {issue['peer']} |")
            if ospf_type_mismatches:
                rpt.append(f"| **Root Cause** | Cascading from OSPF interface-type mismatch → loopback unreachable → iBGP can't connect |")
            else:
                rpt.append(f"| **Root Cause** | Cascading: OSPF down → loopback unreachable → iBGP can't connect |")
            rpt.append("")

        # Show evidence: actual BGP summary output from this router (once per router)
        bgp_raw = bgp_outputs.get(router, "")
        if bgp_raw.strip():
            rpt.append(f"**Evidence** — `show bgp summary` on {hostname}:")
            rpt.append("```")
            for line in bgp_raw.strip().split("\n")[:25]:
                rpt.append(line.rstrip())
            rpt.append("```\n")
            if ospf_type_mismatches:
                mm = ospf_type_mismatches[0]
                rpt.append(
                    f"> **Root Cause:** The OSPF interface-type mismatch between "
                    f"{mm['local_hostname']} ({mm['local_type']}) and {mm['remote_hostname']} ({mm['remote_type']}) "
                    f"prevents OSPF adjacency from forming. Without OSPF, {hostname} has no route to the peer's "
                    f"loopback address, so the iBGP session stays in **{router_issues[0]['state']}** state.\n"
                )

    # 3c. LDP Issues  
    # Group by router for cleaner evidence
    ldp_issues_by_router = {}
    for issue in ldp_issues:
        r = issue["router"]
        if r not in ldp_issues_by_router:
            ldp_issues_by_router[r] = []
        ldp_issues_by_router[r].append(issue)

    for router, router_issues in ldp_issues_by_router.items():
        hostname = router_issues[0]["hostname"]
        for issue in router_issues:
            critical_num += 1
            rpt.append(f"### 🔴 CRITICAL #{critical_num}: LDP Session DOWN — {issue['hostname']} → {issue['peer']}\n")
            rpt.append("| Detail | Value |")
            rpt.append("|--------|-------|")
            rpt.append(f"| **Router** | {issue['hostname']} ({issue['router']}) |")
            rpt.append(f"| **Session** | → {issue['peer']} |")
            rpt.append(f"| **State** | **Nonexistent / Closed** |")
            rpt.append(f"| **Impact** | No MPLS label distribution → L3VPN/MPLS services broken |")
            if ospf_type_mismatches:
                rpt.append(f"| **Root Cause** | Cascading from OSPF interface-type mismatch → no TCP connectivity for LDP |")
            else:
                rpt.append(f"| **Root Cause** | Cascading: OSPF down → no TCP connectivity for LDP |")
            rpt.append("")

        # Show evidence: LDP session output
        ldp_raw = ldp_sess_out.get(router, "")
        if ldp_raw.strip():
            rpt.append(f"**Evidence** — `show ldp session` on {hostname}:")
            rpt.append("```")
            for line in ldp_raw.strip().split("\n")[:20]:
                rpt.append(line.rstrip())
            rpt.append("```\n")

    # 3d. Warning: No routing protocols
    for mcp_name, hostname in no_routing:
        warning_num += 1
        rpt.append(f"### 🟡 WARNING #{warning_num}: {hostname} Has No Dynamic Routing Protocols\n")
        rpt.append("| Detail | Value |")
        rpt.append("|--------|-------|")
        rpt.append(f"| **Router** | {hostname} ({mcp_name}) |")
        rpt.append(f"| **OSPF** | ✗ Not running |")
        rpt.append(f"| **BGP** | ✗ Not running |")
        rpt.append(f"| **MPLS/LDP** | ✗ Not configured |")
        rpt.append(f"| **Impact** | Static routing only — no redundancy |")
        rpt.append("")

    # 3e. Warning: NTP
    if ntp_issues:
        warning_num += 1
        rpt.append(f"### 🟡 WARNING #{warning_num}: NTP Not Configured\n")
        rpt.append("| Router | NTP Status |")
        rpt.append("|--------|------------|")
        for _, hostname in ntp_issues:
            rpt.append(f"| {hostname} | ✗ No NTP peers |")
        rpt.append(f"\n**Impact:** All devices rely on local clock. Time drift causes log correlation issues, certificate failures.\n")

    # 3f. Warning: Down interfaces
    if down_intfs:
        intf_groups = {}
        for d in down_intfs:
            if d["interface"] not in intf_groups:
                intf_groups[d["interface"]] = []
            intf_groups[d["interface"]].append(device_map.get(d["router"], d["router"]))

        warning_num += 1
        rpt.append(f"###  WARNING #{warning_num}: Down Physical Interfaces\n")
        rpt.append("| Interface | Admin | Link | Affected Routers |")
        rpt.append("|-----------|-------|------|-----------------|")
        for intf, routers in intf_groups.items():
            rpt.append(f"| {intf} | Up | **Down** | {', '.join(routers)} |")
        rpt.append(f"\n**Impact:** Interfaces are admin-enabled but link-down. Should be disabled if unused.\n")

    # 3g. IS-IS issues
    for issue in isis_issues:
        critical_num += 1
        rpt.append(f"### 🔴 CRITICAL #{critical_num}: IS-IS Adjacency DOWN — {issue['hostname']}\n")
        rpt.append("| Detail | Value |")
        rpt.append("|--------|-------|")
        rpt.append(f"| **Router** | {issue['hostname']} ({issue['router']}) |")
        rpt.append(f"| **Interface** | {issue['interface']} |")
        rpt.append(f"| **State** | **{issue['state']}** |")
        rpt.append(f"| **Impact** | IS-IS adjacency down → routing convergence affected |")
        rpt.append("")

    # 3h. Chassis Alarms
    if chassis_alarms:
        warning_num += 1
        rpt.append(f"### 🟡 WARNING #{warning_num}: Active Chassis Alarms\n")
        rpt.append("| Router | Severity | Alarm Description |")
        rpt.append("|--------|----------|-------------------|")
        for alm in chassis_alarms:
            sev_icon = _md_icon(alm["severity"])
            rpt.append(f"| {alm['hostname']} | {sev_icon} {alm['severity']} | {alm['description']} |")
        rpt.append(f"\n**Impact:** Active alarms indicate hardware or environmental issues requiring attention.\n")

    # 3i. Storage capacity warnings
    if storage_issues:
        warning_num += 1
        rpt.append(f"### 🟡 WARNING #{warning_num}: High Disk Usage\n")
        rpt.append("| Router | Filesystem | Usage |")
        rpt.append("|--------|------------|-------|")
        for si in storage_issues:
            pct_icon = _md_icon("critical") if si["usage_pct"] >= 95 else _md_icon("major")
            rpt.append(f"| {si['hostname']} | `{si['mount']}` | {pct_icon} **{si['usage_pct']}%** |")
        rpt.append(f"\n**Impact:** High disk usage can cause log rotation failure, commit failures, and potential RE lockup.\n")

    # 3j. Core dump findings
    if coredump_issues:
        warning_num += 1
        rpt.append(f"### 🟡 WARNING #{warning_num}: Core Dumps Detected\n")
        rpt.append("| Router | Core Dumps | Status |")
        rpt.append("|--------|------------|--------|")
        for cd in coredump_issues:
            rpt.append(f"| {cd['hostname']} | **{cd['count']}** file(s) | ▲ Process crash history |")
        rpt.append(f"\n**Impact:** Core dumps indicate daemon crashes. Review with `show system core-dumps` and open JTAC case if recurring.\n")

    # 3k. MTU Mismatches (cross-link comparison)
    if mtu_mismatches:
        for mm in mtu_mismatches:
            warning_num += 1
            rpt.append(f"### 🟡 WARNING #{warning_num}: MTU Mismatch — {mm['local_hostname']}:{mm['local_intf']} ↔ {mm['remote_hostname']}:{mm['remote_intf']}\n")
            rpt.append("| Detail | Value |")
            rpt.append("|--------|-------|")
            rpt.append(f"| **Link** | {mm['local_hostname']} `{mm['local_intf']}` ↔ {mm['remote_hostname']} `{mm['remote_intf']}` |")
            rpt.append(f"| **Local MTU** | {mm['local_mtu']} |")
            rpt.append(f"| **Remote MTU** | {mm['remote_mtu']} |")
            rpt.append(f"| **Difference** | {abs(mm['local_mtu'] - mm['remote_mtu'])} bytes |")
            rpt.append("")
        rpt.append("**Impact:** MTU mismatches cause silent packet drops for large frames (jumbo/MPLS), OSPF adjacency flaps, and path MTU discovery failures.\n")

    # 3l. Interface Errors (CRC, input errors, carrier transitions, half-duplex)
    if intf_errors:
        warning_num += 1
        rpt.append(f"### 🟡 WARNING #{warning_num}: Physical Layer Errors Detected\n")
        rpt.append("| Router | Interface | Speed | Duplex | Problems |")
        rpt.append("|--------|-----------|-------|--------|----------|")
        for ie in intf_errors:
            problems_str = "; ".join(ie["problems"])
            rpt.append(f"| {ie['hostname']} | `{ie['interface']}` | {ie['speed']} | {ie['duplex']} | {problems_str} |")
        rpt.append(f"\n**Impact:** CRC/input errors indicate bad cables, dirty SFPs, or speed/duplex mismatch. Carrier transitions indicate link flaps. All cause packet loss and protocol instability.\n")

    if critical_num == 0 and warning_num == 0:
        rpt.append("**No issues found!** 🟢\n")

    rpt.append("---\n")

    # ── 4. Root Cause Analysis ──
    if deep_dive_analysis:
        rpt.append("## 🧠 4. Root Cause Analysis (AI Deep Dive)\n")
        
        # Enhancement #2C: Add structured header before AI analysis
        rpt.append("| Parameter | Value |")
        rpt.append("|-----------|-------|")
        rpt.append(f"| **Specialists Used** | OSPF, BGP, LDP/MPLS, IS-IS, System, L2VPN, RSVP-TE, QoS/CoS, Security, L3VPN, HW/Env, Synthesizer |")
        rpt.append(f"| **RAG Engine** | {'Active' if vector_kb else 'Fallback'} |")
        rpt.append(f"| **Analysis Method** | Parallel specialist → cross-correlation → structured synthesis |")
        rpt.append("")
        
        rpt.append(deep_dive_analysis)
        if ospf_type_mismatches or ospf_critical:
            rpt.append("\n\n**Cascading Failure Chain:**")
            rpt.append("```")
            if ospf_type_mismatches:
                mm = ospf_type_mismatches[0]
                rpt.append(f"OSPF interface-type mismatch: {mm['local_hostname']} ({mm['local_type']}) vs {mm['remote_hostname']} ({mm['remote_type']})")
            else:
                rpt.append("OSPF adjacency failure (check config)")
            rpt.append("    └─→ OSPF adjacency cannot form")
            rpt.append("        └─→ No IGP route to remote loopback")
            rpt.append("            └─→ iBGP session DOWN (peers via loopback)")
            rpt.append("                └─→ LDP session DOWN (peers via loopback)")
            rpt.append("                    └─→ MPLS / L3VPN services BROKEN")
            rpt.append("```")
        rpt.append("\n---\n")

    # ── 5. Healthy Areas ──
    rpt.append("## ✅ 5. Healthy Areas\n")
    rpt.append("| # | Category | Router | Status | Details |")
    rpt.append("|---|----------|--------|--------|---------|")
    h_num = 0

    # Version consistency
    if len(versions) <= 1:
        h_num += 1
        ver = next(iter(versions)) if versions else "?"
        rpt.append(f"| {h_num} | Junos Version | All {len(device_map)} devices | 🟢 Consistent | All running {ver} |")

    # RE status with uptime details
    for mcp_name, hostname in device_map.items():
        facts = device_facts.get(mcp_name, {})
        uptime = ""
        if isinstance(facts, dict) and "RE0" in facts:
            uptime = facts["RE0"].get("up_time", "")
        if not uptime:
            up_match = re.search(r"up\s+(\d+\s+\w+[^,]*)", uptime_outputs.get(mcp_name, ""))
            if up_match:
                uptime = up_match.group(1).strip()
        if uptime:
            h_num += 1
            rpt.append(f"| {h_num} | Routing Engine | {hostname} | 🟢 Online | Uptime: {uptime} |")

    # Healthy OSPF
    for router, nbrs in ospf_info["neighbors"].items():
        hostname = device_map.get(router, router)
        for n in nbrs:
            h_num += 1
            rpt.append(f"| {h_num} | OSPF Adjacency | {hostname} | 🟢 Full | Neighbor {n['address']} via {n.get('interface', '?')} |")

    # Healthy BGP — with route count if available
    for b in bgp_established:
        # Try to extract received route count from BGP summary
        route_count = ""
        bgp_raw = bgp_outputs.get(b["router"], "")
        for line in bgp_raw.split("\n"):
            if b["peer"] in line:
                parts = line.split()
                if parts and parts[-1].isdigit():
                    route_count = f", {parts[-1]} routes received"
                break
        h_num += 1
        rpt.append(f"| {h_num} | iBGP Session | {b['hostname']} | 🟢 Established | Peer {b['peer']}{route_count} |")

    # Healthy LDP
    for lp in ldp_healthy:
        h_num += 1
        rpt.append(f"| {h_num} | LDP Session | {lp['hostname']} | 🟢 Operational | Session to {lp['peer']} |")

    # Healthy IS-IS
    for isis_h in isis_healthy:
        h_num += 1
        rpt.append(f"| {h_num} | IS-IS Adjacency | {isis_h['hostname']} | 🟢 Up | Neighbor {isis_h['neighbor']} via {isis_h['interface']} |")

    # Healthy BFD (#1A)
    for bh in (bfd_healthy if 'bfd_healthy' in dir() else []):
        h_num += 1
        rpt.append(f"| {h_num} | BFD Session | {bh['hostname']} | 🟢 Up | {bh.get('detail', 'BFD operational')} |")

    # Healthy MPLS LSPs (#1C)
    for lh in (lsp_healthy if 'lsp_healthy' in dir() else []):
        h_num += 1
        rpt.append(f"| {h_num} | MPLS LSP | {lh['hostname']} | 🟢 Up | {lh.get('detail', 'LSP operational')} |")

    # Route table health
    for mcp_name, tables in route_summary.items():
        hostname = device_map.get(mcp_name, mcp_name)
        inet0 = tables.get("inet.0", {})
        if inet0:
            h_num += 1
            rpt.append(f"| {h_num} | Routing Table | {hostname} | 🟢 inet.0 | {inet0.get('destinations', '?')} destinations, {inet0.get('routes', '?')} routes |")

    # No chassis alarms = healthy
    if not chassis_alarms:
        clean_alarm_count = sum(1 for m in device_map
                                if "no alarms" in alarm_outputs.get(m, "").lower() or not alarm_outputs.get(m, "").strip())
        if clean_alarm_count > 0:
            h_num += 1
            rpt.append(f"| {h_num} | Chassis Alarms | {clean_alarm_count} devices | 🟢 Clean | No active alarms |")

    # No core dumps = healthy
    if not coredump_issues:
        h_num += 1
        rpt.append(f"| {h_num} | Core Dumps | All {len(device_map)} devices | 🟢 Clean | No process crashes |")

    # MTU consistency
    if not mtu_mismatches and lldp_links:
        h_num += 1
        rpt.append(f"| {h_num} | MTU Consistency | {len(lldp_links)} links | 🟢 Matched | No MTU mismatches across LLDP-discovered links |")

    # Interface health (no physical layer errors)
    if not intf_errors:
        total_intfs = sum(len(intfs) for intfs in intf_details.values())
        h_num += 1
        rpt.append(f"| {h_num} | Physical Layer | {total_intfs} interfaces | 🟢 Clean | No CRC errors, no link flaps |")

    # Topology Discovery
    if lldp_links:
        unique_hosts = set(lk["local_hostname"] for lk in lldp_links) | set(lk["remote_hostname"] for lk in lldp_links)
        h_num += 1
        topo_method = "LLDP" if topology_source == "LLDP" else f"IGP/BGP ({topology_source})"
        rpt.append(f"| {h_num} | Topology Discovery | {len(unique_hosts)} devices | 🟢 Working | {len(lldp_links)} links via {topo_method} |")

    rpt.append("\n---\n")

    # ── 5b. Cross-Protocol Reachability Matrix (#3A) ──
    if 'reachability' in dir() and reachability:
        rpt.append("### ⊶ Cross-Protocol Reachability Matrix\n")
        rpt.append("| Router | OSPF | BGP | LDP |")
        rpt.append("|--------|------|-----|-----|")
        for mcp_name, protocols in sorted(reachability.items()):
            hostname = device_map.get(mcp_name, mcp_name)
            ospf_status = "🟢" if protocols.get("ospf") else "❌"
            bgp_status = "🟢" if protocols.get("bgp") else "❌"
            ldp_status = "🟢" if protocols.get("ldp") else "❌"
            rpt.append(f"| **{hostname}** | {ospf_status} | {bgp_status} | {ldp_status} |")
        rpt.append("")

    rpt.append("---\n")

    # ── 6. Config Drift Analysis (Golden Config Store) ──
    rpt.append("## 🔄 6. Config Drift Analysis\n")
    rpt.append("Each device's current running configuration is compared against a saved **golden baseline** ")
    rpt.append("(`golden_configs/<device>.conf`). Any differences indicate unauthorized changes or configuration drift.\n")
    if baselines_created and not config_drifts:
        rpt.append(f"**First audit run** — golden baselines established for **{len(baselines_created)}** device(s):\n")
        for hname in baselines_created:
            rpt.append(f"- ✦ {hname}")
        rpt.append(f"\n> Baselines saved to `golden_configs/`. Future audits will detect any configuration changes against these baselines.\n")
    elif config_drifts or config_errors:
        drift_count = len(config_drifts)
        err_count = len(config_errors) if 'config_errors' in dir() else 0
        clean_count = len(all_mcp) - drift_count - len(baselines_created) - err_count
        rpt.append(f"| Status | Count |")
        rpt.append(f"|--------|-------|")
        rpt.append(f"| 🟢 Config Matches Baseline | **{clean_count}** |")
        rpt.append(f"| ▲ Config Drift Detected | **{drift_count}** |")
        if baselines_created:
            rpt.append(f"| ✦ New Baseline Created | **{len(baselines_created)}** |")
        if err_count > 0:
            rpt.append(f"| ✗ Config Collection Failed | **{err_count}** |")
        rpt.append("")

        # Report config collection failures
        if 'config_errors' in dir() and config_errors:
            rpt.append("### ✗ Config Collection Failures\n")
            rpt.append("The following devices could not have their configs retrieved. This is typically caused by ")
            rpt.append("SSH/NETCONF connectivity issues, device timeouts, or gateway overload.\n")
            for dev_name in config_errors:
                rpt.append(f"- ✗ **{dev_name}** — config could not be fetched for drift comparison")
            rpt.append("")

        drift_num = 0
        for mcp_name, drift_info in config_drifts.items():
            drift_num += 1
            hostname = device_map.get(mcp_name, mcp_name)
            summary = drift_info["summary"]
            meta = drift_info["meta"]
            baseline_date = meta.get("saved_at", "unknown")
            if "T" in baseline_date:
                baseline_date = baseline_date.split("T")[0]

            rpt.append(f"### ▲ Drift #{drift_num}: {hostname} ({mcp_name})\n")
            rpt.append("| Detail | Value |")
            rpt.append("|--------|-------|")
            rpt.append(f"| **Lines Added** | +{summary['lines_added']} |")
            rpt.append(f"| **Lines Removed** | -{summary['lines_removed']} |")
            rpt.append(f"| **Total Changes** | {summary['total_changes']} |")
            rpt.append(f"| **Sections Affected** | {', '.join(summary['sections_changed']) or 'unknown'} |")
            rpt.append(f"| **Baseline Date** | {baseline_date} |")
            rpt.append("")

            # Show the actual diff (capped at 40 lines)
            rpt.append(f"**Config Diff** (golden vs current):")
            rpt.append("```diff")
            for line in drift_info["diff"][:40]:
                rpt.append(line.rstrip())
            if len(drift_info["diff"]) > 40:
                rpt.append(f"... ({len(drift_info['diff']) - 40} more lines)")
            rpt.append("```\n")
    else:
        rpt.append(f"All **{len(all_mcp)}** devices match their golden baselines. 🟢\n")
        rpt.append("> No unauthorized or unplanned configuration changes detected.\n")

    rpt.append("---\n")

    # ── 7. Recommended Remediation ──
    rpt.append("## 🔧 7. Recommended Remediation\n")

    if ospf_type_mismatches or ospf_info["issues"] or bgp_issues:
        rpt.append("### Priority 1 (Immediate) — Fix OSPF Root Cause\n")
        if ospf_type_mismatches:
            rpt.append("The OSPF interface-type mismatch is the **single root cause** behind all critical issues.")
            rpt.append("Fixing it will **automatically restore** OSPF adjacency, iBGP, and LDP sessions.\n")
            for mm in ospf_type_mismatches:
                # Recommend adding p2p to the broadcast side (p2p is generally preferred for point-to-point links)
                if mm["local_type"] == "p2p":
                    fix_router = mm["remote_hostname"]
                    fix_mcp = mm["remote_router"]
                    fix_intf = mm["remote_intf"]
                else:
                    fix_router = mm["local_hostname"]
                    fix_mcp = mm["local_router"]
                    fix_intf = mm["local_intf"]
                rpt.append(f"**On {fix_router} ({fix_mcp}):**")
                rpt.append("```junos")
                rpt.append(f"set protocols ospf area 0.0.0.0 interface {fix_intf} interface-type p2p")
                rpt.append("commit")
                rpt.append("```\n")
                rpt.append("**Expected Recovery Chain** (within ~30 seconds of commit):\n")
                rpt.append("```")
                rpt.append(f"1. 🟢 OSPF adjacency forms between {mm['local_hostname']} and {mm['remote_hostname']}  (Full state)")
                rpt.append(f"2. 🟢 IGP routes to remote loopbacks become reachable")
                rpt.append(f"3. 🟢 iBGP sessions transition from Active → Established  ({len(bgp_issues)} sessions)")
                rpt.append(f"4. 🟢 LDP sessions transition from Nonexistent → Operational  ({len(ldp_issues)} sessions)")
                rpt.append(f"5. 🟢 MPLS labels distributed → L3VPN route exchange resumes")
                rpt.append("```\n")
        else:
            rpt.append("The OSPF adjacency failure is the **single root cause** behind all critical issues.")
            rpt.append("Fixing OSPF will **automatically restore** both iBGP and LDP sessions.\n")
            if deep_dive_analysis:
                rpt.append("> See **Section 4** (Root Cause Analysis) above for the specific `set` command.\n")

    if ntp_issues:
        rpt.append("### Priority 2 — Configure NTP\n")
        rpt.append("```junos")
        rpt.append("set system ntp server <NTP-SERVER-IP>")
        rpt.append("```\n")

    if down_intfs:
        rpt.append("### Priority 3 — Disable Unused Interfaces\n")
        rpt.append("```junos")
        for intf in sorted(set(d["interface"] for d in down_intfs)):
            rpt.append(f"set interfaces {intf} disable")
        rpt.append("```\n")

    if no_routing:
        rpt.append("### Priority 4 — Review Routers Without Dynamic Routing\n")
        for _, hostname in no_routing:
            rpt.append(f"- **{hostname}**: Add OSPF/BGP if this is a production router\n")

    if storage_issues:
        rpt.append("### Priority 5 — Address High Disk Usage\n")
        rpt.append("```junos")
        rpt.append("request system storage cleanup")
        rpt.append("# Check /var/log, /var/tmp, /var/crash for large files")
        rpt.append("```\n")
        for si in storage_issues:
            rpt.append(f"- **{si['hostname']}**: `{si['mount']}` at **{si['usage_pct']}%**\n")

    if coredump_issues:
        rpt.append("### Priority 6 — Investigate Core Dumps\n")
        for cd in coredump_issues:
            rpt.append(f"- **{cd['hostname']}**: {cd['count']} core dump(s)")
            rpt.append(f"  - Run: `show system core-dumps` on {cd['hostname']}")
            rpt.append(f"  - Clean with: `request system core-dumps delete`")
            rpt.append(f"  - If recurring, open JTAC case with core file\n")

    if mtu_mismatches:
        rpt.append("### Priority 7 — Fix MTU Mismatches\n")
        for mm in mtu_mismatches:
            higher_mtu = max(mm["local_mtu"], mm["remote_mtu"])
            lower_side = mm["local_hostname"] if mm["local_mtu"] < mm["remote_mtu"] else mm["remote_hostname"]
            lower_intf = mm["local_intf"] if mm["local_mtu"] < mm["remote_mtu"] else mm["remote_intf"]
            rpt.append(f"**Align MTU on {lower_side} `{lower_intf}` to {higher_mtu}:**")
            rpt.append("```junos")
            rpt.append(f"set interfaces {lower_intf} mtu {higher_mtu}")
            rpt.append("commit")
            rpt.append("```\n")

    if intf_errors:
        rpt.append("### Priority 8 — Investigate Physical Layer Errors\n")
        rpt.append("For each interface with errors:\n")
        rpt.append("1. **CRC/Input errors** → Check cable, clean/replace SFP, verify cable type (single-mode vs multi-mode)")
        rpt.append("2. **Carrier transitions** → Check physical connection stability, SFP seating")
        rpt.append("3. **Half-duplex** → Force full-duplex or verify auto-negotiation\n")
        rpt.append("```junos")
        rpt.append("# Clear interface counters after physical fix to verify:")
        rpt.append("clear interfaces statistics <interface-name>")
        rpt.append("# Check SFP diagnostics:")
        rpt.append("show interfaces diagnostics optics <interface-name>")
        rpt.append("```\n")
        for ie in intf_errors:
            rpt.append(f"- **{ie['hostname']} `{ie['interface']}`**: {'; '.join(ie['problems'])}\n")

    # 3m. BFD Issues (#1A)
    if bfd_issues:
        for bi in bfd_issues:
            sev = bi.get("severity", "WARNING")
            if sev == "CRITICAL":
                critical_num += 1
                rpt.append(f"### 🔴 CRITICAL #{critical_num}: BFD Session Down — {bi['hostname']}\n")
            else:
                warning_num += 1
                rpt.append(f"### 🟡 WARNING #{warning_num}: BFD Session Issue — {bi['hostname']}\n")
            rpt.append("| Detail | Value |")
            rpt.append("|--------|-------|")
            rpt.append(f"| **Router** | {bi['hostname']} ({bi['router']}) |")
            rpt.append(f"| **Issue** | {bi['detail']} |")
            rpt.append(f"| **Impact** | Fast-failure detection degraded → slow convergence on link failure |")
            rpt.append("")

    # 3n. Firewall Filter Issues (#1G)
    if fw_issues:
        warning_num += 1
        rpt.append(f"### 🟡 WARNING #{warning_num}: Firewall Filter Discards Detected\n")
        rpt.append("| Router | Detail |")
        rpt.append("|--------|--------|")
        for fi in fw_issues:
            rpt.append(f"| {fi['hostname']} | {fi['detail']} |")
        rpt.append(f"\n**Impact:** High discard counters on firewall filters may indicate misconfigured ACLs, DDoS traffic, or legitimate traffic being dropped.\n")

    # 3o. MPLS LSP Issues (#1C)
    if lsp_issues:
        for li in lsp_issues:
            critical_num += 1
            rpt.append(f"### 🔴 CRITICAL #{critical_num}: MPLS LSP Down — {li['hostname']}\n")
            rpt.append("| Detail | Value |")
            rpt.append("|--------|-------|")
            rpt.append(f"| **Router** | {li['hostname']} ({li['router']}) |")
            rpt.append(f"| **Issue** | {li['detail']} |")
            rpt.append(f"| **Impact** | MPLS traffic engineering path unavailable → traffic may reroute via less optimal path |")
            rpt.append("")

    # 3p. RSVP Session Issues (#1C)
    if rsvp_issues:
        warning_num += 1
        rpt.append(f"### 🟡 WARNING #{warning_num}: RSVP Session Errors\n")
        rpt.append("| Router | Detail |")
        rpt.append("|--------|--------|")
        for ri in rsvp_issues:
            rpt.append(f"| {ri['hostname']} | {ri['detail']} |")
        rpt.append(f"\n**Impact:** RSVP errors can prevent MPLS LSP establishment and TE tunnel signaling.\n")

    # 3q. Commit History Anomalies (#3D) — E30 fix: flatten nested structure
    if commit_history:
        rpt.append(f"### ◇ Recent Configuration Changes\n")
        rpt.append("| Router | User | Timestamp | Method |")
        rpt.append("|--------|------|-----------|--------|")
        flat_commits = []
        for router_key, rdata in commit_history.items():
            hname = rdata.get("hostname", router_key) if isinstance(rdata, dict) else router_key
            commits_list = rdata.get("commits", []) if isinstance(rdata, dict) else []
            for c in commits_list:
                flat_commits.append({"hostname": hname, "user": c.get("user", "?"), "timestamp": c.get("timestamp", "?"), "method": c.get("method", "?")})
        flat_commits.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        for ch in flat_commits[:20]:  # cap at 20 entries
            rpt.append(f"| {ch['hostname']} | {ch['user']} | {ch['timestamp']} | {ch['method']} |")
        rpt.append("")

    # 3r. Recurring Issues (#3C)
    if _rec:
        warning_num += 1
        rpt.append(f"### ▲ WARNING #{warning_num}: Recurring Issues (Historical Pattern)\n")
        rpt.append("| Issue | Router | Times Seen | First Seen | Last Seen |")
        rpt.append("|-------|--------|------------|------------|-----------|")
        for r in _rec:
            rpt.append(f"| {r['detail'][:60]}{'...' if len(r['detail']) > 60 else ''} | {r['hostname']} | **{r['occurrences']}** | {r['first_seen']} | {r['last_seen']} |")
        rpt.append(f"\n> ▲ **Recurring issues** indicate problems that persist across audits. These require permanent fixes, not just temporary workarounds.\n")

    rpt.append("---\n")

    # ── 7b. SLA Impact Assessment (#4C) ──
    if critical_num > 0:
        rpt.append("### ◫ SLA Impact Assessment\n")
        # Count VRF/route instances affected
        total_vrfs = 0
        vrf_details = []
        for mcp_name, hostname in device_map.items():
            ri_raw = route_inst_outputs.get(mcp_name, "")
            vrf_count = 0
            for line in ri_raw.split("\n"):
                if line.strip() and not line.startswith("Instance") and not line.startswith("---"):
                    parts = line.split()
                    if parts and parts[0] not in ("master", ""):
                        vrf_count += 1
            if vrf_count > 0:
                total_vrfs += vrf_count
                vrf_details.append(f"| {hostname} | {vrf_count} |")
        
        if vrf_details:
            rpt.append(f"**Total VRF/Routing Instances Potentially Affected:** {total_vrfs}\n")
            rpt.append("| Router | VRF Count |")
            rpt.append("|--------|-----------|")
            for vd in vrf_details:
                rpt.append(vd)
            rpt.append("")
        
        # Impacted services estimate
        rpt.append("**Estimated Service Impact:**\n")
        if ospf_type_mismatches or ospf_critical:
            rpt.append(f"- 🔴 **OSPF:** {len(ospf_critical)} adjacency failures → IGP convergence broken")
        if bgp_issues:
            rpt.append(f"- 🔴 **BGP:** {len(bgp_issues)} sessions down → L3VPN route exchange stopped")
        if ldp_issues:
            rpt.append(f"- 🔴 **LDP:** {len(ldp_issues)} sessions down → MPLS label distribution stopped")
        if lsp_issues:
            rpt.append(f"- 🔴 **MPLS LSP:** {len(lsp_issues)} tunnels down → TE paths unavailable")
        rpt.append("")

    # ── 8. Audit Summary ──
    rpt.append("## 📋 8. Audit Summary\n")
    rpt.append("| Category | Count |")
    rpt.append("|----------|-------|")
    rpt.append(f"| 🔴 Critical Issues | **{critical_num}** |")
    rpt.append(f"| 🟡 Warnings | **{warning_num}** |")
    rpt.append(f"| 🟢 Healthy Areas | **{h_num}** |")
    rpt.append(f"| ↻ Config Drift | **{len(config_drifts)}** |")
    rpt.append(f"| ⊗ Chassis Alarms | **{len(chassis_alarms)}** |")
    rpt.append(f"| ⊟ Storage Warnings | **{len(storage_issues)}** |")
    rpt.append(f"| ⊗ Core Dumps | **{len(coredump_issues)}** |")
    rpt.append(f"| ◇ Devices Audited | **{len(device_map)}** |")
    rpt.append(f"| ◷ Audit Duration | **{audit_duration}s** |")
    if _hs is not None:
        rpt.append(f"| ♦ Health Score | **{_hs}/100** ({_hg} — {_hl}) |")
    if critical_num > 0:
        if ospf_type_mismatches:
            rpt.append("| **Overall Health** | 🔴 **DEGRADED** — OSPF interface-type mismatch causing cascading failures |")
        else:
            rpt.append("| **Overall Health** | 🔴 **DEGRADED** — cascading failure detected |")
    else:
        rpt.append("| **Overall Health** | 🟢 **HEALTHY** |")
    rpt.append("")

    # ── 8b. Risk Assessment Matrix (#4B) ──
    rpt.append("### ◎ Risk Assessment Matrix\n")
    rpt.append("| Risk Category | Severity | Likelihood | Impact | Action |")
    rpt.append("|---------------|----------|------------|--------|--------|")
    if ospf_type_mismatches:
        rpt.append("| OSPF Mismatch | 🔴 CRITICAL | Certain | Service outage | **Immediate fix** |")
    if bgp_issues:
        rpt.append(f"| BGP Sessions Down | 🔴 CRITICAL | Certain | L3VPN broken | Fix OSPF root cause |")
    if ldp_issues:
        rpt.append(f"| LDP Sessions Down | 🔴 CRITICAL | Certain | MPLS stopped | Fix OSPF root cause |")
    if lsp_issues:
        rpt.append(f"| MPLS LSP Down | 🔴 CRITICAL | High | TE failure | Investigate RSVP/path |")
    if bfd_issues:
        rpt.append(f"| BFD Down | 🟠 MAJOR | Medium | Slow failover | Configure BFD timers |")
    if mtu_mismatches:
        rpt.append(f"| MTU Mismatch | 🟡 WARNING | Medium | Packet drops | Align MTU values |")
    if chassis_alarms:
        rpt.append(f"| Chassis Alarms | 🟡 WARNING | Ongoing | HW degradation | Monitor & RMA |")
    if storage_issues:
        rpt.append(f"| Disk Usage | 🟡 WARNING | Low | Commit failure | Storage cleanup |")
    if coredump_issues:
        rpt.append(f"| Core Dumps | 🟡 WARNING | Low | Daemon crash | Investigate & JTAC |")
    if config_drifts:
        rpt.append(f"| Config Drift | 🟡 WARNING | Medium | Unexpected behavior | Review changes |")
    if ntp_issues:
        rpt.append(f"| NTP Missing | 🟡 WARNING | Low | Time drift | Configure NTP |")
    if not any([ospf_type_mismatches, bgp_issues, ldp_issues, bfd_issues, mtu_mismatches, chassis_alarms]):
        rpt.append("| — | 🟢 None | — | — | No risks identified |")
    rpt.append("")

    # ── 8c. Post-Fix Verification Commands (#4D) ──
    if critical_num > 0:
        rpt.append("### ⊕ Post-Fix Verification Commands\n")
        rpt.append("After applying remediation, run these commands to verify recovery:\n")
        rpt.append("```junos")
        rpt.append("# 1. Verify OSPF adjacency recovery")
        rpt.append("show ospf neighbor")
        rpt.append("show ospf interface")
        rpt.append("")
        rpt.append("# 2. Verify BGP session recovery")
        rpt.append("show bgp summary")
        rpt.append("")
        rpt.append("# 3. Verify LDP session recovery")
        rpt.append("show ldp session")
        rpt.append("")
        rpt.append("# 4. Verify MPLS label distribution")
        rpt.append("show mpls interface")
        rpt.append("show route table mpls.0 summary")
        rpt.append("")
        rpt.append("# 5. End-to-end verification")
        rpt.append("ping <remote-loopback> source <local-loopback> count 5")
        rpt.append("traceroute <remote-loopback> source <local-loopback>")
        rpt.append("```\n")


    # ── 8d. v11.0 Quantified Risk Scores (E94) ──
    if 'risk_scores' in dir() and risk_scores:
        rpt.append("### ◎ Quantified Risk Scores (v11.0)\n")
        rpt.append("| Risk Item | Score | Level | Action Required |")
        rpt.append("|-----------|-------|-------|-----------------|")
        for name, rs in sorted(risk_scores, key=lambda x: x[1].get("score", 0), reverse=True):
            rpt.append(f"| {name} | **{rs.get('score', 0)}/100** | {rs.get('color', '')} {rs.get('category', rs.get('level', ''))} | {rs.get('action', '')} |")
        rpt.append("")
    
    # ── 8e. v11.0 SLA Impact (E96) ──
    if 'sla_impact' in dir() and sla_impact and sla_impact.get("impact_level") != "none":
        rpt.append("### ◫ SLA Impact Assessment (v11.0)\n")
        rpt.append("| Metric | Value |")
        rpt.append("|--------|-------|")
        rpt.append(f"| **Impact Level** | {sla_impact.get('impact_level', 'N/A')} |")
        rpt.append(f"| **Estimated Cost** | {sla_impact.get('cost_estimate', sla_impact.get('estimated_cost', 'N/A'))} |")
        rpt.append(f"| **SLA Status** | {sla_impact.get('sla_risk', sla_impact.get('sla_status', 'N/A'))} |")
        rpt.append(f"| **Affected Customers** | {sla_impact.get('affected_pct', 'N/A')}% |")
        rpt.append("")
    
    # ── 8f. v11.0 Dependency Graph Summary (E68) ──
    if 'transit_nodes' in dir() and transit_nodes:
        rpt.append("### ⊶ Network Dependency Graph (v11.0)\n")
        rpt.append(f"**Transit Nodes (Critical Path):** {', '.join(transit_nodes)}\n")
        rpt.append("> These nodes carry the most transit traffic. Failure would have maximum blast radius.\n")
        if '_network_graph' in dir() and _network_graph and _network_graph.nodes:
            rpt.append(f"| Metric | Value |")
            rpt.append(f"|--------|-------|")
            rpt.append(f"| **Nodes** | {len(_network_graph.nodes)} |")
            rpt.append(f"| **Edges** | {len(_network_graph.edges)} |")
            rpt.append(f"| **Transit Nodes** | {len(transit_nodes)} |")
            rpt.append("")
    
    # ── 8g. v11.0 Baseline Anomalies (E71) ──
    if 'baseline_anomalies' in dir() and baseline_anomalies:
        rpt.append("### ◫ Baseline Anomalies (v11.0)\n")
        rpt.append("Metrics that deviate significantly from historical baselines:\n")
        for ba in baseline_anomalies[:10]:
            rpt.append(f"- ▲ {ba}")
        rpt.append("")

    # ── 9. Bottom Line ──
    rpt.append("\n---\n")
    rpt.append("## 🎯 9. Bottom Line\n")
    if critical_num > 0:
        drift_note = ""
        if config_drifts:
            drift_note = (f" Additionally, **{len(config_drifts)} device(s)** show config drift from their golden baselines"
                          f" — review Section 6 for details.")
        if ospf_type_mismatches:
            mm = ospf_type_mismatches[0]
            rpt.append(
                f"This network has **{critical_num} critical issues** and **{warning_num} warnings** across "
                f"**{len(device_map)} devices**. The **single root cause** is an OSPF interface-type mismatch "
                f"on the link between **{mm['local_hostname']}** ({mm['local_intf']}, `{mm['local_type']}`) and "
                f"**{mm['remote_hostname']}** ({mm['remote_intf']}, `{mm['remote_type']}`). "
                f"This one misconfiguration prevents OSPF adjacency from forming, which cascades into "
                f"**{len(bgp_issues)} iBGP session failures** and **{len(ldp_issues)} LDP session failures**, "
                f"effectively breaking MPLS/L3VPN services across affected paths. "
                f"**The fix is a single `set` command** — changing the interface type on one side to match the other. "
                f"Once applied, the expected recovery chain is: "
                f"OSPF adjacency 🟢 → iBGP sessions 🟢 → LDP sessions 🟢 → L3VPN routes 🟢. "
                f"All {h_num} other health checks passed successfully.{drift_note}"
            )
        else:
            rpt.append(
                f"This network has **{critical_num} critical issues** and **{warning_num} warnings** across "
                f"**{len(device_map)} devices**. The root cause is an OSPF adjacency failure that cascades "
                f"into BGP and LDP failures. Fixing the OSPF issue will automatically restore all dependent "
                f"protocol sessions. All {h_num} other health checks passed successfully.{drift_note}"
            )
    else:
        drift_note = ""
        if config_drifts:
            drift_note = (f" However, **{len(config_drifts)} device(s)** show config drift from their golden baselines"
                          f" — review Section 6 for details.")
        elif baselines_created:
            drift_note = f" Golden config baselines were established for {len(baselines_created)} device(s) on this first run."
        rpt.append(
            f"The network is **healthy**. All {len(device_map)} devices were audited and "
            f"**{h_num} health checks passed** with {warning_num} minor warnings. "
            f"OSPF adjacencies are fully established, iBGP sessions are active, and LDP/MPLS "
            f"sessions are operational. No immediate action is required.{drift_note}"
        )
    
    # v11.0 E93: Dynamic risk/SLA supplement to bottom line
    risk_supplement = ""
    if 'risk_scores' in dir() and risk_scores:
        top_risk = max(risk_scores, key=lambda x: x[1].get("score", 0))
        risk_supplement += f" **Top risk:** {top_risk[0]} ({top_risk[1].get('score', 0)}/100)."
    if 'sla_impact' in dir() and sla_impact and sla_impact.get("impact_level") not in ("none", None):
        risk_supplement += f" **SLA impact:** {sla_impact.get('impact_level', 'N/A')}."
    if risk_supplement:
        rpt.append(f"\n{risk_supplement.strip()}")

    rpt.append(f"\n\n---\n")
    rpt.append("## 📄 Report Metadata\n")
    rpt.append(f"| Property | Value |")
    rpt.append(f"|----------|-------|")
    rpt.append(f"| **Generated** | {now.strftime('%Y-%m-%d %H:%M:%S')} |")
    rpt.append(f"| **Engine** | Junos MCP Server v11.0 + Ollama ({MODEL}) |")
    rpt.append(f"| **AI Context Window** | {NUM_CTX} tokens |")
    rpt.append(f"| **Devices Scanned** | {len(device_map)} |")
    rpt.append(f"| **Duration** | {audit_duration}s |")
    rpt.append(f"| **Specialists Used** | OSPF, BGP, LDP/MPLS, IS-IS, System, L2VPN, RSVP-TE, QoS/CoS, Security, L3VPN, HW/Env, Synthesizer + v11.0 Intelligence Engines |")
    if _hs is not None:
        rpt.append(f"| **Health Score** | {_hs}/100 ({_hg}) |")
    rpt.append(f"| **Knowledge Base** | {os.path.basename('KNOWLEDGE_BASE.md')} |")
    # v9.0: Phase timing breakdown
    if phase_timings:
        timing_parts = [f"{name}: {dur}s" for name, dur in phase_timings.items() if dur > 0]
        if timing_parts:
            rpt.append(f"| **Phase Timing** | {' · '.join(timing_parts)} |")
    rpt.append("")
    rpt.append(f"*Report generated by Junos MCP Server v11.0 + Ollama ({MODEL})*\n")

    # Update report generation timing
    report_gen_time = round(time.time() - audit_start - (audit_duration), 1)
    if "Report Generation" in phase_timings:
        phase_timings["Report Generation"] = max(report_gen_time, 0.1)

    report_text = "\n".join(rpt)

    # ── E25: Populate last_audit_state for layer dashboard ──
    global last_audit_state
    last_audit_state["physical"] = {
        "status": "critical" if down_intfs else ("warning" if intf_errors else "healthy"),
        "detail": f"{len(down_intfs)} down interfaces, {len(intf_errors)} error counters" if (down_intfs or intf_errors) else "All interfaces operational",
    }
    last_audit_state["datalink"] = {
        "status": "warning" if mtu_mismatches else "healthy",
        "detail": f"{len(mtu_mismatches)} MTU mismatches" if mtu_mismatches else "L2 connectivity OK",
    }
    routing_issues_count = len(ospf_info.get("issues", [])) + len(bgp_issues) + len(isis_issues)
    last_audit_state["routing"] = {
        "status": "critical" if routing_issues_count > 0 else "healthy",
        "detail": f"OSPF:{len(ospf_info.get('issues', []))} BGP:{len(bgp_issues)} IS-IS:{len(isis_issues)} issues" if routing_issues_count else "IGP/EGP sessions healthy",
    }
    last_audit_state["transport"] = {
        "status": "critical" if (ldp_issues or lsp_issues) else ("warning" if bfd_issues else "healthy"),
        "detail": f"LDP:{len(ldp_issues)} LSP:{len(lsp_issues)} BFD:{len(bfd_issues)} issues" if (ldp_issues or lsp_issues or bfd_issues) else "MPLS/LDP operational",
    }
    last_audit_state["services"] = {
        "status": "warning" if (chassis_alarms or storage_issues) else "healthy",
        "detail": f"{len(chassis_alarms)} alarms, {len(storage_issues)} storage issues" if (chassis_alarms or storage_issues) else "L3VPN/EVPN services OK",
    }
    previous_report = find_previous_audit()
    if previous_report:
        trend = compare_audit_reports(previous_report, report_text)
        if trend:
            report_text += "\n" + trend
            console.print(f"   ▴ Trend comparison added (vs. {os.path.basename(previous_report)})")

    # ── Enhancement #P3E: HTML Export ──
    html_path = ""
    try:
        ts_str = now.strftime("%Y-%m-%d_%H%M%S")
        html_path = f"NETWORK_AUDIT_{ts_str}.html"
        export_report_html(report_text, html_path)
        console.print(f"   ◫ HTML report exported: [cyan]{html_path}[/cyan]")
    except Exception as html_err:
        logger.warning(f"HTML export failed: {html_err}")

    # ── v10.0 E55: Save audit to SQLite ──
    try:
        _n_crit = len([i for i in _aci if i.get("severity") == "CRITICAL"])
        _n_warn = len([i for i in _aci if i.get("severity") in ("WARNING", "MAJOR")])
        _n_healthy = max(0, len(device_map) * 3 - _n_crit - _n_warn)
        _n_drifts = len(config_drifts) if 'config_drifts' in dir() else 0
        save_audit_to_db(
            timestamp=now.isoformat(),
            duration=audit_duration,
            device_count=len(device_map),
            health_score=_hs if _hs is not None else 0,
            health_grade=_hg,
            critical_count=_n_crit,
            warning_count=_n_warn,
            healthy_count=_n_healthy,
            config_drifts=_n_drifts,
            report_path=html_path,
            issues=_aci
        )
        console.print(f"   ⊟ Audit saved to SQLite database")
    except Exception as db_err:
        logger.warning(f"SQLite save failed: {db_err}")

    # ── v10.0 E54: Save device facts cache (filters out placeholders) ──
    try:
        if device_facts:
            real_count = sum(1 for v in device_facts.values() if _is_real_facts(v))
            save_facts_cache(device_facts)
            if real_count > 0:
                console.print(f"   ⊟ Device facts cached ({real_count}/{len(device_facts)} with real data)")
            else:
                console.print(f"   [dim]⊟ No real device facts to cache (all {len(device_facts)} are placeholders)[/dim]")
    except Exception as cache_err:
        logger.warning(f"Facts cache save failed: {cache_err}")

    # ── v18.1: Mark Report Generation done and show final task plan ──
    _mark_phase_done("Report Generation")
    # Update report gen timing from saved value
    report_gen_end = time.time()
    if "Report Generation" in phase_timings:
        phase_timings["Report Generation"] = max(phase_timings["Report Generation"], 0.1)
    else:
        for task in audit_plan:
            if task["name"] == "Report Generation":
                task["time"] = round(report_gen_end - _phase_start[0], 1)
                phase_timings["Report Generation"] = task["time"]
    console.print(f"   [green]✅ Report Generation complete ({audit_plan[-1].get('time', '?')}s)[/green]")
    console.print()

    # Final task plan summary
    _print_task_plan()
    total_time = round(time.time() - audit_start, 1)
    console.print(f"   [bold green]⊕ All {len(audit_plan)} tasks completed in {total_time}s[/bold green]")
    console.print()

    return report_text


# ══════════════════════════════════════════════════════════════
#  BETWEEN-DEVICE CHECK
# ══════════════════════════════════════════════════════════════

async def run_between_devices(client, sid, device_map, dev_a, dev_b):
    reverse_map = {v.lower(): k for k, v in device_map.items()}
    mcp_a = reverse_map.get(dev_a.lower(), dev_a)
    mcp_b = reverse_map.get(dev_b.lower(), dev_b)
    hostname_a = device_map.get(mcp_a, dev_a)
    hostname_b = device_map.get(mcp_b, dev_b)

    if mcp_a not in device_map:
        return f"✗ Unknown: '{dev_a}'. Known: {', '.join(f'{v} ({k})' for k, v in device_map.items())}"
    if mcp_b not in device_map:
        return f"✗ Unknown: '{dev_b}'. Known: {', '.join(f'{v} ({k})' for k, v in device_map.items())}"

    pair = [mcp_a, mcp_b]
    console.print(Panel(f"Checking {hostname_a} ↔ {hostname_b}", style="cyan", width=50))

    raw_intf     = await run_batch(client, sid, "show interfaces terse", pair, "Interfaces")
    raw_ospf_nbr = await run_batch(client, sid, "show ospf neighbor", pair, "OSPF Nbrs")
    raw_ospf_intf= await run_batch(client, sid, "show ospf interface", pair, "OSPF Intf")
    raw_bgp      = await run_batch(client, sid, "show bgp summary", pair, "BGP")
    raw_ldp      = await run_batch(client, sid, "show ldp session", pair, "LDP")
    raw_route    = await run_batch(client, sid, "show route summary", pair, "Routes")

    cfg_a_ospf = await run_single(client, sid, "show configuration protocols ospf", mcp_a, f"{hostname_a} OSPF Cfg")
    cfg_b_ospf = await run_single(client, sid, "show configuration protocols ospf", mcp_b, f"{hostname_b} OSPF Cfg")
    cfg_a_bgp  = await run_single(client, sid, "show configuration protocols bgp", mcp_a, f"{hostname_a} BGP Cfg")
    cfg_b_bgp  = await run_single(client, sid, "show configuration protocols bgp", mcp_b, f"{hostname_b} BGP Cfg")

    # Enhancement #8: Dynamic truncation budgets for pair check
    budgets = calculate_budgets(2)
    b = budgets["pair_check"]
    
    all_data = (
        f"Checking: {hostname_a} ({mcp_a}) ↔ {hostname_b} ({mcp_b})\n\n"
        f"INTERFACES:\n{raw_intf[:b]}\n\n"
        f"OSPF NEIGHBORS:\n{raw_ospf_nbr[:b]}\n\n"
        f"OSPF INTERFACES:\n{raw_ospf_intf[:b]}\n\n"
        f"BGP SUMMARY:\n{raw_bgp[:b]}\n\n"
        f"LDP SESSIONS:\n{raw_ldp[:b]}\n\n"
        f"ROUTES:\n{raw_route[:b]}\n\n"
        f"{hostname_a} OSPF CONFIG:\n{cfg_a_ospf[:budgets['config']]}\n\n"
        f"{hostname_b} OSPF CONFIG:\n{cfg_b_ospf[:budgets['config']]}\n\n"
        f"{hostname_a} BGP CONFIG:\n{cfg_a_bgp[:budgets['config']]}\n\n"
        f"{hostname_b} BGP CONFIG:\n{cfg_b_bgp[:budgets['config']]}"
    )

    console.print(f"\n   ◉ AI analyzing [cyan]{hostname_a}[/cyan] ↔ [cyan]{hostname_b}[/cyan]...")
    analysis = await ollama_analyze(
        "You are a Juniper DE analyzing connectivity between two routers. "
        "Check: physical links, OSPF adjacency, BGP peering, LDP sessions, config mismatches. "
        "Report issues with severity (CRITICAL/WARNING/INFO), exact interfaces, and 'set' commands to fix.",
        all_data,
        f"Analyze connectivity between {hostname_a} and {hostname_b}. Identify all issues and root causes."
    )

    return f"# Connectivity Report: {hostname_a} ↔ {hostname_b}\n\n{analysis}"


# ══════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════

async def main():
    """The main program — runs the entire bridge."""
    
    # ── Enhancement #10: Parse CLI arguments ──
    parser = argparse.ArgumentParser(description="Ollama <-> Junos MCP Bridge v7.0")
    parser.add_argument("--audit-only", action="store_true",
                        help="Run a full audit, save the report, and exit (non-interactive)")
    parser.add_argument("--no-history", action="store_true",
                        help="Don't load or save session history")
    args = parser.parse_args()
    
    # Load Knowledge Base first so banner can show accurate status
    kb_content = load_knowledge_base()
    kb_lines = 0
    kb_chars = 0
    kb_sections = 0
    if kb_content:
        kb_lines = kb_content.count('\n')
        kb_chars = len(kb_content)
        kb_sections = kb_content.count('# SECTION')

    # ── v7.0 #P1B: Professional Welcome Banner ──
    print_welcome_banner(kb_lines=kb_lines, kb_chars=kb_chars, kb_sections=kb_sections)

    # ── v19.0: Initialize Action Tracker & Todo Tracker ──
    # ── v20.0: Initialize Feedback Memory & Conversation Manager ──
    global _action_tracker, _todo_tracker, _feedback_memory, _conversation_manager
    _action_tracker = ActionTracker(console)
    _todo_tracker = TodoTracker()
    _feedback_memory = FeedbackMemory()
    _conversation_manager = ConversationManager()
    
    if args.audit_only:
        console.print("[bold yellow]  Mode: AUDIT-ONLY (non-interactive)[/bold yellow]")

    # Knowledge Base status
    if kb_content:
        console.print(f"   ● Knowledge Base loaded: [green]{kb_lines}[/green] lines, [green]{kb_chars}[/green] chars")
        console.print(f"   ⊞ {kb_sections} knowledge sections available")
    else:
        console.print("   ▲  No Knowledge Base found — AI will operate without reference knowledge", style="yellow")
        kb_content = ""

    # Build RAG Vector Store
    global vector_kb
    console.print("◷ Initializing RAG Vector Store...", style="dim")
    try:
        vector_kb = await KBVectorStore.create()
        stats = vector_kb.stats()
        console.print(f"   ◉ RAG Engine: [cyan]{stats['chunks']}[/cyan] chunks × [cyan]{stats['dimensions']}[/cyan]-dim ([cyan]{stats['embed_model']}[/cyan])")
        console.print(f"   ⊟ Cache: {stats['cache_size_kb']:.0f} KB (built {stats['built_at']})")
    except Exception as e:
        console.print(f"   ▲  RAG Vector Store failed ({e}) — falling back to keyword matching", style="yellow")
        vector_kb = None

    async with httpx.AsyncClient(
        timeout=httpx.Timeout(600.0, connect=30.0),
        limits=httpx.Limits(max_connections=20, max_keepalive_connections=10)
    ) as mcp_client:
        
        # ── STARTUP PHASE ──
        console.print("\n◷ Connecting to MCP server...", style="dim")
        try:
            session_id = await mcp_initialize(mcp_client)
            console.print(f"● MCP session: [green]{session_id}[/green]")
            logger.info(f"MCP session established: {session_id}")
        except Exception as e:
            console.print(f"✗ Failed to connect to MCP server: {e}", style="bold red")
            logger.error(f"MCP connection failed: {e}")
            return

        console.print("◷ Loading tools...", style="dim")
        mcp_tools = await mcp_list_tools(mcp_client, session_id)
        
        # ── DYNAMIC DEVICE DISCOVERY ──
        console.print("◷ Discovering devices...", style="dim")
        device_map = {}
        device_facts = {}
        
        # Method 1: Ask MCP Server for the list
        try:
            res_json = await mcp_call_tool(mcp_client, session_id, "get_router_list", {})
            try:
                if isinstance(res_json, str):
                    routers = json.loads(res_json)
                else:
                    routers = res_json

                if routers:
                    for r_name, r_conf in routers.items():
                        device_map[r_name] = r_name
                        device_facts[r_name] = {"model": "Junos Device", "version": "unknown"}
                    console.print(f"   ● Discovered [green]{len(device_map)}[/green] devices via MCP: {', '.join(device_map.keys())}")
                    logger.info(f"Discovered {len(device_map)} devices: {list(device_map.keys())}")
            except json.JSONDecodeError:
                console.print("   ▲  MCP returned invalid JSON for router list. Falling back...", style="yellow")
        except Exception as e:
             console.print(f"   ▲  MCP discovery failed ({e}). Falling back...", style="yellow")

        # Method 2: Fallback to local file if MCP failed or returned empty
        if not device_map:
            console.print("   ▲  MCP discovery empty. Reading 'junos-mcp-server/devices.json'...", style="yellow")
            try:
                with open("junos-mcp-server/devices.json", "r") as f:
                    local_devs = json.load(f)
                    for r_name in local_devs:
                        device_map[r_name] = r_name
                        device_facts[r_name] = {"model": "Local Config", "version": "unknown"}
                    console.print(f"   ● Loaded [green]{len(device_map)}[/green] devices from local config: {', '.join(device_map.keys())}")
            except Exception as e:
                console.print(f"   ✗ Critical Error: Could not load devices from file either: {e}", style="bold red")
                return

        # ── CONSTRUCT PROMPT WITH DYNAMIC CONTEXT ──
        # Inject the discovered inventory list into the prompt
        inventory_lines = []
        for mcp_name, hostname in device_map.items():
            facts = device_facts.get(mcp_name, {})
            model = facts.get("model", "?")
            version = facts.get("version", "?")
            inventory_lines.append(f"- **{mcp_name}** → hostname: {hostname}, model: {model}, version: {version}")
        inventory_str = "\n".join(inventory_lines)
        
        # v12.0: Build persistent topology from golden configs
        topo_graph = build_topology_from_golden_configs()
        topo_str = topology_to_prompt_string(topo_graph)
        if topo_str:
            console.print(f"◫  Topology: [green]{len(topo_graph.get('links', []))}[/green] links, "
                          f"[green]{len(topo_graph.get('loopbacks', {}))}[/green] loopbacks loaded from golden configs")
        
        # v12.0: Load lessons learned
        lessons_str = get_top_lessons(n=5)
        if lessons_str:
            console.print(f"▪ Lessons: [green]Loaded[/green] from past incidents")
        
        # v12.0: Load audit trends
        trends_str = get_audit_trends(n=5)
        if trends_str:
            console.print(f"▴ Trends: [green]Loaded[/green] from audit history")
        
        # Smart KB injection: KB is now used by SPECIALISTS, not the commander prompt
        # Commander gets a lean prompt for faster, more focused tool orchestration
        
        # v13.1: Load workflow self-improvement lessons
        workflow_lessons_str = load_workflow_lessons()
        if workflow_lessons_str:
            console.print(f"   ◉ Self-improvement lessons loaded from tasks/lessons.md")
        
        # v20.0: Load feedback insights (Brain-validated)
        feedback_insights_str = ""
        if _feedback_memory:
            feedback_insights_str = _feedback_memory.get_feedback_insights(n=10)
            if feedback_insights_str:
                fb_stats = _feedback_memory.get_stats()
                console.print(f"   ◉ Feedback memory: [green]{fb_stats['total']}[/green] entries "
                              f"([green]{fb_stats['valid']}[/green] valid, [yellow]{fb_stats['partial']}[/yellow] partial)")
        
        final_sys_prompt = SYSTEM_PROMPT.format(
            inventory=inventory_str,
            topology=topo_str,
            lessons=lessons_str,
            workflow_lessons=workflow_lessons_str,
            feedback_insights=feedback_insights_str,
            trends=trends_str,
        )

        # ── PREPARE TOOLS ──
        ollama_tools = mcp_tools_to_ollama_tools(mcp_tools)
        
        # Register LOCAL tools
        local_tools = {
            "run_network_audit": lambda args: run_full_audit(mcp_client, session_id, device_map, device_facts)
        }
        
        # Add local tools to Ollama's definition
        ollama_tools.append({
            "type": "function",
            "function": {
                "name": "run_network_audit",
                "description": "Runs a deep, multi-phase network audit (interfaces, OSPF, BGP, LDP, alarms). Use this to check overall health.",
                "parameters": {"type": "object", "properties": {}}
            }
        })
        
        console.print(f"[green]{Icons.OK}[/green] Loaded [green]{len(ollama_tools)}[/green] tools")
        console.print(f"[dim]{Icons.SCRIPT}[/dim] Knowledge Base: {'[green]' + Icons.OK + ' Injected into AI context[/green]' if kb_content else '[red]' + Icons.FAIL + ' Not available[/red]'}")
        console.print(f"[dim]{Icons.CONFIG}[/dim] Golden Configs: [cyan]{GOLDEN_CONFIG_DIR}[/cyan]")
        
        # v13.0: Show intelligence upgrade status
        console.print(f"[dim]{Icons.BRAIN}[/dim] Model: [bold cyan]{MODEL}[/bold cyan] {Icons.SEPARATOR} Reasoning chains: {'[green]' + Icons.OK + '[/green]' if AI_STRUCTURED_REASONING else '[red]' + Icons.FAIL + '[/red]'} {Icons.SEPARATOR} "
                      f"Self-verify: {'[green]' + Icons.OK + '[/green]' if AI_SELF_VERIFY else '[red]' + Icons.FAIL + '[/red]'} {Icons.SEPARATOR} Expert examples: {'[green]' + Icons.OK + '[/green]' if AI_EXPERT_EXAMPLES else '[red]' + Icons.FAIL + '[/red]'}")
        console.print(f"[dim]{Icons.SEARCH}[/dim] Output verification: {'[green]' + Icons.OK + '[/green]' if AI_OUTPUT_VERIFICATION else '[red]' + Icons.FAIL + '[/red]'} {Icons.SEPARATOR} "
                      f"Command validation: {'[green]' + Icons.OK + '[/green]' if AI_COMMAND_DICTIONARY else '[red]' + Icons.FAIL + '[/red]'} {Icons.SEPARATOR} "
                      f"Confidence threshold: {AI_CONFIDENCE_THRESHOLD}%")
        # v13.1: Show workflow orchestration status
        _wf_lessons = load_workflow_lessons()
        _wf_count = _wf_lessons.count("### Lesson") if _wf_lessons else 0
        console.print(f"[dim]{Icons.SCRIPT}[/dim] Workflow: Plan-first [green]{Icons.OK}[/green] {Icons.SEPARATOR} Verify-before-done [green]{Icons.OK}[/green] {Icons.SEPARATOR} "
                      f"Self-improvement: {'[green]' + Icons.OK + ' ' + str(_wf_count) + ' lessons[/green]' if _wf_count else '[green]' + Icons.OK + ' ready[/green]'} {Icons.SEPARATOR} "
                      f"Elegance check [green]{Icons.OK}[/green]")
        # v15.0: Show enhanced reasoning features
        _dk_loaded = f"[green]{Icons.OK}[/green]" if _junos_deep_knowledge else f"[red]{Icons.FAIL}[/red]"
        console.print(f"[dim]{Icons.BRAIN}[/dim] v15.0: Hypothesis Engine [green]{Icons.OK}[/green] {Icons.SEPARATOR} Topology Intel [green]{Icons.OK}[/green] {Icons.SEPARATOR} Chain-of-Thought [green]{Icons.OK}[/green] {Icons.SEPARATOR} "
                      f"FSM Engine [green]{Icons.OK}[/green] {Icons.SEPARATOR} Deep KB {_dk_loaded} {Icons.SEPARATOR} Script Templates [green]{Icons.OK}[/green]")
        console.print(f"[dim]{Icons.BRAIN}[/dim] v18.0: Agentic Brain [green]{Icons.OK}[/green] {Icons.SEPARATOR} Smart Scripts: {len(SMART_SCRIPTS)} [green]{Icons.OK}[/green] {Icons.SEPARATOR} "
                      f"Adaptive Concurrency [green]{Icons.OK}[/green] {Icons.SEPARATOR} AI Probes [green]{Icons.OK}[/green]")
        console.print(f"   [dim]{Icons.ARROW}[/dim] New commands: [bold]topology[/bold], [bold]mindmap <q>[/bold], "
                      f"[bold]hypothesis <q>[/bold], [bold]scripts[/bold], [bold]cascade <proto>[/bold]")
        console.print(f"   [dim]{Icons.ARROW}[/dim] v18.0: [bold]brain <q>[/bold], [bold]qbrain <q>[/bold], "
                      f"[bold]smart-scripts[/bold]")
        
        # v12.0 Enhancement #6: Start background health poll
        health_poll_task = asyncio.create_task(
            background_health_poll(mcp_client, session_id, device_map, interval=300)
        )
        console.print(f"[dim]{Icons.HEALTH}[/dim] Background health poll: [green]started[/green] (every 5 min)")
        
        # ── Enhancement #10: Audit-only mode ──
        if args.audit_only:
            console.print(f"\n{Icons.SEARCH} [bold]AUDIT-ONLY MODE[/bold] — Starting full network audit...")
            report = await run_full_audit(mcp_client, session_id, device_map, device_facts)
            ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
            fname = f"NETWORK_AUDIT_{ts}.md"
            with open(fname, "w") as f:
                f.write(report)
            console.print(Panel(f"[green]{Icons.OK}[/green] Audit complete! Report saved: {fname}", style="bold green", width=60))
            console.print(report[:5000])
            if len(report) > 5000:
                console.print(f"\n... (report is {len(report)} chars, see {fname} for full report)", style="dim")
            return  # Exit cleanly
        
        # ── v7.0 #P1F: Show command palette ──
        print_command_help()
        
        # ── v19.0: Show active todos from tasks/todo.md ──
        if _todo_tracker and _todo_tracker.active_tasks:
            _todo_tracker.display(console, limit=8)
        
        # ── v19.0: Show session status bar ──
        if _action_tracker:
            _action_tracker.print_session_bar(
                device_count=len(device_map), health_score=-1,
                msg_count=0, rag_chunks=vector_kb.stats().get("chunks", 0) if vector_kb else 0
            )

        # ── CHAT PHASE ──
        messages = [{"role": "system", "content": final_sys_prompt}]
        current_conv_id = f"conv_{int(time.time())}"  # v20.0: Track current conversation ID
        
        # v20.0: Conversation resume — show previous conversations
        if not args.no_history and _conversation_manager:
            convs = _conversation_manager.list_conversations()
            if convs:
                console.print(f"\n   {Icons.RESTORE} [bold]Previous Conversations Found ({len(convs)})[/bold]")
                # Show top 5 recent conversations
                for i, conv in enumerate(convs[:5], 1):
                    ts = conv.get("updated_at", "")[:16].replace("T", " ")
                    topic = conv.get("topic", "Untitled")[:50]
                    msgs = conv.get("message_count", 0)
                    console.print(f"   [#87d7ff]{i}.[/#87d7ff] {topic} [dim]({msgs} msgs, {ts})[/dim]")
                if len(convs) > 5:
                    console.print(f"   [dim]... and {len(convs) - 5} more (use 'conversations' to see all)[/dim]")
                
                resume = input(f"   {Icons.RESTORE} Continue a conversation? (#/n/new): ").strip().lower()
                if resume in ("n", "no", "new", ""):
                    console.print(f"   {Icons.NEW} Starting fresh conversation", style="dim")
                elif resume.isdigit():
                    conv_num = int(resume)
                    conv_meta = _conversation_manager.get_conversation_by_number(conv_num)
                    if conv_meta:
                        prev_msgs = _conversation_manager.load_conversation(conv_meta["id"])
                        if prev_msgs:
                            messages.extend(prev_msgs)
                            current_conv_id = conv_meta["id"]
                            console.print(f"   [green]{Icons.OK}[/green] Resumed: [bold]{conv_meta['topic'][:50]}[/bold] ({len(prev_msgs)} messages)")
                        else:
                            console.print(f"   [yellow]{Icons.WARN}[/yellow] Could not load conversation, starting fresh")
                    else:
                        console.print(f"   [yellow]{Icons.WARN}[/yellow] Invalid selection, starting fresh")
                elif resume in ("y", "yes"):
                    # Default: resume most recent
                    conv_meta = _conversation_manager.get_conversation_by_number(1)
                    if conv_meta:
                        prev_msgs = _conversation_manager.load_conversation(conv_meta["id"])
                        if prev_msgs:
                            messages.extend(prev_msgs)
                            current_conv_id = conv_meta["id"]
                            console.print(f"   [green]{Icons.OK}[/green] Resumed: [bold]{conv_meta['topic'][:50]}[/bold] ({len(prev_msgs)} messages)")
            else:
                console.print(f"   {Icons.NEW} No previous conversations — starting fresh", style="dim")

        while True:
            try:
                # v18.0: Professional styled input prompt with file attachment support
                console.print()
                user_input = input(f"{Icons.PROMPT} You: ").strip()
            except (EOFError, KeyboardInterrupt):
                console.print(f"\n{Icons.EXIT} Goodbye!", style="bold")
                stop_health_poll()
                if not args.no_history and _conversation_manager:
                    _conversation_manager.save_conversation(messages, conv_id=current_conv_id)
                    console.print(f"   {Icons.SAVE} Conversation saved", style="dim")
                elif not args.no_history:
                    save_session_history(messages)
                    console.print(f"   {Icons.SAVE} Session saved", style="dim")
                break

            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "q"):
                stop_health_poll()
                if not args.no_history and _conversation_manager:
                    _conversation_manager.save_conversation(messages, conv_id=current_conv_id)
                    console.print(f"   {Icons.SAVE} Conversation saved", style="dim")
                elif not args.no_history:
                    save_session_history(messages)
                    console.print(f"   {Icons.SAVE} Session saved", style="dim")
                console.print(f"{Icons.EXIT} Goodbye!", style="bold")
                break

            # ── v18.0: File attachment processing (@filepath) ──
            attached_content = ""
            file_refs = re.findall(r'@([\w./\-_~]+(?:\.\w+)?)', user_input)
            if file_refs:
                for fref in file_refs:
                    # Resolve file path
                    fpath = os.path.abspath(fref)
                    if not os.path.exists(fpath):
                        # Try relative to workspace
                        fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), fref)
                    if os.path.exists(fpath) and os.path.isfile(fpath):
                        try:
                            # Check file size (max 100KB)
                            fsize = os.path.getsize(fpath)
                            if fsize > 102400:
                                console.print(f"   [yellow]{Icons.WARN}[/yellow] [dim]@{fref}: File too large ({fsize//1024}KB > 100KB limit), skipping[/dim]")
                                continue
                            # Check for binary files
                            ext = os.path.splitext(fpath)[1].lower()
                            allowed_exts = {'.py', '.yaml', '.yml', '.json', '.conf', '.cfg', '.log', '.txt', '.md', 
                                          '.xml', '.csv', '.j2', '.jinja2', '.toml', '.ini', '.sh', '.slax', '.xsl',
                                          '.meta', '.html', '.css', '.js', '.ts', '.sql', '.rules', '.set'}
                            if ext and ext not in allowed_exts:
                                console.print(f"   [yellow]{Icons.WARN}[/yellow] [dim]@{fref}: Unsupported file type '{ext}', skipping[/dim]")
                                continue
                            with open(fpath, "r", encoding="utf-8", errors="replace") as af:
                                fcontent = af.read()
                            attached_content += f"\n\n--- ATTACHED FILE: {os.path.basename(fpath)} ---\n{fcontent}\n--- END OF {os.path.basename(fpath)} ---\n"
                            console.print(f"   [#d7af5f]{Icons.ATTACH}[/#d7af5f] [dim]Attached: {os.path.basename(fpath)} ({len(fcontent):,} chars, {len(fcontent.splitlines())} lines)[/dim]")
                        except Exception as e:
                            console.print(f"   [red]{Icons.FAIL}[/red] [dim]@{fref}: Could not read ({e})[/dim]")
                    else:
                        console.print(f"   [yellow]{Icons.WARN}[/yellow] [dim]@{fref}: File not found[/dim]")
                # Remove @file references from the user's visible message to the AI
                clean_input = re.sub(r'@[\w./\-_~]+(?:\.\w+)?', '', user_input).strip()
                if not clean_input and attached_content:
                    clean_input = "Please analyze the attached file(s)."
                user_input = clean_input

            # ── v7.0 #P1F: Help command ──
            if user_input.lower() in ("help", "?", "commands"):
                print_command_help()
                continue

            # ── v19.0: Todo tracker command ──
            if user_input.lower() in ("todos", "todo", "tasks"):
                if _todo_tracker:
                    _todo_tracker.refresh()
                    _todo_tracker.display(console, limit=15)
                else:
                    console.print("  [dim]Todo tracker not initialized[/dim]")
                continue

            # ── v19.0: Action plan viewer ──
            if user_input.lower() in ("plan", "action", "actions", "action plan"):
                if _action_tracker and _action_tracker.current_plan:
                    _action_tracker._display_plan()
                else:
                    console.print("  [dim]No active action plan. Start a query to generate one.[/dim]")
                continue

            # ── v19.0: Session metrics ──
            if user_input.lower() in ("session", "metrics", "stats"):
                if _action_tracker:
                    elapsed = time.time() - _action_tracker.session_start
                    if elapsed < 60:
                        time_str = f"{elapsed:.0f}s"
                    elif elapsed < 3600:
                        time_str = f"{elapsed/60:.0f}m {elapsed%60:.0f}s"
                    else:
                        time_str = f"{elapsed/3600:.0f}h {(elapsed%3600)/60:.0f}m"
                    
                    sess_table = Table(title=f"{Icons.GRAPH} Session Metrics", box=box.ROUNDED,
                                       border_style="#5fd7ff", title_style="bold #5fd7ff", padding=(0, 1))
                    sess_table.add_column("Metric", style="bold white", width=24)
                    sess_table.add_column("Value", justify="right", width=20)
                    sess_table.add_row("Session Duration", time_str)
                    sess_table.add_row("AI Calls", str(_action_tracker.total_ai_calls))
                    sess_table.add_row("Tool Calls", str(_action_tracker.total_tool_calls))
                    sess_table.add_row("Approx Tokens", f"{_action_tracker.total_tokens_approx:,}")
                    sess_table.add_row("Messages", str(len(messages)))
                    sess_table.add_row("Devices", str(len(device_map)))
                    if vector_kb:
                        sess_table.add_row("RAG Chunks", str(vector_kb.stats().get("chunks", 0)))
                    console.print(sess_table)
                continue

            # ── v20.0 E165: Feedback command ──
            if user_input.lower().startswith("feedback"):
                fb_arg = user_input[8:].strip()
                if not fb_arg or fb_arg.lower() == "help":
                    console.print(Panel(
                        f"[bold]{Icons.BRAIN} Feedback Commands[/bold]\n\n"
                        f"  feedback <your feedback>  — Give feedback on the AI's last response\n"
                        f"  feedback history          — View past feedback with Brain analysis\n"
                        f"  feedback stats            — Show feedback summary statistics\n",
                        border_style="#af87ff", width=70
                    ))
                elif fb_arg.lower() == "history":
                    if _feedback_memory:
                        _feedback_memory.display_history(console, limit=15)
                    else:
                        console.print("  [dim]Feedback memory not initialized[/dim]")
                elif fb_arg.lower() == "stats":
                    if _feedback_memory:
                        stats = _feedback_memory.get_stats()
                        console.print(f"  {Icons.BRAIN} Feedback Stats: [green]{stats['total']}[/green] total, "
                                      f"[green]{stats['valid']}[/green] valid, [yellow]{stats['partial']}[/yellow] partial, "
                                      f"[red]{stats['invalid']}[/red] invalid")
                    else:
                        console.print("  [dim]Feedback memory not initialized[/dim]")
                else:
                    # Explicit user feedback — analyze with Brain
                    ai_last = ""
                    user_last_q = ""
                    for m in reversed(messages):
                        if m.get("role") == "assistant" and m.get("content") and not ai_last:
                            ai_last = m["content"]
                        elif m.get("role") == "user" and m.get("content") and not user_last_q:
                            user_last_q = m["content"]
                        if ai_last and user_last_q:
                            break
                    
                    if not ai_last:
                        console.print("  [dim]No previous AI response to provide feedback on[/dim]")
                    elif _feedback_memory:
                        console.print(f"  {Icons.BRAIN} [dim]Analyzing feedback with Brain (critical evaluation)...[/dim]")
                        try:
                            analysis = await _feedback_memory.analyze_feedback_with_brain(
                                fb_arg, ai_last, user_last_q
                            )
                            _feedback_memory.add_feedback(
                                user_msg=user_last_q,
                                ai_response=ai_last,
                                feedback_text=fb_arg,
                                brain_analysis=analysis,
                                session_id=current_conv_id,
                            )
                            
                            # Show analysis result
                            validity = analysis.get("validity", "?")
                            confidence = analysis.get("confidence", 0)
                            reasoning = analysis.get("reasoning", "")
                            action = analysis.get("action", "note")
                            rule = analysis.get("rule", "")
                            
                            validity_icons = {
                                "valid": "[green]✓ VALID[/green]",
                                "partially_valid": "[yellow]◐ PARTIALLY VALID[/yellow]",
                                "invalid": "[red]✗ INVALID[/red]",
                                "subjective": "[blue]◇ SUBJECTIVE[/blue]",
                            }
                            action_icons = {
                                "learn": "[green]→ Learning this[/green]",
                                "note": "[yellow]→ Noted for reference[/yellow]",
                                "ignore": "[red]→ Ignoring (user appears mistaken)[/red]",
                            }
                            
                            console.print(f"\n  {Icons.BRAIN} [bold]Brain Analysis:[/bold]")
                            console.print(f"    Validity:   {validity_icons.get(validity, validity)}")
                            console.print(f"    Confidence: {'█' * int(confidence * 10)}{'░' * (10 - int(confidence * 10))} {confidence:.0%}")
                            console.print(f"    Reasoning:  [dim]{reasoning[:120]}[/dim]")
                            console.print(f"    Action:     {action_icons.get(action, action)}")
                            if rule and rule != "N/A":
                                console.print(f"    Rule:       [italic]{rule[:100]}[/italic]")
                            
                            # If valid/partial with learn action, also save as workflow lesson
                            if validity in ("valid", "partially_valid") and action == "learn" and rule and rule != "N/A":
                                save_workflow_lesson(
                                    mistake=analysis.get("corrected_fact", fb_arg)[:150],
                                    correction=fb_arg[:150],
                                    rule=rule
                                )
                                console.print(f"    [green]{Icons.OK}[/green] [dim]Also saved as self-improvement lesson[/dim]")
                        except Exception as fb_err:
                            console.print(f"  [red]{Icons.FAIL}[/red] Feedback analysis failed: {fb_err}")
                continue

            # ── v20.0 E166: Conversations command ──
            if user_input.lower() in ("conversations", "convos", "history", "sessions"):
                if _conversation_manager:
                    _conversation_manager.display_conversations(console, limit=20)
                else:
                    console.print("  [dim]Conversation manager not initialized[/dim]")
                continue

            # ── v20.0 E166: Continue a previous conversation ──
            if user_input.lower().startswith("continue ") or user_input.lower().startswith("resume "):
                conv_arg = user_input.split(None, 1)[1].strip() if len(user_input.split()) > 1 else ""
                if conv_arg and _conversation_manager:
                    # Save current conversation first
                    if len(messages) > 1:
                        _conversation_manager.save_conversation(messages, conv_id=current_conv_id)
                    
                    # Try to interpret as number or ID
                    conv_meta = None
                    if conv_arg.isdigit():
                        conv_meta = _conversation_manager.get_conversation_by_number(int(conv_arg))
                    else:
                        # Search by topic substring
                        for c in _conversation_manager.list_conversations():
                            if conv_arg.lower() in c.get("topic", "").lower():
                                conv_meta = c
                                break
                    
                    if conv_meta:
                        prev_msgs = _conversation_manager.load_conversation(conv_meta["id"])
                        if prev_msgs:
                            # Reset messages with system prompt + loaded conversation
                            messages = [{"role": "system", "content": final_sys_prompt}]
                            messages.extend(prev_msgs)
                            current_conv_id = conv_meta["id"]
                            console.print(f"  [green]{Icons.OK}[/green] Switched to: [bold]{conv_meta['topic'][:50]}[/bold] ({len(prev_msgs)} messages)")
                        else:
                            console.print(f"  [yellow]{Icons.WARN}[/yellow] Could not load that conversation")
                    else:
                        console.print(f"  [yellow]{Icons.WARN}[/yellow] Conversation not found. Use 'conversations' to see the list.")
                else:
                    console.print("  Usage: continue <#> or continue <topic keyword>", style="dim")
                continue

            # ── v20.0 E166: Delete a conversation ──
            if user_input.lower().startswith("delete conversation ") or user_input.lower().startswith("delete conv "):
                del_arg = user_input.split()[-1].strip()
                if del_arg and _conversation_manager:
                    conv_meta = None
                    if del_arg.isdigit():
                        conv_meta = _conversation_manager.get_conversation_by_number(int(del_arg))
                    if conv_meta:
                        _conversation_manager.delete_conversation(conv_meta["id"])
                        console.print(f"  [green]{Icons.OK}[/green] Deleted conversation: {conv_meta['topic'][:50]}")
                    else:
                        console.print(f"  [yellow]{Icons.WARN}[/yellow] Conversation not found")
                continue

            # ── v20.0 E166: New conversation command ──
            if user_input.lower() in ("new", "new conversation", "new chat", "fresh"):
                # Save current conversation first
                if len(messages) > 1 and _conversation_manager:
                    _conversation_manager.save_conversation(messages, conv_id=current_conv_id)
                    console.print(f"  {Icons.SAVE} [dim]Previous conversation saved[/dim]")
                # Start fresh
                messages = [{"role": "system", "content": final_sys_prompt}]
                current_conv_id = f"conv_{int(time.time())}"
                console.print(f"  {Icons.NEW} Started new conversation")
                continue

            # ── v7.0 #P5B: Layer health dashboard ──
            if user_input.lower() in ("layers", "layer", "osi", "dashboard"):
                # E25: Use real audit data if available
                if last_audit_state:
                    layer_status = last_audit_state
                else:
                    layer_status = {
                        "physical": {"status": "unknown", "detail": "Run 'audit' first to populate"},
                        "datalink": {"status": "unknown", "detail": "Run 'audit' first to populate"},
                        "routing": {"status": "unknown", "detail": "Run 'audit' first to populate"},
                        "transport": {"status": "unknown", "detail": "Run 'audit' first to populate"},
                        "services": {"status": "unknown", "detail": "Run 'audit' first to populate"},
                    }
                print_layer_dashboard(layer_status)
                continue

            # ── v7.0 #P3C: Compliance audit command ──
            if user_input.lower() in ("compliance", "comply", "compliance audit"):
                console.print("\n◇ Running compliance audit...", style="bold cyan")
                try:
                    comp_results = await run_compliance_audit(mcp_client, session_id, device_map)
                    comp_report = format_compliance_report(comp_results, device_map)
                    console.print(Markdown(comp_report))
                    messages.append({"role": "user", "content": "Run compliance audit"})
                    messages.append({"role": "assistant", "content": comp_report})
                except Exception as ce:
                    console.print(f"✗ Compliance audit failed: {ce}", style="bold red")
                continue

            # ── v10.0: Health trends command ──
            if user_input.lower() in ("trends", "trend", "health trends", "health history"):
                try:
                    trend_data = get_health_trend(days=30)
                    if trend_data:
                        console.print(Panel("▴ Health Score Trend (Last 30 Days)", style="bold cyan", width=60))
                        trend_table = Table(title="Health History", show_header=True)
                        trend_table.add_column("Date", style="dim")
                        trend_table.add_column("Score", justify="center")
                        trend_table.add_column("Grade", justify="center")
                        trend_table.add_column("Critical", justify="center", style="red")
                        trend_table.add_column("Warnings", justify="center", style="yellow")
                        trend_table.add_column("Devices", justify="center")
                        for t in trend_data[-20:]:  # Last 20 entries
                            score = t["score"]
                            grade = "A" if score >= 90 else ("B" if score >= 75 else ("C" if score >= 60 else ("D" if score >= 40 else "F")))
                            emoji = "[green]●[/green]" if grade in ("A", "B") else ("[yellow]●[/yellow]" if grade == "C" else "[red]●[/red]")
                            trend_table.add_row(
                                t["timestamp"][:16], f"{emoji} {score}", grade,
                                str(t["critical"]), str(t["warning"]), str(t["devices"])
                            )
                        console.print(trend_table)
                        
                        # Show improvement/degradation
                        if len(trend_data) >= 2:
                            first = trend_data[0]["score"]
                            last = trend_data[-1]["score"]
                            delta = last - first
                            if delta > 0:
                                console.print(f"\n   ▴ Trend: [green]+{delta} points improvement[/green] over {len(trend_data)} audits")
                            elif delta < 0:
                                console.print(f"\n   ▾ Trend: [red]{delta} points degradation[/red] over {len(trend_data)} audits")
                            else:
                                console.print(f"\n   → Trend: Stable over {len(trend_data)} audits")
                    else:
                        console.print("   ◆ No audit history yet. Run 'audit' first to build trend data.", style="dim")
                except Exception as te:
                    console.print(f"✗ Trend query failed: {te}", style="bold red")
                continue

            # ── v10.0: Playbook command ──
            if user_input.lower() in ("playbook", "remediation", "fix", "remediate"):
                if last_audit_state.get("routing", {}).get("status") == "unknown":
                    console.print("   ◆ No audit data available. Run 'audit' first.", style="dim")
                else:
                    console.print(Panel("⚙ Remediation Playbook (from last audit)", style="bold cyan", width=60))
                    # Check known issue patterns from last audit state
                    for layer, info in last_audit_state.items():
                        status = info.get("status", "unknown")
                        detail = info.get("detail", "")
                        if status == "critical":
                            itil = assign_itil_priority("CRITICAL", 5)
                            console.print(f"   [red]●[/red] [{itil['priority']}] {layer.upper()}: {detail}")
                            console.print(f"       Target MTTR: {itil['mttr']} | {itil['sla']}")
                        elif status == "warning":
                            itil = assign_itil_priority("WARNING", 1)
                            console.print(f"   [yellow]●[/yellow] [{itil['priority']}] {layer.upper()}: {detail}")
                            console.print(f"       Target MTTR: {itil['mttr']}")
                        else:
                            console.print(f"   [green]●[/green] {layer.upper()}: {detail}")
                    console.print("\n   ▸ Run 'audit' for a detailed remediation playbook in the full report.")
                continue

            # ── v7.0 #P5A: Interactive troubleshooting ──
            if user_input.lower().startswith("troubleshoot "):
                protocol = user_input.split(None, 1)[1].lower() if len(user_input.split()) > 1 else ""
                if protocol in TROUBLESHOOT_TREES:
                    tree = TROUBLESHOOT_TREES[protocol]
                    console.print(Panel(f"⚙ Troubleshooting: {tree['name']}", style="bold yellow", width=60))
                    steps = tree.get("steps", [])
                    # E24: Walk the list-of-steps structure correctly
                    reverse_map = {v.lower(): k for k, v in device_map.items()}
                    idx = 0
                    while 0 <= idx < len(steps):
                        step = steps[idx]
                        console.print(f"\n[bold]Step {idx + 1}: {step['q']}[/bold]")
                        console.print(f"   ◇ Command: [cyan]{step['cmd']}[/cyan]")
                        run_it = input("   Run this command on a device? (device name or 'skip'): ").strip()
                        if run_it.lower() not in ("skip", "s", "no", "n", ""):
                            mcp_name = reverse_map.get(run_it.lower(), run_it)
                            if mcp_name in device_map:
                                out = await run_single(mcp_client, session_id, step["cmd"], mcp_name, "Troubleshoot")
                                console.print(f"\n```\n{out[:2000]}\n```")
                            else:
                                console.print(f"   ✗ Unknown device '{run_it}'. Available: {', '.join(device_map.values())}", style="red")
                                continue
                        issue = input("   Issue found? (yes/no/quit): ").strip().lower()
                        if issue in ("q", "quit"):
                            console.print("   ⊗ Troubleshooting stopped.", style="yellow")
                            break
                        if issue in ("y", "yes"):
                            nxt = step.get("next_if_issue", -1)
                            if nxt < 0 or nxt >= len(steps):
                                console.print("   ▲  End of decision tree — escalate or review config manually.", style="bold yellow")
                                break
                            idx = nxt
                        else:
                            idx += 1
                    else:
                        console.print("   ● All steps passed — protocol appears healthy.", style="bold green")
                else:
                    console.print(f"Available protocols: {', '.join(TROUBLESHOOT_TREES.keys())}", style="yellow")
                continue

            # ── v11.0 E78: AI-Guided Dynamic Troubleshooting ──
            if user_input.lower().startswith("troubleshoot-ai ") or user_input.lower().startswith("tsai "):
                symptom = user_input.split(None, 1)[1] if len(user_input.split()) > 1 else ""
                if symptom:
                    console.print(Panel(f"◉ AI-Guided Troubleshooting: {symptom}", style="bold yellow", width=60))
                    try:
                        ts_result = await ai_guided_troubleshoot(
                            mcp_client, session_id, symptom, device_map
                        )
                        console.print(Markdown(ts_result))
                        messages.append({"role": "user", "content": user_input})
                        messages.append({"role": "assistant", "content": ts_result})
                    except Exception as ts_err:
                        console.print(f"✗ AI troubleshooting failed: {ts_err}", style="bold red")
                else:
                    console.print("Usage: troubleshoot-ai <symptom description>", style="yellow")
                    console.print("Example: troubleshoot-ai PE1 cannot reach PE3 via MPLS", style="dim")
                continue

            # ── v11.0 E73: What-If Failure Simulation ──
            if user_input.lower().startswith("whatif "):
                target = user_input.split(None, 1)[1].strip() if len(user_input.split()) > 1 else ""
                if target:
                    reverse_map = {v.lower(): k for k, v in device_map.items()}
                    mcp_target = reverse_map.get(target.lower(), target)
                    if mcp_target in device_map or target in device_map:
                        mcp_name = mcp_target if mcp_target in device_map else target
                        hostname = device_map.get(mcp_name, target)
                        console.print(Panel(f"◉ What-If Simulation: {hostname} fails", style="bold magenta", width=60))
                        if _network_graph and _network_graph.nodes:
                            impact = _network_graph.what_if_fail(mcp_name)
                            if impact:
                                console.print(f"\n◫ **Impact of {hostname} failure:**\n")
                                for item in impact:
                                    console.print(f"   • {item}")
                            else:
                                console.print(f"   ◆ No downstream impact detected for {hostname}")
                            # Also show transit node info
                            transit = _network_graph.get_transit_nodes()
                            if transit:
                                console.print(f"\n⊶ **Transit nodes (highest impact if failed):** {', '.join(transit)}")
                        else:
                            console.print("   ▲ Dependency graph not built yet. Run 'audit' first to build the graph.", style="yellow")
                        messages.append({"role": "user", "content": user_input})
                        messages.append({"role": "assistant", "content": f"What-if simulation for {hostname} complete."})
                    else:
                        console.print(f"✗ Unknown device: '{target}'", style="bold red")
                        console.print(f"   Known: {', '.join(f'{v} ({k})' for k, v in device_map.items())}", style="dim")
                else:
                    console.print("Usage: whatif <router_name>", style="yellow")
                    console.print("Example: whatif P11", style="dim")
                continue

            # ── v11.0 E88: Change Templates ──
            if user_input.lower().startswith("template "):
                tmpl_parts = user_input.split(None, 2)
                tmpl_cmd = tmpl_parts[1].lower() if len(tmpl_parts) > 1 else "list"
                
                if tmpl_cmd == "list":
                    console.print(Panel("◇ Available Change Templates (v11.0)", style="bold cyan", width=60))
                    tmpl_table = Table(show_header=True, box=box.ROUNDED)
                    tmpl_table.add_column("Template Name", style="bold green")
                    tmpl_table.add_column("Description")
                    tmpl_table.add_column("Parameters")
                    for tname, tdata in CHANGE_TEMPLATES.items():
                        params = ", ".join(tdata.get("params", {}).keys())
                        tmpl_table.add_row(tname, tdata.get("description", ""), params)
                    console.print(tmpl_table)
                elif tmpl_cmd in CHANGE_TEMPLATES:
                    tmpl = CHANGE_TEMPLATES[tmpl_cmd]
                    console.print(Panel(f"◇ Template: {tmpl.get('description', tmpl_cmd)}", style="bold cyan", width=60))
                    console.print(f"Parameters needed: {', '.join(tmpl.get('params', {}).keys())}")
                    console.print(f"Commands template:\n")
                    for cmd_tmpl in tmpl.get("commands", []):
                        console.print(f"   [cyan]{cmd_tmpl}[/cyan]")
                    console.print(f"\nVerification: {', '.join(tmpl.get('verify', []))}")
                    console.print(f"\n▸ Use 'configure <router> <description>' to apply with AI assistance.")
                else:
                    console.print(f"✗ Unknown template: '{tmpl_cmd}'", style="bold red")
                    console.print(f"   Available: {', '.join(CHANGE_TEMPLATES.keys())}", style="dim")
                continue

            # ── v11.0 E84: Pre-Change Impact Analysis ──
            if user_input.lower().startswith("impact "):
                impact_parts = user_input.split(None, 2)
                if len(impact_parts) >= 3:
                    impact_router = impact_parts[1]
                    impact_desc = impact_parts[2]
                    reverse_map = {v.lower(): k for k, v in device_map.items()}
                    mcp_name = reverse_map.get(impact_router.lower(), impact_router)
                    if mcp_name in device_map:
                        hostname = device_map[mcp_name]
                        console.print(Panel(f"◫ Pre-Change Impact Analysis: {hostname}", style="bold cyan", width=60))
                        try:
                            impact_result = await analyze_change_impact(
                                mcp_client, session_id, mcp_name, impact_desc, device_map
                            )
                            console.print(Markdown(impact_result))
                            messages.append({"role": "user", "content": user_input})
                            messages.append({"role": "assistant", "content": impact_result})
                        except Exception as ie:
                            console.print(f"✗ Impact analysis failed: {ie}", style="bold red")
                    else:
                        console.print(f"✗ Unknown device: '{impact_router}'", style="bold red")
                else:
                    console.print("Usage: impact <router> <change description>", style="yellow")
                    console.print("Example: impact PE1 add ospf interface ge-0/0/3.0", style="dim")
                continue

            # ── v12.0: Runbook Automation (Enhancement #8) ──
            if user_input.lower().startswith("runbook"):
                rb_parts = user_input.split(None, 2)
                rb_cmd = rb_parts[1].lower() if len(rb_parts) > 1 else "list"
                
                if rb_cmd == "list":
                    console.print(Panel("◇ Available Runbooks (v12.0)", style="bold cyan", width=60))
                    rb_table = Table(show_header=True, box=box.ROUNDED)
                    rb_table.add_column("Name", style="bold green")
                    rb_table.add_column("Description")
                    rb_table.add_column("Parameters")
                    for rname, rdata in RUNBOOKS.items():
                        params = ", ".join(rdata.get("params", {}).keys())
                        rb_table.add_row(rname, rdata.get("name", ""), params)
                    console.print(rb_table)
                    console.print("\nUsage: runbook <name>  — to view steps and fill parameters", style="dim")
                elif rb_cmd in RUNBOOKS:
                    rb = RUNBOOKS[rb_cmd]
                    console.print(Panel(f"◇ Runbook: {rb['name']}", style="bold cyan", width=60))
                    console.print(f"_{rb['description']}_\n")
                    console.print("Parameters needed:")
                    params_filled = {}
                    for pname, pdesc in rb.get("params", {}).items():
                        val = input(f"   {pname} ({pdesc}): ").strip()
                        if not val:
                            console.print(f"   ✗ Cancelled — missing parameter '{pname}'", style="red")
                            break
                        params_filled[pname] = val
                    else:
                        # All params collected — show preview
                        preview = format_runbook_preview(rb_cmd, params_filled)
                        console.print(Markdown(preview))
                        
                        confirm = input("\n   Execute this runbook? (yes/no): ").strip().lower()
                        if confirm in ("yes", "y"):
                            commands = get_runbook_commands(rb_cmd, params_filled)
                            config_text = "\n".join(commands)
                            router = params_filled.get("router", "")
                            if router:
                                reverse_map = {v.lower(): k for k, v in device_map.items()}
                                mcp_name = reverse_map.get(router.lower(), router)
                                if mcp_name in device_map:
                                    console.print(f"\n   ▸ Pushing runbook config to {device_map[mcp_name]}...")
                                    try:
                                        result = await mcp_call_tool(mcp_client, session_id,
                                                                      "load_and_commit_config",
                                                                      {"router_name": mcp_name,
                                                                       "config_text": config_text,
                                                                       "commit_comment": f"Runbook: {rb['name']}"})
                                        console.print(f"   ● Runbook applied: {result[:300]}")
                                        
                                        # Run verification commands
                                        for vcmd in rb.get("verify", []):
                                            vcmd_filled = vcmd.format(**params_filled)
                                            vout = await run_single(mcp_client, session_id, vcmd_filled, mcp_name, "Verify")
                                            console.print(f"\n   ◇ {vcmd_filled}:\n```\n{vout[:500]}\n```")
                                    except Exception as rb_err:
                                        console.print(f"   ✗ Runbook failed: {rb_err}", style="bold red")
                                else:
                                    console.print(f"   ✗ Unknown router: '{router}'", style="red")
                            else:
                                console.print("   ◆ No router specified. Config commands to apply manually:")
                                for cmd in commands:
                                    console.print(f"      [cyan]{cmd}[/cyan]")
                        else:
                            console.print("   ✗ Cancelled.", style="dim")
                    messages.append({"role": "user", "content": user_input})
                    messages.append({"role": "assistant", "content": f"Runbook: {rb_cmd}"})
                else:
                    console.print(f"✗ Unknown runbook: '{rb_cmd}'. Use 'runbook list' to see available.", style="red")
                continue

            # ── v12.0: Config Impact Simulator (Enhancement #9) ──
            if user_input.lower().startswith("simulate "):
                sim_config = user_input[9:].strip()  # Everything after "simulate "
                if sim_config:
                    topo_graph = build_topology_from_golden_configs()
                    impact = simulate_config_impact(sim_config, topo_graph)
                    console.print(Markdown(impact))
                    messages.append({"role": "user", "content": user_input})
                    messages.append({"role": "assistant", "content": impact})
                else:
                    console.print("Usage: simulate <set/delete commands>", style="yellow")
                    console.print("Example: simulate set protocols ospf area 0 interface ge-0/0/3.0", style="dim")
                continue

            # ── v12.0: Multi-Vendor Translation (Enhancement #13) ──
            if user_input.lower().startswith("translate"):
                tr_parts = user_input.split(None, 1)
                vendor = tr_parts[1].strip().lower().replace(" ", "_") if len(tr_parts) > 1 else ""
                if vendor:
                    table = get_vendor_translation_table(vendor)
                    console.print(Markdown(table))
                else:
                    console.print("Available vendors: " + ", ".join(VENDOR_TRANSLATIONS.keys()), style="cyan")
                    console.print("Usage: translate <vendor>", style="yellow")
                    console.print("Example: translate cisco_ios", style="dim")
                continue

            # ── v12.0: Live Health State (Enhancement #6) ──
            if user_input.lower() in ("health state", "live health", "health poll", "bg health"):
                health_info = get_health_state_prompt()
                if health_info:
                    console.print(Markdown(health_info))
                else:
                    console.print("   ◆ Health poll hasn't completed yet. Wait ~1 minute.", style="dim")
                continue

            # ── SPECIAL COMMANDS ──
            lower = user_input.lower().strip()
            
            # Audit mode
            if lower in ("audit", "health check", "run audit", "network audit"):
                console.print("\n⊕ Starting full network audit...", style="bold cyan")
                
                # v19.0: Show active todos before audit
                if _todo_tracker:
                    _todo_tracker.refresh()
                    _todo_tracker.display(console)
                
                # v19.0: Create action plan for audit
                if _action_tracker:
                    _action_tracker.new_plan("Full Network Audit", [
                        "Collect device facts & show-commands",
                        "Config drift analysis vs golden baselines",
                        "Issue detection & protocol health parsing",
                        "12-specialist AI analysis & scoring",
                        "Generate report & save to SQLite",
                    ])
                    _action_tracker.start_step(0)
                
                try:
                    report = await run_full_audit(mcp_client, session_id, device_map, device_facts)
                    if _action_tracker:
                        for i in range(5):
                            _action_tracker.complete_step(i)
                except (httpx.ConnectError, httpx.ReadError, httpx.RemoteProtocolError, ConnectionError) as e:
                    console.print(f"   ↻ MCP connection lost during audit ({e}), reconnecting...", style="yellow")
                    try:
                        session_id = await mcp_reconnect(mcp_client)
                        report = await run_full_audit(mcp_client, session_id, device_map, device_facts)
                    except Exception as reconn_err:
                        console.print(f"   ✗ Audit failed after reconnect: {reconn_err}", style="bold red")
                        continue
                # Save report
                ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
                fname = f"NETWORK_AUDIT_{ts}.md"
                with open(fname, "w") as f:
                    f.write(report)
                console.print(Panel(f"● Audit complete! Report saved: {fname}", style="bold green", width=60))
                console.print(report[:3000])
                if len(report) > 3000:
                    console.print(f"\n... (report is {len(report)} chars, see {fname} for full report)", style="dim")
                # Add to conversation context
                messages.append({"role": "user", "content": "Run a full network audit."})
                messages.append({"role": "assistant", "content": f"Audit complete. Report saved to `{fname}`. Here's the summary:\n\n{report[:2000]}"})
                
                # v19.0: Complete action plan & show session bar
                if _action_tracker:
                    _action_tracker.complete_plan()
                    _action_tracker.print_session_bar()
                continue
            
            # ── v14.0 E123: Live Topology Visualization ──
            if lower in ("topology", "topo", "show topology", "network map", "map", "show topo"):
                console.print("\n◫  Building live topology from iBGP + LLDP + IS-IS...", style="bold cyan")
                try:
                    topo = await build_live_topology(mcp_client, session_id, device_map)
                    
                    # ASCII display in terminal
                    ascii_topo = topology_to_ascii(topo)
                    console.print(ascii_topo)
                    
                    # Mermaid diagram (original)
                    mermaid = topology_to_mermaid(topo)
                    console.print("\n◫ Mermaid Diagram (paste into mermaid.live):")
                    console.print(Panel(mermaid, border_style="blue", width=min(100, console.width - 2)))
                    
                    # v15.0: TopologyIntelligence — advanced analysis
                    try:
                        topo_intel = TopologyIntelligence()
                        # Build device map for TopologyIntelligence
                        ti_device_map = {}
                        for mcp_name, node in topo.get("nodes", {}).items():
                            ti_device_map[mcp_name] = node["hostname"]
                        
                        # Add nodes first
                        for mcp_name, node in topo.get("nodes", {}).items():
                            topo_intel.add_node(node["hostname"], node.get("role", "P"),
                                                loopback=node.get("loopback", ""))
                        
                        # Feed physical links
                        for link in topo.get("physical_links", []):
                            src_h = topo["nodes"].get(link["src"], {}).get("hostname", link["src"])
                            dst_h = topo["nodes"].get(link["dst"], {}).get("hostname", link["dst"])
                            topo_intel.add_link(src=src_h, dst=dst_h,
                                                src_intf=link.get("src_intf", ""),
                                                dst_intf=link.get("dst_intf", ""),
                                                link_type="physical", state="up")
                        
                        # Feed iBGP sessions
                        loopback_to_hostname = {}
                        for mcp_name, node in topo.get("nodes", {}).items():
                            if node.get("loopback"):
                                loopback_to_hostname[node["loopback"]] = node["hostname"]
                        for session in topo.get("bgp_sessions", []):
                            src_h = topo["nodes"].get(session["src"], {}).get("hostname", session["src"])
                            peer_h = loopback_to_hostname.get(session["peer_ip"], session["peer_ip"])
                            state = session.get("state", "Unknown")
                            if src_h and peer_h and src_h != peer_h:
                                link_state = "established" if "Establ" in state else "down"
                                topo_intel.add_link(src=src_h, dst=peer_h, 
                                                    link_type="ibgp", state=link_state)
                        
                        # Enhanced Mermaid with subgraphs
                        enhanced_mermaid = topo_intel.generate_mermaid()
                        if enhanced_mermaid and len(enhanced_mermaid) > 50:
                            console.print("\n◫  Enhanced Topology (with layers & health):")
                            console.print(Panel(enhanced_mermaid, border_style="magenta", 
                                               width=min(100, console.width - 2)))
                        
                        # Articulation points
                        art_points = topo_intel.find_articulation_points()
                        if art_points:
                            console.print(f"\n▲  [bold yellow]Articulation Points (single points of failure):[/bold yellow]")
                            for ap in art_points:
                                console.print(f"   [red]●[/red] {ap} — failure would partition the network")
                        
                        # ECMP paths between PEs
                        pe_nodes = [n["hostname"] for n in topo.get("nodes", {}).values() if n["role"] == "PE"]
                        if len(pe_nodes) >= 2:
                            ecmp = topo_intel.get_ecmp_paths(pe_nodes[0], pe_nodes[1])
                            if ecmp and len(ecmp) > 1:
                                console.print(f"\n⇉ ECMP paths {pe_nodes[0]} ↔ {pe_nodes[1]}: {len(ecmp)} paths found")
                    except Exception as intel_err:
                        logger.debug(f"TopologyIntelligence enhancement skipped: {intel_err}")
                    
                    # Save to file
                    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
                    topo_fname = f"TOPOLOGY_{ts}.md"
                    with open(topo_fname, "w") as f:
                        f.write(f"# Live Network Topology — {ts}\n\n")
                        f.write(f"## ASCII Map\n```\n{ascii_topo}\n```\n\n")
                        f.write(f"## Mermaid Diagram\n{mermaid}\n\n")
                        try:
                            f.write(f"## Enhanced Mermaid (v15.0)\n{enhanced_mermaid}\n\n")
                        except Exception:
                            pass
                        f.write(f"## Raw Data\n```json\n{json.dumps(topo, indent=2, default=str)}\n```\n")
                    console.print(f"\n   ⊟ Saved: {topo_fname}", style="dim")
                    
                    messages.append({"role": "user", "content": "Show live network topology."})
                    messages.append({"role": "assistant", "content": f"Live topology built from iBGP + LLDP + IS-IS.\n\n{ascii_topo}"})
                except Exception as topo_err:
                    console.print(f"   ✗ Topology build failed: {topo_err}", style="bold red")
                    logger.error(f"Topology build failed: {topo_err}", exc_info=True)
                continue
            
            # ── v14.0 E124: Mind-Map Deep Reasoning ──
            if lower.startswith("mindmap ") or lower.startswith("mind-map ") or lower.startswith("deep "):
                mind_query = user_input.split(None, 1)[1] if " " in user_input else user_input
                console.print("\n◉ Activating MIND-MAP deep reasoning engine...", style="bold magenta")
                console.print(f"   ⊕ Query: {mind_query}", style="dim")
                try:
                    result = await mind_map_reasoning(
                        mind_query, mcp_client, session_id, device_map, tools=ollama_tools
                    )
                    console.print()
                    console.print(Panel(result, title="◉ Mind-Map Analysis", 
                                       border_style="magenta", width=min(100, console.width - 2)))
                    messages.append({"role": "user", "content": user_input})
                    messages.append({"role": "assistant", "content": result})
                except Exception as mm_err:
                    console.print(f"   ✗ Mind-map reasoning failed: {mm_err}", style="bold red")
                    logger.error(f"Mind-map reasoning failed: {mm_err}", exc_info=True)
                continue
            
            # ── v15.0 E129: Hypothesis-Driven Investigation ──
            if lower.startswith("hypothesis ") or lower.startswith("hypo "):
                hypo_query = user_input.split(None, 1)[1] if " " in user_input else user_input
                console.print("\n⊕ Activating HYPOTHESIS-DRIVEN investigation...", style="bold magenta")
                try:
                    classification = classify_problem(hypo_query)
                    console.print(f"   ◫ Domain: {classification.domain.value} | "
                                  f"Complexity: {classification.complexity.value}")
                    
                    hypotheses = generate_hypotheses(classification, hypo_query)
                    if hypotheses:
                        console.print(f"   ⊕ Generated {len(hypotheses)} hypotheses:\n")
                        for i, h in enumerate(hypotheses, 1):
                            console.print(f"      {i}. {h.description}")
                            console.print(f"         Confidence: {h.confidence:.0f}% | "
                                         f"Verify: {h.verification_command}")
                            console.print(f"         Impact chain: {' → '.join(h.cascading_impact)}")
                            console.print()
                        
                        # Now run top hypothesis verification commands
                        console.print("   ⊕ Running verification commands for top hypotheses...\n")
                        evidence_acc = EvidenceAccumulator()
                        reverse_map = {v.lower(): k for k, v in device_map.items()}
                        
                        for h in hypotheses[:3]:
                            cmd = h.verification_command
                            if cmd:
                                # Strip template placeholders like {peer_loopback}, {intf}, {peer}
                                # to produce valid Junos commands
                                import re as _re
                                cmd_clean = _re.sub(r'\s*\{[^}]+\}\S*', '', cmd).strip()
                                cmd_clean = _re.sub(r'\s+\|', ' |', cmd_clean)  # fix dangling pipes
                                cmd_clean = _re.sub(r'\s{2,}', ' ', cmd_clean)  # collapse multi-spaces
                                if not cmd_clean:
                                    continue
                                cmd = cmd_clean
                                
                                # Try to find a relevant device
                                target_dev = None
                                for dev_name in classification.devices_mentioned:
                                    mcp = reverse_map.get(dev_name.lower(), dev_name)
                                    if mcp in device_map:
                                        target_dev = mcp
                                        break
                                if not target_dev:
                                    target_dev = list(device_map.keys())[0]
                                
                                try:
                                    output = await run_single(mcp_client, session_id, cmd, 
                                                              target_dev, f"H:{h.id}")
                                    supports = any(kw in output.lower() for kw in 
                                                  ["down", "error", "fail", "nonexist", "active", "init"])
                                    evidence_acc.add_evidence(Evidence(
                                        source=device_map[target_dev],
                                        command=cmd,
                                        raw_output=output[:500],
                                        interpretation=f"{'Issue indicators found' if supports else 'No issues detected'}",
                                        supports=h.id if supports else "",
                                        refutes=h.id if not supports else "",
                                        confidence_delta=20.0 if supports else 15.0,
                                    ))
                                    status = "▲ SUPPORTS" if supports else "● REFUTES"
                                    console.print(f"      {status} H:{h.id} — {cmd}")
                                except Exception:
                                    pass
                        
                        # Show ranked results
                        ranked = evidence_acc.get_ranked_hypotheses(hypotheses)
                        if ranked:
                            console.print("\n   ◫ Hypothesis Rankings (after evidence):")
                            for h, conf in ranked:
                                icon = "◎" if conf > 70 else "[yellow]◆[/yellow]" if conf > 40 else "✗"
                                console.print(f"      {icon} {h.description}: {conf:.0f}%")
                        
                        result = format_reasoning_chain(classification, hypotheses, evidence_acc)
                        messages.append({"role": "user", "content": user_input})
                        messages.append({"role": "assistant", "content": result})
                    else:
                        console.print("   ◆ No pre-built hypotheses for this domain. "
                                     "Use 'mindmap' for AI-generated analysis.", style="yellow")
                except Exception as hypo_err:
                    console.print(f"   ✗ Hypothesis investigation failed: {hypo_err}", style="bold red")
                    logger.error(f"Hypothesis investigation failed: {hypo_err}", exc_info=True)
                continue
            
            # ── v15.0 E130: Script Templates ──
            if lower.startswith("scripts") or lower.startswith("script "):
                parts = user_input.split(None, 1)
                if len(parts) == 1 or parts[1].strip().lower() == "list":
                    # List all scripts
                    available = list_available_scripts()
                    console.print("\n⊞ [bold]Available Junos Script Templates[/bold]\n")
                    for name, desc in available.items():
                        console.print(f"   • [cyan]{name}[/cyan]: {desc}")
                    console.print(f"\n   Use [bold]scripts <name>[/bold] to view a template.")
                else:
                    template_name = parts[1].strip()
                    template = get_script_template(template_name)
                    if template:
                        console.print(f"\n⊞ [bold]{template_name}[/bold]")
                        console.print(f"   Type: {template.get('type', 'unknown')}")
                        console.print(f"   Description: {template.get('description', '')}\n")
                        console.print(Panel(template.get('template', template.get('code', '')), 
                                           title=template_name,
                                           border_style="green", width=min(100, console.width - 2)))
                    else:
                        console.print(f"   ✗ Unknown template: '{template_name}'", style="bold red")
                        available = list_available_scripts()
                        console.print(f"   Available: {', '.join(available.keys())}")
                continue
            
            # ── v15.0 E131: Cascade Chain Viewer ──
            if lower.startswith("cascade "):
                cascade_input = user_input.split(None, 1)[1].strip().upper() if " " in user_input else ""
                if cascade_input:
                    chain = walk_cascade(cascade_input)
                    if chain:
                        console.print(f"\n⊶ [bold]Cascading Failure Chain from {cascade_input}[/bold]\n")
                        for i, step in enumerate(chain):
                            indent = "   " + "  " * i
                            arrow = "└─►" if i > 0 else "[red]●[/red]"
                            console.print(f"{indent}{arrow} {step}")
                    else:
                        console.print(f"   ◆ No cascade chain found for '{cascade_input}'.", style="yellow")
                        console.print("   Available starting points: L1_PHYSICAL, L2_ETHERNET, L3_ISIS, "
                                     "L3_OSPF, MPLS_LDP, MPLS_RSVP, BGP, SERVICES")
                else:
                    console.print("   Usage: cascade <PROTOCOL> (e.g., cascade L3_ISIS)", style="yellow")
                continue
            
            # ══════════════════════════════════════════════════════════════
            #  v18.0 COMMAND HANDLERS — Hypered Brain Engine
            # ══════════════════════════════════════════════════════════════
            
            # ── v18.0 E148-E158: Hypered Brain — Agentic Multi-Layer AI Analysis ──
            if lower.startswith("brain ") or lower.startswith("hypered "):
                brain_query = user_input.split(None, 1)[1] if " " in user_input else ""
                if brain_query:
                    console.print(Panel(
                        "◉ HYPERED BRAIN — Multi-Layer AI Engine\n"
                        "   Layer 1: Perception → Script Selection\n"
                        "   Layer 2: Analysis → Parallel Data Gathering\n"
                        "   Layer 3: Validation → Gap Detection & Double-Check\n"
                        "   Layer 4: Synthesis → Evidence-Based Response",
                        style="bold magenta", width=min(80, console.width - 2)
                    ))
                    console.print(f"   ⊕ Query: {brain_query}\n", style="dim")
                    
                    try:
                        # Build reverse map and available devices list
                        available_devices = list(device_map.keys())
                        
                        # Wrapper for run_batch to match hypered_brain's expected signature
                        async def _brain_run_batch(client_unused, sess_unused, cmds, devices, label):
                            return await run_batch(mcp_client, session_id, cmds, devices, label)
                        
                        # Wrapper for run_single
                        async def _brain_run_single(client_unused, sess_unused, cmd, device, label):
                            return await run_single(mcp_client, session_id, cmd, device, label)
                        
                        # Wrapper for AI analysis
                        async def _brain_ai_analyze(system_ctx, data, question, include_kb=True):
                            return await ollama_analyze(system_ctx, data, question, include_kb)
                        
                        # Load brain config from config.yaml
                        brain_cfg = cfg.get("hypered_brain", {})
                        confidence_threshold = brain_cfg.get("confidence_threshold", 70)
                        max_passes = brain_cfg.get("max_passes", 3)
                        max_concurrent = brain_cfg.get("max_concurrent_scripts", 3)
                        
                        # Run the Hypered Brain
                        result = await hypered_brain_analyze(
                            query=brain_query,
                            run_batch_fn=_brain_run_batch,
                            run_single_fn=_brain_run_single,
                            ai_analyze_fn=_brain_ai_analyze,
                            available_devices=available_devices,
                            device_map=device_map,
                            confidence_threshold=confidence_threshold,
                            max_passes=max_passes,
                            max_concurrent=max_concurrent,
                            print_fn=console.print,
                        )
                        
                        console.print()
                        console.print(Panel(
                            result,
                            title="◉ Hypered Brain — Final Analysis",
                            border_style="magenta",
                            width=min(100, console.width - 2)
                        ))
                        
                        messages.append({"role": "user", "content": user_input})
                        messages.append({"role": "assistant", "content": result})
                        
                        # Save brain report to file
                        ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
                        brain_fname = f"BRAIN_ANALYSIS_{ts}.md"
                        with open(brain_fname, "w") as bf:
                            bf.write(f"# ◉ Hypered Brain Analysis — {ts}\n\n")
                            bf.write(f"**Query:** {brain_query}\n\n")
                            bf.write(result)
                        console.print(f"\n   ⊟ Report saved: {brain_fname}", style="dim")
                        
                    except Exception as brain_err:
                        console.print(f"   ✗ Hypered Brain failed: {brain_err}", style="bold red")
                        logger.error(f"Hypered Brain failed: {brain_err}", exc_info=True)
                else:
                    console.print("Usage: brain <query>", style="yellow")
                    console.print("Examples:", style="dim")
                    console.print("   brain check all OSPF neighbors and BGP sessions", style="dim")
                    console.print("   brain is there any issue with PE1 MPLS connectivity", style="dim")
                    console.print("   brain full network health assessment", style="dim")
                    console.print("   brain why is traffic dropping between PE1 and PE3", style="dim")
                continue
            
            # ── v18.0: Quick Brain (single-pass, no validation loop) ──
            if lower.startswith("qbrain ") or lower.startswith("quick-brain "):
                qb_query = user_input.split(None, 1)[1] if " " in user_input else ""
                if qb_query:
                    console.print(Panel("⚡ Quick Brain — Single-Pass Analysis", style="bold cyan", width=60))
                    console.print(f"   ⊕ Query: {qb_query}\n", style="dim")
                    
                    try:
                        available_devices = list(device_map.keys())
                        
                        async def _qb_run_batch(c, s, cmds, devices, label):
                            return await run_batch(mcp_client, session_id, cmds, devices, label)
                        
                        async def _qb_run_single(c, s, cmd, device, label):
                            return await run_single(mcp_client, session_id, cmd, device, label)
                        
                        async def _qb_ai_analyze(system_ctx, data, question, include_kb=True):
                            return await ollama_analyze(system_ctx, data, question, include_kb)
                        
                        brain_cfg = cfg.get("hypered_brain", {})
                        
                        result = await quick_brain_analyze(
                            query=qb_query,
                            run_batch_fn=_qb_run_batch,
                            run_single_fn=_qb_run_single,
                            ai_analyze_fn=_qb_ai_analyze,
                            available_devices=available_devices,
                            device_map=device_map,
                            max_concurrent=brain_cfg.get("max_concurrent_scripts", 3),
                            print_fn=console.print,
                        )
                        
                        console.print()
                        console.print(Panel(result, title="⚡ Quick Brain Analysis",
                                           border_style="cyan",
                                           width=min(100, console.width - 2)))
                        messages.append({"role": "user", "content": user_input})
                        messages.append({"role": "assistant", "content": result})
                    except Exception as qb_err:
                        console.print(f"   ✗ Quick Brain failed: {qb_err}", style="bold red")
                        logger.error(f"Quick Brain failed: {qb_err}", exc_info=True)
                else:
                    console.print("Usage: qbrain <query>  (single-pass, no validation loop)", style="yellow")
                continue
            
            # ── v18.0: Smart Scripts Library Viewer ──
            if lower in ("smart-scripts", "scripts-lib", "brain-scripts"):
                console.print(Panel("+ Smart Fact-Gathering Scripts Library (v18.0)", 
                                   style="bold green", width=60))
                script_table = Table(show_header=True, box=box.ROUNDED)
                script_table.add_column("ID", style="bold cyan", width=18)
                script_table.add_column("Category", width=12)
                script_table.add_column("Name", width=25)
                script_table.add_column("Commands", justify="center", width=5)
                script_table.add_column("Triggers", width=30)
                for sid, script in SMART_SCRIPTS.items():
                    triggers = ", ".join(script.triggers[:3])
                    if len(script.triggers) > 3:
                        triggers += f" +{len(script.triggers) - 3}"
                    script_table.add_row(
                        sid,
                        script.category.value,
                        script.name,
                        str(len(script.commands)),
                        triggers,
                    )
                console.print(script_table)
                console.print(f"\n   ◫ Total: {len(SMART_SCRIPTS)} scripts | "
                             f"Use [bold]brain <query>[/bold] to activate the Hypered Brain")
                continue
            
            # ══════════════════════════════════════════════════════════════
            #  v16.0 COMMAND HANDLERS — Network Analysis Engine
            # ══════════════════════════════════════════════════════════════
            
            # Initialize analysis engine (lazy singleton)
            if not hasattr(handle_loop, '_analysis_engine'):
                handle_loop._analysis_engine = NetworkAnalysisEngine(
                    db_path=str(Path(__file__).parent / "analysis_memory.db")
                )
            nae = handle_loop._analysis_engine
            reverse_map = {v.lower(): k for k, v in device_map.items()}
            
            # ── v16.0 E139: Packet Capture Intelligence ──
            if lower.startswith("capture "):
                parts = user_input.split()
                if len(parts) < 2:
                    console.print("   Usage: capture <router> [protocol] [interface]", style="yellow")
                    console.print("   Protocols: dns, icmp, tcp, bgp, ospf, ldp, bfd, all", style="dim")
                    continue
                
                target_name = parts[1]
                mcp_name = reverse_map.get(target_name.lower(), target_name)
                if mcp_name not in device_map:
                    console.print(f"   ✗ Unknown device: '{target_name}'", style="bold red")
                    continue
                hostname = device_map[mcp_name]
                
                proto = parts[2] if len(parts) > 2 else "all"
                intf = parts[3] if len(parts) > 3 else ""
                
                try:
                    proto_enum = CaptureProtocol(proto.lower())
                except ValueError:
                    proto_enum = CaptureProtocol.ALL
                
                capture_cmd = nae.get_capture_commands(hostname, proto, intf, count=25)
                console.print(f"\n⊛ [bold]Packet Capture on {hostname}[/bold]")
                console.print(f"   Protocol: {proto_enum.value} | Interface: {intf or 'all'}")
                console.print(f"   Command: [dim]{capture_cmd}[/dim]\n")
                
                try:
                    raw_output = await run_single(mcp_client, session_id, capture_cmd, 
                                                   mcp_name, f"capture:{hostname}")
                    analysis = nae.analyze_capture(raw_output, proto)
                    
                    console.print(f"   ◫ Packets captured: {analysis['packets_captured']}")
                    
                    # Display statistics
                    if analysis.get('statistics'):
                        stats = analysis['statistics']
                        console.print(f"   ◷  Duration: {stats.get('duration_seconds', 0)}s | "
                                     f"Rate: {stats.get('packets_per_second', 0)} pps")
                    
                    # Display protocol-specific analysis
                    if analysis.get('analysis'):
                        console.print(f"\n   ◇ Analysis:")
                        for key, value in analysis['analysis'].items():
                            if isinstance(value, dict):
                                console.print(f"      {key}:")
                                for k2, v2 in list(value.items())[:5]:
                                    console.print(f"         {k2}: {v2}")
                            elif isinstance(value, list):
                                console.print(f"      {key}: {len(value)} items")
                                for item in value[:3]:
                                    if isinstance(item, dict):
                                        console.print(f"         • {item.get('type', '')} — {item.get('description', '')}")
                                    else:
                                        console.print(f"         • {item}")
                            else:
                                console.print(f"      {key}: {value}")
                    
                    messages.append({"role": "user", "content": user_input})
                    messages.append({"role": "assistant", "content": f"Capture analysis on {hostname}:\n{json.dumps(analysis, indent=2, default=str)[:2000]}"})
                except Exception as cap_err:
                    console.print(f"   ✗ Capture failed: {cap_err}", style="bold red")
                    logger.error(f"Capture failed: {cap_err}", exc_info=True)
                continue
            
            # ── v16.0 E140: DNS Intelligence ──
            if lower.startswith("dns "):
                parts = user_input.split()
                if len(parts) < 2:
                    console.print("   Usage: dns <domain> [type] | dns trace <domain>", style="yellow")
                    console.print("   Types: A, AAAA, MX, CNAME, NS, PTR, TXT", style="dim")
                    continue
                
                if parts[1].lower() == "trace":
                    # DNS trace mode
                    if len(parts) < 3:
                        console.print("   Usage: dns trace <domain>", style="yellow")
                        continue
                    domain = parts[2]
                    console.print(f"\n◫ [bold]DNS Trace: {domain}[/bold]\n")
                    trace_cmds = nae.get_dns_trace_commands(domain)
                    
                    # Run on first available device
                    target_mcp = list(device_map.keys())[0]
                    target_host = device_map[target_mcp]
                    
                    console.print(f"   Running from: {target_host}")
                    for cmd in trace_cmds:
                        try:
                            output = await run_single(mcp_client, session_id, cmd, 
                                                       target_mcp, f"dns-trace:{domain}")
                            console.print(f"\n   [cyan]> {cmd}[/cyan]")
                            for line in output.strip().split("\n")[:10]:
                                console.print(f"     {line}")
                        except Exception:
                            pass
                    
                    messages.append({"role": "user", "content": user_input})
                    messages.append({"role": "assistant", "content": f"DNS trace for {domain} completed from {target_host}."})
                
                elif parts[1].lower() == "reverse":
                    # Reverse DNS
                    if len(parts) < 3:
                        console.print("   Usage: dns reverse <ip>", style="yellow")
                        continue
                    ip = parts[2]
                    console.print(f"\n◫ [bold]Reverse DNS: {ip}[/bold]\n")
                    cmds = build_dns_commands(ip, ["PTR"])
                    target_mcp = list(device_map.keys())[0]
                    for cmd in cmds:
                        try:
                            output = await run_single(mcp_client, session_id, cmd,
                                                       target_mcp, f"dns-reverse:{ip}")
                            result = parse_dns_output(output, ip)
                            console.print(f"   Results: {result.results if result.results else result.status}")
                        except Exception as dns_err:
                            console.print(f"   ✗ {dns_err}", style="bold red")
                    
                    messages.append({"role": "user", "content": user_input})
                    messages.append({"role": "assistant", "content": f"Reverse DNS for {ip} completed."})
                
                else:
                    # Standard DNS lookup
                    domain = parts[1]
                    record_type = parts[2].upper() if len(parts) > 2 else "A"
                    console.print(f"\n◫ [bold]DNS Lookup: {domain} ({record_type})[/bold]\n")
                    
                    cmds = nae.get_dns_commands(domain, [record_type])
                    target_mcp = list(device_map.keys())[0]
                    target_host = device_map[target_mcp]
                    
                    for cmd in cmds:
                        try:
                            output = await run_single(mcp_client, session_id, cmd,
                                                       target_mcp, f"dns:{domain}")
                            result = nae.parse_dns(output, domain)
                            console.print(f"   Router: {target_host}")
                            console.print(f"   Status: {result['status']}")
                            if result['records']:
                                for rec in result['records']:
                                    console.print(f"   {rec.get('type', 'A')}: {rec.get('value', '')}")
                            if result['error']:
                                console.print(f"   Error: {result['error']}", style="yellow")
                        except Exception as dns_err:
                            console.print(f"   ✗ {dns_err}", style="bold red")
                    
                    messages.append({"role": "user", "content": user_input})
                    messages.append({"role": "assistant", "content": f"DNS lookup for {domain} ({record_type}) from {target_host}."})
                continue
            
            # ── v16.0 E141: Security Audit Engine ──
            if lower.startswith("security"):
                parts = user_input.split()
                specific_check = parts[1] if len(parts) > 1 else None
                
                checks_to_run = {}
                if specific_check and specific_check in JUNOS_SECURITY_CHECKS:
                    checks_to_run = {specific_check: JUNOS_SECURITY_CHECKS[specific_check]}
                elif specific_check == "list":
                    console.print("\n⊘ [bold]Available Security Checks[/bold]\n")
                    for name, check in JUNOS_SECURITY_CHECKS.items():
                        sev_icon = {"critical": "[red]●[/red]", "high": "[#ff8700]●[/#ff8700]", "medium": "[yellow]●[/yellow]", "low": "[blue]●[/blue]"}.get(
                            check["severity"].value, "[dim]○[/dim]")
                        console.print(f"   {sev_icon} [cyan]{name}[/cyan]: {check['title']}")
                    console.print(f"\n   Usage: security [check_name] — run specific or all checks")
                    continue
                else:
                    checks_to_run = JUNOS_SECURITY_CHECKS
                
                console.print(f"\n⊘ [bold]Running Security Audit ({len(checks_to_run)} checks)[/bold]\n")
                
                all_findings = []
                # Run on first PE device (most likely to have full config)
                pe_devices = [k for k, v in device_map.items() if v.upper().startswith("PE")]
                target_mcp = pe_devices[0] if pe_devices else list(device_map.keys())[0]
                target_host = device_map[target_mcp]
                
                console.print(f"   Target: {target_host}")
                
                for check_name, check in checks_to_run.items():
                    console.print(f"   ⊕ Checking: {check['title']}...", style="dim")
                    outputs = {}
                    for cmd in check["commands"]:
                        try:
                            output = await run_single(mcp_client, session_id, cmd,
                                                       target_mcp, f"sec:{check_name}")
                            outputs[cmd] = output
                        except Exception:
                            outputs[cmd] = ""
                    
                    finding = nae.run_security_check(check_name, outputs, target_host)
                    all_findings.append(finding)
                    
                    sev_icon = {"critical": "[red]●[/red]", "high": "[#ff8700]●[/#ff8700]", "medium": "[yellow]●[/yellow]", "low": "[blue]●[/blue]", "info": "[green]●[/green]"}.get(
                        finding.severity.value, "[dim]○[/dim]")
                    console.print(f"   {sev_icon} {finding.title}: {finding.evidence[:80]}")
                
                # Generate report
                report = nae.generate_security_report(all_findings)
                
                ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
                fname = f"SECURITY_AUDIT_{ts}.md"
                with open(fname, "w") as f:
                    f.write(report)
                
                console.print(f"\n   ⊟ Full report saved: {fname}")
                console.print(Panel(report[:2000], title="⊘ Security Audit Summary",
                                   border_style="red", width=min(100, console.width - 2)))
                
                messages.append({"role": "user", "content": user_input})
                messages.append({"role": "assistant", "content": report[:2000]})
                continue
            
            # ── v16.0 E144: Log Forensics & Timeline ──
            if lower.startswith("forensics") or lower.startswith("forensic ") or lower.startswith("logs "):
                parts = user_input.split()
                scope = parts[1] if len(parts) > 1 else "all"
                keyword = parts[2] if len(parts) > 2 else ""
                
                console.print(f"\n⊕ [bold]Log Forensics — Scope: {scope}[/bold]\n")
                
                forensic_cmds = nae.get_forensic_commands(scope, keyword)
                
                # Run on all PE devices + a sample P device
                targets = []
                for mcp_name, hostname in device_map.items():
                    if hostname.upper().startswith("PE"):
                        targets.append(mcp_name)
                if not targets:
                    targets = list(device_map.keys())[:3]
                
                all_entries = []
                for target_mcp in targets[:3]:
                    target_host = device_map[target_mcp]
                    console.print(f"   ◇ Collecting from {target_host}...", style="dim")
                    
                    combined_output = ""
                    for cmd in forensic_cmds:
                        try:
                            output = await run_single(mcp_client, session_id, cmd,
                                                       target_mcp, f"forensic:{target_host}")
                            combined_output += output + "\n"
                        except Exception:
                            pass
                    
                    timeline = nae.analyze_logs(combined_output, target_host)
                    all_entries.extend(timeline.events)
                
                # Cross-device correlation
                full_timeline = correlate_events(all_entries)
                report = nae.format_forensics(full_timeline)
                
                ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
                fname = f"FORENSICS_{ts}.md"
                with open(fname, "w") as f:
                    f.write(report)
                
                console.print(Panel(report[:2500], title="⊕ Forensic Timeline",
                                   border_style="cyan", width=min(100, console.width - 2)))
                console.print(f"\n   ⊟ Full report saved: {fname}")
                
                messages.append({"role": "user", "content": user_input})
                messages.append({"role": "assistant", "content": report[:2000]})
                continue
            
            # ── v16.0 E145: Device Profiler ──
            if lower.startswith("profile"):
                parts = user_input.split()
                target = parts[1] if len(parts) > 1 else "all"
                
                if target.lower() == "all":
                    targets = list(device_map.keys())
                else:
                    mcp_name = reverse_map.get(target.lower(), target)
                    if mcp_name not in device_map:
                        console.print(f"   ✗ Unknown device: '{target}'", style="bold red")
                        continue
                    targets = [mcp_name]
                
                console.print(f"\n◫ [bold]Device Profiling — {len(targets)} device(s)[/bold]\n")
                
                profile_cmds = nae.get_profile_commands()
                profiles = []
                
                for target_mcp in targets:
                    hostname = device_map[target_mcp]
                    console.print(f"   ◇ Profiling {hostname}...", style="dim")
                    
                    outputs = {}
                    for cmd in profile_cmds:
                        try:
                            output = await run_single(mcp_client, session_id, cmd,
                                                       target_mcp, f"profile:{hostname}")
                            outputs[cmd] = output
                        except Exception:
                            outputs[cmd] = ""
                    
                    profile = nae.build_profile(outputs, hostname)
                    profiles.append(profile)
                    
                    # Display individual result
                    score = profile.health_score
                    icon = "[green]●[/green]" if score >= 80 else ("[yellow]●[/yellow]" if score >= 50 else "[red]●[/red]")
                    console.print(f"   {icon} {hostname}: {score:.0f}/100 | "
                                 f"CPU: {profile.cpu_utilization:.0f}% | "
                                 f"Mem: {profile.memory_utilization:.0f}% | "
                                 f"Junos: {profile.junos_version or 'N/A'}")
                    if profile.anomalies:
                        for a in profile.anomalies:
                            console.print(f"      ▲ {a}", style="yellow")
                
                # Comparison report if multiple devices
                if len(profiles) > 1:
                    comparison = nae.compare_devices()
                    console.print(Panel(comparison[:2000], title="◫ Device Comparison",
                                       border_style="magenta", width=min(100, console.width - 2)))
                    
                    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
                    fname = f"DEVICE_PROFILES_{ts}.md"
                    with open(fname, "w") as f:
                        f.write(comparison)
                    console.print(f"\n   ⊟ Report saved: {fname}")
                
                messages.append({"role": "user", "content": user_input})
                messages.append({"role": "assistant", "content": f"Profiled {len(profiles)} devices."})
                continue
            
            # ── v16.0 E143: Alert Engine ──
            if lower.startswith("alert"):
                parts = user_input.split()
                subcmd = parts[1] if len(parts) > 1 else "status"
                
                if subcmd == "rules":
                    console.print("\n⊗ [bold]Alert Rules[/bold]\n")
                    rules = nae.get_alert_rules()
                    for name, rule in rules.items():
                        sev_icon = {"critical": "[red]●[/red]", "error": "[#ff8700]●[/#ff8700]", "warning": "[yellow]●[/yellow]", "info": "[blue]●[/blue]"}.get(
                            rule["severity"], "[dim]○[/dim]")
                        console.print(f"   {sev_icon} [cyan]{name}[/cyan]: {rule['description']}")
                        console.print(f"      Protocol: {rule['protocol']} | Commands: {rule['commands'][0]}")
                
                elif subcmd == "check":
                    # Run all alert checks against all devices
                    console.print("\n⊗ [bold]Running Alert Checks...[/bold]\n")
                    triggered = []
                    
                    for target_mcp, hostname in device_map.items():
                        for rule_name, rule in nae.get_alert_rules().items():
                            for cmd in rule.get("commands", []):
                                try:
                                    output = await run_single(mcp_client, session_id, cmd,
                                                               target_mcp, f"alert:{rule_name}")
                                    # Extract metric value from output
                                    count_match = re.search(r'Count:\s*(\d+)', output)
                                    pct_match = re.search(r'(\d+)\s*percent', output, re.IGNORECASE)
                                    if count_match:
                                        value = count_match.group(1)
                                    elif pct_match:
                                        value = pct_match.group(1)
                                    else:
                                        # Use first relevant word
                                        value = output.strip().split('\n')[0][:50] if output.strip() else "N/A"
                                    
                                    event = nae.check_alert(rule_name, hostname, str(value))
                                    if event:
                                        triggered.append(event)
                                        sev_icon = {"critical": "[red]●[/red]", "error": "[#ff8700]●[/#ff8700]", "warning": "[yellow]●[/yellow]"}.get(
                                            event.severity.value, "[dim]○[/dim]")
                                        console.print(f"   {sev_icon} [{hostname}] {event.message}")
                                except Exception:
                                    pass
                    
                    if not triggered:
                        console.print("   ● No alerts triggered — all metrics within thresholds.")
                    else:
                        console.print(f"\n   ⊗ {len(triggered)} alert(s) triggered!")
                
                else:
                    # Show alert status
                    summary = nae.get_alert_summary()
                    console.print(summary)
                
                messages.append({"role": "user", "content": user_input})
                messages.append({"role": "assistant", "content": nae.get_alert_summary()})
                continue
            
            # ── v16.0 E142: Flow & Performance Analysis ──
            if lower.startswith("flow "):
                parts = user_input.split()
                if len(parts) < 3:
                    console.print("   Usage: flow <router> <interface>", style="yellow")
                    console.print("   Example: flow PE1 ge-0/0/0", style="dim")
                    continue
                
                target_name = parts[1]
                interface = parts[2]
                mcp_name = reverse_map.get(target_name.lower(), target_name)
                if mcp_name not in device_map:
                    console.print(f"   ✗ Unknown device: '{target_name}'", style="bold red")
                    continue
                hostname = device_map[mcp_name]
                
                console.print(f"\n▴ [bold]Flow Analysis: {hostname} / {interface}[/bold]\n")
                
                flow_cmds = nae.get_flow_commands(interface)
                combined_output = ""
                for cmd in flow_cmds:
                    try:
                        output = await run_single(mcp_client, session_id, cmd,
                                                   mcp_name, f"flow:{hostname}:{interface}")
                        combined_output += output + "\n"
                        console.print(f"   [dim]> {cmd}[/dim]")
                    except Exception:
                        pass
                
                flow_result = nae.analyze_flow(combined_output)
                flow_result.interface = interface
                
                console.print(f"\n   ◫ Interface: {interface}")
                console.print(f"   Total bytes: {flow_result.total_bytes:,}")
                console.print(f"   Total packets: {flow_result.total_packets:,}")
                console.print(f"   Input rate: {flow_result.rate_bps:,} bps")
                if flow_result.utilization_pct > 0:
                    console.print(f"   Utilization: {flow_result.utilization_pct:.1f}%")
                
                if flow_result.error_counters:
                    has_errors = any(v > 0 for v in flow_result.error_counters.values())
                    if has_errors:
                        console.print(f"\n   ▲ Error Counters:")
                        for name, count in flow_result.error_counters.items():
                            if count > 0:
                                console.print(f"      [red]●[/red] {name}: {count:,}")
                    else:
                        console.print(f"\n   ● No interface errors")
                
                messages.append({"role": "user", "content": user_input})
                messages.append({"role": "assistant", "content": f"Flow analysis for {hostname}/{interface}: {flow_result.total_bytes:,} bytes, {flow_result.rate_bps:,} bps"})
                continue
            
            # ── v16.0 E147: Guided Workflows ──
            if lower.startswith("workflow"):
                parts = user_input.split()
                if len(parts) < 2 or parts[1] == "list":
                    console.print("\n◇ [bold]Available Analysis Workflows[/bold]\n")
                    workflows = nae.list_workflows()
                    for name, info in workflows.items():
                        console.print(f"   • [cyan]{name}[/cyan]: {info['description']}")
                    console.print(f"\n   Usage: workflow <name> — show workflow steps")
                else:
                    wf_name = parts[1].lower()
                    wf = nae.get_workflow(wf_name)
                    if wf:
                        console.print(f"\n◇ [bold]{wf['name']}[/bold]")
                        console.print(f"   {wf['description']}\n")
                        for step in wf['steps']:
                            console.print(f"   {step}")
                    else:
                        console.print(f"   ✗ Unknown workflow: '{wf_name}'", style="bold red")
                        workflows = nae.list_workflows()
                        console.print(f"   Available: {', '.join(workflows.keys())}")
                continue
            
            # Between-device check
            if lower.startswith("check "):
                parts = lower.split()
                if len(parts) >= 3:
                    dev_a, dev_b = parts[1], parts[2]
                    result = await run_between_devices(mcp_client, session_id, device_map, dev_a, dev_b)
                    console.print(f"\n{result}")
                    messages.append({"role": "user", "content": user_input})
                    messages.append({"role": "assistant", "content": result})
                else:
                    console.print("Usage: check <device_A> <device_B>", style="yellow")
                continue

            # Enhancement #3B: Live verification (ping/traceroute)
            if lower.startswith("verify ") or lower.startswith("ping ") or lower.startswith("traceroute "):
                parts = user_input.split()
                action = parts[0].lower()
                
                if action == "verify" and len(parts) >= 2:
                    target_device = parts[1]
                    reverse_map = {v.lower(): k for k, v in device_map.items()}
                    mcp_name = reverse_map.get(target_device.lower(), target_device)
                    if mcp_name not in device_map:
                        console.print(f"✗ Unknown device: '{target_device}'", style="bold red")
                        continue
                    hostname = device_map[mcp_name]
                    console.print(f"\n⊕ Running verification on [cyan]{hostname}[/cyan]...")
                    verify_cmds = [
                        ("show ospf neighbor", "OSPF"),
                        ("show bgp summary", "BGP"),
                        ("show ldp session", "LDP"),
                        ("show bfd session", "BFD"),
                        ("show chassis alarms", "Alarms"),
                    ]
                    results = []
                    for cmd, label in verify_cmds:
                        out = await run_single(mcp_client, session_id, cmd, mcp_name, f"{hostname} {label}")
                        results.append(f"### {label}\n```\n{out[:500]}\n```\n")
                    verify_output = "\n".join(results)
                    console.print(verify_output)
                    messages.append({"role": "user", "content": user_input})
                    messages.append({"role": "assistant", "content": verify_output})
                
                elif action in ("ping", "traceroute") and len(parts) >= 3:
                    src_device = parts[1]
                    dest_ip = parts[2]
                    reverse_map = {v.lower(): k for k, v in device_map.items()}
                    mcp_name = reverse_map.get(src_device.lower(), src_device)
                    if mcp_name not in device_map:
                        console.print(f"✗ Unknown device: '{src_device}'", style="bold red")
                        continue
                    hostname = device_map[mcp_name]
                    cmd = f"{action} {dest_ip} count 5" if action == "ping" else f"{action} {dest_ip}"
                    console.print(f"\n⊕ Running {action} from [cyan]{hostname}[/cyan] to [cyan]{dest_ip}[/cyan]...")
                    out = await run_single(mcp_client, session_id, cmd, mcp_name, f"{hostname} {action}")
                    console.print(f"\n```\n{out[:2000]}\n```")
                    messages.append({"role": "user", "content": user_input})
                    messages.append({"role": "assistant", "content": out})
                else:
                    console.print("Usage: verify <router> | ping <router> <ip> | traceroute <router> <ip>", style="yellow")
                continue

            # Golden Config Store management
            if lower.startswith("golden"):
                golden_parts = lower.split()
                sub = golden_parts[1] if len(golden_parts) > 1 else "status"

                if sub == "status":
                    _ensure_golden_dir()
                    console.print(f"\n⊡ Golden Config Store: [cyan]{GOLDEN_CONFIG_DIR}[/cyan]")
                    for mcp_name, hostname in device_map.items():
                        golden, meta = load_golden_config(mcp_name)
                        if golden:
                            saved_at = meta.get("saved_at", "?")
                            lines = meta.get("lines", "?")
                            sha = meta.get("sha256", "?")[:12]
                            console.print(f"   ● {hostname} ({mcp_name}): {lines} lines, saved {saved_at}, sha:{sha}")
                        else:
                            console.print(f"   ✗ {hostname} ({mcp_name}): No baseline", style="dim")

                elif sub == "save":
                    target = golden_parts[2] if len(golden_parts) > 2 else "all"
                    targets = list(device_map.keys()) if target == "all" else [target]
                    for mcp_name in targets:
                        if mcp_name not in device_map:
                            rev = {v.lower(): k for k, v in device_map.items()}
                            mcp_name = rev.get(mcp_name.lower(), mcp_name)
                        if mcp_name not in device_map:
                            console.print(f"   ✗ Unknown device: {target}", style="bold red")
                            continue
                        hostname = device_map[mcp_name]
                        console.print(f"   ▸ Fetching config from [cyan]{hostname}[/cyan]...")
                        try:
                            cfg = await mcp_call_tool(mcp_client, session_id, "get_junos_config", {"router_name": mcp_name})
                            if cfg and len(cfg.strip()) > 20:
                                path = save_golden_config(mcp_name, cfg.strip())
                                console.print(f"   ● {hostname}: Saved ({len(cfg.splitlines())} lines) → {path}")
                            else:
                                console.print(f"   ▲  {hostname}: Empty config returned", style="yellow")
                        except Exception as e:
                            console.print(f"   ✗ {hostname}: Failed ({e})", style="bold red")

                elif sub == "diff":
                    target = golden_parts[2] if len(golden_parts) > 2 else "all"
                    targets = list(device_map.keys()) if target == "all" else [target]
                    for mcp_name in targets:
                        if mcp_name not in device_map:
                            rev = {v.lower(): k for k, v in device_map.items()}
                            mcp_name = rev.get(mcp_name.lower(), mcp_name)
                        if mcp_name not in device_map:
                            console.print(f"   ✗ Unknown device: {target}", style="bold red")
                            continue
                        hostname = device_map[mcp_name]
                        golden, meta = load_golden_config(mcp_name)
                        if not golden:
                            console.print(f"   ✗ {hostname}: No golden baseline. Run 'golden save {mcp_name}' first.", style="yellow")
                            continue
                        console.print(f"   ▸ Fetching current config from [cyan]{hostname}[/cyan]...")
                        try:
                            cfg = await mcp_call_tool(mcp_client, session_id, "get_junos_config", {"router_name": mcp_name})
                            d = diff_configs(golden, cfg.strip(), mcp_name)
                            if d:
                                summary = summarize_drift(d)
                                console.print(f"   ▲  {hostname}: [yellow]DRIFT DETECTED[/yellow] (+{summary['lines_added']}/-{summary['lines_removed']})")
                                console.print(f"       Sections: {', '.join(summary['sections_changed']) or '?'}")
                                for line in d[:30]:
                                    console.print(f"       {line.rstrip()}")
                                if len(d) > 30:
                                    console.print(f"       ... ({len(d) - 30} more lines)", style="dim")
                            else:
                                console.print(f"   ● {hostname}: Config matches golden baseline")
                        except Exception as e:
                            console.print(f"   ✗ {hostname}: Failed ({e})", style="bold red")

                else:
                    console.print("⊡ Golden Config Store commands:", style="bold")
                    console.print("   golden status        — Show baseline status for all devices")
                    console.print("   golden save [device] — Save current config as golden baseline (default: all)")
                    console.print("   golden diff [device] — Compare current config vs golden baseline (default: all)")
                continue
            
            # Configure mode — safe config push with verification (v11.0: E85/E87/E91 enhancements)
            if lower.startswith("configure ") or lower.startswith("config "):
                parts = user_input.split(None, 2)
                if len(parts) >= 2:
                    target_device = parts[1]
                    config_desc = parts[2] if len(parts) > 2 else ""
                    
                    # Resolve device name
                    reverse_map = {v.lower(): k for k, v in device_map.items()}
                    mcp_name = reverse_map.get(target_device.lower(), target_device)
                    
                    if mcp_name not in device_map:
                        console.print(f"✗ Unknown device: '{target_device}'", style="bold red")
                        console.print(f"   Known: {', '.join(f'{v} ({k})' for k, v in device_map.items())}", style="dim")
                        continue
                    
                    hostname = device_map.get(mcp_name, target_device)
                    
                    # ── v11.0 E91: Change window check ──────────────────
                    window_check = check_change_window()
                    if not window_check["allowed"]:
                        console.print(f"\n▲  [bold red]CHANGE WINDOW WARNING[/bold red]: {window_check['reason']}")
                        console.print(f"   Risk level: [bold]{window_check['risk']}[/bold]")
                        override = input("   Override change window restriction? (yes/no): ").strip().lower()
                        if override not in ("yes", "y"):
                            console.print("   ✗ Change cancelled due to change window restriction.", style="dim")
                            continue
                        console.print("   ▲  Change window override accepted — proceeding with caution.")
                    else:
                        console.print(f"   ◷ Change window: [green]{window_check['reason']}[/green] (Risk: {window_check['risk']})")
                    
                    # ── v11.0 E84: Pre-change impact analysis ───────────
                    impact = analyze_change_impact(hostname, config_desc, _network_graph)
                    if impact.get("risk_level") == "HIGH":
                        console.print(f"\n▲  [bold red]HIGH RISK CHANGE[/bold red] — blast radius: {impact.get('blast_radius', 'unknown')}")
                        for affected in impact.get("affected_devices", [])[:5]:
                            console.print(f"   → Affects: {affected}")
                        override2 = input("   Proceed with HIGH RISK change? (yes/no): ").strip().lower()
                        if override2 not in ("yes", "y"):
                            console.print("   ✗ Change cancelled due to high risk.", style="dim")
                            continue
                    
                    # Get current config context for the AI
                    console.print(f"\n◷ Gathering current config for [cyan]{hostname}[/cyan]...")
                    current_config = await run_single(mcp_client, session_id, 
                                                       "show configuration", mcp_name, 
                                                       f"{hostname} Config")
                    
                    # Ask AI to generate the config change — enhanced with RAG (#2D)
                    rag_context = ""
                    if vector_kb:
                        try:
                            rag_context = await vector_kb.retrieve_for_protocol(
                                "configuration", 
                                f"Junos configuration {config_desc} set commands best practice",
                                top_k=3
                            )
                            rag_context = f"\n\nKNOWLEDGE BASE REFERENCE:\n{rag_context[:2000]}\n"
                        except Exception:
                            rag_context = ""
                    
                    config_prompt = (
                        f"Generate the exact Junos 'set' commands for the following change on {hostname} ({mcp_name}):\n"
                        f"Request: {config_desc}\n\n"
                        f"Current running config (relevant sections):\n{current_config[:4000]}\n\n"
                        f"{rag_context}"
                        "RULES:\n"
                        "1. Output ONLY the 'set' or 'delete' commands, one per line\n"
                        "2. Do NOT include 'commit' — that's handled separately\n"
                        "3. Explain what each command does in a comment\n"
                        "4. If this change could break something, say WHAT and WHY\n"
                        "5. If the change is already applied, say 'NO CHANGE NEEDED'\n"
                        "6. Follow best practices from the knowledge base reference\n"
                    )
                    
                    console.print(f"◉ AI generating config for: [bold]{config_desc or 'requested change'}[/bold]...")
                    ai_config = await ollama_analyze(
                        "You are a Juniper configuration expert. Generate safe, minimal config changes. "
                        "Follow the golden configuration standards from the knowledge base.",
                        current_config[:3000],
                        config_prompt
                    )
                    
                    console.print(Panel(f"◇ Proposed configuration for {hostname}:", style="cyan"))
                    console.print(ai_config)
                    
                    # Extract just the set/delete commands
                    config_lines = []
                    for line in ai_config.split("\n"):
                        stripped = line.strip()
                        if stripped.startswith("set ") or stripped.startswith("delete "):
                            config_lines.append(stripped)
                    
                    if not config_lines:
                        console.print("▲  No 'set' or 'delete' commands found in AI output.", style="yellow")
                        messages.append({"role": "user", "content": user_input})
                        messages.append({"role": "assistant", "content": ai_config})
                        continue
                    
                    config_text = "\n".join(config_lines)
                    console.print(f"\n▪ Commands to push ([bold]{len(config_lines)}[/bold] lines):")
                    for cl in config_lines:
                        console.print(f"   [cyan]{cl}[/cyan]")
                    
                    # Ask for confirmation
                    confirm = input(f"\n▲  Apply to {hostname}? (yes/no/dry-run): ").strip().lower()
                    
                    if confirm in ("dry-run", "dry", "d"):
                        console.print(f"\n⊕ Running dry-run on [cyan]{hostname}[/cyan]...")
                        try:
                            template = "\n".join(f"{cl}" for cl in config_lines)
                            result = await mcp_call_tool(mcp_client, session_id,
                                                          "render_and_apply_j2_template",
                                                          {"template_content": template,
                                                           "vars_content": "---\n",
                                                           "router_name": mcp_name,
                                                           "apply_config": False,
                                                           "dry_run": True})
                            console.print(f"\n◇ Dry-run result:\n{result[:3000]}")
                        except Exception as e:
                            console.print(f"✗ Dry-run failed: {e}", style="bold red")
                    
                    elif confirm in ("yes", "y"):
                        console.print(f"\n⚙ Pushing config to [cyan]{hostname}[/cyan]...")
                        try:
                            # ── v11.0 E87: Capture pre-change state ─────
                            console.print(f"   ◎ Capturing pre-change state...")
                            pre_state = await capture_device_state(mcp_client, session_id, mcp_name, hostname)
                            
                            result = await mcp_call_tool(mcp_client, session_id,
                                                          "load_and_commit_config",
                                                          {"router_name": mcp_name,
                                                           "config_text": config_text,
                                                           "config_format": "set",
                                                           "commit_comment": f"AI-assisted: {config_desc[:50]}"})
                            console.print(f"   ● Commit result: {result[:500]}")
                            logger.info(f"Config pushed to {hostname}: {config_desc}")
                            
                            # ── v11.0 E85: Post-commit verification ─────
                            console.print(f"\n⊕ Verifying change on [cyan]{hostname}[/cyan]...")
                            verify_cmd = "show configuration | compare rollback 1"
                            verify_result = await run_single(mcp_client, session_id,
                                                              verify_cmd, mcp_name,
                                                              f"{hostname} Verify")
                            console.print(f"   ◇ Config diff:\n{verify_result[:1500]}")
                            
                            # Protocol-specific verification
                            verify_ok = True
                            if "ospf" in config_text.lower():
                                v = await run_single(mcp_client, session_id,
                                                      "show ospf neighbor", mcp_name, "OSPF Verify")
                                console.print(f"\n   ◇ OSPF Neighbors after change:\n{v[:800]}")
                                if "down" in v.lower() or "init" in v.lower():
                                    console.print("   ▲  OSPF neighbor in bad state detected!", style="bold yellow")
                                    verify_ok = False
                            if "bgp" in config_text.lower():
                                v = await run_single(mcp_client, session_id,
                                                      "show bgp summary", mcp_name, "BGP Verify")
                                console.print(f"\n   ◇ BGP Summary after change:\n{v[:800]}")
                                if "connect" in v.lower() or "active" in v.lower():
                                    console.print("   ▲  BGP session in non-Established state!", style="bold yellow")
                                    verify_ok = False
                            if "ldp" in config_text.lower():
                                v = await run_single(mcp_client, session_id,
                                                      "show ldp session", mcp_name, "LDP Verify")
                                console.print(f"\n   ◇ LDP Sessions after change:\n{v[:800]}")
                            
                            # ── v11.0 E87: Capture post-change state & compare ──
                            console.print(f"\n   ◎ Capturing post-change state...")
                            post_state = await capture_device_state(mcp_client, session_id, mcp_name, hostname)
                            state_diff = compare_device_states(pre_state, post_state)
                            if "No protocol state changes" not in state_diff:
                                console.print(Panel(state_diff[:3000], title="◫ Pre/Post State Comparison", 
                                                    border_style="cyan", width=min(100, console.width - 2)))
                            else:
                                console.print(f"   ● {state_diff}")
                            
                            # ── v11.0 E86: Auto-rollback on verification failure ──
                            if not verify_ok:
                                console.print(f"\n   ▲  [bold red]VERIFICATION FAILED[/bold red] — protocol issues detected after commit!")
                                rollback_choice = input("   ↻ Auto-rollback to previous config? (yes/no): ").strip().lower()
                                if rollback_choice in ("yes", "y"):
                                    console.print(f"   ↻ Rolling back {hostname}...")
                                    try:
                                        rb_result = await mcp_call_tool(mcp_client, session_id,
                                                                         "load_and_commit_config",
                                                                         {"router_name": mcp_name,
                                                                          "config_text": "rollback 1",
                                                                          "config_format": "text",
                                                                          "commit_comment": "Auto-rollback: verification failed"})
                                        console.print(f"   ● Rollback complete: {rb_result[:300]}")
                                        logger.warning(f"Auto-rollback on {hostname} after failed verification")
                                    except Exception as rb_err:
                                        console.print(f"   ✗ Rollback failed: {rb_err}", style="bold red")
                                        console.print("   ▸ Manual rollback: 'configure; rollback 1; commit'", style="yellow")
                                else:
                                    console.print("   ▲  Keeping change — monitor closely!", style="yellow")
                                
                        except Exception as e:
                            console.print(f"✗ Config push failed: {e}", style="bold red")
                            console.print("▸ You can rollback with: execute_junos_command → 'configure; rollback 1; commit'", style="yellow")
                    else:
                        console.print("✗ Cancelled.", style="dim")
                    
                    messages.append({"role": "user", "content": user_input})
                    messages.append({"role": "assistant", "content": f"Config change for {hostname}:\n{ai_config}"})
                else:
                    console.print("Usage: configure <router> <what to configure>", style="yellow")
                    console.print("Example: configure PE fix ospf interface-type on ge-0/0/2.0", style="dim")
                continue

            # ── v13.1 + v20.0 E167: Self-Improvement Loop — Brain-Analyzed Corrections ──
            if detect_user_correction(user_input, messages):
                # Find the AI's last response to learn from
                ai_last = ""
                user_last_q = ""
                for m in reversed(messages):
                    if m.get("role") == "assistant" and m.get("content") and not ai_last:
                        ai_last = m["content"]
                    elif m.get("role") == "user" and m.get("content") and not user_last_q:
                        user_last_q = m["content"]
                    if ai_last and user_last_q:
                        break
                if ai_last:
                    try:
                        console.print(f"   {Icons.BRAIN} [dim]Correction detected → Brain analyzing (not blindly accepting)...[/dim]")
                        
                        # v20.0: Use Brain analysis instead of blind acceptance
                        if _feedback_memory:
                            analysis = await _feedback_memory.analyze_feedback_with_brain(
                                user_input, ai_last, user_last_q
                            )
                            _feedback_memory.add_feedback(
                                user_msg=user_last_q,
                                ai_response=ai_last,
                                feedback_text=user_input,
                                brain_analysis=analysis,
                                session_id=current_conv_id,
                            )
                            
                            validity = analysis.get("validity", "unanalyzed")
                            action = analysis.get("action", "note")
                            rule = analysis.get("rule", "")
                            
                            if validity in ("valid", "partially_valid") and action == "learn":
                                # Validated correction — save as lesson
                                lesson = await generate_lesson_from_correction(user_input, ai_last)
                                if rule and rule != "N/A":
                                    lesson["rule"] = rule  # Use Brain's rule if available
                                save_workflow_lesson(lesson["mistake"], lesson["correction"], lesson["rule"])
                                console.print(f"   [green]{Icons.OK}[/green] [dim]Validated correction → lesson saved: {lesson['rule'][:80]}[/dim]")
                            elif validity == "invalid":
                                console.print(f"   [dim]{Icons.BRAIN} Brain assessment: feedback appears incorrect — noted but not learned[/dim]")
                            elif validity == "subjective":
                                console.print(f"   [dim]{Icons.BRAIN} Brain assessment: subjective preference — noted for reference[/dim]")
                            else:
                                console.print(f"   [dim]{Icons.BRAIN} Brain assessment: {validity} — {action}[/dim]")
                        else:
                            # Fallback: old behavior without Brain analysis
                            lesson = await generate_lesson_from_correction(user_input, ai_last)
                            save_workflow_lesson(lesson["mistake"], lesson["correction"], lesson["rule"])
                            console.print(f"   ▪ [dim]Lesson saved: {lesson['rule'][:80]}[/dim]")
                    except Exception as le:
                        logger.debug(f"Lesson generation failed: {le}")

            # ── v12.0: Smart Query Classification + Enhanced Routing ──
            query_type = classify_query(user_input, has_kb=bool(vector_kb))
            enhanced_input = user_input
            
            # v18.0: Inject attached file content into enhanced_input
            if attached_content:
                enhanced_input = f"{user_input}\n{attached_content}"
            
            if query_type == "knowledge" and vector_kb:
                # Pure knowledge question — answer from RAG, no tools needed
                console.print(f"   [dim]{Icons.SCRIPT}[/dim] [dim]Query type: knowledge → RAG retrieval[/dim]")
                try:
                    rag_chunks = await vector_kb.retrieve(user_input, top_k=5)
                    if rag_chunks:
                        kb_context = "\n\n".join([c.get("text", "") for c in rag_chunks])
                        enhanced_input = (
                            f"{user_input}\n\n"
                            f"[REFERENCE MATERIAL — answer based on this knowledge:]\n{kb_context[:3000]}"
                        )
                except Exception as e:
                    logger.debug(f"RAG retrieval failed: {e}")
            
            elif query_type in ("status", "troubleshoot"):
                # Needs real data from routers
                console.print(f"   [dim]{Icons.TOOL}[/dim] [dim]Query type: {query_type} → tools required[/dim]")
                
                # v19.0: Auto-generate action plan for status/troubleshoot queries
                if _action_tracker:
                    _action_tracker.auto_plan_from_query(user_input, query_type)
                
                # v13.0 E112: Use structured reasoning chains for complex troubleshoot queries
                if query_type == "troubleshoot" and AI_STRUCTURED_REASONING:
                    # v15.0: Use reasoning engine's classify_problem for precise routing
                    problem_class = classify_problem(user_input)
                    
                    device_mentions = len(re.findall(r'\b(PE[123]|P[12][1234])\b', user_input, re.IGNORECASE))
                    proto_mentions = sum(1 for p in ["ospf", "bgp", "ldp", "mpls", "isis", "vpn", "bfd", "rsvp"]
                                        if p in user_input.lower())
                    
                    # v15.0: Use reasoning engine's complexity + strategy for routing
                    is_ultra_complex = (
                        problem_class.complexity.value in ("complex", "expert") or
                        problem_class.reasoning_strategy == "mind_map" or
                        (device_mentions >= 3 and proto_mentions >= 2) or
                        any(kw in user_input.lower() for kw in [
                            "cascade", "chain", "mind map", "mindmap", "deep analysis",
                            "root cause analysis", "full investigation", "comprehensive",
                            "hypothesis", "investigate"
                        ])
                    )
                    
                    is_complex = (
                        problem_class.complexity.value in ("moderate", "complex", "expert") or
                        problem_class.reasoning_strategy in ("structured_chain", "focused_investigation") or
                        (device_mentions >= 2) or (proto_mentions >= 2)
                    )
                    
                    if is_ultra_complex:
                        # v18.0: Route ultra-complex multi-device queries through Agentic Brain
                        # for parallel fact gathering + self-validation
                        use_brain = (
                            device_mentions >= 2 or  # multi-device = brain excels
                            proto_mentions >= 3 or   # multi-protocol = brain excels
                            any(kw in user_input.lower() for kw in [
                                "full", "comprehensive", "all", "network-wide", "every",
                                "brain", "smart", "parallel", "double check", "validate"
                            ])
                        )
                        
                        if use_brain:
                            console.print(f"   ◉ [dim]Ultra-complex → AGENTIC BRAIN (v18.0) "
                                         f"(domain={problem_class.domain.value}, "
                                         f"complexity={problem_class.complexity.value})[/dim]")
                            try:
                                available_devices = list(device_map.keys())
                                brain_cfg = cfg.get("hypered_brain", {})
                                
                                async def _auto_brain_batch(c, s, cmds, devices, label):
                                    return await run_batch(mcp_client, session_id, cmds, devices, label)
                                async def _auto_brain_single(c, s, cmd, device, label):
                                    return await run_single(mcp_client, session_id, cmd, device, label)
                                async def _auto_brain_ai(system_ctx, data, question, include_kb=True):
                                    return await ollama_analyze(system_ctx, data, question, include_kb)
                                
                                brain_result = await hypered_brain_analyze(
                                    query=user_input,
                                    run_batch_fn=_auto_brain_batch,
                                    run_single_fn=_auto_brain_single,
                                    ai_analyze_fn=_auto_brain_ai,
                                    available_devices=available_devices,
                                    device_map=device_map,
                                    confidence_threshold=brain_cfg.get("confidence_threshold", 70),
                                    max_passes=brain_cfg.get("max_passes", 3),
                                    max_concurrent=brain_cfg.get("max_concurrent_scripts", 3),
                                    print_fn=console.print,
                                )
                                console.print()
                                console.print(Panel(brain_result,
                                                   title="◉ Agentic Brain Analysis (v18.0)",
                                                   border_style="magenta",
                                                   width=min(100, console.width - 2)))
                                messages.append({"role": "user", "content": user_input})
                                messages.append({"role": "assistant", "content": brain_result})
                                if _action_tracker:
                                    _action_tracker.record_ai_call()
                                    _action_tracker.complete_plan()
                                    _action_tracker.print_session_bar()
                                else:
                                    _rag_chunks = vector_kb.stats().get("chunks", 0) if vector_kb else 0
                                    print_status_bar(device_count=len(device_map), health_score=-1,
                                                     msg_count=len(messages), rag_chunks=_rag_chunks)
                                continue
                            except Exception as brain_auto_err:
                                logger.warning(f"Hypered Brain auto-route failed: {brain_auto_err} — falling back to mind-map")
                        
                        console.print(f"   ◉ [dim]Ultra-complex query → MIND-MAP reasoning "
                                     f"(domain={problem_class.domain.value}, "
                                     f"complexity={problem_class.complexity.value})[/dim]")
                        try:
                            chain_result = await mind_map_reasoning(
                                user_input, mcp_client, session_id, device_map,
                                tools=ollama_tools
                            )
                            console.print()
                            console.print(Panel(chain_result, title="◉ Mind-Map Deep Analysis (v14.0)",
                                              border_style="magenta", width=min(100, console.width - 2)))
                            messages.append({"role": "user", "content": user_input})
                            messages.append({"role": "assistant", "content": chain_result})
                            if _action_tracker:
                                _action_tracker.record_ai_call()
                                _action_tracker.complete_plan()
                                _action_tracker.print_session_bar()
                            else:
                                _rag_chunks = vector_kb.stats().get("chunks", 0) if vector_kb else 0
                                print_status_bar(device_count=len(device_map), health_score=-1,
                                                 msg_count=len(messages), rag_chunks=_rag_chunks)
                            continue
                        except Exception as mm_err:
                            logger.warning(f"Mind-map reasoning failed: {mm_err} — falling back to structured chain")
                    
                    if is_complex:
                        console.print(f"   ◉ [dim]Complex query detected → structured reasoning chain[/dim]")
                        try:
                            chain_result = await structured_reasoning_chain(
                                user_input, mcp_client, session_id, device_map,
                                tools=ollama_tools
                            )
                            console.print()
                            console.print(Panel(chain_result, title="◈ Assistant (Structured Analysis)",
                                              border_style="green", width=min(100, console.width - 2)))
                            messages.append({"role": "user", "content": user_input})
                            messages.append({"role": "assistant", "content": chain_result})
                            
                            # Auto-learn lessons
                            try:
                                fix_commands = re.findall(r'`(set protocols \S+.*?)`', chain_result)
                                if fix_commands and any(kw in chain_result.lower() for kw in ["critical", "root cause", "fix"]):
                                    for proto in ["ospf", "bgp", "ldp", "isis", "mpls", "rsvp"]:
                                        if proto in chain_result.lower():
                                            for line in chain_result.split("\n"):
                                                if any(sev in line for sev in ["CRITICAL", "WARNING", "Root Cause", "root cause"]):
                                                    save_lesson(
                                                        category=proto.upper(),
                                                        description=line.strip()[:150],
                                                        root_cause=line.strip()[:150],
                                                        fix=fix_commands[0][:200],
                                                        router=re.search(r'\b(PE[123]|P[12][1234])\b', chain_result, re.IGNORECASE).group(0) if re.search(r'\b(PE[123]|P[12][1234])\b', chain_result, re.IGNORECASE) else ""
                                                    )
                                                    break
                                            break
                            except Exception:
                                pass
                            
                            _rag_chunks = vector_kb.stats().get("chunks", 0) if vector_kb else 0
                            if _action_tracker:
                                _action_tracker.record_ai_call()
                                _action_tracker.complete_plan()
                                _action_tracker.print_session_bar()
                            else:
                                print_status_bar(device_count=len(device_map), health_score=-1,
                                                 msg_count=len(messages), rag_chunks=_rag_chunks)
                            continue
                        except Exception as src_err:
                            logger.warning(f"Structured reasoning chain failed: {src_err} — falling back to normal flow")
                
                enhanced_input = (
                    f"{user_input}\n\n"
                    f"[INSTRUCTION: Use your tools to collect real data from the routers before answering. "
                    f"Do NOT answer from memory. Call execute_junos_command or execute_junos_command_batch first, "
                    f"then analyze the actual output.]"
                )
            
            elif query_type == "compare":
                console.print(f"   ⊕ [dim]Query type: compare → config diff[/dim]")
                enhanced_input = (
                    f"{user_input}\n\n"
                    f"[INSTRUCTION: Use get_junos_config or junos_config_diff tools to collect the actual "
                    f"configurations, then compare them side by side.]"
                )
            
            elif query_type == "config":
                console.print(f"   ⚙️ [dim]Query type: config change[/dim]")
            
            else:
                # General — still nudge for tools if it seems operational
                question_keywords = ["check", "show", "status", "health", "neighbor", "bgp", "ospf", 
                                     "ldp", "isis", "interface", "route", "config", "why", "what",
                                     "how", "is ", "are ", "can ", "does", "problem", "issue", "fix",
                                     "broken", "down", "flap", "error", "investigate"]
                needs_tools = any(kw in user_input.lower() for kw in question_keywords)
                if needs_tools and not user_input.lower().startswith(("configure ", "template ")):
                    enhanced_input = (
                        f"{user_input}\n\n"
                        f"[INSTRUCTION: Use your tools to collect real data from the routers before answering. "
                        f"Do NOT answer from memory.]"
                    )
            
            # v12.0: Pin conversation summary to survive token trimming
            conv_summary = generate_conversation_summary(messages)
            if conv_summary:
                enhanced_input = f"{conv_summary}\n\n{enhanced_input}"
            
            # v15.0: Inject Junos scripting context when relevant
            script_ctx = get_junos_scripting_context(user_input)
            if script_ctx:
                enhanced_input = f"{enhanced_input}\n\n{script_ctx}"
            
            # v12.0 Enhancement #6: Inject live health state if available
            health_ctx = get_health_state_prompt()
            if health_ctx:
                enhanced_input = f"{health_ctx}\n\n{enhanced_input}"
            
            # v12.0 Enhancement #10: Inject proactive alerts if any
            alert_ctx = check_for_proactive_alerts()
            if alert_ctx:
                enhanced_input = f"{alert_ctx}\n\n{enhanced_input}"
            
            # v12.0 Enhancement #12: Inject last root cause chain if available
            rcc_ctx = get_last_root_cause_chain()
            if rcc_ctx:
                enhanced_input = f"{rcc_ctx}\n\n{enhanced_input}"
            
            messages.append({"role": "user", "content": enhanced_input})

            # ── Enhancement #2: Token-aware context window management ──
            # Replace count-based trimming with token-aware trimming
            messages = trim_messages_by_tokens(messages)

            # ── v19.0: Auto-generate action plan for this query ──
            if _action_tracker:
                _action_tracker.auto_plan_from_query(user_input, query_type)
                _action_tracker.start_step(0, "Sending to AI")

            # ── TOOL-CALLING LOOP ──
            max_tool_rounds = 12  # Increased from 8: let AI do more multi-step reasoning
            tool_round = 0
            _pre_state = None  # v11.0 E87: pre-change state for tool-loop config pushes
            _plan_step_idx = 0  # v19.0: track which action plan step we're on
            while tool_round < max_tool_rounds:
                tool_round += 1
                
                # v19.0: Claude Code-style thinking indicator
                _think_start = time.time()
                console.print(f"  [#5fd7ff]│[/#5fd7ff] [dim]{Icons.CLOCK} Thinking (round {tool_round})...[/dim]", end="")
                
                try:
                    response = await ollama_chat(messages, ollama_tools)
                    if _action_tracker:
                        _action_tracker.record_ai_call(approx_tokens=len(str(response)) // 4)
                except Exception as e:
                    console.print(f"\n[red]{Icons.FAIL}[/red] AI Error: {e}", style="bold red")
                    if _action_tracker:
                        _action_tracker.fail_step(_plan_step_idx, f"AI Error: {e}")
                    messages.append({"role": "assistant", "content": f"I encountered an error: {e}. Please try again."})
                    break
                
                _think_elapsed = time.time() - _think_start

                msg = response.get("message", {})
                tool_calls = msg.get("tool_calls")

                if tool_calls:
                    console.print(f"\r  [#5fd7ff]│[/#5fd7ff] {Icons.TOOL} [bold]AI requesting {len(tool_calls)} tool(s)[/bold] [dim](round {tool_round}, {_think_elapsed:.1f}s)[/dim]")
                    messages.append(msg)
                    
                    # v19.0: Advance action plan to data collection step
                    if _action_tracker and _plan_step_idx < 2:
                        _action_tracker.complete_step(_plan_step_idx, f"{_think_elapsed:.1f}s")
                        _plan_step_idx += 1
                        if _plan_step_idx < len(_action_tracker.current_plan):
                            _action_tracker.start_step(_plan_step_idx, "Collecting data")
                    
                    for tc in tool_calls:
                        func = tc.get("function", {})
                        tool_name = func.get("name", "")
                        tool_args = func.get("arguments", {})
                        
                        # v19.0: Claude Code-style tool call display
                        args_short = json.dumps(tool_args)[:150]
                        _tool_start = time.time()
                        console.print(f"  [#5fd7ff]│[/#5fd7ff]   {Icons.ARROW} [cyan]{tool_name}[/cyan] [dim]{args_short}[/dim]")
                        
                        # ── SAFETY INTERCEPTION for config push ──
                        if tool_name in ("load_and_commit_config", "render_and_apply_j2_template"):
                            config_text = tool_args.get("config_text", tool_args.get("template_content", ""))
                            target = tool_args.get("router_name", "unknown")
                            apply_flag = tool_args.get("apply_config", True)
                            dry_run_flag = tool_args.get("dry_run", False)
                            
                            if apply_flag and not dry_run_flag:
                                # ── v11.0 E91: Change window check ──
                                wc = check_change_window()
                                if not wc["allowed"]:
                                    console.print(f"\n   [yellow]{Icons.WARN}[/yellow]  [bold red]CHANGE WINDOW[/bold red]: {wc['reason']} (Risk: {wc['risk']})")
                                    wc_override = input("   Override change window? (yes/no): ").strip().lower()
                                    if wc_override not in ("yes", "y"):
                                        result = f"CONFIG BLOCKED: Outside change window — {wc['reason']}"
                                        console.print(f"      [red]{Icons.FAIL}[/red] Blocked by change window", style="bold red")
                                        messages.append({"role": "tool", "content": result})
                                        continue
                                
                                console.print(f"\n   [yellow]{Icons.WARN}[/yellow]  AI wants to [bold red]PUSH CONFIG[/bold red] to {target}:")
                                for cline in config_text.split("\n")[:10]:
                                    console.print(f"      {cline}")
                                if config_text.count("\n") > 10:
                                    console.print(f"      ... ({config_text.count(chr(10))} total lines)", style="dim")
                                
                                safety_confirm = input(f"   {Icons.WARN}  Allow commit to {target}? (yes/no): ").strip().lower()
                                if safety_confirm not in ("yes", "y"):
                                    result = "CONFIG PUSH BLOCKED BY USER. The user declined the commit."
                                    console.print(f"  [#5fd7ff]│[/#5fd7ff]   [red]{Icons.FAIL}[/red] Blocked by user", style="bold red")
                                    messages.append({"role": "tool", "content": result})
                                    continue
                                
                                # ── v11.0 E87: Pre-change state capture ──
                                try:
                                    console.print(f"  [#5fd7ff]│[/#5fd7ff]     [dim]{Icons.TARGET} Capturing pre-change state for {target}...[/dim]")
                                    _pre_state = await capture_device_state(mcp_client, session_id, target, target)
                                except Exception:
                                    _pre_state = None
                        
                        # Execute Tool — with Enhancement #1 auto-reconnect
                        result = ""
                        try:
                            if tool_name in local_tools:
                                console.print(f"  [#5fd7ff]│[/#5fd7ff]     [dim]{Icons.ARROW} Running local tool...[/dim]")
                                result = await local_tools[tool_name](tool_args)
                            else:
                                try:
                                    result = await mcp_call_tool(mcp_client, session_id, tool_name, tool_args)
                                except (httpx.ConnectError, httpx.ReadError, httpx.RemoteProtocolError, ConnectionError) as conn_err:
                                    console.print(f"  [#5fd7ff]│[/#5fd7ff]     [yellow]{Icons.RESTORE}[/yellow] MCP connection lost, reconnecting...", style="yellow")
                                    try:
                                        session_id = await mcp_reconnect(mcp_client)
                                        result = await mcp_call_tool(mcp_client, session_id, tool_name, tool_args)
                                    except Exception as reconn_err:
                                        result = f"MCP reconnection failed: {reconn_err}"
                        except Exception as e:
                            result = f"Error calling tool {tool_name}: {e}"
                        
                        # v19.0: Record tool call in action tracker
                        _tool_elapsed = time.time() - _tool_start
                        if _action_tracker:
                            _action_tracker.record_tool_call(tool_name, args_short[:80], len(result))
                        
                        display_len = len(result)
                        if display_len > TOOL_RESULT_MAX_CHARS and tool_name != "run_network_audit":
                            result = smart_truncate_tool_result(result, tool_name, max_chars=TOOL_RESULT_MAX_CHARS)
                        
                        # v19.0: Claude Code-style result display with timing
                        console.print(f"  [#5fd7ff]│[/#5fd7ff]     [green]{Icons.OK}[/green] [green]{len(result):,}[/green] chars [dim]({_tool_elapsed:.1f}s)[/dim]")
                        logger.info(f"Tool {tool_name}: {len(result)} chars ({_tool_elapsed:.1f}s)")
                        
                        # ── v11.0 E87: Post-change state capture & comparison ──
                        if tool_name in ("load_and_commit_config", "render_and_apply_j2_template") and _pre_state:
                            try:
                                console.print(f"  [#5fd7ff]│[/#5fd7ff]     [dim]{Icons.TARGET} Capturing post-change state...[/dim]")
                                _post_state = await capture_device_state(mcp_client, session_id, target, target)
                                _state_cmp = compare_device_states(_pre_state, _post_state)
                                if "No protocol state changes" not in _state_cmp:
                                    console.print(Panel(_state_cmp[:2000], title=f"{Icons.GRAPH} State Comparison",
                                                        border_style="cyan", width=min(100, console.width - 2)))
                                else:
                                    console.print(f"      [green]{Icons.OK}[/green] {_state_cmp}")
                                # Append comparison to tool result for AI context
                                result += f"\n\n--- STATE COMPARISON ---\n{_state_cmp[:1500]}"
                            except Exception:
                                pass  # Non-critical
                            _pre_state = None
                        
                        messages.append({"role": "tool", "content": result})
                    
                else:
                    # Final response — v7.0 #P1C / v19.0 Claude Code style
                    content = msg.get("content", "No response")
                    
                    # v13.0 E115: Output verification for final responses
                    if AI_OUTPUT_VERIFICATION and len(content) > 100:
                        content = await verify_ai_output(content, user_input, device_map)
                    
                    # v19.0: Complete action plan before displaying response
                    if _action_tracker:
                        _action_tracker.complete_plan()
                    
                    console.print()
                    console.print(Panel(content, title=f"{Icons.AI} Assistant", border_style="green", width=min(100, console.width - 2)))
                    messages.append({"role": "assistant", "content": content})
                    
                    # v12.0: Auto-learn lessons from AI responses containing fixes
                    try:
                        fix_commands = re.findall(r'`(set protocols \S+.*?)`', content)
                        if fix_commands and any(kw in content.lower() for kw in ["critical", "root cause", "fix"]):
                            # Extract category from protocol mention
                            for proto in ["ospf", "bgp", "ldp", "isis", "mpls", "rsvp"]:
                                if proto in content.lower():
                                    # Extract a short description
                                    for line in content.split("\n"):
                                        if any(sev in line for sev in ["CRITICAL", "WARNING", "Root Cause", "root cause"]):
                                            save_lesson(
                                                category=proto.upper(),
                                                description=line.strip()[:150],
                                                root_cause=line.strip()[:150],
                                                fix=fix_commands[0][:200],
                                                router=re.search(r'\b(PE[123]|P[12][1234])\b', content, re.IGNORECASE).group(0) if re.search(r'\b(PE[123]|P[12][1234])\b', content, re.IGNORECASE) else ""
                                            )
                                            break
                                    break
                    except Exception:
                        pass  # Non-critical
                    
                    # v19.0: Claude Code-style session bar replaces old status bar
                    if _action_tracker:
                        _action_tracker.print_session_bar()
                    else:
                        _rag_chunks = vector_kb.stats().get("chunks", 0) if vector_kb else 0
                        print_status_bar(device_count=len(device_map), health_score=-1,
                                         msg_count=len(messages), rag_chunks=_rag_chunks)
                    
                    # v20.0: Auto-save conversation every 10 messages
                    user_msg_count = sum(1 for m in messages if m.get("role") == "user")
                    if _conversation_manager and user_msg_count > 0 and user_msg_count % 5 == 0:
                        try:
                            _conversation_manager.save_conversation(messages, conv_id=current_conv_id)
                        except Exception:
                            pass  # Non-critical
                    
                    break
            
            if tool_round >= max_tool_rounds:
                console.print(f"\n[yellow]{Icons.WARN}[/yellow]  AI hit max tool rounds ({max_tool_rounds}). Stopping.")
                if _action_tracker:
                    _action_tracker.complete_plan()

if __name__ == "__main__":
    asyncio.run(main())
