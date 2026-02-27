# ═══════════════════════════════════════════════════════════════
#  Junos AI NOC — Production Dockerfile
# ═══════════════════════════════════════════════════════════════

FROM python:3.12-slim

# ── System dependencies ──
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# ── Working directory ──
WORKDIR /app

# ── Python dependencies ──
COPY web_ui/requirements.txt /app/web_ui/requirements.txt
COPY deploy/requirements-prod.txt /app/deploy/requirements-prod.txt
RUN pip install --no-cache-dir \
    -r /app/web_ui/requirements.txt \
    -r /app/deploy/requirements-prod.txt

# ── Application code ──
COPY web_ui/ /app/web_ui/
COPY modules/ /app/modules/
COPY deploy/ /app/deploy/
COPY config.yaml /app/config.yaml
COPY kb_vectorstore.py /app/kb_vectorstore.py
COPY ingest_pdfs.py /app/ingest_pdfs.py
COPY junos_commands.json /app/junos_commands.json

# ── Golden configs & templates (mounted as volumes in production) ──
COPY golden_configs/ /app/golden_configs/
COPY templates/ /app/templates/

# ── Non-root user ──
RUN useradd -m -s /bin/bash noc && chown -R noc:noc /app
USER noc

# ── Health check ──
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:${NOC_PORT:-5555}/api/health || exit 1

# ── Default: run web server ──
WORKDIR /app/web_ui
EXPOSE ${NOC_PORT:-5555}
CMD ["python", "app.py"]
