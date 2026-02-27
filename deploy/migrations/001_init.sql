-- ═══════════════════════════════════════════════════════════════
--  Junos AI NOC — PostgreSQL Migration v1.0
--  Migrates 5 SQLite databases into a single PostgreSQL instance
-- ═══════════════════════════════════════════════════════════════

CREATE SCHEMA IF NOT EXISTS noc;

-- ─────────────────────────────────────────────────────────────
--  Scheduled Tasks (from scheduled_tasks.db)
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS noc.scheduled_tasks (
    id              SERIAL PRIMARY KEY,
    name            TEXT NOT NULL,
    task_type       TEXT NOT NULL,
    schedule        TEXT NOT NULL,
    target_routers  JSONB NOT NULL DEFAULT '[]',
    command         TEXT NOT NULL,
    enabled         BOOLEAN DEFAULT TRUE,
    last_run        TIMESTAMPTZ,
    last_result     TEXT,
    next_run        TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    run_count       INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS noc.task_history (
    id          SERIAL PRIMARY KEY,
    task_id     INTEGER REFERENCES noc.scheduled_tasks(id) ON DELETE CASCADE,
    run_at      TIMESTAMPTZ DEFAULT NOW(),
    result      TEXT,
    status      TEXT CHECK (status IN ('success', 'error', 'timeout')),
    duration_ms INTEGER
);

-- ─────────────────────────────────────────────────────────────
--  Device Pools (from device_pools.db)
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS noc.device_pools (
    id          SERIAL PRIMARY KEY,
    name        TEXT UNIQUE NOT NULL,
    description TEXT DEFAULT '',
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS noc.pool_members (
    id       SERIAL PRIMARY KEY,
    pool_id  INTEGER REFERENCES noc.device_pools(id) ON DELETE CASCADE,
    router   TEXT NOT NULL,
    UNIQUE(pool_id, router)
);

-- ─────────────────────────────────────────────────────────────
--  Notifications (from notifications.db)
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS noc.notifications (
    id         SERIAL PRIMARY KEY,
    type       TEXT NOT NULL,
    title      TEXT NOT NULL,
    message    TEXT DEFAULT '',
    severity   TEXT DEFAULT 'info' CHECK (severity IN ('info', 'warning', 'error', 'critical')),
    read       BOOLEAN DEFAULT FALSE,
    data       JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─────────────────────────────────────────────────────────────
--  Audit History (from audit_history.db)
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS noc.audit_runs (
    id           SERIAL PRIMARY KEY,
    start_time   TIMESTAMPTZ,
    end_time     TIMESTAMPTZ,
    routers      JSONB DEFAULT '[]',
    total_checks INTEGER DEFAULT 0,
    passed       INTEGER DEFAULT 0,
    failed       INTEGER DEFAULT 0,
    warnings     INTEGER DEFAULT 0,
    status       TEXT DEFAULT 'pending',
    report_path  TEXT
);

CREATE TABLE IF NOT EXISTS noc.audit_findings (
    id          SERIAL PRIMARY KEY,
    run_id      INTEGER REFERENCES noc.audit_runs(id) ON DELETE CASCADE,
    router      TEXT NOT NULL,
    check_id    TEXT NOT NULL,
    check_label TEXT,
    status      TEXT CHECK (status IN ('pass', 'fail', 'warning', 'error')),
    detail      TEXT,
    severity    TEXT DEFAULT 'medium'
);

-- ─────────────────────────────────────────────────────────────
--  Analysis Memory (from analysis_memory.db)
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS noc.investigations (
    id          SERIAL PRIMARY KEY,
    query       TEXT NOT NULL,
    result      TEXT,
    confidence  REAL DEFAULT 0.0,
    model       TEXT,
    routers     JSONB DEFAULT '[]',
    duration_ms INTEGER,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS noc.investigation_findings (
    id                SERIAL PRIMARY KEY,
    investigation_id  INTEGER REFERENCES noc.investigations(id) ON DELETE CASCADE,
    finding_type      TEXT,
    description       TEXT,
    severity          TEXT DEFAULT 'info',
    router            TEXT,
    protocol          TEXT,
    data              JSONB DEFAULT '{}'
);

-- ─────────────────────────────────────────────────────────────
--  Indexes for query performance
-- ─────────────────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_notifications_created ON noc.notifications(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_notifications_unread ON noc.notifications(read) WHERE read = FALSE;
CREATE INDEX IF NOT EXISTS idx_task_history_task ON noc.task_history(task_id, run_at DESC);
CREATE INDEX IF NOT EXISTS idx_scheduled_tasks_next ON noc.scheduled_tasks(next_run) WHERE enabled = TRUE;
CREATE INDEX IF NOT EXISTS idx_investigations_created ON noc.investigations(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_runs_time ON noc.audit_runs(start_time DESC);
CREATE INDEX IF NOT EXISTS idx_audit_findings_run ON noc.audit_findings(run_id);

-- ─────────────────────────────────────────────────────────────
--  Comments for documentation
-- ─────────────────────────────────────────────────────────────
COMMENT ON SCHEMA noc IS 'Junos AI Network Operations Center — all application state';
COMMENT ON TABLE noc.scheduled_tasks IS 'CRON-style scheduled MCP tasks';
COMMENT ON TABLE noc.device_pools IS 'Named groups of routers for batch operations';
COMMENT ON TABLE noc.notifications IS 'In-app notification/alert queue';
COMMENT ON TABLE noc.audit_runs IS 'Network compliance audit execution history';
COMMENT ON TABLE noc.investigations IS 'AI-powered investigation memory for context recall';
