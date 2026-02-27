# 🧠 Intelligence Upgrade Plan — Junos AI NOC Bridge

## Current State Assessment

| Component | Status | Intelligence Level |
|-----------|--------|-------------------|
| Knowledge Base | 3,190 lines, 48 sections | ⭐⭐⭐⭐ Strong |
| RAG Vector Store | nomic-embed-text, cosine similarity, keyword boost | ⭐⭐⭐⭐ Good |
| System Prompt | Safe execution, OSI diagnostic, error handling | ⭐⭐⭐⭐ Good |
| 12 Specialists | OSPF, BGP, IS-IS, LDP, RSVP-TE, L3VPN, L2VPN, System, Security, QoS, HW, Synthesizer | ⭐⭐⭐⭐ Good |
| Self-Learning DB | resolution_db.json (issue→fix mapping) | ⭐⭐⭐ Basic |
| Golden Configs | 11 routers × (conf + meta) | ⭐⭐⭐ Static |
| Jinja2 Templates | 4 templates (BGP, OSPF, LDP, hardening) | ⭐⭐ Minimal |
| PDFs (unused!) | 7 Juniper study guides sitting in /files/ — NOT ingested | ❌ Wasted |
| Topology Awareness | Extracted from LLDP during audit only | ⭐⭐ Limited |
| Chat Memory | session_history.json, trim by tokens | ⭐⭐⭐ Basic |
| Baselines | router_baselines.json (deviation detection) | ⭐⭐⭐ Basic |

---

## 🚀 Upgrade Ideas — Ranked by Impact

### Tier 1: HIGH IMPACT / MODERATE EFFORT

#### 1. 📚 Ingest the 7 Juniper PDFs into the Knowledge Base (HUGE WIN)
**Problem:** You have 7 Juniper study guides (JNCIA, JIR, AJSPR, JMF, JL2V, JSPX, L3VPNs) sitting in `/files/` doing NOTHING. That's ~6,500 pages of expert knowledge the AI can't access.

**Solution:** Extract key content from each PDF → add to `KNOWLEDGE_BASE.md` → RAG auto-rebuilds.

**What to extract:**
- JNCIA: Junos fundamentals, routing basics (some already in KB)
- JIR: Intermediate routing — OSPF advanced, IS-IS, BGP (partial)
- AJSPR: Advanced SP routing — MPLS TE, multicast, CoS (gaps in KB)
- JMF: MPLS fundamentals — label operations, LSP types, FRR (partial)
- JL2V: L2VPN deep — VPLS, CCC, pseudowires, EVPN (big gap!)
- JSPX: SP switching — VLAN, STP, LAG, storm control (gap)
- Layer 3 VPNs: Inter-AS VPN, carrier-of-carriers, hub-spoke (gap)

**Impact:** The AI's knowledge jumps from "senior engineer" to "JNCIE study group" level.

#### 2. 🗺️ Persistent Topology Graph (Always-On Network Map)
**Problem:** Topology is only discovered during full audits. In chat mode, the AI has NO idea which router connects to which.

**Solution:** Build a topology graph at startup (from LLDP or golden configs) and inject a compact adjacency summary into the system prompt.

**Example injection:**
```
PE1 ↔ P11 (ge-0/0/1↔ge-0/0/0, 10.1.11.0/24)
PE1 ↔ P12 (ge-0/0/2↔ge-0/0/1, 10.1.12.0/24)
PE1 ↔ P21 (ge-0/0/3↔ge-0/0/0, 10.1.21.0/24)
...
```

**Impact:** AI can instantly answer "which routers are neighbors of PE1?" or "what's the path from PE1 to PE3?" without making ANY tool calls. Makes troubleshooting 10x faster because it knows the topology before starting.

#### 3. 🔄 Context-Aware Follow-Up (Conversation Memory Enhancement)
**Problem:** If you ask "check BGP on PE1" then follow up with "fix it", the AI often forgets what "it" refers to. The token-trimming can throw away the critical context.

**Solution:** Before trimming, extract and pin a "conversation summary" message that preserves:
- Last device(s) discussed
- Last issue found
- Last fix suggested
- Current troubleshooting state

**Implementation:** After each AI response, generate a 2-line summary and pin it as a system message that survives trimming.

#### 4. 🎯 Query Classification + Smart Routing
**Problem:** Every question goes through the same path: enhanced_input → ollama_chat → tool loop. Simple questions like "what is OSPF?" waste tool calls.

**Solution:** Classify the query before sending to AI:
- **Knowledge question** ("what is OSPF?", "explain BGP communities") → RAG retrieval only, no tools
- **Status question** ("check BGP on PE1") → tools required, current behavior
- **Troubleshooting** ("why is BGP down on PE1?") → tools + specialist chain
- **Config request** ("configure LDP on PE1") → config safety flow
- **Comparison** ("compare PE1 and PE2 config") → config diff flow

**Impact:** Faster responses for knowledge questions, smarter tool selection for operational questions.

---

### Tier 2: MEDIUM IMPACT / MEDIUM EFFORT

#### 5. 📊 Live Network Dashboard State
**Problem:** Each question starts from scratch. The AI doesn't know that "2 minutes ago, all protocols were healthy."

