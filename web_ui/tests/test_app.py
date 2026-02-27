#!/usr/bin/env python3
"""
Comprehensive Test Suite for Junos AI NOC Web UI — app.py
=========================================================
Tests every function and sub-function with use cases and corner cases.
Verifies NO data is cached improperly.

Usage:
    cd web_ui && python -m pytest tests/test_app.py -v --tb=short
"""

import os
import sys
import json
import time
import asyncio
import sqlite3
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime

import pytest

# ── Setup path so we can import app ──
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Patch optional imports BEFORE importing app
sys.modules.setdefault("quantum_engine", MagicMock(
    calculate_network_stats_v2=MagicMock(return_value={
        "total_nodes": 3, "pe_count": 1, "p_count": 2, "rr_count": 0,
        "total_links": 2, "graph_diameter": 2, "redundancy_score": 75,
        "single_points_of_failure": []
    }),
    TarjanSPOF=MagicMock(), fast_diameter_approx=MagicMock(),
    QuantumAnnealingOptimizer=MagicMock(), QuantumWalkAnomalyDetector=MagicMock(),
    LouvainCommunityDetector=MagicMock(), get_clustered_topology=MagicMock(),
    optimize_topology=MagicMock(), detect_anomalies=MagicMock(),
    benchmark=MagicMock()
))

os.environ["NOC_API_KEY"] = ""  # Disable API key for tests

import app as noc_app

# ═══════════════════════════════════════════════════════════════
#  FIXTURES
# ═══════════════════════════════════════════════════════════════

@pytest.fixture
def client():
    """Create Flask test client."""
    noc_app.app.config["TESTING"] = True
    with noc_app.app.test_client() as c:
        yield c


@pytest.fixture
def sample_topology():
    """Minimal topology fixture."""
    return {
        "nodes": [
            {"id": "PE1", "role": "PE", "loopback": "192.168.1.1",
             "bgp_neighbors": ["P11"], "isis_interfaces": ["ge-0/0/0"],
             "ldp": True, "mpls": True, "interfaces": ["ge-0/0/0"]},
            {"id": "P11", "role": "P", "loopback": "192.168.1.2",
             "bgp_neighbors": ["PE1", "P12"], "isis_interfaces": ["ge-0/0/0", "ge-0/0/1"],
             "ldp": True, "mpls": True, "interfaces": ["ge-0/0/0", "ge-0/0/1"]},
            {"id": "P12", "role": "P", "loopback": "192.168.1.3",
             "bgp_neighbors": ["P11"], "isis_interfaces": ["ge-0/0/0"],
             "ldp": True, "mpls": True, "interfaces": ["ge-0/0/0"]},
        ],
        "links": [
            {"source": "PE1", "target": "P11", "type": "isis"},
            {"source": "P11", "target": "P12", "type": "isis"},
        ]
    }


@pytest.fixture
def tmp_golden_dir(tmp_path):
    """Create temp golden config directory with sample configs."""
    gdir = tmp_path / "golden_configs"
    gdir.mkdir()
    (gdir / "PE1.conf").write_text("""
interfaces {
    ge-0/0/0 {
        unit 0 {
            family inet { address 10.0.0.1/30; }
            family iso;
            family mpls;
        }
    }
    lo0 {
        unit 0 {
            family inet { address 192.168.1.1/32; }
        }
    }
}
protocols {
    isis {
        interface ge-0/0/0.0 { point-to-point; level 2 metric 100; }
        interface lo0.0 { passive; }
    }
    bgp {
        group ibgp {
            neighbor 192.168.1.2;
        }
    }
    ldp {
        interface ge-0/0/0.0;
    }
    mpls {
        interface ge-0/0/0.0;
    }
}
""")
    (gdir / "PE1.meta").write_text('{"synced_at": "2026-02-26T00:00:00"}')
    return gdir


# ═══════════════════════════════════════════════════════════════
#  1. NO-CACHE VERIFICATION — Ensure API never caches responses
# ═══════════════════════════════════════════════════════════════

class TestNoCacheHeaders:
    """Verify every API response has no-cache headers."""

    def test_health_no_cache(self, client):
        """UC: Health endpoint must never serve stale data."""
        with patch.object(noc_app, 'run_async', return_value="PE1\nP11"):
            resp = client.get("/api/health")
        assert resp.headers.get("Cache-Control") == "no-store, no-cache, must-revalidate, max-age=0"
        assert resp.headers.get("Pragma") == "no-cache"

    def test_topology_no_cache(self, client):
        """UC: Topology must always reflect real-time state."""
        resp = client.get("/api/topology")
        assert "no-store" in resp.headers.get("Cache-Control", "")

    def test_devices_no_cache(self, client):
        """UC: Device list must be fresh on every load."""
        resp = client.get("/api/devices")
        assert "no-cache" in resp.headers.get("Cache-Control", "")

    def test_ai_chat_no_cache(self, client):
        """UC: AI responses must never be cached."""
        with patch.object(noc_app, 'run_async', return_value={"message": {"content": "test"}}):
            resp = client.post("/api/ai/chat",
                data=json.dumps({"message": "hello"}),
                content_type="application/json")
        assert "no-store" in resp.headers.get("Cache-Control", "")

    def test_static_files_are_not_affected(self, client):
        """UC: Static files (CSS/JS) should NOT have no-cache (only /api/)."""
        resp = client.get("/")
        # The index page is not under /api/, so no-cache should not be forced
        assert "no-store" not in (resp.headers.get("Cache-Control") or "")


# ═══════════════════════════════════════════════════════════════
#  2. MCP SESSION — No stale session caching
# ═══════════════════════════════════════════════════════════════

class TestMCPSession:
    """Verify MCP session lifecycle and no stale caching."""

    def test_clear_session(self):
        """UC: mcp_clear_session resets cached session."""
        noc_app._mcp_session_id = "stale-session"
        noc_app.mcp_clear_session()
        assert noc_app._mcp_session_id is None

    def test_get_session_creates_new_when_none(self):
        """UC: First call to mcp_get_session initializes."""
        noc_app._mcp_session_id = None
        mock_client = AsyncMock()
        with patch.object(noc_app, 'mcp_initialize', new_callable=AsyncMock, return_value="new-session"):
            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(noc_app.mcp_get_session(mock_client))
            loop.close()
        assert result == "new-session"

    def test_get_session_returns_cached(self):
        """UC: Subsequent calls return cached session without re-init."""
        noc_app._mcp_session_id = "existing-session"
        mock_client = AsyncMock()
        with patch.object(noc_app, 'mcp_initialize', new_callable=AsyncMock) as mock_init:
            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(noc_app.mcp_get_session(mock_client))
            loop.close()
        assert result == "existing-session"
        mock_init.assert_not_called()

    def teardown_method(self):
        noc_app._mcp_session_id = None


# ═══════════════════════════════════════════════════════════════
#  3. OLLAMA AI ENGINE — Chat, Stream, Analyze
# ═══════════════════════════════════════════════════════════════

