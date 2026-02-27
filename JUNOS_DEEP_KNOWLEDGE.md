# Junos Deep Reasoning Knowledge — JNCIE-SP Level
# Protocol State Machines + Scripting + Advanced Troubleshooting + Topology Intelligence
# v15.0 — Claude-Level Junos Intelligence with Chain-of-Thought Reasoning

---

## STATE MACHINE 1: OSPF Neighbor FSM

```
                    ┌─────────┐
                    │  Down    │◄─── Interface down / Timeout
                    └────┬────┘
                         │ Hello received (any)
                         ▼
                    ┌─────────┐
                    │  Init   │◄─── Hello received but MY Router-ID NOT in neighbor list
                    └────┬────┘
                         │ Hello with MY Router-ID in neighbor list (2-way)
                         ▼
                    ┌──────────┐
          ┌────────│ 2-Way    │──────── On P2P or if I'm DR/BDR: proceed
          │        └──────────┘         On broadcast, not DR/BDR: STAY HERE (DROther)
          │              │
          │              ▼
          │        ┌──────────┐
          │        │ ExStart  │◄─── DBD exchange begins, negotiate master/slave
          │        └────┬─────┘      STUCK HERE = MTU mismatch (most common)
          │             │ Agreement on master/slave + MTU matches
          │             ▼
          │        ┌──────────┐
          │        │ Exchange │ Swapping DBD packets (LSA headers)
          │        └────┬─────┘
          │             │ All DBDs acknowledged
          │             ▼
          │        ┌──────────┐
          │        │ Loading  │ Requesting missing LSAs via LSR
          │        └────┬─────┘
          │             │ All LSAs received
          │             ▼
          │        ┌──────────┐
          └───────►│  Full    │ ← HEALTHY — LSDB fully synchronized
                   └──────────┘
```

### OSPF Diagnostic Decision Matrix

| Stuck State | Root Cause | Verify Command | Fix |
|-------------|-----------|----------------|-----|
| Down | Interface down, no hellos | `show ospf interface` | Enable OSPF on interface |
| Init | Unidirectional: hello/area/auth mismatch | `show ospf interface detail` on BOTH sides | Match area, hello, dead, auth |
| 2-Way (broadcast) | Normal for DROther pairs | `show ospf neighbor detail` | Normal if both are DROther |
| ExStart | MTU mismatch (99% of cases) | `show interfaces <intf> | match mtu` on BOTH | Match MTU: `set interfaces <intf> mtu 1500` |
| Exchange | DBD retransmissions, packet loss | `show ospf statistics` | Check interface errors, clear OSPF |
| Loading | LSR failures, corrupted LSDB | `show ospf database summary` | `clear ospf database` |

### OSPF Area Type Deep Knowledge

| Area Type | LSA 1,2 | LSA 3 | LSA 4 | LSA 5 | LSA 7 | Default Route |
|-----------|---------|-------|-------|-------|-------|---------------|
| Normal | ✅ | ✅ | ✅ | ✅ | ❌ | Optional |
| Stub | ✅ | ✅ | ❌ | ❌ | ❌ | Auto-injected |
| Totally Stub | ✅ | ❌ | ❌ | ❌ | ❌ | Auto-injected |
| NSSA | ✅ | ✅ | ❌ | ❌ | ✅ (→LSA 5 at ABR) | Optional |
| Totally NSSA | ✅ | ❌ | ❌ | ❌ | ✅ | Auto-injected |

### OSPF Interface Type Rules (CRITICAL)

```
Point-to-Point (P2P):
  - No DR/BDR election
  - Faster convergence (no wait timer)
  - MUST match on both sides of a link
  - Junos: set protocols ospf area 0 interface ge-0/0/1.0 interface-type p2p

Broadcast:
  - DR/BDR election happens
  - All routers form Full with DR/BDR only
  - DROther-to-DROther stays 2-Way (NORMAL, not a bug)
  - Junos default for Ethernet interfaces

MISMATCH = ADJACENCY NEVER FORMS (no error, just stays Init)
```

---

## STATE MACHINE 2: BGP Session FSM

