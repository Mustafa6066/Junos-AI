# 🧠🚀 Junos AI NOC — Master Upgrade Plan v2.0

## From "Smart Chat" → "Autonomous Agentic AI NOC"

**Date:** 2025  
**Current Version:** v21.2  
**Target Version:** v30.0  
**Total Lines Today:** ~33,000+ across 8 major files  
**Philosophy:** Make the AI a **true autonomous network engineer** that can think, investigate, act, and learn — with a UI that makes every capability visible and controllable.

---

## Table of Contents

1. [Current State Gap Analysis](#1-current-state-gap-analysis)
2. [Phase 1: Bridge the Brain to the Web (v22–v23)](#phase-1-bridge-the-brain-to-the-web-v22v23)
3. [Phase 2: Agentic UI Revolution (v24–v25)](#phase-2-agentic-ui-revolution-v24v25)
4. [Phase 3: AI Intelligence Leap (v26–v27)](#phase-3-ai-intelligence-leap-v26v27)
5. [Phase 4: Full Autonomy (v28–v30)](#phase-4-full-autonomy-v28v30)
6. [Architecture Diagrams](#5-architecture-diagrams)
7. [File-by-File Change Map](#6-file-by-file-change-map)
8. [Implementation Priority Matrix](#7-implementation-priority-matrix)
9. [Risk Mitigation](#8-risk-mitigation)

---

## 1. Current State Gap Analysis

### What We Have (Strengths)

| Component | Lines | Capability |
|-----------|-------|-----------|
| `hypered_brain.py` | 1,963 | 6-layer agentic pipeline: Perception→Execution→Analysis→Probing→Validation→Synthesis |
| `reasoning_engine.py` | 1,488 | 7-stage chain-of-thought: Classify→Decompose→Hypothesize→Investigate→Diagnose→Synthesize→Prescribe |
| `ollama_mcp_client.py` | 14,191 | Full terminal AI client with 170+ enhancements, feedback learning, conversation memory |
| `quantum_engine.py` | 906 | TarjanSPOF, QuantumAnnealing, LouvainCommunity, QuantumWalk anomaly detection |
| `network_analysis.py` | 2,149 | 8 modules: Packet Capture, DNS Intel, Security Audit, Flow, Alerts, Forensics, Profiler, Memory |
| `app.py` | 3,623 | 101 API routes, 6 WebSocket events, full Flask backend |
| `noc.js` | 2,595 | D3.js topology, streaming AI chat, copilot sidebar, 21 views, workflow builder |
| `kb_vectorstore.py` | 818 | RAG engine with heading-anchored embeddings, multi-query retrieval, keyword boosting |
| 18 Smart Scripts | — | intf_health, ospf/isis/bgp/ldp state+deep, system_health, vpn, security, topology, perf, route_validation |

### The Critical Gaps ⚠️

| Gap | Impact | Root Cause |
|-----|--------|-----------|
| **Hypered Brain is terminal-only** | The 6-layer agentic architecture (1,963 lines) is INACCESSIBLE from the Web UI | No API endpoints expose `hypered_brain_analyze()` |
| **Reasoning Engine is terminal-only** | The 7-stage pipeline never runs in web mode | No integration between `reasoning_engine.py` and `app.py` |
| **Web AI is text-only chat** | No tool calling from browser, no MCP execution from chat, no investigation progress | `ollama_chat_async()` in app.py is basic text Q&A — no tool loop |
| **No investigation visualization** | Users can't see multi-pass analysis, fact gathering, anomaly detection, confidence scoring | No WebSocket events for brain state updates |
| **AI Quick Actions are hardcoded** | Only 8 static actions in copilot sidebar | Not dynamic, not context-aware, not AI-generated |
| **No structured output** | Ollama integration uses raw text, no JSON mode, no function calling | Missing `format: json` and tool definitions in Ollama calls |
| **No feedback loop in web** | Terminal client has `FeedbackLearningEngine` — web has nothing | Learning engine not exposed via API |
| **No agentic workflows** | Workflow builder is manual-only, AI can't generate or suggest workflows | No AI-driven workflow creation |
| **FactAccumulator web-blind** | Deduplication, contradiction detection, anomaly matrix exist but invisible | No API to surface accumulated facts |
| **Smart Scripts not selectable** | Users can't pick/customize which scripts run in the brain | Script library is internal to hypered_brain.py |

### The Core Problem Statement

> **The most powerful AI capabilities (Hypered Brain, Reasoning Engine, Smart Scripts, FactAccumulator, AdaptiveConcurrency, AIProbe) exist ONLY in the terminal client. The Web UI has a beautiful shell with a basic text chatbot inside it.**

---

## Phase 1: Bridge the Brain to the Web (v22–v23)

### Goal: Expose the terminal-only AI power through the web interface

---

### 1.1 Hypered Brain API Endpoints (v22.0)

**What:** Create API routes that expose `hypered_brain_analyze()` and `quick_brain_analyze()` to the web UI.

**New Routes in `app.py`:**

```python
# ── Hypered Brain Investigation API ──────────────────────
POST /api/brain/investigate
  Body: { "query": "why is BGP down on PE1?", "mode": "full"|"quick", "devices": ["PE1"] }
  Returns: SSE stream of brain events (WebSocket alternative below)

GET  /api/brain/state
  Returns: Current BrainState (layer, facts count, confidence, pass number)

GET  /api/brain/scripts
  Returns: List of all 18 SmartScripts with categories, commands, dependencies

POST /api/brain/scripts/select
  Body: { "query": "BGP issues" }
  Returns: Selected scripts for the query + reasons

GET  /api/brain/facts
  Returns: Current FactAccumulator state (facts, anomaly matrix, contradictions)

POST /api/brain/probe
  Body: { "device": "PE1", "command": "show bgp neighbor", "reason": "verify session" }
  Returns: Probe result

WS   brain_progress
  Emits: { layer, pass, script_running, facts_gathered, confidence, anomalies }
```

**Implementation Details:**

```python
# In app.py — add brain integration
from hypered_brain import hypered_brain_analyze, quick_brain_analyze, SMART_SCRIPTS

@app.route("/api/brain/investigate", methods=["POST"])
async def api_brain_investigate():
    """Run full Hypered Brain investigation with real-time progress via WebSocket."""
    data = request.json or {}
    query = data.get("query", "")
    mode = data.get("mode", "full")
    devices = data.get("devices", [])
    
    # Progress callback that emits WebSocket events
    def progress_callback(event):
        socketio.emit("brain_progress", event)
    
    if mode == "quick":
        result = await quick_brain_analyze(query, mcp_execute_command, ollama_chat_async, devices)
    else:
        result = await hypered_brain_analyze(query, mcp_execute_command, ollama_chat_async, 
                                              devices, progress_callback=progress_callback)
    return jsonify(result)
```

**Changes to `hypered_brain.py`:**
- Add optional `progress_callback` parameter to `hypered_brain_analyze()` 
- Emit events at each layer transition: `{"layer": "perception", "scripts_selected": 5, ...}`
- Emit events for each script execution: `{"script": "bgp_state", "device": "PE1", "status": "running"}`
- Emit events for fact accumulation: `{"facts_total": 23, "anomalies": 2, "contradictions": 0}`
- Emit events for confidence updates: `{"confidence": 0.72, "pass": 2, "gaps": ["ldp_deep needed"]}`

---

### 1.2 Reasoning Engine API (v22.0)

**What:** Expose the 7-stage reasoning pipeline through the web.

**New Routes:**

```python
POST /api/reasoning/analyze
  Body: { "problem": "PE1 can't reach PE3 via MPLS", "context": {...} }
  Returns: SSE stream of reasoning stages

GET  /api/reasoning/hypotheses
  Returns: Current hypothesis tree with probabilities

POST /api/reasoning/classify
  Body: { "query": "BGP flapping on PE1" }
  Returns: { domain, complexity, protocol, devices, osi_layer, keywords }
```

---

### 1.3 Agentic Chat — Tool Calling from Browser (v22.0)

**The Big One.** Transform the web chat from text-only to full agentic mode.

**Current Flow (Broken):**
```
User types → POST /api/ai/chat → ollama raw text → response displayed
```

**Target Flow (Agentic):**
```
User types → POST /api/ai/chat-agentic
  → Query classification (knowledge/status/troubleshoot/config)
  → If knowledge: RAG retrieval → direct answer
  → If status/troubleshoot: 
    → Hypered Brain investigate (with WebSocket progress)
    → AI selects MCP tools to call
    → Tool results streamed back to UI
    → Multi-pass reasoning with confidence gating
    → Final synthesis with remediation
  → If config: Safety gate → template selection → preview → deploy with approval
```

**New Route:**

```python
@app.route("/api/ai/chat-agentic", methods=["POST"])
def api_ai_chat_agentic():
    """Full agentic AI chat with tool calling, investigation, and MCP execution."""
    data = request.json or {}
    message = data.get("message", "")
    conversation_id = data.get("conversation_id", str(uuid4()))
    
    # 1. Classify the query
    classification = classify_query(message)
    socketio.emit("ai_thinking", {"stage": "classifying", "result": classification})
    
    # 2. Route based on classification
    if classification["type"] == "knowledge":
        # RAG-only path — fast
        chunks = await kb_store.retrieve(message, top_k=5)
        context = "\n".join([c["text"] for c in chunks])
        response = await ollama_chat_async(message, context=context)
        return jsonify({"response": response, "type": "knowledge", "sources": chunks})
    
    elif classification["type"] in ("status", "troubleshoot"):
        # Agentic investigation path
        devices = classification.get("devices", [])
        
        # Emit: "Starting investigation..."
        socketio.emit("ai_thinking", {"stage": "investigating", "devices": devices})
        
        # Run Hypered Brain
        brain_result = await hypered_brain_analyze(
            message, mcp_execute_command, ollama_chat_async, devices,
            progress_callback=lambda e: socketio.emit("brain_progress", e)
        )
        
        return jsonify({
            "response": brain_result["synthesis"],
            "type": "investigation",
            "facts": brain_result["facts"],
            "confidence": brain_result["confidence"],
            "passes": brain_result["passes"],
            "anomalies": brain_result["anomalies"],
            "scripts_run": brain_result["scripts_run"]
        })
    
    elif classification["type"] == "config":
        # Config safety path with approval gate
        socketio.emit("ai_thinking", {"stage": "config_analysis"})
        # ... config impact simulation, template matching, preview generation
```

---

### 1.4 WebSocket Brain Events (v22.0)

**What:** Real-time event stream from the brain to the UI during investigations.

**Event Types:**

| Event | Payload | When |
|-------|---------|------|
| `ai_thinking` | `{stage, message}` | Query classified, investigation starting |
| `brain_progress` | `{layer, pass, total_passes}` | Layer transitions |
| `script_running` | `{script_name, device, category}` | Each smart script starts |
| `script_complete` | `{script_name, device, facts_found, duration_ms}` | Script finishes |
| `fact_accumulated` | `{fact_summary, total_facts, anomalies}` | New fact added |
| `probe_executing` | `{device, command, reason}` | AI-directed probe |
| `confidence_update` | `{confidence, pass, gaps}` | Confidence gating check |
| `synthesis_ready` | `{summary, recommendations}` | Final answer ready |
| `tool_called` | `{tool, args, result_preview}` | MCP tool execution |

---

### 1.5 RAG Integration in Web (v23.0)

**What:** Connect `kb_vectorstore.py` to the web backend so AI chat benefits from the knowledge base.

**Current State:** The KB vector store (818 lines) is only used by `ollama_mcp_client.py`. The web backend's `ollama_chat_async()` has NO RAG integration.

**Implementation:**

```python
# In app.py — add at startup
from kb_vectorstore import KBVectorStore

kb_store = None

@app.before_first_request
async def init_kb():
    global kb_store
    kb_store = await KBVectorStore.create()

# In the agentic chat handler — inject RAG context
relevant_chunks = await kb_store.retrieve(message, top_k=3)
rag_context = "REFERENCE KNOWLEDGE:\n" + "\n---\n".join([c["text"] for c in relevant_chunks])
# Inject into the system prompt or user message
```

---

## Phase 2: Agentic UI Revolution (v24–v25)

### Goal: Transform the UI from "dashboard viewer" to "AI command center"

---

### 2.1 Investigation Dashboard Panel (v24.0)

**What:** A dedicated investigation view that shows the brain working in real-time.

**UI Components:**

```
┌─────────────────────────────────────────────────────────────────┐
│ 🧠 AI Investigation — "Why is BGP down on PE1?"                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────── Pipeline Progress ─────────────┐                │
│  │ ✅ Perception  → ✅ Execution → 🔄 Analysis │                │
│  │ ⬜ Probing    → ⬜ Validation → ⬜ Synthesis │                │
│  │ Pass 2 of 3        Confidence: 72%          │                │
│  └─────────────────────────────────────────────┘                │
│                                                                 │
│  ┌─── Scripts Running ───┐  ┌─── Facts Gathered ───────┐      │
│  │ ✅ bgp_state     PE1  │  │ 📌 PE1 BGP: 0/2 Establ  │      │
│  │ ✅ bgp_deep      PE1  │  │ 📌 PE1→P11: TCP rst     │      │
│  │ 🔄 isis_state    PE1  │  │ ⚠️  PE1 lo0: no filter  │      │
│  │ ⬜ intf_health   PE1  │  │ 🔴 Contradiction: ...    │      │
│  │ ⬜ ldp_mpls      PE1  │  │                          │      │
│  └───────────────────────┘  └──────────────────────────┘      │
│                                                                 │
│  ┌─── AI Probes (Agentic) ──────────────────────────────┐      │
│  │ 🔍 "show bgp neighbor 10.255.255.11 detail" on PE1   │      │
│  │    Reason: Verify hold-time and last-error             │      │
│  │    Result: Hold-time expired, peer unreachable         │      │
│  └───────────────────────────────────────────────────────┘      │
│                                                                 │
│  ┌─── Anomaly Matrix ───────────────────────────────────┐      │
│  │ Device  │ BGP │ ISIS │ LDP │ INTF │ Overall          │      │
│  │ PE1     │ 🔴  │  ✅  │ ⚠️  │  ✅  │ CRITICAL        │      │
│  │ P11     │ ✅  │  ✅  │ ✅  │  ✅  │ HEALTHY         │      │
│  └───────────────────────────────────────────────────────┘      │
│                                                                 │
│  ┌─── Synthesis ────────────────────────────────────────┐      │
│  │ Root Cause: BGP hold-timer expired on PE1→10.255...   │      │
│  │ Impact: L3VPN traffic for VPN-A rerouting via PE3     │      │
│  │ Fix: clear bgp neighbor 10.255.255.11 (or check lo0)  │      │
│  │                                                        │      │
│  │ [🔧 Apply Fix]  [📋 Create Runbook]  [📊 Full Report] │      │
│  └────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

**Implementation in `noc.js`:**
- New `renderInvestigationDashboard()` function
- Listen to WebSocket events: `brain_progress`, `script_running`, `fact_accumulated`, etc.
- Animated pipeline progress bar (6 layers)
- Live-updating fact list with color-coded severity
- Anomaly matrix as a heatmap table
- Collapsible sections for each brain layer

---

### 2.2 Agentic Chat Upgrade (v24.0)

**What:** Transform the chat panel from text-only to a full agentic interface.

**New Chat Features:**

1. **Tool Call Visualization**
   - When AI calls MCP tools, show them inline:
   ```
   🤖 AI: Let me check BGP on PE1...
   
   ┌─ 🔧 Tool Call ──────────────────────────┐
   │ execute_junos_command                     │
   │ Router: PE1                               │
   │ Command: show bgp summary                 │
   │ ⏱️ 1.2s  ✅ Success                      │
   │ ▼ Show Output                             │
   └───────────────────────────────────────────┘
   
   🤖 AI: BGP has 2 peers, 1 is Established and 1 is Active...
   ```

2. **Thinking Indicators**
   - Show what the AI is doing: "🧠 Classifying query...", "📊 Running 5 scripts on PE1...", "🔍 AI Probe: checking hold-timer..."

3. **Confidence Badge**
   - Show confidence level on each response: `[Confidence: 87% — High]`

4. **Action Buttons on Responses**
   - `[🔧 Apply Fix]` — Execute the suggested remediation
   - `[📋 Save as Runbook]` — Convert the investigation into a reusable runbook
   - `[🔄 Dig Deeper]` — Run another pass with the brain
   - `[📊 Full Report]` — Generate a detailed audit report
   - `[👍 / 👎]` — Feedback for the learning engine

5. **Context Cards**
   - Show the devices, protocols, and facts that were used for the response
   - Clickable to drill into topology view or config view

---

### 2.3 Dynamic Quick Actions (v24.0)

**What:** Replace the 8 hardcoded quick actions with AI-generated contextual actions.

**Current (Hardcoded):**
```javascript
const actions = [
    { label: "Health Check", view: "dashboard", action: "health" },
    // ... 7 more static actions
];
```

**Upgraded (Dynamic):**
```javascript
async function generateQuickActions(currentView, selectedDevice) {
    const response = await fetch("/api/ai/quick-actions", {
        method: "POST",
        body: JSON.stringify({
            view: currentView,
            device: selectedDevice,
            recent_alerts: currentAlerts,
            last_investigation: lastBrainResult
        })
    });
    const actions = await response.json();
    // AI returns contextual actions like:
    // - "PE1 BGP flapped 3x today — Investigate?"
    // - "Config drift detected on P11 — Run compliance check?"
    // - "ISIS adjacency down PE1↔P13 — Start diagnosis?"
    renderQuickActions(actions);
}
```

**Backend Route:**
```python
@app.route("/api/ai/quick-actions", methods=["POST"])
def api_ai_quick_actions():
    """Generate contextual AI quick actions based on current state."""
    data = request.json or {}
    view = data.get("view", "dashboard")
    device = data.get("device", "")
    alerts = data.get("recent_alerts", [])
    
    # Build context
    context = {
        "current_view": view,
        "selected_device": device,
        "active_alerts": alerts,
        "network_health": get_cached_health_state(),
        "recent_investigations": get_recent_investigations(limit=3)
    }
    
    actions = run_async(ollama_analyze_async(
        "Generate 5 contextual quick actions for a network engineer. "
        "Each action should have: label, description, action_type (investigate/check/deploy/compare), "
        "and parameters. Return as JSON array.",
        json.dumps(context),
        "Based on the current network state and view, what are the most useful actions?"
    ))
    return jsonify(json.loads(actions))  # Parse AI JSON response
```

---

### 2.4 Approval Gates & Safety UI (v25.0)

**What:** For any destructive action (config deploy, rollback, clear commands), show a visual approval gate.

**UI Component:**
```
┌─── ⚠️ Action Requires Approval ─────────────────────┐
│                                                       │
│  Action: Deploy BGP config to PE1                     │
│                                                       │
│  ┌── Config Preview ──────────────────────────────┐  │
│  │ set protocols bgp group IBGP neighbor 10.255.. │  │
│  │ set protocols bgp group IBGP local-as 65000    │  │
│  └────────────────────────────────────────────────┘  │
│                                                       │
│  ┌── AI Risk Assessment ──────────────────────────┐  │
│  │ Risk: LOW                                       │  │
│  │ Impact: Adds new BGP peer, no existing change   │  │
│  │ Rollback: Automatic if commit fails             │  │
│  └────────────────────────────────────────────────┘  │
│                                                       │
│  [✅ Approve & Deploy]    [❌ Cancel]    [📝 Edit]   │
└───────────────────────────────────────────────────────┘
```

---

### 2.5 Copilot Sidebar v2 — Full Agentic Panel (v25.0)

**What:** Upgrade the copilot sidebar from a mini-chat to a full agentic control center.

**New Sidebar Sections:**

1. **🧠 Brain Status** — Shows if an investigation is running, which layer, confidence
2. **📊 Network Pulse** — Live health indicators (green/yellow/red per protocol)
3. **🔔 Active Alerts** — Proactive alerts from background monitoring
4. **📋 Recent Actions** — Last 5 actions taken by the AI (with undo option)
5. **💡 AI Suggestions** — Context-aware suggestions based on current view
6. **🔧 Quick Tools** — Dynamic quick actions (from §2.3)
7. **📝 Investigation History** — Past brain investigations with replay option
8. **🎯 Confidence Meter** — Real-time confidence gauge

---

### 2.6 Topology Integration with Brain (v25.0)

**What:** When the brain runs an investigation, highlight affected devices/links on the topology map in real-time.

**Implementation:**
- During investigation, emit `topology_highlight` WebSocket events
- Pulse affected nodes red/yellow
- Show the investigation path on the topology (which devices were queried)
- After synthesis, color-code nodes by health status from the investigation

---

## Phase 3: AI Intelligence Leap (v26–v27)

### Goal: Make the AI dramatically smarter and more accurate

---

### 3.1 Structured Output / JSON Mode (v26.0)

**What:** Upgrade Ollama integration to use structured JSON output for reliable tool calling.

**Current Problem:** The AI returns free-form text that must be parsed with regex. This is fragile and error-prone.

**Solution:**

```python
async def ollama_chat_structured(prompt: str, schema: dict) -> dict:
    """Call Ollama with JSON mode for structured output."""
    response = await httpx.post(f"{OLLAMA_URL}/api/chat", json={
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "format": schema,  # JSON schema for structured output
        "options": {"temperature": 0.1}
    })
    return response.json()["message"]["content"]  # Guaranteed JSON

# Example: Tool selection
tools_schema = {
    "type": "object",
    "properties": {
        "tools_to_call": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "tool": {"type": "string", "enum": ["execute_command", "get_config", "get_facts"]},
                    "router": {"type": "string"},
                    "command": {"type": "string"},
                    "reason": {"type": "string"}
                }
            }
        }
    }
}
```

---

### 3.2 Multi-Model Ensemble (v26.0)

**What:** Use different models for different tasks to maximize accuracy.

**Strategy:**

| Task | Model | Why |
|------|-------|-----|
| Query classification | `gpt-oss` (fast) | Simple classification, low latency |
| RAG retrieval | `nomic-embed-text` | Already using for embeddings |
| Protocol analysis | `gpt-oss` (precise, temp=0.05) | Needs exact Junos knowledge |
| Root cause synthesis | `gpt-oss` (creative, temp=0.3) | Needs creative reasoning |
| Config generation | `gpt-oss` (strict, temp=0.0) | Must be syntactically perfect |
| Risk assessment | `gpt-oss` (balanced, temp=0.15) | Needs judgment |

**Implementation:**
```python
MODEL_PROFILES = {
    "classify": {"model": "gpt-oss", "temperature": 0.1, "top_p": 0.8},
    "analyze":  {"model": "gpt-oss", "temperature": 0.05, "top_p": 0.9},
    "reason":   {"model": "gpt-oss", "temperature": 0.3, "top_p": 0.95},
    "config":   {"model": "gpt-oss", "temperature": 0.0, "top_p": 0.8},
    "assess":   {"model": "gpt-oss", "temperature": 0.15, "top_p": 0.9},
}
```

---

### 3.3 Memory Architecture Upgrade (v26.0)

**What:** Give the web AI persistent memory across sessions — not just conversation history.

**Memory Layers:**

```
┌─────────────────────────────────────────────┐
│ Layer 1: Working Memory (per-session)       │
│   - Current conversation                     │
│   - Active investigation state               │
│   - Last tool results                        │
├─────────────────────────────────────────────┤
│ Layer 2: Short-Term Memory (SQLite)          │
│   - Last 50 conversations with summaries     │
│   - Recent investigations with outcomes      │
│   - Device health snapshots (last 24 hours)  │
├─────────────────────────────────────────────┤
│ Layer 3: Long-Term Memory (knowledge store)  │
│   - Lessons learned (from feedback)          │
│   - Resolved issues → fix patterns           │
│   - Network baselines (what "normal" looks)  │
│   - User preferences and patterns            │
├─────────────────────────────────────────────┤
│ Layer 4: Institutional Memory (KB + RAG)     │
│   - KNOWLEDGE_BASE.md (5,270 lines)          │
│   - EXPERT_EXAMPLES.md (19 walkthroughs)     │
│   - JUNOS_DEEP_KNOWLEDGE.md                  │
│   - Ingested PDF knowledge                   │
└─────────────────────────────────────────────┘
```

**New SQLite Tables:**

```sql
CREATE TABLE ai_memory (
    id INTEGER PRIMARY KEY,
    memory_type TEXT,        -- 'lesson', 'pattern', 'baseline', 'preference'
    category TEXT,           -- 'bgp', 'ospf', 'general', etc.
    content TEXT,            -- The memory content
    confidence REAL,         -- How reliable is this memory (0-1)
    access_count INTEGER,    -- How often retrieved
    last_accessed TEXT,      -- For LRU eviction
    created_at TEXT,
    source TEXT              -- 'user_feedback', 'investigation', 'observation'
);

CREATE TABLE investigation_history (
    id INTEGER PRIMARY KEY,
    query TEXT,
    classification TEXT,
    devices TEXT,
    scripts_run TEXT,
    facts_gathered INTEGER,
    confidence REAL,
    synthesis TEXT,
    duration_ms INTEGER,
    user_feedback TEXT,      -- 'helpful', 'wrong', 'partially_correct'
    created_at TEXT
);
```

---

### 3.4 Feedback Learning in Web (v26.0)

**What:** Port the terminal client's `FeedbackLearningEngine` to the web UI.

**How it works:**

1. Every AI response gets a 👍/👎 button
2. On 👎: "What was wrong?" → captures the correction
3. On 👍: Reinforces the approach for similar future queries
4. Learning is stored in `ai_memory` table with `source='user_feedback'`
5. Before each AI call, retrieve relevant memories:
   ```python
   memories = get_relevant_memories(query, category=classification["protocol"])
   if memories:
       context += "\n\nLEARNED FROM PAST EXPERIENCE:\n" + format_memories(memories)
   ```

---

### 3.5 Cross-Device Correlation Engine (v27.0)

**What:** When investigating an issue, automatically correlate data across all devices in the path.

**Current:** Brain runs scripts on explicitly-listed devices. If user says "PE1", it only checks PE1.

**Upgraded:** Brain uses topology to identify the full path and checks all devices in the blast radius.

```python
async def identify_blast_radius(device: str, issue_type: str) -> list[str]:
    """Given a device and issue, find all potentially affected devices."""
    topology = build_topology_from_golden_configs()
    adjacency = build_adjacency(topology)
    
    # Direct neighbors
    neighbors = adjacency.get(device, [])
    
    # For BGP issues: check all BGP peers
    if issue_type in ("bgp", "routing"):
        bgp_peers = get_bgp_peers_from_config(device)
        neighbors.extend(bgp_peers)
    
    # For MPLS/LDP issues: check all LSP paths
    if issue_type in ("mpls", "ldp", "l3vpn"):
        lsp_paths = get_lsp_paths(device, topology)
        neighbors.extend(lsp_paths)
    
    return list(set(neighbors))
```

---

### 3.6 Hypothesis-Driven Investigation (v27.0)

**What:** Instead of running all relevant scripts, the AI forms hypotheses and tests them strategically.

**Flow:**
```
1. AI classifies problem → "BGP session flapping"
2. Generates ranked hypotheses:
   H1 (60%): Hold-timer expiring due to CPU overload
   H2 (25%): Interface flapping causing TCP reset  
   H3 (15%): Authentication mismatch after config change
3. For each hypothesis (highest probability first):
   - Determine verification commands
   - Execute via MCP
   - Evaluate evidence: supports / contradicts / inconclusive
   - Update probabilities
4. Stop when confidence > 85% or all hypotheses tested
```

**Integration with Reasoning Engine:**
```python
# reasoning_engine.py already has the hypothesis library!
# Wire it into the brain:

from reasoning_engine import classify_problem, generate_hypotheses

async def hypothesis_driven_investigate(query, devices, mcp_func, llm_func):
    classification = classify_problem(query)
    hypotheses = generate_hypotheses(classification)
    
    for h in sorted(hypotheses, key=lambda x: x.probability, reverse=True):
        # Run verification commands
        for cmd in h.verification_commands:
            result = await mcp_func(devices[0], cmd)
            evidence = await llm_func(f"Does this evidence support hypothesis '{h.description}'?\n{result}")
            h.update_probability(evidence)
        
        if h.probability > 0.85:
            return h  # High confidence — stop here
```

---

### 3.7 Proactive Anomaly Detection (v27.0)

**What:** Background thread that continuously monitors the network and alerts the UI before the user asks.

**Implementation:**

```python
class ProactiveMonitor:
    """Background thread that runs every 5 minutes and checks for anomalies."""
    
    def __init__(self):
        self.baseline = load_network_baseline()
        self.alert_queue = asyncio.Queue()
    
    async def monitor_loop(self):
        while True:
            for device in devices:
                # Quick health check
                health = await quick_brain_analyze(f"health check {device}", ...)
                
                # Compare against baseline
                deviations = compare_to_baseline(health, self.baseline[device])
                
                if deviations:
                    alert = {
                        "device": device,
                        "deviations": deviations,
                        "severity": classify_severity(deviations),
                        "timestamp": datetime.now().isoformat()
                    }
                    self.alert_queue.put(alert)
                    socketio.emit("proactive_alert", alert)
            
            await asyncio.sleep(300)  # 5 minutes
```

**UI Integration:**
- Alert banner at the top of the page: "⚠️ PE1 BGP peer count dropped from 2 to 1 — Investigate?"
- Alert history panel in copilot sidebar
- Click-to-investigate: One click launches a full brain investigation

---

## Phase 4: Full Autonomy (v28–v30)

### Goal: AI operates autonomously with human oversight

---

### 4.1 AI-Generated Workflows (v28.0)

**What:** AI creates workflows from natural language descriptions.

**User says:** "Create a workflow that checks BGP on all PE routers every hour and alerts if any peer is down"

**AI generates:**
```json
{
  "name": "BGP Health Monitor",
  "schedule": "0 * * * *",
  "steps": [
    {"type": "batch", "command": "show bgp summary", "routers": ["PE1","PE2","PE3"]},
    {"type": "ai_analyze", "question": "Are all BGP peers Established?"},
    {"type": "condition", "check": "contains 'down' or 'Active'", 
     "on_true": "continue", "on_false": "stop"},
    {"type": "notify", "channel_id": 1, "title": "BGP Alert", 
     "message": "BGP peer down detected"}
  ]
}
```

---

### 4.2 Auto-Remediation with Approval (v28.0)

**What:** AI detects issues and proposes fixes. With approval, it deploys them.

**Flow:**
```
1. Proactive monitor detects: "PE1 LDP session down to P11"
2. Brain investigates autonomously
3. Root cause: "LDP interface not configured on ge-0/0/1"
4. AI generates fix: "set protocols ldp interface ge-0/0/1.0"
5. Simulates impact: "Low risk — adds LDP to existing P2P link"
6. Sends to UI: Approval gate with preview + risk assessment
7. User clicks "Approve" → AI deploys via MCP
8. AI verifies: "LDP session PE1↔P11 now Operational"
9. Records in lessons learned
```

---

### 4.3 Multi-Agent Collaboration (v29.0)

**What:** Specialized AI agents that collaborate on complex investigations.

**Agents:**

| Agent | Role | Specialization |
|-------|------|---------------|
| 🔍 Detective | Investigates symptoms | Runs smart scripts, gathers facts |
| 🧠 Analyst | Reasons about data | Hypothesis testing, root cause analysis |
| 🛡️ Security | Checks security posture | Credential scan, hardening assessment |
| ⚡ Performance | Analyzes performance | Traffic, capacity, bottlenecks |
| 🔧 Engineer | Generates configs | Template rendering, config safety |
| 📊 Reporter | Creates reports | Audit reports, compliance reports |

**Collaboration Protocol:**
```
User: "PE1 is having issues"

Detective → gathers data from PE1 and neighbors
Detective → passes facts to Analyst
Analyst → forms hypotheses, requests more data from Detective
Analyst → identifies security concern, routes to Security agent
Security → finds cleartext SNMP community, reports back
Analyst → synthesizes root cause + security finding
Engineer → generates remediation config
Reporter → creates incident report
```

---

### 4.4 Natural Language Network Programming (v29.0)

**What:** Users describe what they want in plain English, AI translates to Junos config.

**Examples:**

| User Says | AI Generates |
|-----------|-------------|
| "Add PE1 to the IBGP mesh" | Full BGP config with all existing peers + new PE1 sessions |
| "Create a VPN called CUSTOMER-A between PE1 and PE3" | Complete L3VPN config on both PEs with RD/RT |
| "Enable MPLS fast-reroute on all core links" | RSVP FRR config for every P-P and P-PE link |
| "Harden all routers" | System hardening template deployed to all routers |

---

### 4.5 Conversation Intelligence (v30.0)

**What:** AI understands context deeply across conversations and proactively connects insights.

**Features:**
- "Last time you asked about PE1, the issue was LDP. It's still showing the same symptom."
- "This is the 3rd time this week a BGP session has flapped. I recommend checking the underlying ISIS stability."
- "Based on the config changes made yesterday, I predict PE2 might have similar issues. Want me to check?"

---

### 4.6 Visual Investigation Replay (v30.0)

**What:** Record and replay past investigations as an animated timeline.

**Use case:** Training, post-incident review, knowledge sharing.

**UI:** Timeline slider that replays the brain's investigation step by step with the topology highlighting which devices were queried and what was found.

---

## 5. Architecture Diagrams

### Current Architecture (v21.2)

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Browser     │────▶│  Flask App   │────▶│  Ollama API  │
│   (noc.js)    │◀────│  (app.py)    │◀────│  (gpt-oss)   │
│   Text Chat   │     │  101 routes  │     │  Text Q&A    │
└──────────────┘     │  No Brain    │     └──────────────┘
                      │  integration │
                      └──────┬───────┘
                             │
                      ┌──────▼───────┐
                      │  MCP Server   │
                      │  (jmcp.py)    │
                      │  10 tools     │
                      └──────┬───────┘
                             │
                      ┌──────▼───────┐
                      │  Junos Lab    │
                      │  11 routers   │
                      └──────────────┘
```

### Target Architecture (v30.0)

```
┌────────────────────────────────────────────────────────────────┐
│                        Browser (noc.js v3)                      │
│  ┌────────────┐  ┌──────────────┐  ┌────────────────────────┐  │
│  │ Agentic    │  │ Investigation│  │ Approval Gates         │  │
│  │ Chat       │  │ Dashboard    │  │ & Safety Controls      │  │
│  │ + Tool Viz │  │ + Live Brain │  │ + Config Preview       │  │
│  └──────┬─────┘  └──────┬───────┘  └────────────┬───────────┘  │
│         │               │                        │              │
│         └───────────────┼────────────────────────┘              │
│                         │ WebSocket (brain_progress,            │
│                         │  tool_called, proactive_alert, etc.)  │
└─────────────────────────┼──────────────────────────────────────┘
                          │
┌─────────────────────────▼──────────────────────────────────────┐
│                    Flask App (app.py v3)                         │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────────┐ │
│  │ Agentic     │  │ Brain API    │  │ Memory & Learning      │ │
│  │ Chat Route  │  │ Endpoints    │  │ Engine                 │ │
│  │ + Query     │  │ + Progress   │  │ + Feedback             │ │
│  │   Classify  │  │   Stream     │  │ + Baselines            │ │
│  └──────┬──────┘  └──────┬───────┘  └────────────┬───────────┘ │
│         │                │                        │             │
│  ┌──────▼────────────────▼────────────────────────▼──────────┐ │
│  │                  Orchestration Layer                       │ │
│  │  Query Classify → Brain Select → Tool Call → Synthesize   │ │
│  └──────┬────────────────┬────────────────────────┬──────────┘ │
│         │                │                        │             │
│  ┌──────▼──────┐  ┌──────▼───────┐  ┌────────────▼──────────┐ │
│  │ Hypered     │  │ Reasoning    │  │ Quantum Engine        │ │
│  │ Brain       │  │ Engine       │  │ + Network Analysis    │ │
│  │ (6 layers)  │  │ (7 stages)   │  │ + KB Vector Store     │ │
│  └──────┬──────┘  └──────┬───────┘  └────────────┬──────────┘ │
└─────────┼────────────────┼────────────────────────┼────────────┘
          │                │                        │
   ┌──────▼────────────────▼────────────────────────▼────────┐
   │                    Ollama API                            │
   │   gpt-oss (classify) │ gpt-oss (analyze) │ nomic-embed  │
   │   temp=0.1           │ temp=0.05         │ (RAG)        │
   └──────────────────────┬──────────────────────────────────┘
                          │
   ┌──────────────────────▼──────────────────────────────────┐
   │                    MCP Server (jmcp.py)                   │
   │   execute_command │ batch │ get_config │ deploy │ facts  │
   └──────────────────────┬──────────────────────────────────┘
                          │
   ┌──────────────────────▼──────────────────────────────────┐
   │                    Junos Lab (11 routers)                 │
   │   PE1  PE2  PE3  P11  P12  P13  P14  P21  P22  P23  P24 │
   └──────────────────────────────────────────────────────────┘
```

---

## 6. File-by-File Change Map

### Phase 1 Changes (v22–v23)

| File | Changes | New Lines Est. |
|------|---------|---------------|
| `app.py` | +Brain API endpoints, +Reasoning API, +Agentic chat route, +WebSocket events, +RAG init | +800 |
| `hypered_brain.py` | +progress_callback param, +event emission at each layer | +150 |
| `reasoning_engine.py` | +API-friendly return types, +hypothesis JSON serialization | +100 |
| `kb_vectorstore.py` | +singleton accessor for web, +async-safe initialization | +50 |
| `noc.js` | +WebSocket brain event handlers, +tool call rendering in chat | +300 |
| `noc.css` | +brain progress styles, +tool call card styles | +200 |
| `index.html` | +Investigation view nav entry | +20 |

### Phase 2 Changes (v24–v25)

| File | Changes | New Lines Est. |
|------|---------|---------------|
| `noc.js` | +Investigation dashboard, +Agentic chat UI, +Dynamic quick actions, +Approval gates, +Copilot v2, +Topology highlights | +1,500 |
| `noc.css` | +Investigation dashboard styles, +Approval gate styles, +Copilot v2 styles | +800 |
| `app.py` | +Quick actions API, +Approval workflow, +Investigation history API | +400 |
| `index.html` | +Investigation view, +Approval modal, +Copilot v2 structure | +200 |

### Phase 3 Changes (v26–v27)

| File | Changes | New Lines Est. |
|------|---------|---------------|
| `app.py` | +Memory architecture, +Feedback learning API, +Proactive monitor, +Cross-device correlation | +600 |
| `hypered_brain.py` | +Hypothesis-driven mode, +Blast radius expansion, +Memory integration | +400 |
| `reasoning_engine.py` | +Web-friendly hypothesis testing, +Evidence evaluation | +300 |
| NEW: `memory_engine.py` | Memory layers, feedback learning, baseline management | +500 |
| NEW: `proactive_monitor.py` | Background monitoring, anomaly detection, alert generation | +400 |
| `noc.js` | +Feedback UI, +Alert banner, +Memory indicators | +400 |

### Phase 4 Changes (v28–v30)

| File | Changes | New Lines Est. |
|------|---------|---------------|
| NEW: `agent_orchestra.py` | Multi-agent collaboration framework | +800 |
| NEW: `nl_config_engine.py` | Natural language to Junos config translation | +600 |
| `app.py` | +Auto-remediation, +AI workflow generation, +NL config API | +500 |
| `hypered_brain.py` | +Multi-agent dispatch, +Auto-remediation pipeline | +300 |
| `noc.js` | +Investigation replay, +NL config UI, +Auto-remediation approval | +800 |

### Total New Code Estimate

| Phase | New Lines | Cumulative |
|-------|----------|-----------|
| Phase 1 (v22–23) | ~1,620 | ~34,620 |
| Phase 2 (v24–25) | ~2,900 | ~37,520 |
| Phase 3 (v26–27) | ~2,600 | ~40,120 |
| Phase 4 (v28–30) | ~3,000 | ~43,120 |

---

## 7. Implementation Priority Matrix

### Immediate Impact (Do First)

| # | Task | Impact | Effort | Files |
|---|------|--------|--------|-------|
| 1 | Brain API endpoints in app.py | 🔴 Critical | 4 hrs | app.py, hypered_brain.py |
| 2 | WebSocket brain progress events | 🔴 Critical | 3 hrs | app.py, noc.js |
| 3 | Agentic chat route (tool calling from browser) | 🔴 Critical | 6 hrs | app.py, noc.js |
| 4 | RAG integration in web backend | 🟡 High | 2 hrs | app.py, kb_vectorstore.py |
| 5 | Tool call visualization in chat UI | 🟡 High | 4 hrs | noc.js, noc.css |

### High Value (Do Next)

| # | Task | Impact | Effort | Files |
|---|------|--------|--------|-------|
| 6 | Investigation dashboard panel | 🟡 High | 8 hrs | noc.js, noc.css, index.html |
| 7 | Dynamic quick actions (AI-generated) | 🟡 High | 3 hrs | noc.js, app.py |
| 8 | Feedback learning (👍/👎 buttons) | 🟡 High | 4 hrs | noc.js, app.py |
| 9 | Confidence badges on responses | 🟢 Medium | 2 hrs | noc.js |
| 10 | Action buttons on AI responses | 🟢 Medium | 3 hrs | noc.js |

### Strategic (Build Over Time)

| # | Task | Impact | Effort | Files |
|---|------|--------|--------|-------|
| 11 | Memory architecture (4 layers) | 🟡 High | 8 hrs | memory_engine.py, app.py |
| 12 | Proactive anomaly detection | 🟡 High | 6 hrs | proactive_monitor.py, app.py, noc.js |
| 13 | Approval gates for config deploy | 🟢 Medium | 4 hrs | noc.js, app.py |
| 14 | Cross-device correlation | 🟢 Medium | 6 hrs | hypered_brain.py |
| 15 | Hypothesis-driven investigation | 🟢 Medium | 8 hrs | reasoning_engine.py, hypered_brain.py |

### Long-Term Vision

| # | Task | Impact | Effort | Files |
|---|------|--------|--------|-------|
| 16 | AI-generated workflows | 🟢 Medium | 6 hrs | app.py, noc.js |
| 17 | Auto-remediation with approval | 🟡 High | 10 hrs | app.py, hypered_brain.py, noc.js |
| 18 | Multi-agent collaboration | 🟢 Medium | 12 hrs | agent_orchestra.py |
| 19 | Natural language config | 🟢 Medium | 8 hrs | nl_config_engine.py |
| 20 | Investigation replay/timeline | 🟢 Low | 6 hrs | noc.js |

---

## 8. Risk Mitigation

### Risk: Ollama Latency with Complex Pipelines

**Problem:** Multi-pass brain investigations could take 30+ seconds with a local LLM.

**Mitigations:**
- `AdaptiveConcurrency` already auto-tunes parallelism (3–6 concurrent)
- `quick_brain_analyze()` for simple queries (single pass, ~5 seconds)
- Streaming SSE keeps the user informed during long investigations
- Cache frequently-asked queries and their results
- Skip redundant script execution if facts already gathered

### Risk: UI Overwhelm

**Problem:** Too many real-time events could make the UI noisy and confusing.

**Mitigations:**
- Collapsible sections — expanded by default for investigations, collapsed for routine checks
- Severity-based filtering — only show critical/warning in compact mode
- "AI is thinking..." summary mode — single line until investigation completes
- User preference: "detailed" vs "summary" investigation mode

### Risk: Config Safety

**Problem:** Agentic AI with MCP access could deploy bad configs.

**Mitigations:**
- All config changes require explicit approval gate (Phase 2.4)
- `commit check` before `commit` (already in MCP server)
- AI risk assessment on every config change
- Automatic `rollback 1` if verification fails
- Audit trail for every action taken
- Read-only mode toggle in settings

### Risk: Memory Bloat

**Problem:** Persistent memory could grow indefinitely.

**Mitigations:**
- LRU eviction for least-accessed memories
- Confidence decay — memories lose confidence over time if not reinforced
- Size limits per memory type
- Periodic garbage collection

---

## Summary: The Vision

| Today (v21.2) | Tomorrow (v30.0) |
|---|---|
| Beautiful dashboard with text chat | Full agentic command center |
| "Ask AI a question, get text back" | "AI investigates autonomously, shows its work, proposes fixes" |
| Terminal client has the smart brain | Web UI has the smart brain + visualization |
| 8 hardcoded quick actions | Dynamic AI-generated contextual actions |
| No tool calling from browser | Full MCP execution with live progress |
| No learning in web | 4-layer memory with feedback loop |
| Manual workflows only | AI-generated + auto-remediation workflows |
| Reactive — user must ask | Proactive — AI alerts before user notices |
| Single-device investigation | Cross-device correlation with blast radius |
| No investigation history | Recorded, replayable, searchable investigations |
| One AI model profile | Task-specific model profiles for accuracy |

---

## Next Step

**Tell me which items to build first, and I'll start implementing.**

The recommended first sprint (2-3 sessions):
1. Brain API endpoints (§1.1)
2. WebSocket brain progress (§1.4)
3. Agentic chat route (§1.3)
4. Tool call visualization (§2.2.1)
5. RAG in web (§1.5)

This alone transforms the web UI from "text chatbot" to "autonomous investigator."