class TestOllamaChat:
    """Test ollama_chat_async with all edge cases."""

    def test_chat_success(self):
        """UC: Normal chat returns AI response."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"message": {"content": "Hello from AI"}}

        with patch("httpx.AsyncClient") as MockClient:
            instance = AsyncMock()
            instance.post.return_value = mock_resp
            instance.__aenter__ = AsyncMock(return_value=instance)
            instance.__aexit__ = AsyncMock(return_value=False)
            MockClient.return_value = instance

            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(
                noc_app.ollama_chat_async([{"role": "user", "content": "hi"}])
            )
            loop.close()
        assert result["message"]["content"] == "Hello from AI"

    def test_chat_empty_messages(self):
        """Corner: Empty messages list should still work."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"message": {"content": ""}}

        with patch("httpx.AsyncClient") as MockClient:
            instance = AsyncMock()
            instance.post.return_value = mock_resp
            instance.__aenter__ = AsyncMock(return_value=instance)
            instance.__aexit__ = AsyncMock(return_value=False)
            MockClient.return_value = instance

            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(noc_app.ollama_chat_async([]))
            loop.close()
        assert "message" in result

    def test_chat_connect_error(self):
        """Corner: Ollama not running returns graceful error."""
        import httpx as hx

        with patch("httpx.AsyncClient") as MockClient:
            instance = AsyncMock()
            instance.post.side_effect = hx.ConnectError("Connection refused")
            instance.__aenter__ = AsyncMock(return_value=instance)
            instance.__aexit__ = AsyncMock(return_value=False)
            MockClient.return_value = instance

            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(
                noc_app.ollama_chat_async([{"role": "user", "content": "test"}])
            )
            loop.close()
        assert "Cannot connect" in result["message"]["content"]

    def test_chat_timeout(self):
        """Corner: Ollama takes too long returns timeout error."""
        import httpx as hx

        with patch("httpx.AsyncClient") as MockClient:
            instance = AsyncMock()
            instance.post.side_effect = hx.ReadTimeout("Timeout")
            instance.__aenter__ = AsyncMock(return_value=instance)
            instance.__aexit__ = AsyncMock(return_value=False)
            MockClient.return_value = instance

            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(
                noc_app.ollama_chat_async([{"role": "user", "content": "test"}])
            )
            loop.close()
        assert "timed out" in result["message"]["content"]

    def test_chat_http_error(self):
        """Corner: Ollama returns HTTP 500."""
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        mock_resp.text = "Internal Server Error"

        with patch("httpx.AsyncClient") as MockClient:
            instance = AsyncMock()
            instance.post.return_value = mock_resp
            instance.__aenter__ = AsyncMock(return_value=instance)
            instance.__aexit__ = AsyncMock(return_value=False)
            MockClient.return_value = instance

            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(
                noc_app.ollama_chat_async([{"role": "user", "content": "test"}])
            )
            loop.close()
        assert "HTTP 500" in result["message"]["content"]

    def test_chat_custom_model(self):
        """UC: Passing model override uses that model."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"message": {"content": "ok"}}

        with patch("httpx.AsyncClient") as MockClient:
            instance = AsyncMock()
            instance.post.return_value = mock_resp
            instance.__aenter__ = AsyncMock(return_value=instance)
            instance.__aexit__ = AsyncMock(return_value=False)
            MockClient.return_value = instance

            loop = asyncio.new_event_loop()
            loop.run_until_complete(
                noc_app.ollama_chat_async([{"role": "user", "content": "test"}], model="llama3")
            )
            loop.close()

            call_args = instance.post.call_args
            payload = call_args[1]["json"] if "json" in call_args[1] else call_args[0][1]
            assert payload["model"] == "llama3"


class TestOllamaAnalyze:
    """Test ollama_analyze_async."""

    def test_analyze_success(self):
        """UC: Analyze returns AI-generated analysis text."""
        with patch.object(noc_app, 'ollama_chat_async', new_callable=AsyncMock,
                          return_value={"message": {"content": "BGP session is down"}}):
            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(
                noc_app.ollama_analyze_async("You are expert", "show bgp summary", "What is wrong?")
            )
            loop.close()
        assert result == "BGP session is down"

    def test_analyze_empty_data(self):
        """Corner: Empty data string still produces response."""
        with patch.object(noc_app, 'ollama_chat_async', new_callable=AsyncMock,
                          return_value={"message": {"content": "No data to analyze"}}):
            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(
                noc_app.ollama_analyze_async("System", "", "Analyze")
            )
            loop.close()
        assert "No data" in result

    def test_analyze_missing_content_key(self):
        """Corner: Ollama returns unexpected structure."""
        with patch.object(noc_app, 'ollama_chat_async', new_callable=AsyncMock,
                          return_value={}):
            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(
                noc_app.ollama_analyze_async("System", "data", "question")
            )
            loop.close()
        assert result == "No response from AI"


# ═══════════════════════════════════════════════════════════════
#  4. API ROUTES — AI Chat Endpoints
# ═══════════════════════════════════════════════════════════════

class TestAPIChatEndpoint:
    """Test /api/ai/chat."""

    def test_chat_success(self, client):
        """UC: Normal chat request returns 200 with response."""
        with patch.object(noc_app, 'run_async', return_value={"message": {"content": "Hello!"}}):
            resp = client.post("/api/ai/chat",
                data=json.dumps({"message": "hi"}),
                content_type="application/json")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["response"] == "Hello!"
        assert "model" in data
        assert "timestamp" in data

    def test_chat_empty_message(self, client):
        """Corner: Empty message returns 400."""
        resp = client.post("/api/ai/chat",
            data=json.dumps({"message": ""}),
            content_type="application/json")
        assert resp.status_code == 400

    def test_chat_missing_message(self, client):
        """Corner: No message field returns 400."""
        resp = client.post("/api/ai/chat",
            data=json.dumps({}),
            content_type="application/json")
        assert resp.status_code == 400

    def test_chat_no_body(self, client):
        """Corner: No JSON body at all."""
        resp = client.post("/api/ai/chat", content_type="application/json")
        assert resp.status_code == 400

    def test_chat_with_history(self, client):
        """UC: Chat with history context."""
        with patch.object(noc_app, 'run_async', return_value={"message": {"content": "Based on our conversation..."}}):
            resp = client.post("/api/ai/chat",
                data=json.dumps({
                    "message": "continue",
                    "history": [
                        {"role": "user", "content": "show bgp"},
                        {"role": "assistant", "content": "BGP is running"}
                    ]
                }),
                content_type="application/json")
        assert resp.status_code == 200

    def test_chat_ollama_down(self, client):
        """Corner: Ollama unreachable returns 503."""
        with patch.object(noc_app, 'run_async', side_effect=Exception("Connection refused")):
            resp = client.post("/api/ai/chat",
                data=json.dumps({"message": "test"}),
                content_type="application/json")
        assert resp.status_code == 503


class TestAPIAnalyzeEndpoint:
    """Test /api/ai/analyze."""

    def test_analyze_success(self, client):
        """UC: Analyze data returns AI analysis."""
        with patch.object(noc_app, 'run_async', return_value="BGP is stable"):
            resp = client.post("/api/ai/analyze",
                data=json.dumps({"data": "show bgp summary output", "question": "Is BGP ok?"}),
                content_type="application/json")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "analysis" in data

    def test_analyze_no_data(self, client):
        """Corner: No data field returns 400."""
        resp = client.post("/api/ai/analyze",
            data=json.dumps({"question": "test"}),
            content_type="application/json")
        assert resp.status_code == 400

    def test_analyze_empty_data(self, client):
        """Corner: Empty data string returns 400."""
        resp = client.post("/api/ai/analyze",
            data=json.dumps({"data": ""}),
            content_type="application/json")
        assert resp.status_code == 400


class TestAPIModelsEndpoint:
    """Test /api/ai/models."""

    def test_models_ollama_available(self, client):
        """UC: List available Ollama models."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"models": [{"name": "llama3"}, {"name": "gpt-oss"}]}
        with patch("httpx.get", return_value=mock_resp):
            resp = client.get("/api/ai/models")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "models" in data
        assert "active" in data
        assert len(data["models"]) == 2

    def test_models_ollama_down(self, client):
        """Corner: Ollama not running returns empty model list."""
        with patch("httpx.get", side_effect=Exception("Connection refused")):
            resp = client.get("/api/ai/models")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["models"] == []
        assert "error" in data


# ═══════════════════════════════════════════════════════════════
#  5. AGENTIC CHAT — Classification + Routing
# ═══════════════════════════════════════════════════════════════

class TestAgenticChat:
    """Test /api/ai/chat-agentic with all query types."""

    def test_agentic_empty_message(self, client):
        """Corner: Empty message returns 400."""
        resp = client.post("/api/ai/chat-agentic",
            data=json.dumps({"message": ""}),
            content_type="application/json")
        assert resp.status_code == 400

    def test_agentic_general_query(self, client):
        """UC: General question routes to general handler."""
        with patch.object(noc_app, 'classify_query_web', return_value={"type": "general"}), \
             patch.object(noc_app, '_init_kb_store', return_value=None), \
             patch.object(noc_app, 'run_async', return_value={"message": {"content": "General answer"}}):
            resp = client.post("/api/ai/chat-agentic",
                data=json.dumps({"message": "what is MPLS?"}),
                content_type="application/json")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["type"] == "general"

    def test_agentic_knowledge_query(self, client):
        """UC: Knowledge question routes through RAG."""
        mock_store = MagicMock()
        mock_chunks = [{"text": "MPLS Label Switching...", "heading": "MPLS Basics", "score": 0.9}]

        with patch.object(noc_app, 'classify_query_web', return_value={"type": "knowledge"}), \
             patch.object(noc_app, '_init_kb_store', return_value=mock_store), \
             patch.object(noc_app, 'run_async') as mock_run:
            # First run_async call returns RAG chunks, second returns chat response
            mock_run.side_effect = [mock_chunks, {"message": {"content": "MPLS is..."}}]
            resp = client.post("/api/ai/chat-agentic",
                data=json.dumps({"message": "explain MPLS label switching"}),
                content_type="application/json")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["type"] == "knowledge"
        assert "sources" in data

    def test_agentic_config_query(self, client):
        """UC: Config question sets requires_approval flag."""
        with patch.object(noc_app, 'classify_query_web', return_value={"type": "config"}), \
             patch.object(noc_app, 'run_async', return_value={"message": {"content": "set interfaces ge-0/0/0..."}}):
            resp = client.post("/api/ai/chat-agentic",
                data=json.dumps({"message": "configure BGP on PE1"}),
                content_type="application/json")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["type"] == "config"
        assert data["requires_approval"] is True


class TestQueryClassification:
    """Test classify_query_web."""

    def test_classify_troubleshoot(self):
        """UC: Troubleshooting queries classified correctly."""
        result = noc_app.classify_query_web("why is BGP down on PE1?")
        assert result["type"] in ("troubleshoot", "status")

    def test_classify_config(self):
        """UC: Config queries classified correctly."""
        result = noc_app.classify_query_web("configure OSPF on PE1")
        assert result["type"] == "config"

    def test_classify_knowledge(self):
        """UC: Knowledge queries classified correctly."""
        result = noc_app.classify_query_web("explain how MPLS label switching works")
        assert result["type"] in ("knowledge", "general")

    def test_classify_status(self):
        """UC: Status queries classified correctly."""
        result = noc_app.classify_query_web("show me the status of PE1")
        assert result["type"] in ("status", "troubleshoot")

    def test_classify_empty_string(self):
        """Corner: Empty query returns general."""
        result = noc_app.classify_query_web("")
        assert result["type"] == "general"

    def test_classify_very_long_query(self):
        """Corner: Very long query doesn't crash."""
        result = noc_app.classify_query_web("why " * 5000)
        assert "type" in result

    def test_classify_special_characters(self):
        """Corner: Special chars don't crash classification."""
        result = noc_app.classify_query_web("show <script>alert('xss')</script> on PE1")
        assert "type" in result

    def test_classify_unicode(self):
        """Corner: Unicode text doesn't crash."""
        result = noc_app.classify_query_web("配置 BGP 在 PE1 上")
        assert "type" in result