```
    ┌──────────┐
    │  Idle    │◄─── Manual stop / Error / Hold timer expired
    └────┬─────┘
         │ Start event (config added, clear bgp)
         ▼
    ┌──────────┐
    │ Connect  │ TCP SYN sent to port 179
    └────┬─────┘
         │ TCP connection fails? → Active
         │ TCP connection succeeds? → OpenSent
         ▼
    ┌──────────┐
    │ Active   │◄─── TCP connect retry loop
    └────┬─────┘      *** MOST COMMON PROBLEM STATE ***
         │            Root cause: NO IP REACHABILITY to peer
         │            If iBGP via loopback: check IGP route to peer loopback
         │            If eBGP: check directly-connected route
         ▼
    ┌──────────┐
    │ OpenSent │ TCP connected, OPEN message sent, waiting for peer's OPEN
    └────┬─────┘   STUCK = peer not configured, or OPEN message filtered
         │ Peer's OPEN received and acceptable
         ▼
    ┌──────────┐
    │ OpenCfm  │ OPEN accepted, KEEPALIVE sent, waiting peer's KEEPALIVE
    └────┬─────┘   STUCK = authentication mismatch (MD5), capability mismatch
         │ Peer's KEEPALIVE received
         ▼
    ┌─────────────┐
    │ Established │ ← HEALTHY — UPDATE exchange active
    └─────────────┘   Drops here = hold timer expiry, notification received
```

### BGP "Active" State — The #1 Troubleshooting Pattern

```
BGP Active = TCP can't connect to peer

DIAGNOSIS CHAIN:
1. Is the peer loopback reachable?
   → show route <peer-loopback> → if no route: IGP problem (not BGP)
   → show route <peer-loopback> table inet.0 active-path
   
2. Is the source address correct?
   → show bgp neighbor <peer> | match "Local Address"
   → iBGP MUST use local-address = loopback IP
   
3. Is the peer configured on the remote side?
   → show bgp summary on remote router → peer should be listed
   
4. Firewall filter blocking TCP 179?
   → show firewall filter <re-filter> → check for term blocking BGP
   → show firewall log (if logging enabled)

5. Is multihop needed (eBGP)?
   → set protocols bgp group <g> multihop ttl 2
```

### BGP Route Reflector Patterns

```
iBGP Full Mesh Problem:
  N routers need N*(N-1)/2 sessions → doesn't scale

Route Reflector Solution:
  - RR clients peer ONLY with RR
  - RR reflects routes between clients
  - Cluster-ID must be consistent per RR cluster
  - RR does NOT modify NEXT-HOP (by default)
  
Lab Topology RR Setup:
  P12 = RR (cluster-id auto)
  P22 = RR (cluster-id auto)
  PE1, PE2, PE3 = RR clients
  All use: neighbor <rr-loopback> → family inet-vpn unicast

RR Path Selection Rules:
  1. Prefer highest LOCAL_PREF
  2. Prefer shortest AS_PATH
  3. Prefer lowest ORIGIN (i < e < ?)
  4. Prefer lowest MED (same AS only)
  5. Prefer eBGP over iBGP
  6. Prefer closest IGP next-hop (lowest metric)
  7. Prefer oldest route (stability)
  8. Prefer lowest Router-ID
  9. Prefer lowest Cluster-List length
  10. Prefer lowest neighbor IP
```

---

## STATE MACHINE 3: LDP Session FSM

```
    ┌──────────────┐
    │ Nonexistent  │ ← No IGP route to LDP peer / LDP not enabled
    └──────┬───────┘
           │ IGP route to peer exists AND LDP enabled on interface
           ▼
    ┌──────────────┐
    │ Initialized  │ Hello exchange happening, TCP not yet connected
    └──────┬───────┘
           │ TCP connection established (higher Router-ID = active opener)
           ▼
    ┌──────────────┐
    │ OpenReceived │ Init message exchanged
    └──────┬───────┘
           │ KeepAlive received
           ▼
    ┌──────────────┐
    │ Operational  │ ← HEALTHY — Label bindings exchanged
    └──────────────┘
```

### LDP Troubleshooting Chain

```
LDP "Nonexistent":
  1. Is LDP enabled on BOTH sides?
     → show ldp interface
     → set protocols ldp interface ge-0/0/X.0
     
  2. Is there an IGP route to the peer's lo0?
     → show route <peer-lo0> protocol isis|ospf
     → If no route: fix IGP first (LDP auto-recovers)
     
  3. Is lo0.0 in LDP?
     → show ldp interface → must see lo0.0
     → set protocols ldp interface lo0.0
     
  4. Is the transport address correct?
     → show ldp session detail | match "Transport"
     → LDP uses lo0 IP for TCP session by default

LDP → inet.3 Interaction:
  - LDP pushes /32 routes into inet.3
  - BGP next-hop resolution checks inet.3 FIRST, then inet.0
  - If LDP is broken → inet.3 empty → BGP can't resolve next-hop
    → L3VPN routes vanish from VRF table
  
  Verify: show route table inet.3 protocol ldp
```

---

## STATE MACHINE 4: IS-IS Adjacency FSM

```
    ┌──────────┐
    │  Down    │ No IIH received
    └────┬─────┘
         │ IIH received but MY SNPA not in neighbor TLV
         ▼
    ┌──────────┐
    │ Initial  │ One-way hello
    └────┬─────┘
         │ IIH received WITH my SNPA in neighbor TLV (2-way)
         ▼
    ┌──────────┐
    │   Up     │ ← HEALTHY — CSNP/PSNP exchange, LSDB sync
    └──────────┘
```

