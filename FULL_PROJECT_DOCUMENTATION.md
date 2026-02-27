# Junos AI Network Operations Center — Full Project Documentation

## Version 21.2 — Full-Stack Agentic Web NOC with Zero-Config Onboarding

---

```
═══════════════════════════════════════════════════════════════════════════════════
       ██╗██╗   ██╗███╗   ██╗ ██████╗ ███████╗     █████╗ ██╗
       ██║██║   ██║████╗  ██║██╔═══██╗██╔════╝    ██╔══██╗██║
       ██║██║   ██║██╔██╗ ██║██║   ██║███████╗    ███████║██║
  ██   ██║██║   ██║██║╚██╗██║██║   ██║╚════██║    ██╔══██║██║
  ╚█████╔╝╚██████╔╝██║ ╚████║╚██████╔╝███████║    ██║  ██║██║
   ╚════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝    ╚═╝  ╚═╝╚═╝
   AI Network Operations Center — Full-Stack Autonomous Junos Intelligence
═══════════════════════════════════════════════════════════════════════════════════
```

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Quick Start — Zero-Config Onboarding Guide](#2-quick-start--zero-config-onboarding-guide)
3. [System Architecture](#3-system-architecture)
4. [Component Deep Dive](#4-component-deep-dive)
   - 4.1 [Junos MCP Server (`jmcp.py`)](#41-junos-mcp-server-jmcppy)
   - 4.2 [Ollama MCP Client / Bridge (`ollama_mcp_client.py`)](#42-ollama-mcp-client--bridge-ollama_mcp_clientpy)
   - 4.3 [Hypered Brain Engine (`hypered_brain.py`)](#43-hypered-brain-engine-hypered_brainpy)
   - 4.4 [Reasoning Engine (`reasoning_engine.py`)](#44-reasoning-engine-reasoning_enginepy)
   - 4.5 [Network Analysis Engine (`network_analysis.py`)](#45-network-analysis-engine-network_analysispy)
   - 4.6 [Knowledge Base Vector Store (`kb_vectorstore.py`)](#46-knowledge-base-vector-store-kb_vectorstorepy)
   - 4.7 [PDF Knowledge Ingester (`ingest_pdfs.py`)](#47-pdf-knowledge-ingester-ingest_pdfspy)
   - 4.8 [Configuration System (`config.yaml`)](#48-configuration-system-configyaml)
5. [Web UI — Full-Stack Network Operations Dashboard](#5-web-ui--full-stack-network-operations-dashboard)
   - 5.1 [Architecture & Technology Stack](#51-architecture--technology-stack)
   - 5.2 [Navigation & Layout System](#52-navigation--layout-system)
   - 5.3 [Dashboard View](#53-dashboard-view)
   - 5.4 [Network Topology Visualization](#54-network-topology-visualization)
   - 5.5 [AI Command Center (Chat)](#55-ai-command-center-chat)
   - 5.6 [AI Copilot Sidebar](#56-ai-copilot-sidebar)
   - 5.7 [Device Inventory](#57-device-inventory)
   - 5.8 [Device Pools](#58-device-pools)
   - 5.9 [Ping & Reachability](#59-ping--reachability)
   - 5.10 [Path Finder](#510-path-finder)
   - 5.11 [Configuration Management](#511-configuration-management)
   - 5.12 [Template Engine](#512-template-engine)
   - 5.13 [Data Validation](#513-data-validation)
   - 5.14 [Git Export (Config Version Control)](#514-git-export-config-version-control)
   - 5.15 [Result Comparison](#515-result-comparison)
   - 5.16 [Workflow Builder](#516-workflow-builder)
   - 5.17 [Task Scheduler](#517-task-scheduler)
   - 5.18 [Log Forensics](#518-log-forensics)
   - 5.19 [Notification Channels](#519-notification-channels)
   - 5.20 [Config Rollback](#520-config-rollback)
   - 5.21 [Network Discovery & Interface Analysis](#521-network-discovery--interface-analysis)
   - 5.22 [Protocol Traffic Analysis](#522-protocol-traffic-analysis)
   - 5.23 [Security Threat Analysis](#523-security-threat-analysis)
   - 5.24 [DNS Diagnostics](#524-dns-diagnostics)
   - 5.25 [Advanced Path Analysis & Capacity Planning](#525-advanced-path-analysis--capacity-planning)
   - 5.26 [Live Monitoring & Alerting](#526-live-monitoring--alerting)
6. [Quantum-Inspired Network Optimization Engine](#6-quantum-inspired-network-optimization-engine)
7. [REST API Reference (101 Endpoints)](#7-rest-api-reference-101-endpoints)
8. [WebSocket Real-Time Events](#8-websocket-real-time-events)
9. [Data Flow & Communication](#9-data-flow--communication)
10. [AI Intelligence Layers](#10-ai-intelligence-layers)
11. [Specialist AI System](#11-specialist-ai-system)
12. [Hypered Brain — 6-Layer Agentic Architecture](#12-hypered-brain--6-layer-agentic-architecture)
13. [Smart Script Library](#13-smart-script-library)
14. [Audit System](#14-audit-system)
15. [Interactive Chat Mode (Terminal)](#15-interactive-chat-mode-terminal)
16. [Safety & Change Management](#16-safety--change-management)
17. [Knowledge Base & RAG Pipeline](#17-knowledge-base--rag-pipeline)
18. [Network Topology Intelligence](#18-network-topology-intelligence)
19. [Lab Topology & Device Inventory](#19-lab-topology--device-inventory)
20. [Reporting System](#20-reporting-system)
21. [Persistence & Memory](#21-persistence--memory)
22. [Configuration Templates](#22-configuration-templates)
23. [Golden Configs & Compliance](#23-golden-configs--compliance)
24. [Bootstrap & Zero-Config Onboarding System](#24-bootstrap--zero-config-onboarding-system)
25. [Local-Only Architecture](#25-local-only-architecture)
26. [Database Schema](#26-database-schema)
27. [How to Build & Run — Complete Step-by-Step Guide](#27-how-to-build--run--complete-step-by-step-guide)
28. [Troubleshooting Guide](#28-troubleshooting-guide)
29. [Version History](#29-version-history)
30. [File Inventory & Line Counts](#30-file-inventory--line-counts)

---

## 1. Project Overview

### What Is This Project?

The **Junos AI Network Operations Center** is a fully autonomous, AI-powered network management system for Juniper Networks routers running Junos OS. It features a **full-stack web-based dashboard** that provides visual, interactive access to every capability — from topology visualization to AI-powered diagnostics. It combines:

- **A Full-Stack Web UI** (Flask + Single-Page Application) with **21 interactive views**, dark/light theming, and a persistent AI Copilot sidebar
- **Zero-Config Onboarding** — connect your MCP server and devices, the tool auto-discovers and populates everything
- **A Model Context Protocol (MCP) Server** that provides live read/write access to Junos routers via SSH/NETCONF
- **A local AI engine** (GPT-OSS 13B via Ollama) that acts as a JNCIE-SP level network engineer
- **A Quantum-Inspired Network Optimization Engine** with 5 advanced graph algorithms for production-scale analysis
- **A 6-layer Agentic Brain** that autonomously investigates, diagnoses, and prescribes fixes
- **A RAG (Retrieval Augmented Generation) pipeline** backed by a 184KB+ Junos knowledge base and 7 Juniper certification PDFs
- **A multi-specialist analysis system** with 8 protocol-specific AI specialists
- **Network Discovery, Traffic Analysis, Security Auditing, DNS Diagnostics, and Capacity Planning** — all AI-powered
- **An automated audit engine** that generates executive-grade network health reports
- **Zero external dependencies** — all libraries, fonts, and assets bundled locally

### Key Capabilities

| Capability | Description |
|---|---|
| **Zero-Config Onboarding** | Just connect MCP server + devices — the tool auto-discovers routers, pulls configs, and builds topology |
| **Web-Based Dashboard** | 21-view single-page application with real-time WebSocket updates, D3.js topology, AI Copilot sidebar |
| **AI Chat & Copilot** | Full conversational AI with SSE streaming, context-aware sidebar available from every view |
| **Autonomous Investigation** | AI identifies problems, collects data, forms hypotheses, and diagnoses root causes — without human guidance |
| **Live Network Access** | Real-time SSH into routers via MCP tools (show commands, config push, template rendering) |
| **Network Discovery** | Full infrastructure scanning — interfaces, LLDP neighbors, OS fingerprinting, and AI-powered infrastructure mapping |
| **Protocol Traffic Analysis** | Real-time protocol statistics, flow analysis, session tracking — equivalent to Wireshark expert analysis |
| **Security Threat Detection** | AI-powered security auditing, credential scanning, threat detection, and CIS-style hardening reports |
| **DNS Diagnostics** | DNS resolution, reverse lookup, batch queries, and AI configuration auditing across all routers |
| **Advanced Path Analysis** | Multi-algorithm path computation, what-if failure simulation, and AI capacity planning |
| **Live Monitoring** | Real-time health dashboard, protocol health checks, and AI incident response across all routers |
| **Quantum-Grade Analysis** | Tarjan SPOF detection O(V+E), quantum walk anomaly detection, Louvain community detection, simulated annealing optimization |
| **Multi-Pass Validation** | AI re-checks its own conclusions with additional data collection passes until confidence >= 70% |
| **Workflow Automation** | Visual workflow builder with 12 step types — chain MCP commands, AI analysis, conditions, notifications |
| **Scheduled Tasks** | CRON-style recurring task execution with history, calendar view, and background scheduler |
| **Config Version Control** | Git-based config export with AI-generated commit messages, diff viewer, and rollback |
| **Data Validation** | Pattern matching, batch validation, and AI compliance auditing across all routers |
| **Notification Service** | Slack, Mattermost, and webhook channels with AI-generated alert summaries |
| **Result Comparison** | Capture command outputs before/after changes, side-by-side diff with AI analysis |
| **Config Rollback** | Preview and execute configuration rollback on routers with AI risk assessment |
| **8 Protocol Specialists** | OSPF, IS-IS, BGP, LDP/MPLS, L2VPN/EVPN, System Health, Security, QoS/CoS |
| **18 Smart Scripts** | Pre-defined diagnostic scripts covering connectivity, protocol state, health, security, topology, performance |
| **Evidence-Based Diagnosis** | Every finding cites specific command output; no hallucination allowed |
| **Safe Config Push** | Human approval required, change window enforcement, pre/post state capture, auto-rollback |
| **RAG Knowledge Base** | 184KB Junos knowledge + 7 PDFs -> chunked -> embedded -> semantic retrieval at query time |
| **Executive Reporting** | Markdown + HTML reports with severity heatmaps, risk scoring, remediation playbooks |
| **Self-Learning** | Lessons from corrections stored, resolution database grows, baselines tracked |
| **Compliance Auditing** | 20+ CIS-aligned checks (NTP, SSH, SNMP, BGP auth, OSPF auth, RE protection, etc.) |

### Technology Stack

| Component | Technology |
|---|---|
| **Web Backend** | Flask 3.0+ + Flask-SocketIO 5.3+ + Flask-CORS 4.0+ (port 5555) |
| **Web Frontend** | Single-Page Application (HTML5 + CSS3 + JavaScript) — 21 views |
| **Topology Engine** | D3.js v7.9.0 (force-directed, hierarchical, radial, circular layouts) |
| **Real-Time Comms** | Socket.IO 4.7.5 (WebSocket with fallback) |
| **Icon System** | Lucide Icons (SVG icon library, locally bundled) |
| **Typography** | Inter + JetBrains Mono (WOFF2, locally bundled) |
| **AI Model** | GPT-OSS (13B) via Ollama (`http://127.0.0.1:11434`) |
| **Embedding Model** | `nomic-embed-text` (274MB, 768-dim) via Ollama |
| **MCP Server** | Python + Starlette + Junos PyEZ (`http://127.0.0.1:30030/mcp/`) |
| **MCP Client/Bridge** | Python 3.12 + httpx (async HTTP) + Rich (terminal UI) |
| **Quantum Engine** | Pure Python — Tarjan, BFS, Simulated Annealing, Quantum Walk, Louvain (~900 lines) |
| **Network Devices** | Juniper vMX routers (SSH/NETCONF via PyEZ) |
| **Protocols Covered** | OSPF, IS-IS, BGP, LDP, MPLS, RSVP-TE, L3VPN, L2VPN, EVPN, BFD, QoS/CoS |
| **Persistence** | 5 SQLite databases + JSON caches + Pickle vector store |
| **Terminal UI** | Rich library (panels, tables, progress bars, colored output) |
| **External Dependencies** | **NONE** — all libraries, fonts, and assets bundled locally |

### Codebase Summary

| File | Lines | Purpose |
|---|---|---|
| `web_ui/app.py` | 3,622 | Flask backend — 101 API routes, MCP bridge, AI engine, scheduler, workflow engine |
| `web_ui/static/js/noc.js` | 2,594 | Frontend JavaScript — all 21 views, topology, AI chat, WebSocket |
| `web_ui/static/css/noc.css` | 4,146 | Full theme system — dark/light mode, glass-morphism, responsive |
| `web_ui/templates/index.html` | 1,277 | SPA HTML — 21 view sections, navigation, modals |
| `ollama_mcp_client.py` | 12,627 | Terminal AI client — audit engine, specialists, reasoning, tool loop |
| `hypered_brain.py` | 1,963 | 6-layer autonomous investigation engine |
| `reasoning_engine.py` | 1,488 | 7-stage reasoning pipeline |
| `network_analysis.py` | 2,149 | 8 analysis modules — security, DNS, flow, alerts |
| `web_ui/quantum_engine.py` | 906 | 5 quantum-inspired graph algorithms |
| `junos-mcp-server/jmcp.py` | 1,786 | MCP server — Junos PyEZ gateway |
| `kb_vectorstore.py` | 798 | RAG vector store with semantic search |
| **Total** | **~33,000+** | Full-stack AI NOC platform |

---

## 2. Quick Start — Zero-Config Onboarding Guide

### Prerequisites

Before you begin, ensure you have these three services ready:

| Service | What It Is | How to Get It |
|---|---|---|
| **MCP Server** | The Junos MCP Server that connects to your routers | See [Section 4.1](#41-junos-mcp-server-jmcppy) — runs on port 30030 |
| **Ollama** | Local AI model server | Install from [ollama.ai](https://ollama.ai), pull `gpt-oss` model |
| **Devices** | Your Juniper routers with SSH/NETCONF access | Configure in `junos-mcp-server/devices.json` |

### Step 1: Install Dependencies

```bash
# Clone or download the project
cd "MCP Localhost"

# Install Python dependencies for the web UI
cd web_ui
pip install flask flask-socketio flask-cors httpx pyyaml jinja2

# Install MCP server dependencies
cd ../junos-mcp-server
pip install -r requirements.txt
```

### Step 2: Configure Your Devices

Create or edit `junos-mcp-server/devices.json`:

```json
{
    "PE1": {
        "ip": "192.168.1.1",
        "port": 22,
        "username": "admin",
        "auth": {
            "type": "ssh_key",
            "ssh_key_path": "/home/user/.ssh/id_rsa"
        }
    },
    "PE2": {
        "ip": "192.168.1.2",
        "port": 22,
        "username": "admin",
        "auth": {
            "type": "password",
            "password": "YourPassword"
        }
    }
}
```

**Authentication options:**
- `ssh_key` — path to private key file (recommended)
- `password` — plaintext password (for lab environments)

### Step 3: Configure the System

Edit `config.yaml` (or use the defaults):

```yaml
mcp:
  url: "http://127.0.0.1:30030/mcp/"
  call_timeout: 120.0

ai:
  ollama_url: "http://127.0.0.1:11434"
  model: "gpt-oss"
  context_window: 32768
  temperature: 0.12
```

### Step 4: Start the Services

```bash
# Terminal 1: Start the MCP Server
cd junos-mcp-server
python jmcp.py
# Server starts on http://127.0.0.1:30030/mcp/

# Terminal 2: Start Ollama with your AI model
ollama serve
# Then in another terminal: ollama pull gpt-oss

# Terminal 3: Start the Web UI
cd web_ui
python app.py
# NOC starts on http://127.0.0.1:5555
```

### Step 5: Open the Web UI

1. Open your browser to `http://127.0.0.1:5555`
2. **First-run detection**: The dashboard will show a **Bootstrap Banner** indicating that no golden configs have been synced yet
3. Click **"Sync All Configs from MCP"** — this pulls the running configuration from every device via MCP and saves them as golden configs
4. Wait for the sync to complete (progress shown in real-time)
5. Once synced, the topology map, device inventory, config views, and all analysis features are fully populated

### Step 6: Verify Everything Works

After the initial sync, verify:

| What to Check | How |
|---|---|
| **MCP Connection** | Check the green "MCP" indicator in the header bar |
| **Ollama Connection** | Check the green "Ollama" indicator in the header bar |
| **Topology** | Click "Topology" in the nav — you should see your network graph |
| **Devices** | Click "Devices" — all your routers should appear with roles and protocol counts |
| **Configs** | Click "Configs" — all golden configs should be listed |
| **AI Chat** | Open AI Chat, type "Give me a network health summary" |

### What If I Don't Have `devices.json`?

The system can auto-discover devices from the MCP server itself. If `devices.json` is missing, the NOC will:

1. Query the MCP server for its router list via `get_router_list`
2. Parse the response and build a device inventory
3. Use that inventory for all views

You can then sync configs via the Bootstrap banner.

### What If Golden Configs Are Missing?

Every endpoint that needs a golden config has an **automatic MCP fallback**:

- **Config viewer**: Auto-fetches from MCP and saves as golden config
- **Config diff**: Auto-pulls running config via MCP for comparison
- **Compliance audit**: Uses live config from MCP if no golden config exists
- **Security scan**: Pulls live config per-router as needed
- **Hardening report**: Falls back to MCP live config

This means the tool works **from the very first click** — no manual file creation required.

---

## 3. System Architecture

### High-Level Architecture Diagram (v21.2)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER                                           │
│              Web Browser (http://127.0.0.1:5555)                           │
│        ┌───────────────────────────────────────────────────────┐           │
│        │                 WEB UI (SPA)                          │           │
│        │  21 Views · D3.js Topology · AI Copilot · Workflows  │           │
│        │  Dark/Light Theme · Lucide Icons · Inter/JetBrains   │           │
│        └─────────────────────┬─────────────────────────────────┘           │
│                               │  REST API (101 endpoints) + WebSocket     │
└───────────────────────────────┼────────────────────────────────────────────┘
                                │
┌───────────────────────────────▼────────────────────────────────────────────┐
│                   FLASK BACKEND (app.py — 3,622 lines)                     │
│                   Port 5555 · Flask-SocketIO · ThreadPoolExecutor          │
│                                                                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐     │
│  │ 101 REST │ │ WebSocket│ │ Scheduler│ │ Workflow │ │ Quantum      │     │
│  │ API      │ │ Events   │ │ Engine   │ │ Engine   │ │ Engine       │     │
│  │ Endpoints│ │ (6)      │ │ (bg loop)│ │ v2 (12   │ │ (5 algos)   │     │
│  │          │ │          │ │          │ │  steps)  │ │              │     │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └──────┬───────┘     │
│       │             │            │             │              │             │
│  ┌────▼─────────────▼────────────▼─────────────▼──────────────▼──────────┐  │
│  │              MCP BRIDGE + OLLAMA INTERFACE + BOOTSTRAP               │  │
│  │    httpx → MCP Server (JSON-RPC)   │   httpx → Ollama (Chat/Stream) │  │
│  │    Auto-sync configs on demand     │   AI Analysis for all features  │  │
│  └─────────────────┬───────────────────┴──────────────────────────────────┘  │
│                    │                                                         │
│  ┌─────────────────▼─────────────────────────────────────────────────────┐  │
│  │  5 SQLite DBs: scheduled_tasks · device_pools · notifications        │  │
│  │                 audit_history · analysis_memory                       │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬───────────────────────────────────────────┘
                                 │  HTTP (JSON-RPC)    │  HTTP (Ollama API)
                    ┌────────────▼───────┐    ┌───────▼──────────┐
                    │  JUNOS MCP SERVER  │    │  OLLAMA (Local)  │
                    │  jmcp.py — 1,786L  │    │  GPT-OSS 13B    │
                    │  Port 30030        │    │  Port 11434      │
                    └────────┬───────────┘    └──────────────────┘
                             │  SSH (NETCONF via PyEZ)
┌────────────────────────────▼───────────────────────────────────────────────┐
│                    JUNIPER vMX LAB (N Routers)                             │
│                                                                            │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐       │
│  │ P11 │ │ P12 │ │ P13 │ │ P14 │ │ P21 │ │ P22 │ │ P23 │ │ P24 │       │
│  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘       │
│  ┌──┴─────┐ ┌──┴─────┐ ┌──┴─────┐                                       │
│  │  PE1   │ │  PE2   │ │  PE3   │  (Provider Edge — VPN services)        │
│  └────────┘ └────────┘ └────────┘                                        │
└────────────────────────────────────────────────────────────────────────────┘
```

### Communication Architecture

```
Browser ←→ Flask (REST + WebSocket) ←→ MCP Server (JSON-RPC 2.0 + SSE) ←→ Routers (SSH)
                                    ←→ Ollama (Chat/Stream/Embed)
```

### Bootstrap Flow (First Run)

```
User opens http://127.0.0.1:5555
    │
    ▼
app.py starts → auto-creates all directories (golden_configs, workflows, results, etc.)
    │
    ├─ load_devices() → tries devices.json
    │   └─ FALLBACK: queries MCP get_router_list → parses router names → builds device dict
    │
    ├─ build_topology_from_golden_configs() → no .conf files found
    │   └─ FALLBACK: builds minimal topology from device inventory (names + roles)
    │
    ▼
Dashboard renders → checkBootstrap() → GET /api/bootstrap/status
    │
    ├─ bootstrapped: false, missing_configs: ["P11","P12","PE1",...]
    │
    ▼
Bootstrap Banner appears: "Welcome! Sync All Configs from MCP"
    │
    ▼
User clicks "Sync" → POST /api/bootstrap/sync
    │
    ├─ For each router: mcp_get_config(router) → save as golden_configs/ROUTER.conf + .meta
    │
    ▼
All configs synced → Topology populated → Dashboard fully functional
```

---

## 4. Component Deep Dive

### 4.1 Junos MCP Server (`jmcp.py`)

**Location:** `junos-mcp-server/jmcp.py`
**Lines of Code:** 1,786
**Language:** Python 3.12
**Framework:** Starlette (ASGI) + MCP SDK
**Network Library:** Junos PyEZ (NETCONF over SSH)
**Port:** 30030

#### Purpose
The MCP Server is the **gateway between AI and the physical network**. It exposes Junos router operations as MCP tools that any AI client can invoke via JSON-RPC 2.0 over HTTP with SSE streaming.

#### MCP Tools Exposed

| Tool Name | Description | Parameters |
|---|---|---|
| `execute_junos_command` | Run a single Junos CLI command on one router | `router_name`, `command`, `timeout` |
| `execute_junos_command_batch` | Run the **same** command on **multiple** routers in parallel | `router_names[]`, `command`, `timeout` |
| `gather_device_facts` | Collect device facts (hostname, model, version, serial, uptime) | `router_name`, `timeout` |
| `get_junos_config` | Retrieve the full running configuration | `router_name` |
| `junos_config_diff` | Show config diff against a rollback version (1-49) | `router_name`, `version` |
| `load_and_commit_config` | Push configuration and commit | `router_name`, `config_text`, `commit_comment` |
| `render_and_apply_j2_template` | Render Jinja2 template with YAML vars, optionally apply | `template_content`, `vars_content`, `router_name`, `apply_config`, `dry_run` |
| `get_router_list` | List all configured routers (names, IPs, ports) | -- |
| `add_device` | Add a new device to the server's device inventory | `device_name`, `device_ip`, `device_port`, `username`, `ssh_key_path` |
| `reload_devices` | Reload the device inventory from a JSON file | `file_name` |

#### Batch Execution Architecture

The batch command execution uses a **ThreadPoolExecutor** for true parallel SSH:

```python
async def handle_execute_junos_command_batch(arguments, context):
    """Execute same command on N routers using thread pool for parallelism."""
    router_names = arguments["router_names"]
    command = arguments["command"]
    
    with ThreadPoolExecutor(max_workers=len(router_names)) as executor:
        futures = {
            executor.submit(execute_on_device, name, command): name
            for name in router_names
        }
        for future in as_completed(futures):
            # Collect results as they complete
```

Each router connection is an independent SSH/NETCONF session via PyEZ:

```python
with Device(host=ip, port=port, user=username, passwd=password) as dev:
    result = dev.cli(command, warning=False)
```

#### Device Configuration (`devices.json`)

```json
{
    "PE1": {
        "ip": "192.168.1.1",
        "port": 22,
        "username": "admin",
        "auth": {
            "type": "ssh_key",
            "ssh_key_path": "/home/user/.ssh/id_rsa"
        }
    },
    "P11": {
        "ip": "192.168.1.10",
        "port": 22,
        "username": "admin",
        "auth": {
            "type": "password",
            "password": "YourPassword"
        }
    }
}
```

#### Starting the MCP Server

```bash
cd junos-mcp-server
python jmcp.py
# Or with make:
make run
```

The server listens on `http://127.0.0.1:30030/mcp/` and accepts JSON-RPC 2.0 requests.

---

### 4.2 Ollama MCP Client / Bridge (`ollama_mcp_client.py`)

**Location:** `ollama_mcp_client.py`
**Lines of Code:** 12,627
**Language:** Python 3.12 (async/await throughout)

This is the **central nervous system** of the project — the largest file, containing the interactive chat system, audit engine, specialist AI layers, tool-calling loop, and all integration logic.

#### Major Subsystems

| Subsystem | Lines (approx.) | Function |
|---|---|---|
| **MCP Communication Layer** | 2700-2970 | `mcp_initialize()`, `mcp_call_tool()`, `run_batch()`, `run_single()` |
| **Ollama AI Interface** | 3544-3700 | `ollama_chat()` — sends messages to GPT-OSS via Ollama API |
| **Query Classifier** | 3797-3960 | `classify_query()` — routes queries to appropriate handler |
| **Structured Reasoning** | 5628-5900 | `structured_reasoning_chain()` — multi-step problem decomposition |
| **Mind-Map Reasoning** | 5278-5600 | `mind_map_reasoning()` — hierarchical investigation branches |
| **Protocol Specialists** | 6193-6900 | 8 specialist functions (OSPF, BGP, IS-IS, LDP, L2VPN, Health, Security, QoS) |
| **Specialist Orchestrator** | 7200-7500 | Parallel execution of specialists with dependency ordering |
| **Full Audit Engine** | 7848-10300 | `run_full_audit()` — 7-phase comprehensive network audit |
| **System Prompt** | 7638-7800 | JNCIE-SP level AI instructions with reasoning pipeline |
| **Main Entry Point** | 10319-10500 | `main()` — startup, device discovery, interactive loop |
| **Interactive Tool Loop** | 12400-12627 | AI tool-calling loop with safety interception |
| **Compliance Engine** | 2173-2700 | 20+ CIS-aligned compliance checks |
| **Change Management** | 1543-1600 | Pre/post state capture, change window enforcement |
| **Topology Builder** | 4972-5200 | Live topology from LLDP + iBGP + IS-IS fusion |
| **Config Drift Detection** | 1200-1500 | Golden config comparison with diff |

#### Key Functions

| Function | Purpose |
|---|---|
| `mcp_call_tool(client, sid, tool_name, arguments)` | Fundamental MCP JSON-RPC communication |
| `run_batch(client, sid, command, router_names, label)` | Execute command on multiple routers via MCP batch |
| `run_single(client, sid, command, router_name, label)` | Execute command on a single router |
| `ollama_chat(messages, tools, retries)` | Send conversation to GPT-OSS via Ollama API |
| `classify_query(user_input)` | Route query to optimal handler (audit/troubleshoot/complex/config/compare/knowledge/general) |
| `structured_reasoning_chain(query, ...)` | 7-stage reasoning pipeline (CLASSIFY → DIAGNOSE → PRESCRIBE) |
| `mind_map_reasoning(query, ...)` | Hierarchical problem decomposition for ultra-complex queries |
| `run_full_audit()` | Complete 7-phase network audit with executive report generation |

#### Query Classification

| Query Type | Handler | Example |
|---|---|---|
| `audit` | Full audit pipeline | "run a full audit" |
| `troubleshoot` | Structured reasoning chain | "why can't PE1 reach PE3?" |
| `complex` | Mind-map reasoning | "analyze the full MPLS topology" |
| `config` | Config push with safety | "configure OSPF on PE1" |
| `compare` | Config diff tool | "compare P11 and P12 configs" |
| `knowledge` | RAG-only (no tools) | "explain OSPF area types" |
| `general` | Standard tool-calling loop | "show BGP summary on PE1" |

---

### 4.3 Hypered Brain Engine (`hypered_brain.py`)

**Location:** `hypered_brain.py`
**Lines of Code:** 1,963
**Version:** v18.0
**Exports:** 25 public symbols

This is the **flagship intelligence module** — a 6-layer autonomous investigation engine.

#### 6-Layer Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    USER QUERY / TRIGGER                             │
└────────────────────────────┬────────────────────────────────────────┘
                             │
  LAYER 0: PERCEPTION — Intent Classification & Strategy Planning
  LAYER 1: EXECUTION — Adaptive Parallel Pipeline (smart scripts + AI probes)
  LAYER 2: ANALYSIS — Progressive AI Reasoning (cross-device correlation)
  LAYER 3: VALIDATION — Self-Audit & Gap Filling (confidence gating)
  LAYER 4: SYNTHESIS — Root Cause & Prescriptive Fix (evidence-cited)
  LAYER 5: MEMORY — Cross-Session Learning (fingerprints, baselines, resolutions)
```

#### Core Data Structures

| Structure | Purpose |
|---|---|
| `GatheredFact` | Single evidence point with source, device, category, value, raw evidence, confidence, anomaly flag |
| `FactAccumulator` | Deduplicated evidence store with contradiction detection and cross-device anomaly matrix |
| `AdaptiveConcurrency` | Self-tuning parallelism (3-6 concurrent SSH sessions based on gateway latency) |
| `AIProbe` | AI-directed data collection request with device, command, reason, and priority |

---

### 4.4 Reasoning Engine (`reasoning_engine.py`)

**Location:** `reasoning_engine.py`
**Lines of Code:** 1,488
**Version:** v15.0

Implements a 7-stage reasoning pipeline:

```
CLASSIFY → DECOMPOSE → HYPOTHESIZE → INVESTIGATE → DIAGNOSE → SYNTHESIZE → PRESCRIBE
```

Key innovations:
- **Hypothesis-driven investigation** (Popperian method)
- **Protocol FSM anchoring** — maps findings to protocol state machines
- **Cascade Graph Walking** using `PROTOCOL_DEPENDENCY_GRAPH`

---

### 4.5 Network Analysis Engine (`network_analysis.py`)

**Location:** `network_analysis.py`
**Lines of Code:** 2,149
**Version:** v16.0

Provides 8 analysis modules:

| Module | Capabilities |
|---|---|
| **Packet Capture** | Protocol-level analysis via Junos commands |
| **DNS Intelligence** | DNS configuration auditing and resolution testing |
| **Security Audit** | 13 security checks (SSH, SNMP, NTP, firewall, etc.) |
| **Flow Analysis** | Traffic flow tracking and analysis |
| **Alert Engine** | 9 threshold-based alert rules |
| **Log Forensics** | Log parsing, pattern detection, and correlation |
| **Device Profiler** | OS fingerprinting and capability detection |
| **Persistent Memory** | Cross-session analysis storage and baseline tracking |

---

### 4.6 Knowledge Base Vector Store (`kb_vectorstore.py`)

**Location:** `kb_vectorstore.py`
**Lines of Code:** 798

Implements a local RAG pipeline:

```
KNOWLEDGE_BASE.md (184KB+) + 7 Juniper PDFs
    → chunk by heading (200-400 tokens)
    → anchor with section prefix
    → embed with nomic-embed-text (768-dim)
    → store in kb_vectors.pkl
    → at query time: multi-query embed → cosine similarity + keyword boost
    → threshold 0.55 → top-K retrieval → inject into AI prompt
```

---

### 4.7 PDF Knowledge Ingester (`ingest_pdfs.py`)

**Location:** `ingest_pdfs.py`
**Lines of Code:** 321

Extracts content from 7 Juniper certification PDFs using PyMuPDF and appends to `KNOWLEDGE_BASE.md`:

| PDF | Topic |
|---|---|
| `JNCIA.pdf` | Juniper Networks Certified Internet Associate |
| `Junos Intermediate Routing JIR.pdf` | Intermediate routing concepts |
| `Advanced Junos Service Provider Routing (AJSPR).pdf` | Advanced SP routing |
| `Junos MPLS Fundamentals JMF.pdf` | MPLS, LDP, RSVP-TE fundamentals |
| `Junos Service Provider Switching JSPX.pdf` | Layer 2 switching, VLANs |
| `Junos Layer 2 VPNs JL2V.pdf` | L2VPN, VPLS, pseudowires |
| `Layer 3 VPNs.pdf` | L3VPN (VRF, route-target, route-distinguisher) |

---

### 4.8 Configuration System (`config.yaml`)

**Location:** `config.yaml`
**Lines:** 298

Centralizes all settings:

```yaml
# MCP Server Connection
mcp:
  url: "http://127.0.0.1:30030/mcp/"
  call_timeout: 120.0

# AI Engine
ai:
  ollama_url: "http://127.0.0.1:11434"
  model: "gpt-oss"
  context_window: 32768
  temperature: 0.12

# Hypered Brain tuning
hypered_brain:
  max_passes: 3
  confidence_threshold: 0.70
  max_concurrent_sessions: 6

# Compliance checks (20+)
compliance:
  checks:
    - ntp_configured
    - syslog_configured
    - snmp_no_public
    - ssh_only
    - login_banner
    - rescue_config
    # ... and more

# Device roles
device_roles:
  PE: [PE1, PE2, PE3]
  P: [P11, P13, P14, P21, P23, P24]
  RR: [P12, P22]

# Change management windows
change_management:
  allowed_hours: [2, 3, 4, 5]  # 2am-5am
  require_approval: true
```

---

## 5. Web UI — Full-Stack Network Operations Dashboard

### 5.1 Architecture & Technology Stack

The Web UI is a **single-page application (SPA)** served by a Flask backend, providing a complete visual interface to every NOC capability.

#### Backend (`web_ui/app.py` — 3,622 lines)

| Component | Details |
|---|---|
| **Framework** | Flask 3.0+ with Flask-SocketIO 5.3+ |
| **Async Mode** | `threading` (ThreadPoolExecutor with 4 workers) |
| **Port** | 5555 (configurable via `NOC_PORT` env var) |
| **API Endpoints** | 101 REST API routes |
| **MCP Bridge** | httpx async HTTP client → `http://127.0.0.1:30030/mcp/` |
| **AI Bridge** | httpx → `http://127.0.0.1:11434/api/chat` (Ollama) |
| **Real-Time** | Flask-SocketIO WebSocket (6 event handlers) |
| **Background** | Scheduler loop (10-second interval) for recurring tasks |
| **Databases** | 5 SQLite databases (scheduled_tasks, device_pools, notifications, audit_history, analysis_memory) |
| **Auto-Bootstrap** | Zero-config onboarding — auto-creates dirs, auto-fetches configs from MCP |

#### Frontend (`web_ui/templates/index.html` + `web_ui/static/`)

| Component | Details |
|---|---|
| **HTML** | Single-page app with 21 view sections (show/hide via JS) |
| **CSS** | `noc.css` (4,146 lines) + `fonts.css` (27 lines) — dark/light theme |
| **JavaScript** | `noc.js` (2,594 lines) — all frontend logic |
| **Topology** | D3.js v7.9.0 (273KB, locally bundled) |
| **Real-Time** | Socket.IO 4.7.5 (49KB, locally bundled) |
| **Icons** | Lucide Icons (383KB, locally bundled) |
| **Fonts** | Inter (225KB) + JetBrains Mono (54KB) — WOFF2, locally bundled |

#### Local-Only Asset Bundle

All external dependencies are bundled locally — zero CDN calls, zero external network requests:

```
web_ui/static/
├── css/
│   ├── noc.css          (4,146 lines — full theme system)
│   └── fonts.css        (27 lines — @font-face declarations)
├── js/
│   ├── noc.js           (2,594 lines — all frontend logic)
│   ├── d3.v7.min.js     (273KB — D3.js topology engine)
│   ├── socket.io.min.js (49KB — real-time WebSocket)
│   └── lucide.min.js    (383KB — SVG icon library)
└── fonts/
    ├── inter.woff2          (225KB — UI typography)
    └── jetbrains-mono.woff2 (54KB — code typography)
```

---

### 5.2 Navigation & Layout System

The UI features a **glass-morphism header** with organized navigation:

#### Header Bar
- **Logo**: SVG network icon with "Junos AI NOC" branding + version badge ("v21.2")
- **AI Copilot Toggle**: Opens the persistent AI sidebar from any view
- **Theme Toggle**: Switches between dark and light modes (sun/moon icon)
- **Connection Status**: Live indicator showing MCP + Ollama connectivity
- **Mobile Menu**: Hamburger menu for responsive layouts

#### Navigation Structure

| Group | Views | Description |
|---|---|---|
| **Primary** | Dashboard, Topology, AI Chat | Core operations — always visible in nav bar |
| **Infrastructure** | Devices, Device Pools, Ping & Reachability, Path Finder, Discovery | Device management, network testing, infrastructure scanning |
| **Configuration** | Golden Configs, Templates, Validation, Git Export, Compare | Config lifecycle management |
| **Automation** | Workflows, Scheduler, Log Forensics, Alerts, Config Rollback | Operational automation & monitoring |
| **Analysis** | Traffic Analysis, Security Analysis, DNS Diagnostics, Capacity Planning | Advanced AI-powered analytics |

Navigation uses **dropdown menus** for each group, keeping the header clean while providing instant access to all 21 views.

---

### 5.3 Dashboard View

The dashboard provides a **real-time overview** of the entire network at a glance.

#### Bootstrap Banner (First Run)
On first run (no golden configs synced), a prominent banner appears:
- "Welcome to Junos AI NOC" message
- **Sync All Configs from MCP** button — one-click full onboarding
- Progress indicator during sync
- Automatically dismisses after successful sync

#### AI Contextual Bar
A smart bar at the top with quick AI actions:
- **Health Check** — instant AI health assessment
- **Anomalies** — detect network anomalies
- **Optimize** — AI recommendations for network improvements

#### Stats Cards (6 metrics)

| Card | Metric | Color Accent |
|---|---|---|
| Total Devices | Count of all managed routers | Green |
| Physical Links | Number of physical connections | Blue |
| iBGP Sessions | Active BGP peering count | Purple |
| Redundancy Score | Network redundancy percentage | Teal |
| Graph Diameter | Maximum shortest path (hops) | Amber |
| Points of Failure | SPOF count (Tarjan's algorithm) | Rose |

#### Dashboard Panels
- **Network Topology Overview** — Mini D3.js force-directed topology preview with "Expand" button
- **Device Roles** — SVG donut chart showing PE/P/RR distribution
- **Protocol Summary** — Horizontal bar chart of protocol counts (IS-IS, BGP, LDP, OSPF)
- **Device Inventory Table** — Searchable table with columns: Device, Role, Loopback, Interfaces, IS-IS, BGP, LDP, Status

---

### 5.4 Network Topology Visualization

A full-screen **interactive D3.js topology** with advanced features.

#### AI Contextual Bar
- **Redundancy** — AI analysis of network redundancy
- **Capacity** — AI capacity planning recommendations

#### Layout Options

| Layout | Algorithm |
|---|---|
| Force-Directed | D3.js force simulation with collision detection |
| Hierarchical | Top-down tree layout by device role |
| Radial | Circular layout radiating from core |
| Circular | Even circular distribution |

#### Layer Toggles
Toggle visibility of overlay layers:
- **IS-IS** links (checked by default)
- **iBGP** sessions (checked by default)
- **LDP** sessions
- **Labels** (device names, checked by default)

#### Legend
- PE Router (color-coded dot)
- P Router (color-coded dot)
- Route Reflector (color-coded dot)
- Physical Link (solid line)
- iBGP Session (dashed line)

#### Node Interaction
Clicking a node opens a **detail panel** with:
- Device name, role, loopback IP
- Interface list with protocol state
- Neighbor adjacencies
- Quick actions (view config, ping, run command)

---

### 5.5 AI Command Center (Chat)

A full **conversational AI interface** with streaming responses.

#### Features
- **SSE Streaming**: AI responses stream word-by-word via Server-Sent Events (`/api/ai/stream`)
- **Markdown Rendering**: Responses rendered with proper formatting
- **Context Injection**: Each message includes device inventory, topology state, and conversation history
- **Local Fallback**: If Ollama is unavailable, returns topology/BGP/SPOF info from local data
- **Multi-line Input**: Textarea supports Shift+Enter for multi-line queries

#### Quick Action Buttons

| Button | Prompt |
|---|---|
| Health Assessment | "Give me a full network health assessment" |
| SPOF + Remediation | "What are the single points of failure and how to fix them?" |
| BGP Audit | "Audit all BGP sessions and identify issues" |
| Security Audit | "Run a full security compliance audit on all routers" |
| Best Practice Check | "Compare current configs against best practices" |
| Audit Trail | "Show my recent actions and AI audit trail" |

---

### 5.6 AI Copilot Sidebar

A **persistent slide-out sidebar** available from every view, providing context-aware AI assistance.

#### Sections

| Section | Description |
|---|---|
| **Action Audit Trail** | Chronological log of all user actions with timestamps and badge count |
| **AI Insights** | Context-aware suggestions based on the current view and recent activity |
| **Mini Chat** | Embedded chat with SSE streaming — ask quick questions without leaving the current view |
| **Quick Actions** | View-specific AI actions (e.g., "Audit Config" on Configs view, "Redundancy Check" on Topology) |

#### Copilot Behavior by View

| Active View | AI Context |
|---|---|
| Dashboard | Network health stats, device counts, protocol state |
| Topology | Graph metrics, SPOF nodes, redundancy analysis |
| Configs | Current config content for audit, drift detection |
| Templates | Template variables and rendering context |
| Discovery | Infrastructure scan results for analysis |
| Traffic | Protocol statistics and flow data |
| Security | Security audit findings and threat indicators |
| DNS | DNS configuration consistency |

---

### 5.7 Device Inventory

Displays **all managed devices** as visual cards in a responsive grid.

Each card shows:
- Device name and role badge (PE/P/RR)
- Loopback IP address
- Interface count
- Protocol status indicators (IS-IS, BGP, LDP)
- Connection status

---

### 5.8 Device Pools

Group devices by role, location, or function with AI assistance.

#### Features
- **Create Pool**: Name, description, color picker, multi-select devices, tags
- **AI Recommend Pools**: AI analyzes topology and recommends optimal groupings based on device roles, protocol participation, and redundancy
- **Pool Cards**: Visual cards with member count, color coding, and tag badges
- **CRUD Operations**: Create, read, update, delete pools (SQLite-backed)

---

### 5.9 Ping & Reachability

Network reachability testing via MCP with AI analysis.

#### Controls
- **Single Ping**: Select a router and ping it via MCP (`show system uptime`)
- **Sweep All Routers**: Ping all routers in parallel and display a results grid
- **AI Analyze**: AI analyzes ping results for patterns, latency anomalies, and reachability gaps

---

### 5.10 Path Finder

IS-IS metric-based **shortest path analysis** between any two routers.

#### Features
- Source and target router selection dropdowns
- **Dijkstra shortest path** calculation using IS-IS metrics from golden configs
- Path visualization with hop-by-hop details (interfaces, metrics)
- Dedicated topology SVG showing the computed path highlighted on the network graph

---

### 5.11 Configuration Management

Golden config viewing, diffing, and cross-device search.

#### AI Contextual Bar
- **Audit Config**: AI reviews the currently viewed configuration
- **Drift Check**: AI compares running config against golden baseline
- **Sync from MCP**: Pull fresh configs from all devices via MCP

#### Features

| Feature | Description |
|---|---|
| **Config List** | Sidebar showing all golden configs |
| **Config Viewer** | Syntax-highlighted config display with line numbers |
| **Config Diff** | Side-by-side diff (running vs golden) using difflib |
| **Cross-Device Search** | Search across all configs with optional regex support |
| **Auto-Fetch** | If a golden config is missing, it's automatically pulled from MCP and saved |

---

### 5.12 Template Engine

Jinja2 template rendering and **live deployment** to routers via MCP.

#### Layout
- **Template Sidebar**: List of available templates (from `templates/` directory)
- **Template Source**: Read-only display of the selected template content
- **Variables Input**: YAML/JSON editor for template variables
- **Rendered Output**: Preview of the rendered configuration

#### Available Templates

| Template | Purpose | Key Variables |
|---|---|---|
| `ospf_p2p.j2` | OSPF point-to-point interfaces | `interface`, `area`, `hello`, `dead` |
| `bgp_ibgp.j2` | iBGP session configuration | `local_as`, `neighbor_ip`, `group_name`, `cluster_id` |
| `mpls_ldp.j2` | MPLS/LDP interface enablement | `interfaces[]` |
| `system_hardening.j2` | Security hardening | `ntp_servers[]`, `syslog_hosts[]`, `snmp_community` |

---

### 5.13 Data Validation

Validate command outputs against patterns with AI compliance auditing.

#### Validation Modes

| Mode | Description |
|---|---|
| **Single Validation** | Run a command on one router, check output against a pattern (contains, regex, not_contains, exact) |
| **Batch Validation** | Run the same validation rule against all routers simultaneously |
| **AI Compliance Audit** | AI reviews configs against 20+ best practice checks (NTP, SSH, SNMP, BGP auth, IS-IS auth, etc.) |

---

### 5.14 Git Export (Config Version Control)

Version-control golden configs with **AI-generated commit messages**.

#### Features
- **Init Repo**: Initialize a Git repository in the export directory
- **Export & Commit**: Copy all golden configs, generate AI commit message, and commit
- **Commit History**: View the full Git log with commit messages and timestamps
- **Diff Viewer**: View the diff for any commit

---

### 5.15 Result Comparison

Capture command outputs and **compare them side-by-side** with AI diff analysis.

#### Workflow
1. **Capture**: Run a command on a router and save the output (e.g., "bgp-before-change")
2. **Compare**: Select two captured results and generate a side-by-side diff
3. **AI Analysis**: AI analyzes the differences and explains implications

---

### 5.16 Workflow Builder

A visual **workflow builder** for chaining MCP operations, templates, AI analysis, and conditions.

#### 12 Step Types

| Step Type | Description |
|---|---|
| `command` | Execute a single MCP command on a router |
| `batch` | Execute a command on multiple routers in parallel |
| `template` | Render a Jinja2 template with variables |
| `deploy` | Deploy rendered config to a router via MCP |
| `ai_analyze` | Send data to AI for analysis and get recommendations |
| `condition` | Check a condition (regex match, value comparison) — branch logic |
| `wait` | Pause execution for a specified duration |
| `rest_call` | Make an HTTP REST API call (GET/POST/PUT/DELETE) with optional AI analysis of response |
| `python_snippet` | Execute a sandboxed Python code snippet |
| `ping_sweep` | Ping all routers and collect results |
| `validate` | Validate command output against a pattern |
| `notify` | Send a notification to a configured channel |

#### Execution
- Steps execute sequentially with variable substitution (`{{variable_name}}`)
- Step references: `$step_N` uses output from step N
- Execution results displayed in real-time via WebSocket
- Condition steps enable branching (skip remaining steps on failure)

---

### 5.17 Task Scheduler

CRON-style **scheduled command execution** with background scheduler.

#### Create Task Form
- Task name (e.g., "BGP Health Check")
- Interval selection: 30s, 5m, 15m, 1h, 6h, 24h
- CRON expression support (e.g., `*/5 * * * *` for every 5 minutes)
- CRON aliases: `@hourly`, `@daily`, `@weekly`, `@monthly`, `@yearly`
- Command to execute
- Target routers (multi-select)

#### Background Engine
A background thread runs on a 10-second loop, checking all active tasks and executing any whose interval has elapsed. Results are stored in SQLite, emitted via WebSocket in real-time.

#### Calendar View
`GET /api/scheduled-tasks/calendar` returns all scheduled and completed tasks formatted as calendar events.

---

### 5.18 Log Forensics

Browse, filter, and **AI-analyze** system logs.

#### Features
- **Log File Sidebar**: Lists all log files from the `logs/` directory
- **Level Filter**: Show only ERROR, WARNING, INFO, or DEBUG entries
- **Text Search**: Full-text search within the selected log file
- **Tail Lines**: Show only the last N lines
- **AI Analyze**: Send log content to AI for pattern detection, error correlation, and root cause analysis

---

### 5.19 Notification Channels

Configure **Slack, Mattermost, and webhook** alert channels.

#### Features
- Create channels with name, type (Slack/Mattermost/Webhook), and webhook URL
- Send notifications with severity classification (Info/Warning/Critical)
- **AI Summary**: AI generates actionable alert summaries from recent events
- Notification history with delivery status tracking (SQLite-backed)

---

### 5.20 Config Rollback

Preview and execute **configuration rollback** on routers.

#### Features
- **Diff Preview**: View the config diff between current and rollback version (1-49)
- **AI Risk Assessment**: Before executing, AI analyzes the diff for risk level, protocol impact, and service disruption
- **Execute Rollback**: Apply the rollback via MCP with commit confirmation
- Risk levels: LOW / MEDIUM / HIGH / CRITICAL

---

### 5.21 Network Discovery & Interface Analysis

Full infrastructure scanning — interface enumeration, LLDP neighbor discovery, OS fingerprinting, and AI-powered infrastructure mapping.

#### Features

| Feature | API Endpoint | Description |
|---|---|---|
| **Interface Terse** | `GET /api/discovery/interfaces/<router>` | All interfaces with status, IPs, descriptions |
| **Interface Detail** | `GET /api/discovery/interfaces/<router>/detail` | Detailed statistics: errors, CRC, MTU, speed, counters |
| **Neighbor Discovery** | `GET /api/discovery/neighbors/<router>` | LLDP neighbors + ARP table |
| **Full Scan** | `POST /api/discovery/full-scan` | Scan all routers: facts, interfaces, LLDP, version |
| **AI Infrastructure Map** | `POST /api/discovery/ai-map` | AI builds infrastructure map with recommendations |

#### AI Infrastructure Analysis
The AI analyzes scan data and provides:
1. Complete device inventory with roles, OS versions, and capabilities
2. Layer 2 neighbor map (who connects to whom)
3. IP addressing scheme analysis (subnets, overlap detection)
4. Protocol deployment coverage per device
5. Anomaly detection: unused interfaces, missing neighbors, version mismatches
6. Infrastructure health score (1-10)
7. Recommendations for improvement

---

### 5.22 Protocol Traffic Analysis

Real-time protocol statistics, traffic flow analysis, session tracking, and AI-powered anomaly detection via Junos show commands.

#### Features

| Feature | API Endpoint | Description |
|---|---|---|
| **Protocol Stats** | `GET /api/traffic/protocol-stats/<router>` | IS-IS, BGP, OSPF, LDP, MPLS, RSVP statistics |
| **Interface Counters** | `GET /api/traffic/interface-counters/<router>` | Real-time packet rates, errors, drops |
| **Flow Analysis** | `GET /api/traffic/flow-analysis/<router>` | Route summary, MPLS LSPs, LDP sessions, firewall counters |
| **Session Table** | `GET /api/traffic/session-table/<router>` | BGP neighbors, IS-IS adjacencies, LDP neighbors |
| **AI Traffic Analysis** | `POST /api/traffic/ai-analyze` | Deep AI analysis (general, security, performance, anomaly) |

#### AI Analysis Types

| Type | Focus |
|---|---|
| `general` | Comprehensive protocol traffic analysis: packet counts, session health, error rates |
| `security` | Unauthorized sessions, unusual traffic, BGP hijack indicators, rogue neighbors |
| `performance` | Congestion points, high-error interfaces, CRC errors, MTU mismatches |
| `anomaly` | Traffic spikes, flapping sessions, route oscillation, asymmetric routing |

---

### 5.23 Security Threat Analysis

Comprehensive security auditing with AI-powered threat detection, credential scanning, and CIS-style hardening reports.

#### Features

| Feature | API Endpoint | Description |
|---|---|---|
| **Security Audit** | `GET /api/security/audit/<router>` | Full audit: login, SSH, SNMP, firewall, syslog, NTP, alarms, lo0 filter |
| **Threat Check** | `POST /api/security/threat-check` | AI analyzes syslog, auth logs, connections, commit history for threats |
| **Credential Scan** | `POST /api/security/credential-scan` | Scan configs for cleartext passwords, weak SNMP communities, missing auth |
| **Hardening Report** | `POST /api/security/hardening-report` | CIS-style hardening assessment with scoring (100-point scale) |

#### Hardening Report Categories (100 points total)

| Category | Points | Checks |
|---|---|---|
| Management Plane Security | 20 | SSH, console, SNMP, NTP, syslog |
| Control Plane Protection | 20 | lo0 filter, RE protection, DDoS prevention |
| Data Plane Security | 20 | Firewall filters, policing, uRPF |
| Routing Protocol Security | 20 | IS-IS auth, BGP MD5, route filtering |
| Operational Security | 20 | Commit confirm, rollback config, rescue config |

#### Credential Scan Checks
1. Cleartext passwords (any 'password' not starting with `$9$`)
2. SNMP community strings (especially 'public' or 'private')
3. BGP/IS-IS/OSPF authentication (MD5 or missing)
4. SSH key strength and encryption algorithms
5. RADIUS/TACACS+ shared secrets exposure
6. Default credentials still present

---

### 5.24 DNS Diagnostics

DNS resolution analysis, cache inspection, and configuration auditing via Junos DNS capabilities.

#### Features

| Feature | API Endpoint | Description |
|---|---|---|
| **DNS Lookup** | `GET /api/dns/lookup/<router>` | Resolve hostname, check DNS servers configured |
| **Reverse Lookup** | `GET /api/dns/reverse/<router>` | IP-to-hostname reverse resolution |
| **Batch Lookup** | `POST /api/dns/batch` | Resolve multiple domains from a router (max 20) |
| **Config Audit** | `POST /api/dns/config-audit` | AI audits DNS config consistency across all routers |

#### DNS Config Audit Checks
1. DNS server consistency — are all routers using the same name servers?
2. Reachability — are configured DNS servers reachable?
3. Redundancy — does each router have at least 2 DNS servers?
4. Best practices — NTP sync, DNS timeout settings, search domains
5. Security — DNS over TLS/HTTPS availability, DNSSEC support
6. Recommendations for improvement

---

### 5.25 Advanced Path Analysis & Capacity Planning

Multi-algorithm path computation, what-if failure simulation, and AI-powered capacity planning.

#### Features

| Feature | API Endpoint | Description |
|---|---|---|
| **Multi-Algorithm Path** | `POST /api/path/multi-algorithm` | Dijkstra + K-shortest paths (Yen's algorithm) |
| **What-If Analysis** | `POST /api/path/what-if` | Simulate node/link failure and compute impact |
| **Capacity Planning** | `POST /api/path/capacity-plan` | AI-powered capacity and growth recommendations |

#### What-If Failure Analysis
1. Simulate removing a node or link from the topology
2. Check if the remaining network is still connected
3. Identify isolated nodes
4. AI analyzes affected services (VPN, MPLS LSPs, BGP sessions)
5. Estimate convergence time
6. Recommend remediation and prevention steps

#### Capacity Planning AI Analysis
1. Current capacity utilization assessment per node
2. Bottleneck identification (nodes with most traffic paths)
3. Where to add new links for redundancy
4. Interface capacity upgrades needed
5. Growth projection recommendations
6. Cost-benefit analysis of proposed changes
7. Priority ranking of improvements

---

### 5.26 Live Monitoring & Alerting

Real-time health monitoring across all routers with AI-powered incident response.

#### Features

| Feature | API Endpoint | Description |
|---|---|---|
| **Health Dashboard** | `GET /api/monitor/health-dashboard` | Uptime + alarms for all routers, reachability score |
| **Protocol Health** | `GET /api/monitor/protocol-health` | IS-IS adjacency, BGP summary, LDP session across all routers |
| **AI Incident Response** | `POST /api/monitor/ai-incident` | AI incident classification (P1-P4), root cause, triage commands, remediation |

#### AI Incident Response
Given symptoms, the AI provides:
1. Incident classification (P1/P2/P3/P4)
2. Root cause hypothesis (ranked by probability)
3. Affected blast radius (devices, services, customers)
4. Immediate triage commands to run
5. Remediation steps (ordered by priority)
6. Escalation criteria
7. Post-incident review checklist

---

## 6. Quantum-Inspired Network Optimization Engine

**Location:** `web_ui/quantum_engine.py`
**Lines of Code:** 906
**Version:** v1.0

A production-grade graph algorithms module designed for **2,000-10,000 node** SP/MPLS networks.

### Why "Quantum-Inspired"?

- **Simulated Quantum Annealing (SQA)**: Uses quantum tunneling metaphor to escape local minima in combinatorial optimization
- **Quantum Walk-based Search**: O(sqrt(N)) graph search vs O(N) classical for anomaly detection
- **QAOA-inspired variational heuristics**: For NP-hard partition/placement problems

### 5 Algorithms

| Algorithm | Class | Complexity | Purpose |
|---|---|---|---|
| **TarjanSPOF** | `TarjanSPOF` | O(V+E) | Find articulation points (SPOFs) and bridge links — iterative DFS |
| **Diameter Approx** | `fast_diameter_approx()` | O(V+E) | Double-BFS diameter approximation |
| **Quantum Annealing Optimizer** | `QuantumAnnealingOptimizer` | Heuristic | Simulated annealing for SPOF elimination |
| **Quantum Walk Anomaly Detector** | `QuantumWalkAnomalyDetector` | O(V+E) | Graph topology anomaly detection |
| **Louvain Community Detector** | `LouvainCommunityDetector` | O(E*log(V)) | Modularity-based community detection |

### API Endpoints (5)

| Endpoint | Method | Description |
|---|---|---|
| `/api/quantum/optimize` | POST | Run quantum annealing optimization, return proposed links |
| `/api/quantum/anomalies` | GET | Run quantum walk anomaly detection |
| `/api/quantum/communities` | GET | Run Louvain community detection |
| `/api/quantum/spof` | GET | Run Tarjan SPOF detection |
| `/api/quantum/benchmark` | GET | Run full benchmark suite (params: `nodes`, `degree`) |

---

## 7. REST API Reference (101 Endpoints)

The Flask backend exposes **101 REST API endpoints** organized into 20 feature groups.

### Bootstrap & Onboarding (3 endpoints)

| Endpoint | Method | Description |
|---|---|---|
| `/api/bootstrap/status` | GET | Check if golden configs exist — first-run detection |
| `/api/bootstrap/sync` | POST | Pull live configs from all MCP devices and save as golden configs |
| `/api/bootstrap/sync-one/<router>` | POST | Pull and save config for a single router |

### Topology & Network (4 endpoints)

| Endpoint | Method | Description |
|---|---|---|
| `/api/topology` | GET | Full network topology (nodes, links, BGP links). Params: `clustered`, `max_visible` |
| `/api/topology/stats` | GET | Topology statistics via quantum engine |
| `/api/network-stats` | GET | Comprehensive network statistics |
| `/api/shortest-path` | GET | Dijkstra shortest path. Params: `source`, `target` |

### Devices (1 endpoint)

| Endpoint | Method | Description |
|---|---|---|
| `/api/devices` | GET | All devices with role, loopback, interfaces, protocol counts |

### Golden Configs (4 endpoints)

| Endpoint | Method | Description |
|---|---|---|
| `/api/golden-configs` | GET | List all golden configs with metadata and content |
| `/api/golden-configs/<router>` | GET | Full golden config for a router (auto-fetches from MCP if missing) |
| `/api/config-diff/<router>` | GET | Diff between running and golden config (auto-fetches if missing) |
| `/api/config-search` | GET | Search across all configs. Params: `q`, `regex` |

### MCP Operations (6 endpoints)

| Endpoint | Method | Description |
|---|---|---|
| `/api/mcp/execute` | POST | Execute a single Junos command. Body: `router`, `command` |
| `/api/mcp/batch` | POST | Execute on multiple routers. Body: `routers[]`, `command` |
| `/api/mcp/facts/<router>` | GET | Device facts via MCP `gather_device_facts` |
| `/api/mcp/live-config/<router>` | GET | Live running config + diff against golden |
| `/api/mcp/deploy-config` | POST | Deploy config to a router. Body: `router`, `config`, `comment` |
| `/api/mcp/poll-status` | POST | Poll all devices for real-time dashboard status |

### AI Engine (3 endpoints)

| Endpoint | Method | Description |
|---|---|---|
| `/api/ai/chat` | POST | Complete AI response. Body: `message`, `history[]` |
| `/api/ai/stream` | POST | SSE streaming response. Body: `message`, `history[]` |
| `/api/ai/analyze` | POST | Focused AI analysis. Body: `data`, `question`, `system` |

### Templates (3 endpoints)

| Endpoint | Method | Description |
|---|---|---|
| `/api/templates` | GET | List all available Jinja2 templates |
| `/api/templates/render` | POST | Render template with variables. Body: `template`, `variables` |
| `/api/templates/deploy` | POST | Render and deploy to router. Body: `template`, `variables`, `router` |

### Quantum Engine (5 endpoints)

| Endpoint | Method | Description |
|---|---|---|
| `/api/quantum/optimize` | POST | Quantum annealing SPOF elimination |
| `/api/quantum/anomalies` | GET | Quantum walk anomaly detection |
| `/api/quantum/communities` | GET | Louvain community detection |
| `/api/quantum/spof` | GET | Tarjan articulation points + bridges |
| `/api/quantum/benchmark` | GET | Benchmark suite. Params: `nodes`, `degree` |

### Scheduled Tasks (8 endpoints)

| Endpoint | Method | Description |
|---|---|---|
| `/api/scheduled-tasks` | GET | List all scheduled tasks |
| `/api/scheduled-tasks` | POST | Create a new task. Body: `name`, `command`, `schedule`, `routers[]` |
| `/api/scheduled-tasks/<id>` | DELETE | Delete a task |
| `/api/scheduled-tasks/<id>/toggle` | POST | Toggle enabled/disabled |
| `/api/scheduled-tasks/<id>/run` | POST | Run immediately |
| `/api/scheduled-tasks/<id>/history` | GET | Task execution history |
| `/api/scheduled-tasks/cron` | POST | Create task with CRON expression |
| `/api/scheduled-tasks/calendar` | GET | Calendar view of all scheduled/completed tasks |

### Workflows (4 endpoints)

| Endpoint | Method | Description |
|---|---|---|
| `/api/workflows` | GET | List all saved workflows |
| `/api/workflows` | POST | Save a workflow definition |
| `/api/workflows/<name>` | DELETE | Delete a workflow |
| `/api/workflows/execute` | POST | Execute a workflow. Body: `name`, `steps[]`, `variables` |

### Device Pools (5 endpoints)

| Endpoint | Method | Description |
|---|---|---|
| `/api/pools` | GET | List all device pools |
| `/api/pools` | POST | Create a new pool. Body: `name`, `devices[]`, `color`, `tags[]` |
| `/api/pools/<id>` | PUT | Update a pool |
| `/api/pools/<id>` | DELETE | Delete a pool |
| `/api/pools/ai-recommend` | POST | AI-recommended pool groupings |

### Ping & Reachability (3 endpoints)

| Endpoint | Method | Description |
|---|---|---|
| `/api/ping/<router>` | GET | Ping a single router via MCP |
| `/api/ping/sweep` | POST | Sweep ping all routers. Body: `routers[]` (optional) |
| `/api/ping/ai-analyze` | POST | AI analysis of ping results |

### Data Validation (3 endpoints)

| Endpoint | Method | Description |
|---|---|---|
| `/api/validate` | POST | Validate command output. Body: `router`, `command`, `pattern`, `match_type` |
| `/api/validate/batch` | POST | Batch validate. Body: `routers[]`, `command`, `pattern` |
| `/api/validate/ai-compliance` | POST | AI compliance audit (auto-fetches config from MCP if needed) |

### Notifications (6 endpoints)

| Endpoint | Method | Description |
|---|---|---|
| `/api/notifications/channels` | GET | List notification channels |
| `/api/notifications/channels` | POST | Create channel. Body: `name`, `channel_type`, `webhook_url` |
| `/api/notifications/channels/<id>` | DELETE | Delete a channel |
| `/api/notifications/send` | POST | Send notification. Body: `channel_id`, `title`, `message`, `severity` |
| `/api/notifications/history` | GET | Notification delivery history |
| `/api/notifications/ai-summary` | POST | AI-generated alert summary |

### Git Export (4 endpoints)

| Endpoint | Method | Description |
|---|---|---|
| `/api/git-export/init` | POST | Initialize Git repository |
| `/api/git-export/export` | POST | Export configs and commit (AI commit message) |
| `/api/git-export/log` | GET | Commit log (last 20) |
| `/api/git-export/diff/<commit>` | GET | Diff for a specific commit |

### Config Rollback (2 endpoints)

| Endpoint | Method | Description |
|---|---|---|
| `/api/rollback/diff/<router>` | GET | Rollback diff preview. Params: `version` |
| `/api/rollback/execute` | POST | Execute rollback with AI risk assessment. Body: `router`, `version`, `confirm` |

### Result Comparison (5 endpoints)

| Endpoint | Method | Description |
|---|---|---|
| `/api/results/capture` | POST | Capture command output. Body: `name`, `router`, `command` |
| `/api/results` | GET | List all captured results |
| `/api/results/<name>` | GET | Get a specific captured result |
| `/api/results/compare` | POST | Compare two results. Body: `result_a`, `result_b` |
| `/api/results/<name>` | DELETE | Delete a captured result |

### Network Discovery (5 endpoints)

| Endpoint | Method | Description |
|---|---|---|
| `/api/discovery/interfaces/<router>` | GET | Interface terse + descriptions |
| `/api/discovery/interfaces/<router>/detail` | GET | Extensive interface statistics |
| `/api/discovery/neighbors/<router>` | GET | LLDP neighbors + ARP table |
| `/api/discovery/full-scan` | POST | Full infrastructure scan. Body: `routers[]` |
| `/api/discovery/ai-map` | POST | AI infrastructure mapping. Body: `scan_data` |

### Protocol Traffic Analysis (5 endpoints)

| Endpoint | Method | Description |
|---|---|---|
| `/api/traffic/protocol-stats/<router>` | GET | IS-IS, BGP, OSPF, LDP, MPLS, RSVP stats |
| `/api/traffic/interface-counters/<router>` | GET | Interface counters. Params: `interface` |
| `/api/traffic/flow-analysis/<router>` | GET | Routes, LSPs, LDP sessions, firewall counters |
| `/api/traffic/session-table/<router>` | GET | BGP, IS-IS, LDP neighbor sessions |
| `/api/traffic/ai-analyze` | POST | AI traffic analysis. Body: `traffic_data`, `type` |

### DNS Diagnostics (4 endpoints)

| Endpoint | Method | Description |
|---|---|---|
| `/api/dns/lookup/<router>` | GET | DNS lookup. Params: `domain`, `type` |
| `/api/dns/reverse/<router>` | GET | Reverse DNS. Params: `ip` |
| `/api/dns/batch` | POST | Batch DNS lookup. Body: `router`, `domains[]` |
| `/api/dns/config-audit` | POST | AI DNS configuration audit. Body: `routers[]` |

### Security Analysis (4 endpoints)

| Endpoint | Method | Description |
|---|---|---|
| `/api/security/audit/<router>` | GET | Full security data collection (login, SSH, SNMP, firewall, etc.) |
| `/api/security/threat-check` | POST | AI threat detection from logs + config. Body: `router` |
| `/api/security/credential-scan` | POST | Scan for cleartext credentials. Body: `routers[]` |
| `/api/security/hardening-report` | POST | CIS-style hardening report (100-point). Body: `router` |

### Advanced Path Analysis (3 endpoints)

| Endpoint | Method | Description |
|---|---|---|
| `/api/path/multi-algorithm` | POST | Multi-algorithm path computation. Body: `source`, `target` |
| `/api/path/what-if` | POST | Failure simulation. Body: `failed_node` or `failed_link` |
| `/api/path/capacity-plan` | POST | AI capacity planning recommendations |

### Live Monitoring (3 endpoints)

| Endpoint | Method | Description |
|---|---|---|
| `/api/monitor/health-dashboard` | GET | Real-time health for all routers |
| `/api/monitor/protocol-health` | GET | IS-IS, BGP, LDP health across all routers |
| `/api/monitor/ai-incident` | POST | AI incident response. Body: `symptoms` |

### System (7 endpoints)

| Endpoint | Method | Description |
|---|---|---|
| `/api/health` | GET | Health check (MCP + Ollama connectivity) |
| `/api/config` | GET | System configuration (sanitized) |
| `/api/logs` | GET | List available log files |
| `/api/logs/<filename>` | GET | Log file content. Params: `level`, `search`, `tail` |
| `/api/audit-history` | GET | Audit history |
| `/api/conversations` | GET | Conversation history |
| `/` | GET | Serve the SPA |

---

## 8. WebSocket Real-Time Events

The Flask-SocketIO server handles 6 WebSocket event types:

### Client → Server Events

| Event | Description | Payload |
|---|---|---|
| `connect` | Client connects | -- |
| `request_topology` | Request fresh topology data | -- |
| `request_path` | Request shortest path | `{source, target}` |
| `chat_message` | Send AI chat message | `{message, history[]}` |
| `mcp_command` | Execute MCP command | `{router, command}` |
| `poll_devices` | Poll all devices for live status | -- |

### Server → Client Events

| Event | Description | Payload |
|---|---|---|
| `connected` | Connection confirmed | `{status, timestamp}` |
| `topology_update` | Full topology graph data | `{nodes, links, bgp_links, ...}` |
| `path_result` | Shortest path result | `{path, cost, hops, links}` |
| `chat_response` | AI chat response | `{response, model, timestamp}` |
| `mcp_result` | MCP command output | `{router, command, output}` |
| `device_status` | Device poll results | `{output, routers, timestamp}` |
| `task_result` | Scheduled task execution result | `{task_id, name, status, result, duration}` |
| `workflow_progress` | Workflow step progress | `{step, total, name, status}` |

---

## 9. Data Flow & Communication

### Web UI Request Flow

```
User clicks "Ping PE1" in browser
    │
    ▼
noc.js: fetch("/api/ping/PE1")
    │
    ▼
app.py: @app.route("/api/ping/<router>")
    │
    ├─ Build MCP JSON-RPC payload:
    │   {"method":"tools/call", "params":{"name":"execute_junos_command",
    │    "arguments":{"router_name":"PE1","command":"show system uptime"}}}
    │
    ├─ httpx.post("http://127.0.0.1:30030/mcp/", json=payload)
    │
    ├─ MCP Server: SSH to PE1 → execute command → return output
    │
    └─ Flask returns JSON: {"router":"PE1","reachable":true,"latency_ms":123}
    │
    ▼
noc.js: render ping result card in DOM
```

### AI Chat Streaming Flow

```
User types "What are the SPOFs?" in AI Chat
    │
    ▼
noc.js: fetch("/api/ai/stream", {method:"POST", body:{message:"..."}})
    │
    ▼
app.py: @app.route("/api/ai/stream")
    │
    ├─ Build system prompt with topology context + device inventory
    ├─ Append conversation history (last 10 messages)
    │
    ├─ Start background thread → httpx stream to Ollama
    │   {"model":"gpt-oss", "messages":[...], "stream":true}
    │
    ├─ Stream SSE: data: {"token":"The"}\n\n
    │              data: {"token":" network"}\n\n
    │              data: {"token":" has"}\n\n ...
    │              data: {"done":true}\n\n
    │
    └─ Flask yields each token as SSE event to browser
    │
    ▼
noc.js: EventSource reads tokens → appends to chat bubble in real-time
```

### Bootstrap Auto-Fetch Flow

```
User opens Configs → clicks "PE1" → golden config missing
    │
    ▼
app.py: api_golden_config("PE1")
    │
    ├─ Check: golden_configs/PE1.conf → NOT FOUND
    │
    ├─ FALLBACK: mcp_get_config("PE1")
    │   └─ MCP Server: SSH to PE1 → "show configuration" → return config text
    │
    ├─ Auto-save: golden_configs/PE1.conf + PE1.meta
    │
    └─ Return config to browser
    │
    ▼
Config viewer shows PE1 config. Future requests use the saved file.
```

---

## 10. AI Intelligence Layers

```
┌──────────────────────────────────────────────────────────────┐
│  LAYER 3: COMMANDER (Web UI Chat / Terminal Chat)            │
│  - Lightweight system prompt (JNCIE-SP persona)              │
│  - Tool-calling loop (MCP tools + local tools)               │
│  - SSE streaming for Web UI                                  │
│  - Context: device inventory + topology + history            │
└──────────────────────┬───────────────────────────────────────┘
                       │ (delegates to)
┌──────────────────────▼───────────────────────────────────────┐
│  LAYER 2: SYNTHESIZER                                        │
│  - Combines findings from all specialists                    │
│  - Root cause chain construction                             │
│  - Severity scoring (risk x likelihood)                      │
└──────────────────────┬───────────────────────────────────────┘
                       │ (feeds into)
┌──────────────────────▼───────────────────────────────────────┐
│  LAYER 1: PROTOCOL SPECIALISTS (8 parallel)                  │
│  - OSPF, IS-IS, BGP, LDP/MPLS, L2VPN, Health, Sec, QoS     │
│  - Each: focused expert prompt + RAG KB                      │
│  - Structured JSON output → feeding Synthesizer              │
└──────────────────────┬───────────────────────────────────────┘
                       │ (powered by)
┌──────────────────────▼───────────────────────────────────────┐
│  LAYER 0: RAG KNOWLEDGE BASE                                 │
│  - 184KB+ KNOWLEDGE_BASE.md → chunked → embedded            │
│  - 7 Juniper PDFs → extracted → embedded                    │
│  - nomic-embed-text (768-dim vectors)                        │
│  - Cosine similarity + keyword boost retrieval               │
└──────────────────────────────────────────────────────────────┘
```

---

## 11. Specialist AI System

### 8 Protocol Specialists

| Specialist | Input Data | Depends On | Key Checks |
|---|---|---|---|
| **OSPF** | `show ospf neighbor/interface/database` | -- | Adjacency states, timer consistency, area config, authentication |
| **BGP** | `show bgp summary/neighbor` | OSPF | Session states, prefix counts, RR topology, authentication |
| **IS-IS** | `show isis adjacency/interface/database` | -- | Adjacency states, level config, metric-style, DIS election |
| **LDP/MPLS** | `show ldp session/neighbor, mpls interface` | OSPF | Session states, label bindings, inet.3 routes |
| **L2VPN/EVPN** | `show l2circuit/evpn/route-instance` | OSPF+BGP | Circuit states, pseudowire status, route-target config |
| **System Health** | `show chassis/system/storage` | -- | CPU, memory, storage, alarms, core dumps |
| **Security** | `show config firewall/ssh/snmp/ntp` | -- | RE protection, SSH config, SNMP communities |
| **QoS/CoS** | `show class-of-service/interface queue` | -- | Queue drops, scheduler maps, classifier, rewrite rules |

### Execution Order

```
Layer 1a: specialist_ospf(), specialist_isis(), specialist_system_health()
Layer 1b: specialist_bgp(ospf_findings)
Layer 1c: specialist_l2vpn(ospf_findings, bgp_findings)
Layer 1d: specialist_security(), specialist_qos_cos()
Final:    synthesize_findings(all_specialist_outputs)
```

---

## 12. Hypered Brain — 6-Layer Agentic Architecture

### What Makes It "Agentic"?

1. **Decides what to investigate** — Perception layer selects scripts based on query
2. **Adapts parallelism** — Adaptive Concurrency controller adjusts to gateway load
3. **Requests additional data** — AI-Directed Probes collect data the AI deems necessary
4. **Detects contradictions** — when two data sources disagree
5. **Self-validates** — runs additional passes until confidence is sufficient
6. **Remembers** — findings stored across sessions for pattern recognition

### Multi-Pass Validation Loop

```
Pass 1: Select scripts → Execute → Accumulate facts → AI analyzes → Confidence 45%
  → Detect gaps → Extract AI probes → 45% < 70% → CONTINUE

Pass 2: Follow-up scripts + AI probes → New facts merge → AI re-analyzes → Confidence 78%
  → No remaining gaps → STOP

Synthesis: Build final validated response with complete evidence chain
```

---

## 13. Smart Script Library

18 pre-defined smart scripts organized by category:

| Priority | Category | Script | Description |
|---|---|---|---|
| 1 | Connectivity | `intf_health` | Interface Health Scanner |
| 2 | Protocol State | `ospf_state` | OSPF adjacency/interface/database check |
| 2 | Protocol State | `isis_state` | IS-IS adjacency/interface/database check |
| 2 | Protocol State | `bgp_state` | BGP session/prefix/RR check |
| 2 | Protocol State | `ldp_mpls_state` | LDP session/MPLS interface check |
| 2 | Health | `system_health` | System Health Scanner (CPU, memory, alarms) |
| 3 | Connectivity | `reachability_matrix` | Loopback Reachability Matrix |
| 3 | Topology | `topology_scan` | Live Topology Scanner (LLDP + IS-IS) |
| 3 | Protocol State | `route_validation` | Route Table Validator |
| 4 | Configuration | `commit_history` | Recent Commit History |
| 4 | Service | `vpn_state` | VPN Service Analyzer (PE only) |
| 4 | Performance | `perf_baseline` | Performance Baseline |
| 5 | Security | `security_posture` | Security Posture Check |
| 7 | Deep Dive | `ospf_deep` | OSPF Deep Dive (databases, timers, auth) |
| 7 | Deep Dive | `isis_deep` | IS-IS Deep Dive (LSPDB, timers, auth) |
| 7 | Deep Dive | `bgp_deep` | BGP Deep Dive (neighbors, policies) |
| 7 | Deep Dive | `ldp_deep` | LDP Deep Dive (sessions, labels, FEC) |
| 8 | Deep Dive | `intf_deep_dive` | Interface Deep Dive (errors, CRC, MTU) |

Script selection: keyword matching + broad query detection + dependency resolution + priority sorting, capped at 8 scripts per pass.

---

## 14. Audit System

### Full Audit Pipeline (7 phases)

| Phase | Name | What Happens |
|---|---|---|
| 1 | Device Facts | Fetch model, version, serial, uptime from all devices |
| 2 | Data Collection | 20+ show commands across all devices in parallel batches |
| 3 | Issue Detection | Programmatic analysis of errors, protocol states, resources |
| 4 | Config Drift | Compare running configs against golden configs (difflib) |
| 5 | Deep Dive Audit | Hypered Brain multi-pass smart script analysis |
| 6 | AI Analysis | 8 specialists in parallel, synthesizer merges findings |
| 7 | Report Generation | Markdown + HTML reports with heatmap, compliance, topology |

---

## 15. Interactive Chat Mode (Terminal)

The original terminal-based chat interface (via `ollama_mcp_client.py`) remains fully functional alongside the Web UI.

### Commands

| Command | Description |
|---|---|
| `audit` | Run full 7-phase network audit |
| `topology` | Display ASCII network topology |
| `health` | Quick system health check |
| `troubleshoot <problem>` | AI troubleshooting with structured reasoning |
| `configure <device> <config>` | Push configuration with safety gates |
| `compare <device1> <device2>` | Config diff between two devices |
| `@filepath` | Ingest a file for context |
| `exit` / `quit` | Exit the chat |

### Tool-Calling Loop
Multi-round loop (max 12 rounds) where AI autonomously calls MCP tools, collects data, and builds an evidence-based response.

---

## 16. Safety & Change Management

### 6-Gate Configuration Push Safety

```
Gate 1: CHANGE WINDOW CHECK — Is it within allowed hours?
Gate 2: HUMAN APPROVAL — User must type "yes" to proceed
Gate 3: PRE-CHANGE STATE CAPTURE — Capture OSPF/BGP/LDP/interface states
Gate 4: COMMIT CONFIRMED (5 min) — Auto-rollback timer
Gate 5: POST-CHANGE STATE CAPTURE — Compare with pre-change baseline
Gate 6: AUTO-ROLLBACK ON FAILURE — Protocol state regression → auto-rollback
```

---

## 17. Knowledge Base & RAG Pipeline

### Sources
- **KNOWLEDGE_BASE.md** (184KB+) — Comprehensive Junos reference
- **EXPERT_EXAMPLES.md** — Protocol troubleshooting patterns
- **JUNOS_DEEP_KNOWLEDGE.md** — Advanced chain-of-thought methodology
- **7 Juniper PDFs** — JNCIA, JIR, AJSPR, JMF, JSPX, JL2V, L3VPN

### Pipeline
```
Source docs → Chunk by heading (200-400 tokens) → Anchor with section prefix
→ Embed with nomic-embed-text (768-dim) → Store in kb_vectors.pkl
→ At query time: Multi-query embed → Cosine similarity + keyword boost
→ Threshold 0.55 → Top-K retrieval → Inject into AI prompt
```

---

## 18. Network Topology Intelligence

### Multi-Layer Topology Fusion

```
Source 1: LLDP neighbors        → Physical adjacency layer
Source 2: OSPF/IS-IS adjacency  → IGP topology layer
Source 3: iBGP sessions         → Route reflector hierarchy layer
Source 4: LDP sessions          → MPLS transport layer
Source 5: Golden configs        → Static reference topology
→ FUSED TOPOLOGY GRAPH: nodes + edges + metrics + states
```

### Analysis Capabilities
- Articulation Point Detection (Tarjan's algorithm)
- ECMP Path Analysis
- Transit Node Identification
- D3.js Interactive Visualization (Web UI — 4 layout modes)
- Mermaid Diagrams (HTML reports)
- ASCII Topology (terminal)
- Adjacency Matrix

---

## 19. Lab Topology & Device Inventory

### Device Inventory (Example Lab)

| Device | Role | Description |
|---|---|---|
| **P11-P14** | Provider (Core) | Core transit routers, Area 0 |
| **P21-P24** | Provider (Core) | Core transit routers, Area 0 |
| **P12, P22** | Route Reflector | iBGP route reflectors |
| **PE1, PE2, PE3** | Provider Edge | VPN services, customer-facing |

Protocol Suite: OSPF + IS-IS + BGP + LDP + MPLS + L3VPN + EVPN

> **Note:** The system works with any number of Junos routers. Simply configure them in `devices.json` and let the bootstrap system pull their configs.

---

## 20. Reporting System

### Report Formats
- **Markdown**: `audit_report_YYYY-MM-DD.md` — Full text with tables, code blocks, evidence
- **HTML**: `audit_report_YYYY-MM-DD.html` — Interactive with CSS, topology, collapsible sections

### Report Sections
Executive Summary, Device Inventory, Severity Heatmap, Findings by Severity, Root Cause Chains, Compliance Scorecard, Config Drift, Remediation Playbook, Hypered Brain Metadata, Risk Matrix.

---

## 21. Persistence & Memory

### Storage Layer

| Store | Format | Purpose | File |
|---|---|---|---|
| **Audit History** | SQLite | Historical audit results | `audit_history.db` |
| **Analysis Memory** | SQLite | Investigation history, baselines | `analysis_memory.db` |
| **Scheduled Tasks** | SQLite | Task definitions + execution history | `web_ui/scheduled_tasks.db` |
| **Device Pools** | SQLite | Pool definitions with members | `web_ui/device_pools.db` |
| **Notifications** | SQLite | Channels + notification history | `web_ui/notifications.db` |
| **Device Facts Cache** | JSON | Cached device facts with TTL | `device_facts_cache.json` |
| **Session History** | JSON | Conversation history | `session_history.json` |
| **Resolution DB** | JSON | Self-learning fix patterns | `resolution_db.json` |
| **KB Vectors** | Pickle | Pre-computed embeddings (768-dim) | `kb_vectors.pkl` |
| **Workflows** | JSON | Workflow definitions | `web_ui/workflows/*.json` |
| **Captured Results** | JSON | Command output snapshots | `web_ui/results/*.json` |
| **Golden Configs** | Text | Router configurations + metadata | `golden_configs/*.conf` + `*.meta` |
| **Git Export** | Git repo | Version-controlled config history | `web_ui/git_export/` |

---

## 22. Configuration Templates

### Jinja2 Templates (`templates/`)

| Template | Purpose | Key Variables |
|---|---|---|
| `ospf_p2p.j2` | OSPF point-to-point interfaces | `interface`, `area`, `hello`, `dead` |
| `bgp_ibgp.j2` | iBGP session configuration | `local_as`, `neighbor_ip`, `group_name`, `cluster_id` |
| `mpls_ldp.j2` | MPLS/LDP interface enablement | `interfaces[]` |
| `system_hardening.j2` | Security hardening | `ntp_servers[]`, `syslog_hosts[]`, `snmp_community` |

Templates can be rendered and deployed via:
1. Web UI Template Engine view
2. Workflow Builder (template step type)
3. MCP `render_and_apply_j2_template` tool
4. Terminal chat `configure` command

---

## 23. Golden Configs & Compliance

### Golden Configurations
Located in `golden_configs/`: One `.conf` file per router + one `.meta` JSON file with sync metadata.

### Auto-Sync
Golden configs are automatically created via:
- **Bootstrap sync** — one-click pull of all router configs from MCP
- **On-demand fetch** — any API endpoint that needs a golden config will auto-pull it from MCP and save it
- **Manual sync** — "Sync from MCP" button in the Configs view

### Config Drift Detection
Running config vs golden config comparison using `difflib.unified_diff()`. Available via Web UI Config Management view or during audit Phase 4.

### Compliance Checks (20+)
Defined in `config.yaml`:
NTP, Syslog, SNMP, SSH Only, Login Banner, Rescue Config, LLDP, Root Auth, SSH v2, Console Timeout, Password Min Length, RE Protection, SNMP No Public, OSPF Auth, BGP Auth, Storm Control, Dual Syslog, NETCONF, Commit Synchronize, DNS Configured.

---

## 24. Bootstrap & Zero-Config Onboarding System

### Design Philosophy

The system is designed so that a new user needs **only two things** to get started:
1. A running MCP server connected to Junos devices
2. The Web UI running on port 5555

Everything else is auto-discovered, auto-created, and auto-populated.

### Auto-Creation on Startup

When `app.py` starts, it automatically creates these directories if they don't exist:

```
golden_configs/      — Router configuration files
web_ui/workflows/    — Saved workflow definitions
web_ui/results/      — Captured command outputs
web_ui/git_export/   — Git-versioned config repository
conversations/       — Chat conversation history
templates/           — Jinja2 configuration templates
tasks/               — Task definitions and notes
logs/                — System log files
```

### Device Discovery Fallback

```python
def load_devices():
    """Load device inventory — first from devices.json, fallback to MCP router list."""
    # Try 1: Load from junos-mcp-server/devices.json
    # Try 2: Query MCP server get_router_list tool
    # Try 3: Return empty dict (user can sync later)
```

### Golden Config Auto-Fetch

Every endpoint that accesses golden configs has an automatic fallback:

| Endpoint | Fallback Behavior |
|---|---|
| `GET /api/golden-configs/<router>` | Pulls from MCP, saves as .conf + .meta, returns to user |
| `GET /api/config-diff/<router>` | Pulls golden config from MCP if missing |
| `POST /api/validate/ai-compliance` | Uses live config from MCP if golden config doesn't exist |
| `POST /api/security/credential-scan` | Per-router MCP fallback for missing configs |
| `POST /api/security/hardening-report` | Uses live config from MCP if golden config doesn't exist |

### Topology Fallback

If no golden config files exist, `build_topology_from_golden_configs()` builds a minimal topology from the device inventory (names + roles), so the dashboard and topology views are never empty.

### Frontend Bootstrap Banner

On first load, the frontend calls `GET /api/bootstrap/status` and displays a welcome banner if configs haven't been synced yet:

```
┌──────────────────────────────────────────────────────┐
│  Welcome to Junos AI NOC                             │
│                                                      │
│  No golden configs found. Click below to sync        │
│  configurations from your MCP-connected devices.     │
│                                                      │
│  [  Sync All Configs from MCP  ]                     │
│                                                      │
│  Progress: ████████████████████████ 11/11 synced     │
└──────────────────────────────────────────────────────┘
```

### Bootstrap API Reference

| Endpoint | Method | Request Body | Response |
|---|---|---|---|
| `/api/bootstrap/status` | GET | -- | `{bootstrapped: bool, total_devices: int, synced_configs: int, missing_configs: [str]}` |
| `/api/bootstrap/sync` | POST | -- | `{status: "ok", synced: int, failed: int, results: [...]}` |
| `/api/bootstrap/sync-one/<router>` | POST | -- | `{status: "ok", router: str, lines: int}` |

---

## 25. Local-Only Architecture

The entire system runs **100% locally** with zero external network dependencies.

### Network Connections (localhost only)

| Service | URL | Purpose |
|---|---|---|
| Web UI | `http://127.0.0.1:5555` | Browser interface |
| MCP Server | `http://127.0.0.1:30030/mcp/` | Router access gateway |
| Ollama | `http://127.0.0.1:11434` | AI model inference |

### Why Local-Only?

- **Air-gapped network environments**: Many SP/enterprise NOCs operate in restricted networks
- **Data sovereignty**: No router data, configs, or credentials leave the local machine
- **Deterministic behavior**: No dependency on external service availability
- **Compliance**: Meets security requirements for ITAR, HIPAA, PCI-DSS environments

### Bundled Libraries

| Library | Version | Size | Purpose |
|---|---|---|---|
| D3.js | 7.9.0 | 273KB | Topology visualization |
| Socket.IO Client | 4.7.5 | 49KB | Real-time WebSocket |
| Lucide | latest | 383KB | SVG icon system |
| Inter | -- | 225KB | UI typography (WOFF2) |
| JetBrains Mono | -- | 54KB | Code typography (WOFF2) |

---

## 26. Database Schema

### `scheduled_tasks.db`

```sql
CREATE TABLE scheduled_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    task_type TEXT NOT NULL,
    schedule TEXT NOT NULL,
    target_routers TEXT NOT NULL,         -- JSON array
    command TEXT NOT NULL,
    enabled INTEGER DEFAULT 1,
    last_run TEXT,
    last_result TEXT,
    next_run TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    run_count INTEGER DEFAULT 0
);

CREATE TABLE task_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER,
    run_at TEXT,
    result TEXT,
    status TEXT,
    duration_ms INTEGER,
    FOREIGN KEY (task_id) REFERENCES scheduled_tasks(id)
);
```

### `device_pools.db`

```sql
CREATE TABLE device_pools (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT DEFAULT '',
    devices TEXT NOT NULL DEFAULT '[]',   -- JSON array
    tags TEXT DEFAULT '[]',               -- JSON array
    color TEXT DEFAULT '#01A982',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

### `notifications.db`

```sql
CREATE TABLE notification_channels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    channel_type TEXT NOT NULL,           -- "slack", "mattermost", "webhook", "email"
    webhook_url TEXT DEFAULT '',
    config TEXT DEFAULT '{}',
    enabled INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notification_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_id INTEGER,
    title TEXT,
    message TEXT,
    severity TEXT DEFAULT 'info',
    sent_at TEXT DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'sent',
    response TEXT DEFAULT ''
);
```

### `audit_history.db`

```sql
CREATE TABLE audit_runs (
    id INTEGER PRIMARY KEY,
    start_time TEXT,
    end_time TEXT,
    summary TEXT,
    findings_count INTEGER,
    critical_count INTEGER,
    report_path TEXT
);
```

### `analysis_memory.db`

```sql
CREATE TABLE investigations (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    query TEXT,
    findings TEXT,
    device TEXT,
    category TEXT
);

CREATE TABLE baselines (
    device TEXT,
    metric TEXT,
    value REAL,
    updated TEXT
);
```

---

## 27. How to Build & Run — Complete Step-by-Step Guide

### System Requirements

| Requirement | Minimum | Recommended |
|---|---|---|
| **Python** | 3.10+ | 3.12 |
| **RAM** | 8 GB | 16 GB (for AI model) |
| **Disk** | 5 GB | 20 GB (with AI model) |
| **OS** | macOS / Linux / WSL2 | macOS or Ubuntu 22.04 |
| **Network** | Access to Junos routers via SSH | -- |
| **Git** | Optional (for config export) | Recommended |

### Full Installation

```bash
# 1. Clone the project
git clone <repository-url>
cd "MCP Localhost"

# 2. Create a Python virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

# 3. Install MCP server dependencies
cd junos-mcp-server
pip install -r requirements.txt

# 4. Install Web UI dependencies
cd ../web_ui
pip install flask flask-socketio flask-cors httpx pyyaml jinja2

# 5. Install Ollama (macOS)
brew install ollama
# Or download from https://ollama.ai

# 6. Pull the AI model
ollama pull gpt-oss
# Also pull the embedding model (for RAG):
ollama pull nomic-embed-text

# 7. Configure devices (edit junos-mcp-server/devices.json)
#    See Section 4.1 for format

# 8. Configure system (edit config.yaml)
#    See Section 4.8 for all options
```

### Starting All Services

```bash
# Terminal 1: Ollama
ollama serve

# Terminal 2: MCP Server
cd junos-mcp-server
python jmcp.py

# Terminal 3: Web UI
cd web_ui
python app.py
```

### Startup Banner

When `app.py` starts successfully, you'll see:

```
═══════════════════════════════════════════════════════════════════
  Junos AI NOC v21.2 — Network Operations Center
  URL: http://127.0.0.1:5555
  MCP: http://127.0.0.1:30030/mcp/
  AI:  http://127.0.0.1:11434 (gpt-oss)
  API: 101 endpoints | WebSocket: 6 events
═══════════════════════════════════════════════════════════════════
```

### Verifying the Installation

```bash
# Check MCP Server
curl http://127.0.0.1:30030/mcp/ -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'

# Check Ollama
curl http://127.0.0.1:11434/api/tags

# Check Web UI health
curl http://127.0.0.1:5555/api/health
# Expected: {"mcp":"ok","ollama":"ok","model":"gpt-oss"}
```

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `NOC_PORT` | 5555 | Web UI port |
| `FLASK_DEBUG` | -- | Enable debug mode |

### Running the Terminal Client

```bash
# The terminal AI client runs independently of the Web UI
cd "MCP Localhost"
python ollama_mcp_client.py
```

### Running the Full Audit (Terminal)

```bash
cd "MCP Localhost"
python run_audit.py
# This triggers the 7-phase audit pipeline and generates reports
```

---

## 28. Troubleshooting Guide

### MCP Server Won't Connect

**Symptom:** Health check shows `mcp: "error"` or MCP indicator is red in the header.

**Checklist:**
1. Is the MCP server running? → `python jmcp.py`
2. Is it on the right port? → Check `config.yaml` → `mcp.url`
3. Can you reach it? → `curl http://127.0.0.1:30030/mcp/`
4. Are devices configured? → Check `junos-mcp-server/devices.json`
5. Check for port conflicts → `lsof -i :30030`

### Ollama Won't Respond

**Symptom:** AI chat shows "AI engine unavailable" or `ollama: "error"` in health check.

**Checklist:**
1. Is Ollama running? → `ollama serve`
2. Is the model pulled? → `ollama list` should show `gpt-oss`
3. Is it on the right port? → Check `config.yaml` → `ai.ollama_url`
4. Is there enough RAM? → The 13B model needs ~8GB free
5. Check Ollama logs → `journalctl -u ollama` (Linux) or check Activity Monitor (macOS)

### Empty Topology / Dashboard

**Symptom:** Topology shows no nodes, dashboard stats are all zero.

**Solution:**
1. Click "Sync All Configs from MCP" in the bootstrap banner
2. Or manually: `curl -X POST http://127.0.0.1:5555/api/bootstrap/sync`
3. Verify: `curl http://127.0.0.1:5555/api/bootstrap/status`
4. Check that `golden_configs/` directory has `.conf` files

### Golden Config Missing for a Router

**Symptom:** Config view shows 404 or "No config found."

**Solution:**
1. The system will auto-fetch from MCP on next access (just refresh)
2. Or manually sync: `curl -X POST http://127.0.0.1:5555/api/bootstrap/sync-one/PE1`
3. Or click "Sync from MCP" in the Configs view header

### SSH Connection Failures to Routers

**Symptom:** MCP commands return "Error" or timeout.

**Checklist:**
1. Can you SSH manually? → `ssh -p <port> <user>@<ip>`
2. Check `devices.json` — correct IP, port, username, auth
3. Check SSH key permissions: `chmod 600 ~/.ssh/id_rsa`
4. Increase timeout in `config.yaml` → `mcp.call_timeout`
5. Check NETCONF is enabled on the router → `set system services netconf ssh`

### WebSocket Not Connecting

**Symptom:** Real-time updates don't work, connection indicator stays grey.

**Checklist:**
1. Is Flask-SocketIO installed? → `pip install flask-socketio`
2. Check browser console for WebSocket errors (F12 → Console tab)
3. Try a different browser (Chrome recommended)
4. Ensure no firewall is blocking port 5555

### AI Responses Are Slow

**Symptom:** AI chat takes 30+ seconds to respond.

**Checklist:**
1. Check CPU/GPU utilization during inference → `top` or Activity Monitor
2. Reduce `context_window` in `config.yaml` (e.g., 16384 instead of 32768)
3. Consider a smaller model if hardware is limited
4. Check if other Ollama models are loaded (they consume memory)

### Config Diff Shows No Changes

**Symptom:** Config diff returns empty when you know there are changes.

**Explanation:**
- The diff compares the **golden config file** against the **live running config via MCP**
- If the golden config was just synced, it matches the live config (no diff)
- Make changes on the router first, then run the diff

---

## 29. Version History

| Version | Date | Changes |
|---|---|---|
| **v21.2** | 2026-02-22 | Zero-config onboarding, bootstrap system, 101 API endpoints, 21 views, network discovery, traffic analysis, security auditing, DNS diagnostics, capacity planning, live monitoring, comprehensive documentation |
| **v21.1** | 2026-02-21 | UI professionalization (Lucide icons, no emojis), local-only bundling, api_compare_results bug fix, full documentation rewrite |
| **v19.0** | 2026-02-19 | Full-stack Web UI, D3.js topology, AI chat with SSE streaming, 16 views, quantum engine, WebSocket events |
| **v18.0** | 2026-02-18 | Hypered Brain v18, 6-layer agentic architecture, adaptive concurrency, AI-directed probes |
| **v17.0** | 2026-02-17 | Reasoning engine v15, 7-stage pipeline, hypothesis-driven investigation |
| **v16.0** | 2026-02-16 | Network analysis engine, 8 analysis modules, persistent memory |
| **v15.0** | 2026-02-15 | 8 protocol specialists, RAG pipeline, full audit system, knowledge base |
| **v14.0** | 2026-02-14 | Interactive chat mode, tool-calling loop, safety gates |
| **v13.0** | 2026-02-13 | MCP server batch execution, parallel SSH, ThreadPoolExecutor |

---

## 30. File Inventory & Line Counts

### Web UI Files

| File | Lines | Description |
|---|---|---|
| `web_ui/app.py` | 3,622 | Flask backend — 101 API routes, all engines |
| `web_ui/static/js/noc.js` | 2,594 | Frontend JS — 21 views, topology, AI chat |
| `web_ui/static/css/noc.css` | 4,146 | Full dark/light theme system |
| `web_ui/static/css/fonts.css` | 27 | @font-face declarations |
| `web_ui/templates/index.html` | 1,277 | SPA HTML — 21 view sections |
| `web_ui/quantum_engine.py` | 906 | 5 quantum-inspired graph algorithms |
| **Subtotal** | **12,572** | |

### Core AI Files

| File | Lines | Description |
|---|---|---|
| `ollama_mcp_client.py` | 12,627 | Terminal AI client — full system |
| `hypered_brain.py` | 1,963 | 6-layer agentic brain |
| `reasoning_engine.py` | 1,488 | 7-stage reasoning pipeline |
| `network_analysis.py` | 2,149 | 8 analysis modules |
| `kb_vectorstore.py` | 798 | RAG vector store |
| `ingest_pdfs.py` | 321 | PDF ingestion pipeline |
| **Subtotal** | **19,346** | |

### MCP Server Files

| File | Lines | Description |
|---|---|---|
| `junos-mcp-server/jmcp.py` | 1,786 | MCP server — Junos gateway |
| `junos-mcp-server/utils/config.py` | ~200 | Configuration utilities |
| **Subtotal** | **~1,986** | |

### Static Assets (Locally Bundled)

| File | Size | Description |
|---|---|---|
| `d3.v7.min.js` | 273 KB | D3.js topology visualization |
| `socket.io.min.js` | 49 KB | Socket.IO real-time communication |
| `lucide.min.js` | 383 KB | Lucide SVG icon library |
| `inter.woff2` | 225 KB | Inter UI font |
| `jetbrains-mono.woff2` | 54 KB | JetBrains Mono code font |

### Configuration & Knowledge

| File | Lines/Size | Description |
|---|---|---|
| `config.yaml` | 298 lines | System configuration |
| `KNOWLEDGE_BASE.md` | 184 KB+ | Junos technical knowledge base |
| `EXPERT_EXAMPLES.md` | ~50 KB | Troubleshooting patterns |
| `JUNOS_DEEP_KNOWLEDGE.md` | ~30 KB | Advanced reasoning methodology |
| `junos_commands.json` | ~200 | Command reference |

### **Grand Total: ~33,000+ lines of code**

---

*End of Documentation — Junos AI Network Operations Center v21.2*