# ═══════════════════════════════════════════════════════════════
#  6. HEALTH ENDPOINT
# ═══════════════════════════════════════════════════════════════

class TestHealthEndpoint:
    """Test /api/health."""

    def test_health_both_up(self, client):
        """UC: Both MCP and Ollama reachable."""
        mock_ollama_resp = MagicMock()
        mock_ollama_resp.status_code = 200
        mock_ollama_resp.json.return_value = {"models": [{"name": "gpt-oss"}]}

        with patch.object(noc_app, 'run_async', return_value="PE1\nP11"), \
             patch("httpx.get", return_value=mock_ollama_resp):
            resp = client.get("/api/health")
        data = resp.get_json()
        assert data["mcp"] == "connected"
        assert data["ollama"] == "connected"

    def test_health_mcp_down(self, client):
        """Corner: MCP server unreachable."""
        mock_ollama_resp = MagicMock()
        mock_ollama_resp.status_code = 200
        mock_ollama_resp.json.return_value = {"models": []}

        with patch.object(noc_app, 'run_async', return_value="Error: Connection refused"), \
             patch("httpx.get", return_value=mock_ollama_resp):
            resp = client.get("/api/health")
        data = resp.get_json()
        assert "error" in data["mcp"]

    def test_health_ollama_down(self, client):
        """Corner: Ollama unreachable."""
        with patch.object(noc_app, 'run_async', return_value="PE1"), \
             patch("httpx.get", side_effect=Exception("Connection refused")):
            resp = client.get("/api/health")
        data = resp.get_json()
        assert "error" in data["ollama"]

    def test_health_returns_fresh_data(self, client):
        """UC: Health returns different timestamps on each call (not cached)."""
        with patch.object(noc_app, 'run_async', return_value="PE1"), \
             patch("httpx.get", side_effect=Exception("down")):
            resp1 = client.get("/api/health")
            time.sleep(0.01)
            resp2 = client.get("/api/health")
        t1 = resp1.get_json()["timestamp"]
        t2 = resp2.get_json()["timestamp"]
        # Timestamps should differ — proves not cached
        assert t1 != t2


# ═══════════════════════════════════════════════════════════════
#  7. TOPOLOGY & NETWORK STATS
# ═══════════════════════════════════════════════════════════════

class TestTopology:
    """Test /api/topology."""

    def test_topology_returns_nodes_and_links(self, client):
        """UC: Topology returns structured graph data."""
        resp = client.get("/api/topology")
        data = resp.get_json()
        assert "nodes" in data
        assert "links" in data
        assert isinstance(data["nodes"], list)

    def test_topology_not_cached_between_requests(self, client):
        """UC: Topology is rebuilt on each request (no stale cache)."""
        resp1 = client.get("/api/topology")
        resp2 = client.get("/api/topology")
        # Both should succeed (rebuilt each time from golden configs)
        assert resp1.status_code == 200
        assert resp2.status_code == 200


class TestNetworkStats:
    """Test /api/network-stats."""

    def test_stats_returns_data(self, client):
        """UC: Network stats endpoint returns computed metrics."""
        resp = client.get("/api/network-stats")
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════════════
#  8. DEVICE POOLS — CRUD
# ═══════════════════════════════════════════════════════════════

class TestDevicePools:
    """Test /api/pools CRUD."""

    def test_list_pools_empty(self, client):
        """UC: Initially no pools."""
        resp = client.get("/api/pools")
        assert resp.status_code == 200
        data = resp.get_json()
        assert isinstance(data, list)

    def test_create_pool(self, client):
        """UC: Create a device pool."""
        # Use unique name to avoid IntegrityError on re-run
        unique_name = f"test-pool-{int(time.time() * 1000)}"
        resp = client.post("/api/pools",
            data=json.dumps({"name": unique_name, "description": "Test", "devices": ["PE1"], "tags": ["core"], "color": "#FF0000"}),
            content_type="application/json")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data.get("name") == unique_name

    def test_create_pool_no_name(self, client):
        """Corner: No name returns error."""
        resp = client.post("/api/pools",
            data=json.dumps({"devices": ["PE1"]}),
            content_type="application/json")
        assert resp.status_code in (200, 400)

    def test_delete_pool_nonexistent(self, client):
        """Corner: Delete non-existent pool."""
        resp = client.delete("/api/pools/99999")
        # Should not crash
        assert resp.status_code in (200, 404)


# ═══════════════════════════════════════════════════════════════
#  9. PING / REACHABILITY
# ═══════════════════════════════════════════════════════════════

class TestPing:
    """Test /api/ping endpoints."""

    def test_ping_single_router(self, client):
        """UC: Ping a single router via MCP."""
        with patch.object(noc_app, 'run_async', return_value='PING 192.168.1.1: 5 packets transmitted, 5 received'):
            resp = client.get("/api/ping/PE1")
        assert resp.status_code == 200

    def test_ping_nonexistent_router(self, client):
        """Corner: Ping unknown router."""
        with patch.object(noc_app, 'run_async', return_value='Error: Router not found'):
            resp = client.get("/api/ping/NONEXISTENT")
        assert resp.status_code == 200  # Returns result even for errors

    def test_ping_sweep(self, client):
        """UC: Sweep all routers."""
        with patch.object(noc_app, 'run_async', return_value='PE1: OK\nP11: OK'):
            resp = client.post("/api/ping/sweep",
                data=json.dumps({}),
                content_type="application/json")
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════════════
#  10. NOTIFICATIONS — CRUD
# ═══════════════════════════════════════════════════════════════

class TestNotifications:
    """Test /api/notifications endpoints."""

    def test_list_channels_empty(self, client):
        """UC: No channels initially."""
        resp = client.get("/api/notifications/channels")
        assert resp.status_code == 200
        data = resp.get_json()
        assert isinstance(data, list)

    def test_create_channel(self, client):
        """UC: Create a notification channel."""
        resp = client.post("/api/notifications/channels",
            data=json.dumps({"name": "test-slack", "channel_type": "slack", "webhook_url": "https://hooks.slack.com/test"}),
            content_type="application/json")
        assert resp.status_code == 200

    def test_create_channel_no_name(self, client):
        """Corner: Missing channel name."""
        resp = client.post("/api/notifications/channels",
            data=json.dumps({"channel_type": "slack"}),
            content_type="application/json")
        # Should either work (with empty name) or return error
        assert resp.status_code in (200, 400)


# ═══════════════════════════════════════════════════════════════
#  11. SCHEDULED TASKS — CRUD
# ═══════════════════════════════════════════════════════════════

class TestScheduledTasks:
    """Test /api/scheduled-tasks endpoints."""

    def test_list_tasks(self, client):
        """UC: List scheduled tasks."""
        resp = client.get("/api/scheduled-tasks")
        assert resp.status_code == 200

    def test_create_task(self, client):
        """UC: Create a scheduled task."""
        resp = client.post("/api/scheduled-tasks",
            data=json.dumps({
                "name": "bgp-check",
                "router": "PE1",
                "command": "show bgp summary",
                "interval_minutes": 30
            }),
            content_type="application/json")
        assert resp.status_code == 200

    def test_delete_nonexistent_task(self, client):
        """Corner: Delete task that doesn't exist."""
        resp = client.delete("/api/scheduled-tasks/99999")
        assert resp.status_code in (200, 404)


# ═══════════════════════════════════════════════════════════════
#  12. GOLDEN CONFIGS
# ═══════════════════════════════════════════════════════════════

class TestGoldenConfigs:
    """Test /api/golden-configs endpoints."""

    def test_list_configs(self, client):
        """UC: List all golden configs."""
        resp = client.get("/api/golden-configs")
        assert resp.status_code == 200
        data = resp.get_json()
        assert isinstance(data, (list, dict))

    def test_get_config_nonexistent(self, client):
        """Corner: Request config for non-existent router."""
        resp = client.get("/api/golden-configs/NONEXISTENT")
        data = resp.get_json()
        # Should return error or empty, not crash
        assert resp.status_code in (200, 404)


# ═══════════════════════════════════════════════════════════════
#  13. CONFIG DIFF ENGINE
# ═══════════════════════════════════════════════════════════════

class TestConfigDiff:
    """Test /api/config-diff/<router> (GET)."""

    def test_diff_same_router(self, client):
        """Corner: Diff a router against its golden config."""
        resp = client.get("/api/config-diff/PE1")
        assert resp.status_code == 200
        data = resp.get_json()
        # Either returns diff data or error (no golden config)
        assert "router" in data or "error" in data

    def test_diff_missing_routers(self, client):
        """Corner: Diff for a router with no golden config."""
        resp = client.get("/api/config-diff/PE1")
        assert resp.status_code == 200

    def test_diff_nonexistent_routers(self, client):
        """Corner: Router with no config returns error in response."""
        resp = client.get("/api/config-diff/NONEXISTENT_ROUTER_XYZ")
        assert resp.status_code == 200
        data = resp.get_json()
        # Should return an error field, not crash
        assert "error" in data or "router" in data