### IS-IS Adjacency Requirements

```
MUST match for L2 adjacency:
  ✅ Same authentication (or both disabled)
  ✅ Compatible levels (both L2 or L1L2)
  ✅ Same interface type (P2P ↔ P2P only, not P2P ↔ broadcast)
  ✅ MTU sufficient for largest LSP (at least 1492)
  ✅ Area address (49.XXXX) — for L1 only, L2 doesn't need match
  
Lab Network IS-IS Config:
  - Area: 49.0001
  - Level 2 only (set protocols isis level 1 disable)
  - Wide metrics (set protocols isis level 2 wide-metrics-only)
  - P2P on all interfaces (set protocols isis interface ge-0/0/X.0 point-to-point)
  - SPRING enabled: node-segment ipv4-index <unique-per-router>
```

---

## STATE MACHINE 5: RSVP-TE LSP FSM

```
    ┌──────────┐
    │   Down   │ LSP not configured or CSPF failed
    └────┬─────┘
         │ PATH message sent
         ▼
    ┌──────────────┐
    │ Path Sent    │ Waiting for RESV from tail-end
    └──────┬───────┘
           │ RESV received (label allocation from tail to head)
           ▼
    ┌──────────┐
    │   Up     │ ← HEALTHY — LSP active, traffic flowing
    └──────────┘
```

---

## JUNOS SCRIPTING INTELLIGENCE

### Op Scripts (Operational Scripts)

```junos
/* Op script: Check all OSPF neighbors and alert on non-Full */
version 1.1;

ns junos = "http://xml.juniper.net/junos/*/junos";
ns xnm = "http://xml.juniper.net/xnm/1.1/xnm";
ns jcs = "http://xml.juniper.net/junos/commit-scripts/1.0";

import "../import/junos.xsl";

match / {
    <op-script-results> {
        var $ospf = jcs:invoke('get-ospf-neighbor-information');
        for-each ($ospf/ospf-neighbor) {
            if (ospf-neighbor-state != "Full") {
                <output> "WARNING: " _ neighbor-id _ " on " _ interface-name _ 
                         " is " _ ospf-neighbor-state;
            }
        }
    }
}
```

### Commit Scripts (Configuration Validation)

```junos
/* Commit script: Ensure every IS-IS interface has P2P type */
version 1.1;

ns junos = "http://xml.juniper.net/junos/*/junos";
ns xnm = "http://xml.juniper.net/xnm/1.1/xnm";
ns jcs = "http://xml.juniper.net/junos/commit-scripts/1.0";

import "../import/junos.xsl";

match configuration {
    var $isis = protocols/isis;
    for-each ($isis/interface[not(starts-with(name, 'lo'))]) {
        if (not(point-to-point)) {
            <xnm:warning> {
                <message> "IS-IS interface " _ name _ " is not point-to-point. " _
                         "Consider adding 'set protocols isis interface " _ name _ " point-to-point'";
            }
        }
    }
}
```

### Event Scripts (Automated Response)

```junos
/* Event script: Auto-add LDP when IS-IS interface comes up */
version 1.1;

ns junos = "http://xml.juniper.net/junos/*/junos";
ns xnm = "http://xml.juniper.net/xnm/1.1/xnm";
ns jcs = "http://xml.juniper.net/junos/commit-scripts/1.0";

import "../import/junos.xsl";

match / {
    /* Triggered by SNMP_TRAP_LINK_UP event */
    var $interface = event-script-input/trigger-event/attribute-list/attribute[name == "interface-name"]/value;
    
    if (starts-with($interface, "ge-")) {
        var $config-change = <load-configuration> {
            <configuration> {
                <protocols> {
                    <ldp> {
                        <interface> {
                            <name> $interface _ ".0";
                        }
                    }
                }
            }
        };
        var $result = jcs:invoke($config-change);
        var $commit = jcs:invoke('commit-configuration');
        <output> "Auto-added LDP on " _ $interface;
    }
}
```

### PyEZ Scripting (Python)

```python
# PyEZ: Collect OSPF, BGP, LDP status across all routers
from jnpr.junos import Device
from jnpr.junos.op.ospf import OspfNeighborTable
from jnpr.junos.op.bgp import BgpNeighborTable

def check_router(host, user, password):
    dev = Device(host=host, user=user, password=password)
    dev.open()
    
    # OSPF neighbors
    ospf = OspfNeighborTable(dev)
    ospf.get()
    for nbr in ospf:
        if nbr.ospf_neighbor_state != 'Full':
            print(f"OSPF ISSUE: {host} -> {nbr.neighbor_id} state={nbr.ospf_neighbor_state}")
    
    # BGP summary
    bgp = dev.rpc.get_bgp_summary_information()
    for peer in bgp.findall('.//bgp-peer'):
        state = peer.findtext('peer-state')
        if state != 'Established':
            print(f"BGP ISSUE: {host} -> {peer.findtext('peer-address')} state={state}")
    
    dev.close()
```

