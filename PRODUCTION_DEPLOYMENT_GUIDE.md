# Junos AI NOC — Production Deployment Guide
## Enterprise-Grade Architecture for Multi-User, Real-Time Operations

> **Version**: 24.0 | **Date**: 2026-02-27
> **Audience**: Platform engineers, DevOps, network operations leads

---

## Table of Contents

1. [Architecture Overview — Lab vs Production](#1-architecture-overview)
2. [Infrastructure & Deployment](#2-infrastructure--deployment)
   - [2.1 WSGI Server (Gunicorn + Eventlet)](#21-wsgi-server)
   - [2.2 Database Migration (SQLite → PostgreSQL)](#22-database-migration)
   - [2.3 Task Queue (Celery + Redis)](#23-task-queue)
   - [2.4 Reverse Proxy (Nginx + SSL)](#24-reverse-proxy)
   - [2.5 Docker Compose (Full Stack)](#25-docker-compose)
3. [Security Hardening](#3-security-hardening)
   - [3.1 OAuth2 / OIDC Authentication](#31-oauth2--oidc)
   - [3.2 Role-Based Access Control (RBAC)](#32-rbac)
   - [3.3 Secrets Management](#33-secrets-management)
4. [AI Engine Validation](#4-ai-engine-validation)
   - [4.1 Model Verification](#41-model-verification)
   - [4.2 RAG Pipeline Validation](#42-rag-pipeline-validation)
   - [4.3 Hypered Brain Pipeline](#43-hypered-brain-pipeline)
5. [Real-Time Operations](#5-real-time-operations)
   - [5.1 WebSocket & SSE Health](#51-websocket--sse-health)
   - [5.2 NETCONF Keepalives](#52-netconf-keepalives)
   - [5.3 Circuit Breaker Monitoring](#53-circuit-breaker-monitoring)
   - [5.4 Live Dashboard Verification](#54-live-dashboard-verification)
6. [Health Check Endpoints](#6-health-check-endpoints)
7. [Monitoring & Observability](#7-monitoring--observability)
8. [Runbook — First Production Deployment](#8-runbook)

---

## 1. Architecture Overview

### Current Lab Architecture (What We Have)

```
┌──────────────────────────────────────────────┐
│  Single Process: python app.py               │
│  ├─ Flask Dev Server (Werkzeug)              │
│  ├─ ThreadPoolExecutor(4) for MCP/AI calls   │
│  ├─ Daemon Thread: scheduler_loop()          │
│  ├─ SQLite × 5 (audit, analysis, pools,      │
│  │     scheduled, notifications)             │
│  ├─ Local file: .secret_key                  │
│  └─ Local file: devices.json (credentials)   │
│                                              │
│  Clients: 1–3 concurrent (lab engineers)     │
│  Auth: Optional X-API-Key header             │
│  CORS: localhost only                        │
│  SSL: None                                   │
└──────────────────────────────────────────────┘
```

### Target Production Architecture

```
                    ┌─────────────┐
                    │   Traefik   │ ← TLS termination, rate limiting
                    │   / Nginx   │
                    └──────┬──────┘
                           │ :443
              ┌────────────┼────────────┐
              │            │            │
        ┌─────▼────┐ ┌────▼─────┐ ┌────▼─────┐
        │ Gunicorn │ │ Gunicorn │ │ Gunicorn │  ← 3+ Eventlet workers
        │ Worker 1 │ │ Worker 2 │ │ Worker 3 │
        └─────┬────┘ └────┬─────┘ └────┬─────┘
              │            │            │
        ┌─────▼────────────▼────────────▼─────┐
        │         Redis (pub/sub + cache)      │
        │    SocketIO message bus across       │
        │    workers for WebSocket broadcast   │
        └─────┬───────────────────┬────────────┘
              │                   │
     ┌────────▼──────┐   ┌───────▼────────┐
     │  PostgreSQL   │   │ Celery Workers  │ ← Scheduled tasks, batch MCP,
     │  (all state)  │   │   × 4          │   AI analysis, heavy compute
     └───────────────┘   └───────┬────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   Junos MCP Server      │
                    │   (NETCONF/SSH pool)    │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  Juniper Network Fabric │
                    └─────────────────────────┘
```

---

## 2. Infrastructure & Deployment

### 2.1 WSGI Server

**Problem:** `socketio.run()` uses Werkzeug — single-threaded, no connection pooling, crashes under load.

**Solution:** Gunicorn with Eventlet workers + Redis message queue for SocketIO.

**`gunicorn.conf.py`** (included in `deploy/`):

```python
# Production Gunicorn config for Junos AI NOC
import os

bind = f"0.0.0.0:{os.environ.get('NOC_PORT', '5555')}"
workers = int(os.environ.get("NOC_WORKERS", 3))
worker_class = "eventlet"
timeout = 300                # MCP calls can take up to 120s
graceful_timeout = 30
keepalive = 5
max_requests = 1000          # Recycle workers to prevent memory leaks
max_requests_jitter = 50
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Preload app for faster worker startup (shared code, separate state)
preload_app = True
```

**Run command:**
```bash
gunicorn --config deploy/gunicorn.conf.py "app:app"
```

Or with SocketIO (required for WebSocket support):
```bash
gunicorn --config deploy/gunicorn.conf.py \
  --worker-class eventlet \
  "app:app"
```

> **Critical:** When running multiple Gunicorn workers, SocketIO must use Redis as a message queue so WebSocket events broadcast across all workers. See `deploy/docker-compose.yml`.

---

### 2.2 Database Migration

**Problem:** 5 SQLite databases lock on concurrent writes — incompatible with multi-worker deployment.

| Current SQLite DB | Purpose | Tables |
|-------------------|---------|--------|
| `audit_history.db` | Audit run history | `audit_runs`, `audit_findings` |
| `analysis_memory.db` | AI investigation memory | `investigations`, `findings` |
| `scheduled_tasks.db` | CRON scheduler | `scheduled_tasks`, `task_history` |
| `device_pools.db` | Device group management | `pools`, `pool_members` |
| `notifications.db` | In-app alerts | `notifications` |

**Solution:** Single PostgreSQL instance with schemas.

**Migration SQL** (included in `deploy/migrations/001_init.sql`):

```sql
-- All 5 SQLite databases → single PostgreSQL with schemas
CREATE SCHEMA IF NOT EXISTS noc;

-- Scheduled Tasks (from scheduled_tasks.db)
CREATE TABLE noc.scheduled_tasks (
    id            SERIAL PRIMARY KEY,
    name          TEXT NOT NULL,
    task_type     TEXT NOT NULL,
    schedule      TEXT NOT NULL,
    target_routers JSONB NOT NULL,
    command       TEXT NOT NULL,
    enabled       BOOLEAN DEFAULT TRUE,
    last_run      TIMESTAMPTZ,
    last_result   TEXT,
    next_run      TIMESTAMPTZ,
    created_at    TIMESTAMPTZ DEFAULT NOW(),
    run_count     INTEGER DEFAULT 0
);

CREATE TABLE noc.task_history (
    id          SERIAL PRIMARY KEY,
    task_id     INTEGER REFERENCES noc.scheduled_tasks(id) ON DELETE CASCADE,
    run_at      TIMESTAMPTZ DEFAULT NOW(),
    result      TEXT,
    status      TEXT,
    duration_ms INTEGER
);

-- Device Pools (from device_pools.db)
CREATE TABLE noc.device_pools (
    id          SERIAL PRIMARY KEY,
    name        TEXT UNIQUE NOT NULL,
    description TEXT,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE noc.pool_members (
    id       SERIAL PRIMARY KEY,
    pool_id  INTEGER REFERENCES noc.device_pools(id) ON DELETE CASCADE,
    router   TEXT NOT NULL,
    UNIQUE(pool_id, router)
);

-- Notifications (from notifications.db)
CREATE TABLE noc.notifications (
    id         SERIAL PRIMARY KEY,
    type       TEXT NOT NULL,
    title      TEXT NOT NULL,
    message    TEXT,
    severity   TEXT DEFAULT 'info',
    read       BOOLEAN DEFAULT FALSE,
    data       JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Audit History (from audit_history.db)
CREATE TABLE noc.audit_runs (
    id           SERIAL PRIMARY KEY,
    start_time   TIMESTAMPTZ,
    end_time     TIMESTAMPTZ,
    routers      JSONB,
    total_checks INTEGER,
    passed       INTEGER,
    failed       INTEGER,
    warnings     INTEGER,
    status       TEXT,
    report_path  TEXT
);

-- Analysis Memory (from analysis_memory.db)
CREATE TABLE noc.investigations (
    id          SERIAL PRIMARY KEY,
    query       TEXT NOT NULL,
    result      TEXT,
    confidence  REAL,
    model       TEXT,
    routers     JSONB,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_notifications_created ON noc.notifications(created_at DESC);
CREATE INDEX idx_task_history_task ON noc.task_history(task_id, run_at DESC);
CREATE INDEX idx_investigations_created ON noc.investigations(created_at DESC);
```

**Environment variable to switch:**
```bash
# SQLite mode (default, backward-compatible)
export NOC_DB_MODE=sqlite

# PostgreSQL mode
export NOC_DB_MODE=postgres
export DATABASE_URL=postgresql://noc_user:secure_password@localhost:5432/junos_noc
```

---

### 2.3 Task Queue

**Problem:** `scheduler_loop()` runs in a daemon thread. If the process crashes, scheduled tasks stop. Under multiple Gunicorn workers, each worker spins up its own scheduler thread (duplicate execution).

**Solution:** Celery with Redis broker.

**`deploy/celery_worker.py`** (example structure):

```python
from celery import Celery
from celery.schedules import crontab
import os

redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery("junos_noc", broker=redis_url, backend=redis_url)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    task_acks_late=True,           # Re-queue if worker dies mid-task
    worker_prefetch_multiplier=1,  # One task at a time per worker (MCP is I/O bound)
    task_soft_time_limit=300,      # 5 min soft limit
    task_time_limit=600,           # 10 min hard kill
)

@celery_app.task(bind=True, max_retries=2, default_retry_delay=10)
def execute_mcp_command(self, router_name, command):
    """Execute a single MCP command as a Celery task."""
    # Import here to avoid circular imports
    from app import run_async, mcp_execute_command
    try:
        return run_async(mcp_execute_command(router_name, command))
    except Exception as exc:
        raise self.retry(exc=exc)

@celery_app.task(bind=True, max_retries=1)
def execute_mcp_batch(self, command, router_names):
    """Execute batch MCP command as a Celery task."""
    from app import run_async, mcp_execute_batch
    try:
        return run_async(mcp_execute_batch(command, router_names))
    except Exception as exc:
        raise self.retry(exc=exc)

@celery_app.task
def run_scheduled_task(task_id):
    """Execute a scheduled task from the database."""
    from app import run_async, mcp_execute_command, mcp_execute_batch
    import json, sqlite3, time
    from datetime import datetime
    # ... task execution logic (same as scheduler_loop but durable)
```

**Run workers:**
```bash
celery -A deploy.celery_worker worker --loglevel=info --concurrency=4
celery -A deploy.celery_worker beat --loglevel=info  # For periodic tasks
```

---

### 2.4 Reverse Proxy

**Problem:** No HTTPS, no rate limiting, no request size limits.

**`deploy/nginx.conf`** (included):

```nginx
upstream noc_backend {
    # Gunicorn workers
    server 127.0.0.1:5555;
}

server {
    listen 443 ssl http2;
    server_name noc.example.com;

    ssl_certificate     /etc/ssl/certs/noc.crt;
    ssl_certificate_key /etc/ssl/private/noc.key;
    ssl_protocols       TLSv1.2 TLSv1.3;

    # ── Security Headers ──
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;

    # ── Rate Limiting ──
    limit_req_zone $binary_remote_addr zone=api:10m rate=30r/s;
    limit_req_zone $binary_remote_addr zone=ai:10m rate=5r/s;

    # ── Static Assets (bypass Flask) ──
    location /static/ {
        alias /opt/junos-noc/web_ui/static/;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }

    # ── AI Streaming (SSE) — CRITICAL: disable buffering ──
    location /api/ai/stream {
        proxy_pass http://noc_backend;
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 600s;
        chunked_transfer_encoding off;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;

        limit_req zone=ai burst=3 nodelay;
    }

    # ── WebSocket (Socket.IO) — CRITICAL: protocol upgrade ──
    location /socket.io/ {
        proxy_pass http://noc_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 86400s;  # 24h for persistent WS connections
        proxy_send_timeout 86400s;
    }

    # ── All Other API Requests ──
    location /api/ {
        proxy_pass http://noc_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;

        limit_req zone=api burst=50 nodelay;
        client_max_body_size 10M;
    }

    # ── Frontend SPA ──
    location / {
        proxy_pass http://noc_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# ── HTTP → HTTPS redirect ──
server {
    listen 80;
    server_name noc.example.com;
    return 301 https://$host$request_uri;
}
```

---

### 2.5 Docker Compose

**`deploy/docker-compose.yml`** (full production stack):

```yaml
version: "3.9"

services:
  # ── PostgreSQL ──
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: junos_noc
      POSTGRES_USER: noc_user
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-changeme}
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./migrations/001_init.sql:/docker-entrypoint-initdb.d/001_init.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U noc_user -d junos_noc"]
      interval: 10s
      retries: 5

  # ── Redis (SocketIO message bus + Celery broker) ──
  redis:
    image: redis:7-alpine
    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      retries: 5

  # ── Junos AI NOC Web UI ──
  noc-web:
    build:
      context: ../
      dockerfile: deploy/Dockerfile
    environment:
      NOC_PORT: "5555"
      NOC_HOST: "0.0.0.0"
      NOC_DB_MODE: postgres
      DATABASE_URL: postgresql://noc_user:${POSTGRES_PASSWORD:-changeme}@postgres:5432/junos_noc
      REDIS_URL: redis://redis:6379/0
      NOC_API_KEY: ${NOC_API_KEY:-}
      FLASK_SECRET_KEY: ${FLASK_SECRET_KEY:-}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    ports:
      - "5555:5555"
    volumes:
      - ../golden_configs:/app/golden_configs
      - ../templates:/app/templates
      - ../logs:/app/logs
      - ../config.yaml:/app/config.yaml:ro

  # ── Celery Worker (background tasks) ──
  celery-worker:
    build:
      context: ../
      dockerfile: deploy/Dockerfile
    command: celery -A deploy.celery_worker worker --loglevel=info --concurrency=4
    environment:
      DATABASE_URL: postgresql://noc_user:${POSTGRES_PASSWORD:-changeme}@postgres:5432/junos_noc
      REDIS_URL: redis://redis:6379/0
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ../golden_configs:/app/golden_configs
      - ../config.yaml:/app/config.yaml:ro

  # ── Celery Beat (periodic task scheduler) ──
  celery-beat:
    build:
      context: ../
      dockerfile: deploy/Dockerfile
    command: celery -A deploy.celery_worker beat --loglevel=info
    environment:
      DATABASE_URL: postgresql://noc_user:${POSTGRES_PASSWORD:-changeme}@postgres:5432/junos_noc
      REDIS_URL: redis://redis:6379/0
    depends_on:
      redis:
        condition: service_healthy

  # ── Nginx Reverse Proxy ──
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - ./certs:/etc/ssl:ro
      - ../web_ui/static:/opt/junos-noc/web_ui/static:ro
    depends_on:
      - noc-web

  # ── Ollama (Local AI) ──
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_models:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]

volumes:
  pgdata:
  ollama_models:
```

---

## 3. Security Hardening

### 3.1 OAuth2 / OIDC

The current `X-API-Key` header is a shared secret — anyone with the key has full access. For production with a web UI managing core network infrastructure, implement proper identity.

**Recommended approach:**

| Provider | Best For |
|----------|----------|
| **Keycloak** (self-hosted) | Air-gapped / on-prem NOC environments |
| **Azure AD** | Microsoft-shop enterprises |
| **Okta** | Cloud-first organizations |

**Integration pattern:**

```
Browser → Nginx → OAuth2 Proxy → Flask App
                      ↓
                  Keycloak / Azure AD
```

Use [OAuth2-Proxy](https://oauth2-proxy.github.io/) as a sidecar in front of the app. This requires zero code changes to `app.py` — Nginx routes all requests through the proxy first.

### 3.2 RBAC

Add role-based authorization at the Flask middleware layer:

| Role | Permissions |
|------|-------------|
| `viewer` | Read topology, view configs, browse logs |
| `operator` | Execute commands, run investigations, manage pools |
| `engineer` | Deploy configs, create workflows, manage templates |
| `admin` | Manage scheduled tasks, access security audit, RBAC admin |

The OAuth2 token's claims (`groups` or `roles`) map to these levels. Add a decorator:

```python
def require_role(min_role):
    """RBAC decorator — checks JWT role claim."""
    role_hierarchy = {"viewer": 0, "operator": 1, "engineer": 2, "admin": 3}
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_role = request.headers.get("X-User-Role", "viewer")
            if role_hierarchy.get(user_role, 0) < role_hierarchy[min_role]:
                return jsonify({"error": "Insufficient permissions"}), 403
            return f(*args, **kwargs)
        return wrapped
    return decorator

# Usage:
@app.route("/api/mcp/deploy-config", methods=["POST"])
@require_role("engineer")
def api_mcp_deploy_config():
    ...
```

### 3.3 Secrets Management

| Secret | Current Location | Production Target |
|--------|-----------------|-------------------|
| Flask `SECRET_KEY` | `.secret_key` file | `FLASK_SECRET_KEY` env var → Vault |
| Device credentials | `devices.json` | HashiCorp Vault `secret/junos/devices` |
| Database password | Docker env | Vault or AWS Secrets Manager |
| API keys | `NOC_API_KEY` env | Vault `secret/noc/api-keys` |

**Vault integration pattern:**
```bash
# Fetch secrets at container startup
export FLASK_SECRET_KEY=$(vault kv get -field=key secret/noc/flask)
export DATABASE_URL=$(vault kv get -field=url secret/noc/database)
```

---

## 4. AI Engine Validation

### 4.1 Model Verification

The system requires **two** Ollama models:

```bash
# Core reasoning model (chat, analysis, specialists)
ollama pull gpt-oss

# Embedding model (RAG vector store)
ollama pull nomic-embed-text
```

**Verify at startup:**
```bash
# Check models are available
ollama list

# Expected output should include:
# gpt-oss:latest         ... GB
# nomic-embed-text:latest  274 MB

# Verify the app detects them — look for this in startup logs:
python web_ui/app.py 2>&1 | grep -i "ollama model"
# ✓ Ollama model 'gpt-oss' is available
```

**If `gpt-oss` is not available**, the `detect_ollama_model()` function will auto-select the first available model and log:
```
⚠ Ollama model 'gpt-oss' not found. Auto-selected 'llama3' from 2 available models
```

### 4.2 RAG Pipeline Validation

The knowledge base is stored in `kb_vectors.pkl` — built by `ingest_pdfs.py` from 7 Juniper training PDFs (184KB+ of domain knowledge).

**Verify the vector store exists:**
```bash
ls -la kb_vectors.pkl
# Should be > 1MB if properly built

# If missing, rebuild:
python ingest_pdfs.py
```

**Verify RAG is working:**
1. Open the web UI → AI Chat
2. Ask: *"What is the difference between L2VPN and L3VPN in Junos?"*
3. The response should include a **RAG/Sources** badge indicating retrieval from the knowledge base
4. If the answer is generic (not Junos-specific), the vector store may be empty or corrupt — rebuild it

### 4.3 Hypered Brain Pipeline

The 6-layer cognitive architecture processes complex investigations:

```
┌─────────────────────────────────────────────┐
│ Layer 1: PERCEPTION                          │
│   → Parse query, identify target routers     │
│   → Select relevant MCP commands             │
├─────────────────────────────────────────────┤
│ Layer 2: EXECUTION                           │
│   → Run commands via MCP (parallel)          │
│   → Collect raw device output                │
├─────────────────────────────────────────────┤
│ Layer 3: ANALYSIS                            │
│   → AI analyzes collected data               │
│   → Protocol state machine matching          │
│   → Cascade failure chain detection          │
├─────────────────────────────────────────────┤
│ Layer 4: VALIDATION                          │
│   → Self-verify findings (confidence check)  │
│   → Cross-reference with knowledge base      │
│   → Score confidence: 0–100%                 │
├─────────────────────────────────────────────┤
│ Layer 5: SYNTHESIS                           │
│   → Generate structured report               │
│   → Risk scoring + SLA impact                │
│   → Remediation recommendations              │
├─────────────────────────────────────────────┤
│ Layer 6: FEEDBACK                            │
│   → Store results in analysis memory         │
│   → Update issue fingerprints                │
│   → Learn from corrections                   │
└─────────────────────────────────────────────┘
```

**Verification steps:**
1. Open the web UI → AI Chat
2. Enter: *"Run a comprehensive investigation on PE1"*
3. Watch the **Brain Progress Bar** step through: Perception → Execution → Analysis → Validation → Synthesis
4. Check the response for a **Confidence Score** (e.g., `● 85% (High)`)
5. If confidence is below 70%, the validation layer re-runs analysis (up to `max_passes: 3`)

**Tuning** (in `config.yaml`):
```yaml
hypered_brain:
  confidence_threshold: 70    # Lower = faster, higher = more thorough
  max_passes: 3               # 1 = no re-validation, 3 = production-grade
  max_concurrent_scripts: 3   # Increase to 5 for faster labs
```

---

## 5. Real-Time Operations

### 5.1 WebSocket & SSE Health

**AI Streaming (SSE):**
- Endpoint: `POST /api/ai/stream`
- The response is `text/event-stream` with token-by-token delivery
- **Nginx MUST have `proxy_buffering off`** on this route or streaming breaks (user sees nothing for 30+ seconds, then gets the entire response at once)

**WebSocket (Socket.IO):**
- Path: `/socket.io/`
- Used for: task results, workflow progress, device polling, topology updates
- **Nginx MUST allow protocol upgrade** (`Upgrade: websocket`) or Socket.IO falls back to HTTP long-polling (10× slower)
- **Multi-worker mode:** Set `socketio = SocketIO(app, message_queue="redis://...")` to broadcast across Gunicorn workers

**Verification:**
```bash
# Check WebSocket is working (not falling back to polling)
# In browser DevTools → Network → WS tab
# You should see a persistent WebSocket connection to /socket.io/
# If you only see XHR requests to /socket.io/, the upgrade is failing
```

### 5.2 NETCONF Keepalives

The MCP Server connects to Juniper routers via Junos PyEZ (NETCONF over SSH). Firewalls often silently drop idle SSH sessions after 5–15 minutes.

**On Juniper routers:**
```junos
set system services ssh client-alive-interval 60
set system services ssh client-alive-count-max 3
```

**On the MCP Server side:**
- The `jmcp.py` server creates connections on-demand and should tear down idle connections
- If routers become unreachable after idle periods, add SSH keepalives to the NETCONF connection parameters

### 5.3 Circuit Breaker Monitoring

The system tracks device failures internally. When a device fails 3 consecutive times, it's isolated for 5 minutes to prevent cascading timeouts.

**Check circuit breaker state via logs:**
```bash
grep -i "circuit\|isolat\|breaker" logs/bridge_*.log
```

**If the UI stops showing data for a router:**
1. Check if the circuit breaker tripped (3 consecutive failures)
2. The device will auto-recover after 5 minutes
3. To force-reset: restart the MCP server or clear the session with `mcp_clear_session()`

### 5.4 Live Dashboard Verification

**Steps:**
1. Navigate to **Dashboard** → verify stat cards show live data
2. Navigate to **Topology** → nodes should render with color-coded roles
3. Click **Live Monitoring** → verify `/api/monitor/health-dashboard` is being polled
4. **Real-time test:** Shut down an interface on a lab router → the topology link should turn red within 30 seconds (next poll cycle)
5. Verify in browser DevTools → Network: periodic XHR requests to `/api/monitor/health-dashboard`

---

## 6. Health Check Endpoints

The application includes a production health check endpoint for load balancer probes:

| Endpoint | Purpose | Expected Response |
|----------|---------|-------------------|
| `GET /api/health` | Basic liveness | `{"status": "ok"}` |
| `GET /api/bootstrap/status` | Config readiness | `{"bootstrapped": true, ...}` |
| `GET /api/topology/stats` | Topology health | Network statistics JSON |
| `GET /api/config` | Config validation | Loaded YAML config |

**Nginx health check:**
```nginx
location /healthz {
    proxy_pass http://noc_backend/api/health;
    access_log off;
}
```

---

## 7. Monitoring & Observability

### Recommended Stack

| Tool | Purpose |
|------|---------|
| **Prometheus** | Metrics collection (Flask request latency, MCP call duration, AI response time) |
| **Grafana** | Dashboard visualization |
| **Loki** | Log aggregation (replace file-based logs) |
| **Jaeger** | Distributed tracing (MCP call chains) |

### Key Metrics to Monitor

| Metric | Alert Threshold |
|--------|----------------|
| MCP call latency (p95) | > 30s |
| AI response time (p95) | > 60s |
| WebSocket connected clients | > 100 (scale workers) |
| PostgreSQL connection pool | > 80% utilization |
| Celery task queue depth | > 50 pending |
| Redis memory usage | > 200MB |
| Device reachability score | < 80% |
| Circuit breaker trips/hour | > 5 |

---

## 8. Runbook — First Production Deployment

### Prerequisites Checklist

```
□ PostgreSQL 16+ installed and accessible
□ Redis 7+ installed and accessible
□ Ollama installed with gpt-oss + nomic-embed-text models
□ Junos MCP Server running on port 30030
□ SSL certificates for the NOC domain
□ DNS record pointing to the server
□ Firewall rules: 443 inbound, 830 outbound (NETCONF), 11434 local (Ollama)
```

### Step-by-Step

```bash
# 1. Clone and enter project
git clone https://github.com/Mustafa6066/Junos-AI.git
cd Junos-AI

# 2. Set environment variables
export POSTGRES_PASSWORD="$(openssl rand -hex 16)"
export FLASK_SECRET_KEY="$(openssl rand -hex 32)"
export NOC_API_KEY="$(openssl rand -hex 24)"

# 3. Generate self-signed SSL certs (or use your CA)
mkdir -p deploy/certs
openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout deploy/certs/private/noc.key \
  -out deploy/certs/certs/noc.crt \
  -subj "/CN=noc.example.com"

# 4. Configure devices
cp junos-mcp-server/devices-template.json junos-mcp-server/devices.json
# Edit devices.json with your router IPs

# 5. Start the full stack
cd deploy
docker compose up -d

# 6. Verify health
curl -k https://localhost/api/health
# {"status": "ok"}

# 7. Pull AI models into the Ollama container
docker exec -it deploy-ollama-1 ollama pull gpt-oss
docker exec -it deploy-ollama-1 ollama pull nomic-embed-text

# 8. Sync golden configs (first run)
curl -k -X POST https://localhost/api/bootstrap/sync

# 9. Open the NOC
open https://noc.example.com
```

### Post-Deployment Verification

```bash
# ✓ WebSocket connected (check browser DevTools → WS tab)
# ✓ AI Chat responds to "show interfaces on PE1"
# ✓ Topology renders with all nodes
# ✓ Scheduler shows in /api/scheduled-tasks
# ✓ Health dashboard polls automatically
# ✓ Brain progress bar works on investigation queries
```

---

## Migration Path Summary

| Component | Lab (Current) | Production (Target) | Effort |
|-----------|--------------|---------------------|--------|
| Web Server | `socketio.run()` | Gunicorn + Eventlet | Low |
| Database | SQLite × 5 | PostgreSQL | Medium |
| Task Queue | `threading.Thread` | Celery + Redis | Medium |
| SSL | None | Nginx + Let's Encrypt | Low |
| Auth | `X-API-Key` | OAuth2-Proxy + Keycloak | Medium |
| RBAC | None | Role decorator + JWT | Medium |
| Secrets | Local files | HashiCorp Vault | Low |
| Monitoring | Log files | Prometheus + Grafana | Medium |
| SocketIO | Threading mode | Redis message queue | Low |

**Estimated effort for full production migration: 2–3 weeks for a 2-person team.**

---

<p align="center">
  <sub>Junos AI NOC — Production Deployment Guide v24.0</sub>
</p>