**Solution:** Background health poll every 5 minutes → store in memory:
```python
network_state = {
    "last_check": "2026-02-19 15:30",
    "ospf_healthy": True,
    "bgp_sessions": {"PE1": 2, "PE2": 2, ...},
    "alerts": [],
    "recent_changes": ["PE1: LDP pref set to 15 at 14:20"]
}
```
Inject this summary into the system prompt so the AI always knows current state.

#### 6. 🧪 "What-If" Config Simulator
**Problem:** Before pushing config, there's no way to predict impact.

**Solution:** When the AI proposes a config change, simulate the impact:
1. Parse the `set` commands
2. Check which protocols/interfaces are affected
3. Use the topology graph to predict cascading effects
4. Show: "This change will affect: OSPF adjacency PE1↔P11, LDP session to 10.255.255.11"

#### 7. 📝 Lessons Learned Database (Self-Improving AI)
**Problem:** `resolution_db.json` stores fix mappings, but the AI doesn't learn *patterns*. If OSPF breaks 3 times due to type mismatch, it doesn't proactively warn.

**Solution:** Create `lessons_learned.md` that stores:
```markdown
## Lesson: OSPF Interface Type Mismatch
- **Seen:** 3 times (PE1↔P11, PE1↔P12, P21↔P22)
- **Root Cause:** Mixed PtToPt vs broadcast types
- **Fix:** Always use `interface-type p2p` on all core links
- **Prevention:** Add to compliance check (E49)
```
Inject top 5 lessons into system prompt. The AI gets smarter over time.

#### 8. 🔗 Multi-Hop Root Cause Chain
**Problem:** The AI finds issues per-protocol but doesn't always connect them across the network.

**Solution:** After collecting all protocol data, build a dependency graph:
```
P13 firewall filter → blocks OSPF → PE1↔P13 no adjacency → 
LDP to 10.255.255.13 Nonexistent → BGP to P22 via P13 path unavailable → 
VPN-A suboptimal routing
```
The AI already has `root_cause_chains` in config, but it's not injected into the chat prompt. Wire it up.

---

### Tier 3: CREATIVE / ADVANCED

#### 9. 🔊 Natural Language Alerts (Proactive AI)
Instead of the user asking "is anything broken?", the AI proactively says:
> "⚠️ I noticed PE1's BGP to 10.255.255.12 flapped 3 times in the last hour. Want me to investigate?"

**Implementation:** Background monitoring thread + alert injection into chat.

#### 10. 📋 Runbook Automation
**Problem:** Complex tasks (e.g., "add a new VPN customer") require 15+ commands across 3 routers. The AI has to figure this out each time.

**Solution:** Predefined runbooks in YAML:
```yaml
runbooks:
  - name: "Add L3VPN Customer"
    steps:
      - router: PE
        commands:
          - "set routing-instances {name} instance-type vrf"
          - "set routing-instances {name} interface {intf}"
          - "set routing-instances {name} route-distinguisher {as}:{id}"
          - "set routing-instances {name} vrf-target target:{as}:{id}"
```
The AI selects the right runbook, fills in variables, and executes with safety checks.

#### 11. 🤖 Model Upgrade Path: qwen2.5:14b → qwen3:14b
When Qwen 3 stabilizes, it should give better tool calling and reasoning. The architecture is already model-agnostic (config.yaml driven).

#### 12. 📈 Trend Analysis (Time-Series Intelligence)
**Problem:** `audit_history.db` stores historical audits but the AI never looks at trends.

**Solution:** Before answering, query the last 5 audits:
- "Critical issues trending ↑ or ↓?"  
- "Which router has the most recurring issues?"
- "Is config drift increasing?"

Inject a 3-line trend summary into the prompt.

#### 13. 🌐 Multi-Vendor Readiness
The MCP architecture is vendor-neutral. Add a second MCP server for Cisco/Arista and the same AI works across vendors. Just add translation mappings:
```yaml
vendor_translations:
  cisco:
    "show bgp summary": "show ip bgp summary"
    "show ospf neighbor": "show ip ospf neighbor"
```

---

## Recommended Implementation Order

| Priority | Item | Effort | Impact |
|----------|------|--------|--------|
| 1 | 🗺️ Persistent Topology Graph (#2) | 2 hours | Instant topology awareness |
| 2 | 📚 PDF Knowledge Ingestion (#1) | 4 hours | Massive knowledge upgrade |
| 3 | 🎯 Query Classification (#4) | 2 hours | Smarter routing, faster responses |
| 4 | 🔄 Conversation Summary Pin (#3) | 1 hour | Better follow-up handling |
| 5 | 📝 Lessons Learned DB (#7) | 2 hours | Self-improving over time |
| 6 | 📊 Live Network State (#5) | 3 hours | Always-aware AI |
| 7 | 📈 Trend Analysis (#12) | 2 hours | Historical intelligence |
| 8 | 📋 Runbook Automation (#10) | 4 hours | Complex task automation |
| 9 | 🧪 What-If Simulator (#6) | 4 hours | Predictive safety |
| 10 | 🔊 Proactive Alerts (#9) | 3 hours | Autonomous monitoring |

---

## Which ones should we implement? Tell me and I'll start building.