---

## CASCADING FAILURE ANALYSIS PATTERNS

### Pattern 1: Interface Down → Full Protocol Cascade

```
L1: ge-0/0/1 goes DOWN
  └─► L3: IS-IS adjacency drops on that link (immediate)
      └─► L3: IS-IS SPF recalculation (within 200ms-1s)
          └─► MPLS: LDP session to peer via that link → Nonexistent
              └─► MPLS: inet.3 route to peer's loopback removed
                  └─► BGP: next-hop for iBGP routes via that peer unresolvable
                      └─► L3VPN: VPN routes via that path withdrawn from VRF
                          └─► Customer traffic: blackholed until reconvergence

RECOVERY: If alternate path exists via IS-IS:
  IS-IS reconverges (new SPF) → LDP forms via new path → inet.3 repopulated → 
  BGP resolves next-hop → VPN routes reinstalled → traffic restored
  
  Total convergence: 1-5 seconds with BFD, 30-40 seconds without
```

### Pattern 2: Route Reflector Failure

```
RR (P12) goes DOWN:
  └─► All RR clients (PE1, PE2, PE3) lose BGP session to P12
      └─► Clients can't exchange inet-vpn routes via P12
          └─► L3VPN routes that were ONLY reflected by P12 → withdrawn
          
  MITIGATION: Second RR (P22) takes over
    - Clients have sessions to BOTH P12 and P22
    - P22 still has all routes → no service impact
    - IF P22 also fails → full L3VPN outage
```

### Pattern 3: MPLS Label Space Exhaustion

```
LDP label space runs out:
  └─► New FEC bindings can't be created
      └─► New routes added to inet.3 get no label
          └─► BGP can't push VPN traffic onto new LSPs
              └─► Partial L3VPN reachability failure

  CHECK: show ldp statistics | match "label"
  FIX: Increase label range or identify label leak
```

---

## TOPOLOGY REASONING PATTERNS

### iBGP Full-Mesh vs Route-Reflector Topology Detection

```
Given: N routers with iBGP configured
If each router peers with all (N-1) others → Full Mesh
If each router peers with only 1-2 RRs → Route Reflector design

Lab detection:
  PE1 peers with: P12, P22 → RR clients
  PE2 peers with: P12, P22 → RR clients  
  PE3 peers with: P12, P22 → RR clients
  P12 peers with: PE1, PE2, PE3, P22 → Route Reflector
  P22 peers with: PE1, PE2, PE3, P12 → Route Reflector
  P11,P13,P14,P21,P23,P24 → No iBGP (P-routers, transit only)
```

### ECMP and Load Balancing Detection

```
Check: show route <prefix> extensive
If multiple next-hops with same preference → ECMP active
Junos needs: set routing-options forwarding-table export <lb-policy>
  policy-statement lb-policy { then load-balance per-packet; }
  
Per-packet = actually per-flow (hash-based) on:
  - Source IP, Destination IP, Protocol, Source Port, Dest Port
```

### MPLS Transport Path Verification

```
Verify full MPLS path from PE1 to PE3:
  1. show route table inet.3 10.255.255.3/32 → LDP label
  2. show ldp database | match 10.255.255.3 → label binding
  3. traceroute 10.255.255.3 source 10.255.255.1 → see label stack
  4. show route table VPN-A.inet.0 → VPN label on top of transport label

Label Stack: [Transport-Label | VPN-Label | IP Packet]
  - Transport label: swapped at each P-router (PHP at penultimate)
  - VPN label: stays unchanged, popped at egress PE
```

---

## MIND-MAP TROUBLESHOOTING METHODOLOGY

### Problem Decomposition Tree