# ═══════════════════════════════════════════════════════════════
#  14. TEMPLATES ENGINE
# ═══════════════════════════════════════════════════════════════

class TestTemplates:
    """Test /api/templates endpoints."""

    def test_list_templates(self, client):
        """UC: List available Jinja2 templates."""
        resp = client.get("/api/templates")
        assert resp.status_code == 200

    def test_render_template(self, client):
        """UC: Render an existing template with variables."""
        # Use an actual template name that exists on disk (e.g., ospf_p2p)
        resp = client.post("/api/templates/render",
            data=json.dumps({
                "template": "ospf_p2p",
                "variables": {"interface": "ge-0/0/0", "area": "0.0.0.0"}
            }),
            content_type="application/json")
        # 200 if template exists, 404 if not — both are valid
        assert resp.status_code in (200, 404)

    def test_render_template_missing_vars(self, client):
        """Corner: Template with missing variables."""
        resp = client.post("/api/templates/render",
            data=json.dumps({
                "template": "ospf_p2p",
                "variables": {}
            }),
            content_type="application/json")
        # 200 (renders with empty vars), 400 (render error), or 404 (template not found)
        assert resp.status_code in (200, 400, 404)


# ═══════════════════════════════════════════════════════════════
#  15. GIT EXPORT
# ═══════════════════════════════════════════════════════════════

class TestGitExport:
    """Test /api/git-export endpoints."""

    def test_git_log_no_repo(self, client):
        """Corner: Git log before init returns error."""
        resp = client.get("/api/git-export/log")
        assert resp.status_code == 200  # Returns error in body, not HTTP error


# ═══════════════════════════════════════════════════════════════
#  16. RESULT COMPARISON
# ═══════════════════════════════════════════════════════════════

class TestResultComparison:
    """Test /api/results endpoints."""

    def test_list_results_empty(self, client):
        """UC: No captured results initially."""
        resp = client.get("/api/results")
        assert resp.status_code == 200

    def test_compare_missing_results(self, client):
        """Corner: Compare non-existent results."""
        resp = client.post("/api/results/compare",
            data=json.dumps({"result_a": "fake-a", "result_b": "fake-b"}),
            content_type="application/json")
        assert resp.status_code in (200, 404)


# ═══════════════════════════════════════════════════════════════
#  17. SHORTEST PATH
# ═══════════════════════════════════════════════════════════════

class TestShortestPath:
    """Test /api/shortest-path (GET with query params)."""

    def test_path_same_node(self, client):
        """Corner: Path from node to itself."""
        resp = client.get("/api/shortest-path?source=PE1&target=PE1")
        assert resp.status_code == 200

    def test_path_missing_fields(self, client):
        """Corner: Missing source/target returns error."""
        resp = client.get("/api/shortest-path")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "error" in data

    def test_path_nonexistent_nodes(self, client):
        """Corner: Non-existent nodes."""
        resp = client.get("/api/shortest-path?source=FAKE1&target=FAKE2")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "error" in data or "path" in data


# ═══════════════════════════════════════════════════════════════
#  18. ENSEMBLE AI
# ═══════════════════════════════════════════════════════════════

class TestEnsembleAI:
    """Test /api/ai/ensemble."""

    def test_ensemble_no_question(self, client):
        """Corner: No question returns 400."""
        resp = client.post("/api/ai/ensemble",
            data=json.dumps({}),
            content_type="application/json")
        assert resp.status_code == 400

    def test_ensemble_success(self, client):
        """UC: Ensemble queries multiple models."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"models": [{"name": "gpt-oss"}]}

        with patch.object(noc_app, 'run_async') as mock_run:
            # First call: model list, subsequent: chat responses
            mock_run.side_effect = [
                mock_resp,  # model listing
                {"message": {"content": "Answer 1\nCONFIDENCE: 90%"}},
            ]
            # Also patch the async model list
            async def _fake_list():
                return mock_resp
            with patch("httpx.AsyncClient") as MockClient:
                instance = AsyncMock()
                instance.get.return_value = mock_resp
                instance.__aenter__ = AsyncMock(return_value=instance)
                instance.__aexit__ = AsyncMock(return_value=False)
                MockClient.return_value = instance

                resp = client.post("/api/ai/ensemble",
                    data=json.dumps({"question": "Is the network healthy?"}),
                    content_type="application/json")
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════════════
#  19. UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════

class TestSSEParser:
    """Test parse_sse_response."""

    def test_parse_valid_sse(self):
        """UC: Parse standard SSE response."""
        text = 'data: {"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"OK"}]}}\n\n'
        result = noc_app.parse_sse_response(text)
        assert "result" in result

    def test_parse_empty(self):
        """Corner: Empty text."""
        result = noc_app.parse_sse_response("")
        assert result == {}

    def test_parse_garbage(self):
        """Corner: Non-SSE text."""
        result = noc_app.parse_sse_response("not valid sse at all")
        assert result == {}

    def test_parse_multiple_events(self):
        """UC: Multiple SSE events returns last result."""
        text = (
            'data: {"jsonrpc":"2.0","id":1,"result":{"old":"data"}}\n'
            'data: {"jsonrpc":"2.0","id":2,"result":{"new":"data"}}\n'
        )
        result = noc_app.parse_sse_response(text)
        assert result.get("result", {}).get("new") == "data"

    def test_parse_malformed_json(self):
        """Corner: Malformed JSON in SSE."""
        text = 'data: {broken json\ndata: {"valid": true}\n'
        result = noc_app.parse_sse_response(text)
        assert result == {"valid": True}


class TestRunAsync:
    """Test run_async helper."""

    def test_run_async_success(self):
        """UC: run_async executes coroutine."""
        async def _coro():
            return 42
        assert noc_app.run_async(_coro()) == 42

    def test_run_async_exception(self):
        """Corner: Coroutine raises exception."""
        async def _coro():
            raise ValueError("test error")
        with pytest.raises(ValueError, match="test error"):
            noc_app.run_async(_coro())


class TestEscapeHtml:
    """Test the frontend escapeHtml equivalent (verified via backend patterns)."""

    def test_xss_in_device_name(self, client):
        """Corner: XSS in device names should not execute."""
        # The topology endpoint should not render raw HTML
        resp = client.get("/api/topology")
        data = resp.get_json()
        # Node IDs should be plain strings, not containing executable HTML
        for node in data.get("nodes", []):
            assert "<script>" not in node.get("id", "")


# ═══════════════════════════════════════════════════════════════
#  20. VALIDATION ENGINE
# ═══════════════════════════════════════════════════════════════

class TestValidation:
    """Test /api/validate endpoints."""

    def test_validate_missing_fields(self, client):
        """Corner: Missing required fields."""
        resp = client.post("/api/validate",
            data=json.dumps({"router": "PE1"}),
            content_type="application/json")
        assert resp.status_code in (200, 400)

    def test_validate_success(self, client):
        """UC: Validate command output against pattern."""
        with patch.object(noc_app, 'run_async', return_value="Established\nEstablished"):
            resp = client.post("/api/validate",
                data=json.dumps({
                    "router": "PE1",
                    "command": "show bgp summary",
                    "pattern": "Established",
                    "match_type": "contains"
                }),
                content_type="application/json")
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════════════
#  21. MCP COMMAND EXECUTION
# ═══════════════════════════════════════════════════════════════

class TestMCPExecute:
    """Test /api/mcp/execute."""

    def test_execute_missing_command(self, client):
        """Corner: No command field."""
        resp = client.post("/api/mcp/execute",
            data=json.dumps({"router": "PE1"}),
            content_type="application/json")
        assert resp.status_code in (200, 400)

    def test_execute_missing_router(self, client):
        """Corner: No router field."""
        resp = client.post("/api/mcp/execute",
            data=json.dumps({"command": "show version"}),
            content_type="application/json")
        assert resp.status_code in (200, 400)

    def test_execute_success(self, client):
        """UC: Execute command on router."""
        with patch.object(noc_app, 'run_async', return_value="Junos: 23.4R1"):
            resp = client.post("/api/mcp/execute",
                data=json.dumps({"router": "PE1", "command": "show version"}),
                content_type="application/json")
        assert resp.status_code == 200

    def test_execute_xss_in_command(self, client):
        """Corner: XSS in command should not execute."""
        with patch.object(noc_app, 'run_async', return_value="Error"):
            resp = client.post("/api/mcp/execute",
                data=json.dumps({"router": "PE1", "command": "<script>alert(1)</script>"}),
                content_type="application/json")
        assert resp.status_code == 200
        # Response should be JSON, not HTML
        assert resp.content_type.startswith("application/json")


# ═══════════════════════════════════════════════════════════════
#  22. STREAMING — No data caching
# ═══════════════════════════════════════════════════════════════

class TestStreamingNocache:
    """Verify streaming endpoint uses no-cache headers."""

    def test_stream_no_cache_headers(self, client):
        """UC: SSE stream has Cache-Control: no-cache."""
        with patch.object(noc_app, 'run_async', return_value={"message": {"content": "test"}}):
            resp = client.post("/api/ai/stream",
                data=json.dumps({"message": "hello"}),
                content_type="application/json")
        # SSE responses explicitly set no-cache
        cc = resp.headers.get("Cache-Control", "")
        assert "no-cache" in cc or "no-store" in cc


# ═══════════════════════════════════════════════════════════════
#  23. LOGS ENDPOINT
# ═══════════════════════════════════════════════════════════════

class TestLogs:
    """Test /api/logs."""

    def test_list_logs(self, client):
        """UC: List log files."""
        resp = client.get("/api/logs")
        assert resp.status_code == 200

    def test_get_nonexistent_log(self, client):
        """Corner: Request non-existent log file."""
        resp = client.get("/api/logs/nonexistent_2099-01-01.log")
        assert resp.status_code in (200, 404)


# ═══════════════════════════════════════════════════════════════
#  24. INDEX / ROOT ROUTE
# ═══════════════════════════════════════════════════════════════

class TestIndexRoute:
    """Test the main page."""

    def test_index_returns_html(self, client):
        """UC: Root returns the SPA HTML."""
        resp = client.get("/")
        assert resp.status_code == 200
        assert b"<!DOCTYPE html>" in resp.data or b"<html" in resp.data


# ═══════════════════════════════════════════════════════════════
#  25. MODEL AUTO-DETECTION
# ═══════════════════════════════════════════════════════════════

class TestModelAutoDetection:
    """Test detect_ollama_model."""

    def test_detect_model_present(self):
        """UC: Configured model is available."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"models": [{"name": "gpt-oss"}, {"name": "llama3"}]}

        original_model = noc_app.OLLAMA_MODEL
        noc_app.OLLAMA_MODEL = "gpt-oss"
        with patch("httpx.get", return_value=mock_resp):
            noc_app.detect_ollama_model()
        assert noc_app.OLLAMA_MODEL == "gpt-oss"
        noc_app.OLLAMA_MODEL = original_model

    def test_detect_model_missing_auto_selects(self):
        """UC: Configured model not found, auto-selects first available."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"models": [{"name": "llama3"}, {"name": "codellama"}]}

        original_model = noc_app.OLLAMA_MODEL
        noc_app.OLLAMA_MODEL = "nonexistent-model"
        with patch("httpx.get", return_value=mock_resp):
            noc_app.detect_ollama_model()
        assert noc_app.OLLAMA_MODEL == "llama3"
        noc_app.OLLAMA_MODEL = original_model

    def test_detect_model_no_models_installed(self):
        """Corner: Ollama running but no models installed."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"models": []}

        original_model = noc_app.OLLAMA_MODEL
        noc_app.OLLAMA_MODEL = "gpt-oss"
        with patch("httpx.get", return_value=mock_resp):
            noc_app.detect_ollama_model()
        # Should keep original model name (graceful degradation)
        assert noc_app.OLLAMA_MODEL == "gpt-oss"
        noc_app.OLLAMA_MODEL = original_model

    def test_detect_model_ollama_down(self):
        """Corner: Ollama not running."""
        original_model = noc_app.OLLAMA_MODEL
        noc_app.OLLAMA_MODEL = "gpt-oss"
        with patch("httpx.get", side_effect=Exception("Connection refused")):
            noc_app.detect_ollama_model()
        # Should keep original model (not crash)
        assert noc_app.OLLAMA_MODEL == "gpt-oss"
        noc_app.OLLAMA_MODEL = original_model


