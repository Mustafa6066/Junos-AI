<p align="center">
  <img src="https://img.shields.io/badge/Junos_AI-Network_Operations_Center-00C853?style=for-the-badge&logo=juniper&logoColor=white" alt="Junos AI NOC"/>
</p>

<h1 align="center">Junos AI — Intelligent Network Agency</h1>

<p align="center">
  <strong>AI-powered Network Operations Center for Juniper Junos infrastructure</strong><br/>
  <em>MCP Bridge · Ollama AI · Quantum Optimization · Liquid Glass UI</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.12+"/>
  <img src="https://img.shields.io/badge/flask-3.0+-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask"/>
  <img src="https://img.shields.io/badge/ollama-local_AI-FF6F00?style=flat-square" alt="Ollama"/>
  <img src="https://img.shields.io/badge/MCP-protocol-8E24AA?style=flat-square" alt="MCP"/>
  <img src="https://img.shields.io/badge/D3.js-v7-F9A825?style=flat-square&logo=d3dotjs&logoColor=white" alt="D3.js"/>
  <img src="https://img.shields.io/badge/tests-403_passing-00C853?style=flat-square" alt="Tests"/>
  <img src="https://img.shields.io/badge/license-Apache_2.0-blue?style=flat-square" alt="License"/>
</p>

---

## Overview