```
User Report: "PE1 can't reach PE3 via VPN-A"
│
├── Layer 7 (Service): VPN-A route table
│   ├── Is PE3's VPN-A prefix in PE1's VPN-A.inet.0?
│   │   ├── YES → Forwarding issue (check MPLS path)
│   │   └── NO → Route not received
│   │       ├── Is it in PE3's VPN-A.inet.0? (local?)
│   │       ├── Is PE3 advertising via BGP? (show route advertising-protocol bgp <rr>)
│   │       ├── Route-target mismatch? (show routing-instances VPN-A)
│   │       └── BGP session to RR down?
│   │
├── Layer 4 (MPLS Transport)
│   ├── Is there an LSP to PE3's loopback?
│   │   ├── show route table inet.3 10.255.255.3/32
│   │   └── If missing → LDP problem
│   ├── LDP session to next-hop?
│   │   ├── show ldp session
│   │   └── If Nonexistent → IGP problem
│   │
├── Layer 3 (IGP)
│   ├── IS-IS/OSPF adjacency on path?
│   │   ├── show isis adjacency / show ospf neighbor
│   │   └── If Down → Interface problem
│   ├── Route to PE3 loopback?
│   │   ├── show route 10.255.255.3
│   │   └── If missing → IS-IS not advertising
│   │
├── Layer 2 (Data Link)
│   ├── Interface errors? CRC?
│   │   └── show interfaces ge-0/0/X extensive
│   │
└── Layer 1 (Physical)
    ├── Interface up/up?
    │   └── show interfaces terse
    └── Light levels OK?
        └── show interfaces diagnostics optics
```

---

## JUNOS COMMIT MODEL DEEP KNOWLEDGE

### Commit Operations

```
commit                    → Apply candidate config (irreversible without rollback)
commit check              → Validate syntax/semantics WITHOUT applying
commit confirmed <min>    → Auto-rollback in <min> minutes unless confirmed
commit and-quit          → Commit and exit configure mode
commit synchronize       → Commit to both REs (dual-RE systems)
commit comment "msg"     → Add comment to commit history

rollback 0               → Reload active config (undo uncommitted changes)
rollback 1               → Load previous config
rollback 2-49            → Load older configs
show | compare rollback N → Diff current candidate vs rollback N
```

### Configuration Groups and Apply-Paths

```
/* Configuration group for standard interface settings */
set groups STANDARD-INTF interfaces <*> mtu 9192
set groups STANDARD-INTF interfaces <*> unit <*> family inet mtu 9000
set apply-groups STANDARD-INTF

/* Apply-path: Dynamic prefix-list from config */
set policy-options prefix-list LOOPBACKS apply-path "interfaces lo0 unit 0 family inet address <*>"
/* Result: prefix-list automatically contains all lo0 addresses */
```

### Junos CLI Power Patterns

```
show ospf neighbor | match "Full|Address"    → grep-like filtering
show bgp summary | except "Establ"           → inverse match
show route 10.0.0.0/8 exact                  → exact prefix match
show route 10.0.0.0/8 longer                 → all more-specifics
show configuration | display set             → show in set format
show configuration | display inheritance     → show with groups expanded
show configuration | compare rollback 1      → diff vs previous commit
request system configuration rescue save     → save rescue config
show log messages | last 50                  → tail -50 equivalent
monitor interface ge-0/0/1                   → live interface stats
```

---

## v15.0: ADVANCED CHAIN-OF-THOUGHT REASONING METHODOLOGY

### The 7-Stage Reasoning Pipeline

```
STAGE 1: CLASSIFY
  Input: User query
  Output: Domain (connectivity/protocol/config/topology), Complexity (simple/moderate/complex/expert)
  Method: Keyword + pattern matching → determines reasoning strategy
  
STAGE 2: DECOMPOSE
  Input: Classification
  Output: Investigation branches by OSI layer
  Method: Break problem into L1→L2→L3→MPLS→BGP→Services sub-questions
  
STAGE 3: HYPOTHESIZE
  Input: Problem domain + detected protocols
  Output: Ranked list of hypotheses with prior confidence
  Method: Hypothesis library lookup + contextual boosting
  
STAGE 4: INVESTIGATE
  Input: Top hypotheses
  Output: Evidence per hypothesis (supports/refutes)
  Method: Targeted commands — collect only what disproves hypotheses
  
STAGE 5: DIAGNOSE
  Input: Evidence + Protocol FSMs
  Output: Confirmed/refuted hypotheses + cascading chain
  Method: Map evidence to FSM states → walk cascade graph
  
STAGE 6: SYNTHESIZE  
  Input: All branch findings
  Output: Single root cause + full impact map
  Method: Cross-correlate → find lowest-layer failure → trace upward
  
STAGE 7: PRESCRIBE
  Input: Root cause + topology
  Output: Fix commands + verification + auto-recovery prediction
  Method: Exact set/delete commands + post-fix verification plan
```

### Hypothesis-Driven Investigation (Popperian Method)