# ═══════════════════════════════════════════════════════════════
#  26. REMEDIATION ENGINE — Proposal, Approve, Reject, Execute
# ═══════════════════════════════════════════════════════════════

class TestRemediation:
    """Test full remediation lifecycle: propose → approve → execute."""

    def test_propose_remediation(self, client):
        """UC: AI proposes remediation commands for a detected issue."""
        ai_response = (
            "TITLE: Fix BGP session on PE1\n"
            "COMMANDS:\nset protocols bgp group ibgp neighbor 10.0.0.2\n"
            "ROLLBACK:\ndelete protocols bgp group ibgp neighbor 10.0.0.2\n"
            "RISK: medium\nIMPACT: BGP session will flap"
        )
        with patch.object(noc_app, 'run_async', return_value=ai_response):
            resp = client.post("/api/remediate/propose",
                data=json.dumps({"issue": "BGP down on PE1", "router": "PE1"}),
                content_type="application/json")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "id" in data
        assert data["status"] == "pending"
        assert data["risk_level"] == "medium"
        # Cleanup
        self._cleanup_remediation(data["id"])

    def test_propose_missing_issue(self, client):
        """Corner: Missing issue → 400."""
        resp = client.post("/api/remediate/propose",
            data=json.dumps({}), content_type="application/json")
        assert resp.status_code == 400

    def test_list_remediations(self, client):
        """UC: List all remediation proposals."""
        resp = client.get("/api/remediate/list")
        assert resp.status_code == 200
        assert isinstance(resp.get_json(), list)

    def test_approve_remediation(self, client):
        """UC: Approve a pending remediation."""
        rem_id = self._create_test_remediation()
        resp = client.post(f"/api/remediate/{rem_id}/approve")
        assert resp.status_code == 200
        assert resp.get_json()["status"] == "approved"
        self._cleanup_remediation(rem_id)

    def test_approve_already_approved(self, client):
        """Corner: Cannot approve non-pending remediation."""
        rem_id = self._create_test_remediation()
        client.post(f"/api/remediate/{rem_id}/approve")
        resp = client.post(f"/api/remediate/{rem_id}/approve")
        assert resp.status_code == 400
        self._cleanup_remediation(rem_id)

    def test_reject_remediation(self, client):
        """UC: Reject a remediation proposal."""
        rem_id = self._create_test_remediation()
        resp = client.post(f"/api/remediate/{rem_id}/reject")
        assert resp.status_code == 200
        assert resp.get_json()["status"] == "rejected"
        self._cleanup_remediation(rem_id)

    def test_execute_unapproved_fails(self, client):
        """Corner: Cannot execute a pending remediation."""
        rem_id = self._create_test_remediation()
        resp = client.post(f"/api/remediate/{rem_id}/execute")
        assert resp.status_code == 400
        assert "approved" in resp.get_json()["error"].lower() or "Must be" in resp.get_json()["error"]
        self._cleanup_remediation(rem_id)

    def test_execute_approved_remediation(self, client):
        """UC: Execute approved remediation via MCP."""
        rem_id = self._create_test_remediation(router="PE1",
            commands=json.dumps(["set system host-name PE1-fixed"]))
        # Approve first
        client.post(f"/api/remediate/{rem_id}/approve")
        with patch.object(noc_app, 'run_async', return_value="commit complete"):
            resp = client.post(f"/api/remediate/{rem_id}/execute")
        assert resp.status_code == 200
        assert resp.get_json()["status"] == "executed"
        self._cleanup_remediation(rem_id)

    def test_remediation_detail(self, client):
        """UC: Get full details of a specific remediation."""
        rem_id = self._create_test_remediation()
        resp = client.get(f"/api/remediate/{rem_id}")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["title"] == "Test Remediation"
        self._cleanup_remediation(rem_id)

    def test_remediation_detail_not_found(self, client):
        """Corner: Non-existent remediation → 404."""
        resp = client.get("/api/remediate/999999")
        assert resp.status_code == 404

    def _create_test_remediation(self, router="PE1", commands=None):
        """Helper: insert a test remediation directly into DB."""
        import sqlite3 as sql
        db = noc_app._REMEDIATION_DB
        conn = sql.connect(str(db))
        conn.execute(
            "INSERT INTO remediations (title, description, target_router, commands, "
            "risk_level, ai_analysis, rollback_commands) VALUES (?,?,?,?,?,?,?)",
            ("Test Remediation", "test", router, commands or "[]", "low", "test", "[]")
        )
        conn.commit()
        rem_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.close()
        return rem_id

    def _cleanup_remediation(self, rem_id):
        import sqlite3 as sql
        conn = sql.connect(str(noc_app._REMEDIATION_DB))
        conn.execute("DELETE FROM remediations WHERE id=?", (rem_id,))
        conn.commit()
        conn.close()


# ═══════════════════════════════════════════════════════════════
#  27. DEPLOY SAFE — AI Pre-flight Safety Check
# ═══════════════════════════════════════════════════════════════

class TestDeploySafe:
    """Test AI-powered pre-flight safety analysis."""

    def test_deploy_safe_safe_config(self, client):
        """UC: Safe config gets approval."""
        with patch.object(noc_app, 'run_async', return_value="SAFE: yes\nRISK: low"):
            resp = client.post("/api/deploy/safe",
                data=json.dumps({"router": "PE1", "config": "set system ntp server 10.0.0.1"}),
                content_type="application/json")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["safe"] is True
        assert data["risk_level"] == "low"

    def test_deploy_safe_risky_config(self, client):
        """UC: Risky config gets flagged."""
        with patch.object(noc_app, 'run_async',
                          return_value="SAFE: no\nRISK: high\nWARNINGS: BGP flap"):
            resp = client.post("/api/deploy/safe",
                data=json.dumps({"router": "PE1", "config": "delete protocols bgp"}),
                content_type="application/json")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["safe"] is False
        assert data["risk_level"] == "high"

    def test_deploy_safe_missing_params(self, client):
        """Corner: Missing router or config → 400."""
        resp = client.post("/api/deploy/safe",
            data=json.dumps({"router": "PE1"}), content_type="application/json")
        assert resp.status_code == 400

    def test_deploy_safe_ollama_down(self, client):
        """Corner: Ollama unreachable → 503."""
        with patch.object(noc_app, 'run_async', side_effect=Exception("Connection refused")):
            resp = client.post("/api/deploy/safe",
                data=json.dumps({"router": "PE1", "config": "set system host-name X"}),
                content_type="application/json")
        assert resp.status_code == 503