**Junos AI** is a full-stack, AI-agentic Network Operations Center (NOC) that connects to live Juniper Junos devices through the [Model Context Protocol (MCP)](https://github.com/Juniper/junos-mcp-server). It combines a local AI engine (Ollama), quantum-inspired graph optimization, and a production-grade web dashboard into a single platform for network engineers.

> **Zero cloud dependency.** Everything runs locally — your data, your AI, your network.

```
┌─────────────────────────────────────────────────────────────┐
│                    Junos AI NOC (Flask)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │
│  │ AI Chat  │  │ Topology │  │ Configs  │  │ Workflows  │  │
│  │ (Agentic)│  │ (D3.js)  │  │ (Diff)   │  │ (Engine)   │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └─────┬──────┘  │
│       │              │              │               │        │
│  ┌────▼──────────────▼──────────────▼───────────────▼────┐  │
│  │              Quantum Optimization Engine               │  │
│  │  Tarjan O(V+E) · Annealing · Louvain · Quantum Walk   │  │
│  └───────────────────────┬───────────────────────────────┘  │
└──────────────────────────┼──────────────────────────────────┘
                           │
              ┌────────────▼────────────┐
              │   Junos MCP Server      │
              │   (NETCONF/SSH)         │
              └────────────┬────────────┘
                           │
           ┌───────────────▼────────────────┐
           │  Juniper Routers (PE/P/RR)     │
           │  IS-IS · MPLS · BGP · LDP     │
           └────────────────────────────────┘
```

---

## Features

### 🧠 AI Engine
| Feature | Description |
|---------|-------------|
| **Agentic Chat** | Natural-language interface with MCP tool-calling — "show me BGP neighbors on PE1" triggers live device queries |
| **Streaming Responses** | Token-by-token AI output via WebSocket for real-time feedback |
| **RAG Knowledge Base** | Ingests Junos training PDFs (JNCIA, AJSPR, JMF, JIR, JL2V, JSPX) into vector store for retrieval-augmented generation |
| **Model Auto-Detection** | On startup, detects available Ollama models and auto-selects fallback if configured model is missing |
| **AI Copilot Sidebar** | Context-aware assistant available on every view — knows which page you're on |

### 🌐 Network Visualization
| Feature | Description |
|---------|-------------|
| **D3.js Topology** | Interactive force-directed graph with PE/P/RR node roles, IS-IS links, iBGP sessions |
| **Clustered View** | Auto-clusters large topologies (2000+ nodes) for readability |
| **Live Status Overlay** | Polls MCP to show real-time interface/protocol status |
| **Shortest Path Finder** | Dijkstra's algorithm using IS-IS metrics from golden configs |

### ⚡ Quantum-Inspired Optimization
| Algorithm | Complexity | Purpose |
|-----------|-----------|---------|
| **Tarjan's SPOF Detection** | O(V+E) | Articulation points + bridge links (1000× faster than brute-force) |
| **Simulated Quantum Annealing** | Heuristic | Optimal link placement to eliminate single points of failure |
| **Quantum Walk Anomaly Detection** | O(√N) | Graph-based anomaly scoring for nodes and links |
| **Louvain Community Detection** | O(N log N) | Cluster topology into logical communities |
| **Double-BFS Diameter** | O(V+E) | Fast graph diameter approximation |

### 🔧 Configuration Management
| Feature | Description |
|---------|-------------|
| **Golden Config Store** | Baseline configs per router — auto-synced from MCP |
| **Diff Engine** | Unified diff between golden and live configs with additions/deletions count |
| **Config Search** | Regex search across all golden configs |
| **Template Engine** | Jinja2 templates for BGP, OSPF, MPLS LDP, system hardening |
| **One-Click Deploy** | Render template → preview → deploy to router via MCP |
| **Git Export** | Export configs to a git-friendly directory structure |

### 🔄 Automation
| Feature | Description |
|---------|-------------|
| **Workflow Builder** | Chain MCP operations: command → batch → template → deploy → AI analyze → condition → wait |
| **Scheduled Tasks** | CRON-style scheduler with interval support (5m, 1h, 24h) and task history |
| **Device Pools** | Group routers for batch operations — "run X on all PE routers" |
| **Batch Execution** | Parallel command execution across multiple routers |

### 🛡️ Operations
| Feature | Description |
|---------|-------------|
| **Investigation** | AI-powered root cause analysis for network issues |
| **Remediation** | Automated fix suggestions with one-click deployment |
| **Predictive Analysis** | Ensemble AI models for capacity planning and failure prediction |
| **Security & Compliance** | Audit configs against hardening templates |
| **Log Forensics** | Browse, filter, and AI-analyze bridge logs |
| **Notification System** | In-app alerts for scheduler results, workflow completions |

### 🎨 User Interface
| Feature | Description |
|---------|-------------|
| **Apple Liquid Glass** | Frosted-glass aesthetic with backdrop-filter blur, glass orbs, animated gradients |
| **AI Agency Design** | Pill-group navigation, live status badges, neural engine branding |
| **Dark / Light Mode** | Full theme toggle with CSS custom properties |
| **Responsive Layout** | Adapts from desktop to tablet with collapsible nav groups |
| **WebSocket Real-Time** | Live updates for task results, workflow progress, device polling |

---

## Quick Start

### Prerequisites

| Requirement | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.12+ | Backend server |
| **Ollama** | Latest | Local AI inference |
| **Junos MCP Server** | Latest | Device connectivity via NETCONF |
| **Node.js** | 18+ | Frontend test runner (optional) |

### 1. Clone

```bash
git clone https://github.com/Mustafa6066/Junos-AI.git
cd Junos-AI
```

### 2. Install Dependencies

```bash
# Backend
cd web_ui
pip install -r requirements.txt

# Frontend tests (optional)
npm install
```

### 3. Configure

Edit `config.yaml` in the project root:

```yaml
mcp:
  url: "http://127.0.0.1:30030/mcp/"
  call_timeout: 120.0

ai:
  model: "gpt-oss"                    # Your Ollama model name
  ollama_url: "http://127.0.0.1:11434"
  context_window: 32768
  temperature: 0.12
```

### 4. Configure Devices

Copy the template and add your Juniper routers:

```bash
cd junos-mcp-server
cp devices-template.json devices.json
```

```json
{
  "PE1": { "ip": "10.0.0.1", "port": "830" },
  "PE2": { "ip": "10.0.0.2", "port": "830" },
  "P11": { "ip": "10.0.0.11", "port": "830" }
}
```

### 5. Start Services

```bash
# Terminal 1 — Start MCP Server
cd junos-mcp-server
python jmcp.py --transport streamable-http --port 30030

# Terminal 2 — Start Ollama (if not running)
ollama serve

# Terminal 3 — Start NOC Web UI
cd web_ui
python app.py
```

### 6. Open

```
http://localhost:5555
```

On first launch, click **"Sync from MCP"** on the Dashboard to pull golden configs from all connected devices.

---

## Project Structure

```
Junos-AI/
├── config.yaml                 # All tunable settings
├── junos-mcp-server/           # MCP server (Juniper/junos-mcp-server)
│   ├── jmcp.py                 # MCP server entry point
│   ├── devices.json            # Router inventory (git-ignored)
│   └── devices-template.json   # Template for device config
├── web_ui/
│   ├── app.py                  # Flask backend (4,981 lines — 75+ API endpoints)
│   ├── quantum_engine.py       # Quantum-inspired graph algorithms (906 lines)
│   ├── requirements.txt        # Python dependencies
│   ├── templates/
│   │   └── index.html          # Single-page app (1,410 lines)
│   ├── static/
│   │   ├── css/
│   │   │   ├── glass.css       # Apple Liquid Glass design system
│   │   │   ├── noc.css         # NOC-specific component styles
│   │   │   └── fonts.css       # Inter + JetBrains Mono
│   │   ├── js/
│   │   │   ├── noc.js          # Frontend logic (4,473 lines — 140+ functions)
│   │   │   ├── d3.v7.min.js    # D3.js for topology visualization
│   │   │   ├── socket.io.min.js
│   │   │   └── lucide.min.js   # Icon library
│   │   └── fonts/
│   └── tests/
│       ├── test_app.py         # Backend tests (182 tests)
│       └── test_noc.js         # Frontend tests (221 tests)
├── golden_configs/             # Baseline router configurations
│   ├── PE1.conf ... PE3.conf
│   └── P11.conf ... P24.conf
├── templates/                  # Jinja2 deployment templates
│   ├── bgp_ibgp.j2
│   ├── mpls_ldp.j2
│   ├── ospf_p2p.j2
│   └── system_hardening.j2
├── files/                      # Junos training PDFs (RAG knowledge base)
├── modules/                    # CLI bridge modules
│   ├── intelligence.py         # AI reasoning engine
│   ├── topology.py             # Topology builder
│   ├── parsers.py              # Junos output parsers
│   └── ...
├── kb_vectorstore.py           # Vector store for RAG
├── ingest_pdfs.py              # PDF → vector ingestion pipeline
└── logs/                       # Bridge operation logs
```

---

## API Reference

The backend exposes **75+ REST endpoints** under `/api/`. Key groups:

| Group | Endpoints | Description |
|-------|-----------|-------------|
| **Bootstrap** | `/api/bootstrap/status`, `/api/bootstrap/sync` | First-run config sync |
| **Topology** | `/api/topology`, `/api/topology/stats` | Graph data + network statistics |
| **Devices** | `/api/devices`, `/api/mcp/facts/<router>` | Inventory + live device facts |
| **Configs** | `/api/golden-configs`, `/api/config-diff/<router>` | Golden configs + diff engine |
| **MCP Execute** | `/api/mcp/execute`, `/api/mcp/batch` | Run Junos commands |
| **AI Chat** | `/api/ai/chat` | Ollama-powered agentic chat |
| **Templates** | `/api/templates/render`, `/api/templates/deploy` | Jinja2 render + deploy |
| **Scheduler** | `/api/scheduled-tasks` | CRUD + run-now + history |
| **Workflows** | `/api/workflows`, `/api/workflows/execute` | Build + execute workflows |
| **Quantum** | `/api/quantum/optimize`, `/api/quantum/anomalies`, `/api/quantum/spof` | Graph optimization |
| **Paths** | `/api/shortest-path` | Dijkstra with IS-IS metrics |
| **Logs** | `/api/logs`, `/api/logs/<filename>` | Log file browser |
| **Security** | `/api/security/audit` | Compliance checking |

> Full use case documentation: [`web_ui/USE_CASES.md`](web_ui/USE_CASES.md) (860 lines covering every function)

---

## Testing

```bash
# Run all tests (403 total)
cd web_ui

# Backend — 182 tests
python -m pytest tests/test_app.py -v

# Frontend — 221 tests
npx jest tests/test_noc.js --verbose

# Both via npm
npm test
```

**Test coverage includes:**
- All 75+ API endpoints (status codes, JSON schemas, error handling)
- MCP bridge integration (mock-based)
- AI chat pipeline (mock Ollama)
- Quantum engine algorithms
- Frontend function existence + DOM interaction
- WebSocket event handling
- Edge cases (empty inputs, missing devices, timeouts)

---

## Security

| Control | Implementation |
|---------|---------------|
| **API Key Auth** | Optional — set `NOC_API_KEY` env var to require `X-API-Key` header on all `/api/` requests |
| **CORS Lockdown** | Restricted to `localhost` origins only |
| **Secret Key** | Auto-generated per-instance, stored in `.secret_key` (git-ignored) |
| **No Caching** | All API responses include `Cache-Control: no-store` headers |
| **Credentials** | `devices.json` is git-ignored — never committed |
| **Local AI** | Ollama runs 100% locally — no data leaves your machine |

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NOC_PORT` | `5555` | Web UI listen port |
| `NOC_HOST` | `127.0.0.1` | Bind address |
| `NOC_API_KEY` | *(empty)* | Set to enable API key authentication |
| `FLASK_DEBUG` | *(unset)* | Set to enable debug mode |

---

## Built With

| Technology | Role |
|-----------|------|
| [Flask](https://flask.palletsprojects.com/) + [SocketIO](https://flask-socketio.readthedocs.io/) | Backend server + WebSocket |
| [Ollama](https://ollama.ai/) | Local LLM inference (GPT-OSS, Llama, etc.) |
| [Junos MCP Server](https://github.com/Juniper/junos-mcp-server) | NETCONF bridge to Juniper devices |
| [D3.js v7](https://d3js.org/) | Force-directed topology visualization |
| [Jinja2](https://jinja.palletsprojects.com/) | Configuration template engine |
| [Lucide Icons](https://lucide.dev/) | UI icon set |
| [Inter](https://rsms.me/inter/) + [JetBrains Mono](https://www.jetbrains.com/lp/mono/) | Typography |

---

## Documentation

| Document | Description |
|----------|-------------|
| [`PRODUCTION_DEPLOYMENT_GUIDE.md`](PRODUCTION_DEPLOYMENT_GUIDE.md) | **Production readiness** — Gunicorn, PostgreSQL, Celery, Nginx, Docker, RBAC, AI validation |
| [`config.yaml`](config.yaml) | All tunable settings with inline comments |
| [`web_ui/USE_CASES.md`](web_ui/USE_CASES.md) | Complete function-by-function use case catalog |
| [`FULL_PROJECT_DOCUMENTATION.md`](FULL_PROJECT_DOCUMENTATION.md) | Architecture deep dive |
| [`AI_PLAYBOOK.md`](AI_PLAYBOOK.md) | AI reasoning patterns and prompt engineering |
| [`KNOWLEDGE_BASE.md`](KNOWLEDGE_BASE.md) | Junos protocol reference |
| [`JUNOS_DEEP_KNOWLEDGE.md`](JUNOS_DEEP_KNOWLEDGE.md) | Advanced Junos troubleshooting |
| [`EXPERT_EXAMPLES.md`](EXPERT_EXAMPLES.md) | Real-world expert examples for RAG |
| [`junos-mcp-server/README.md`](junos-mcp-server/README.md) | MCP server setup and usage |

---

## Production Deployment

For enterprise-grade deployment with PostgreSQL, Celery workers, Nginx SSL termination, and Docker Compose — see the **[Production Deployment Guide](PRODUCTION_DEPLOYMENT_GUIDE.md)**.

```bash
cd deploy
cp .env.example .env   # Fill in secrets
docker compose up -d   # Start full stack
```

Key components:
- **Gunicorn + Eventlet** — replaces Flask dev server (multi-worker, WebSocket-safe)
- **PostgreSQL** — replaces 5 SQLite databases (concurrent-safe)
- **Celery + Redis** — replaces daemon thread scheduler (durable, restartable)
- **Nginx** — TLS, static files, rate limiting, SSE/WebSocket proxy rules
- **OAuth2-Proxy** — optional SSO integration (Keycloak, Azure AD, Okta)

---

## License

This project is licensed under the Apache License 2.0 — see the [LICENSE](junos-mcp-server/LICENSE) file for details.

---

<p align="center">
  <strong>Junos AI</strong> — Built for network engineers who demand intelligence at the edge.<br/>
  <sub>Powered by Ollama · MCP Protocol · Quantum-Inspired Algorithms</sub>
</p>