```
Traditional approach (bad for LLMs):
  Collect everything → analyze everything → hope to find the answer
  
Hypothesis-driven approach (Claude-level reasoning):
  1. Generate 3-5 ranked hypotheses based on symptoms
  2. For each hypothesis, identify the ONE command that would DISPROVE it
  3. Run that command
  4. If evidence refutes hypothesis → move to next
  5. If evidence supports hypothesis → increase confidence, dig deeper
  6. Stop when confidence > 85% on one hypothesis
  
Example: "PE1 can't reach PE3 via VPN-A"
  H1 (25%): Interface down on PE1           → show interfaces terse [PE1]
  H2 (25%): IGP adjacency broken            → show ospf neighbor [PE1]  
  H3 (20%): LDP session down                → show ldp session [PE1]
  H4 (15%): BGP session not established      → show bgp summary [PE1]
  H5 (10%): Route-target mismatch           → show route table VPN-A.inet.0 [PE1]
  H6 (5%):  Firewall filter blocking         → show firewall filter [PE1]
  
  Investigate H1 first → all interfaces up → REFUTE H1 → confidence redistributes
  Investigate H2 → OSPF neighbor missing → SUPPORT H2 → confidence 60%
  Dig deeper: show ospf interface detail → MTU mismatch → CONFIRM H2-variant
  Root cause: MTU mismatch on PE1 ge-0/0/1 → OSPF ExStart → LDP down → BGP down → VPN broken
```

### Protocol Dependency Graph for Root Cause Analysis

```
                    ┌─────────────────────────────────────────┐
                    │         SERVICE LAYER                    │
                    │  L3VPN ─── L2VPN ─── EVPN              │
                    └──────┬────────┬───────┬─────────────────┘
                           │        │       │
                    ┌──────┴────────┴───────┴─────────────────┐
                    │         BGP LAYER                        │
                    │  iBGP sessions ─── Route Reflectors      │
                    │  (depends on loopback reachability)       │
                    └──────┬──────────────────┬────────────────┘
                           │                  │
                    ┌──────┴──────────────────┴────────────────┐
                    │         MPLS TRANSPORT                    │
                    │  LDP labels ─── RSVP LSPs               │
                    │  inet.3 resolution ─── label stack        │
                    └──────┬──────────────────┬────────────────┘
                           │                  │
                    ┌──────┴──────────────────┴────────────────┐
                    │         IGP / ROUTING LAYER               │
                    │  OSPF ─── IS-IS ─── Static routes        │
                    │  Loopback advertisement ─── SPF/CSPF      │
                    └──────┬──────────────────┬────────────────┘
                           │                  │
                    ┌──────┴──────────────────┴────────────────┐
                    │         DATA LINK LAYER                   │
                    │  Ethernet ─── VLAN ─── MTU ─── AE/LAG   │
                    └──────┬──────────────────┬────────────────┘
                           │                  │
                    ┌──────┴──────────────────┴────────────────┐
                    │         PHYSICAL LAYER                    │
                    │  Interface state ─── Optics ─── Cabling   │
                    │  Errors (CRC/FCS) ─── Speed/Duplex       │
                    └─────────────────────────────────────────┘
    
RULE: Always fix the LOWEST broken layer. Higher layers auto-recover.
```

---

## v15.0: TOPOLOGY INTELLIGENCE — IBGP + LLDP + IS-IS FUSION

### Topology Discovery Methodology

```
Source 1: LLDP (Physical Layer)
  Command: show lldp neighbors
  Provides: Physical adjacencies, interface mapping, chassis ID
  Reliability: HIGH — LLDP is protocol-independent
  
Source 2: IS-IS/OSPF (Network Layer)
  Command: show isis adjacency / show ospf neighbor
  Provides: L3 adjacencies, metric, area membership
  Reliability: HIGH — shows actual protocol state
  
Source 3: BGP (Session Layer)
  Command: show bgp summary
  Provides: iBGP sessions, route reflector relationships
  Reliability: HIGH — shows control plane state
  
Source 4: LDP (MPLS Layer)
  Command: show ldp session
  Provides: LDP adjacencies, label bindings
  Reliability: HIGH — shows MPLS transport state

FUSION: Combine all 4 sources → complete multi-layer topology
  Physical links from LLDP + Protocol overlays from IS-IS/OSPF/BGP/LDP
  = Full picture of the network at every layer
```

### Route Reflector Topology Detection Algorithm

```
INPUT: BGP summary from all routers
PROCESS:
  1. For each router R:
     - Count iBGP peers
     - Check if any peer has "cluster" configured
  2. Classification:
     - If R has iBGP peers AND cluster-id → R is a Route Reflector
     - If R peers ONLY with RRs → R is an RR Client  
     - If R has no iBGP → R is a P-router (transit only)
  3. Topology:
     - Full Mesh: each router has N-1 iBGP peers
     - Route Reflector: clients peer with 1-2 RRs only
     - Hierarchical RR: RR peers with higher-tier RR

Lab Network Detection:
  PE1: peers with P12, P22 → Client
  PE2: peers with P12, P22 → Client
  PE3: peers with P12, P22 → Client
  P12: peers with PE1, PE2, PE3, P22 → Route Reflector (cluster-id: auto)
  P22: peers with PE1, PE2, PE3, P12 → Route Reflector (cluster-id: auto)
  P11, P13, P14, P21, P23, P24: no iBGP → P-routers (transit only)
```