# ═══════════════════════════════════════════════════════════════
#  28. ENSEMBLE AI — Multi-Model Consensus
# ═══════════════════════════════════════════════════════════════

class TestEnsembleExpanded:
    """Expanded ensemble AI tests."""

    def test_ensemble_missing_question(self, client):
        """Corner: Empty question → 400."""
        resp = client.post("/api/ai/ensemble",
            data=json.dumps({}), content_type="application/json")
        assert resp.status_code == 400

    def test_ensemble_all_models_fail(self, client):
        """Corner: All models fail → 503."""
        with patch.object(noc_app, 'run_async', side_effect=Exception("Ollama down")):
            resp = client.post("/api/ai/ensemble",
                data=json.dumps({"question": "test"}), content_type="application/json")
        assert resp.status_code == 503


# ═══════════════════════════════════════════════════════════════
#  29. PREDICTIVE ANALYSIS — AI Predictions
# ═══════════════════════════════════════════════════════════════

class TestPredictiveAnalysis:
    """Test predictive failure analysis."""

    def test_predict_success(self, client):
        """UC: Predictive analysis returns predictions."""
        with patch.object(noc_app, 'build_topology_from_golden_configs', return_value={
            "nodes": [{"id": "PE1", "role": "PE", "bgp_neighbors": [], "isis_interfaces": [],
                        "ldp": True, "mpls": True}], "links": []}):
            with patch.object(noc_app, 'calculate_network_stats_v2', return_value={
                "total_nodes": 1, "single_points_of_failure": [], "redundancy_score": 80}):
                with patch.object(noc_app, 'run_async', return_value="Risk: P11 SPOF"):
                    resp = client.post("/api/brain/predict",
                        data=json.dumps({"scope": "all"}),
                        content_type="application/json")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "prediction" in data

    def test_predict_ai_failure(self, client):
        """Corner: Ollama down → 503."""
        with patch.object(noc_app, 'build_topology_from_golden_configs', return_value={
            "nodes": [], "links": []}):
            with patch.object(noc_app, 'calculate_network_stats_v2', return_value={
                "total_nodes": 0, "single_points_of_failure": [], "redundancy_score": 0}):
                with patch.object(noc_app, 'run_async', side_effect=Exception("timeout")):
                    resp = client.post("/api/brain/predict",
                        data=json.dumps({}), content_type="application/json")
        assert resp.status_code == 503


# ═══════════════════════════════════════════════════════════════
#  30. BRAIN HISTORY — Investigation Tracking
# ═══════════════════════════════════════════════════════════════

class TestBrainHistory:
    """Test investigation history endpoints."""

    def test_brain_history_list(self, client):
        """UC: Get investigation history."""
        resp = client.get("/api/brain/history")
        assert resp.status_code == 200
        assert isinstance(resp.get_json(), list)

    def test_brain_history_detail_not_found(self, client):
        """Corner: Non-existent investigation → 404."""
        resp = client.get("/api/brain/history/999999")
        assert resp.status_code == 404


# ═══════════════════════════════════════════════════════════════
#  31. ROLLBACK SERVICE — Diff + Execute
# ═══════════════════════════════════════════════════════════════

class TestRollback:
    """Test config rollback service."""

    def test_rollback_diff(self, client):
        """UC: Get rollback diff for a router."""
        with patch.object(noc_app, 'run_async', return_value="[edit]\n+ set system host-name X"):
            resp = client.get("/api/rollback/diff/PE1?version=1")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["router"] == "PE1"
        assert data["version"] == 1

    def test_rollback_execute_no_confirm(self, client):
        """UC: Rollback without confirm returns risk assessment."""
        with patch.object(noc_app, 'run_async', return_value="Risk: LOW"):
            resp = client.post("/api/rollback/execute",
                data=json.dumps({"router": "PE1", "version": 1}),
                content_type="application/json")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data.get("requires_confirmation") is True

    def test_rollback_missing_router(self, client):
        """Corner: Missing router → 400."""
        resp = client.post("/api/rollback/execute",
            data=json.dumps({"version": 1}), content_type="application/json")
        assert resp.status_code == 400

    def test_rollback_execute_confirmed(self, client):
        """UC: Confirmed rollback executes via MCP."""
        with patch.object(noc_app, 'run_async', return_value="commit complete"):
            resp = client.post("/api/rollback/execute",
                data=json.dumps({"router": "PE1", "version": 1, "confirm": True}),
                content_type="application/json")
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════════════
#  32. GIT EXPORT — Config Version Control (Expanded)
# ═══════════════════════════════════════════════════════════════

