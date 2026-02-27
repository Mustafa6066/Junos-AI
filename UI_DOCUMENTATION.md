# Junos AI NOC v22.0 — Complete UI Documentation

> Comprehensive technical and functional reference for every element of the Junos AI Network Operations Center user interface.

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Technology Stack](#2-technology-stack)
3. [Design System](#3-design-system)
4. [Application Shell & Header](#4-application-shell--header)
5. [Navigation System](#5-navigation-system)
6. [AI Copilot Sidebar](#6-ai-copilot-sidebar)
7. [Help System](#7-help-system)
8. [Views — Detailed Breakdown](#8-views--detailed-breakdown)
   - [8.1 Dashboard](#81-dashboard)
   - [8.2 Network Topology](#82-network-topology)
   - [8.3 AI Chat (Command Center)](#83-ai-chat-command-center)
   - [8.4 Investigation Engine](#84-investigation-engine)
   - [8.5 Remediation Center](#85-remediation-center)
   - [8.6 Predictive Intelligence](#86-predictive-intelligence)
   - [8.7 Capacity Planning](#87-capacity-planning)
   - [8.8 Device Inventory](#88-device-inventory)
   - [8.9 Device Pools](#89-device-pools)
   - [8.10 Ping & Reachability](#810-ping--reachability)
   - [8.11 Path Finder](#811-path-finder)
   - [8.12 Network Discovery](#812-network-discovery)
   - [8.13 Traffic Analysis](#813-traffic-analysis)
   - [8.14 Security Center](#814-security-center)
   - [8.15 DNS Diagnostics](#815-dns-diagnostics)
   - [8.16 Golden Configs](#816-golden-configs)
   - [8.17 Template Engine](#817-template-engine)
   - [8.18 Data Validation](#818-data-validation)
   - [8.19 Result Comparison](#819-result-comparison)
   - [8.20 Git Export](#820-git-export)
   - [8.21 Workflow Builder](#821-workflow-builder)
   - [8.22 Task Scheduler](#822-task-scheduler)
   - [8.23 Log Forensics](#823-log-forensics)
   - [8.24 Notification Channels](#824-notification-channels)
9. [Chain-of-Thought Reasoning](#9-chain-of-thought-reasoning)
10. [Real-Time Features](#10-real-time-features)
11. [Data Flow Architecture](#11-data-flow-architecture)
12. [Responsive Design](#12-responsive-design)
13. [File Reference](#13-file-reference)

---

## 1. Architecture Overview

Junos AI NOC is a **single-page application (SPA)** that serves as a full-featured AI-powered network operations center for Juniper Networks routers. The UI is served by a Flask backend and communicates with two primary services:

- **MCP Server** (`http://127.0.0.1:30030/mcp/`) — JSON-RPC 2.0 endpoint managing 11 Junos routers (P11-P14, P21-P24, PE1-PE3). Executes live commands, gathers facts, renders templates, and commits configurations.
- **Ollama AI Engine** (`http://127.0.0.1:11434`) — Local LLM inference server running the `gpt-oss` model. Powers all AI analysis, chat, chain-of-thought reasoning, and the 7-layer Brain Engine.

The UI is a single HTML page (`index.html`) containing 25 view sections, only one of which is visible at any time. Navigation switches between views without page reloads. All state is managed in-memory via a global JavaScript `state` object.

```
Browser (SPA)
    |
    +-- Flask Backend (port 5555) -- 24+ REST API endpoints
    |       |
    |       +-- MCP Server (port 30030) -- 11 Junos routers
    |       |
    |       +-- Ollama (port 11434) -- gpt-oss model
    |       |
    |       +-- Golden Configs (local .conf files)
    |       |
    |       +-- RAG Knowledge Base (vectorstore)
    |
    +-- WebSocket (Socket.IO) -- Real-time events
```

---

## 2. Technology Stack

| Layer | Technology | Details |
|-------|-----------|---------|
| **Frontend** | HTML5 / CSS3 / Vanilla JS | No framework — pure DOM manipulation |
| **Visualization** | D3.js v7.9.0 | Force-directed topology, SVG charts |
| **Real-time** | Socket.IO 4.7.5 | WebSocket with polling fallback |
| **Icons** | Lucide Icons | SVG icon library, loaded locally |
| **Fonts** | Inter + JetBrains Mono | WOFF2 format, served from `/static/css/fonts.css` |
| **Backend** | Flask + Flask-SocketIO | Python, port 5555 |
| **AI** | Ollama (gpt-oss) | Local LLM, 16 models available |
| **MCP** | JSON-RPC 2.0 | 10 tools, 11 Junos devices |

All libraries are loaded locally — the application functions fully offline with no CDN dependencies.

---

## 3. Design System

### 3.1 Color Palette

The design is inspired by the HPE (Hewlett Packard Enterprise) brand system with a network-operations aesthetic.

| Token | Value | Usage |
|-------|-------|-------|
| `--hpe-green` | `#01A982` | Primary accent, active states, success indicators |
| `--hpe-green-light` | `#17EBA0` | Hover states, highlights |
| `--hpe-green-dark` | `#008567` | Pressed states |
| `--hpe-teal` | `#00E8CF` | Secondary accent |
| `--hpe-purple` | `#7630EA` | Route Reflector nodes, iBGP sessions |
| `--hpe-blue` | `#0D5FFF` | P Router nodes, informational elements |
| `--hpe-orange` | `#FF8300` | Warnings |
| `--hpe-amber` | `#FFBC44` | Graph diameter stat card |
| `--hpe-rose` | `#FC6161` | Errors, critical alerts, SPOF count |
| `--hpe-magenta` | `#FF2DAF` | Accent highlights |

### 3.2 Topology Node Colors

| Token | Value | Maps To |
|-------|-------|---------|
| `--node-pe` | `#01A982` | PE (Provider Edge) routers |
| `--node-p` | `#0D5FFF` | P (Provider Core) routers |
| `--node-rr` | `#7630EA` | RR (Route Reflector) routers |

### 3.3 Typography

| Token | Font Stack | Usage |
|-------|-----------|-------|
| `--font-sans` | `Inter, -apple-system, BlinkMacSystemFont, Segoe UI, system-ui, sans-serif` | All UI text |
| `--font-mono` | `JetBrains Mono, Fira Code, Cascadia Code, monospace` | Config viewers, code blocks, log output |

### 3.4 Spacing & Radii

| Token | Value |
|-------|-------|
| `--header-height` | `72px` |
| `--radius-sm` | `8px` |
| `--radius-md` | `12px` |
| `--radius-lg` | `16px` |
| `--radius-xl` | `24px` |

### 3.5 Transitions

| Token | Value |
|-------|-------|
| `--ease-out` | `cubic-bezier(0.16, 1, 0.3, 1)` |
| `--transition-fast` | `150ms` |
| `--transition-normal` | `250ms` |
| `--transition-slow` | `400ms` |

### 3.6 Dark Theme (Default)

- Background body: `#0B0F19` (deep navy)
- Surface: `#111827`
- Elevated: `#1A2332`
- Cards: `rgba(26, 35, 50, 0.85)` with `20px` backdrop blur (glassmorphism)
- Text primary: `#F1F5F9`
- Text secondary: `#94A3B8`
- Borders: `rgba(255, 255, 255, 0.06)` to `rgba(255, 255, 255, 0.1)`
- Shadows: Deep black-based (`rgba(0,0,0,0.3)` to `rgba(0,0,0,0.5)`)
- Green glow: `0 0 30px rgba(1, 169, 130, 0.15)`

### 3.7 Light Theme

- Background body: `#F7F9FC`
- Surface: `#FFFFFF`
- Cards: `rgba(255, 255, 255, 0.9)`
- Text primary: `#1E293B`
- Borders: `rgba(0, 0, 0, 0.04)` to `rgba(0, 0, 0, 0.08)`
- Shadows: Light (`rgba(0,0,0,0.06)` to `rgba(0,0,0,0.1)`)

Theme is toggled via the sun/moon icon in the header and persists in `localStorage` under key `noc-theme`.

---

## 4. Application Shell & Header

### 4.1 Fixed Glassmorphism Header

The header is a `72px` tall fixed bar at the top of the viewport with glassmorphism styling:
- `backdrop-filter: blur(20px)` for frosted glass effect
- Semi-transparent background from `--bg-glass`
- Subtle bottom border and shadow
- Transitions to a more compact "scrolled" state when the user scrolls past 10px

**Header layout (left to right):**

| Section | Elements |
|---------|----------|
| **Left** | Logo (SVG topology triangle graph) + Title "Junos AI NOC" with green accent on "NOC" + Version badge `v22.0` |
| **Center** | Primary navigation (Dashboard, Topology, AI Chat) + 3 dropdown menus (Intelligence, Infrastructure, Operations) |
| **Right** | AI Copilot toggle (sparkles icon with pulse dot) + Theme toggle (sun/moon) + Connection status badge (green dot + "Live" / "Offline") + Mobile menu hamburger |

### 4.2 Logo

The logo is a minimal SVG topology graph drawn inline:
- A circle border at 30% opacity
- Three nodes (top, bottom-left, bottom-right) as filled circles
- Three connecting lines forming a triangle
- Color inherits from `currentColor` (adapts to theme)

### 4.3 Connection Status Badge

Located at the far right of the header. Three possible states:

| State | Dot Color | Text | Condition |
|-------|-----------|------|-----------|
| **Live** | Green pulsing | "Live" | MCP connected, devices reachable |
| **MCP Up** | Amber | "MCP Up" | MCP connected but devices unreachable |
| **Offline** | Gray | "Offline" | MCP server not reachable |

---

## 5. Navigation System

The navigation is organized into **3 primary buttons** and **3 dropdown menus**, providing access to all 25 views.

### 5.1 Primary Buttons (Always Visible)

| Button | Icon | View | Description |
|--------|------|------|-------------|
| **Dashboard** | `layout-dashboard` | `dashboard` | Network health overview — default landing view |
| **Topology** | `network` | `topology` | Interactive D3.js force-directed graph |
| **AI Chat** | `bot` | `ai-chat` | Full conversational AI interface |

### 5.2 Intelligence Dropdown (`navAI`)

AI-powered analysis views. Icon: `brain`.

| Item | Icon | View | Description |
|------|------|------|-------------|
| Investigate | `search` | `investigate` | Deep Brain-powered root cause analysis |
| Remediate | `wrench` | `remediate` | Propose, approve & deploy fixes |
| Predict | `trending-up` | `predictive` | Failure forecast & ensemble analysis |
| Capacity Planning | `bar-chart-3` | `capacity` | What-if & growth analysis |

### 5.3 Infrastructure Dropdown (`navInfra`)

Device and network infrastructure tools. Icon: `server`.

| Item | Icon | View | Description |
|------|------|------|-------------|
| Devices | `monitor` | `devices` | Device inventory & monitoring |
| Device Pools | `layers` | `pools` | Logical device grouping |
| Ping & Reachability | `radio` | `ping` | ICMP testing via MCP |
| Path Finder | `route` | `pathfinder` | IS-IS shortest path analysis |
| Discovery | `scan` | `discovery` | LLDP / ARP neighbor mapping |
| Traffic Analysis | `activity` | `traffic` | Protocol stats & flow inspection |
| Security Center | `shield-alert` | `security` | Threat detection & hardening |
| DNS Diagnostics | `globe` | `dns` | Resolution & config audit |

### 5.4 Operations Dropdown (`navOps`) — Mega Menu

Two-column wide dropdown. Icon: `settings`.

**Left Column — Configuration:**

| Item | Icon | View | Description |
|------|------|------|-------------|
| Golden Configs | `file-diff` | `configs` | Diffs & cross-device search |
| Templates | `file-code` | `templates` | Jinja2 rendering & deploy |
| Validation | `shield-check` | `validation` | AI compliance checking |
| Compare | `columns-2` | `compare` | Side-by-side diff analysis |
| Git Export | `git-branch` | `git-export` | Version-control configs |

**Right Column — Automation:**

| Item | Icon | View | Description |
|------|------|------|-------------|
| Workflows | `git-merge` | `workflows` | Chain MCP operations |
| Scheduler | `clock` | `scheduler` | CRON-style task execution |
| Log Forensics | `scroll-text` | `logs` | Browse & analyze logs |
| Alerts | `bell` | `notifications` | Slack, webhook notifications |

### 5.5 Navigation Behavior

- **Active state**: The active view's button or dropdown item gets an `.active` class (green indicator bar and highlighted text). Parent dropdown triggers show a `.has-active-child` class.
- **Dropdown backdrop**: An invisible full-screen backdrop is activated when any dropdown opens. Clicking it closes all dropdowns.
- **Escape key**: Pressing Escape closes all open dropdowns and the help modal.
- **Mobile**: A hamburger menu button toggles the navigation into a vertical mobile-open state.

---

## 6. AI Copilot Sidebar

A **persistent slide-in sidebar** accessible from any view via the sparkles icon in the header. It provides context-aware AI assistance without leaving the current view.

### 6.1 Structure

| Section | Description |
|---------|-------------|
| **Header** | Title "AI Copilot" with clear and close buttons |
| **Context Bar** | Shows "Watching: [current view name]" — updates automatically when switching views |
| **Audit Trail** | Collapsible section tracking all user actions (navigation, deploys, executions, config views, searches). Each action is timestamped with an icon. Important actions receive AI-generated commentary (1-sentence assessment). Max 50 entries, most recent 20 displayed. |
| **AI Insights** | Auto-generated bullet insights for the current view, cached for 60 seconds. Dashboard gets topology health insights. Topology gets design analysis. Configs get management tips. Other views get generic tips. |
| **Proactive Suggestions** | AI-generated suggestions based on the current context |
| **Mini Chat** | Compact chat input at the bottom for quick questions. Uses the agentic AI endpoint. Responses include type badges (Brain, RAG, Quick). |

### 6.2 Context Awareness Map

When the user switches views, the copilot updates its context text:

| View | Context Text |
|------|-------------|
| Dashboard | "Watching: Dashboard — Monitoring network health" |
| Topology | "Watching: Topology — Analyzing network structure" |
| AI Chat | "Active: Full AI Conversation Mode" |
| Configs | "Watching: Configuration Management" |
| Templates | "Watching: Template Engine — Ready to audit deployments" |
| Logs | "Watching: Log Forensics — Scanning for anomalies" |
| Others | "Watching: [view name]" |

### 6.3 Audit Trail Actions

Each logged action has a type that maps to an icon:

| Type | Icon | Examples |
|------|------|----------|
| `navigate` | compass | View switches, help views |
| `deploy` | upload | Template deployments, remediation deploys |
| `execute` | zap | Command executions, workflow runs |
| `create` | plus-circle | Pool creation, channel creation |
| `delete` | trash-2 | Resource deletion |
| `config_view` | file-text | Config file opened for viewing |
| `search` | search | Config search, log search |
| `ai` | bot | AI quick actions, AI analysis |
| `warning` | alert-triangle | Errors, failures |
| `ping` | radio | Ping operations |
| `validate` | check-circle-2 | Validation runs |

---

## 7. Help System

Every view includes a **help icon button** (circle with "?" icon) in the top-right corner of the view header. Clicking it opens a centered modal with structured guidance.

### 7.1 Help Modal Structure

| Section | Content |
|---------|---------|
| **Purpose** | What the view does and why it exists |
| **Inputs** | What the user needs to provide or configure |
| **Expected Output** | What results the view produces |
| **Tips** | 2-3 bullet-point tips for effective use (green dot bullets) |

### 7.2 Coverage

All 24 views have help entries defined in the `VIEW_HELP` dictionary in `noc.js`. Each entry contains `purpose`, `inputs`, `outputs`, and `tips[]`.

### 7.3 Modal Behavior

- Opens centered on screen with a dark semi-transparent overlay
- Click overlay or press Escape to close
- Close button (X) in the top-right corner
- Glassmorphism styling with rounded corners and backdrop blur

---

## 8. Views — Detailed Breakdown

### 8.1 Dashboard

**View ID:** `view-dashboard` | **Default active view**

The landing page providing a real-time network health overview.

**Components:**

| Component | Description |
|-----------|-------------|
| **Bootstrap Banner** | Shown on first run when no golden configs exist. Offers a "Sync All Configs" button to fetch configurations from MCP-connected routers. Shows progress during sync. Hidden once configs are available. |
| **AI Context Bar** | Green-accented bar with 3 quick action buttons: Health Check, Anomalies, Optimize. Each triggers an AI analysis in the copilot sidebar. |
| **Stats Grid** | 6 stat cards in a responsive grid: |
| | 1. **Total Devices** (green accent) — count of topology nodes |
| | 2. **Physical Links** (blue accent) — count of topology links |
| | 3. **iBGP Sessions** (purple accent) — count of BGP sessions |
| | 4. **Redundancy Score** (teal accent) — graph theory redundancy metric |
| | 5. **Graph Diameter** (amber accent) — longest shortest path in the topology |
| | 6. **Points of Failure** (rose accent) — SPOF count |
| **Dashboard Grid** | 3-card grid: |
| | 1. **Mini Topology** — Compact D3.js force-directed preview with "Expand" button |
| | 2. **Device Roles** — SVG donut chart showing PE / P / RR distribution |
| | 3. **Protocol Summary** — Horizontal bar chart showing IS-IS, BGP, LDP, RSVP, MPLS adoption |
| **Device Inventory Table** | Full-width data table with columns: Device, Role, Loopback, Interfaces, IS-IS, BGP, LDP, Status. Includes a filter input for real-time text search. Status shows Live (green), Down (red), or Config-only (gray). |

**Data Source Indicator:** The subtitle dynamically shows the data source:
- "Live MCP — N devices reachable" with a green badge
- "MCP Connected — N devices unreachable" with an amber badge  
- "Offline — Showing golden config data" with a gray badge

**API Endpoints Used:** `/api/topology`, `/api/devices`, `/api/network-stats`, `/api/mcp/live-devices`, `/api/health`

---

### 8.2 Network Topology

**View ID:** `view-topology`

Interactive D3.js force-directed topology visualization.

**Components:**

| Component | Description |
|-----------|-------------|
| **AI Context Bar** | Quick actions: Redundancy analysis, Capacity analysis |
| **Topology Controls** | Layout selector (Force-Directed, Hierarchical, Radial, Circular) + Layer toggles (IS-IS, iBGP, LDP, Labels) + Reset button |
| **Topology SVG** | Full-width interactive SVG canvas. Nodes are draggable. Supports pan and zoom. |
| **Legend** | Color-coded legend showing PE Router (green), P Router (blue), Route Reflector (purple), Physical Link (solid), iBGP Session (dashed) |
| **Node Detail Panel** | Slide-in panel showing per-node information: interfaces, IS-IS neighbors, BGP sessions. Opens on node click. Close button (X). |

**Layout Modes:**
- **Force-Directed**: Physics-based simulation where connected nodes attract and unconnected nodes repel. Best for organic exploration.
- **Hierarchical**: Top-down layout with PE nodes at edges and P/RR nodes in the core.
- **Radial**: Concentric circles with the most-connected node at center.
- **Circular**: Nodes placed evenly around a circle.

**Interaction:**
- Click a node to open its detail panel
- Drag nodes to rearrange the layout
- Scroll/pinch to zoom
- Layer toggles show/hide different protocol overlays

---

### 8.3 AI Chat (Command Center)

**View ID:** `view-ai-chat`

Full conversational AI interface powered by the 7-layer Brain Engine.

**Components:**

| Component | Description |
|-----------|-------------|
| **Welcome Screen** | Displayed when no messages exist. Shows the AI avatar (topology SVG), title "Junos AI Digital Partner", description, and 6 quick-action buttons. |
| **Chat Messages** | Scrollable message list with user and AI messages. AI messages include expandable chain-of-thought panels and confidence bars. |
| **Chat Input** | Textarea at the bottom with send button. Enter sends, Shift+Enter adds newline. |

**Quick Action Buttons:**
1. Health Assessment — full network health report
2. SPOF + Remediation — single points of failure analysis
3. BGP Audit — iBGP session verification
4. Security Audit — CIS-style compliance check
5. Best Practice Check — config vs. best practices comparison
6. Audit Trail — recent user actions summary

**AI Response Pipeline (3-level fallback):**
1. **Agentic** (`/api/ai/chat-agentic`) — Full Brain Engine with investigation, RAG, and protocol specialists
2. **Streaming** (`/api/ai/chat-stream`) — Streamed token-by-token responses
3. **Non-streaming** (`/api/ai/chat`) — Standard request/response
4. **Local fallback** — Error message if all API calls fail

**Chain-of-Thought Panel:** Each AI response can include a collapsible CoT panel showing reasoning steps and confidence score. See [Section 9](#9-chain-of-thought-reasoning) for details.

---

### 8.4 Investigation Engine

**View ID:** `view-investigate` | **Dynamically rendered by `renderInvestigationView()`**

AI-powered deep investigation using the 7-layer Brain Engine.

**Functionality:**
- Describe a network problem in natural language
- Select a symptom category for structured analysis
- The Brain Engine orchestrates multi-source evidence gathering
- Results include step-by-step chain-of-thought reasoning, root cause identification, confidence scores, affected devices, and remediation options

**Features:**
- Help button with contextual guidance
- Integrates with the remediation center for one-click fix application
- Brain progress events streamed via WebSocket

---

### 8.5 Remediation Center

**View ID:** `view-remediate` | **Dynamically rendered by `renderRemediationView()`**

AI-generated fix playbooks with review-before-deploy workflow.

**Functionality:**
- Reviews AI-recommended Junos configuration changes
- Allows selective approval of individual remediation actions
- Deploys approved changes to routers via MCP
- Generates rollback plans alongside every fix
- All actions logged in the audit trail

---

### 8.6 Predictive Intelligence

**View ID:** `view-predictive` | **Dynamically rendered by `renderPredictiveView()`**

Ensemble AI analysis for proactive risk forecasting.

**Functionality:**
- Combines topology graph metrics, protocol health scores, and historical patterns
- Generates per-device risk scores and failure probability forecasts
- Identifies protocol degradation trends and capacity bottlenecks
- Produces preemptive recommendations

---

### 8.7 Capacity Planning

**View ID:** `view-capacity`

What-if failure simulation and growth analysis.

**Components:**

| Component | Description |
|-----------|-------------|
| **What-If Failure Analysis** | Select a node or link pair to simulate removal from the topology. Shows impact on paths and traffic re-routing. |
| **Multi-Path Analysis** | Select source and target nodes to compute all equal and unequal cost paths between them. |
| **AI Capacity Plan** | One-click button to generate a full AI-powered capacity plan including bottleneck analysis, growth projections, and upgrade roadmap. |
| **Results Display** | Raw output in a code block + AI analysis in a formatted card |

---

### 8.8 Device Inventory

**View ID:** `view-devices`

Card-based device grid showing all routers.

**Components:**
- Grid of device cards, each showing:
  - Device name and role (PE / P / RR)
  - Loopback IP address
  - Interface count
  - Protocol status (IS-IS, BGP, LDP) with Yes/No badges
  - Live MCP reachability badge (green = reachable, red = unreachable, gray = config-only)

---

### 8.9 Device Pools

**View ID:** `view-pools`

Logical device grouping for bulk operations.

**Components:**

| Component | Description |
|-----------|-------------|
| **Toolbar** | Create Pool button + AI Recommend Pools button |
| **AI Recommendations** | Collapsible card showing AI-suggested groupings based on topology roles |
| **Pools Grid** | Color-coded pool cards showing name, description, member devices, and tags |
| **Create Pool Modal** | Form with name, description, color picker, multi-select device list, and comma-separated tags |

---

### 8.10 Ping & Reachability

**View ID:** `view-ping`

ICMP-equivalent testing via MCP.

**Components:**

| Component | Description |
|-----------|-------------|
| **Ping Controls** | Single router dropdown + Ping button + Sweep All Routers button + AI Analyze button |
| **Results Grid** | Per-device result cards showing Reachable/Unreachable with response time |
| **AI Analysis** | Correlates unreachable devices with IS-IS topology to find the likely failure point |

---

### 8.11 Path Finder

**View ID:** `view-pathfinder`

IS-IS metric-based shortest path computation using Dijkstra's algorithm.

**Components:**

| Component | Description |
|-----------|-------------|
| **Path Controls** | Source router dropdown, arrow indicator, target router dropdown, Find Path button |
| **Path Results** | Ordered hop list with per-link IS-IS metrics and total path cost. Shows ECMP paths when available. |
| **Path Topology** | Dedicated SVG topology with the computed path highlighted |

---

### 8.12 Network Discovery

**View ID:** `view-discovery`

Infrastructure scanning via MCP.

**Components:**

| Component | Description |
|-----------|-------------|
| **Full Scan** | One-click button to scan all routers for interfaces, LLDP neighbors, ARP tables, and OS versions |
| **Per-Device Discovery** | Router selector + buttons for Interfaces, Neighbors, Detail Stats |
| **Results** | Raw Junos output in a code block + AI Analyze button |
| **AI Analysis** | Builds a complete physical connectivity map from scan results |

---

### 8.13 Traffic Analysis

**View ID:** `view-traffic`

Protocol statistics and flow analysis.

**Components:**

| Component | Description |
|-----------|-------------|
| **Controls** | Router selector + 4 analysis buttons (Protocol Stats, Interface Counters, Flow Analysis, Sessions) + optional interface filter |
| **Results** | Raw Junos output in a code block |
| **AI Analysis** | Selectable focus mode (General, Performance, Security, Anomaly Detection) + AI Analyze button |

---

### 8.14 Security Center

**View ID:** `view-security`

Comprehensive security audit suite.

**Components:**

| Component | Description |
|-----------|-------------|
| **Per-Device Audit** | Router selector + Security Audit button + Threat Detection button + Hardening Report button |
| **Fleet Security** | Credential Scan (All Routers) — scans all configs for cleartext passwords, weak SNMP communities, missing auth. Protocol Health Check — validates BGP/IS-IS authentication. |
| **Results** | Raw output + AI Security Analysis card |

---

### 8.15 DNS Diagnostics

**View ID:** `view-dns`

DNS resolution testing from the router's perspective.

**Components:**

| Component | Description |
|-----------|-------------|
| **DNS Lookup** | Router + domain input for forward lookups |
| **Reverse DNS** | Router + IP input for reverse lookups |
| **Batch DNS** | Comma-separated domains + router for multi-domain batch queries |
| **DNS Config Audit** | AI-powered audit across all routers for consistency, redundancy, and security |
| **Results** | Raw output + AI DNS Analysis card |

---

### 8.16 Golden Configs

**View ID:** `view-configs`

Browse, search, and AI-audit golden configurations.

**Components:**

| Component | Description |
|-----------|-------------|
| **AI Context Bar** | Quick actions: Audit Config, Drift Check, Sync from MCP |
| **Search Toolbar** | Full-text search with regex toggle across all configs |
| **Config List** | Sidebar listing all available router configs |
| **Config Viewer** | Main panel displaying config content with syntax highlighting. Empty state shows "Select a config to view." |
| **Search Results** | Collapsible card showing cross-device search hits with highlighted matches |

**AI Integration:**
- **Audit Config**: AI reviews the viewed config for security issues and best practice violations
- **Drift Check**: AI compares configs across devices for inconsistencies
- **Sync from MCP**: Fetches fresh configs from live routers via MCP

---

### 8.17 Template Engine

**View ID:** `view-templates`

Jinja2 template rendering and deployment.

**Components:**

| Component | Description |
|-----------|-------------|
| **Template Sidebar** | List of available Jinja2 templates (loaded from server) |
| **Template Source** | Read-only code view of the selected template |
| **Variables Input** | Textarea for YAML or JSON template variables |
| **Actions** | Render Preview button + Deploy target router selector + Deploy to Router button |
| **Rendered Output** | Preview of the rendered config with line count badge |
| **Deployment Result** | MCP commit result with diff summary |

**Available Templates:** `bgp_ibgp.j2`, `mpls_ldp.j2`, `ospf_p2p.j2`, `system_hardening.j2`

---

### 8.18 Data Validation

**View ID:** `view-validation`

Pattern-based output validation with AI compliance.

**Components:**

| Component | Description |
|-----------|-------------|
| **Validation Rule** | Router + Command + Pattern + Match Type (Contains, Regex, Not Contains, Exact) |
| **Actions** | Validate (single router) + Validate All Routers (batch) + AI Compliance Audit |
| **Validation Results** | Pass/Fail per router with matched output snippet |
| **Compliance Report** | AI-generated CIS-style report with specific Junos remediation commands |

---

### 8.19 Result Comparison

**View ID:** `view-compare`

Capture-and-compare workflow for command outputs.

**Components:**

| Component | Description |
|-----------|-------------|
| **Capture** | Name + Router + Command -> Capture button |
| **Compare** | Dropdown A + Dropdown B -> Compare button |
| **Comparison Output** | Side-by-side diff with green (added) and red (removed) highlighting. AI explains what changed and its operational impact. |
| **Captured Results Table** | Persistent table of all captured results with name, router, command, line count, timestamp, and actions |

---

### 8.20 Git Export

**View ID:** `view-git-export`

Version control for golden configurations.

**Components:**

| Component | Description |
|-----------|-------------|
| **Toolbar** | Init Repo button + Export & Commit button + Custom commit message input |
| **Export Result** | Shows commit confirmation with files and changes |
| **Commit History** | Full-width table of git commits with change summaries. Refresh button to reload. |

**AI Feature:** Leave the commit message blank and AI will auto-generate a descriptive message based on config diffs.

---

### 8.21 Workflow Builder

**View ID:** `view-workflows`

Visual workflow builder for chaining operations.

**Components:**

| Component | Description |
|-----------|-------------|
| **Workflow Sidebar** | List of saved workflows + New Workflow button |
| **Workflow Header** | Name input + Save + Execute buttons |
| **Steps Area** | Visual list of workflow steps. Empty state prompt when no steps exist. |
| **Add Step** | Step type dropdown + Add Step button |
| **Execution Results** | Per-step output displayed after running the workflow |

**Step Types:**
1. **MCP Command** — Execute a single Junos command on a router
2. **Batch Command** — Execute the same command across multiple routers in parallel
3. **Render Template** — Render a Jinja2 template with variables
4. **Deploy Config** — Commit rendered config to a router via MCP
5. **AI Analyze** — Run AI analysis on previous step output
6. **Condition Check** — Branch based on command output matching a pattern
7. **Wait** — Pause for a specified duration
8. **REST API Call** — Call an external REST endpoint
9. **Python Snippet** — Execute inline Python code
10. **Ping Sweep** — Ping all routers in parallel
11. **Validate Output** — Check previous step output against a pattern
12. **Send Notification** — Send an alert via configured notification channels

---

### 8.22 Task Scheduler

**View ID:** `view-scheduler`

CRON-style recurring command execution.

**Components:**

| Component | Description |
|-----------|-------------|
| **Create Task Form** | Task name + Interval (30s / 5m / 15m / 1h / 6h / 24h) + Junos command + Target routers (multi-select) |
| **Active Tasks Table** | Columns: Name, Command, Interval, Routers, Last Run, Runs, Status, Actions |

**Intervals:** Every 30 seconds, 5 minutes (default), 15 minutes, 1 hour, 6 hours, or Daily.

---

### 8.23 Log Forensics

**View ID:** `view-logs`

Log browsing and AI analysis.

**Components:**

| Component | Description |
|-----------|-------------|
| **Log Sidebar** | List of available log files |
| **Log Toolbar** | Level filter (ERROR, WARNING, INFO, DEBUG) + Search input + Tail N lines + Apply + AI Analyze button |
| **Log Viewer** | Color-coded log display by severity level |
| **AI Log Analysis** | Structured summary identifying error patterns, root causes, and recurring issues |

---

### 8.24 Notification Channels

**View ID:** `view-notifications`

Alert channel management.

**Components:**

| Component | Description |
|-----------|-------------|
| **Toolbar** | Add Channel button + History button |
| **Channel Grid** | Cards showing configured notification channels with status |
| **Test Notification** | Channel selector + Severity + Title + Message + Send + AI Summary button |
| **Notification History** | Collapsible table of sent notifications |
| **Create Channel Modal** | Name + Type (Slack / Mattermost / Generic Webhook) + Webhook URL |

---

## 9. Chain-of-Thought Reasoning

The AI Chat view features an advanced chain-of-thought (CoT) reasoning panel that makes the AI's thinking process visible.

### 9.1 CoT Panel Structure

Each AI response can include an expandable panel below the message text:

```
[Reasoning ▼]
  1. [done]  Classifying query type          — "Network topology analysis"
  2. [done]  Loading topology context         — "11 nodes, 24 links loaded"
  3. [done]  Running Protocol Specialists     — "IS-IS, BGP, LDP analyzed"
  4. [done]  Synthesizing recommendation      — "3 findings generated"

  Confidence: ████████░░ 82%
```

### 9.2 Step States

| State | Icon | Color |
|-------|------|-------|
| `pending` | Circle outline | Gray |
| `active` | Pulsing dot | Green animated |
| `done` | Checkmark | Green solid |

### 9.3 Live CoT Panel

During AI processing, a live CoT panel appears inside the typing indicator, showing real-time reasoning steps as they occur via WebSocket `ai_thinking` events.

### 9.4 Stage Mappings

The `handleAiThinking()` function maps 10 AI processing stages to human-readable labels:

| Stage | Label |
|-------|-------|
| `classifying` | Classifying query type |
| `loading_context` | Loading topology context |
| `rag_search` | Searching knowledge base |
| `protocol_specialist` | Running Protocol Specialists |
| `brain_analysis` | Deep Brain analysis |
| `synthesizing` | Synthesizing recommendation |
| `formatting` | Formatting response |
| `streaming` | Streaming response |
| `mcp_query` | Querying MCP devices |
| `building_response` | Building final response |

### 9.5 Confidence Bar

A horizontal progress bar at the bottom of the CoT panel:
- Track: Semi-transparent background
- Fill: Green gradient (`--hpe-green` to `--hpe-green-light`)
- Percentage text displayed to the right
- Width animated with CSS transition

---

## 10. Real-Time Features

### 10.1 WebSocket Events (Socket.IO)

| Event | Direction | Description |
|-------|-----------|-------------|
| `connect` | Server → Client | Connection established — status dot turns green |
| `disconnect` | Server → Client | Connection lost — status dot turns gray |
| `topology_data` | Server → Client | Full topology data push — triggers dashboard re-render |
| `path_result` | Server → Client | Shortest path computation result |
| `chat_response` | Server → Client | AI chat response (non-streaming mode) |
| `brain_progress` | Server → Client | Investigation/remediation progress events |
| `brain_log` | Server → Client | Brain Engine diagnostic log entries |
| `ai_thinking` | Server → Client | Live reasoning stage updates for CoT panel |

### 10.2 Live MCP Polling

The function `pollLiveDeviceStatus()` calls `/api/mcp/live-devices` to:
- Fetch which devices are currently reachable via MCP
- Update the header connection status badge
- Merge live status into topology nodes (affects device table Status column)
- Update the dashboard subtitle with data source indicator

### 10.3 Streaming AI Responses

The AI Chat supports token-by-token streaming via `/api/ai/chat-stream`:
- Response text is appended character-by-character to the message bubble
- Typing indicator with live CoT panel shows during processing
- Fallback to non-streaming if streaming endpoint fails

---

## 11. Data Flow Architecture

### 11.1 Startup Sequence

```
DOMContentLoaded
    |
    +-- setTheme() — Apply dark/light from localStorage
    +-- initHeaderScroll() — Register scroll listener
    +-- initSocket() — Connect WebSocket
    +-- loadAll() — Parallel API calls:
            |
            +-- GET /api/topology       → state.topology
            +-- GET /api/devices        → state.devices
            +-- GET /api/network-stats  → state.stats
            |
            +-- renderDashboard()
            +-- populatePathSelectors()
            +-- renderConfigList()
            +-- renderDevicesGrid()
            +-- loadTemplates()
            +-- loadLogFiles()
            +-- loadScheduledTasks()
            +-- loadWorkflows()
            +-- checkHealth()
            +-- checkBootstrap()
            +-- pollLiveDeviceStatus()
```

### 11.2 View Switching

```
switchView(view)
    |
    +-- Hide all views, show target view
    +-- Update nav active states (buttons + dropdown items + parent dropdowns)
    +-- Close mobile menu
    +-- Trigger view-specific data loading/rendering
    +-- updateCopilotContext(view) — Update copilot awareness
    +-- logAuditAction('navigate', ...) — Record in audit trail
```

### 11.3 AI Request Flow

```
User types message → sendChat()
    |
    +-- Append user message to chat
    +-- Show typing indicator with live CoT panel
    |
    +-- Try /api/ai/chat-agentic (POST)
    |       |
    |       +-- Brain Engine processes:
    |           1. Query classification
    |           2. Context loading (topology, configs)
    |           3. RAG knowledge base search
    |           4. Protocol specialist analysis
    |           5. Synthesis and recommendation
    |       |
    |       +-- WebSocket emits ai_thinking events → Live CoT panel updates
    |       |
    |       +-- Response includes: text, type, confidence, metadata
    |
    +-- Fallback to /api/ai/chat-stream if agentic fails
    +-- Fallback to /api/ai/chat if streaming fails
    |
    +-- buildCotSteps(data) — Construct reasoning trace from response metadata
    +-- appendChatMessage('ai', text, cotSteps, confidence)
```

### 11.4 MCP Command Execution Flow

```
User action (ping, discovery, validation, etc.)
    |
    +-- Frontend calls Flask API endpoint
    |       |
    |       +-- Flask forwards to MCP Server via JSON-RPC 2.0
    |       |       |
    |       |       +-- MCP executes Junos command on target router(s)
    |       |       +-- Returns structured result
    |       |
    |       +-- Flask optionally runs AI analysis on the result
    |       +-- Returns combined result to frontend
    |
    +-- Frontend renders raw output + AI analysis
```

---

## 12. Responsive Design

The UI adapts to different screen sizes:

| Breakpoint | Behavior |
|------------|----------|
| **Desktop** (> 1024px) | Full horizontal navigation, all dropdowns visible, side-by-side layouts |
| **Tablet** (768px - 1024px) | Navigation items may wrap, grids reduce columns |
| **Mobile** (< 768px) | Hamburger menu toggles vertical navigation. Sidebar layouts stack vertically. Cards go full-width. AI Copilot sidebar overlays the content. |

**Key responsive patterns:**
- `.dashboard-grid` switches from 3-column to 2-column to 1-column
- `.stats-grid` wraps from 6 cards across to 3-across to 2-across
- `.config-panels` stacks config list above config viewer
- `.template-layout` stacks sidebar above main editor
- Navigation dropdown menus adjust width and positioning
- The Operations mega-menu columns stack vertically on narrow screens

---

## 13. File Reference

| File | Lines | Purpose |
|------|-------|---------|
| `web_ui/templates/index.html` | ~1,390 | Application shell — all 25 view sections, header, navigation, modals, copilot sidebar |
| `web_ui/static/js/noc.js` | ~3,811 | All frontend logic — navigation, data loading, rendering, AI integration, WebSocket, help system |
| `web_ui/static/css/noc.css` | ~5,274 | Complete styling — design tokens, dark/light themes, glassmorphism, all component styles, responsive breakpoints, animations |
| `web_ui/static/css/fonts.css` | — | Font-face declarations for Inter and JetBrains Mono (WOFF2) |
| `web_ui/static/js/lucide.min.js` | — | Lucide icon library (SVG icons) |
| `web_ui/static/js/d3.v7.min.js` | — | D3.js v7.9.0 (topology visualization) |
| `web_ui/static/js/socket.io.min.js` | — | Socket.IO v4.7.5 (WebSocket client) |
| `web_ui/app.py` | ~4,897 | Flask backend — API endpoints, MCP integration, Ollama AI, Brain Engine |

---

*Document generated for Junos AI NOC v22.0. Last updated: 2025.*