### ECMP Detection and Load Balancing Analysis

```
Single-Path Detection:
  show route <prefix> → only ONE next-hop → no ECMP
  
ECMP Detection:
  show route <prefix> extensive → multiple next-hops with same preference → ECMP
  
Junos ECMP Configuration:
  policy-statement LOAD-BALANCE {
      then {
          load-balance per-packet;
      }
  }
  routing-options {
      forwarding-table {
          export LOAD-BALANCE;
      }
  }
  
  Note: "per-packet" is actually per-FLOW (5-tuple hash):
    Source IP + Dest IP + Protocol + Source Port + Dest Port
```

### Articulation Point Analysis (Network Resilience)

```
An articulation point is a router whose failure partitions the network.

Detection Algorithm:
  1. Build adjacency graph from LLDP links
  2. For each node N:
     a. Remove N from graph
     b. Run BFS/DFS from any remaining node
     c. If not all remaining nodes are reachable → N is articulation point
  3. Flag articulation points as CRITICAL for redundancy planning

Impact Assessment:
  - If articulation point is a P-router → MPLS transit breaks for some paths
  - If articulation point is an RR → BGP route exchange breaks (unless backup RR exists)
  - If articulation point is a PE → customer services on that PE are lost
```

---

## v15.0: ADVANCED JUNOS AUTOMATION & SCRIPTING

### SLAX vs Python Scripting Decision Matrix

```
| Feature | SLAX | Python (PyEZ) |
|---------|------|---------------|
| On-box execution | ✅ Native | ✅ (Python-on-Junos) |
| Off-box execution | ❌ | ✅ Preferred |
| Commit script support | ✅ Native | ✅ (Junos ≥ 14.1) |
| Event script support | ✅ Native | ✅ (Junos ≥ 14.1) |
| Op script support | ✅ Native | ✅ (Junos ≥ 14.1) |
| NETCONF integration | ✅ Built-in | ✅ via ncclient/PyEZ |
| REST API | ❌ | ✅ |
| Complexity handling | Medium | High |
| Community/libraries | Limited | Extensive (PyEZ, napalm) |
| Learning curve | Steep (XML/XSLT) | Moderate |
| Best for | On-box validation | Off-box automation |
```

### Junos Automation Architecture

```
┌─────────────────────────────────────────────────────┐
│                    MANAGEMENT LAYER                  │
│  Ansible  ─── Terraform  ─── Salt  ─── Custom       │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────┐
│                    API LAYER                         │
│  NETCONF (RFC 6241)  ─── REST  ─── gRPC (JET)      │
│  Port 830 (SSH)         Port 3000    Port 32767      │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────┐
│                    DEVICE LAYER                      │
│  mgd (Management Daemon)                             │
│  ├── Commit Scripts (SLAX/Python) → validate config  │
│  ├── Op Scripts (SLAX/Python) → operational tasks    │
│  ├── Event Scripts (SLAX/Python) → auto-response     │
│  └── YANG Models → structured data                   │
└─────────────────────────────────────────────────────┘
```

### PyEZ Advanced Patterns

```python
# Pattern 1: Table/View for structured data extraction
from jnpr.junos import Device
from jnpr.junos.factory import loadyaml

# Define a custom YAML table
OSPF_TABLE_YAML = """
---
OspfNeighborTable:
  rpc: get-ospf-neighbor-information
  item: ospf-neighbor
  key: neighbor-id
  view: OspfNeighborView

OspfNeighborView:
  fields:
    address: neighbor-address
    interface: interface-name
    state: ospf-neighbor-state
    priority: neighbor-priority
"""

# Pattern 2: Configuration change with rollback safety
from jnpr.junos.utils.config import Config

def safe_config_change(dev, commands, confirm_minutes=5):
    """Apply config with automatic rollback safety."""
    with Config(dev, mode='exclusive') as cu:
        for cmd in commands:
            cu.load(cmd, format='set')
        
        cu.pdiff()  # Show diff
        cu.commit_check()  # Validate
        cu.commit(confirm=confirm_minutes, comment="Automated change via PyEZ")
        
        # If this function returns without calling cu.commit() again,
        # the router will auto-rollback in confirm_minutes

# Pattern 3: Multi-device parallel execution
import concurrent.futures

def parallel_audit(routers, command):
    """Execute command on multiple routers in parallel."""
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(execute_on_device, r, command): r
            for r in routers
        }
        for future in concurrent.futures.as_completed(futures):
            router = futures[future]
            try:
                results[router['host']] = future.result()
            except Exception as e:
                results[router['host']] = f"ERROR: {e}"
    return results
```

