# Junos AI NOC — Complete Use Case Catalog
## Every Function & Sub-Function Documented

> **Version**: 22.1 | **Generated**: 2026-02-26  
> **Total API Endpoints**: 75+ | **Frontend Functions**: 140+ | **AI-Powered Features**: 20+

---

## Table of Contents

1. [AI Engine (Ollama)](#1-ai-engine-ollama)
2. [MCP Bridge (Junos Device Control)](#2-mcp-bridge-junos-device-control)
3. [Agentic Chat (Brain + RAG + MCP)](#3-agentic-chat-brain--rag--mcp)
4. [Topology & Network Analysis](#4-topology--network-analysis)
5. [Configuration Management](#5-configuration-management)
6. [Device Pools](#6-device-pools)
7. [Ping & Reachability](#7-ping--reachability)
8. [Data Validation](#8-data-validation)
9. [Notification Service](#9-notification-service)
10. [Scheduled Tasks & Cron](#10-scheduled-tasks--cron)
11. [Workflow Engine](#11-workflow-engine)
12. [Git Export](#12-git-export)
13. [Result Comparison](#13-result-comparison)
14. [Config Rollback](#14-config-rollback)
15. [Remediation Engine](#15-remediation-engine)
16. [Predictive Analysis & Ensemble AI](#16-predictive-analysis--ensemble-ai)
17. [Discovery & Monitoring](#17-discovery--monitoring)
18. [Security & Compliance](#18-security--compliance)
19. [Path Analysis (Advanced)](#19-path-analysis-advanced)
20. [Quantum-Inspired Optimization](#20-quantum-inspired-optimization)
21. [Frontend UI Functions](#21-frontend-ui-functions)
22. [WebSocket Real-Time Events](#22-websocket-real-time-events)
23. [Utility & Infrastructure](#23-utility--infrastructure)

---

## 1. AI Engine (Ollama)

### `detect_ollama_model()`
| Field | Detail |
|-------|--------|
| **Purpose** | Auto-detect available Ollama models at startup; fall back to first available if configured model is missing |
| **Use Case** | NOC boots → checks if "gpt-oss" exists in Ollama → if not, auto-selects "llama3" |
| **Sub-functions** | `httpx.get(/api/tags)` |
| **Corner Case** | Ollama not running → keeps configured model name, logs warning |
| **Corner Case** | Ollama running but 0 models installed → logs warning, AI features unavailable |

### `ollama_chat_async(messages, stream, model)`
| Field | Detail |
|-------|--------|
| **Purpose** | Send chat messages to Ollama and return AI response |
| **Use Case** | User sends "What is MPLS?" → builds message array → calls Ollama → returns response text |
| **Sub-functions** | `httpx.AsyncClient.post(/api/chat)` |
| **Corner Case** | Ollama offline → returns "⚠ Cannot connect to Ollama" (no crash) |
| **Corner Case** | Read timeout → returns "⚠ Ollama request timed out" |
| **Corner Case** | HTTP 500 from Ollama → returns "AI Error (HTTP 500): ..." |
| **Corner Case** | Custom model override → uses passed model instead of global |

### `ollama_analyze_async(system, data, question)`
| Field | Detail |
|-------|--------|
| **Purpose** | Focused AI analysis of structured data (configs, outputs, etc.) |
| **Use Case** | Pass BGP summary output → AI analyzes session states → returns findings |
| **Sub-functions** | `ollama_chat_async()` |
| **Corner Case** | Empty data string → AI still produces response ("No data to analyze") |
| **Corner Case** | Ollama returns empty response → returns "No response from AI" |

### `ollama_stream_async(messages)`
| Field | Detail |
|-------|--------|
| **Purpose** | Stream AI response token-by-token for real-time chat experience |
| **Use Case** | User asks question → tokens appear one by one in chat bubble |
| **Sub-functions** | `httpx.AsyncClient.stream()`, `aiter_lines()` |
| **Corner Case** | Ollama offline → yields error message |
| **Corner Case** | Stream timeout → yields "⚠ Ollama stream timed out" |

### `POST /api/ai/chat`
| Field | Detail |
|-------|--------|
| **Purpose** | HTTP endpoint for AI chat (non-streaming) |
| **Use Case** | Frontend sends `{message: "explain IS-IS"}` → returns `{response: "...", model: "gpt-oss"}` |
| **Corner Case** | Empty/missing message → 400 error |
| **Corner Case** | Ollama down → 503 with fallback flag |

### `POST /api/ai/stream`
| Field | Detail |
|-------|--------|
| **Purpose** | SSE streaming endpoint for real-time AI responses |
| **Use Case** | Frontend opens EventSource → receives tokens as `data: {"token": "..."}` events |
| **Corner Case** | Queue-based architecture prevents blocking Flask threads |

### `POST /api/ai/analyze`
| Field | Detail |
|-------|--------|
| **Purpose** | AI analysis of arbitrary data |
| **Use Case** | Pass config text + "Is this secure?" → AI returns security analysis |
| **Corner Case** | Empty data → 400 error |

### `GET /api/ai/models`
| Field | Detail |
|-------|--------|
| **Purpose** | List all available Ollama models and active model |
| **Use Case** | Frontend model selector shows available models |
| **Corner Case** | Ollama down → returns empty list with error field |

---

## 2. MCP Bridge (Junos Device Control)

### `mcp_initialize(client)`
| Field | Detail |
|-------|--------|
| **Purpose** | Initialize MCP JSON-RPC session with the Junos MCP server |
| **Use Case** | First API call → handshake → receive session ID |
| **Sub-functions** | `_mcp_post()`, sends `notifications/initialized` |

### `mcp_get_session(client)` / `mcp_clear_session()`
| Field | Detail |
|-------|--------|
| **Purpose** | Session lifecycle — cache session ID, clear on stale errors |
| **Use Case** | Normal: returns cached session. After error: clears → re-initializes |
| **Corner Case** | Stale session → mcp_clear_session() + retry |

### `mcp_execute_command(router, command)`
| Field | Detail |
|-------|--------|
| **Purpose** | Execute a single Junos CLI command on a router |
| **Use Case** | `mcp_execute_command("PE1", "show bgp summary")` → returns CLI output |
| **Sub-functions** | `mcp_get_session()`, `mcp_call_tool("execute_junos_command")` |
| **Corner Case** | Stale session → auto-clears and retries once |
| **Corner Case** | MCP server down → returns "Error: ..." |

### `mcp_execute_batch(command, router_names)`
| Field | Detail |
|-------|--------|
| **Purpose** | Execute same command on multiple routers in parallel |
| **Use Case** | "show isis adjacency" on all 13 routers simultaneously |
| **Sub-functions** | `mcp_call_tool("execute_junos_command_batch")` |

### `mcp_get_config(router)` / `mcp_get_facts(router)`
| Field | Detail |
|-------|--------|
| **Purpose** | Retrieve running config or device facts from a router |
| **Use Case** | Config sync, golden config comparison, device inventory |

### `mcp_load_config(router, config_text, comment)`
| Field | Detail |
|-------|--------|
| **Purpose** | Push and commit configuration to a router |
| **Use Case** | Remediation deployment, template push, rollback |
| **Corner Case** | Commit failure → returns error string |

### `POST /api/mcp/execute`
| Field | Detail |
|-------|--------|
| **Purpose** | HTTP endpoint for single command execution |
| **Use Case** | Frontend MCP terminal sends `{router: "PE1", command: "show version"}` |
| **Corner Case** | Missing router/command → 400 |

### `POST /api/mcp/batch`
| Field | Detail |
|-------|--------|
| **Purpose** | HTTP endpoint for batch command execution |
| **Use Case** | Execute "show system uptime" on all devices at once |

### `GET /api/mcp/facts/<router>` / `GET /api/mcp/live-config/<router>`
| Field | Detail |
|-------|--------|
| **Purpose** | Get device facts or live running config from MCP |

### `POST /api/mcp/deploy-config`
| Field | Detail |
|-------|--------|
| **Purpose** | Deploy configuration to a router via MCP |

---

## 3. Agentic Chat (Brain + RAG + MCP)

### `POST /api/ai/chat-agentic`
| Field | Detail |
|-------|--------|
| **Purpose** | Full agentic AI — classifies query → routes to Brain/RAG/MCP/General |
| **Use Case 1 (Knowledge)** | "What is MPLS?" → RAG retrieval → Ollama with reference knowledge |
| **Use Case 2 (Troubleshoot)** | "Why is BGP down on PE1?" → Brain investigation → MCP probes → AI analysis |
| **Use Case 3 (Status)** | "Show me PE1 status" → Quick brain analysis or MCP check |
| **Use Case 4 (Config)** | "Configure OSPF on PE1" → Generate commands with WARNINGS + requires_approval flag |
| **Use Case 5 (General)** | "Hello" → General AI response with optional RAG boost |
| **Corner Case** | Empty message → 400 |
| **Corner Case** | Brain not available → falls back to general AI |

### `classify_query_web(message)`
| Field | Detail |
|-------|--------|
| **Purpose** | Classify user intent: knowledge / config / troubleshoot / status / general |
| **Use Case** | "why is BGP down?" → `{type: "troubleshoot", confidence: 0.85}` |
| **Corner Case** | Empty string → general |
| **Corner Case** | Unicode text → doesn't crash |
| **Corner Case** | XSS injection → doesn't crash, returns general |

### `GET /api/brain/status`
| Field | Detail |
|-------|--------|
| **Purpose** | Check if Brain, Reasoning, and RAG engines are available |

### `GET /api/brain/scripts` / `POST /api/brain/scripts/select`
| Field | Detail |
|-------|--------|
| **Purpose** | List smart investigation scripts / select scripts for a query |

### `POST /api/brain/classify`
| Field | Detail |
|-------|--------|
| **Purpose** | Classify query using both web classifier and reasoning engine |

### `POST /api/brain/investigate`
| Field | Detail |
|-------|--------|
| **Purpose** | Full 6-layer Brain investigation with WebSocket progress events |
| **Use Case** | "Investigate BGP issues on PE1" → perception → execution → analysis → synthesis |
| **Corner Case** | Brain not available → 503 |

### `POST /api/brain/rag`
| Field | Detail |
|-------|--------|
| **Purpose** | Query RAG knowledge base for Junos reference knowledge |
| **Corner Case** | KB not loaded → 503 |

### `GET /api/brain/history` / `GET /api/brain/history/<id>`
| Field | Detail |
|-------|--------|
| **Purpose** | Investigation history for audit trail and learning |

---

## 4. Topology & Network Analysis

### `build_topology_from_golden_configs()`
| Field | Detail |
|-------|--------|
| **Purpose** | Parse all golden configs to build graph topology (nodes, links, protocols) |
| **Use Case** | Extract IS-IS interfaces, BGP peers, loopbacks, VPN instances from set-format configs |
| **Corner Case** | No golden configs → falls back to devices.json minimal topology |

### `calculate_network_stats(topology)` / `calculate_network_stats_v2()`
| Field | Detail |
|-------|--------|
| **Purpose** | Graph analytics: degree distribution, diameter, SPOFs, redundancy score |
| **Use Case** | Dashboard shows: 13 nodes, 16 links, 2 SPOFs, 85% redundancy |

### `find_shortest_path(source, target)`
| Field | Detail |
|-------|--------|
| **Purpose** | Dijkstra shortest path using IS-IS metrics |
| **Use Case** | PE1→PE3: path=[PE1, P11, P12, PE3], cost=300, hops=3 |
| **Corner Case** | Same source/target → path=[PE1], cost=0 |
| **Corner Case** | Unreachable nodes → error message |

### `GET /api/topology` / `GET /api/topology/stats`
| Field | Detail |
|-------|--------|
| **Purpose** | Topology data for D3.js visualization + computed stats |

### `GET /api/shortest-path?source=X&target=Y`
| Field | Detail |
|-------|--------|
| **Purpose** | Shortest path analysis endpoint |
| **Corner Case** | Missing params → error JSON |

---

## 5. Configuration Management

### `get_config_diff(router)`
| Field | Detail |
|-------|--------|
| **Purpose** | Unified diff between golden config and running config |
| **Use Case** | Detect config drift after maintenance window |
| **Corner Case** | No golden config → attempts MCP fetch → saves as golden |

### `search_configs(pattern, regex)`
| Field | Detail |
|-------|--------|
| **Purpose** | Search across all golden configs for a pattern |
| **Use Case** | Find all routers with "community public" → security audit |

### `GET /api/golden-configs` / `GET /api/golden-configs/<router>`
| Field | Detail |
|-------|--------|
| **Purpose** | List all golden configs or get specific router config |
| **Corner Case** | Missing router → auto-fetches from MCP |

### `GET /api/config-diff/<router>`
| Field | Detail |
|-------|--------|
| **Purpose** | Compare golden vs running config for a router |

### `GET /api/config-search?q=pattern&regex=true`
| Field | Detail |
|-------|--------|
| **Purpose** | Cross-config search |

### `POST /api/templates/render` / `POST /api/templates/deploy`
| Field | Detail |
|-------|--------|
| **Purpose** | Render Jinja2 templates with variables / deploy rendered config |
| **Use Case** | Select ospf_p2p template → fill vars → preview → deploy to PE1 |
| **Corner Case** | Template not found → 404 |
| **Corner Case** | Missing variables → renders with empty values |

### `POST /api/bootstrap/sync` / `POST /api/bootstrap/sync-one/<router>`
| Field | Detail |
|-------|--------|
| **Purpose** | Pull live configs from MCP and save as golden configs (one-click onboarding) |

---

## 6. Device Pools

### `POST /api/pools` / `GET /api/pools` / `PUT /api/pools/<id>` / `DELETE /api/pools/<id>`
| Field | Detail |
|-------|--------|
| **Purpose** | CRUD for logical device groupings (by role, location, function) |
| **Use Case** | Create "Core Routers" pool with [P11, P12, P13, P14] for bulk operations |
| **Corner Case** | Duplicate name → 409 IntegrityError |
| **Corner Case** | No name → 400 |

### `POST /api/pools/ai-recommend`
| Field | Detail |
|-------|--------|
| **Purpose** | AI recommends optimal device groupings based on topology |
| **Use Case** | AI suggests: "PE Pool", "Core Plane 1", "Core Plane 2", "Route Reflectors" |

---

## 7. Ping & Reachability

### `GET /api/ping/<router>`
| Field | Detail |
|-------|--------|
| **Purpose** | Ping single router via MCP "show system uptime" |
| **Use Case** | Quick health check → returns reachable=true, latency_ms=45 |

### `POST /api/ping/sweep`
| Field | Detail |
|-------|--------|
| **Purpose** | Ping all routers simultaneously |
| **Use Case** | Dashboard health indicator: 12/13 devices reachable |

### `POST /api/ping/ai-analyze`
| Field | Detail |
|-------|--------|
| **Purpose** | AI analyzes ping sweep results for patterns |
| **Use Case** | "P11 unreachable" → AI identifies potential ISIS adjacency down, LDP sessions affected |

---

## 8. Data Validation

### `POST /api/validate`
| Field | Detail |
|-------|--------|
| **Purpose** | Run command on router, validate output against pattern |
| **Use Case** | Command: "show bgp summary" Pattern: "Established" Match: contains → PASS/FAIL |
| **Match Types** | contains, regex, exact, not_contains |

### `POST /api/validate/batch`
| Field | Detail |
|-------|--------|
| **Purpose** | Run same validation across multiple routers |

### `POST /api/validate/ai-compliance`
| Field | Detail |
|-------|--------|
| **Purpose** | AI-powered compliance audit (NTP, SNMP, SSH, IS-IS auth, etc.) |
| **Use Case** | Check PE1 against 10-point security checklist → PASS/FAIL per item |

---

## 9. Notification Service

### `POST /api/notifications/channels` / `GET /api/notifications/channels` / `DELETE /api/notifications/channels/<id>`
| Field | Detail |
|-------|--------|
| **Purpose** | CRUD for notification channels (Slack, webhook, Mattermost) |

### `POST /api/notifications/send`
| Field | Detail |
|-------|--------|
| **Purpose** | Send alert via configured channel |
| **Use Case** | BGP down alert → Slack webhook → formatted message |
| **Security** | External webhooks blocked by default (NOC_ALLOW_EXTERNAL_WEBHOOKS=true to enable) |

### `GET /api/notifications/history`
| Field | Detail |
|-------|--------|
| **Purpose** | Audit trail of all sent notifications |

### `POST /api/notifications/ai-summary`
| Field | Detail |
|-------|--------|
| **Purpose** | AI generates concise alert summary from events |

---

## 10. Scheduled Tasks & Cron

### `POST /api/scheduled-tasks` / `GET /api/scheduled-tasks` / `DELETE /api/scheduled-tasks/<id>`
| Field | Detail |
|-------|--------|
| **Purpose** | CRUD for recurring automated commands |
| **Use Case** | "Check BGP every 30 minutes on all PE routers" |

### `POST /api/scheduled-tasks/<id>/toggle` / `POST /api/scheduled-tasks/<id>/run`
| Field | Detail |
|-------|--------|
| **Purpose** | Enable/disable task or trigger immediate execution |

### `POST /api/scheduled-tasks/cron`
| Field | Detail |
|-------|--------|
| **Purpose** | Create task with cron expression scheduling |
| **Use Case** | `*/5 * * * *` → every 5 minutes |
| **Supported** | @hourly, @daily, @weekly, `*/N * * * *`, specific time crons |

### `GET /api/scheduled-tasks/calendar`
| Field | Detail |
|-------|--------|
| **Purpose** | Calendar view of scheduled + completed tasks |

### `scheduler_loop()` (background thread)
| Field | Detail |
|-------|--------|
| **Purpose** | Background thread checks every 10s for due tasks and executes them |

---

## 11. Workflow Engine

### `POST /api/workflows` / `GET /api/workflows` / `DELETE /api/workflows/<name>`
| Field | Detail |
|-------|--------|
| **Purpose** | CRUD for multi-step automation workflows |

### `POST /api/workflows/execute`
| Field | Detail |
|-------|--------|
| **Purpose** | Execute a workflow (sequence of steps) |
| **Step Types** | command, batch, template, deploy, ai_analyze, condition, wait, rest_call, python_snippet, ping_sweep, validate, notify |
| **Use Case** | 1) Check BGP → 2) If down → 3) AI analyze → 4) Notify Slack |
| **Security** | Python snippets run in sandboxed exec with blocked patterns (no import, no os, no subprocess) |

---

## 12. Git Export

### `POST /api/git-export/init` / `POST /api/git-export/export`
| Field | Detail |
|-------|--------|
| **Purpose** | Version-control golden configs in a local git repository |
| **Use Case** | Export all configs → AI generates commit message → git commit |

### `GET /api/git-export/log` / `GET /api/git-export/diff/<commit>`
| Field | Detail |
|-------|--------|
| **Purpose** | View commit history and diffs |

---

## 13. Result Comparison

### `POST /api/results/capture`
| Field | Detail |
|-------|--------|
| **Purpose** | Capture command output as named result for later comparison |
| **Use Case** | Capture "show bgp summary" before and after maintenance window |

### `GET /api/results` / `GET /api/results/<name>` / `DELETE /api/results/<name>`
| Field | Detail |
|-------|--------|
| **Purpose** | CRUD for captured results |

### `POST /api/results/compare`
| Field | Detail |
|-------|--------|
| **Purpose** | Side-by-side diff of two captured results with AI analysis |
| **Use Case** | Compare pre- vs post-maintenance BGP summary → AI explains what changed |

---

## 14. Config Rollback

### `GET /api/rollback/diff/<router>?version=N`
| Field | Detail |
|-------|--------|
| **Purpose** | Show config diff against rollback version |

### `POST /api/rollback/execute`
| Field | Detail |
|-------|--------|
| **Purpose** | Execute rollback with AI risk assessment and confirmation gate |
| **Use Case** | 1) Show diff → 2) AI risk analysis → 3) Confirm → 4) Execute rollback |

---

## 15. Remediation Engine

### `POST /api/remediate/propose`
| Field | Detail |
|-------|--------|
| **Purpose** | AI generates remediation commands for a detected issue |
| **Use Case** | "BGP session to P12 is down" → AI proposes: `set protocols bgp group ibgp neighbor ...` |
| **Output** | Title, commands, rollback commands, risk level, impact assessment |

### `GET /api/remediate/list` / `GET /api/remediate/<id>`
| Field | Detail |
|-------|--------|
| **Purpose** | List and view remediation proposals |

### `POST /api/remediate/<id>/approve` / `POST /api/remediate/<id>/reject`
| Field | Detail |
|-------|--------|
| **Purpose** | Approval gate — human must approve before execution |

### `POST /api/remediate/<id>/execute`
| Field | Detail |
|-------|--------|
| **Purpose** | Execute approved remediation via MCP config push |
| **Corner Case** | Non-approved status → 400 error |

### `POST /api/deploy/safe`
| Field | Detail |
|-------|--------|
| **Purpose** | AI pre-flight safety check before any config deployment |

---

## 16. Predictive Analysis & Ensemble AI

### `POST /api/ai/ensemble`
| Field | Detail |
|-------|--------|
| **Purpose** | Query multiple Ollama models and produce consensus answer |
| **Use Case** | Ask question to 3 models → compare answers → return highest-confidence |

### `POST /api/brain/predict`
| Field | Detail |
|-------|--------|
| **Purpose** | Predictive failure analysis using investigation history + current topology |
| **Use Case** | AI predicts: "P11 is SPOF with high risk of cascading failure in next 24h" |

### `POST /api/ai/confidence-score`
| Field | Detail |
|-------|--------|
| **Purpose** | Score AI response confidence based on source, validation, and response quality |

### `POST /api/ai/copilot-suggest`
| Field | Detail |
|-------|--------|
| **Purpose** | Proactive suggestions based on current view and network state |

### `POST /api/ai/quick-actions`
| Field | Detail |
|-------|--------|
| **Purpose** | Dynamic context-aware quick action buttons |

---

## 17. Discovery & Monitoring

### `GET /api/discovery/interfaces/<router>` / `GET /api/discovery/interfaces/<router>/detail`
| Field | Detail |
|-------|--------|
| **Purpose** | Discover all interfaces with status, IPs, MACs, traffic stats |

### `GET /api/discovery/neighbors/<router>`
| Field | Detail |
|-------|--------|
| **Purpose** | LLDP + ARP neighbor discovery |

### `POST /api/discovery/full-scan`
| Field | Detail |
|-------|--------|
| **Purpose** | Full infrastructure scan across all routers |

### `GET /api/monitor/health-dashboard`
| Field | Detail |
|-------|--------|
| **Purpose** | Real-time health dashboard: uptime + alarms for all routers |

### `GET /api/monitor/protocol-health`
| Field | Detail |
|-------|--------|
| **Purpose** | Check ISIS, BGP, LDP health across the network |

### `POST /api/monitor/ai-incident`
| Field | Detail |
|-------|--------|
| **Purpose** | AI-powered incident detection and response recommendation |

---

## 18. Security & Compliance

### `POST /api/security/audit`
| Field | Detail |
|-------|--------|
| **Purpose** | Run security audit commands on a router |

### `POST /api/security/threat-analysis`
| Field | Detail |
|-------|--------|
| **Purpose** | AI-powered threat analysis of security data |

### `POST /api/security/credential-scan`
| Field | Detail |
|-------|--------|
| **Purpose** | Scan configs for cleartext credentials, weak community strings |

### `POST /api/security/hardening-report`
| Field | Detail |
|-------|--------|
| **Purpose** | CIS benchmark-style security hardening report |

---

## 19. Path Analysis (Advanced)

### `POST /api/path/multi-algorithm`
| Field | Detail |
|-------|--------|
| **Purpose** | Compute paths using Dijkstra + K-shortest (Yen's algorithm) |

### `POST /api/path/what-if`
| Field | Detail |
|-------|--------|
| **Purpose** | Simulate node/link failure and compute impact |
| **Use Case** | "What if P11 fails?" → 3 nodes isolated, VPN-A affected |

### `POST /api/path/capacity-plan`
| Field | Detail |
|-------|--------|
| **Purpose** | AI-powered capacity planning recommendations |

---

## 20. Quantum-Inspired Optimization

### `POST /api/quantum/optimize`
| Field | Detail |
|-------|--------|
| **Purpose** | Quantum annealing: find optimal new links to eliminate SPOFs |

### `GET /api/quantum/anomalies`
| Field | Detail |
|-------|--------|
| **Purpose** | Quantum walk anomaly detection across network graph |

### `GET /api/quantum/communities`
| Field | Detail |
|-------|--------|
| **Purpose** | Louvain community detection for topology clustering |

### `GET /api/quantum/spof`
| Field | Detail |
|-------|--------|
| **Purpose** | Tarjan's O(V+E) articulation point + bridge detection |

### `GET /api/quantum/benchmark`
| Field | Detail |
|-------|--------|
| **Purpose** | Benchmark quantum engine on synthetic graph |

---

## 21. Frontend UI Functions

### Core Navigation
| Function | Purpose |
|----------|---------|
| `switchView(view)` | Navigate between 15+ views with animation transitions |
| `toggleNavDropdown(id)` | Open/close header navigation dropdowns |
| `closeAllDropdowns()` | Close all open dropdown menus |
| `toggleMobileMenu()` | Toggle mobile hamburger menu |
| `setTheme(t)` / `toggleTheme()` | Dark/Light mode toggle with persistence |

### Dashboard
| Function | Purpose |
|----------|---------|
| `renderDashboard()` | Render dashboard with animated stat cards |
| `renderRoleChart(nodes)` | SVG donut chart of device roles |
| `renderProtocolBars(nodes)` | Protocol distribution bar chart |
| `renderDeviceTable(nodes)` | Sortable device inventory table |
| `filterDeviceTable()` | Real-time search filtering |
| `animateValue(el, target)` | Smooth number counter animation |

### Topology (D3.js)
| Function | Purpose |
|----------|---------|
| `renderTopology()` | Full D3.js force-directed graph |
| `renderMiniTopology(topo)` | Mini topology in sidebar |
| `renderPathTopology(path)` | Highlight shortest path on graph |
| `buildLinks(topo)` | Build D3 link objects from topology |
| `changeTopoLayout(layout)` | Switch between force/circular/hierarchical layouts |
| `showNodeDetail(node)` | Slide-in panel with device details |

### AI Chat
| Function | Purpose |
|----------|---------|
| `sendChat()` | Send message via agentic → streaming → non-streaming → fallback chain |
| `startStreamingMessage()` | Create streaming chat bubble with cursor |
| `appendStreamToken(bubble, text)` | Append token to streaming bubble |
| `finalizeStreamMessage(bubble, cursor, text)` | Complete streaming and format markdown |
| `appendChatMessage(role, text, cot, conf)` | Render chat message with CoT and confidence |
| `formatChatText(text)` | Convert markdown to styled HTML |
| `showTypingIndicator()` / `removeTypingIndicator()` | AI thinking animation |
| `buildCotSteps(data)` | Build Chain-of-Thought visualization |
| `generateLocalResponse(msg)` | Offline fallback response generator |

### AI Copilot Sidebar
| Function | Purpose |
|----------|---------|
| `toggleAICopilot()` | Open/close copilot sidebar |
| `sendCopilotMessage()` | Send message in copilot context |
| `generateViewInsights(view)` | AI-generated insights per view |
| `loadCopilotSuggestions(view)` | Load proactive suggestions |
| `aiQuickAction(view, action)` | Execute quick action from copilot |
| `logAuditAction(type, text)` | Log user action to audit trail |
| `renderAuditTrail()` | Display audit history |

### Configuration
| Function | Purpose |
|----------|---------|
| `renderConfigList()` | List golden configs with metadata |
| `loadConfig(router)` | Load and display config with syntax highlighting |
| `searchConfigs()` | Cross-config pattern search |
| `loadTemplates()` / `renderTemplateList()` | Template management |
| `selectTemplate(name)` | Load template into editor |
| `renderTemplate()` / `deployTemplate()` | Preview and deploy |

### Device Pools
| Function | Purpose |
|----------|---------|
| `loadPools()` / `renderPoolsGrid(pools)` | Load and render pool cards |
| `createPool()` / `deletePool(id)` | CRUD operations |
| `aiRecommendPools()` | AI-powered pool recommendations |
| `applyPoolRecommendation(rec)` | Apply AI suggestion |

### Ping & Validation
| Function | Purpose |
|----------|---------|
| `pingSingleRouter()` / `pingSweepAll()` | Reachability checks |
| `renderPingResults(results, ms)` | Visualize ping results |
| `aiAnalyzePing()` | AI analysis of ping results |
| `runValidation()` / `runBatchValidation()` | Command output validation |
| `runAICompliance()` | AI compliance check |

### Notifications
| Function | Purpose |
|----------|---------|
| `loadNotificationChannels()` / `createChannel()` | Channel CRUD |
| `sendTestNotification()` | Test notification delivery |
| `loadNotificationHistory()` | View sent notifications |
| `aiSummarizeAlerts()` | AI alert summary |

### Scheduler & Workflows
| Function | Purpose |
|----------|---------|
| `loadScheduledTasks()` / `createScheduledTask()` | Task management |
| `toggleTask(id)` / `runTaskNow(id)` / `deleteTask(id)` | Task operations |
| `loadWorkflows()` / `newWorkflow()` / `loadWorkflow(name)` | Workflow CRUD |
| `addWorkflowStep()` / `removeWorkflowStep(idx)` | Step management |
| `saveCurrentWorkflow()` / `executeCurrentWorkflow()` | Save and execute |

### Investigation & Remediation
| Function | Purpose |
|----------|---------|
| `renderInvestigationView()` | Investigation dashboard |
| `startInvestigation()` / `loadInvestigation(id)` | Start/load investigation |
| `renderRemediationView()` | Remediation dashboard |
| `proposeRemediation()` | AI remediation proposal |
| `approveRemediation(id)` / `rejectRemediation(id)` / `executeRemediation(id)` | Approval flow |
| `renderPredictiveView()` | Predictive analysis dashboard |
| `runPrediction()` / `runEnsemble()` | AI prediction and ensemble |

### Discovery & Security
| Function | Purpose |
|----------|---------|
| `runDiscoveryScan()` / `discoverInterfaces()` / `discoverNeighbors()` | Device discovery |
| `runSecurityAudit()` / `runThreatCheck()` | Security checks |
| `runHardeningReport()` / `runCredentialScan()` | Security reports |

### Advanced Path Analysis
| Function | Purpose |
|----------|---------|
| `runWhatIf()` | Failure simulation |
| `runMultiPath()` | Multi-algorithm path computation |
| `runCapacityPlan()` | AI capacity planning |

---

## 22. WebSocket Real-Time Events

| Event | Direction | Purpose |
|-------|-----------|---------|
| `connected` | Server→Client | Connection established confirmation |
| `topology_update` | Server→Client | Real-time topology changes |
| `path_result` | Server→Client | Shortest path calculation result |
| `chat_response` | Server→Client | AI chat response via WebSocket |
| `mcp_result` | Server→Client | MCP command execution result |
| `device_status` | Server→Client | Live device status update |
| `task_result` | Server→Client | Scheduled task execution result |
| `workflow_progress` | Server→Client | Workflow step completion progress |
| `brain_progress` | Server→Client | Brain investigation layer changes |
| `brain_log` | Server→Client | Brain investigation log messages |
| `ai_thinking` | Server→Client | AI processing stage indicator |

---

## 23. Utility & Infrastructure

### `parse_sse_response(text)`
| Field | Detail |
|-------|--------|
| **Purpose** | Parse SSE event stream and extract final JSON-RPC result |
| **Corner Case** | Empty text → {} |
| **Corner Case** | Malformed JSON → skips, returns last valid |

### `run_async(coro)`
| Field | Detail |
|-------|--------|
| **Purpose** | Run async coroutine from sync Flask context |
| **Corner Case** | Exception in coroutine → propagated to caller |

### `escapeHtml(str)` (frontend)
| Field | Detail |
|-------|--------|
| **Purpose** | XSS prevention — escapes &, <, >, ", ' |
| **Corner Case** | null/undefined → empty string |
| **Corner Case** | Number → stringified |

### `calculate_next_run(schedule)` / `parse_cron_expression(cron)`
| Field | Detail |
|-------|--------|
| **Purpose** | Parse schedule strings (5m, 1h, 30s) and cron expressions |

### `_no_cache(response)` (after_request middleware)
| Field | Detail |
|-------|--------|
| **Purpose** | Add no-cache headers to ALL /api/ responses |
| **Scope** | Only /api/ paths — static files unaffected |

### `_check_api_key()` (before_request middleware)
| Field | Detail |
|-------|--------|
| **Purpose** | Optional API key authentication (set NOC_API_KEY env var) |

---

*Total documented: 75+ API endpoints, 140+ frontend functions, 20+ AI-powered features, 11 WebSocket events*
