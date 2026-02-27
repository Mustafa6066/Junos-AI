# Expert Troubleshooting Examples — Junos MPLS/VPN Lab
# v13.0: Pattern-based reasoning examples for AI few-shot injection
# These examples teach the AI HOW to reason, not just WHAT the answer is.

---

## OSPF Examples

### Example OSPF-1: Interface Type Mismatch (Point-to-Point vs Broadcast)
**SYMPTOM:** OSPF neighbor between PE1 (ge-0/0/1) and P11 (ge-0/0/0) never forms. Both interfaces show "Up" but 0 neighbors.
**DATA COLLECTED:**
```
PE1> show ospf interface ge-0/0/1.0
  Interface           State   Area    DR ID           BDR ID    Nbrs
  ge-0/0/1.0          PtToPt  0.0.0.0 0.0.0.0         0.0.0.0   0

P11> show ospf interface ge-0/0/0.0
  Interface           State   Area    DR ID           BDR ID    Nbrs
  ge-0/0/0.0          DR      0.0.0.0 10.255.255.11   0.0.0.0   0
```
**REASONING:**
  STEP 1: PE1 ge-0/0/1.0 is "PtToPt" (point-to-point). P11 ge-0/0/0.0 is "DR" (broadcast/designated router).
  STEP 2: Both sides of an OSPF link MUST have the same interface type. PtToPt ↔ Broadcast = INCOMPATIBLE.
  STEP 3: The hello packets differ in format — PtToPt omits DR/BDR election, Broadcast includes it. They cannot negotiate.
  STEP 4: This is the ROOT CAUSE of zero neighbors. No cascading failure yet because other paths may exist.
**ROOT CAUSE:** OSPF interface type mismatch — PE1 is point-to-point, P11 is broadcast.
**FIX:**
```
set protocols ospf area 0 interface ge-0/0/0.0 interface-type p2p
```
Apply on P11 to match PE1's point-to-point type.
**VERIFICATION:** `show ospf neighbor` on both PE1 and P11 — should show "Full" state.
**CASCADING:** Once OSPF adjacency forms → LDP session auto-establishes → BGP reachability to PE1's loopback restores → iBGP session comes up.
**CONFIDENCE:** HIGH

### Example OSPF-2: Hello/Dead Timer Mismatch
**SYMPTOM:** OSPF neighbors PE2 and P12 show "Init" state — stuck, never reaching Full.
**DATA COLLECTED:**
```
PE2> show ospf interface ge-0/0/2.0 detail
  Hello: 10s  Dead: 40s  Area: 0.0.0.0  Type: PtToPt

P12> show ospf interface ge-0/0/1.0 detail
  Hello: 30s  Dead: 120s  Area: 0.0.0.0  Type: PtToPt
```
**REASONING:**
  STEP 1: PE2 hello=10s dead=40s. P12 hello=30s dead=120s.
  STEP 2: OSPF requires MATCHING hello AND dead timers on both sides.
  STEP 3: "Init" state = PE2 sees P12's hello but P12 doesn't see PE2 in its neighbor list (timer mismatch → OSPF ignores the hello).
  STEP 4: Timer mismatch is the root cause.
**ROOT CAUSE:** OSPF hello/dead timer mismatch between PE2 (10/40) and P12 (30/120).
**FIX:**
```
# On P12, change to standard 10/40 timers:
set protocols ospf area 0 interface ge-0/0/1.0 hello-interval 10
set protocols ospf area 0 interface ge-0/0/1.0 dead-interval 40
```
**VERIFICATION:** `show ospf neighbor` — should transition Init → Full within 40 seconds.
**CONFIDENCE:** HIGH