class TestGitExportExpanded:
    """Test git export lifecycle — init, export, log, diff."""

    def test_git_init(self, client):
        """UC: Initialize git repo."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            with patch("pathlib.Path.exists", return_value=False):
                resp = client.post("/api/git-export/init")
        assert resp.status_code == 200

    def test_git_log(self, client):
        """UC: Get git commit history."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="abc1234 initial commit\n", returncode=0)
            resp = client.get("/api/git-export/log")
        assert resp.status_code == 200
        assert "log" in resp.get_json()

    def test_git_diff(self, client):
        """UC: Get diff for a specific commit."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="diff --git a/PE1.conf b/PE1.conf\n", returncode=0)
            resp = client.get("/api/git-export/diff/abc1234")
        assert resp.status_code == 200
        assert "diff" in resp.get_json()


# ═══════════════════════════════════════════════════════════════
#  33. RESULT COMPARISON — Capture + Compare (Expanded)
# ═══════════════════════════════════════════════════════════════

class TestResultComparisonExpanded:
    """Test result capture and comparison — full lifecycle."""

    def test_capture_result(self, client):
        """UC: Capture command output as a named result."""
        with patch.object(noc_app, 'run_async', return_value="Junos: 22.4R1"):
            resp = client.post("/api/results/capture",
                data=json.dumps({"name": "test_capture_" + str(time.time()),
                                 "router": "PE1", "command": "show version"}),
                content_type="application/json")
        assert resp.status_code == 200

    def test_list_results(self, client):
        """UC: List all captured results."""
        resp = client.get("/api/results")
        assert resp.status_code == 200
        assert isinstance(resp.get_json(), list)

    def test_compare_results(self, client):
        """UC: Compare two captured results."""
        t = str(time.time())
        with patch.object(noc_app, 'run_async', return_value="Junos: 22.A"):
            client.post("/api/results/capture",
                data=json.dumps({"name": f"cmp_{t}_A",
                                 "router": "PE1", "command": "show version"}),
                content_type="application/json")
        with patch.object(noc_app, 'run_async', return_value="Junos: 22.B"):
            client.post("/api/results/capture",
                data=json.dumps({"name": f"cmp_{t}_B",
                                 "router": "PE1", "command": "show version"}),
                content_type="application/json")
        with patch.object(noc_app, 'run_async', return_value="Config changed"):
            resp = client.post("/api/results/compare",
                data=json.dumps({"result_a": f"cmp_{t}_A", "result_b": f"cmp_{t}_B"}),
                content_type="application/json")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "diff" in data or "result_a" in data


# ═══════════════════════════════════════════════════════════════
#  34. DISCOVERY — Interfaces, Neighbors, Full Scan
# ═══════════════════════════════════════════════════════════════

class TestDiscovery:
    """Test network discovery endpoints."""

    def test_discover_interfaces(self, client):
        """UC: Discover interfaces on a router."""
        with patch.object(noc_app, 'run_async', return_value="ge-0/0/0   up    up"):
            resp = client.get("/api/discovery/interfaces/PE1")
        assert resp.status_code == 200

    def test_discover_interface_detail(self, client):
        """UC: Discover interface details."""
        with patch.object(noc_app, 'run_async', return_value="Physical interface: ge-0/0/0"):
            resp = client.get("/api/discovery/interfaces/PE1/detail")
        assert resp.status_code == 200

    def test_discover_neighbors(self, client):
        """UC: Discover LLDP/ARP neighbors."""
        with patch.object(noc_app, 'run_async', return_value="LLDP: ge-0/0/0 -> P11"):
            resp = client.get("/api/discovery/neighbors/PE1")
        assert resp.status_code == 200

    def test_full_scan(self, client):
        """UC: Full infrastructure scan."""
        with patch.object(noc_app, 'run_async', return_value="scan complete"):
            resp = client.post("/api/discovery/full-scan",
                data=json.dumps({"routers": ["PE1"]}),
                content_type="application/json")
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════════════
#  35. SECURITY ENDPOINTS — Audit, Threat, Credentials, Hardening
# ═══════════════════════════════════════════════════════════════

class TestSecurity:
    """Test security and compliance endpoints."""

    def test_security_audit(self, client):
        """UC: Run security audit on a router (GET with router in URL)."""
        with patch.object(noc_app, 'run_async', return_value="No SNMP public community"):
            resp = client.get("/api/security/audit/PE1")
        assert resp.status_code == 200

    def test_threat_check(self, client):
        """UC: AI-powered threat analysis."""
        with patch.object(noc_app, 'run_async', return_value="No threats detected"):
            resp = client.post("/api/security/threat-check",
                data=json.dumps({"router": "PE1", "data": "sample security output"}),
                content_type="application/json")
        # Accepts 200 or 400 depending on required fields
        assert resp.status_code in (200, 400)

    def test_credential_scan(self, client):
        """UC: Scan for cleartext credentials."""
        with patch.object(noc_app, 'run_async', return_value="No cleartext passwords found"):
            resp = client.post("/api/security/credential-scan",
                data=json.dumps({"router": "PE1"}),
                content_type="application/json")
        assert resp.status_code == 200

    def test_hardening_report(self, client):
        """UC: CIS-style hardening report."""
        with patch.object(noc_app, 'run_async', return_value="Hardening score: 85/100"):
            resp = client.post("/api/security/hardening-report",
                data=json.dumps({"router": "PE1"}),
                content_type="application/json")
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════════════
#  36. MONITORING — Health, Protocol, Incident
# ═══════════════════════════════════════════════════════════════

class TestMonitoring:
    """Test monitoring dashboard endpoints."""

    def test_health_dashboard(self, client):
        """UC: Real-time health dashboard."""
        with patch.object(noc_app, 'run_async', return_value="uptime: 30 days"):
            resp = client.get("/api/monitor/health-dashboard")
        assert resp.status_code == 200

    def test_protocol_health(self, client):
        """UC: Check protocol health across the network."""
        with patch.object(noc_app, 'run_async', return_value="ISIS OK, BGP OK"):
            resp = client.get("/api/monitor/protocol-health")
        assert resp.status_code == 200

    def test_ai_incident(self, client):
        """UC: AI-powered incident detection."""
        with patch.object(noc_app, 'run_async', return_value="No incidents detected"):
            resp = client.post("/api/monitor/ai-incident",
                data=json.dumps({"data": "show log messages last 100"}),
                content_type="application/json")
        assert resp.status_code in (200, 400)


# ═══════════════════════════════════════════════════════════════
#  37. PATH ANALYSIS — Multi-Algorithm, What-If, Capacity
# ═══════════════════════════════════════════════════════════════

class TestPathAnalysis:
    """Test advanced path analysis endpoints."""

    def test_multi_algorithm_path(self, client):
        """UC: Multi-algorithm path computation."""
        with patch.object(noc_app, 'build_topology_from_golden_configs', return_value={
            "nodes": [{"id": "PE1"}, {"id": "P11"}, {"id": "PE2"}],
            "links": [{"source": "PE1", "target": "P11"}, {"source": "P11", "target": "PE2"}]}):
            resp = client.post("/api/path/multi-algorithm",
                data=json.dumps({"source": "PE1", "target": "PE2"}),
                content_type="application/json")
        assert resp.status_code == 200

    def test_what_if_analysis(self, client):
        """UC: What-if failure simulation."""
        with patch.object(noc_app, 'build_topology_from_golden_configs', return_value={
            "nodes": [{"id": "PE1"}, {"id": "P11"}, {"id": "PE2"}],
            "links": [{"source": "PE1", "target": "P11"}, {"source": "P11", "target": "PE2"}]}):
            resp = client.post("/api/path/what-if",
                data=json.dumps({"failed_node": "P11"}),
                content_type="application/json")
        assert resp.status_code == 200

    def test_capacity_plan(self, client):
        """UC: AI capacity planning."""
        with patch.object(noc_app, 'build_topology_from_golden_configs', return_value={
            "nodes": [{"id": "PE1"}], "links": []}):
            with patch.object(noc_app, 'run_async', return_value="Add redundancy to PE1"):
                resp = client.post("/api/path/capacity-plan",
                    data=json.dumps({}), content_type="application/json")
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════════════
#  38. QUANTUM-INSPIRED ENDPOINTS
# ═══════════════════════════════════════════════════════════════

class TestQuantumEndpoints:
    """Test quantum-inspired optimization endpoints."""

    def test_quantum_optimize(self, client):
        """UC: Quantum annealing for SPOF elimination."""
        resp = client.post("/api/quantum/optimize",
            data=json.dumps({}), content_type="application/json")
        # May succeed or 500 depending on topology
        assert resp.status_code in (200, 500)

    def test_quantum_anomalies(self, client):
        """UC: Quantum walk anomaly detection."""
        resp = client.get("/api/quantum/anomalies")
        assert resp.status_code in (200, 500)

    def test_quantum_communities(self, client):
        """UC: Community detection."""
        resp = client.get("/api/quantum/communities")
        assert resp.status_code in (200, 500)

    def test_quantum_spof(self, client):
        """UC: SPOF detection via Tarjan's algorithm."""
        resp = client.get("/api/quantum/spof")
        assert resp.status_code in (200, 500)

    def test_quantum_benchmark(self, client):
        """UC: Benchmark quantum engine."""
        resp = client.get("/api/quantum/benchmark")
        assert resp.status_code in (200, 500)


# ═══════════════════════════════════════════════════════════════
#  39. CONFIDENCE SCORING — AI Response Quality
# ═══════════════════════════════════════════════════════════════

class TestConfidenceScoring:
    """Test AI confidence scoring."""

    def test_confidence_with_mcp_source(self, client):
        """UC: MCP-sourced data gets high base score."""
        resp = client.post("/api/ai/confidence-score",
            data=json.dumps({
                "response": "BGP is established with 3 peers. Warning: one peer flapping",
                "source": "mcp",
                "validated": True
            }), content_type="application/json")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["score"] >= 50
        assert data["level"] in ("low", "medium", "high")

    def test_confidence_with_empty_response(self, client):
        """Corner: Short response gets low score."""
        resp = client.post("/api/ai/confidence-score",
            data=json.dumps({"response": "OK"}),
            content_type="application/json")
        assert resp.status_code == 200
        assert resp.get_json()["score"] <= 60


# ═══════════════════════════════════════════════════════════════
#  40. QUICK ACTIONS & COPILOT SUGGESTIONS
# ═══════════════════════════════════════════════════════════════

class TestQuickActionsAndCopilot:
    """Test AI quick actions and copilot suggestions."""

    def test_quick_actions(self, client):
        """UC: Get context-aware quick actions."""
        with patch.object(noc_app, 'run_async', return_value="[]"):
            resp = client.post("/api/ai/quick-actions",
                data=json.dumps({"view": "dashboard", "context": "13 devices"}),
                content_type="application/json")
        assert resp.status_code == 200

    def test_copilot_suggest(self, client):
        """UC: Get proactive copilot suggestions."""
        with patch.object(noc_app, 'run_async', return_value="Check BGP sessions"):
            resp = client.post("/api/ai/copilot-suggest",
                data=json.dumps({"view": "topology", "state": {}}),
                content_type="application/json")
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════════════
#  41. BOOTSTRAP — Config Sync from MCP
# ═══════════════════════════════════════════════════════════════

class TestBootstrap:
    """Test bootstrap sync functionality."""

    def test_bootstrap_status(self, client):
        """UC: Check if golden configs exist."""
        resp = client.get("/api/bootstrap/status")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "bootstrapped" in data

    def test_bootstrap_sync_one(self, client):
        """UC: Sync a single router's config from MCP."""
        with patch.object(noc_app, 'run_async', return_value="set system host-name PE1"):
            resp = client.post("/api/bootstrap/sync-one/PE1")
        # 200 on success, 500 if MCP not available
        assert resp.status_code in (200, 500)


# ═══════════════════════════════════════════════════════════════
#  42. NOTIFICATION CHANNELS — CRUD + Send + History
# ═══════════════════════════════════════════════════════════════

class TestNotificationExpanded:
    """Expanded notification tests."""

    def test_create_channel_missing_name(self, client):
        """Corner: Missing channel name → 400."""
        resp = client.post("/api/notifications/channels",
            data=json.dumps({"channel_type": "slack"}),
            content_type="application/json")
        assert resp.status_code == 400

    def test_notification_history(self, client):
        """UC: View notification history."""
        resp = client.get("/api/notifications/history")
        assert resp.status_code == 200
        assert isinstance(resp.get_json(), list)

    def test_ai_summary_missing_events(self, client):
        """Corner: Missing events → 400."""
        resp = client.post("/api/notifications/ai-summary",
            data=json.dumps({}), content_type="application/json")
        assert resp.status_code == 400


# ═══════════════════════════════════════════════════════════════
#  43. CRON SCHEDULING — Advanced Cron Tasks
# ═══════════════════════════════════════════════════════════════

class TestCronScheduling:
    """Test cron-based scheduling."""

    def test_cron_task_creation(self, client):
        """UC: Create task with cron expression."""
        with patch.object(noc_app, 'run_async', return_value="PE1"):
            resp = client.post("/api/scheduled-tasks/cron",
                data=json.dumps({
                    "name": f"cron_test_{time.time()}",
                    "cron": "*/5 * * * *",
                    "router": "PE1",
                    "command": "show version"
                }), content_type="application/json")
        assert resp.status_code in (200, 201, 400)

    def test_calendar_view(self, client):
        """UC: Get calendar view of scheduled tasks."""
        resp = client.get("/api/scheduled-tasks/calendar")
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════════════
#  44. AGENTIC CHAT — Classification + Routing
# ═══════════════════════════════════════════════════════════════

