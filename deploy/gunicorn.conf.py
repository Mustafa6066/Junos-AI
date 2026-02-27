# Production Gunicorn config for Junos AI NOC
# Usage: gunicorn --config deploy/gunicorn.conf.py "app:app"

import os

# ── Bind ──
bind = f"0.0.0.0:{os.environ.get('NOC_PORT', '5555')}"

# ── Workers ──
# Rule of thumb: (2 × CPU cores) + 1, but capped for I/O-bound workloads
workers = int(os.environ.get("NOC_WORKERS", 3))
worker_class = "eventlet"  # Required for Flask-SocketIO WebSocket support

# ── Timeouts ──
timeout = 300          # MCP calls can take up to 120s; AI up to 600s
graceful_timeout = 30  # Time to finish requests on SIGTERM
keepalive = 5          # Seconds to wait for next request on keep-alive

# ── Memory management ──
max_requests = 1000          # Recycle worker after N requests (prevents memory leaks)
max_requests_jitter = 50     # Random jitter to avoid all workers restarting at once

# ── Logging ──
accesslog = "-"     # stdout
errorlog = "-"      # stderr
loglevel = os.environ.get("NOC_LOG_LEVEL", "info")

# ── Performance ──
preload_app = True  # Load app before forking workers (shared code, separate state)

# ── Security ──
limit_request_line = 8190
limit_request_fields = 100
limit_request_field_size = 8190