### Example OSPF-3: Area ID Mismatch
**SYMPTOM:** OSPF adjacency between P13 and P14 stuck at Init.
**DATA COLLECTED:**
```
P13> show ospf interface ge-0/0/3.0 detail
  Area: 0.0.0.0  Hello: 10  Dead: 40  Type: PtToPt

P14> show ospf interface ge-0/0/2.0 detail
  Area: 0.0.0.1  Hello: 10  Dead: 40  Type: PtToPt
```
**REASONING:**
  STEP 1: P13 is in area 0.0.0.0, P14 is in area 0.0.0.1.
  STEP 2: OSPF requires both sides of a link to be in the SAME area.
  STEP 3: Area mismatch causes hellos to be discarded — adjacency never forms.
  STEP 4: Root cause is P14's misconfigured area.
**ROOT CAUSE:** Area ID mismatch — P13 in area 0, P14 in area 1 on the same link.
**FIX:**
```
# On P14:
delete protocols ospf area 0.0.0.1 interface ge-0/0/2.0
set protocols ospf area 0 interface ge-0/0/2.0 interface-type p2p
```
**CONFIDENCE:** HIGH

---

## BGP Examples

### Example BGP-1: Session Stuck in Active State (IGP Root Cause)
**SYMPTOM:** PE1 BGP session to RR P12 shows "Active" — not establishing.
**DATA COLLECTED:**
```
PE1> show bgp summary
  Peer        AS    InPkt  OutPkt  State
  10.255.255.12 65000  0      0     Active

PE1> show route 10.255.255.12/32
  inet.0: no matching route found
```
**REASONING:**
  STEP 1: BGP state "Active" = TCP cannot connect to peer 10.255.255.12.
  STEP 2: iBGP peers are configured via loopback addresses. TCP connect requires an IGP route to the peer's loopback.
  STEP 3: `show route 10.255.255.12/32` returns "no matching route" — PE1 has NO path to P12's loopback.
  STEP 4: This is NOT a BGP problem. The ROOT CAUSE is IGP failure — OSPF/IS-IS is not advertising P12's loopback to PE1.
