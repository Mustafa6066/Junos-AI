# Junos AI NOC v22.0 — Complete Operations Guide

> **AI-Powered Network Operations Center for Juniper Networks**
> Built with Flask · Ollama AI · MCP Protocol · D3.js Topology · Quantum Analysis Engine

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Architecture Overview](#2-architecture-overview)
3. [Prerequisites](#3-prerequisites)
4. [Installation & Setup](#4-installation--setup)
5. [Configuration Reference](#5-configuration-reference)
6. [First-Run Experience](#6-first-run-experience)
7. [Dashboard & Topology](#7-dashboard--topology)
8. [Device Management](#8-device-management)
9. [AI Chat & Reasoning Engine](#9-ai-chat--reasoning-engine)
10. [Brain Engine (Hypered Brain)](#10-brain-engine-hypered-brain)
11. [Golden Configs & Config Diff](#11-golden-configs--config-diff)
12. [MCP Command Execution](#12-mcp-command-execution)
13. [Templates & Deployment](#13-templates--deployment)
14. [Workflows & Automation](#14-workflows--automation)
15. [Scheduled Tasks](#15-scheduled-tasks)
16. [Compliance & Validation](#16-compliance--validation)
17. [Security Audit Center](#17-security-audit-center)
18. [Remediation Engine](#18-remediation-engine)
19. [Device Pools](#19-device-pools)
20. [Ping & Connectivity](#20-ping--connectivity)
21. [Traffic Analysis](#21-traffic-analysis)
22. [Discovery Engine](#22-discovery-engine)
23. [DNS Intelligence](#23-dns-intelligence)
24. [Path Analysis & Quantum Engine](#24-path-analysis--quantum-engine)
25. [Monitoring & Health Dashboard](#25-monitoring--health-dashboard)
26. [Notifications](#26-notifications)
27. [Git Export & Version Control](#27-git-export--version-control)
28. [Rollback Management](#28-rollback-management)
29. [Results Capture & Compare](#29-results-capture--compare)
30. [Logs Viewer](#30-logs-viewer)
31. [Copilot Sidebar](#31-copilot-sidebar)
32. [API Reference](#32-api-reference)
33. [Troubleshooting](#33-troubleshooting)
34. [Security Considerations](#34-security-considerations)
35. [File & Directory Reference](#35-file--directory-reference)

---

## 1. Introduction

**Junos AI NOC** is a full-featured, AI-powered Network Operations Center designed specifically for Juniper Networks environments. It combines live device communication via the **Model Context Protocol (MCP)** server, local AI reasoning through **Ollama**, and a rich web-based interface to provide:

- **Real-time topology visualization** — Interactive D3.js network map parsed from golden configs
- **AI-powered troubleshooting** — Agentic chat with chain-of-thought reasoning, hypothesis generation, and autonomous script execution
- **Configuration management** — Golden config storage, Jinja2 templates, diff comparison, and safe deployment with commit-confirmed rollback
- **Automated compliance auditing** — 20+ configurable CIS-style checks executed across your entire fleet
- **Multi-pass investigation (Brain Engine)** — Hypered Brain autonomously selects scripts, runs them on devices, validates findings, and loops until confident
- **Quantum-inspired network analysis** — Single-point-of-failure detection, community clustering, anomaly detection, multi-algorithm path analysis
- **Workflow orchestration** — Chain commands, templates, AI analysis, conditions, waits, and deployments into reusable workflows
- **Scheduled automation** — Cron-style or interval-based recurring task execution with full history
- **Security auditing** — Credential scanning, hardening reports, threat checks, and firewall rule analysis
- **Version control integration** — Git-based config export with commit history and diff viewer

### Target Audience

- Network Operations Center (NOC) engineers
- Network architects managing Junos MPLS/IS-IS/BGP-based service provider networks
- Automation engineers building NetDevOps workflows
- Anyone managing Juniper routers (MX, PTX, ACX, SRX, vMX, cRPD, JCNR)

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser (Web UI)                          │
│  index.html + noc.js + noc.css + D3.js + Socket.IO         │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP REST + WebSocket
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Flask Backend (app.py — port 5555)             │
│  ┌──────────┐ ┌──────────┐ ┌───────────┐ ┌──────────────┐  │
│  │ AI Engine│ │ MCP      │ │ Scheduler │ │ Quantum      │  │
│  │ (Ollama) │ │ Bridge   │ │ Engine    │ │ Engine       │  │
│  └────┬─────┘ └────┬─────┘ └───────────┘ └──────────────┘  │
│       │             │                                       │
│  ┌────┴──────┐ ┌────┴─────────────────────────────────────┐ │
│  │ Brain     │ │ SQLite DBs: audit, analysis, scheduled,  │ │
│  │ Engine    │ │ pools, notifications                     │ │
│  └───────────┘ └──────────────────────────────────────────┘ │
└────────┬───────────────┬────────────────────────────────────┘
         │               │
         ▼               ▼
┌──────────────┐  ┌──────────────────────────────────────────┐
│   Ollama     │  │  Junos MCP Server (port 30030)           │
│ (port 11434) │  │  ┌──────────────────────────────────┐    │
│ Model:       │  │  │ JSON-RPC 2.0 → PyEZ → SSH/NETCONF│    │
│  gpt-oss     │  │  └──────────────────────────────────┘    │
└──────────────┘  │  Devices: P11-P14, P21-P24, PE1-PE3     │
                  └──────────────────────────────────────────┘
                              │ SSH (various ports)
                              ▼
                  ┌──────────────────────────┐
                  │   Junos Routers (11x)    │
                  │   66.129.234.209         │
                  │   Ports: 32010–32078     │
                  └──────────────────────────┘
```

### Component Summary

| Component | Technology | Port | Purpose |
|-----------|-----------|------|---------|
| **Web UI** | Flask + Socket.IO | `5555` | Web interface, REST API, WebSocket events |
| **AI Engine** | Ollama (gpt-oss) | `11434` | Local LLM for chat, analysis, reasoning |
| **MCP Server** | junos-mcp-server | `30030` | Device communication bridge (JSON-RPC 2.0) |
| **Topology Engine** | D3.js + Python parser | — | Interactive network map from golden configs |
| **Quantum Engine** | Custom Python (quantum_engine.py) | — | SPOF, communities, anomalies, path optimization |
| **Databases** | SQLite | — | Audit history, analysis memory, schedules, pools, notifications |

---

## 3. Prerequisites

### Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| **Python** | 3.10+ | Backend runtime |
| **Ollama** | Latest | Local AI model hosting |
| **Git** | Any | Config version control features |

### Required Python Packages

```
flask
flask-socketio
flask-cors
httpx
jinja2
pyyaml
eventlet (or gevent)
```

### AI Model

The system is configured to use the `gpt-oss` model via Ollama. Install it:

```bash
ollama pull gpt-oss
```

> **Note:** You can change the model in `config.yaml` under `ai.model`. Any Ollama-compatible model works (e.g., `llama3`, `mistral`, `qwen2.5`).

### Network Requirements

- Access to Junos routers via SSH (MCP server handles the connection)
- MCP server running on `http://127.0.0.1:30030`
- Ollama running on `http://127.0.0.1:11434`
- All services on localhost (CORS restricted)

---

## 4. Installation & Setup

### Step 1: Clone / Copy the Project

```bash
cd ~/Desktop
# The project lives in "MCP Localhost/"
```

### Step 2: Install MCP Server

```bash
cd junos-mcp-server/
pip install -r requirements.txt
# Or using uv:
uv pip install -r requirements.txt
```

### Step 3: Configure Devices

Edit `junos-mcp-server/devices.json` with your router inventory:

```json
{
  "devices": [
    {
      "name": "PE1",
      "host": "66.129.234.209",
      "port": 32070,
      "username": "jcluser",
      "password": "Juniper!1",
      "platform": "junos"
    }
  ]
}
```

Each device entry needs:
- `name` — Unique device identifier (used throughout the UI)
- `host` — IP address or hostname
- `port` — SSH port (default: 22)
- `username` / `password` — SSH credentials
- `platform` — Always `"junos"`

> **Security Warning:** Use SSH key authentication for production. The MCP server supports `ssh_key_path` in device entries.

### Step 4: Start the MCP Server

```bash
cd junos-mcp-server/
python jmcp.py
# Starts on http://127.0.0.1:30030
```

### Step 5: Start Ollama

```bash
ollama serve
# Runs on http://127.0.0.1:11434
```

### Step 6: Install Web UI Dependencies

```bash
cd web_ui/
pip install flask flask-socketio flask-cors httpx pyyaml jinja2 eventlet
```

### Step 7: Start the Web UI

```bash
cd web_ui/
python app.py
# Starts on http://localhost:5555
```

You'll see the startup banner:

```
╔══════════════════════════════════════════════════════════════╗
║   Junos AI NOC — Web UI v22.0 (Full MCP + AI)               ║
║   URL:    http://localhost:5555                              ║
║   MCP:    http://127.0.0.1:30030/mcp/                       ║
║   Ollama: http://127.0.0.1:11434                            ║
║   Configs: 11 golden | Templates: 4                         ║
║   Scheduler: Active | Workflows: 0 saved                    ║
╚══════════════════════════════════════════════════════════════╝
```

### Step 8: Open the UI

Navigate to **http://localhost:5555** in your browser.

### Environment Variables (Optional)

| Variable | Default | Description |
|----------|---------|-------------|
| `NOC_PORT` | `5555` | Web server port |
| `NOC_HOST` | `127.0.0.1` | Bind address |
| `NOC_API_KEY` | — | If set, all API calls require `X-API-Key` header |
| `FLASK_DEBUG` | — | Enable debug mode (hot reload, verbose errors) |

---

## 5. Configuration Reference

All settings live in **`config.yaml`** (300 lines). No Python code editing required.

### 5.1 MCP Connection

```yaml
mcp:
  url: "http://127.0.0.1:30030/mcp/"
  batch_concurrency: 2        # Max simultaneous batch commands
  call_timeout: 120.0         # Per-call timeout (seconds)
  batch_retry: 1              # Retry failed batches N times
  batch_retry_delay: 3.0      # Seconds between retries
  max_response_chars: 500000  # Truncate responses larger than this
```

### 5.2 AI Model Settings

```yaml
ai:
  model: "gpt-oss"                  # Ollama model name
  ollama_url: "http://127.0.0.1:11434"
  context_window: 32768             # Token context window
  max_context_usage: 0.80           # Trim history at 80%
  temperature: 0.12                 # Low = more deterministic
  top_p: 0.9                        # Nucleus sampling
  repeat_penalty: 1.1               # Anti-repetition
  max_tool_rounds: 15               # Max AI tool-calling rounds
  structured_reasoning: true        # Multi-step reasoning chains
  confidence_threshold: 70          # Min confidence % before retry
  deep_reasoning: true              # Mind-map reasoning for complex queries
  fsm_diagnosis: true               # Protocol state machine diagnosis
  cascade_detection: true           # Cascading failure chain detection
```

### 5.3 Hypered Brain Engine

```yaml
hypered_brain:
  confidence_threshold: 70    # Min confidence % to accept
  max_passes: 3               # Validation passes (1-3)
  max_concurrent_scripts: 3   # Parallel script workers
  max_scripts_per_pass: 8     # Scripts per perception pass
  script_timeout: 60          # Per-script timeout (seconds)
  enable_follow_up: true      # Auto deep-dive on anomalies
  save_reports: true          # Save reports to files
```

### 5.4 Health Thresholds

```yaml
thresholds:
  crc_errors_per_audit: 10
  input_errors_per_audit: 50
  carrier_transitions: 10
  storage_pct_warning: 80
  storage_pct_critical: 95
  interface_utilization_warning: 80     # % bandwidth
  interface_utilization_critical: 95
  bgp_flap_threshold: 5                # Flaps per hour
  memory_utilization_warning: 80        # RE memory %
  cpu_utilization_warning: 80           # RE CPU %
  uptime_min_hours: 24
  bgp_prefix_warning_ratio: 0.9
```

### 5.5 Compliance Checks

The system ships with **20+ compliance checks** — each defined in config.yaml:

| Check ID | Description | Command |
|----------|-------------|---------|
| `ntp` | NTP configured | `show ntp associations no-resolve` |
| `syslog` | Syslog configured | `show configuration system syslog` |
| `snmp` | SNMP configured | `show configuration snmp` |
| `ssh_only` | SSH only (no telnet) | `show configuration system services` |
| `login_banner` | Login banner set | `show configuration system login message` |
| `rescue` | Rescue config saved | `show system storage` |
| `lldp` | LLDP enabled | `show lldp` |
| `root_auth` | Root auth set | `show configuration system root-authentication` |
| `ssh_v2` | SSH protocol v2 only | `show configuration system services ssh` |
| `console_timeout` | Console timeout configured | `show configuration system login` |
| `password_min_length` | Password min length set | `show configuration system login password` |
| `re_protection` | RE protection filter on lo0 | `show configuration interfaces lo0 ...` |
| `snmp_no_public` | SNMP community not 'public' | `show configuration snmp community` |
| `ospf_auth` | OSPF authentication | `show configuration protocols ospf` |
| `bgp_auth` | BGP authentication | `show configuration protocols bgp` |
| `storm_control` | Storm control on edges | `show configuration forwarding-options storm-control` |
| `dual_syslog` | Multiple syslog servers | `show configuration system syslog` |
| `netconf` | NETCONF over SSH | `show configuration system services netconf` |
| `commit_sync` | Commit synchronize (dual RE) | `show configuration system` |
| `dns_configured` | DNS name servers set | `show configuration system name-server` |

### 5.6 Device Roles

```yaml
device_roles:
  pe:
    prefix: "PE"
    extra_commands:
      - "show route instance summary"
      - "show bgp group summary"
      - "show services l2circuit connections summary"
      - "show evpn instance"
  p:
    prefix: "P"
    exclude_prefix: "PE"
    extra_commands:
      - "show ted database"
  rr:
    prefix: "RR"
    extra_commands:
      - "show bgp group summary"
      - "show route receive-protocol bgp summary"
```

### 5.7 Change Management

```yaml
change_management:
  change_windows:
    weekday_start: 22         # Changes allowed 22:00–06:00 on weekdays
    weekday_end: 6
    weekend_allowed: true     # All day on weekends
  commit_confirmed_minutes: 5 # Auto-rollback if not confirmed within 5 min
  pre_post_state_capture: true
  auto_rollback_on_failure: false
```

### 5.8 Intelligence Settings

```yaml
intelligence:
  dependency_graph: true          # Build topology dependency graph
  baseline_detection: true        # Compare against saved baselines
  baseline_deviation_pct: 25      # % deviation to flag anomaly
  risk_scoring: true              # Per-finding risk scores
  sla_estimation: true            # SLA impact estimation
  default_sla_target: 99.99       # Target SLA %
  root_cause_chains: true         # Multi-hop root cause analysis
```

### 5.9 Network Analysis Engine

```yaml
network_analysis:
  capture:
    default_count: 25           # Default packet count
    default_duration: 10        # Capture duration (seconds)
    max_count: 100
  dns:
    default_record_type: "A"
    trace_enabled: true
  security:
    auto_remediate: false       # Never auto-push security fixes
    credential_scan: true
  alerts:
    enabled: true
    check_interval_min: 5
    auto_investigate: true      # Auto-trigger hypothesis engine
  forensics:
    max_entries: 100
    correlation_window_sec: 300
  profiler:
    health_thresholds:
      cpu_warning: 60
      cpu_critical: 80
      memory_warning: 70
      memory_critical: 85
      temperature_warning: 55
      temperature_critical: 65
  memory:
    db_path: "analysis_memory.db"
    max_investigations: 1000
    context_recall: true        # Recall past investigations
```

---

## 6. First-Run Experience

When you first open the UI at `http://localhost:5555`:

### 6.1 Bootstrap Sync

1. The dashboard shows a **Bootstrap Status** panel if golden configs are missing
2. Click **"Sync All Configs"** to pull running configs from all routers via MCP
3. Each config is saved to `golden_configs/<router>.conf` along with metadata (`.meta` file)
4. You can also sync individual routers with the per-router sync button

### 6.2 What Happens During Bootstrap

- The backend calls `mcp_get_config(router_name)` for each device
- Running configurations are fetched via NETCONF and saved as golden configs
- The topology engine parses these configs to build the D3.js network map
- Network statistics are calculated (node count, link count, SPOF, redundancy score)

### 6.3 After Bootstrap

- The **Topology Map** populates with all routers, links, and protocol info
- All views become functional — configs, diffs, compliance, etc.
- The scheduler starts its background loop (checks every 10 seconds)

---

## 7. Dashboard & Topology

### 7.1 Interactive Topology Map

The main dashboard displays a live D3.js force-directed network topology:

- **Nodes** — Color-coded by role:
  - 🟢 **PE** (Provider Edge) — Customer-facing routers
  - 🔵 **P** (Provider Core) — Transit routers
  - 🟡 **RR** (Route Reflector) — BGP route reflectors
- **Links** — Extracted from interface configurations, showing:
  - IS-IS adjacencies
  - Interface names
  - IP addressing
- **Interactions:**
  - Click a node to see device details
  - Drag nodes to rearrange layout
  - Zoom/pan with mouse wheel
  - Select source/destination for path analysis

### 7.2 Network Statistics Panel

Displayed alongside the topology:

| Metric | Description |
|--------|-------------|
| Total Nodes | Number of routers in the topology |
| Total Links | Number of point-to-point connections |
| PE/P/RR Count | Breakdown by device role |
| Avg Degree | Average connections per node |
| Graph Diameter | Longest shortest-path in the network |
| BGP Sessions | Total configured BGP peerings |
| IS-IS Adjacencies | Total IS-IS neighbor relationships |
| LDP Sessions | Routers with LDP enabled |
| VPN Instances | Routers with L3VPN/L2VPN configured |
| SPOF | Single Points of Failure (critical!) |
| Redundancy Score | % of nodes that are NOT single points of failure |

### 7.3 Shortest Path Finder

1. Select a **Source** and **Destination** router
2. Click **"Find Path"**
3. The shortest path is highlighted on the topology map
4. Path hops and interface details are displayed

---

## 8. Device Management

### 8.1 Device List

Navigate to the **Devices** view to see all configured routers:

- Device name, host IP, SSH port
- Role (PE/P/RR) auto-detected from naming convention
- Loopback address (from golden config)
- Quick actions: Sync Config, Get Facts, Ping

### 8.2 Device Facts

Click **"Get Facts"** on any device to retrieve:

- Hostname, model, serial number
- Junos version
- Uptime
- RE (Routing Engine) status

The data comes live from the router via MCP → `gather_device_facts`.

### 8.3 Live Config

Click on a device to fetch its **live running configuration** directly from the router via `get_junos_config`. This can then be compared against the golden config.

### 8.4 Poll Status

The **Poll Status** feature queries multiple routers simultaneously and reports their reachability and response time.

---

## 9. AI Chat & Reasoning Engine

### 9.1 Chat Modes

The AI chat supports three modes:

#### Standard Chat (`/api/ai/chat`)
- Single request/response
- Uses system context with topology awareness
- Good for quick questions

#### Streaming Chat (`/api/ai/stream`)
- Token-by-token streaming response
- Shows the AI "typing" in real time
- Ideal for longer explanations

#### Agentic Chat (`/api/ai/chat-agentic`)
- **Most powerful mode** — the AI can autonomously:
  1. Classify the problem (BGP, OSPF, MPLS, Interface, etc.)
  2. Select relevant routers based on topology
  3. Execute Junos commands via MCP
  4. Analyze outputs
  5. Run follow-up commands based on findings
  6. Provide chain-of-thought reasoning
- Up to **15 tool rounds** per query (configurable in `config.yaml`)
- Shows live chain-of-thought reasoning panel

### 9.2 Chain-of-Thought (CoT) Reasoning

When enabled, the AI shows its reasoning process:

```
🔍 REASONING CHAIN:
├─ Step 1: Classify query as "BGP convergence issue"
├─ Step 2: Identify affected routers: PE1, PE2
├─ Step 3: Run "show bgp summary" on PE1, PE2
├─ Step 4: Analyze BGP state — found PE2 in "Active" state
├─ Step 5: Run "show bgp neighbor 10.0.0.2" on PE1
├─ Step 6: Check IS-IS adjacency between PE1↔P11
├─ Step 7: Root cause: IS-IS adjacency down, BGP cannot establish
└─ Confidence: 94%
```

### 9.3 Quick Actions

Pre-built diagnostic actions accessible from the AI panel:

- Health check on a specific router
- BGP summary analysis
- Interface error scan
- MPLS LSP status
- Route table analysis

### 9.4 Copilot Suggestions

The **Copilot Sidebar** provides context-aware suggestions based on your current view:

- If viewing a config diff → suggests relevant compliance checks
- If on topology → suggests SPOF analysis
- If investigating an issue → suggests next diagnostic commands

### 9.5 Confidence Scoring

Every AI analysis includes a confidence score:

- **90-100%** — High confidence, evidence-backed conclusion
- **70-89%** — Moderate confidence, may need verification
- **Below 70%** — Low confidence, triggers re-analysis or escalation

### 9.6 Ensemble Analysis

Multi-perspective analysis where the AI approaches the problem from different angles:

- **Protocol Expert** — Analyzes protocol state machines
- **Topology Expert** — Considers network-wide impact
- **Historical Expert** — Compares against past incidents
- Results are merged into a unified assessment

---

## 10. Brain Engine (Hypered Brain)

### 10.1 What Is It?

The Hypered Brain is an **autonomous multi-pass investigation engine**:

1. **Problem Classification** — AI categorizes the issue
2. **Script Selection** — Brain selects relevant diagnostic scripts from a library
3. **Parallel Execution** — Scripts run on target routers concurrently (up to 3 parallel workers)
4. **Analysis** — AI analyzes all outputs together
5. **Validation Loop** — If confidence < threshold (70%), it selects MORE scripts and loops
6. **Final Report** — Comprehensive investigation report with root cause, evidence, and recommendations

### 10.2 Using the Brain

1. Navigate to the **Brain** view
2. Enter a problem description (e.g., "PE1 is dropping customer traffic")
3. Click **"Investigate"**
4. Watch the live progress:
   - Scripts being selected
   - Commands executing on routers
   - Confidence building pass-by-pass
5. Review the final report

### 10.3 Brain Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `confidence_threshold` | 70 | Min confidence to accept findings |
| `max_passes` | 3 | Max investigation passes |
| `max_concurrent_scripts` | 3 | Parallel execution workers |
| `max_scripts_per_pass` | 8 | Scripts per pass |
| `script_timeout` | 60 | Per-script timeout (seconds) |
| `enable_follow_up` | true | Auto deep-dive on anomalies |

### 10.4 Brain Status

Check the Brain's status at any time:
- Current investigation state
- Script library contents
- Past investigations with full history

### 10.5 RAG (Retrieval-Augmented Generation)

The Brain can query the **Knowledge Base** (`kb_vectorstore.py`) for:
- Juniper documentation excerpts
- Protocol-specific troubleshooting guides
- Previous investigation findings
- Expert examples from `EXPERT_EXAMPLES.md`

### 10.6 Predictive Analysis

The Brain's **predict** feature uses historical data and current device state to forecast potential issues:
- Interface degradation trends
- BGP stability predictions
- Capacity planning recommendations

---

## 11. Golden Configs & Config Diff

### 11.1 Golden Config Management

Golden configs are the **baseline reference** for each router:

- Stored in `golden_configs/<router>.conf`
- Metadata in `golden_configs/<router>.meta` (sync time, hash, version)
- Used for topology building, compliance checks, and drift detection

### 11.2 Viewing Configs

1. Navigate to the **Configs** view
2. Select a router from the dropdown
3. View the full golden configuration with syntax highlighting
4. Use the **search bar** to find specific stanzas

### 11.3 Config Diff

Compare **golden config vs. live running config**:

1. Navigate to the **Config Diff** view
2. Select a router
3. The system fetches the live config via MCP and compares it against the golden
4. Differences are highlighted:
   - 🟢 **Added** lines (in live but not golden)
   - 🔴 **Removed** lines (in golden but not live)
   - 🟡 **Changed** lines

### 11.4 Config Search

Search across ALL golden configs simultaneously:

- Enter a search term (e.g., "bgp group", "10.0.0.1", "firewall filter")
- Optionally enable **regex** mode
- Results show: router name, line number, matching text

---

## 12. MCP Command Execution

### 12.1 Single Command

Execute any Junos CLI command on a specific router:

1. Select a router
2. Enter a command (e.g., `show bgp summary`)
3. Click **Execute**
4. View the raw output

### 12.2 Batch Command

Execute the same command on **multiple routers** simultaneously:

1. Select multiple routers (or "All")
2. Enter a command
3. Click **Execute Batch**
4. Results come back in parallel (controlled by `batch_concurrency` in config)

### 12.3 Supported MCP Tools

| Tool | Description |
|------|-------------|
| `execute_junos_command` | Run any operational CLI command |
| `execute_junos_command_batch` | Run a command on multiple routers |
| `get_junos_config` | Fetch running configuration |
| `gather_device_facts` | Get device model, version, uptime |
| `load_and_commit_config` | Push and commit configuration |
| `render_and_apply_j2_template` | Render Jinja2 template and apply |
| `get_router_list` | List all configured devices |

---

## 13. Templates & Deployment

### 13.1 Jinja2 Templates

Pre-built templates in the `templates/` directory:

| Template | Purpose |
|----------|---------|
| `bgp_ibgp.j2` | iBGP peering configuration |
| `mpls_ldp.j2` | MPLS LDP configuration |
| `ospf_p2p.j2` | OSPF point-to-point interface config |
| `system_hardening.j2` | Security hardening baseline |

### 13.2 Rendering Templates

1. Navigate to **Templates** view
2. Select a template
3. Fill in the variables (each template has its own variable set)
4. Click **"Render"** to preview the generated config
5. Review the output before deploying

### 13.3 Deploying Templates

1. After rendering, click **"Deploy"**
2. Select the target router
3. Enter a commit comment
4. The config is pushed via `load_and_commit_config`
5. Uses **commit confirmed** (auto-rollback after 5 minutes if not confirmed)

### 13.4 Safe Deploy

The `/api/deploy/safe` endpoint provides additional safety:

- Change window validation (weekday 22:00–06:00)
- Pre-state capture (protocol states before change)
- Commit confirmed with configurable timeout
- Post-state capture and comparison

---

## 14. Workflows & Automation

### 14.1 What Are Workflows?

Workflows are **multi-step automation chains** saved as JSON files in the `workflows/` directory.

### 14.2 Workflow Step Types

| Step Type | Description |
|-----------|-------------|
| `command` | Execute a single Junos command on one router |
| `batch` | Execute a command on multiple routers |
| `template` | Render a Jinja2 template |
| `deploy` | Push rendered config to a router |
| `ai_analyze` | Send output to AI for analysis |
| `condition` | Check if a previous step's output matches a pattern |
| `wait` | Pause execution for N seconds |

### 14.3 Creating a Workflow

1. Navigate to **Workflows** view
2. Click **"New Workflow"**
3. Add steps one by one
4. Configure each step's parameters
5. Set **variables** that can be referenced across steps with `{{variable_name}}`
6. Save the workflow

### 14.4 Variable Substitution

Define variables at the workflow level, then reference them in any step:

```json
{
  "variables": {
    "target_router": "PE1",
    "interface": "ge-0/0/0"
  },
  "steps": [
    {
      "type": "command",
      "router": "{{target_router}}",
      "command": "show interfaces {{interface}} extensive"
    }
  ]
}
```

### 14.5 Cross-Step References

Steps can reference previous step outputs:

- `$step_1` — Output of step 1
- Used in `deploy` (config from previous template render)
- Used in `ai_analyze` (analyze previous command output)
- Used in `condition` (check previous step's output)

### 14.6 Executing Workflows

1. Select a saved workflow
2. Click **"Execute"**
3. Watch real-time progress via WebSocket (`workflow_progress` events)
4. Each step reports: status (success/error/skipped), output, duration

---

## 15. Scheduled Tasks

### 15.1 Creating a Scheduled Task

1. Navigate to **Scheduler** view
2. Click **"New Task"**
3. Configure:
   - **Name** — Descriptive task name
   - **Task Type** — Type of operation
   - **Schedule** — Interval (`5m`, `1h`, `30s`, `24h`) or cron expression (`*/5 * * * *`)
   - **Target Routers** — One or more routers
   - **Command** — Junos command to execute
4. Save — the task starts automatically

### 15.2 Schedule Formats

| Format | Example | Description |
|--------|---------|-------------|
| Interval | `5m` | Every 5 minutes |
| Interval | `1h` | Every hour |
| Interval | `30s` | Every 30 seconds |
| Interval | `24h` | Every 24 hours |
| Cron | `*/5 * * * *` | Every 5 minutes (cron) |
| Cron | `0 2 * * *` | Daily at 2:00 AM |

### 15.3 Managing Tasks

- **Toggle** — Enable/disable without deleting
- **Run Now** — Execute immediately regardless of schedule
- **Delete** — Remove the task
- **History** — View past execution results with timestamps and duration

### 15.4 Task Results

Results are emitted via WebSocket (`task_result` event) and stored in SQLite:
- Execution timestamp
- Status (success/error)
- Duration (milliseconds)
- Output (truncated to 5000 chars)

### 15.5 Calendar View

The calendar view (`/api/scheduled-tasks/calendar`) shows upcoming and past task executions in a timeline format.

---

## 16. Compliance & Validation

### 16.1 Single-Device Validation

1. Navigate to **Compliance** view
2. Select a router
3. Click **"Validate"**
4. Each of the 20+ compliance checks runs against the device
5. Results show PASS ✅ or FAIL ❌ for each check

### 16.2 Batch Validation

Run compliance checks across the entire fleet:

1. Click **"Validate All"** or select multiple routers
2. All checks run in parallel via MCP batch
3. Get a fleet-wide compliance matrix

### 16.3 AI Compliance Analysis

The AI compliance endpoint (`/api/validate/ai-compliance`) goes deeper:

- Runs all standard checks
- AI analyzes the results in context
- Provides remediation recommendations
- Prioritizes findings by risk level

---

## 17. Security Audit Center

### 17.1 Security Audit

Per-device security audit (`/api/security/audit/<router>`):

- Reviews firewall filters
- Checks access control lists
- Analyzes protocol security settings
- Reports vulnerabilities

### 17.2 Threat Check

AI-powered threat assessment:

- Input indicators (IPs, patterns, behaviors)
- AI correlates against device state
- Provides threat classification and response recommendations

### 17.3 Credential Scan

Scan configurations for security issues:

- Default credentials detection
- Weak password patterns
- Plaintext passwords in configs
- Community string analysis

### 17.4 Hardening Report

Comprehensive security hardening assessment:

- CIS-style benchmark evaluation
- Per-device hardening score
- Specific remediation steps for each finding
- Priority-ranked recommendations

---

## 18. Remediation Engine

### 18.1 Propose Remediation

When an issue is found (manually or via Brain/AI):

1. Click **"Propose Fix"** or use `/api/remediate/propose`
2. AI generates specific configuration changes
3. Each remediation includes:
   - Description of the issue
   - Proposed config change (Junos set commands)
   - Risk assessment
   - Rollback plan

### 18.2 Approval Workflow

Remediations follow a controlled workflow:

1. **Proposed** — AI generates the fix
2. **Approved** — Human reviews and approves
3. **Executed** — Config is pushed to the router
4. **Rejected** — Human rejects with reason

### 18.3 Remediation API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/remediate/propose` | POST | Create new remediation |
| `/api/remediate/list` | GET | List all remediations |
| `/api/remediate/<id>` | GET | Get specific remediation |
| `/api/remediate/<id>/approve` | POST | Approve a remediation |
| `/api/remediate/<id>/reject` | POST | Reject a remediation |
| `/api/remediate/<id>/execute` | POST | Execute approved remediation |

---

## 19. Device Pools

### 19.1 What Are Pools?

Device pools are logical groups of routers for batch operations:

- **Core Pool** — All P routers
- **Edge Pool** — All PE routers
- **Maintenance Pool** — Routers scheduled for maintenance
- Custom pools for any purpose

### 19.2 Managing Pools

1. Navigate to **Pools** view
2. Create pools with name, description, and device list
3. Edit pool membership at any time
4. Delete unused pools

### 19.3 AI-Recommended Pools

The AI can suggest optimal pool configurations based on:

- Network topology and device roles
- Traffic patterns
- Maintenance schedules
- Geographic or logical groupings

---

## 20. Ping & Connectivity

### 20.1 Single Ping

Ping a specific router to check reachability:

1. Select a router
2. Click **"Ping"**
3. View: response time, packet loss, round-trip times

### 20.2 Ping Sweep

Ping all routers (or a selected group) simultaneously:

1. Click **"Sweep All"**
2. Results show a matrix of reachability
3. Color-coded: 🟢 reachable, 🔴 unreachable, 🟡 slow

### 20.3 AI Ping Analysis

After a sweep, AI analyzes the results:

- Identifies patterns (e.g., all routers in a region down)
- Correlates with topology (is a transit router down?)
- Suggests root cause and next steps

---

## 21. Traffic Analysis

### 21.1 Protocol Statistics

Per-router protocol traffic analysis:

- Protocol distribution (BGP, IS-IS, MPLS, OSPF)
- Packet counts by protocol
- Error rates and drops

### 21.2 Interface Counters

Detailed per-interface traffic metrics:

- Input/output bytes and packets
- Error counters (CRC, input errors, output drops)
- Utilization percentage

### 21.3 Flow Analysis

Deep packet flow analysis on a specific router:

- Active flow count
- Top talkers
- Protocol breakdown

### 21.4 Session Table

Active session information for security devices:

- Current sessions
- Session creation rate
- Protocol distribution

### 21.5 AI Traffic Analysis

AI-powered analysis of traffic patterns:

- Anomaly detection
- Bandwidth optimization suggestions
- Capacity planning recommendations

---

## 22. Discovery Engine

### 22.1 Interface Discovery

Discover all interfaces on a router:

- Interface names and types
- Operational status (up/down)
- IP addressing
- Speed/duplex settings

### 22.2 Neighbor Discovery

Find all directly connected neighbors:

- LLDP neighbors
- IS-IS adjacencies
- BGP peerings
- Interface-level connectivity

### 22.3 Full Network Scan

Scan all routers simultaneously to build a comprehensive view:

- All interfaces across the fleet
- All neighbor relationships
- Link mapping

### 22.4 AI Topology Map

AI generates an intelligent topology description:

- Analyzes scan results
- Identifies connectivity patterns
- Highlights potential issues
- Produces a logical network map

---

## 23. DNS Intelligence

### 23.1 DNS Lookup

Forward DNS resolution from a router's perspective:

- Specify a hostname and record type (A, AAAA, MX, etc.)
- See the resolution path and results

### 23.2 Reverse DNS

Reverse DNS lookup for IP addresses:

- Convert IPs to hostnames
- Useful for log correlation

### 23.3 Batch DNS

Bulk DNS operations across multiple routers or hostnames.

### 23.4 DNS Config Audit

Audit DNS configuration across the fleet:

- Check that DNS servers are configured
- Verify DNS resolution works
- Identify misconfigured DNS settings

---

## 24. Path Analysis & Quantum Engine

### 24.1 Shortest Path

Find the shortest path between any two routers:

1. Select source and destination
2. View the path with all intermediate hops
3. Path is highlighted on the topology map

### 24.2 Multi-Algorithm Path Analysis

Compare paths using different algorithms:

- **Dijkstra** — Standard shortest path
- **BFS** — Breadth-first search
- **All Paths** — Enumerate all possible paths
- Comparison of hop count, latency estimates, and path diversity

### 24.3 What-If Analysis

Simulate network failures:

1. Select a link or node to "fail"
2. See how traffic would reroute
3. Identify if the network remains connected
4. Assess impact on specific source-destination pairs

### 24.4 Capacity Planning

AI-driven capacity analysis:

- Current link utilization estimates
- Growth projections
- Bottleneck identification
- Upgrade recommendations

### 24.5 Quantum Engine Features

| Feature | Description |
|---------|-------------|
| **SPOF Detection** | Tarjan's algorithm finds single points of failure |
| **Community Detection** | Louvain algorithm finds logical clusters |
| **Anomaly Detection** | Quantum walk-based anomaly detector |
| **Path Optimization** | Quantum annealing-inspired optimizer |
| **Benchmark** | Performance benchmark of all quantum algorithms |

---

## 25. Monitoring & Health Dashboard

### 25.1 Health Dashboard

Aggregated health view across all devices:

- Per-device health score
- Protocol status (BGP, IS-IS, MPLS)
- Resource utilization (CPU, memory, storage)
- Alert summary

### 25.2 Protocol Health

Per-protocol health monitoring:

- BGP session states across all routers
- IS-IS adjacency status
- MPLS LSP status
- OSPF neighbor states

### 25.3 AI Incident Detection

Automated incident detection and response:

1. Input symptoms (text description)
2. AI classifies incident priority (P1–P4)
3. Provides:
   - Root cause hypothesis (ranked by probability)
   - Blast radius assessment
   - Triage commands to run
   - Remediation steps
   - Escalation criteria
   - Post-incident review checklist

---

## 26. Notifications

### 26.1 Notification Channels

Configure notification destinations:

- **Webhook** — HTTP POST to any URL
- **Email** — SMTP-based notifications
- **Slack** — Webhook integration
- **Custom** — Any HTTP endpoint

### 26.2 Sending Notifications

Notifications can be triggered:

- Manually from the UI
- From scheduled tasks
- From workflow steps
- From alert thresholds

### 26.3 Notification History

Full audit trail of all sent notifications:

- Timestamp
- Channel used
- Message content
- Delivery status

### 26.4 AI Summary

AI-generated summary of notification history:

- Pattern detection (recurring issues)
- Trend analysis
- Recommendation for alert tuning

---

## 27. Git Export & Version Control

### 27.1 Initialize Git Repository

1. Navigate to **Git Export** view
2. Click **"Initialize"** to create a git repo in the export directory
3. The `git_export/` directory is created and initialized

### 27.2 Export Configs

1. Click **"Export"** to save all golden configs to the git repo
2. Each export creates a commit with:
   - All `.conf` files
   - Timestamp-based commit message
   - Full diff of changes since last export

### 27.3 Commit History

View the git log:

- Commit hash, author, date, message
- Click any commit to see the full diff

### 27.4 Config Diff by Commit

Compare any two commits to see exactly what changed in your network configurations over time.

---

## 28. Rollback Management

### 28.1 Rollback Diff

View the difference between the current config and a previous rollback version:

1. Select a router
2. The system fetches `show configuration | compare rollback 1`
3. See exactly what would be rolled back

### 28.2 Execute Rollback

Perform a configuration rollback:

1. Review the rollback diff
2. Confirm the rollback
3. The system executes `rollback 1` and commits
4. Uses commit confirmed for safety

---

## 29. Results Capture & Compare

### 29.1 Capture Results

Save command outputs for later comparison:

1. Execute any command
2. Click **"Capture"** to save the output with a name and timestamp
3. Results stored in `results/` directory

### 29.2 Compare Results

Compare two captured results side-by-side:

1. Select two saved captures
2. View the diff highlighting changes
3. Useful for pre/post maintenance comparison

### 29.3 Results Management

- **List** all saved captures
- **View** individual captures
- **Delete** old captures
- **Compare** any two captures

---

## 30. Logs Viewer

### 30.1 Bridge Logs

View MCP bridge communication logs:

- Located in `logs/` directory
- Named by date: `bridge_YYYY-MM-DD.log`
- Shows all MCP communication including requests and responses

### 30.2 Log Viewer

1. Navigate to **Logs** view
2. Select a log file from the list
3. View contents with timestamp highlighting
4. Search within logs

---

## 31. Copilot Sidebar

### 31.1 What Is Copilot?

The Copilot Sidebar is a persistent AI assistant panel that provides:

- **Context-aware suggestions** based on your current view
- **Quick actions** relevant to what you're looking at
- **Proactive recommendations** for network improvement

### 31.2 How It Works

1. The sidebar sends your current view context to `/api/ai/copilot-suggest`
2. AI analyzes the context and generates actionable suggestions
3. Suggestions appear as clickable cards
4. Click a suggestion to execute the recommended action

---

## 32. API Reference

### 32.1 Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | System health check |
| GET | `/api/devices` | List all devices |
| GET | `/api/config` | Get running config.yaml |
| GET | `/api/network-stats` | Topology statistics |

### 32.2 Bootstrap

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/bootstrap/status` | Check golden config sync status |
| POST | `/api/bootstrap/sync` | Sync all routers' configs |
| POST | `/api/bootstrap/sync-one/<router>` | Sync one router's config |

### 32.3 Topology

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/topology` | Get topology graph data |
| GET | `/api/topology/stats` | Get topology statistics |
| GET | `/api/shortest-path?source=X&target=Y` | Find shortest path |

### 32.4 Golden Configs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/golden-configs` | List all golden configs |
| GET | `/api/golden-configs/<router>` | Get specific golden config |
| GET | `/api/config-diff/<router>` | Diff golden vs. live |
| GET | `/api/config-search?q=X&regex=0` | Search across configs |

### 32.5 MCP Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/mcp/execute` | Execute single command |
| POST | `/api/mcp/batch` | Execute batch command |
| GET | `/api/mcp/facts/<router>` | Get device facts |
| GET | `/api/mcp/live-config/<router>` | Get live running config |
| POST | `/api/mcp/deploy-config` | Deploy configuration |
| POST | `/api/mcp/poll-status` | Poll device status |
| GET | `/api/mcp/live-devices` | List live devices from MCP |

### 32.6 Templates

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/templates` | List available templates |
| POST | `/api/templates/render` | Render a template with variables |
| POST | `/api/templates/deploy` | Deploy rendered template |

### 32.7 Scheduled Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/scheduled-tasks` | List all tasks |
| POST | `/api/scheduled-tasks` | Create new task |
| DELETE | `/api/scheduled-tasks/<id>` | Delete a task |
| POST | `/api/scheduled-tasks/<id>/toggle` | Enable/disable task |
| POST | `/api/scheduled-tasks/<id>/run` | Run task now |
| GET | `/api/scheduled-tasks/<id>/history` | Get task history |
| POST | `/api/scheduled-tasks/cron` | Create cron-based task |
| GET | `/api/scheduled-tasks/calendar` | Calendar view |

### 32.8 Workflows

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/workflows` | List workflows |
| POST | `/api/workflows` | Save workflow |
| DELETE | `/api/workflows/<name>` | Delete workflow |
| POST | `/api/workflows/execute` | Execute workflow |

### 32.9 AI & Brain

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ai/chat` | Standard AI chat |
| POST | `/api/ai/stream` | Streaming AI chat |
| POST | `/api/ai/analyze` | Focused AI analysis |
| POST | `/api/ai/chat-agentic` | Agentic AI (multi-tool) |
| POST | `/api/ai/quick-actions` | Quick diagnostic actions |
| POST | `/api/ai/copilot-suggest` | Copilot suggestions |
| POST | `/api/ai/confidence-score` | Score analysis confidence |
| POST | `/api/ai/ensemble` | Multi-perspective analysis |
| GET | `/api/brain/status` | Brain engine status |
| GET | `/api/brain/scripts` | Available scripts |
| POST | `/api/brain/scripts/select` | Select scripts |
| POST | `/api/brain/classify` | Classify a problem |
| POST | `/api/brain/investigate` | Start investigation |
| POST | `/api/brain/rag` | RAG knowledge query |
| POST | `/api/brain/predict` | Predictive analysis |
| GET | `/api/brain/history` | Investigation history |
| GET | `/api/brain/history/<id>` | Specific investigation |

### 32.10 Remediation

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/remediate/propose` | Propose remediation |
| GET | `/api/remediate/list` | List remediations |
| GET | `/api/remediate/<id>` | Get remediation detail |
| POST | `/api/remediate/<id>/approve` | Approve remediation |
| POST | `/api/remediate/<id>/reject` | Reject remediation |
| POST | `/api/remediate/<id>/execute` | Execute remediation |
| POST | `/api/deploy/safe` | Safe deployment with rollback |

### 32.11 Pools

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/pools` | List all pools |
| POST | `/api/pools` | Create pool |
| PUT | `/api/pools/<id>` | Update pool |
| DELETE | `/api/pools/<id>` | Delete pool |
| POST | `/api/pools/ai-recommend` | AI-recommended pools |

### 32.12 Ping & Connectivity

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/ping/<router>` | Ping a router |
| POST | `/api/ping/sweep` | Ping sweep |
| POST | `/api/ping/ai-analyze` | AI ping analysis |

### 32.13 Compliance & Validation

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/validate` | Validate single device |
| POST | `/api/validate/batch` | Validate multiple devices |
| POST | `/api/validate/ai-compliance` | AI compliance analysis |

### 32.14 Notifications

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/notifications/channels` | List channels |
| POST | `/api/notifications/channels` | Create channel |
| DELETE | `/api/notifications/channels/<id>` | Delete channel |
| POST | `/api/notifications/send` | Send notification |
| GET | `/api/notifications/history` | Notification history |
| POST | `/api/notifications/ai-summary` | AI summary |

### 32.15 Git Export

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/git-export/init` | Initialize git repo |
| POST | `/api/git-export/export` | Export configs to git |
| GET | `/api/git-export/log` | Git commit log |
| GET | `/api/git-export/diff/<commit>` | Diff at commit |

### 32.16 Rollback

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/rollback/diff/<router>` | Rollback diff |
| POST | `/api/rollback/execute` | Execute rollback |

### 32.17 Results

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/results/capture` | Capture results |
| GET | `/api/results` | List captures |
| GET | `/api/results/<name>` | Get specific capture |
| POST | `/api/results/compare` | Compare two captures |
| DELETE | `/api/results/<name>` | Delete capture |

### 32.18 Discovery

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/discovery/interfaces/<router>` | Interface list |
| GET | `/api/discovery/interfaces/<router>/detail` | Interface detail |
| GET | `/api/discovery/neighbors/<router>` | Neighbor discovery |
| POST | `/api/discovery/full-scan` | Full network scan |
| POST | `/api/discovery/ai-map` | AI topology map |

### 32.19 Traffic Analysis

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/traffic/protocol-stats/<router>` | Protocol stats |
| GET | `/api/traffic/interface-counters/<router>` | Interface counters |
| GET | `/api/traffic/flow-analysis/<router>` | Flow analysis |
| GET | `/api/traffic/session-table/<router>` | Session table |
| POST | `/api/traffic/ai-analyze` | AI traffic analysis |

### 32.20 DNS Intelligence

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dns/lookup/<router>` | DNS lookup |
| GET | `/api/dns/reverse/<router>` | Reverse DNS |
| POST | `/api/dns/batch` | Batch DNS |
| POST | `/api/dns/config-audit` | DNS config audit |

### 32.21 Security

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/security/audit/<router>` | Security audit |
| POST | `/api/security/threat-check` | Threat check |
| POST | `/api/security/credential-scan` | Credential scan |
| POST | `/api/security/hardening-report` | Hardening report |

### 32.22 Path Analysis

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/path/multi-algorithm` | Multi-algorithm path |
| POST | `/api/path/what-if` | What-if simulation |
| POST | `/api/path/capacity-plan` | Capacity planning |

### 32.23 Monitoring

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/monitor/health-dashboard` | Health dashboard |
| GET | `/api/monitor/protocol-health` | Protocol health |
| POST | `/api/monitor/ai-incident` | AI incident response |

### 32.24 Quantum Engine

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/quantum/optimize` | Quantum path optimization |
| GET | `/api/quantum/anomalies` | Anomaly detection |
| GET | `/api/quantum/communities` | Community detection |
| GET | `/api/quantum/spof` | Single points of failure |
| GET | `/api/quantum/benchmark` | Algorithm benchmark |

### 32.25 Miscellaneous

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/audit-history` | Audit run history |
| GET | `/api/conversations` | Conversation history |
| GET | `/api/logs` | List log files |
| GET | `/api/logs/<filename>` | Read log file |

### 32.26 WebSocket Events

| Event | Direction | Description |
|-------|-----------|-------------|
| `connect` | Client → Server | Initial connection |
| `request_topology` | Client → Server | Request topology data |
| `request_path` | Client → Server | Request path analysis |
| `chat_message` | Bidirectional | AI chat over WebSocket |
| `mcp_command` | Client → Server | Execute MCP command |
| `poll_devices` | Client → Server | Poll device status |
| `task_result` | Server → Client | Scheduled task result |
| `workflow_progress` | Server → Client | Workflow step progress |

---

## 33. Troubleshooting

### 33.1 Cannot Connect to MCP Server

**Symptom:** "MCP connection failed" or no device data

**Solutions:**
1. Verify MCP server is running: `curl http://127.0.0.1:30030/mcp/`
2. Check `config.yaml` → `mcp.url` matches the MCP server address
3. Verify `devices.json` has correct device entries
4. Check MCP server logs for SSH connection errors

### 33.2 Ollama Not Responding

**Symptom:** AI features return errors or timeout

**Solutions:**
1. Verify Ollama is running: `curl http://127.0.0.1:11434/api/tags`
2. Check the model is pulled: `ollama list`
3. Pull the model if missing: `ollama pull gpt-oss`
4. Check `config.yaml` → `ai.ollama_url` is correct

### 33.3 Topology Map is Empty

**Symptom:** No nodes or links on the map

**Solutions:**
1. Check if golden configs exist in `golden_configs/`
2. Run a bootstrap sync: click "Sync All Configs"
3. Verify configs have interface and routing protocol stanzas
4. Check browser console for JavaScript errors

### 33.4 Command Execution Timeout

**Symptom:** Commands hang or return timeout errors

**Solutions:**
1. Increase `mcp.call_timeout` in `config.yaml` (default: 120s)
2. Check router SSH connectivity from the MCP server
3. Verify device credentials in `devices.json`
4. Reduce `batch_concurrency` if running many parallel commands

### 33.5 Brain Engine Low Confidence

**Symptom:** Brain loops to max passes without reaching confidence threshold

**Solutions:**
1. Lower `hypered_brain.confidence_threshold` (default: 70)
2. Increase `max_passes` for more thorough investigation
3. Increase `max_scripts_per_pass` to gather more evidence
4. Ensure the script library has relevant diagnostic scripts

### 33.6 WebSocket Disconnects

**Symptom:** Real-time features stop updating

**Solutions:**
1. Check browser console for WebSocket connection errors
2. Ensure Flask-SocketIO is properly installed: `pip install flask-socketio eventlet`
3. Check for proxy/firewall blocking WebSocket upgrades
4. Refresh the page to reconnect

### 33.7 Database Errors

**Symptom:** SQLite errors in the logs

**Solutions:**
1. Ensure write permissions on the project directory
2. Delete corrupted `.db` files (they auto-recreate)
3. Check disk space — SQLite fails silently on full disk

---

## 34. Security Considerations

### 34.1 Authentication

- **API Key:** Set `NOC_API_KEY` environment variable to require `X-API-Key` header on all API requests
- **No built-in user auth** — deploy behind a reverse proxy with authentication (NGINX, Caddy, etc.)

### 34.2 CORS Policy

- CORS is restricted to localhost origins by default
- Change the CORS configuration in `app.py` if accessing from other hosts

### 34.3 Secret Key

- Flask session secret key is auto-generated per-instance
- Stored in `.secret_key` file (gitignored)
- Regenerated if the file is deleted

### 34.4 Device Credentials

- Stored in `devices.json` (plaintext by default)
- **Recommendation:** Use SSH key authentication (`ssh_key_path` in device config)
- Never commit `devices.json` to version control with real credentials

### 34.5 Network Exposure

- Default bind: `127.0.0.1` (localhost only)
- Set `NOC_HOST=0.0.0.0` only behind a firewall/VPN
- All device communication goes through MCP server — no direct SSH from the web UI

### 34.6 Configuration Safety

- `auto_remediate` is **false** by default — no automatic config changes
- All config deployments use **commit confirmed** with 5-minute auto-rollback
- Change windows enforced (weekday 22:00–06:00)

---

## 35. File & Directory Reference

### 35.1 Root Directory

| File/Dir | Purpose |
|----------|---------|
| `config.yaml` | Master configuration file (all settings) |
| `audit_history.db` | SQLite — audit run history |
| `kb_vectors.pkl` | Knowledge base vector store (pickle) |
| `kb_vectorstore.py` | Vector store builder for RAG |
| `ingest_pdfs.py` | PDF ingestion for knowledge base |
| `ollama_mcp_client.py` | Standalone CLI MCP client |
| `run_audit.py` | Standalone audit runner |
| `junos_commands.json` | Junos command dictionary (validation) |
| `KNOWLEDGE_BASE.md` | Junos knowledge base text |
| `JUNOS_DEEP_KNOWLEDGE.md` | Advanced Junos reference |
| `EXPERT_EXAMPLES.md` | Protocol-specific troubleshooting examples |
| `FULL_PROJECT_DOCUMENTATION.md` | Project documentation |

### 35.2 Web UI (`web_ui/`)

| File | Lines | Purpose |
|------|-------|---------|
| `app.py` | ~4,899 | Flask backend — all API routes, engines, logic |
| `templates/index.html` | ~1,390 | HTML template with all UI components |
| `static/noc.js` | ~3,811 | JavaScript — all frontend logic |
| `static/noc.css` | ~5,274 | CSS — complete styling and animations |
| `quantum_engine.py` | ~500+ | Quantum-inspired graph analysis algorithms |

### 35.3 MCP Server (`junos-mcp-server/`)

| File | Purpose |
|------|---------|
| `jmcp.py` | Main MCP server implementation |
| `devices.json` | Device inventory (SSH credentials) |
| `requirements.txt` | Python dependencies |
| `pyproject.toml` | Project metadata |
| `jmcp_token_manager.py` | Token-based authentication |

### 35.4 Data Directories

| Directory | Purpose |
|-----------|---------|
| `golden_configs/` | Saved baseline configurations (`.conf` + `.meta`) |
| `templates/` | Jinja2 config templates (`.j2` files) |
| `workflows/` | Saved workflow definitions (`.json`) |
| `results/` | Captured command outputs |
| `git_export/` | Git-versioned config exports |
| `conversations/` | Chat conversation history |
| `logs/` | MCP bridge communication logs |
| `tasks/` | Todo lists and planning documents |
| `files/` | Juniper training PDFs for knowledge base |

### 35.5 Database Files

| File | Engine | Purpose |
|------|--------|---------|
| `audit_history.db` | SQLite | Audit run records |
| `analysis_memory.db` | SQLite | AI investigation memory (past findings) |
| `scheduled_tasks.db` | SQLite | Scheduler task definitions and history |
| `device_pools.db` | SQLite | Device pool definitions |
| `notifications.db` | SQLite | Notification channels and history |

---

## Quick Start Checklist

- [ ] Install Python 3.10+
- [ ] Install Ollama and pull `gpt-oss` model
- [ ] Configure `junos-mcp-server/devices.json` with your routers
- [ ] Start MCP server (`python jmcp.py`)
- [ ] Start Ollama (`ollama serve`)
- [ ] Start Web UI (`cd web_ui && python app.py`)
- [ ] Open `http://localhost:5555`
- [ ] Run Bootstrap Sync to fetch golden configs
- [ ] Explore the topology map
- [ ] Try an AI chat: "What's the health of my network?"
- [ ] Run a compliance check across all routers
- [ ] Create your first scheduled task

---

*Junos AI NOC v22.0 — Built for network engineers who demand intelligence at the speed of thought.*