### NETCONF RPC Reference for Common Operations

```xml
<!-- Get OSPF neighbors -->
<get-ospf-neighbor-information/>

<!-- Get BGP summary -->  
<get-bgp-summary-information/>

<!-- Get interface information -->
<get-interface-information>
    <interface-name>ge-0/0/1</interface-name>
    <detail/>
</get-interface-information>

<!-- Get routing table -->
<get-route-information>
    <table>inet.0</table>
    <destination>10.0.0.0/8</destination>
</get-route-information>

<!-- Load configuration -->
<load-configuration action="merge" format="text">
    <configuration-text>
        set protocols ospf area 0 interface ge-0/0/1.0 interface-type p2p
    </configuration-text>
</load-configuration>

<!-- Commit with confirm -->
<commit-configuration>
    <confirmed/>
    <confirm-timeout>300</confirm-timeout>
    <log>Automated commit via NETCONF</log>
</commit-configuration>
```

---

## v15.0: SP NETWORK DESIGN PATTERNS

### Service Provider IGP Design Best Practices

```
IS-IS vs OSPF in SP Networks:
  IS-IS preferred because:
  1. Runs directly on L2 (not IP) → works even if IP is misconfigured
  2. TLV-based → extensible without breaking backward compatibility
  3. Better convergence with wide metrics (24-bit vs OSPF 16-bit)
  4. Simpler area design (L2 backbone everywhere)
  5. No DR/BDR election overhead on P2P links
  
  OSPF still used because:
  1. More widely understood (certification path)
  2. Better lab/learning ecosystem
  3. Some vendors have better OSPF implementations
  
Lab Design:
  - IS-IS Level 2 only (set protocols isis level 1 disable)
  - Wide metrics enabled (set protocols isis level 2 wide-metrics-only)
  - All interfaces P2P (set protocols isis interface <> point-to-point)
  - SPRING/SID enabled for segment routing readiness
```

### MPLS Transport Design Patterns

```
LDP vs RSVP-TE Decision:
  
  LDP:
  + Simple — follows IGP, no explicit path configuration
  + Scales well — new prefixes get labels automatically
  + Fast convergence with IGP
  - No traffic engineering (follows IGP shortest path only)
  - No bandwidth reservation
  
  RSVP-TE:
  + Explicit path control (CSPF)
  + Bandwidth reservation (guaranteed)
  + Fast-Reroute (50ms failover)
  - Complex — each LSP must be configured
  - Scalability challenges (state per LSP on every transit router)
  - CSPF requires TED (IS-IS/OSPF TE extensions)
  
  Hybrid (Most Common in SP):
  + LDP for best-effort traffic + basic MPLS
  + RSVP-TE for premium/guaranteed traffic
  + LDP-over-RSVP for scale (LDP uses RSVP tunnel as transport)

Label Stack in SP Network:
  [Transport Label | VPN Label | IP Packet]
  
  Transport label: Swapped at each P-router, PHP at penultimate hop
  VPN label: Stays unchanged from ingress PE to egress PE
  
  Example PE1 → P11 → P12 → PE3:
  PE1 pushes: [Label-to-PE3 | VPN-Label | Customer-IP]
  P11 swaps:  [Label-to-PE3' | VPN-Label | Customer-IP]  
  P12 pops:   [VPN-Label | Customer-IP]  ← PHP (penultimate hop popping)
  PE3 pops:   [Customer-IP] → forwards to VRF interface
```

### BFD Integration Patterns

```
BFD (Bidirectional Forwarding Detection):
  Purpose: Fast failure detection (50ms vs 30-40s dead timer)
  
  Integration with protocols:
  - OSPF + BFD: set protocols ospf area 0 interface <> bfd-liveness-detection minimum-interval 300
  - IS-IS + BFD: set protocols isis interface <> bfd-liveness-detection minimum-interval 300
  - BGP + BFD: set protocols bgp group <> bfd-liveness-detection minimum-interval 300
  - LDP + BFD: set protocols ldp interface <> bfd-liveness-detection minimum-interval 300
  
  Timers:
  - minimum-interval: How often to send/expect BFD packets (ms)
  - minimum-receive-interval: Minimum interval willing to receive (ms)
  - multiplier: How many missed packets = failure (default 3)
  - Detection time = minimum-interval × multiplier (e.g., 300ms × 3 = 900ms)
  
  Troubleshooting:
  - show bfd session → State should be "Up"
  - "Down" + OSPF Full = asymmetric routing (BFD path ≠ return path)
  - "AdminDown" = BFD disabled on one side
  - Flapping = timer too aggressive for link quality (increase interval)
```