**ROOT CAUSE:** Missing IGP route to 10.255.255.12 (P12's loopback). BGP Active is a SYMPTOM, not the cause.
**FIX:** Fix the underlying IGP issue first:
```
# Check P12's loopback is in OSPF/IS-IS:
show ospf interface lo0.0    # on P12
show isis interface lo0.0     # on P12
# If missing:
set protocols ospf area 0 interface lo0.0 passive
set protocols isis interface lo0.0 passive
```
**VERIFICATION:** 
1. `show route 10.255.255.12/32` on PE1 — should appear via OSPF/IS-IS
2. `show bgp neighbor 10.255.255.12` — should transition Active → OpenSent → Established
**CASCADING:** BGP Active → no L3VPN routes exchanged → VPN-A traffic fails between PE1 and all PEs.
**CONFIDENCE:** HIGH

### Example BGP-2: Route Reflector Missing Client Configuration
**SYMPTOM:** PE3 has BGP Established to RR P22 but receives 0 routes from other PEs.
**DATA COLLECTED:**
```
PE3> show bgp summary
  Peer         AS    InPkt  OutPkt  State     Received/Accepted
  10.255.255.22 65000 50    45      Established  0/0

P22> show bgp group IBGP
  Type: Internal    Local AS: 65000
  Neighbor: 10.255.255.3  → cluster not configured
  Export: [ NEXT-HOP-SELF ]
```
**REASONING:**
  STEP 1: BGP is Established (TCP connected, OPEN exchanged) but PE3 receives 0 routes.
  STEP 2: P22 is a Route Reflector. RRs must have `cluster` ID and clients configured as RR clients.
  STEP 3: P22's config shows PE3 as a regular iBGP peer, NOT an RR client. Without `cluster`, P22 won't reflect routes from other PEs to PE3.
  STEP 4: Root cause is missing RR client configuration on P22 for PE3.
**ROOT CAUSE:** P22 (Route Reflector) not configured with PE3 as an RR client.
**FIX:**
```
# On P22:
set protocols bgp group IBGP cluster 10.255.255.22
set protocols bgp group IBGP neighbor 10.255.255.3 type internal
```
**CONFIDENCE:** HIGH

### Example BGP-3: Authentication Mismatch
**SYMPTOM:** BGP session between PE1 and RR P12 shows "Idle" with "Cease: connection rejected."
**DATA COLLECTED:**
```
PE1> show bgp neighbor 10.255.255.12
  State: Idle  Last Error: Cease: connection rejected
  Authentication: MD5, key configured

P12> show bgp neighbor 10.255.255.1
  State: Idle  Last Error: Open Message Error
  Authentication: none
```
**REASONING:**
  STEP 1: PE1 has MD5 authentication enabled. P12 has no authentication.
  STEP 2: When PE1 sends TCP SYN with MD5 digest, P12 rejects it (unexpected auth).
  STEP 3: Both sides must either BOTH have auth with MATCHING keys, or NEITHER have auth.
**ROOT CAUSE:** BGP authentication mismatch — PE1 has MD5, P12 does not.
**FIX:**
```
# Either add auth to P12:
set protocols bgp group IBGP authentication-key "same-key-as-PE1"
# Or remove auth from PE1:
delete protocols bgp group IBGP authentication-key
```
**CONFIDENCE:** HIGH

---

## LDP/MPLS Examples

### Example LDP-1: LDP Session "Nonexistent" (IGP Root Cause)
**SYMPTOM:** LDP session between PE1 and P11 shows "Nonexistent" despite both having LDP enabled.
**DATA COLLECTED:**
```
PE1> show ldp session
  Address          State       Connection  Hold time
  10.255.255.11    Nonexistent

PE1> show ldp neighbor
  (no LDP neighbors found)

PE1> show route 10.255.255.11/32
  inet.0: no matching route found
```
**REASONING:**
  STEP 1: LDP "Nonexistent" = LDP discovered the peer but cannot establish TCP session.
  STEP 2: LDP uses the peer's router-id (loopback) for TCP session setup. Requires IGP route to that loopback.
  STEP 3: No route to 10.255.255.11 — the IGP (OSPF/IS-IS) is not providing reachability.
  STEP 4: ROOT CAUSE is IGP failure, same pattern as BGP Active. Fix IGP first.
**ROOT CAUSE:** No IGP route to P11's loopback 10.255.255.11 — LDP cannot establish TCP session.
**FIX:** Fix IGP adjacency between PE1 and P11 first (see OSPF examples).
**CASCADING:** No LDP → no MPLS labels for inet.3 → BGP next-hop not resolvable → L3VPN routes withdrawn.
**CONFIDENCE:** HIGH

### Example LDP-2: LDP Not Enabled on Interface
**SYMPTOM:** LDP session exists between PE1 and P11 via other paths but no label binding for direct link.
**DATA COLLECTED:**
```
PE1> show ldp interface
  Interface        Label-space-ID  Nbr-count   Next-hello
  ge-0/0/1.0       10.255.255.1:0  1           3
  ge-0/0/2.0       10.255.255.1:0  1           4
  (ge-0/0/3.0 NOT listed — LDP not enabled on this interface)

PE1> show configuration protocols ldp
  interface ge-0/0/1.0;
  interface ge-0/0/2.0;
  # ge-0/0/3.0 is MISSING
```
**REASONING:**
  STEP 1: LDP is only enabled on ge-0/0/1 and ge-0/0/2. ge-0/0/3 is missing.
  STEP 2: Traffic to certain destinations may take a suboptimal path because no label is bound for the direct link via ge-0/0/3.
  STEP 3: Simple configuration omission.
**ROOT CAUSE:** LDP not enabled on ge-0/0/3.0.
**FIX:**
```
set protocols ldp interface ge-0/0/3.0
```
**CONFIDENCE:** HIGH

---

## IS-IS Examples

### Example ISIS-1: IS-IS Adjacency Not Forming (Level Mismatch)
**SYMPTOM:** IS-IS adjacency between P21 and P22 not forming despite both having IS-IS configured.
**DATA COLLECTED:**
```
P21> show isis adjacency
  (no IS-IS adjacencies on ge-0/0/1.0)

P21> show isis interface ge-0/0/1.0 detail
  Level 2 enabled, Level 1 disabled
  
P22> show isis interface ge-0/0/0.0 detail
  Level 1 enabled, Level 2 disabled
```
**REASONING:**
  STEP 1: P21 runs IS-IS Level 2 only. P22 runs Level 1 only.
  STEP 2: IS-IS requires at least one common level between neighbors to form adjacency.
  STEP 3: L2-only ↔ L1-only = no common level → adjacency cannot form.
**ROOT CAUSE:** IS-IS level mismatch — P21 is L2-only, P22 is L1-only on the connecting interface.
**FIX:**
```
# On P22 (or P21, depending on design), enable the matching level:
set protocols isis interface ge-0/0/0.0 level 2 enable
# Or set both to level 1-2:
set protocols isis interface ge-0/0/0.0 level 1-2
```
**CONFIDENCE:** HIGH

### Example ISIS-2: IS-IS Authentication Failure
**SYMPTOM:** IS-IS neighbors PE2 and P23 show adjacency down with "authentication failure" in logs.
**DATA COLLECTED:**
```
PE2> show isis interface ge-0/0/4.0 detail
  Authentication: MD5 key-chain "isis-key"

P23> show isis interface ge-0/0/1.0 detail
  Authentication: not configured
```
**REASONING:**
  STEP 1: PE2 has IS-IS authentication enabled. P23 does not.
  STEP 2: IS-IS PDUs from PE2 include HMAC-MD5 TLV. P23 rejects them (unexpected auth) OR P23's hellos lack auth and PE2 rejects them.
  STEP 3: Both sides must match on authentication presence and key.
**ROOT CAUSE:** IS-IS authentication mismatch between PE2 and P23.
**FIX:**
```
# On P23:
set protocols isis interface ge-0/0/1.0 level 2 hello-authentication-key "same-key"
set protocols isis interface ge-0/0/1.0 level 2 hello-authentication-type md5
```
**CONFIDENCE:** HIGH

---

## L3VPN Examples

### Example L3VPN-1: VRF Routes Not Exchanged (Missing Route Target)
**SYMPTOM:** VPN-A customer on PE1 cannot reach VPN-A customer on PE3. VRF route table on PE3 shows no routes from PE1.
**DATA COLLECTED:**
```
PE1> show route table VPN-A.inet.0
  10.100.1.0/24 *[Direct/0] via ge-0/0/5.0
  10.100.1.1/32 *[Local/0] via ge-0/0/5.0

PE3> show route table VPN-A.inet.0
  10.100.3.0/24 *[Direct/0] via ge-0/0/5.0
  (NO routes from PE1 — 10.100.1.0/24 is MISSING)

PE1> show route advertising-protocol bgp 10.255.255.12 table VPN-A.inet.0
  10.100.1.0/24  RT: 65000:100

PE3> show configuration routing-instances VPN-A
  vrf-import VPN-A-IMPORT;
  
PE3> show policy VPN-A-IMPORT
  term accept { from community VPN-A-RT; then accept; }
  VPN-A-RT members: target:65000:200
```
**REASONING:**
  STEP 1: PE1 advertises 10.100.1.0/24 with route-target 65000:100.
  STEP 2: PE3's VPN-A import policy accepts routes with RT 65000:200.
  STEP 3: 65000:100 ≠ 65000:200 → PE3's import policy rejects PE1's VPN-A routes.
  STEP 4: Route target mismatch between PE1's export and PE3's import.
**ROOT CAUSE:** Route target mismatch — PE1 exports with 65000:100, PE3 imports with 65000:200.
**FIX:**
```
# Either fix PE3's import to accept 65000:100:
set policy-options community VPN-A-RT members target:65000:100
# Or fix PE1's export to use 65000:200:
set routing-instances VPN-A vrf-target target:65000:200
```
**VERIFICATION:** `show route table VPN-A.inet.0` on PE3 — should now show 10.100.1.0/24 from PE1.
**CONFIDENCE:** HIGH

### Example L3VPN-2: MPLS Transport Failure Breaks L3VPN
**SYMPTOM:** All L3VPN traffic between PE1 and PE3 fails. VPN routes exist in VRF table but traffic is blackholed.
**DATA COLLECTED:**
```
PE3> show route table VPN-A.inet.0
  10.100.1.0/24 *[BGP/170] via 10.255.255.1, Push 299984, Push 299792 (S=0)
    > to 10.1.23.1 via ge-0/0/1.0

PE3> show route table inet.3 10.255.255.1
  (no matching route in inet.3)

PE3> show ldp session
  (no LDP sessions)
```
**REASONING:**
  STEP 1: VPN route exists and shows correct label stack (VPN label + transport label).
  STEP 2: But inet.3 has no route to 10.255.255.1 (PE1's loopback) — the MPLS transport is broken.
  STEP 3: LDP sessions are ALL down — no label-switched paths.
  STEP 4: Root cause chain: LDP down → no inet.3 entries → BGP next-hop unresolvable via MPLS → VPN traffic cannot be label-switched.
  STEP 5: Check WHY LDP is down — likely IGP failure upstream.
**ROOT CAUSE:** MPLS transport failure (LDP sessions down) → cascades to L3VPN blackhole.
**FIX:** Fix LDP/IGP first (see LDP examples), then VPN auto-recovers.
**CONFIDENCE:** HIGH

---

## Cascading Failure Examples

### Example CASCADE-1: Single Link Failure → Multi-Protocol Impact
**SYMPTOM:** PE1 reports: BGP Active to P12, LDP Nonexistent to P11, VPN-A routes missing.
**DATA COLLECTED:**
```
PE1> show interfaces ge-0/0/1 terse
  ge-0/0/1.0  up  down  ← Physical up but protocol down

PE1> show ospf neighbor
  (0 OSPF neighbors)

PE1> show ldp session
  10.255.255.11  Nonexistent

PE1> show bgp summary
  10.255.255.12  Active
```
**REASONING (Bottom-Up OSI):**
  STEP 1 (L1): ge-0/0/1.0 shows "protocol down" — check encapsulation/config
  STEP 2 (L2): Protocol down could be a VLAN or family inet missing on unit 0
  STEP 3 (L3): With the only interface down, OSPF has no neighbors → no IGP routes to ANY peer
  STEP 4 (MPLS): No IGP routes → LDP sessions go Nonexistent (can't reach loopbacks)
  STEP 5 (BGP): No loopback reachability → BGP goes Active
  STEP 6 (Services): No BGP → no VPN routes exchanged → VPN-A blackhole
  **KEY INSIGHT:** This is a SINGLE root cause (interface protocol down) with 5 cascading symptoms.
**ROOT CAUSE:** ge-0/0/1.0 protocol down — likely missing `family inet` or address configuration.
**FIX:**
```
show configuration interfaces ge-0/0/1  # Check what's missing
set interfaces ge-0/0/1 unit 0 family inet address 10.1.11.1/24
```
**CONFIDENCE:** HIGH — classic cascading failure pattern.

### Example CASCADE-2: Firewall Filter Blocking LDP (Hidden Root Cause)
**SYMPTOM:** LDP sessions between P13 and all neighbors drop intermittently. OSPF stays up.
**DATA COLLECTED:**
```
P13> show ldp session
  10.255.255.11  Nonexistent
  10.255.255.14  Nonexistent

P13> show ospf neighbor
  10.255.255.11  Full
  10.255.255.14  Full

P13> show firewall filter RE-PROTECT counter
  tcp-646-accept   0
  tcp-646-deny     847  ← LDP packets being DENIED

P13> show configuration firewall filter RE-PROTECT
  term ldp-deny {
    from protocol tcp destination-port 646;
    then discard;
  }
```
**REASONING:**
  STEP 1: OSPF is Full (uses IP protocol 89, not TCP) — so L3 is fine.
  STEP 2: LDP uses TCP port 646. The firewall filter RE-PROTECT has a term that DISCARDS TCP/646.
  STEP 3: This is a HIDDEN root cause — the filter is on the RE (loopback), not on an interface, so it's not obvious.
  STEP 4: Counter shows 847 discarded LDP packets — definitive proof.
**ROOT CAUSE:** Firewall filter "RE-PROTECT" on P13 is blocking LDP TCP/646.
**FIX:**
```
# Change the deny term to accept:
delete firewall filter RE-PROTECT term ldp-deny
set firewall filter RE-PROTECT term ldp-accept from protocol tcp destination-port 646
set firewall filter RE-PROTECT term ldp-accept then accept
# Insert BEFORE the default deny term
insert firewall filter RE-PROTECT term ldp-accept before term default-deny
```
**VERIFICATION:** `show ldp session` — sessions should transition to Operational within 30 seconds.
**CONFIDENCE:** HIGH

---

## System Health Examples

### Example HEALTH-1: High CPU Causing Protocol Flaps
**SYMPTOM:** Multiple protocols flapping on P11 — OSPF neighbors going Up/Down, BGP sessions resetting.
**DATA COLLECTED:**
```
P11> show chassis routing-engine
  CPU utilization: 98% user, 1% system
  Memory utilization: 45%

P11> show system processes extensive | match "rpd|CPU"
  rpd    99.2%  ← Routing Protocol Daemon consuming 99% CPU

P11> show log messages | match "RPD_OSPF|RPD_BGP" | last 20
  RPD_OSPF_NBRDOWN: neighbor 10.255.255.1 (ge-0/0/0.0) state changed from Full to Init
  RPD_BGP_NEIGHBOR_STATE_CHANGED: 10.255.255.12 (Internal AS 65000) old state: Established
```
**REASONING:**
  STEP 1: CPU at 98% with rpd at 99.2% — the routing daemon is overloaded.
  STEP 2: When rpd can't process hello/keepalive packets in time, OSPF dead timer expires and BGP hold timer expires.
  STEP 3: This causes ALL protocol adjacencies to flap simultaneously — a signature of rpd overload.
  STEP 4: Need to identify WHY rpd is at 99% — route churn, config commit loop, or genuine overload.
**ROOT CAUSE:** rpd process overload (99% CPU) causing hello/keepalive packet processing delays → multi-protocol flaps.
**FIX:** Investigate rpd overload cause:
```
show task replication    # Check for replication issues
show route summary       # Check for route table explosion
show system commit       # Check for recent commits that might trigger SPF storms
```
**CONFIDENCE:** MEDIUM — need to identify why rpd is overloaded.

### Example HEALTH-2: Storage Full Preventing Commits
**SYMPTOM:** Config commits fail on PE2 with "error: could not write file."
**DATA COLLECTED:**
```
PE2> show system storage
  Filesystem   Size  Used  Avail  Capacity  Mounted on
  /dev/gpt/junos  2.0G  1.9G  50M    97%    /
```
**REASONING:**
  STEP 1: Root filesystem at 97% capacity — only 50MB free.
  STEP 2: Junos needs space to write the commit file and create rollback snapshots.
  STEP 3: Common cause: accumulated log files, core dumps, or too many rollback versions.
**ROOT CAUSE:** Filesystem full at 97% — cannot write commit files.
**FIX:**
```
request system storage cleanup    # Remove temp files, old rollbacks
file delete /var/log/messages.0.gz    # Delete old compressed logs
file delete /var/crash/*              # Delete core dumps
```
**CONFIDENCE:** HIGH

---

## RSVP-TE Examples

### Example RSVP-1: LSP Down Due to CSPF Failure
**SYMPTOM:** RSVP LSP "PE1-to-PE3" is down. Path computation fails.
**DATA COLLECTED:**
```
PE1> show mpls lsp name PE1-to-PE3 detail
  State: Down
  Last CSPF error: no route found to destination

PE1> show ted database extensive | match "10.255.255.3"
  (no TED entry for PE3's loopback)
```
**REASONING:**
  STEP 1: CSPF (Constrained SPF) cannot find a path to PE3.
  STEP 2: CSPF uses the Traffic Engineering Database (TED) which is populated by IS-IS/OSPF TE extensions.
  STEP 3: PE3's loopback is missing from TED — either TE extensions are not enabled or IGP adjacency to PE3 is broken.
**ROOT CAUSE:** PE3 not appearing in TED — TE extensions disabled or IGP path broken.
**FIX:**
```
# Verify TE is enabled on all routers in the path:
show configuration protocols isis interface <intf> level 2 te-metric
# If missing:
set protocols isis traffic-engineering family inet-mpls
```
**CONFIDENCE:** MEDIUM — need to verify each hop in the path.

---

## Multi-Device Correlation Examples

### Example MULTI-1: Asymmetric Routing Causing BFD Flap
**SYMPTOM:** BFD session between PE1 and P11 flaps every 30 seconds despite OSPF being Full.
**DATA COLLECTED:**
```
PE1> show bfd session detail
  Session to 10.1.11.2 (P11): state Flapping
  Detect time: 300ms  Transmit interval: 100ms
  Adaptive: no

PE1> show ospf interface ge-0/0/1.0 detail
  Metric: 10

P11> show ospf interface ge-0/0/0.0 detail
  Metric: 100

PE1> show route 10.1.11.2
  via ge-0/0/1.0 (direct)

P11> show route 10.1.11.1
  via ge-0/0/2.0 (ospf, metric 20)  ← NOT the direct link!
```
**REASONING:**
  STEP 1: PE1 sends BFD packets directly to P11 via ge-0/0/1.
  STEP 2: But P11 routes BACK to PE1 via ge-0/0/2 (through another router) because the OSPF metric on ge-0/0/0 is 100, higher than the alternate path (metric 20).
  STEP 3: BFD is unidirectionally testing the direct link, but return traffic takes a different path. If the alternate path has jitter > 300ms, BFD detects "failure."
  STEP 4: Root cause is asymmetric OSPF metrics causing asymmetric routing.
**ROOT CAUSE:** Asymmetric OSPF metrics — P11 ge-0/0/0 has metric 100 instead of 10, causing return traffic to take alternate path.
**FIX:**
```
# On P11:
set protocols ospf area 0 interface ge-0/0/0.0 metric 10
```
**CONFIDENCE:** HIGH

---

## Healthy Network Reference

### Example HEALTHY-1: All Protocols Green
**SYMPTOM:** None — routine health check.
**DATA:**
```
All routers:
  OSPF: All adjacencies Full, consistent PtToPt types, matching timers
  IS-IS: All L2 adjacencies Up, matching areas and authentication
  BGP: All sessions Established, routes received > 0
  LDP: All sessions Operational, label bindings present in inet.3
  BFD: All sessions Up with no recent flaps
  Interfaces: All Up/Up, CRC errors = 0, no carrier transitions in 24h
  System: CPU < 30%, Memory < 50%, Storage < 70%, Uptime > 7 days
```
**ANALYSIS:** Network is HEALTHY. All protocol state machines are in their expected terminal states. No cascading failure risk detected.
**CONFIDENCE:** HIGH