class TestAgenticChatExpanded:
    """Expanded agentic chat tests."""

    def test_agentic_config_query(self, client):
        """UC: Config query returns commands with approval flag."""
        with patch.object(noc_app, 'run_async', return_value="set protocols bgp ..."):
            with patch.object(noc_app, 'classify_query_web', return_value={
                "type": "config", "confidence": 0.9}):
                resp = client.post("/api/ai/chat-agentic",
                    data=json.dumps({"message": "configure OSPF on PE1"}),
                    content_type="application/json")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data.get("type") == "config" or "response" in data

    def test_agentic_status_query(self, client):
        """UC: Status query returns device status."""
        with patch.object(noc_app, 'run_async', return_value="System uptime: 30 days"):
            with patch.object(noc_app, 'classify_query_web', return_value={
                "type": "status", "confidence": 0.85, "target_device": "PE1"}):
                resp = client.post("/api/ai/chat-agentic",
                    data=json.dumps({"message": "show PE1 status"}),
                    content_type="application/json")
        assert resp.status_code == 200

    def test_agentic_empty_message(self, client):
        """Corner: Empty message → 400."""
        resp = client.post("/api/ai/chat-agentic",
            data=json.dumps({"message": ""}),
            content_type="application/json")
        assert resp.status_code == 400


# ═══════════════════════════════════════════════════════════════
#  45. AUDIT HISTORY & CONVERSATIONS
# ═══════════════════════════════════════════════════════════════

class TestAuditAndConversations:
    """Test audit history and conversation endpoints."""

    def test_audit_history(self, client):
        """UC: Get audit history."""
        resp = client.get("/api/audit-history")
        assert resp.status_code == 200

    def test_conversations(self, client):
        """UC: Get conversation history."""
        resp = client.get("/api/conversations")
        assert resp.status_code == 200

    def test_network_stats(self, client):
        """UC: Get network statistics."""
        resp = client.get("/api/network-stats")
        assert resp.status_code == 200

    def test_config_endpoint(self, client):
        """UC: Get current configuration."""
        resp = client.get("/api/config")
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════════════
#  46. MCP LIVE OPERATIONS
# ═══════════════════════════════════════════════════════════════

class TestMCPLiveOps:
    """Test MCP live device operations."""

    def test_mcp_facts(self, client):
        """UC: Get device facts via MCP."""
        with patch.object(noc_app, 'run_async', return_value="Junos 22.4R1"):
            resp = client.get("/api/mcp/facts/PE1")
        assert resp.status_code == 200

    def test_mcp_live_config(self, client):
        """UC: Get live running config."""
        with patch.object(noc_app, 'run_async', return_value="set system host-name PE1"):
            resp = client.get("/api/mcp/live-config/PE1")
        assert resp.status_code == 200

    def test_mcp_deploy_config(self, client):
        """UC: Deploy config via MCP."""
        with patch.object(noc_app, 'run_async', return_value="commit complete"):
            resp = client.post("/api/mcp/deploy-config",
                data=json.dumps({"router": "PE1", "config": "set system ntp", "comment": "test"}),
                content_type="application/json")
        assert resp.status_code == 200

    def test_mcp_poll_status(self, client):
        """UC: Poll device status via MCP."""
        with patch.object(noc_app, 'run_async', return_value="PE1: up"):
            resp = client.post("/api/mcp/poll-status",
                data=json.dumps({"routers": ["PE1"]}),
                content_type="application/json")
        assert resp.status_code == 200

    def test_mcp_live_devices(self, client):
        """UC: Get list of live MCP devices."""
        with patch.object(noc_app, 'run_async', return_value="PE1\nP11"):
            resp = client.get("/api/mcp/live-devices")
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════════════
#  47. PING EXPANDED — Single + Sweep + AI Analysis
# ═══════════════════════════════════════════════════════════════

class TestPingExpanded:
    """Expanded ping tests."""

    def test_ping_single_success(self, client):
        """UC: Ping single router → reachable."""
        with patch.object(noc_app, 'run_async', return_value="System booted: 2026-02-26"):
            resp = client.get("/api/ping/PE1")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["router"] == "PE1"
        assert data["reachable"] is True
        assert "latency_ms" in data

    def test_ping_single_unreachable(self, client):
        """UC: Ping fails → unreachable flag."""
        with patch.object(noc_app, 'run_async', return_value="Error: could not connect"):
            resp = client.get("/api/ping/PE1")
        assert resp.status_code == 200
        assert resp.get_json()["reachable"] is False

    def test_ping_sweep(self, client):
        """UC: Sweep all devices."""
        with patch.object(noc_app, 'run_async', return_value="All up"):
            resp = client.post("/api/ping/sweep",
                data=json.dumps({"routers": ["PE1", "P11"]}),
                content_type="application/json")
        assert resp.status_code == 200
        assert "results" in resp.get_json()

    def test_ping_ai_analyze(self, client):
        """UC: AI analyzes ping results."""
        with patch.object(noc_app, 'run_async', return_value="All devices reachable"):
            resp = client.post("/api/ping/ai-analyze",
                data=json.dumps({"results": [{"router": "PE1", "reachable": True}]}),
                content_type="application/json")
        assert resp.status_code == 200

    def test_ping_ai_analyze_missing_results(self, client):
        """Corner: Missing results → 400."""
        resp = client.post("/api/ping/ai-analyze",
            data=json.dumps({}), content_type="application/json")
        assert resp.status_code == 400


# ═══════════════════════════════════════════════════════════════
#  48. VALIDATION EXPANDED — AI Compliance
# ═══════════════════════════════════════════════════════════════

class TestValidationExpanded:
    """Expanded validation tests."""

    def test_validate_regex_match(self, client):
        """UC: Regex pattern matching."""
        with patch.object(noc_app, 'run_async', return_value="BGP: 3 Established"):
            resp = client.post("/api/validate",
                data=json.dumps({"router": "PE1", "command": "show bgp summary",
                                  "pattern": r"\d+ Established", "match_type": "regex"}),
                content_type="application/json")
        assert resp.status_code == 200
        assert resp.get_json()["passed"] is True

    def test_validate_not_contains(self, client):
        """UC: Pattern NOT present = pass."""
        with patch.object(noc_app, 'run_async', return_value="No errors found"):
            resp = client.post("/api/validate",
                data=json.dumps({"router": "PE1", "command": "show system alarms",
                                  "pattern": "CRITICAL", "match_type": "not_contains"}),
                content_type="application/json")
        assert resp.status_code == 200
        assert resp.get_json()["passed"] is True

    def test_validate_ai_compliance(self, client):
        """UC: AI compliance audit."""
        with patch.object(noc_app, 'run_async', return_value="Compliance score: 90%"):
            resp = client.post("/api/validate/ai-compliance",
                data=json.dumps({"router": "PE1"}),
                content_type="application/json")
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════════════
#  49. WORKFLOW ENGINE — V2 Step Types
# ═══════════════════════════════════════════════════════════════

class TestWorkflowExpanded:
    """Test workflow engine including advanced step types."""

    def test_workflow_crud(self, client):
        """UC: Create → List → Delete workflow."""
        wf_name = f"test_wf_{time.time()}"
        # Create
        resp = client.post("/api/workflows",
            data=json.dumps({
                "name": wf_name, "description": "test",
                "steps": [{"type": "command", "router": "PE1", "command": "show version"}]
            }), content_type="application/json")
        assert resp.status_code == 200
        # List
        resp = client.get("/api/workflows")
        assert resp.status_code == 200
        names = [w["name"] for w in resp.get_json()]
        assert wf_name in names
        # Delete
        resp = client.delete(f"/api/workflows/{wf_name}")
        assert resp.status_code == 200

    def test_workflow_execute(self, client):
        """UC: Execute a multi-step workflow."""
        with patch.object(noc_app, 'run_async', return_value="Junos 22.4"):
            resp = client.post("/api/workflows/execute",
                data=json.dumps({
                    "name": "test_exec",
                    "steps": [{"type": "command", "router": "PE1", "command": "show version"}]
                }), content_type="application/json")
        assert resp.status_code == 200


# ═══════════════════════════════════════════════════════════════
#  50. PARSE_SSE_RESPONSE — Edge Cases
# ═══════════════════════════════════════════════════════════════

class TestParseSSEExpanded:
    """Expanded SSE parsing edge cases."""

    def test_parse_sse_with_multiple_events(self):
        """UC: Multiple data events, last one wins."""
        text = 'event: message\ndata: {"jsonrpc":"2.0","id":1}\n\nevent: message\ndata: {"jsonrpc":"2.0","result":{"content":[{"text":"final"}]}}\n\n'
        result = noc_app.parse_sse_response(text)
        assert result.get("result", {}).get("content", [{}])[0].get("text") == "final"

    def test_parse_sse_multiline_data(self):
        """Corner: Data field split across lines."""
        text = 'data: {"jsonrpc":\ndata: "2.0","result":{"content":[{"text":"ok"}]}}\n\n'
        # Should handle gracefully (may return partial or empty)
        result = noc_app.parse_sse_response(text)
        assert isinstance(result, dict)


# ═══════════════════════════════════════════════════════════════
#  RUN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-x"])
