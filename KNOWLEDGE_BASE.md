# AI Network Engineering Knowledge Base
## Juniper Networks — Complete NRE Reference v3.0

> **Version:** 3.0 — Juniper Documentation Enriched Edition  
> **Purpose:** This document is the AI's comprehensive technical brain — injected into specialist prompts.  
> **Coverage:** Junos CLI, Protocols (OSPF, IS-IS, BGP, LDP, RSVP-TE, MPLS), L3VPN, L2VPN/VPLS, Firewall Filters, Policers, CoS, System Administration, Hardware, High Availability, Security, Automation.  
> **Sources:** Juniper TechLibrary (juniper.net/documentation), operational experience, SP best practices.  

---

# SECTION 1: JUNOS CLI FUNDAMENTALS

## 1.1 Junos OS Architecture

### Routing Engine (RE) vs Packet Forwarding Engine (PFE)
- **RE:** Runs Junos OS (FreeBSD-based), handles control plane (routing protocols, CLI, SNMP)
- **PFE:** ASIC/Memory-based, handles data plane (packet forwarding at line rate)
- RE and PFE communicate via internal link
- Control plane failure ≠ data plane failure (existing forwarding continues briefly)

### Process Architecture
```
Key processes (daemons):
  rpd    — Routing Protocol Daemon (OSPF, BGP, IS-IS, LDP, RSVP, static)
  chassisd — Chassis management (alarms, fans, PSU, temperature)
  pfed   — PFE management
  mgd    — Management daemon (CLI, NETCONF, REST)
  dcd    — Device Configuration Daemon
  snmpd  — SNMP daemon
  ntpd   — NTP daemon
  sshd   — SSH server
  alarmd — Alarm daemon
```

### Configuration Model
```
Junos uses a candidate → commit model:
  1. User edits candidate configuration
  2. "commit check" validates syntax and semantics
  3. "commit" activates the candidate → becomes active config
  4. Previous configs stored as rollback 0-49
  5. "rollback N" reverts to previous configuration
```

## 1.2 CLI Modes

### Operational Mode
```
user@router> show ospf neighbor
user@router> ping 10.0.0.1
user@router> traceroute 10.0.0.1
user@router> monitor interface ge-0/0/0
user@router> request system reboot
```

### Configuration Mode
```
user@router> configure               # enter config mode
user@router# set protocols ospf ...   # make changes
user@router# show | compare          # see pending changes
user@router# commit check            # validate only
user@router# commit                  # activate
user@router# commit confirmed 5      # auto-rollback in 5 min if not confirmed
user@router# rollback 1              # revert to previous config
user@router# run show ospf neighbor  # run operational command from config mode
```

### Configuration Mode Variants
```
configure              — shared edit (multiple users can edit)
configure exclusive    — locked edit (only one user can edit)
configure private      — private copy (merge on commit)
```

## 1.3 Show Commands — Complete Reference

### `show interfaces terse`
**Columns:** Interface | Admin | Link | Proto | Local
**Key states:**
- `up/up` = Healthy — interface is admin-enabled and has link
- `up/down` = Admin enabled but physically disconnected (cable/VM/optic issue)
- `down/down` = Administratively disabled (`set interfaces <intf> disable`)

**Filter useful interfaces:** Skip internal/management:
- Skip: `pfe-`, `pfh-`, `pip-`, `bme-`, `jsrv-`, `lc-`, `cb-`, `em-`, `dsc`, `gre`, `ipip`, `tap`, `lsi`, `.local.`, `demux`, `vtep`, `esi`
- Focus on: `ge-*`, `xe-*`, `et-*`, `ae-*`, `lo0`, `irb`

### `show interfaces <intf> extensive`
**Key fields to check:**
- **Input/Output errors:** Should be 0. Non-zero = physical layer problem
- **CRC errors:** Indicates cable or optic issue
- **Input/Output drops:** Policer drops or queue overflow
- **Input/Output discards:** Interface overloaded or filter drops
- **MTU:** Default 1514 for Ethernet. Check both sides match.
- **Speed/Duplex:** Should be auto or explicitly matched on both sides
- **Last flapped:** Recent flap = instability investigation needed
- **Traffic statistics:** bps, pps — shows utilization level

### `show interfaces <intf> media`
Shows physical media info: speed, duplex, MTU, MAC address.
Useful for MTU mismatch troubleshooting.

### `show interfaces <intf> statistics`
Shows counters. Use `clear interfaces statistics <intf>` to reset and watch for new errors.

### `show ospf neighbor`
**Columns:** Address | Interface | State | ID | Pri | Dead
**Healthy state:** `Full`
**Unhealthy states:**
- `Init` = One-way: this side sees hellos, remote doesn't → ACL, MTU, or physical
- `ExStart` / `Exchange` = Stuck in DB exchange → MTU mismatch (most common cause)
- `2Way` = Mutual visibility but no Full → DR/BDR on broadcast, OR type mismatch
- `Down` = No hellos → physical, area mismatch, authentication, or interface not OSPF-enabled
- **Missing entirely** = OSPF not configured on remote, no connectivity, or passive

### `show ospf neighbor detail`
**Additional fields:**
- `Adjacency timer` — how long until dead-interval expires
- `Hello interval` — must match on both sides (default 10s)
- `Dead interval` — must match (default 40s)
- `Retransmit interval` — default 5s
- `Area` — must match between neighbors
- `Authentication type` — none, simple, md5 — must match
- `Options` — capability flags (E=external, L=LLS, N=NSSA)
- `Neighbor uptime` — how long the adjacency has been Full

### `show ospf interface`
**Columns:** Interface | State | Area | DR ID | BDR ID | Nbrs
**State column meanings:**
- `PtToPt` = Point-to-point mode (`interface-type p2p` configured)
- `DR` = This router is the Designated Router on this broadcast segment
- `BDR` = This router is the Backup Designated Router
- `DROther` = Neither DR nor BDR (normal for broadcast with 3+ routers)
- `Waiting` = DR election in progress
- `Down` = OSPF enabled but interface not operational (no IP? link down?)
- `Passive` = Advertised but no adjacency (used for lo0)

**CRITICAL RULE:** If one side is `PtToPt` and the other is `DR/BDR/DROther`, there is an **interface-type mismatch**. The adjacency WILL NOT form or will be unstable. This is the #1 OSPF misconfiguration.

### `show ospf interface detail`
**Additional fields:**
- Hello interval, Dead interval, Retransmit interval
- Authentication type
- Network type
- Passive flag
- Prefix length
- Area type (backbone, stub, NSSA)
- SPF delay and hold time

### OSPF Area Types (Juniper TechLibrary)
**Backbone Area (Area 0.0.0.0):**
- All inter-area traffic must transit Area 0
- Every ABR must have an interface in Area 0
- If physical connectivity to Area 0 impossible → use virtual-link

**Stub Area:**
- Does NOT accept Type 5 External LSAs
- ABR injects default route (0/0) as Type 3 Summary LSA
- Reduces LSDB size for branch routers
- Config: `set protocols ospf area 0.0.0.X stub`

**Totally Stubby Area:**
- Does NOT accept Type 3 Summary OR Type 5 External LSAs
- Only default route from ABR
- Maximum LSDB reduction
- Config: `set protocols ospf area 0.0.0.X stub no-summaries`

**Not-So-Stubby Area (NSSA):**
- Like Stub but allows local redistribution into OSPF via Type 7 LSAs
- ABR translates Type 7 → Type 5 at area border
- Config: `set protocols ospf area 0.0.0.X nssa`

**DR/BDR Election (Broadcast/NBMA Networks):**
- Only on broadcast/NBMA segments (NOT on p2p)
- Highest priority wins DR (default priority = 128)
- Second highest = BDR
- Priority 0 = ineligible for DR/BDR
- DR election is NON-PREEMPTIVE — once elected, DR stays until failure
- All routers form Full adjacency with DR and BDR only
- DROther routers remain in 2Way state with each other (normal)

**Virtual Links:**
- Used when an area cannot physically connect to Area 0
- Configured between two ABRs through a transit area
- Transit area must NOT be a stub area
- Config: `set protocols ospf area <transit-area> virtual-link neighbor-id <remote-router-id> transit-area <transit-area>`

### OSPF Interface Types (Juniper CLI Reference)
**Software auto-selects based on physical interface type:**
- Ethernet/GE/XE/ET → defaults to `broadcast`
- Serial/PPP/T1/E1 → defaults to `point-to-point`

**Manual override options (`interface-type`):**
| Type | DR/BDR | Hellos | Use Case |
|------|--------|--------|----------|
| `p2p` | No | Multicast 224.0.0.5 | Standard for all SP core links |
| `broadcast` | Yes | Multicast 224.0.0.5/6 | Multi-access LAN with OSPF |
| `nbma` | Yes | Unicast | Frame Relay/ATM with DR election |
| `p2mp` | No | Unicast | Partial mesh Frame Relay/ATM |
| `p2mp-over-lan` | No | Multicast | Point-to-multipoint over Ethernet |

**CRITICAL:** When overriding, BOTH sides of a link MUST use the same type. Mismatch = adjacency failure.

### `show ospf database`
**LSA Types:**
- `Router` (Type 1) = Every router originates one per area. Contains all links.
- `Network` (Type 2) = DR originates for broadcast/NBMA networks (NOT for p2p)
- `Summary` (Type 3) = ABR originates for inter-area routes
- `ASBRSummary` (Type 4) = ABR originates to reach ASBRs
- `External` (Type 5) = ASBR originates for redistributed routes
- `NSSA` (Type 7) = Like Type 5 but for NSSA areas
- `OpaqArea` (Type 10) = Opaque LSA, area scope (used by MPLS TE)
- `OpaqAS` (Type 11) = Opaque LSA, AS scope

**Diagnostic use:**
- Missing Router LSA = router has no OSPF adjacency in that area
- Multiple Network LSAs for same subnet = possible DR election issue
- Inconsistent LSDB between routers = partial adjacency or area mismatch

### `show ospf database detail`
Shows full LSA contents including:
- Link types and link IDs
- Metrics
- Advertising router
- LSA age (max 3600s, then refreshed)
- Sequence number (higher = newer)

### `show ospf route`
Shows OSPF-computed routes (SPF results). Includes:
- Destination prefix
- Area
- Next-hop interface
- Metric
- Route type (Intra, Inter, Ext1, Ext2)

### `show ospf statistics`
Shows OSPF packet counters:
- Hello, DB Description, LS Request, LS Update, LS Acknowledge
- Errors: auth failures, bad packet, bad area, etc.
- SPF runs and last SPF time

### `show bgp summary`
**Columns:** Groups | Peers | Down Peers (header)
**Per-peer:** Peer | AS | InPkt | OutPkt | OutQ | Flaps | Last | Up/Down | State|#Active/#Received/#Accepted
**State meanings:**
- Number (e.g., `5/10/2`) = **Established** ✅ — Active/Received/Accepted prefixes
- `Active` = TCP connection attempted, remote unreachable → check IGP first
- `Idle` = Not trying → disabled, policy rejection, or max-prefix limit
- `Connect` = TCP SYN sent → remote not listening on port 179
- `OpenSent` = TCP connected, OPEN sent → waiting for peer response
- `OpenConfirm` = OPEN received → parameter mismatch (AS, hold-time, capabilities)
- `Idle(Admin)` = Peer administratively disabled

**CRITICAL:** `Active` state with OutPkt=0 means BGP has NEVER exchanged messages. This is almost always caused by IGP failure — the loopback peering address is unreachable.

### BGP Session States (Juniper TechLibrary — Detailed)
The BGP finite state machine has 6 states:
1. **Idle** — Waiting for a Start event. BGP refuses all incoming connections. After Start event, initializes resources, starts ConnectRetry timer, initiates TCP transport, listens for TCP connection, transitions to Connect.
2. **Connect** — Waiting for TCP connection to complete. If TCP succeeds → send OPEN → move to OpenSent. If TCP fails → restart ConnectRetry timer → move to Active. If ConnectRetry expires → restart timer, initiate new TCP, stay in Connect.
3. **Active** — Trying to acquire a peer by initiating TCP transport. If TCP succeeds → send OPEN → move to OpenSent. **Flip-flopping between Connect and Active indicates TCP transport problem** (firewall, wrong IP, wrong port, remote not listening).
4. **OpenSent** — OPEN message sent, waiting for peer OPEN. Compares AS numbers, checks BGP version (must be 4), validates fields. If mismatch → sends NOTIFICATION → moves to Idle.
5. **OpenConfirm** — Received valid OPEN from peer, sent KEEPALIVE, waiting for peer KEEPALIVE. If KEEPALIVE received → move to Established. If NOTIFICATION or error → move to Idle.
6. **Established** — Final operational state. Peers exchange UPDATE messages. Route information is exchanged. Connection remains until NOTIFICATION, error, or admin action.

### BGP Path Selection Algorithm — Junos 15-Step Decision (Juniper TechLibrary)
When multiple paths exist for the same prefix, Junos selects the BEST path using these steps IN ORDER:
```
Step 1:  Next-hop must be RESOLVABLE (reachable via IGP/static). Unreachable = reject.
Step 2:  Lowest PREFERENCE value (routing-options preference — Junos-specific, default 170)
Step 3:  Highest LOCAL-PREFERENCE (default 100, set via policy)
Step 4:  Shortest AIGP metric (Accumulated IGP — if enabled)
Step 5:  Shortest AS-PATH length (fewer AS hops preferred)
Step 6:  Lowest ORIGIN value (IGP=0 < EGP=1 < Incomplete=2)
Step 7:  Lowest MED (Multi-Exit Discriminator — compared ONLY between paths from same neighbor AS)
Step 8:  Strictly INTERNAL paths preferred over external (within same AS)
Step 9:  EBGP paths preferred over IBGP paths
Step 10: Lowest IGP metric to BGP next-hop (nearest exit / hot-potato routing)
Step 11: For EBGP: oldest route preferred (stability). For IBGP: shortest cluster-list length
Step 12: Lowest ROUTER-ID of advertising router
Step 13: Shortest CLUSTER-LIST length (fewer RR reflections preferred)
Step 14: Lowest PEER IP address (final tiebreaker)
Step 15: PRIMARY path preferred over SECONDARY (for add-path scenarios)
```
**Key insight:** Steps 1-3 are most commonly decisive in real networks. Local-preference is the primary knob for traffic engineering within an AS.

### BGP Message Types (Juniper TechLibrary)
| Message | Function |
|---------|----------|
| **OPEN** | Initiates session — carries AS number, hold time, BGP ID, capabilities |
| **UPDATE** | Advertises new routes or withdraws old routes — carries NLRI, path attributes |
| **KEEPALIVE** | Confirms peer is alive — sent every hold-time/3 seconds (default 20s for 60s hold) |
| **NOTIFICATION** | Reports errors — causes session teardown. Contains error code + subcode |
| **ROUTE-REFRESH** | Requests peer to re-send routes for an address family (RFC 2918) |

### BGP Troubleshooting — Key Commands (Juniper TechLibrary)
**Verification checklist:**
1. `show bgp summary` → Check Down peers, State column (Active = not established)
2. `show route advertising-protocol bgp <peer>` → What are we sending?
3. `show route receive-protocol bgp <peer>` → What did we receive?
4. `show route <prefix> detail` → Check **Inactive reason** field:
   - `Not Best in its group` = another path won selection
   - `IGP metric` = lost at Step 10
   - `Local Preference` = lost at Step 3
   - `AS path` = lost at Step 5
   - `Router ID` = lost at Step 12
   - `Next hop unusable` = failed Step 1 (IGP broken)

**Common BGP misconfigurations:**
- Missing `local-address` statement → BGP uses physical interface IP instead of loopback
- Using interface address instead of loopback as neighbor → session breaks on link failure
- IBGP requires full mesh or route-reflector — partial mesh = missing routes
- EBGP next-hop-self policy needed on border routers for IBGP redistribution

### `show bgp neighbor <peer-ip>`
**Key fields:**
- Peer state and last state change
- Local/Remote AS
- Hold time and keepalive interval
- Address families (AFI/SAFI): inet-unicast, inet-vpn-unicast, inet6-unicast, l2vpn, etc.
- Import/Export policies
- Prefix counts per family
- Last error message
- Flap count and last flap

### `show bgp neighbor <peer> received-routes`
Shows all routes received from this peer before import policy.

### `show bgp neighbor <peer> advertised-routes`
Shows all routes advertised to this peer after export policy.

### `show route protocol bgp`
Shows all routes learned via BGP in the routing table.

### `show route table bgp.l3vpn.0`
Shows all L3VPN routes in the VPNv4 table.

### `show ldp session`
**Columns:** Address | State | Connection | Hold time | Adv. Mode
**State meanings:**
- `Operational` = Healthy ✅ — labels being exchanged
- `Nonexistent` = No TCP connection → loopback unreachable (fix IGP first)
- `Closed` = Session was up but closed → keepalive timeout, transport change, or config removed
- `Initialized` = TCP connecting → may succeed soon or fail

### `show ldp session detail`
**Key fields:**
- Transport address (usually loopback)
- Keepalive interval and hold time
- Label advertisement mode (DU = Downstream Unsolicited)
- Session uptime
- Statistics: labels advertised/received

### `show ldp neighbor`
Shows directly connected LDP neighbors (Hello adjacencies).
- If empty but LDP configured → check: `family mpls` on interface, LDP on interface
- Neighbor appears before session (Hello → TCP → Session)

### `show ldp database`
Shows all labels learned and advertised per session.
- Input labels: labels learned from this neighbor
- Output labels: labels advertised to this neighbor

### `show ldp interface`
Shows LDP-enabled interfaces. All core interfaces should be listed.

### LDP Fundamentals (Juniper TechLibrary)
**LDP Protocol Mechanics:**
- LDP uses **Downstream Unsolicited (DU)** mode — labels advertised without being requested
- LDP discovers neighbors via UDP Hello messages (port 646) on directly connected interfaces
- After Hello, establishes TCP session (port 646) for label exchange
- Transport address (usually loopback) determines TCP session endpoints
- LDP MUST be configured on the SAME interfaces as the IGP — if IGP runs on an interface but LDP doesn't, remote loopbacks via that path will have no labels

**LDP over RSVP Tunneling:**
- LDP can use RSVP-TE LSPs as single "virtual hops"
- Enables combining LDP's simplicity with RSVP-TE's traffic engineering
- LDP sees the RSVP tunnel as a direct adjacency
- Config: LDP automatically tunnels over RSVP LSPs when both are configured on same interfaces

**LDP Session Protection:**
- Maintains LDP session and labels during brief IGP outages
- Prevents label churn during link flaps
- Config: `set protocols ldp session-protection timeout 600`
- Recommended for all SP networks

### `show mpls interface`
Shows MPLS-enabled interfaces. Must match LDP interfaces (except lo0).

### `show mpls lsp`
Shows MPLS Label Switched Paths (RSVP-TE).
**States:**
- `Up` = LSP is active and forwarding ✅
- `Down` = LSP failed — check RSVP errors
- `Detour` = Using Fast Reroute detour path

### `show mpls lsp detail`
Full LSP details: ERO (explicit route), RRO (record route), bandwidth, metrics.

### `show route table mpls.0`
Shows MPLS label forwarding table. Maps incoming labels to outgoing labels and next-hops.
- Pop = remove label (penultimate hop popping)
- Swap = change label and forward

### `show route table inet.3`
Shows BGP next-hop resolution table. Populated by LDP/RSVP.
- Used for resolving BGP next-hops in VPN scenarios
- If empty → LDP/RSVP not working → BGP VPN routes won't resolve

### `show route <prefix>`
Shows all routes for a specific prefix across all tables.
- Check protocol, next-hop, preference, metric
- Active route marked with `*`

### `show route <prefix> detail`
Full route details: communities, AS-path, local-preference, MED, etc.

### `show route summary`
Route count per table and protocol. Key tables:
- `inet.0` = IPv4 unicast
- `inet.3` = BGP next-hop resolution (LDP/RSVP)
- `inet6.0` = IPv6 unicast
- `mpls.0` = MPLS label table
- `bgp.l3vpn.0` = L3VPN routes
- `<VRF>.inet.0` = VRF routing table

### `show chassis alarms`
- `No alarms currently active` = Healthy ✅
- Common alarms:
  - `License` = Junos feature license expired
  - `FPC` = Line card issue
  - `Fan` = Fan failure
  - `PSU` = Power supply failure
  - `Temperature` = Overheating

### Chassis Alarms — Deep Reference (Juniper TechLibrary)
**Key principle:** Chassis alarms are **PRESET by Junos**. You CANNOT modify or create them. You CANNOT clear them — you MUST remedy the underlying cause.

**Alarm Classes:**
| Class | LED Color | Severity | Response |
|-------|-----------|----------|----------|
| Major | 🔴 Red | Service-affecting or hardware failure | Immediate |
| Minor | 🟡 Yellow | Degraded or approaching threshold | Same day |

**Output fields from `show chassis alarms`:**
- **Alarm time** — timestamp when alarm was raised
- **Class** — Major or Minor
- **Description** — human-readable alarm text

**Common Alarm Descriptions and Meaning:**
| Alarm Text | Class | Root Cause | Action |
|------------|-------|------------|--------|
| `PEM X Not Present` | Major | Power Entry Module removed/failed | Replace PEM, check power |
| `PEM X Not OK` | Major | PEM installed but not functioning | Reseat or replace PEM |
| `Fan Tray X Not Present` | Major | Fan tray missing | Install fan tray |
| `Fan Tray X Not OK` | Major | Fan tray installed but failing | Replace fan tray |
| `FPC X Major Errors` | Major | Line card hardware error | Check `show chassis fpc`, RMA if persistent |
| `FPC X Not Powered` | Minor | Line card powered off | Check `request chassis fpc slot X online` |
| `Loss of communication with <component>` | Major | Internal bus failure | Reseat component, escalate |
| `Backup RE Active` | Minor | Primary RE failed, backup took over | Investigate primary RE |
| `Temperature above normal` | Minor | Approaching thermal threshold | Check fans, ambient temp, airflow |
| `Unreachable destinations` | Minor | FIB has unreachable entries | Check routing table for discard routes |
| `link down on interface` | Minor | Physical link down | Check cable/optics/remote |

**CM_ALARM Error Codes:**
- Error codes follow binary structure: LSB (bit 0) = error type, bits 1-31 = actual error code
- Chip-specific codes: L-chip, M-chip, N-chip, R-chip, I-chip errors
- Use `show chassis alarms detail` for extended error information on platforms that support it

### `show chassis hardware`
Shows installed hardware: RE, FPC, PIC, MIC, optics, serial numbers.
Useful for inventory and RMA.

### `show chassis hardware detail`
Includes part numbers, descriptions, serial numbers for all components.

### `show chassis environment`
Shows temperatures, fan speeds, power supply status.

### `show chassis fpc`
Shows line card status: Online, Offline, Error.

### `show chassis routing-engine`
Shows RE status: CPU utilization, memory, temperature, uptime.
- CPU > 80% sustained = investigate (show system processes extensive)
- Memory > 80% = investigate (show task memory detail)

### `show system uptime`
Shows:
- Current time
- System booted at: [timestamp]
- Last configured at: [timestamp] by [user]
- Uptime: [days hours minutes]

Recent reboot (< 1 hour) = investigate. Check `show system core-dumps`.

### `show system processes extensive`
Shows all processes and CPU usage. If rpd is high:
- Many routes being processed
- SPF running frequently (unstable OSPF)
- BGP UPDATE storm

### `show system core-dumps`
Lists core dump files — indicates process crashes.
Core dumps for `rpd` = routing protocol daemon crashed.

### `show system storage`
Shows filesystem usage. If /var > 90% → clean up logs.

### System Storage — Deep Reference (Juniper TechLibrary)
**Output fields from `show system storage`:**
- **Filesystem** — mount point device
- **Size** — total partition size
- **Used** — space consumed
- **Avail** — space remaining
- **Capacity** — percentage used (THIS is the key metric)
- **Mounted on** — filesystem path

**Critical Filesystems to Monitor:**
| Mount Point | Contains | Threshold | Action |
|-------------|----------|-----------|--------|
| `/dev/gpt/junos` (/) | Junos OS root | > 90% | Investigate — may need cleanup or image management |
| `/var` | Logs, core dumps, crash files | > 80% | `request system storage cleanup` |
| `/config` | Configuration files, rollbacks | > 90% | Reduce rollback count `set system max-configurations-on-flash 5` |
| `/tmp` | Temporary files | > 90% | `request system storage cleanup` |
| `/var/tmp` | Temporary files | > 80% | Manual cleanup of old files |
| `/mfs` (memory FS) | In-memory filesystem | > 80% | Investigate — possible memory leak |

**Storage Cleanup Commands:**
```junos
request system storage cleanup               # interactive cleanup
request system storage cleanup no-confirm    # auto cleanup
file delete /var/log/messages.0.gz           # manual file deletion
file list /var/crash/ detail                 # check crash files
clear log messages                           # clear syslog
```

**Storage Health Rules:**
- Any filesystem > 90% capacity = 🟡 WARNING
- Any filesystem = 100% = 🔴 CRITICAL (can cause commit failures, log loss)
- `/var` filling up often indicates: excessive logging, uncleared core dumps, or audit files

### `show lldp neighbors`
**Columns:** Local Interface | Parent Interface | Chassis Id | Port info | System Name
- Used to build physical topology map
- System Name = remote router hostname
- Maps local interface to remote interface for cross-referencing

### `show lldp neighbors detail`
Additional info: system description, management address, port description.

### `show configuration protocols ospf`
Shows OSPF configuration. Check:
- Area ID (must match between neighbors)
- `interface-type p2p` (must match on both sides of a link)
- Hello/dead intervals (must match)
- Authentication type and key (must match)
- `passive` keyword (passive = no adjacency)
- Reference-bandwidth (affects metric calculation)

### `show configuration protocols bgp`
Shows BGP configuration. Check:
- Groups and types (internal/external)
- Local-address (should be loopback for iBGP)
- Neighbors and peer IPs
- Address families enabled
- Import/export policies
- AS number

### `show configuration protocols ldp`
Shows LDP configuration. Check:
- Interfaces (all core + lo0)
- Transport address (should be loopback)

### `show configuration protocols mpls`
Shows MPLS configuration. Check:
- Interfaces (should match LDP minus lo0)
- LSP definitions (if RSVP-TE)

### `show configuration interfaces`
Full interface configuration including:
- IP addresses
- Family configuration (inet, iso, mpls)
- Description
- MTU
- VLANs
- Unit configuration

### `show route protocol ospf`
Shows routes learned via OSPF. If empty → no OSPF adjacencies up.

### `show route advertising-protocol bgp <peer>`
Shows routes advertised to a BGP peer.

### `show route receive-protocol bgp <peer>`
Shows routes received from a BGP peer.

### `show system ntp status`
Shows NTP synchronization status:
- `stratum` = accuracy level (1-15, lower is better, 16 = unsynchronized)
- `offset` = time difference from source
- `jitter` = time variance

### `show system ntp associations`
Shows NTP peers and their status.

### `show firewall`
Shows firewall filter statistics. Each term shows packet/byte counters.

### `show firewall filter <name>`
Shows specific filter term counters.

### `show policer`
Shows policer statistics — rate limiting counters.

### `show class-of-service interface <intf>`
Shows CoS queue statistics: scheduled, transmitted, dropped, RED drops.

---

# SECTION 2: GOLDEN CONFIGURATIONS

## 2.1 OSPF — Point-to-Point Links

**Standard:** ALL point-to-point links between routers MUST use `interface-type p2p`.
Broadcast mode is ONLY for multi-access LAN segments (very rare in SP cores).

```junos
set protocols ospf area 0.0.0.0 interface ge-0/0/0.0 interface-type p2p
set protocols ospf area 0.0.0.0 interface ge-0/0/0.0 hello-interval 10
set protocols ospf area 0.0.0.0 interface ge-0/0/0.0 dead-interval 40
set protocols ospf area 0.0.0.0 interface lo0.0 passive
```

**Why p2p?**
- No DR/BDR election → faster convergence (10s vs 40s+)
- No Type 2 LSA → smaller LSDB → less memory, faster SPF
- Works on /30 and /31 links
- Avoids #1 misconfiguration: p2p vs broadcast mismatch
- Standard for ALL service provider core networks

## 2.2 OSPF — Multi-Area Design

```junos
# Backbone area (all P and PE routers)
set protocols ospf area 0.0.0.0 interface ge-0/0/0.0 interface-type p2p
set protocols ospf area 0.0.0.0 interface lo0.0 passive

# Stub area (branch offices — no external routes)
set protocols ospf area 0.0.0.1 stub
set protocols ospf area 0.0.0.1 interface ge-0/0/1.0 interface-type p2p

# NSSA area (redistributing into OSPF)
set protocols ospf area 0.0.0.2 nssa
set protocols ospf area 0.0.0.2 interface ge-0/0/2.0 interface-type p2p
```

## 2.3 OSPF — BFD (Bidirectional Forwarding Detection)

```junos
set protocols ospf area 0.0.0.0 interface ge-0/0/0.0 bfd-liveness-detection minimum-interval 300
set protocols ospf area 0.0.0.0 interface ge-0/0/0.0 bfd-liveness-detection multiplier 3
```
BFD provides sub-second failure detection (300ms × 3 = 900ms failover).

## 2.4 OSPF — Authentication

```junos
# MD5 Authentication (recommended)
set protocols ospf area 0.0.0.0 interface ge-0/0/0.0 authentication md5 1 key "secretkey123"
```
Both sides MUST match: type, key-id, and key value.

## 2.5 OSPF — Reference Bandwidth

```junos
set protocols ospf reference-bandwidth 100g
```
Without this, 1G and 10G links get the same metric. Set >= highest link speed.

## 2.6 IS-IS Configuration (Alternative IGP)

```junos
set protocols isis interface ge-0/0/0.0 point-to-point
set protocols isis interface ge-0/0/0.0 level 2 metric 10
set protocols isis interface lo0.0 passive
set protocols isis level 1 disable
set protocols isis level 2 wide-metrics-only
set interfaces lo0 unit 0 family iso address 49.0001.0102.5525.5001.00
```

## 2.7 BGP — iBGP with Loopback Peering

```junos
set routing-options autonomous-system 65000
set routing-options router-id 10.255.255.1

set protocols bgp group IBGP type internal
set protocols bgp group IBGP local-address 10.255.255.1
set protocols bgp group IBGP family inet unicast
set protocols bgp group IBGP family inet-vpn unicast
set protocols bgp group IBGP neighbor 10.255.255.2
set protocols bgp group IBGP neighbor 10.255.255.3
```

**Why loopback peering?**
- Loopback is always up → survives physical link failures
- Works with ECMP
- Standard SP design pattern

## 2.8 BGP — Route Reflector

```junos
# On Route Reflector:
set protocols bgp group IBGP-CLIENTS type internal
set protocols bgp group IBGP-CLIENTS local-address 10.255.255.1
set protocols bgp group IBGP-CLIENTS cluster 10.255.255.1
set protocols bgp group IBGP-CLIENTS family inet-vpn unicast
set protocols bgp group IBGP-CLIENTS neighbor 10.255.255.11

# On Client:
set protocols bgp group IBGP type internal
set protocols bgp group IBGP local-address 10.255.255.11
set protocols bgp group IBGP neighbor 10.255.255.1
```

## 2.9 BGP — eBGP Peering

```junos
set protocols bgp group EBGP type external
set protocols bgp group EBGP peer-as 174
set protocols bgp group EBGP neighbor 198.51.100.1
set protocols bgp group EBGP import IMPORT-FROM-UPSTREAM
set protocols bgp group EBGP export EXPORT-TO-UPSTREAM
```

## 2.10 BGP — Address Families

```junos
family inet unicast       # IPv4
family inet-vpn unicast   # L3VPN
family inet6 unicast      # IPv6
family inet6-vpn unicast  # IPv6 VPN
family l2vpn signaling    # VPLS
family evpn signaling     # EVPN
family route-target       # Route Target Constrained Distribution
```

## 2.11 BGP — Policies

```junos
# Prefix list filtering
set policy-options prefix-list ALLOWED 10.0.0.0/8
set policy-options policy-statement FILTER term 1 from prefix-list ALLOWED
set policy-options policy-statement FILTER term 1 then accept
set policy-options policy-statement FILTER term 2 then reject

# Local preference for primary/backup
set policy-options policy-statement PRIMARY term 1 then local-preference 200
set policy-options policy-statement BACKUP term 1 then local-preference 100

# Community tagging
set policy-options community CUST-A members target:65000:100
set policy-options policy-statement TAG term 1 then community add CUST-A

# AS-path filtering
set policy-options as-path CUSTOMER "^65001$"
set policy-options policy-statement FILTER-AS term 1 from as-path CUSTOMER
set policy-options policy-statement FILTER-AS term 1 then accept
```

## 2.12 LDP Configuration

```junos
set protocols ldp interface ge-0/0/0.0
set protocols ldp interface ge-0/0/1.0
set protocols ldp interface lo0.0
set protocols ldp transport-address 10.255.255.1
set protocols ldp session-protection timeout 600
```

**Key rules:**
- LDP on ALL core-facing interfaces AND lo0.0
- Transport address = loopback IP
- Session protection maintains labels during failover

## 2.13 MPLS Configuration

```junos
set protocols mpls interface ge-0/0/0.0
set protocols mpls interface ge-0/0/1.0
```

**Key rules:**
- MPLS on SAME interfaces as LDP (except lo0)
- Don't forget `family mpls` on the interface itself

## 2.14 RSVP-TE Configuration

```junos
set protocols rsvp interface ge-0/0/0.0
set protocols rsvp interface lo0.0
set protocols mpls label-switched-path LSP-TO-PE2 to 10.255.255.2
set protocols mpls label-switched-path LSP-TO-PE2 bandwidth 500m
```

## 2.15 Interface Configuration — Complete

```junos
# Core interface
set interfaces ge-0/0/0 description "LINK_TO_P12_ge-0/0/1"
set interfaces ge-0/0/0 mtu 9192
set interfaces ge-0/0/0 unit 0 family inet address 10.0.0.1/30
set interfaces ge-0/0/0 unit 0 family iso
set interfaces ge-0/0/0 unit 0 family mpls

# Loopback
set interfaces lo0 unit 0 family inet address 10.255.255.1/32
set interfaces lo0 unit 0 family iso address 49.0001.0102.5525.5001.00

# LAG
set chassis aggregated-devices ethernet device-count 4
set interfaces ae0 aggregated-ether-options lacp active
set interfaces ge-0/0/0 ether-options 802.3ad ae0
```

## 2.16 Static Routes

```junos
set routing-options static route 0.0.0.0/0 next-hop 198.51.100.1
set routing-options static route 192.168.0.0/16 discard   # null route
```

---

# SECTION 3: L3VPN CONFIGURATION AND TROUBLESHOOTING

## 3.1 L3VPN — VRF Configuration

```junos
set routing-instances CUSTOMER-A instance-type vrf
set routing-instances CUSTOMER-A interface ge-0/0/3.100
set routing-instances CUSTOMER-A route-distinguisher 65000:100
set routing-instances CUSTOMER-A vrf-target target:65000:100
set routing-instances CUSTOMER-A vrf-table-label

# PE-CE static
set routing-instances CUSTOMER-A routing-options static route 192.168.1.0/24 next-hop 10.1.1.2

# PE-CE BGP
set routing-instances CUSTOMER-A protocols bgp group CE-A type external
set routing-instances CUSTOMER-A protocols bgp group CE-A peer-as 65001
set routing-instances CUSTOMER-A protocols bgp group CE-A neighbor 10.1.1.2

# PE-CE OSPF
set routing-instances CUSTOMER-A protocols ospf area 0.0.0.0 interface ge-0/0/3.100
```

## 3.2 L3VPN — Troubleshooting

```
Step 1: show route table CUSTOMER-A.inet.0 → local + remote routes?
Step 2: show route table bgp.l3vpn.0 → VPNv4 routes from remote PE?
Step 3: show bgp summary → iBGP to remote PE established + inet-vpn?
Step 4: show route table inet.3 <remote-PE-loopback> → MPLS path exists?
Step 5: Check route-target import/export match on both PEs
```

---

# SECTION 4: L2VPN AND VPLS

## 4.1 VPLS Configuration

```junos
set routing-instances VPLS-A instance-type vpls
set routing-instances VPLS-A interface ge-0/0/3.200
set routing-instances VPLS-A route-distinguisher 65000:200
set routing-instances VPLS-A vrf-target target:65000:200
set routing-instances VPLS-A protocols vpls site-id 1
```

## 4.2 EVPN Configuration

```junos
set routing-instances EVPN-A instance-type evpn
set routing-instances EVPN-A interface ge-0/0/3.300
set routing-instances EVPN-A route-distinguisher 65000:300
set routing-instances EVPN-A vrf-target target:65000:300
set routing-instances EVPN-A protocols evpn
```

---

# SECTION 5: TROUBLESHOOTING DECISION TREES

## 5.1 OSPF Adjacency Not Forming

```
START: "show ospf neighbor" — is the neighbor present?
│
├─ NO neighbor at all
│   ├─ Check "show interfaces terse <intf>" → Is link UP/UP?
│   │   ├─ NO → Fix physical layer (cable/VM/optic)
│   │   └─ YES → Check "show ospf interface" on BOTH sides
│   │       ├─ Interface missing from OSPF output?
│   │       │   └─ Add: set protocols ospf area X interface <intf>
│   │       ├─ Interface shows "Down"?
│   │       │   └─ Check: family inet address configured? Link up?
│   │       ├─ Interface shows "Passive"?
│   │       │   └─ Remove passive or move to correct interface
│   │       └─ Interface shows state but no neighbor?
│   │           ├─ Area ID mismatch → fix area on one side
│   │           ├─ Hello-interval mismatch → fix timers
│   │           ├─ Dead-interval mismatch → fix timers
│   │           ├─ Authentication mismatch → fix auth keys
│   │           └─ Interface-type mismatch (p2p vs broadcast) → fix type
│   │
│   └─ Is "passive" configured? → Passive = no adjacency (by design for lo0)
│
├─ Neighbor in Init state
│   └─ One-way communication
│       ├─ Check MTU on both sides
│       ├─ Check firewall filters
│       └─ OSPF protocol 89 must be allowed
│
├─ Neighbor in ExStart/Exchange
│   └─ MTU MISMATCH is #1 cause
│       ├─ "show interfaces <intf> media | match mtu" on BOTH sides
│       └─ Fix: set interfaces <intf> mtu <value> (match both)
│
├─ Neighbor in 2Way (on broadcast network)
│   └─ Normal for DROther routers
│       If unexpected → should be p2p? Fix: set interface-type p2p BOTH sides
│
├─ Neighbor in Loading
│   └─ Usually transient. If stuck → retransmission issues → check MTU
│
└─ Neighbor in Full → HEALTHY ✅
```

## 5.2 BGP Session Not Establishing

```
START: "show bgp summary" — what state?
│
├─ Active
│   └─ #1 cause: Remote loopback UNREACHABLE
│       ├─ "show route <peer-loopback>" → Route?
│       │   ├─ NO → IGP broken. Fix OSPF/IS-IS first.
│       │   └─ YES → Ping test, check TCP 179, check config
│
├─ Idle → Disabled, max-prefix, or policy issue
├─ Idle(Admin) → Administratively disabled
├─ Connect → Remote not listening on TCP 179
├─ OpenSent → Waiting for peer OPEN message
├─ OpenConfirm → Parameter mismatch (AS, hold-time, capabilities)
└─ Established (prefix count) → HEALTHY ✅
    └─ 0/0/0 = established but no routes → check policies
```

## 5.3 LDP Session Not Forming

```
START: "show ldp session" — what state?
│
├─ Nonexistent → No TCP connection
│   ├─ LDP configured on interface?
│   ├─ lo0.0 in LDP config?
│   ├─ Transport address reachable via IGP?
│   ├─ family mpls on interface?
│   └─ Check LDP hellos: show ldp neighbor
│
├─ Initialized → TCP connecting → wait 30s
├─ Closed → Session was up but dropped → check IGP stability
└─ Operational → HEALTHY ✅
```

## 5.4 MPLS Not Working

```
START: "show mpls interface" — interfaces listed?
│
├─ NO → MPLS not configured. Fix: set protocols mpls interface <intf>
├─ YES but no labels → LDP not distributing. Fix LDP first.
└─ Labels present but traffic not forwarding → Check inet.3, downstream
```

## 5.4.1 MPLS Layered Troubleshooting Model (Juniper TechLibrary)

**Systematic bottom-up approach — check each layer before moving up:**

```
LAYER 1: PHYSICAL
  Commands: show interfaces terse, show interfaces <intf> extensive
  Check: All core interfaces UP/UP, no CRC/input/output errors
  Failure: Fix cable, SFP, remote side before proceeding
     │
LAYER 2: DATA LINK
  Commands: show interfaces <intf> extensive (check encapsulation, MTU)
  Check: Encapsulation matches, MTU consistent across path
  Failure: Fix MTU mismatch, encapsulation type
     │
LAYER 3: IP / IGP
  Commands: show ospf neighbor, show isis adjacency, ping <remote-loopback>
  Check: All IGP adjacencies Full/Up, all loopbacks reachable
  Failure: Fix OSPF/IS-IS issues (type mismatch, area mismatch, timers)
     │
LAYER 4: RSVP (if using RSVP-TE)
  Commands: show rsvp interface, show rsvp session [detail], show rsvp neighbor
  Check: RSVP interfaces listed, reservations active
  Common failures:
    - "CSPF failed: no route toward <destination>" → OSPF-TE not enabled or link not advertised
    - Missing RSVP interface → add: set protocols rsvp interface <intf>
    - Bandwidth unavailable → reduce LSP bandwidth or add links
  Reservation styles:
    - FF (Fixed Filter) — one sender, one reservation
    - SE (Shared Explicit) — multiple senders share reservation
    - WF (Wildcard Filter) — any sender, shared reservation
     │
LAYER 5: MPLS / LSP
  Commands: show mpls interface, show mpls lsp [extensive], show route table mpls.0
  Check: MPLS interfaces listed, LSPs in UP state, label table populated
  Common failures:
    - MPLS label allocation failure → check label range, restart LDP/RSVP
    - Missing MPLS interface → add: set protocols mpls interface <intf>
    - LSP Down → check show mpls lsp name <name> extensive for error reason
  Verification: ping mpls rsvp <lsp-name> (tests MPLS data plane end-to-end)
     │
LAYER 6: BGP / SERVICES
  Commands: show bgp summary, show route table bgp.l3vpn.0, show route table inet.3
  Check: BGP established, VPN routes present, inet.3 has next-hop entries
  Failure: If Layers 1-5 are OK but BGP broken → check BGP-specific config
```

**Key MPLS Troubleshooting Commands:**
```junos
show mpls interface                    # list MPLS-enabled interfaces
show mpls lsp                         # LSP status summary
show mpls lsp extensive               # detailed LSP info with ERO/RRO
show mpls lsp name <name> extensive   # specific LSP troubleshooting
show rsvp session                     # RSVP reservation status
show rsvp session detail              # reservation details
show rsvp interface                   # RSVP-enabled interfaces
show rsvp neighbor                    # RSVP neighbors
show route table mpls.0               # MPLS label forwarding table
ping mpls rsvp <lsp-name>            # test MPLS data plane
ping mpls ldp <fec>                   # test LDP data plane
traceroute mpls rsvp <lsp-name>       # trace MPLS path with labels
```

**Link Protection Verification:**
```junos
# Check if link protection is configured
show configuration protocols rsvp | match protection
show configuration protocols mpls | match fast-reroute

# Verify bypass LSPs
show mpls lsp bypass
show rsvp session bypass

# Link protection vs Node-Link protection
# link-protection: protects against link failure only
# node-link-protection: protects against both node and link failure (preferred)
set protocols rsvp interface <intf> link-protection
set protocols rsvp interface <intf> node-link-protection  # more comprehensive
```

## 5.5 Cascading Failure Analysis

**THE GOLDEN RULE:** In MPLS/VPN networks, failures cascade bottom-up:

```
PHYSICAL LAYER FAILURE (link down)
    └─→ OSPF/IS-IS adjacency drops
        └─→ Routes to remote loopbacks withdrawn
            └─→ LDP sessions go Nonexistent
                └─→ MPLS labels withdrawn
                    └─→ iBGP sessions go Active
                        └─→ VPN routes disappear
                            └─→ Customer traffic BLACKHOLED
```

**ALWAYS fix the LOWEST broken layer first. Everything above auto-recovers.**

### Recovery Timeline After IGP Fix
```
T+0s:    IGP fix applied
T+10s:   OSPF Hellos exchanged
T+30-40s: OSPF adjacency → Full
T+45s:   Routes to loopbacks installed in inet.0
T+50-55s: LDP session → Operational
T+55-60s: MPLS labels distributed
T+60-65s: BGP TCP session connects
T+65-70s: BGP → Established
T+70-90s: VPN tables populated
T+90s:   Full convergence
```

## 5.6 Interface Troubleshooting

```
up/down → Cable? SFP? VM networking? Remote side disabled?
Verify: show interfaces <intf> extensive → check error counters
        show interfaces <intf> media → speed/duplex
        show chassis hardware | match <intf> → hardware status
```

## 5.7 Routing Table Troubleshooting

```
No route → Which protocol should provide it? Check that protocol.
Wrong next-hop → Multiple protocols? Check preference values.

Protocol preferences (lower wins):
  Direct: 0, Static: 5, OSPF-int: 10, IS-IS-L1: 15, IS-IS-L2: 18,
  OSPF-ext: 150, BGP: 170
```

---

# SECTION 6: FIREWALL FILTERS AND SECURITY

## 6.1 RE Protection Filter

```junos
set firewall family inet filter PROTECT-RE term ALLOW-BGP from protocol tcp
set firewall family inet filter PROTECT-RE term ALLOW-BGP from port bgp
set firewall family inet filter PROTECT-RE term ALLOW-BGP then accept

set firewall family inet filter PROTECT-RE term ALLOW-OSPF from protocol ospf
set firewall family inet filter PROTECT-RE term ALLOW-OSPF then accept

set firewall family inet filter PROTECT-RE term ALLOW-LDP from protocol tcp
set firewall family inet filter PROTECT-RE term ALLOW-LDP from port 646
set firewall family inet filter PROTECT-RE term ALLOW-LDP then accept

set firewall family inet filter PROTECT-RE term ALLOW-LDP-UDP from protocol udp
set firewall family inet filter PROTECT-RE term ALLOW-LDP-UDP from port 646
set firewall family inet filter PROTECT-RE term ALLOW-LDP-UDP then accept

set firewall family inet filter PROTECT-RE term ALLOW-SSH from protocol tcp
set firewall family inet filter PROTECT-RE term ALLOW-SSH from port ssh
set firewall family inet filter PROTECT-RE term ALLOW-SSH then accept

set firewall family inet filter PROTECT-RE term ALLOW-ICMP from protocol icmp
set firewall family inet filter PROTECT-RE term ALLOW-ICMP then accept

set firewall family inet filter PROTECT-RE term ALLOW-NTP from protocol udp
set firewall family inet filter PROTECT-RE term ALLOW-NTP from port ntp
set firewall family inet filter PROTECT-RE term ALLOW-NTP then accept

set firewall family inet filter PROTECT-RE term ALLOW-BFD from protocol udp
set firewall family inet filter PROTECT-RE term ALLOW-BFD from port 3784-3785
set firewall family inet filter PROTECT-RE term ALLOW-BFD then accept

set firewall family inet filter PROTECT-RE term ALLOW-RSVP from protocol rsvp
set firewall family inet filter PROTECT-RE term ALLOW-RSVP then accept

set firewall family inet filter PROTECT-RE term DEFAULT-DENY then discard

set interfaces lo0 unit 0 family inet filter input PROTECT-RE
```

## 6.2 Policers

```junos
set firewall policer RATE-1M if-exceeding bandwidth-limit 1m
set firewall policer RATE-1M if-exceeding burst-size-limit 15k
set firewall policer RATE-1M then discard
```

---

# SECTION 7: SYSTEM ADMINISTRATION

## 7.1 System Configuration

```junos
set system host-name P11
set system domain-name lab.example.com
set system name-server 8.8.8.8
set system ntp server 10.0.0.1
set system time-zone America/New_York
set system login message "Authorized Access Only"

set system services ssh root-login deny
set system services ssh protocol-version v2
set system services netconf ssh

set system syslog host 10.0.0.100 any info
set system syslog file messages any notice
set system syslog file interactive-commands interactive-commands any
```

## 7.2 SNMP Configuration

```junos
set snmp community public authorization read-only
set snmp community public clients 10.0.0.0/24
set snmp trap-group TRAPS targets 10.0.0.100
set snmp trap-group TRAPS categories chassis link routing
```

## 7.3 Commit Options

```junos
commit                          # immediate
commit check                    # validate only
commit confirmed 5              # auto-rollback in 5 min
commit at "22:00"               # scheduled
commit comment "description"    # with audit trail
```

## 7.4 Rollback Operations

```junos
show system commit                              # history
show configuration | compare rollback 1         # diff
rollback 1                                      # revert
commit comment "Emergency rollback"             # activate
```

---

# SECTION 8: CLASS OF SERVICE (CoS)

## 8.1 Basic CoS

```junos
# Forwarding classes
set class-of-service forwarding-classes class BEST-EFFORT queue-num 0
set class-of-service forwarding-classes class VOICE queue-num 2
set class-of-service forwarding-classes class NETWORK-CONTROL queue-num 3

# Scheduler
set class-of-service schedulers VOICE-SCHED transmit-rate percent 15
set class-of-service schedulers VOICE-SCHED priority strict-high

# Apply
set class-of-service interfaces ge-0/0/0 scheduler-map QOS-MAP
```

---

# SECTION 9: HIGH AVAILABILITY

## 9.1 Graceful Restart

```junos
set protocols ospf graceful-restart
set protocols bgp group IBGP graceful-restart
set protocols ldp graceful-restart
```

## 9.2 Non-Stop Routing

```junos
set routing-options nonstop-routing
set chassis redundancy graceful-switchover
```

## 9.3 VRRP

```junos
set interfaces ge-0/0/0 unit 0 family inet address 10.0.0.2/24 vrrp-group 1 virtual-address 10.0.0.1
set interfaces ge-0/0/0 unit 0 family inet address 10.0.0.2/24 vrrp-group 1 priority 200
set interfaces ge-0/0/0 unit 0 family inet address 10.0.0.2/24 vrrp-group 1 preempt
```

## 9.4 BFD

```junos
# On OSPF
set protocols ospf area 0 interface ge-0/0/0.0 bfd-liveness-detection minimum-interval 300
set protocols ospf area 0 interface ge-0/0/0.0 bfd-liveness-detection multiplier 3

# On BGP
set protocols bgp group IBGP bfd-liveness-detection minimum-interval 1000
set protocols bgp group IBGP bfd-liveness-detection multiplier 3
```

---

# SECTION 10: NETWORK DESIGN PATTERNS

## 10.1 Service Provider Core

```
[CE] ─── [PE] ─── [P] ─── [P] ─── [PE] ─── [CE]
          │                          │
          └── iBGP (via loopbacks) ──┘
```

**Roles:**
- **P routers:** OSPF + LDP + MPLS only. No BGP. Transit traffic.
- **PE routers:** OSPF + LDP + MPLS + iBGP (inet-vpn). Customer-facing.
- **CE routers:** Customer. Static/eBGP/OSPF to PE.
- **RR:** iBGP route reflector for large networks.

## 10.2 Full Mesh vs Route Reflector

```
Full mesh: n*(n-1)/2 sessions. 5 PEs = 10. 10 PEs = 45.
Use RR when > 4-5 PEs.
```

## 10.3 Area Design

```
Single area (0): Fine for < 50 routers
Multi-area:
  Area 0 = backbone
  Stub = no externals, default from ABR
  Totally Stub = only default from ABR
  NSSA = local redistribution with Type 7
```

---

# SECTION 11: MPLS TRAFFIC ENGINEERING

## 11.1 TE Configuration

```junos
set protocols ospf traffic-engineering
set protocols rsvp interface ge-0/0/0.0
set protocols mpls label-switched-path LSP-TO-PE2 to 10.255.255.2
set protocols mpls label-switched-path LSP-TO-PE2 bandwidth 500m
```

## 11.2 Fast Reroute

```junos
set protocols mpls label-switched-path LSP-TO-PE2 fast-reroute
set protocols rsvp interface ge-0/0/0.0 link-protection
```

## 11.3 Auto-Bandwidth

```junos
set protocols mpls label-switched-path LSP-TO-PE2 auto-bandwidth
set protocols mpls label-switched-path LSP-TO-PE2 auto-bandwidth adjust-interval 300
set protocols mpls label-switched-path LSP-TO-PE2 auto-bandwidth minimum-bandwidth 10m
set protocols mpls label-switched-path LSP-TO-PE2 auto-bandwidth maximum-bandwidth 1g
```

---

# SECTION 12: CONFIGURATION PUSH SAFETY

## 12.1 Pre-Push Checklist

| Step | Action |
|------|--------|
| 1 | Identify exact change and target router(s) |
| 2 | Predict impact — what changes? what might break? |
| 3 | Show exact commands to user for approval |
| 4 | Dry-run if possible |
| 5 | Commit with meaningful comment |
| 6 | Verify immediately with protocol-specific show command |

## 12.2 Common Safe Fixes

```junos
# OSPF interface-type mismatch
set protocols ospf area 0.0.0.0 interface <INTF> interface-type p2p

# Missing OSPF interface
set protocols ospf area 0.0.0.0 interface <INTF> interface-type p2p
set protocols ospf area 0.0.0.0 interface <INTF> hello-interval 10
set protocols ospf area 0.0.0.0 interface <INTF> dead-interval 40

# Missing LDP
set protocols ldp interface <INTF>

# Missing MPLS
set protocols mpls interface <INTF>

# Missing family mpls
set interfaces <INTF> unit 0 family mpls

# Enable disabled interface
delete interfaces <INTF> disable

# Add NTP
set system ntp server <NTP-IP>

# Add description
set interfaces <INTF> description "LINK_TO_<REMOTE>_<REMOTE_INTF>"
```

## 12.3 Rollback Procedure

```junos
configure exclusive
rollback 1
commit comment "Emergency rollback"
```

---

# SECTION 13: ROUTING POLICY

## 13.1 Common Patterns

```junos
# Redistribute static into OSPF
set policy-options policy-statement STATIC-TO-OSPF term 1 from protocol static
set policy-options policy-statement STATIC-TO-OSPF term 1 then accept
set protocols ospf export STATIC-TO-OSPF

# Prefix list filtering
set policy-options prefix-list ALLOWED 10.0.0.0/8
set policy-options policy-statement FILTER term 1 from prefix-list ALLOWED
set policy-options policy-statement FILTER term 1 then accept
set policy-options policy-statement FILTER term 2 then reject

# Community-based VRF import/export
set policy-options community CUST-A members target:65000:100
set routing-instances CUST-A vrf-target target:65000:100
```

---

# SECTION 14: JUNOS AUTOMATION

## 14.1 NETCONF

```
ssh user@router -p 830 -s netconf
Operations: get-config, edit-config, commit, lock, unlock
```

## 14.2 REST API

```junos
set system services rest http port 8080
```

## 14.3 PyEZ

```python
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
dev = Device(host='10.0.0.1', user='admin', password='pass')
dev.open()
with Config(dev, mode='exclusive') as cu:
    cu.load('set system host-name NEWNAME', format='set')
    cu.commit(comment='Changed hostname')
dev.close()
```

---

# SECTION 15: COMMON JUNOS ERROR MESSAGES

## 15.1 CLI Errors

| Error | Meaning |
|-------|---------|
| `syntax error` | Invalid command syntax |
| `unknown command` | Wrong mode (op vs config) |
| `configuration check-out failed` | Another user has exclusive lock |
| `commit failed` | Config validation failed |

## 15.2 Protocol Errors

| Log Message | Meaning | Action |
|-------------|---------|--------|
| `OSPF MTU mismatch` | MTU differs on link | Fix MTU both sides |
| `OSPF hello mismatch` | Timer mismatch | Align timers |
| `OSPF area mismatch` | Area ID differs | Fix area config |
| `OSPF auth mismatch` | Auth key differs | Fix auth keys |
| `BGP NOTIFICATION: cease` | Admin shutdown or max-prefix | Check remote |
| `BGP NOTIFICATION: open error` | Parameter mismatch | Check AS, capabilities |
| `RPD_LDP_NBRDOWN` | LDP neighbor down | Check IGP and interface |

---

# SECTION 16: PERFORMANCE TUNING

## 16.1 OSPF Tuning

```junos
set protocols ospf spf-options delay 200
set protocols ospf spf-options holddown 2000
set protocols ospf reference-bandwidth 100g
set protocols ospf overload timeout 600    # stub router during maintenance
```

## 16.2 BGP Tuning

```junos
set protocols bgp group IBGP graceful-restart
set protocols bgp group IBGP out-delay 5
set protocols bgp group EBGP family inet unicast prefix-limit maximum 1000
set protocols bgp group EBGP family inet unicast prefix-limit teardown 80
```

---

# SECTION 17: MONITORING AND DEBUGGING

## 17.1 Real-Time Monitoring

```junos
monitor interface ge-0/0/0             # live traffic
monitor traffic interface ge-0/0/0 matching "tcp port 179"   # packet capture
```

## 17.2 Traceoptions (Protocol Debugging)

```junos
# OSPF traceoptions — detailed flags (Juniper TechLibrary)
set protocols ospf traceoptions file ospf-trace size 10m files 5
set protocols ospf traceoptions flag hello detail       # hello packet exchange
set protocols ospf traceoptions flag event detail       # state machine events
set protocols ospf traceoptions flag lsa-update detail  # LSA updates
set protocols ospf traceoptions flag spf detail         # SPF calculations
set protocols ospf traceoptions flag error detail       # protocol errors
set protocols ospf traceoptions flag state detail       # state transitions
set protocols ospf traceoptions flag database-description detail  # DD exchange

# BGP traceoptions (Juniper TechLibrary)
set protocols bgp traceoptions file bgp-trace size 10m files 5
set protocols bgp traceoptions flag update detail       # UPDATE messages
set protocols bgp traceoptions flag open detail         # OPEN messages
set protocols bgp traceoptions flag keepalive detail    # KEEPALIVE messages
set protocols bgp traceoptions flag state detail        # FSM state changes
set protocols bgp traceoptions flag route detail        # route processing
set protocols bgp traceoptions flag timer detail        # timer events

# IS-IS traceoptions
set protocols isis traceoptions file isis-trace size 10m files 5
set protocols isis traceoptions flag hello detail
set protocols isis traceoptions flag spf detail
set protocols isis traceoptions flag error detail

# LDP traceoptions
set protocols ldp traceoptions file ldp-trace size 10m files 5
set protocols ldp traceoptions flag error detail
set protocols ldp traceoptions flag event detail
set protocols ldp traceoptions flag session detail

# RSVP traceoptions
set protocols rsvp traceoptions file rsvp-trace size 10m files 5
set protocols rsvp traceoptions flag error detail
set protocols rsvp traceoptions flag state detail
set protocols rsvp traceoptions flag path detail
set protocols rsvp traceoptions flag resv detail

# IMPORTANT: Remove ALL traceoptions after debugging!
delete protocols ospf traceoptions
delete protocols bgp traceoptions
delete protocols isis traceoptions
delete protocols ldp traceoptions
delete protocols rsvp traceoptions
```

**Traceoptions Best Practices:**
- Always set file size and rotation (`size 10m files 5`)
- Use `detail` flag for maximum information
- Remove traceoptions after debugging — they consume CPU and disk
- View trace output: `show log <trace-filename>` or `monitor start <trace-filename>`
- Trace files stored in `/var/log/`

## 17.3 Diagnostic Commands

```junos
ping 10.0.0.1 source 10.255.255.1 size 1472 do-not-fragment count 5
traceroute 10.0.0.1 source 10.255.255.1 no-resolve
show route forwarding-table destination 10.0.0.1
```

---

# SECTION 18: AUDIT QUALITY STANDARDS

## 18.1 Good Audit Report Contents

1. Device inventory with versions, uptime, serial, RE status
2. Physical topology from LLDP with ASCII diagram
3. Issues ranked: CRITICAL → WARNING → INFO
4. Root cause analysis with evidence
5. Cascading failure chain
6. Cross-reference evidence from BOTH sides
7. Exact fix commands with router names
8. Healthy areas confirmed
9. Prioritized remediation
10. Recovery prediction with timeline

## 18.2 Severity Definitions

| Level | Criteria | Response |
|-------|----------|----------|
| 🔴 CRITICAL | Service-affecting NOW | Immediate |
| 🟡 WARNING | Risk of impact | Same day |
| ℹ️ INFO | Best practice violation | Next maintenance |

## 18.3 Root Cause vs Symptom

**WRONG:**
```
Issue 1: BGP Active → fix BGP
Issue 2: LDP Nonexistent → fix LDP
Issue 3: OSPF 0 neighbors → fix OSPF
```

**CORRECT:**
```
ROOT CAUSE: OSPF interface-type mismatch (P11=PtToPt, P12=DR)
  SYMPTOM: OSPF 0 neighbors
  SYMPTOM: LDP Nonexistent (transport unreachable)
  SYMPTOM: BGP Active (loopback unreachable)
FIX: set protocols ospf area 0 interface ge-0/0/0.0 interface-type p2p (on P12)
RECOVERY: OSPF→Full(40s) → LDP→Operational(60s) → BGP→Established(90s)
```

---

# SECTION 19: THINKING FRAMEWORK

## Step 1: Establish Baseline
- How many routers? Roles? (P/PE/CE/RR)
- Expected protocols? (OSPF, BGP, LDP, MPLS)
- Expected topology?

## Step 2: Check Layer by Layer (Bottom-Up)
```
1. PHYSICAL: All interfaces UP/UP?
2. IGP:      All OSPF/IS-IS adjacencies Full?
3. LDP:      All sessions Operational?
4. BGP:      All sessions Established?
5. MPLS:     mpls.0 populated? inet.3 has entries?
6. SERVICES: VPN tables populated?
```

## Step 3: Identify Root Cause
Start from LOWEST broken layer = root cause.
```
IF physical down → root cause = physical
ELSE IF OSPF broken → root cause = OSPF
ELSE IF LDP broken (OSPF ok) → root cause = LDP config
ELSE IF BGP broken (OSPF/LDP ok) → root cause = BGP config
```

## Step 4: Prescribe Fix
Exact `set` command, exact router, predicted recovery with timeline.

## Step 5: Verify
Check fixed layer + all layers above for cascading recovery.

---

# SECTION 20: FEW-SHOT EXAMPLES

## Example 1: OSPF Type Mismatch

**Data:**
```
P11 show ospf interface: ge-0/0/0.0 PtToPt 0.0.0.0 0 neighbors
P12 show ospf interface: ge-0/0/1.0 DR 0.0.0.0 0 neighbors
```

**Correct Analysis:**
"🔴 CRITICAL: OSPF interface-type mismatch on P11↔P12 link.
- P11 ge-0/0/0.0 = PtToPt, P12 ge-0/0/1.0 = DR (broadcast)
- Root Cause: Network type mismatch prevents adjacency
- Cascade: OSPF down → LDP Nonexistent → BGP Active → VPN broken
- Fix: `set protocols ospf area 0 interface ge-0/0/1.0 interface-type p2p` on P12
- Recovery: OSPF Full(40s) → LDP(60s) → BGP(90s)"

## Example 2: BGP Active (Cascading)

**Data:**
```
P11 show bgp summary: 10.255.255.12 Active, OutPkt=0
P11 show route 10.255.255.12: no route
```

**Correct Analysis:**
"🔴 BGP Active is a SYMPTOM, not root cause. Loopback 10.255.255.12 has no route.
Root cause is IGP (OSPF) failure. Fix OSPF first. BGP auto-recovers."

## Example 3: Healthy Network

**Data:** All OSPF Full, all BGP Established, all LDP Operational, no alarms.

**Correct Analysis:**
"✅ Network HEALTHY. All protocols nominal. No action required."

## Example 4: Multiple Symptoms, Single Root Cause

**Data:**
```
P11: OSPF to P12 = 0 neighbors (type mismatch)
P11: OSPF to P13 = Full ✅
P11: BGP to 10.255.255.12 = Active, BGP to 10.255.255.13 = Established ✅
P11: LDP to 10.255.255.12 = Nonexistent, LDP to 10.255.255.13 = Operational ✅
```

**Correct Analysis:**
"ONE root cause (OSPF mismatch on P11↔P12) causing THREE symptoms.
P11↔P13 is healthy → confirms issue is specific to P11↔P12 link.
Fix OSPF type on P12 → all three symptoms auto-recover."

## Example 5: NTP Warning

"🟡 WARNING: NTP not configured on any router.
Impact: Clock drift → log correlation issues, certificate failures.
Fix: `set system ntp server <IP>` on all routers.
Priority: Low — next maintenance window."

---

# SECTION 22: MPLS DEEP REFERENCE

> **Source:** Juniper TechLibrary — MPLS Overview (juniper.net/documentation/us/en/software/junos/mpls/topics/topic-map/mpls-overview.html)

## 22.1 What Is MPLS?

MPLS (Multiprotocol Label Switching) is a protocol that uses **labels** to route packets instead of IP addresses. Only the **first device** (ingress LER) does a routing lookup and finds the ultimate destination along with a path — called a **label-switched path (LSP)**. Each transit switch pops its label and forwards to the next label in the sequence.

**Key Advantages over conventional forwarding:**
- Packets arriving on different ports can be assigned different labels
- A packet arriving at a particular PE can be assigned a label different from the same packet entering at a different PE
- Labels can represent explicit routes — no need for the packet to carry the full route identity
- Supports traffic engineering for precise control over traffic paths

## 22.2 MPLS Router Roles

| Role | Also Called | Function |
|------|-----------|----------|
| **Label Edge Router (LER)** | Ingress node, PE | Encapsulates IP packets with MPLS labels at network entry |
| **Label Switching Router (LSR)** | Transit, P router | Swaps labels and forwards MPLS packets within the MPLS network |
| **Egress Router** | Egress LER | Removes the last label before packets leave the MPLS network |

**Service Provider Terminology:**
- **P router** = Provider backbone router (label switching only)
- **PE router** = Provider Edge (customer-facing, terminates IP/L3VPN/L2VPN/VPLS)
- **CE router** = Customer Edge (communicates with PE)

## 22.3 MPLS Configuration Steps

### Configure LSRs (Transit Routers):
```junos
# 1. Enable MPLS on interfaces
[edit interfaces ge-0/0/0 unit 0]
family mpls;

# 2. Add interfaces under MPLS protocol
[edit protocols mpls]
interface ge-0/0/0;

# 3. Configure label distribution protocol (LDP)
[edit protocols ldp]
interface ge-0/0/0.0;
```

### Configure Ingress/Egress LER:
- Create one or more **named paths** on ingress and egress routers
- For each path, specify some/all transit routers, or leave empty for dynamic path

## 22.4 MPLS Protocol Interactions

| Protocol | Role with MPLS |
|----------|---------------|
| **RSVP-TE** | Reserves bandwidth for LSPs (traffic engineering) |
| **LDP** | Defacto label distribution protocol; usually tunneled inside RSVP-TE |
| **IGP (OSPF/IS-IS)** | PE and P routers run IGP to find optimal paths to BGP next hops |
| **BGP** | PE routers exchange customer prefixes; determines routes automatically |
| **OSPF/IS-IS** | Used for routing between MPLS PE and CE; VRF-aware instances |

## 22.5 MPLS Technologies

- **FRR (Fast Reroute):** Pre-computed alternate LSPs for rapid convergence on failure
- **Link Protection:** Bypass LSP for every possible link failure
- **Node Protection:** Bypass LSP for every possible node (switch) failure
- **VPLS:** Ethernet multipoint switching service over MPLS (emulates L2 switch)
- **L3VPN:** IP-based VPN with individual virtual routing domains per customer
- **TTL Processing:** Uniform mode (all nodes visible) vs Pipe mode (only ingress/egress visible)

## 22.6 Cisco ↔ Juniper MPLS Terminology Map

| Cisco Term | Juniper Term |
|-----------|-------------|
| affinities | admin-groups |
| autoroute announce | TE shortcuts |
| forwarding adjacency | LSP-advertise |
| tunnel | LSP |
| make-before-break | adaptive |
| application-window | adjust-interval |
| shared risk link groups | fate-sharing |

## 22.7 Why NOT Use MPLS?

- No protocols to auto-discover MPLS enabled nodes
- Must build the MPLS mesh switch by switch (use scripts)
- MPLS hides suboptimal topologies from BGP
- Large LSPs limited by circuits they traverse (workaround: multiple parallel LSPs)

---

# SECTION 23: SEGMENT ROUTING (SPRING) REFERENCE

> **Source:** Juniper TechLibrary — What Is Segment Routing and SPRING? (juniper.net/documentation/us/en/software/junos/segment-routing/topics/concept/what-is-segment-routing-spring.html)

## 23.1 What Is Segment Routing?

Segment Routing (SR) is a method of generating **instructions** (called **segments**) that indicate how a packet can be forwarded or processed across a topology. Multiple segments can be **stacked together** to define an end-to-end path between any two devices.

**Key Principle:** Segments are advertised **directly inside routing protocols** (IS-IS, OSPF, BGP) — no additional protocol needed.

## 23.2 Segment Types and Examples

Segments can represent these instructions:
- Forward a packet down the **IGP shortest path** to a particular remote router
- Send the packet directly to a **next-hop neighbor** (out a specific interface)
- Override the **BGP best-path** decision at an AS border router
- **Load-balance** between two or more transit/endpoint routers
- Send toward the **nearest border router** out of multiple exit points
- Redirect down a specific **TE tunnel**
- Define a **constrained topology** and forward via shortest path within it
- Remove all segment instructions and process the packet in a specific **L2/L3 forwarding table**

## 23.3 How Segments Are Advertised

Each SR-enabled device generates segments and advertises them via **protocol extensions** in:
- **IS-IS** — TLVs in Link-State PDUs (LSPs)
- **OSPF** — Additional info in Link-State Advertisements (LSAs)
- **BGP** — Between BGP peers

**Result:** Every SR-enabled device has full visibility of every segment instruction advertised by every other node.

## 23.4 Segment Identifiers (SIDs)

| Segment Type | SR-MPLS | SRv6 |
|-------------|---------|------|
| **Node Segment** | MPLS label (SID as index + label block) | IPv6 locator address |
| **Adjacency Segment** | Locally significant MPLS label | End.X SID (IPv6 address) |

**Node Segment:** "Forward to me via IGP shortest path" — tagged to loopback prefix
**Adjacency Segment:** "Send directly to this specific neighbor" — tagged to adjacency

## 23.5 SR-MPLS vs SRv6 Data Plane

- **SR-MPLS:** One MPLS label = one segment. Stack multiple labels for TE paths
- **SRv6:** One or more segments encoded inside IPv6 addresses. Multiple addresses stored in **Segment Routing Header (SRH)** (IPv6 extension header)
- For simple shortest-path forwarding: only **one label/address** needed (BGP-free core)

## 23.6 Key SR Features

- **BGP-free core:** Packets follow IGP shortest path using single node segment
- **Traffic Engineering (SR-TE):** Stack segments for precise path control
- **Backup paths:** Pre-computed segment stacks for fast failover
- **Multi-domain paths:** Segment stacks crossing multiple areas/ASs
- **Multi-topology:** Constrained topologies using flex-algo
- **No signaling required:** All instructions already advertised via IGP

## 23.7 SR Configuration Prerequisites

- Strong working knowledge of **IS-IS or OSPF** required
- Understanding of **MPLS label switching** for SR-MPLS
- Understanding of **IPv6** for SRv6
- Use **Feature Explorer** (apps.juniper.net/feature-explorer) to verify platform support

---

# SECTION 24: LAYER 2 / ETHERNET SWITCHING DEEP REFERENCE

> **Source:** Juniper TechLibrary — Layer 2 Networking (juniper.net/documentation/us/en/software/junos/multicast-l2/topics/topic-map/layer-2-understanding.html)

## 24.1 Layer 2 Fundamentals

**Layer 2 (Data Link Layer)** — the second level in the OSI model. Transfers data between adjacent network nodes in a WAN or between nodes on the same LAN.

**Key Concepts:**
- **Frame:** Smallest unit of bits on a Layer 2 network (defined structure for error detection, control)
- **Unicast:** One node → one node
- **Multicast:** One node → multiple nodes
- **Broadcast:** One node → all nodes in the broadcast domain
- **Broadcast domain:** Logical division where all nodes can be reached at Layer 2

**Sublayers:**
- **LLC (Logical Link Control):** Manages communications links, handles frame traffic
- **MAC (Media Access Control):** Governs protocol access to physical medium; uses MAC addresses

## 24.2 VLANs

A **VLAN** (Virtual LAN) is a collection of network nodes grouped into separate **broadcast domains**. VLANs limit traffic flowing across the LAN, reducing collisions and retransmissions.

- Physical location of nodes doesn't matter — group by department, function, etc.
- Each VLAN identified by **IEEE 802.1Q tag** and unique IP subnetwork
- Frames tagged with 802.1Q to identify VLAN membership

## 24.3 Interface Modes

| Mode | Description | Use Case |
|------|------------|----------|
| **Access** | Connects to end devices (PC, phone, printer). Belongs to single VLAN. Normal Ethernet frames. | Edge ports (default for all ports) |
| **Tagged-Access** | Like access but reflects tagged packets back for VMs on same server. | Cloud/virtualization scenarios |
| **Trunk** | Handles traffic for multiple VLANs multiplexed over same physical connection. | Switch-to-switch interconnects |

**Native VLAN:** Configured on trunk ports to accept untagged data packets. Frames on native VLAN leave trunk port without 802.1Q header.

## 24.4 Layer 2 Features (QFX Series)

- Unicast, multicast, broadcast traffic
- Bridging and VLAN 802.1Q tagging
- **STP** extensions across multiple switches (prevents loops): 802.1d, RSTP, MSTP, Root Guard
- **MAC learning** (per-VLAN MAC learning, Layer 2 learning suppression)
- **Link aggregation (LAG)** — group physical interfaces into single logical interface
- **Storm control** on physical port for unicast/multicast/broadcast

## 24.5 Enhanced Layer 2 Software (ELS) CLI

ELS provides a **uniform CLI** for Layer 2 features across QFX, EX, and other Juniper devices.

### Key ELS Configuration Tasks:

**Configure a VLAN:**
```junos
set vlans vlan-name vlan-id vlan-id-number
set interfaces interface-name family ethernet-switching vlan members vlan-name
```

**Configure Access Interface:**
```junos
set interfaces interface-name unit 0 family ethernet-switching interface-mode access
```

**Configure Trunk Interface:**
```junos
set interfaces interface-name unit 0 family ethernet-switching interface-mode trunk
```

**Configure Native VLAN:**
```junos
set interfaces interface-name native-vlan-id number
set interfaces interface-name unit 0 family ethernet-switching vlan members native-vlan-id-number
```

**Configure IRB Interface (Integrated Routing and Bridging):**
```junos
set vlans vlan-name vlan-id vlan-id
set interfaces irb unit logical-unit-number family inet address ip-address
set vlans vlan-name l3-interface irb.logical-unit-number
```

**Configure LAG (Aggregated Ethernet):**
```junos
# Set number of AE interfaces
set chassis aggregated-devices ethernet device-count number

# Set minimum links and speed
set interfaces aex aggregated-ether-options minimum-links number
set interfaces aex aggregated-ether-options link-speed link-speed

# Add member interfaces
set interfaces interface-name ether-options 802.3ad aex

# Enable LACP
set interfaces aex aggregated-ether-options lacp active
set interfaces aex aggregated-ether-options lacp periodic interval
```

### Key ELS CLI Changes (from legacy):

| Legacy | ELS |
|--------|-----|
| `ethernet-switching-options` | `switch-options` |
| `port-mode` | `interface-mode` |
| `interfaces vlan` | `interfaces irb` |
| `l3-interface vlan.x` | `l3-interface irb.x` |
| `show bridge domain` | `show vlans` |
| `show bridge mac-table` | `show ethernet-switching table` |
| `show l2-learning interface` | `show ethernet-switching interface` |

## 24.6 Layer 2 Transparent Mode (SRX Series)

- Deploys firewall without changing routing infrastructure (acts as L2 switch)
- Device operates in transparent mode when all physical interfaces are Layer 2
- Provides full security services (ALGs, FWAUTH, IDP, Screens, AppSecure)
- **Not supported:** NAT, VPN, STP/RSTP/MSTP, IGMP snooping, Q-in-Q

---

# SECTION 25: VIRTUAL CHASSIS REFERENCE

> **Source:** Juniper TechLibrary — Virtual Chassis Overview for Switches (juniper.net/documentation/us/en/software/junos/virtual-chassis/topics/concept/virtual-chassis-switches-overview.html)

## 25.1 What Is Virtual Chassis?

Virtual Chassis enables interconnecting supported combinations of **EX Series** and **QFX Series** switches into **one logical device** that you configure and manage as a single unit. Member switches are identified by a **member ID** within the Virtual Chassis.

## 25.2 Benefits

- **Simplified management:** Multiple devices managed as single device
- **Increased fault tolerance/HA:** VC remains active when single member fails; traffic redirected
- **Flattened network:** Devices synchronize to one resilient logical device
- **Simplified L2 topology:** Minimizes/eliminates need for STP
- **Flexible expansion:** Add members to increase access ports with minimal topology impact

## 25.3 Member Switch Roles

| Role | Description |
|------|-------------|
| **Primary RE** | Main Routing Engine — handles control plane, manages all members |
| **Backup RE** | Standby Routing Engine — takes over if primary fails (GRES supported) |
| **Linecard** | Forwarding-only role — any VC-capable switch can operate as linecard |

- Standalone switch = single-member VC with member ID `0`, primary role
- **Nonprovisioned VC:** Uses election algorithm for primary/backup selection
- **Preprovisioned VC:** Administrator assigns roles via serial number mapping

## 25.4 Virtual Chassis Ports (VCPs)

VCPs connect member switches and carry all data and control traffic between members.

**VCP Types:**
- **Network/uplink ports:** Can be configured as VCPs (most common)
- **Default factory VCPs:** Pre-configured as VCPs but convertible to network ports
- **Dedicated VCPs:** Fixed VCP-only ports (few switches)

**VCP LAG:** Redundant VCP links of same speed between same two members automatically form a VCP Link Aggregation Group.

**Interface naming:** Member ID functions as FPC slot number: `ge-{member-id}/0/0`

## 25.5 Configuration Modes

**Nonprovisioned:**
- Automatic role election when members interconnect
- Simpler setup, less deterministic control

**Preprovisioned:**
- Associate serial numbers with member IDs
- Deterministic role and ID assignment
- **Autoprovisioning:** Automatic VCP conversion when cabling new switches under certain conditions

## 25.6 High Availability Features

- **Dual Routing Engines:** Standalone switches with single RE gain backup RE capability in VC
- **GRES (Graceful RE Switchover):** Hitless failover between primary and backup
- **Multi-member LAG:** LAG bundles spanning multiple VC members enable traffic redirection on member failure
- **Sub-second convergence** on device or link failure

## 25.7 Global Management

- **Console port:** Connect to any member's console to reach the primary
- **VME (Virtual Management Ethernet):** Single IP address to remotely manage entire VC via any member's management port
- **J-Web:** View VC as single device (where supported)

## 25.8 Mixed Virtual Chassis

- Some switch combinations require **mixed mode** setting for interoperability
- Other combinations work without mixed mode (e.g., switches running same Junos image)
- **EX9200:** Not recommended for VC — migrate to MC-LAG or Junos Fusion Enterprise

---

# SECTION 26: BGP EXPANDED REFERENCE

> **Source:** Juniper TechLibrary — BGP Overview (juniper.net/documentation/us/en/software/junos/bgp/topics/topic-map/bgp-overview.html)

## 26.1 BGP Fundamentals

**BGP (Border Gateway Protocol)** is an EGP used to exchange routing information among routers in different ASs. BGP uses **TCP port 179** for connections, eliminating need for update fragmentation/retransmission.

**Junos OS supports BGP version 4** — adds CIDR support and route aggregation (including AS path aggregation).

**Multiprotocol BGP (MBGP):** Extensions for IPv6 via MP_REACH_NLRI and MP_UNREACH_NLRI attributes.

## 26.2 Autonomous Systems (AS)

An AS is a set of routers under **single technical administration** using a single IGP and common metrics. To other ASs, an AS appears to have a single, coherent interior routing plan.

**AS Path:** Sequence of autonomous systems the route traversed. Used with path attributes to determine network topology, detect/eliminate routing loops, enforce policy.

## 26.3 EBGP vs IBGP Deep Mechanics

| Feature | EBGP | IBGP |
|---------|------|------|
| **Peers** | In different ASs | In same AS |
| **Connectivity** | Normally share a subnet | Can be anywhere in local AS (not directly connected) |
| **Next hop** | Computed from shared interface | Resolved using IGP routes |
| **Function** | Inter-AS routing | Intra-AS routing; propagates external routes to internal routers |

**IBGP groups** use IGP routes to resolve forwarding addresses and propagate external routes among all internal IBGP routers.

**Multiple Instances:** Configured under `[edit routing-instances]` — primarily for **Layer 3 VPN** support. Routes go to `instance-name.inet.0` table.

## 26.4 BGP Route Resolution (Deep)

IBGP routes with next-hop to remote BGP neighbor must have next hop resolved using another route:

1. **Partial resolution:** Protocol next hop resolved via helper routes (RSVP/IGP); metric values derived from helpers
2. **Complete resolution:** Final forwarding next hop derived based on forwarding export policy

**Starting in Junos OS 17.2R1:** Resolver optimized for increased throughput:
- Lower RIB resolution lookup cost (resolver cache)
- BGP route selection triggered only after getting next-hop info from resolver
- Path equivalence groups avoid redundant resolution for paths sharing same forwarding state

## 26.5 BGP RIB Sharding and Update IO

**RIB Sharding:** Splits unified BGP RIB into multiple sub-RIBs, each handled by a separate thread for concurrency.

**Update IO Threads:** Handle generating per-peer updates and sending them. One update thread may serve one or more BGP groups.

```junos
# Enable BGP update threading and RIB sharding
set system processes routing bgp update-threading <number-of-threads>
set system processes routing bgp rib-sharding <number-of-threads>
```

- Update threading: range 1-128
- RIB sharding: range 1-31
- Default threads = number of CPU cores
- Only supported on 64-bit rpd
- Disabled by default

## 26.6 BGP Path Selection — Full 15-Step Algorithm (from official docs)

1. Verify next hop can be resolved
2. Choose path with **lowest preference** value (routing protocol process preference)
3. Prefer path with **higher local preference** (for non-BGP: lowest preference2)
4. If AIGP enabled: add IGP metric, prefer **lower AIGP**
5. Prefer **shortest AS path** (skip if `as-path-ignore` configured)
6. Prefer route with **lowest origin** code (IGP=0 < EGP=1 < Incomplete=2)
7. Prefer **lowest MED** (only compared for same neighbor AS)
8. Prefer **strictly internal paths** (IGP, static, direct, local)
9. Prefer **EBGP paths** over IBGP paths
10. Prefer path with **lowest IGP metric** to next hop
11. If both external: prefer **oldest path** (first learned — minimizes route-flapping)
12. Prefer path from peer with **lowest Router ID**
13. Prefer path with **shortest cluster list** length
14. Prefer path from peer with **lowest peer IP address**
15. Prefer **primary route** over secondary route

## 26.7 Routing Table Path Selection Options

```junos
[edit protocols bgp] path-selection {
    (always-compare-med | cisco-non-deterministic | external-router-id);
    as-path-ignore;
    l2vpn-use-bgp-rules;
    med-plus-igp {
        igp-multiplier number;
        med-multiplier number;
    }
}
```

- `cisco-non-deterministic` — Evaluates routes in order received (not grouped by neighbor AS)
- `always-compare-med` — Compare MEDs regardless of peer AS
- `external-router-id` — Override "prefer oldest external path" rule
- `med-plus-igp` — Add IGP cost to MED before comparison

## 26.8 Key Supported RFCs

| RFC | Description |
|-----|-------------|
| RFC 4271 | BGP-4 specification |
| RFC 4456 | BGP Route Reflection |
| RFC 4364 | BGP/MPLS IP VPNs |
| RFC 4724 | Graceful Restart for BGP |
| RFC 7911 | Advertisement of Multiple Paths (Add-Path) |
| RFC 8326 | Graceful BGP Session Shutdown |
| RFC 8212 | Default EBGP Route Propagation |
| RFC 6811 | BGP Prefix Origin Validation (RPKI) |
| RFC 7432 | BGP MPLS-Based EVPN |
| RFC 5549 | IPv4 NLRI with IPv6 Next Hop |
| RFC 2918 | Route Refresh Capability |
| RFC 3065 | AS Confederations |
| RFC 7854 | BGP Monitoring Protocol (BMP) |
| RFC 8669 | SR Prefix SID Extensions for BGP |

---

# SECTION 27: JUNOS OS PLATFORM & UPGRADE REFERENCE

> **Source:** Juniper TechLibrary — Junos OS & Junos OS Evolved product pages, Getting Started guides, Install/Upgrade guides

## 27.1 Junos OS vs Junos OS Evolved

| Feature | Junos OS | Junos OS Evolved |
|---------|----------|-----------------|
| **Description** | Network OS powering broad portfolio of physical/virtual networking & security products | Next-gen Junos enabling higher availability, faster deployments, rapid innovation |
| **Foundation** | Built for reliability, security, flexibility | Aligned with Junos OS for seamless management & automation |
| **Latest Release** | **25.4R1** | Check juniper.net for latest |
| **CLI Compatibility** | Standard Junos CLI | Same CLI as Junos OS (aligned) |

## 27.2 Getting Started — Key Topics

**First-Time Device Access:**
- Console port connection
- How to access device first time
- Root password configuration

**Management Interfaces:**
- Management Ethernet interfaces overview
- Management interface in dedicated instance (dedicated management VRF)
- Loopback interface overview

**Remote Access:**
- Enable remote access services (SSH, etc.)

## 27.3 Install/Upgrade Guide — Key Topics

### Junos OS:
- Software packages and installation overview
- Upgrading and downgrading Junos OS releases
- System backup and recovery procedures
- Installing and upgrading firmware
- Storage media management
- **ZTP (Zero Touch Provisioning)** — automatic deployment
- Platform-specific: Installing on EX Series, MX Series (via USB), Recovery of Junos OS

### Junos OS Evolved:
- Back up and recover configuration
- Boot by USB drive
- Install/upgrade/downgrade software
- Software installation overview
- **Ensure sufficient disk space** before upgrades

## 27.4 Juniper Support Resources

| Resource | URL |
|----------|-----|
| **Download Software** | support.juniper.net/support/downloads/ |
| **End of Life Dates** | support.juniper.net/support/eol/software/junos/ |
| **PR Search** | prsearch.juniper.net/home |
| **Technical Bulletins** | supportportal.juniper.net |
| **Feature Explorer** | apps.juniper.net/feature-explorer/ |
| **Free Training** | learningportal.juniper.net |
| **Certification** | JNCP program (juniper.net) |
| **CLI Explorer** | juniper.net/documentation/content-applications/cli-explorer/junos/ |
| **Ask AI Chatbot** | Available on Juniper documentation pages |

## 27.5 Junos CLI Reference Guide

The **Junos CLI Reference** provides all Junos CLI commands and configuration statements in two main sections:
1. **Configuration Statements** — All `set` hierarchy statements
2. **Operational Commands** — All `show`, `request`, `clear`, `monitor`, etc. commands

**Useful trending operational commands:**
- `show interfaces diagnostics optics` — Optical transceiver diagnostics
- `monitor traffic` — Real-time packet capture
- `show route` — Routing table lookup
- `show bgp summary` — BGP peer status

## 27.6 Interfaces for Ethernet Switches

**Key topics covered:**
- **Gigabit Ethernet Interfaces** — Physical port configuration
- **Aggregated Ethernet (LAG)** — Link aggregation groups
- **Energy Efficient Ethernet (EEE)** — Power savings on idle links
- **Switching Interface Features** — Access/trunk modes, VLAN membership
- **Optical Transceivers** — SFP/SFP+/QSFP support and diagnostics
- **Port Speed/Channelization** — Speed negotiation, channelized ports
- **Monitor and Troubleshoot Interfaces** — `show interfaces`, diagnostics commands

---

# SECTION 28: JUNOS CLI MASTERY (Source: JNCIA)

## 28.1 The Two CLI Modes

**Operational Mode ( `>` )** — Read-only monitoring and troubleshooting:
- `show interfaces terse` — Summary of all interfaces and status
- `show route` — Display routing table
- `show configuration` — View running config
- `ping` / `traceroute` — Reachability testing
- `monitor traffic interface ge-0/0/0` — Real-time packet capture (tcpdump)
- `clear interface statistics ge-0/0/0` — Reset counters

**Configuration Mode ( `#` )** — Making changes:
- Enter via `configure` from operational mode
- All changes go to **candidate config** (not live)
- `commit` activates changes (atomic transaction)
- `exit` returns to operational mode

## 28.2 Configuration Workflow — Candidate vs Active

Junos NEVER edits the live config directly. You always work on a **candidate configuration**:

1. `configure` — Creates working copy
2. `set` / `delete` / `rename` — Edit the candidate
3. `show | compare` — Diff candidate vs active
4. `commit check` — Validate without applying
5. `commit` — Apply atomically (all-or-nothing)
6. `commit confirmed 5` — Auto-reverts if you get locked out
7. `rollback 0-49` — Revert to previous config

**Key safety features:**
- `commit confirmed <minutes>` — Auto-reverts if you get locked out
- `commit at "2026-02-17 02:00:00"` — Schedule changes for maintenance window
- `commit synchronize` — Sync config across dual REs
- Up to **50 rollback** configurations stored

## 28.3 CLI Navigation Power Features

- **`?`** — Context-sensitive help at any point
- **Tab/Space** — Command completion
- **`| match <regex>`** — Filter output (like grep)
- **`| count`** — Count matching lines
- **`| except <pattern>`** — Exclude lines
- **`| find <pattern>`** — Jump to first match
- **`| last <N>`** — Show last N lines
- **`| display set`** — Show config as set commands
- **`| display xml`** — Show config as XML
- **`help topic <concept>`** — Detailed explanation
- **`help reference <command>`** — Full syntax reference

## 28.4 Interface Naming Convention

Format: `media-type - FPC/PIC/Port`

| Prefix | Type | Speed |
|--------|------|-------|
| `ge` | Gigabit Ethernet | 1 Gbps |
| `xe` | 10-Gigabit Ethernet | 10 Gbps |
| `et` | 100-Gigabit Ethernet | 100 Gbps |
| `so` | SONET/SDH | Various |
| `fxp0` | Management Ethernet | Dedicated |
| `lo0` | Loopback | Virtual |

- **FPC** = Flexible PIC Concentrator (slot number, usually 0 on fixed devices)
- **PIC** = Physical Interface Card (module, usually 0 on fixed devices)
- **Port** = Physical port number

Example: `ge-0/0/0` = Gigabit Ethernet, FPC 0, PIC 0, Port 0

**Physical vs Logical:**
- Physical: `ge-0/0/0` — speed, MTU, link mode
- Logical: `ge-0/0/0.0` (unit 0) — IP address, family, VLAN

## 28.5 Syslog Configuration and Severity Levels

| Level | Name | Description |
|-------|------|-------------|
| 0 | Emergency | System unusable |
| 1 | Alert | Immediate action needed |
| 2 | Critical | Critical conditions |
| 3 | Error | Error conditions |
| 4 | Warning | Warning conditions |
| 5 | Notice | Normal but significant |
| 6 | Info | Informational |
| 7 | Debug | Debug-level messages |

```junos
set system syslog host 10.10.10.100 any notice
set system syslog host 10.10.10.100 authorization info
set system syslog file messages any notice
set system syslog file interactive-commands interactive-commands any
set system syslog file security authorization info
```

Verification: `show log messages | match BGP`

## 28.6 NTP Configuration

```junos
set system ntp server 10.10.10.1
set system ntp server 10.10.10.2
```

Verify: `show ntp status` / `show ntp associations` (look for `*` = active sync source)

## 28.7 SNMP Monitoring

```junos
set snmp community MY-COMMUNITY authorization read-only
set snmp community MY-COMMUNITY clients 10.10.0.0/16
set snmp trap-group ALERTS targets 10.10.10.100
set snmp trap-group ALERTS categories link authentication
```

---

# SECTION 29: ROUTING FUNDAMENTALS DEEP REFERENCE (Source: JNCIA, JIR)

## 29.1 Route Preference (Administrative Distance)

Lower number = more trusted:

| Source | Preference | Analogy |
|--------|-----------|---------|
| Direct | 0 | "I see it myself" |
| Local | 0 | "It is my own address" |
| Static | 5 | "I configured it" |
| OSPF Internal | 10 | "My IGP colleague told me" |
| IS-IS Level 1 Internal | 15 | "IS-IS intra-area" |
| IS-IS Level 2 Internal | 18 | "IS-IS inter-area" |
| RIP | 100 | "Someone far away told me" |
| OSPF AS External | 150 | "Heard through the grapevine" |
| IS-IS Level 1 External | 160 | "IS-IS external L1" |
| IS-IS Level 2 External | 165 | "IS-IS external L2" |
| BGP (eBGP and iBGP) | 170 | "Internet rumor" |

## 29.2 Longest Prefix Match Rule

The most specific route always wins:
```
10.0.0.0/8      -> Interface A  (covers 10.0.0.0 - 10.255.255.255)
10.1.0.0/16     -> Interface B  (covers 10.1.0.0 - 10.1.255.255)
10.1.1.0/24     -> Interface C  (covers 10.1.1.0 - 10.1.1.255)

Destination: 10.1.1.100 -> Winner: 10.1.1.0/24 (most specific)
```

## 29.3 Static Route Variations

```junos
# Basic next-hop
set routing-options static route 192.168.1.0/24 next-hop 10.1.1.254

# Qualified next-hop (primary + backup)
set routing-options static route 192.168.1.0/24 qualified-next-hop 10.1.1.1 preference 10
set routing-options static route 192.168.1.0/24 qualified-next-hop 10.1.1.2 preference 20

# Discard route (black hole - drop silently)
set routing-options static route 192.168.100.0/24 discard

# Reject route (drop + send ICMP unreachable)
set routing-options static route 192.168.200.0/24 reject

# Floating static (backup for dynamic route - higher preference)
set routing-options static route 10.0.0.0/8 next-hop 192.168.1.1 preference 250
```

## 29.4 Aggregate Routes - Summarization

Combine multiple specific routes into one summary:
```junos
set routing-options aggregate route 10.0.0.0/8
# Only exists if at least one contributing route exists
# Automatically advertised instead of specifics
```

## 29.5 Route Troubleshooting Checklist

1. `show route 192.168.1.0/24` — Does route exist?
2. `show route 192.168.1.0/24 detail` — Is it active? What state?
3. `show route 192.168.1.0/24 all` — Show hidden/inactive routes too
4. `show route <next-hop-ip>` — Is next-hop reachable?
5. `show route forwarding-table destination 192.168.1.0/24` — Is it in FIB?

---

# SECTION 30: OSPF COMPREHENSIVE REFERENCE (Source: JNCIA, JIR, AJSPR)

## 30.1 OSPF Packet Types

| Type | Name | Purpose |
|------|------|---------|
| 1 | Hello | Neighbor discovery + keepalive (every 10s default) |
| 2 | DBD (Database Description) | Summary of LSDB during sync |
| 3 | LSR (Link State Request) | Request specific LSA details |
| 4 | LSU (Link State Update) | Carry actual LSA data |
| 5 | LSAck | Acknowledge received LSAs |

## 30.2 OSPF Neighbor State Machine

```
Down -> Init -> 2-Way -> ExStart -> Exchange -> Loading -> Full
```

| State | Meaning |
|-------|---------|
| Down | No hellos received |
| Init | Hello received but not yet two-way |
| 2-Way | Both routers see each other (DR/BDR election happens here) |
| ExStart | Negotiate master/slave for DBD exchange |
| Exchange | Exchanging DBD summaries |
| Loading | Requesting missing LSAs |
| Full | Fully synchronized - adjacency established |

## 30.3 LSA Types

| Type | Name | Generated By | Scope |
|------|------|-------------|-------|
| 1 | Router LSA | Every router | Within area |
| 2 | Network LSA | DR only | Within area |
| 3 | Summary LSA | ABR | Between areas |
| 4 | ASBR Summary LSA | ABR | Between areas |
| 5 | External LSA | ASBR | AS-wide |
| 7 | NSSA External LSA | ASBR in NSSA | Within NSSA (converted to Type 5 at ABR) |

## 30.4 OSPF Area Types

| Area Type | Type 1-2 | Type 3 | Type 4 | Type 5 | Type 7 | Use Case |
|-----------|----------|--------|--------|--------|--------|----------|
| Normal | Yes | Yes | Yes | Yes | No | Standard area |
| Stub | Yes | Yes | No | No | No | Branch offices (gets default route) |
| Totally Stubby | Yes | Default only | No | No | No | Remote sites needing only default |
| NSSA | Yes | Yes | No | No | Yes | Stub + can originate externals |
| Totally NSSA | Yes | Default only | No | No | Yes | Most restrictive + local externals |

Configuration:
```junos
# Stub area (all routers in the area must agree)
set protocols ospf area 0.0.0.1 stub
set protocols ospf area 0.0.0.1 stub default-metric 10

# Totally stubby (ABR adds no-summaries)
set protocols ospf area 0.0.0.1 stub no-summaries default-metric 10

# NSSA
set protocols ospf area 0.0.0.2 nssa
set protocols ospf area 0.0.0.2 nssa default-lsa default-metric 10

# Totally NSSA
set protocols ospf area 0.0.0.2 nssa no-summaries default-lsa default-metric 10
```

## 30.5 Designated Router (DR) Election

On multi-access networks (Ethernet), OSPF elects a DR to reduce adjacency count:

- **DR** — All routers form adjacency with DR (elected by highest priority, then highest Router ID)
- **BDR** — Backup DR (second highest)
- **DROther** — All other routers (only adjacent to DR and BDR, not each other)

Without DR: N*(N-1)/2 adjacencies. With DR: N-1 adjacencies.

```junos
# Set OSPF priority (0 = never become DR)
set protocols ospf area 0.0.0.0 interface ge-0/0/0.0 priority 200
set protocols ospf area 0.0.0.0 interface ge-0/0/0.0 priority 0
```

## 30.6 Virtual Links

Solve the problem of non-contiguous Area 0:

```junos
# On both ABRs - transit area cannot be stub!
set protocols ospf area 0.0.0.1 virtual-link neighbor-id 192.168.1.2 transit-area 0.0.0.1
```

Verify: `show ospf virtual-link`

## 30.7 OSPF External Route Types

**Type 1 (E1)**: External metric + internal path cost  
**Type 2 (E2)**: External metric only (default)

```junos
# Change external metric type
set policy-options policy-statement REDIST term 1 then external type 1
```

## 30.8 OSPF Troubleshooting Methodology

```
Layer 1-2: Interfaces up?
    |
OSPF Neighbors: Adjacencies formed? (show ospf neighbor)
    |- No -> Check Layer 1-3, then BGP config (TCP 179 reachability)
    |- Yes -> Routes Received? (show route receive-protocol bgp <peer>)
        |- No -> Check policies, NLRI, address families
        |- Yes -> Routes Installed? (show route protocol bgp)
            |- No -> Check preference, policies, next-hop resolution
            |- Yes -> Traffic flowing? (verify forwarding-table)
```

Common failure patterns:
- **MTU mismatch** — Adjacency stuck in ExStart/Exchange
- **Area mismatch** — No adjacency forms
- **Hello/Dead timer mismatch** — No adjacency forms
- **Authentication failure** — No adjacency forms
- **Duplicate Router-ID** — Flapping adjacency
- **Interface type mismatch** — PtToPt vs Broadcast/DR mode

Advanced diagnostics:
```junos
set protocols ospf traceoptions file ospf-debug.log size 10m
set protocols ospf traceoptions flag hello detail
set protocols ospf traceoptions flag error
set protocols ospf traceoptions flag lsa-update detail
set protocols ospf traceoptions flag spf detail

show ospf spf log
show ospf database checksum
show task memory detail | match ospf
```

## 30.9 Complete OSPF Deployment Pattern

```junos
# Step 1: Router ID (use loopback)
set interfaces lo0 unit 0 family inet address 10.0.0.1/32
set routing-options router-id 10.0.0.1

# Step 2: OSPF config
set protocols ospf area 0.0.0.0 interface lo0.0 passive
set protocols ospf area 0.0.0.0 interface ge-0/0/0.0 interface-type p2p
set protocols ospf area 0.0.0.0 interface ge-0/0/1.0 interface-type p2p

# Step 3: Export policy (redistribute connected)
set policy-options policy-statement CONNECTED-TO-OSPF term 1 from protocol direct
set policy-options policy-statement CONNECTED-TO-OSPF term 1 from route-filter 192.168.0.0/16 orlonger
set policy-options policy-statement CONNECTED-TO-OSPF term 1 then accept
set protocols ospf export CONNECTED-TO-OSPF

# Step 4: Reference bandwidth for accurate costs
set protocols ospf reference-bandwidth 100g
```

---

# SECTION 31: IS-IS REFERENCE (Source: JIR, AJSPR)

## 31.1 IS-IS vs OSPF Key Differences

| Aspect | OSPF | IS-IS |
|--------|------|-------|
| Runs over | IP (Protocol 89) | Layer 2 directly |
| Areas | Change at ABRs | Levels overlap on same router |
| Addressing | Router-ID (IP) | NET (System ID) |
| Extensibility | New LSA types required | Simple TLVs |
| Packet types | 5 types | 3 PDU types |
| Popular in | Enterprise | ISP/SP cores |

## 31.2 IS-IS Addressing - NET Format

```
NET: 49.0001.0100.0000.0001.00

49      - AFI (private)
0001    - Area ID
0100.0000.0001 - System ID (unique per router)
00      - NSEL (always 00 for routers)
```

**System ID derivation from IP:**
- Loopback 10.0.0.1 -> System ID: 0100.0000.0001
- Loopback 172.16.1.1 -> System ID: 1721.6001.0001

## 31.3 IS-IS Levels

| Level | Scope | Analogy |
|-------|-------|---------|
| Level 1 | Intra-area routing | OSPF internal routes |
| Level 2 | Inter-area routing | OSPF backbone |
| Level 1/2 | Both (default in Junos) | OSPF ABR |

## 31.4 IS-IS PDU Types

| PDU | Purpose |
|-----|---------|
| Hello (IIH) | Neighbor discovery (L1, L2, or P2P variants) |
| LSP | Link state information (like OSPF LSA) |
| CSNP | Complete Sequence Number PDU (database summary) |
| PSNP | Partial Sequence Number PDU (request/acknowledge) |

## 31.5 IS-IS Configuration

```junos
set interfaces lo0 unit 0 family iso address 49.0001.0100.0000.0001.00
set interfaces ge-0/0/0 unit 0 family iso
set protocols isis interface ge-0/0/0.0 point-to-point
set protocols isis interface lo0.0 passive
set protocols isis level 1 disable   # L2-only (common in ISP cores)
set protocols isis level 2 wide-metrics-only
set interfaces lo0 unit 0 family iso address 49.0001.0102.5525.5001.00
```

Verify: `show isis adjacency` / `show isis database` / `show isis route`

## 31.6 IS-IS Wide Metrics

```junos
# Enable wide metrics (required for TE)
set protocols isis level 2 wide-metrics-only
```

## 31.7 IS-IS Route Leaking

Allow L2 routes to be advertised into L1 (inter-area route injection):
```junos
set protocols isis level 1 route-leak from level 2
# OR with policy for selective leaking
set policy-options policy-statement LEAK-L2-TO-L1 from protocol isis
set policy-options policy-statement LEAK-L2-TO-L1 from level 2
set policy-options policy-statement LEAK-L2-TO-L1 then accept
```

## 31.8 IS-IS Troubleshooting

```junos
show isis adjacency                    # Neighbor state
show isis adjacency detail             # Hello timers, circuit type
show isis database                     # LSPDB contents
show isis database extensive           # Full LSP details with TLVs
show isis route                        # IS-IS computed routes
show isis spf log                      # SPF calculation history
show isis interface                    # IS-IS enabled interfaces
show isis statistics                   # PDU counts and errors

# Debug
set protocols isis traceoptions file isis-debug.log size 10m
set protocols isis traceoptions flag error
set protocols isis traceoptions flag spf
set protocols isis traceoptions flag lsp
```

---

# SECTION 32: BGP COMPREHENSIVE REFERENCE (Source: JNCIA, JIR, AJSPR)

## 32.1 BGP Fundamentals

- Uses **TCP port 179** for reliable communication
- Two modes: **eBGP** (between ASes) vs **iBGP** (within same AS)
- BGP is a **path-vector** protocol — makes policy decisions, not shortest-path

| Aspect | eBGP | iBGP |
|--------|------|------|
| **Peers** | In different ASs | In same AS |
| **Connectivity** | Normally share a subnet | Can be anywhere in local AS (not directly connected) |
| **Next hop** | Computed from shared interface | Resolved using IGP routes |
| **Function** | Inter-AS routing | Intra-AS routing; propagates external routes to internal routers |

**IBGP groups** use IGP routes to resolve forwarding addresses and propagate external routes among all internal IBGP routers.

**Multiple Instances:** Configured under `[edit routing-instances]` — primarily for **Layer 3 VPN** support. Routes go to `instance-name.inet.0` table.

## 32.2 BGP Message Types

| Message | Purpose |
|---------|---------|
| OPEN | Establish session (capabilities, ASN, hold time, BGP ID) |
| UPDATE | Advertise/withdraw routes (NLRI + attributes) |
| KEEPALIVE | Maintain session (every 60s default) |
| NOTIFICATION | Report errors (session tears down after) |

## 32.3 BGP Path Selection Algorithm (Decision Order)

1. Highest LOCAL_PREF (default 100)
2. Shortest AS_PATH
3. Lowest ORIGIN (IGP < EGP < Incomplete)
4. Lowest MED (only compared for same neighbor AS)
5. eBGP preferred over iBGP
6. Lowest IGP metric to next-hop
7. Oldest route (most stable)
8. Lowest Router ID

## 32.4 BGP Attributes Deep Dive

**Well-known Mandatory:**
- `AS_PATH` — List of ASes traversed (loop prevention + path selection)
- `NEXT_HOP` — Where to forward packets
- `ORIGIN` — How route entered BGP: IGP (i) > EGP (e) > Incomplete (?)

**Well-known Discretionary:**
- `LOCAL_PREF` — iBGP only, higher = preferred (default 100)
- `ATOMIC_AGGREGATE` — Indicates route aggregation with info loss

**Optional Transitive:**
- `COMMUNITY` — Tags for grouping routes (e.g., no-export, no-advertise)
- `AGGREGATOR` — ASN and IP of aggregating router

**Optional Non-Transitive:**
- `MED` (Multi-Exit Discriminator) — Suggest entry point to neighbor AS (lower wins)
- `CLUSTER_LIST` — Route reflector loop prevention
- `ORIGINATOR_ID` — Route reflector loop prevention

## 32.5 iBGP Next-Hop Problem

**Critical issue:** iBGP does NOT change the next-hop by default:
```
[R-External]---eBGP---[R-Edge]---iBGP---[R-Core]
  10.1.1.1            172.16.1.1         172.16.2.1

R-Core learns routes with next-hop 10.1.1.1 (R-External)
But R-Core has NO route to 10.1.1.1 -> routes are hidden!
```

**Solution:** next-hop-self on iBGP peering:
```junos
set protocols bgp group IBGP-MESH type internal
set protocols bgp group IBGP-MESH local-address 10.0.0.1
set protocols bgp group IBGP-MESH next-hop-self
```

## 32.6 iBGP Full Mesh Problem and Solutions

iBGP split-horizon: routes from iBGP peer NOT re-advertised to other iBGP peers.
Full mesh required: n routers = n(n-1)/2 sessions.

| Routers | Full Mesh Sessions |
|---------|-------------------|
| 4 | 6 |
| 10 | 45 |
| 20 | 190 |
| 100 | 4,950 |

### Solution 1: Route Reflection

```junos
# On the Route Reflector:
set protocols bgp group RR-CLIENTS type internal
set protocols bgp group RR-CLIENTS local-address 10.0.0.1
set protocols bgp group RR-CLIENTS cluster 10.0.0.1
set protocols bgp group RR-CLIENTS neighbor 10.0.0.2
set protocols bgp group RR-CLIENTS neighbor 10.0.0.3

# On clients (simple - just peer with RR):
set protocols bgp group INTERNAL type internal
set protocols bgp group INTERNAL local-address 10.0.0.2
set protocols bgp group INTERNAL neighbor 10.0.0.1
```

**Reflection rules:**
1. Route from eBGP peer -> Reflect to ALL iBGP (clients + non-clients)
2. Route from client -> Reflect to all other clients AND all non-clients
3. Route from non-client -> Reflect only to clients

**Loop prevention attributes:**
- `ORIGINATOR_ID` — Original router ID of route source
- `CLUSTER_LIST` — List of cluster IDs traversed

### Solution 2: Confederations

Divide the AS into smaller sub-ASes:
```junos
set routing-options confederation 65000
set routing-options confederation members 65001 65002 65003

set protocols bgp group CONFED-EBGP type external
set protocols bgp group CONFED-EBGP peer-as 65002
```

## 32.7 BGP Route Damping

Suppresses flapping routes to prevent instability:

| Parameter | Default | Description |
|-----------|---------|-------------|
| Half-life | 15 min | Time for penalty to decay by 50% |
| Suppress threshold | 3,000 | Penalty at which route is suppressed |
| Reuse threshold | 750 | Penalty below which route is reused |
| Max suppress time | 60 min | Maximum time route stays suppressed |

Each flap adds +1,000 penalty. Penalty decays exponentially.

```junos
set protocols bgp group EBGP damping
set policy-options damping AGGRESSIVE half-life 15
set policy-options damping AGGRESSIVE suppress 2000
set policy-options damping AGGRESSIVE reuse 500
set policy-options damping AGGRESSIVE max-suppress 60
```

Verify: `show route damping suppressed`

## 32.8 BGP Troubleshooting Methodology

```
Is BGP Session Up? (show bgp summary)
|- No -> Check Layer 1-3, then BGP config (TCP 179 reachability)
|- Yes -> Routes Received? (show route receive-protocol bgp <peer>)
    |- No -> Check policies, NLRI, address families
    |- Yes -> Routes Installed? (show route protocol bgp)
        |- No -> Check preference, policies, next-hop resolution
        |- Yes -> Traffic flowing? (verify forwarding-table)
```

**Common iBGP issues:**
1. **Next-hop unreachable** — Need next-hop-self or IGP route to next-hop
2. **Route reflection hidden routes** — RR cannot resolve next-hop so will not reflect
3. **Missing MP-BGP family** — Need `family inet-vpn unicast` for L3VPN

**Common eBGP issues:**
1. **TTL problem** — Multi-hop needs `multihop ttl <N>`
2. **AS mismatch** — peer-as must match remote AS
3. **MD5 auth failure** — Keys must match exactly

---

# SECTION 33: ROUTING POLICY ADVANCED REFERENCE (Source: JNCIA, JIR, AJSPR)

## 33.1 Default Policy Behavior

| From | To | Default Action |
|------|----|---------------|
| BGP | OSPF | Reject (not redistributed) |
| OSPF | BGP | Accept (advertised) |
| Static | OSPF | Reject (must create export policy) |
| Direct | OSPF | Reject (must create export policy) |

## 33.2 Policy Structure

```junos
set policy-options policy-statement <name> term <term-name> from <match-conditions>
set policy-options policy-statement <name> term <term-name> then <actions>
```

Processing: Terms evaluated in order. First match wins. If no match then default action applies.

## 33.3 Advanced Route Filter Options

```junos
# exact - Match this exact prefix only
from route-filter 10.0.0.0/8 exact

# orlonger - Match this prefix or anything more specific
from route-filter 10.0.0.0/8 orlonger

# longer - Match only MORE specific (not the prefix itself)
from route-filter 10.0.0.0/8 longer

# upto - Match prefix and specifics up to given length
from route-filter 10.0.0.0/8 upto /24

# prefix-length-range - Match only specific prefix lengths
from route-filter 10.0.0.0/8 prefix-length-range /20-/24

# through - Match range of prefixes
from route-filter 10.0.0.0/16 through 10.0.255.0/24
```

## 33.4 Prefix Lists - Reusable Filters

```junos
# Define prefix list
set policy-options prefix-list CUSTOMER-PREFIXES 192.168.0.0/24
set policy-options prefix-list CUSTOMER-PREFIXES 192.168.1.0/24
set policy-options prefix-list CUSTOMER-PREFIXES 172.16.0.0/20

# Dynamic prefix list from config (auto-populated!)
set policy-options prefix-list CONNECTED-ROUTES apply-path "interfaces <*> unit <*> family inet address <*>"

# Use in policy
set policy-options policy-statement POLICY1 term 1 from prefix-list CUSTOMER-PREFIXES
```

## 33.5 BGP Communities

```junos
# Define community
set policy-options community CUSTOMERS members 65000:100
set policy-options community NO-EXPORT members no-export

# Match community
set policy-options policy-statement FILTER term 1 from community CUSTOMERS

# Set community
set policy-options policy-statement TAG term 1 then community set CUSTOMERS
set policy-options policy-statement TAG term 1 then community add NO-EXPORT

# Delete community
set policy-options policy-statement STRIP term 1 then community delete ALL-COMMUNITIES
```

## 33.6 AS-Path Regular Expressions

```junos
# Define AS-path regex
set policy-options as-path CUSTOMER-AS ".* 65001 .*"
set policy-options as-path DIRECT-PEER "65001"
set policy-options as-path ORIGINATED "65001$"

# Use in policy
set policy-options policy-statement FILTER term 1 from as-path CUSTOMER-AS
```

## 33.7 Classic Use Case: Advertise Default Route into OSPF

```junos
# 1. Define the policy
set policy-options policy-statement ADVERTISE-DEFAULT from protocol static
set policy-options policy-statement ADVERTISE-DEFAULT from route-filter 0.0.0.0/0 exact
set policy-options policy-statement ADVERTISE-DEFAULT then accept

# 2. Apply as OSPF export
set protocols ospf export ADVERTISE-DEFAULT
```

---

# SECTION 34: FIREWALL FILTERS DEEP REFERENCE (Source: JNCIA, JIR)

## 34.1 Filter Structure

Terms processed top-to-bottom. First match wins. **Default action if no term matches = ACCEPT** (unlike routing policy which defaults to reject).

## 34.2 Match Conditions

```junos
from {
    source-address 10.10.0.0/16;
    destination-address 192.168.1.0/24;
    protocol tcp;
    protocol udp;
    source-port 1024-65535;
    destination-port [22 80 443];
    tcp-flags syn;
    icmp-type echo-request;
    packet-size 64-1500;
    dscp ef;
}
```

## 34.3 Actions

| Action | Effect |
|--------|--------|
| accept | Allow packet |
| discard | Drop silently (most common) |
| reject | Drop + send ICMP unreachable |
| count <name> | Increment counter |
| log | Log packet summary |
| policer <name> | Apply rate limiting |
| loss-priority high | Mark for preferential dropping |
| forwarding-class <name> | Assign to CoS queue |

## 34.4 Protect the Routing Engine (Classic Pattern)

```junos
set firewall family inet filter PROTECT-RE term ALLOW-SSH from source-address 10.10.0.0/16
set firewall family inet filter PROTECT-RE term ALLOW-SSH from protocol tcp
set firewall family inet filter PROTECT-RE term ALLOW-SSH from destination-port ssh
set firewall family inet filter PROTECT-RE term ALLOW-SSH then accept

set firewall family inet filter PROTECT-RE term ALLOW-BGP from protocol tcp
set firewall family inet filter PROTECT-RE term ALLOW-BGP from destination-port bgp
set firewall family inet filter PROTECT-RE term ALLOW-BGP then accept

set firewall family inet filter PROTECT-RE term ALLOW-OSPF from protocol ospf
set firewall family inet filter PROTECT-RE term ALLOW-OSPF then accept

set firewall family inet filter PROTECT-RE term ALLOW-ICMP from protocol icmp
set firewall family inet filter PROTECT-RE term ALLOW-ICMP from icmp-type [echo-request echo-reply]
set firewall family inet filter PROTECT-RE term ALLOW-ICMP then accept
set firewall family inet filter PROTECT-RE term ALLOW-ICMP then policer ICMP-RATE

set firewall family inet filter PROTECT-RE term ALLOW-NTP from protocol udp
set firewall family inet filter PROTECT-RE term ALLOW-NTP from destination-port ntp
set firewall family inet filter PROTECT-RE term ALLOW-NTP then accept

set firewall family inet filter PROTECT-RE term DENY-ALL then log
set firewall family inet filter PROTECT-RE term DENY-ALL then discard

# Apply to loopback (gateway to RE)
set interfaces lo0 unit 0 family inet filter input PROTECT-RE
```

---

# SECTION 47: COMMIT OPERATIONS — CONFIRMED, CHECK, ROLLBACK (Source: JNCIA, JIR, JTAC)

## 47.1 Commit Confirm — Safe Remote Changes

`commit confirmed <minutes>` is the **#1 safety mechanism** for remote changes. If you lose connectivity
after a commit, the device **automatically rolls back** after the specified timeout.

### Workflow
```
1. Make configuration changes
2. commit confirmed 5              # Auto-rollback in 5 minutes
3. Verify the change works         # Test connectivity, protocols
4. commit                           # Finalize (cancel the auto-rollback timer)
```

### Critical Rules
- **Always use `commit confirmed` when changing interfaces, routing, or firewall filters remotely**
- If you don't issue a second `commit` within the timer, the router rolls back automatically
- The rollback timer starts when the confirmed commit succeeds
- A second `commit` (without `confirmed`) finalizes the change and cancels the timer
- `commit confirmed` locks the candidate config — other users cannot edit until finalized or rolled back

### Common Scenarios
| Scenario | What Happens |
|----------|-------------|
| Change works, you run `commit` within 5 min | Change is finalized, timer cancelled |
| Change breaks connectivity | Auto-rollback after 5 min restores previous config |
| You forget to finalize | Auto-rollback after timer expires |
| Session disconnects | Timer continues on device, auto-rollback if needed |

### Junos Commands
```junos
commit confirmed 3                 # 3-minute rollback timer
commit confirmed 10                # 10-minute rollback timer
commit                              # Finalize (cancel timer)
show system commit                  # Verify commit history
```

## 47.2 Commit Check — Pre-Validation

`commit check` validates the candidate configuration **without applying** it. Use this to catch
syntax errors, semantic errors, and constraint violations before committing.

```junos
commit check                        # Validate candidate config
# Output: "configuration check succeeds" or error details
```

### What Commit Check Validates
- Syntax correctness (missing brackets, typos)
- Semantic correctness (referenced objects exist, e.g., policy referenced in BGP exists)
- Constraint violations (e.g., duplicate IP addresses, overlapping ranges)
- Interface references (e.g., interface exists in chassis)

### What Commit Check Does NOT Validate
- Runtime behavior (whether the route will work, whether OSPF will form adjacency)
- Remote side configuration (peer's BGP config, neighbor's OSPF area)
- Traffic impact (whether traffic will be dropped during convergence)

## 47.3 Rollback — Configuration Recovery

Junos stores up to **50 rollback configurations** (rollback 0 = current, rollback 1 = previous, etc.).

```junos
show system rollback compare 0 1    # Diff current vs previous config
rollback 1                          # Load previous config into candidate
commit comment "Rollback to previous" # Apply the rollback

# Emergency: rollback to factory defaults
load factory-default
set system root-authentication plain-text-password
commit
```

---

# SECTION 48: OPERATIONAL HEALTH THRESHOLDS & NORMAL BASELINES (Source: JTAC, Operational Experience)

## 48.1 Interface Health Thresholds

| Metric | Normal | Warning | Critical | Action |
|--------|--------|---------|----------|--------|
| CRC Errors | 0 | 1-100 | >100 | Check cable/optic/SFP |
| Input Errors | 0 | 1-50 | >50 | Check MTU, encapsulation |
| Output Errors | 0 | 1-50 | >50 | Check congestion, queuing |
| Drops (input) | 0 | 1-100 | >100 | Check policer, CoS |
| Drops (output) | 0 | 1-100 | >100 | Check queue depth, scheduling |
| Flaps (24h) | 0 | 1-3 | >3 | Check physical layer |
| Carrier transitions | 0 | 1-2 | >2 | Unstable link — replace cable/optic |

## 48.2 System Health Thresholds

| Metric | Normal | Warning | Critical | Action |
|--------|--------|---------|----------|--------|
| CPU (RE) | <50% | 50-80% | >80% | Check routing table size, BGP updates |
| Memory (RE) | <70% | 70-85% | >85% | Check route count, clear caches |
| Storage /var | <80% | 80-90% | >90% | `request system storage cleanup` |
| Storage /var/tmp | <70% | 70-85% | >85% | Delete old packages |
| Uptime | >30 days | 1-30 days | <1 day | Recent crash — check core dumps |
| Temperature | <55°C | 55-65°C | >65°C | Check fans, airflow |
| Core Dumps | 0 | 1 (old) | 1+ (recent) | Check daemon, escalate to JTAC |

## 48.3 Protocol Health Baselines

| Protocol | Metric | Normal | Warning | Critical |
|----------|--------|--------|---------|----------|
| OSPF | Neighbor state | Full | Loading/Exchange | Init/Down |
| OSPF | SPF runs (5 min) | 0-1 | 2-5 | >5 (instability) |
| OSPF | Dead interval | 40s (default) | Custom ok | Mismatch between peers |
| BGP | Session state | Established | OpenConfirm | Active/Idle |
| BGP | Received prefixes | Expected count ±10% | ±20% | >50% deviation or 0 |
| BGP | Flap count (24h) | 0 | 1-3 | >3 |
| LDP | Session state | Operational | Nonexistent (new) | Nonexistent (was up) |
| BFD | Session state | Up | AdminDown | Down |
| BFD | Flaps (1h) | 0 | 1-2 | >2 |
| IS-IS | Adjacency state | Up | Init | Down |

## 48.4 Route Table Baselines

| Table | Expected | Warning Deviation | Investigation |
|-------|----------|-------------------|---------------|
| inet.0 | Stable count ±5% | >10% change in 1h | Route leak, policy change |
| inet.3 | = LDP neighbors | Count mismatch | LDP session issues |
| bgp.l3vpn.0 | Stable per VRF | Sudden increase | Route leak between VRFs |
| mpls.0 | = LSP count × 2 | Significant change | LSP teardown/reroute |

## 48.5 Alarm Severity Classification

| Alarm Text | Severity | Impact | Action |
|------------|----------|--------|--------|
| `Rescue configuration is not set` | LOW | No rescue config backup | `request system configuration rescue save` |
| `Loss of redundancy` | MEDIUM | Single RE running | Monitor, plan maintenance |
| `FPC offline` | CRITICAL | Linecard down, interfaces affected | Check FPC, reseat or replace |
| `PEM failure` | HIGH | Power redundancy lost | Replace PEM |
| `Fan failure` | HIGH | Cooling degraded | Replace fan tray |
| `RE switchover` | CRITICAL | Active RE changed | Check why — crash? manual? |
| `License expired` | MEDIUM | Features may stop working | Renew license |


---

# SECTION 60: ADVANCED JUNOS SERVICE PROVIDER ROUTING — PDF EXTRACTED KNOWLEDGE

> **Source:** Advanced Junos Service Provider Routing study guide (auto-extracted)

## 60.1 Part 2: The Junos CLI Masterclass (The How)

Part 2: The Junos CLI Masterclass (The How)
BGP Troubleshooting Command Hierarchy
IBGP Troubleshooting Patterns
Pattern 1: Systematic IBGP Verification
Pattern 2: IBGP Next-Hop Resolution
But what if 65003 has a better path you want to use?
## Session-level troubleshooting
show bgp summary ## Quick overview
show bgp neighbor <address> ## Detailed neighbor state
show log messages | match BGP ## BGP state changes
## Route-level troubleshooting
show route receive-protocol bgp <peer> ## Pre-policy routes
show route protocol bgp ## Post-policy routes
show route advertising-protocol bgp ## Advertised routes
## Hidden routes investigation
show route hidden ## All hidden routes
show route hidden detail ## Why routes are hidden
## BGP state and statistics
show bgp statistics ## Packet counters
monitor traffic interface <int> matching "port 179"  ## Live BGP packets
## Step 1: Verify IBGP session establishment
user@router> show bgp summary
Groups: 1 Peers: 3 Down peers: 1 ## One peer is down!
Peer AS InPkt OutPkt State|#Active/Received/Accepted
172.16.1.1 65000 142 145 Establ 10/15/12
172.16.2.1 65000 0 0 Active ## Problem peer
172.16.3.1 65000 150 148 Establ 5/8/8
## Step 2: Check specific peer details
user@router> show bgp neighbor 172.16.2.1
Peer: 172.16.2.1 AS 65000 Local: 172.16.0.1+51289 AS 65000
  Type: Internal State: Active ## Stuck in Active state
  Last State: Connect Last Event: ConnectRetry
  Last Error: Hold Timer Expired Error
  Options: <Preference LocalAddress>
  Local
[...truncated...]

## 60.2 Part 1: The Conceptual Lecture (The Why)

Part 1: The Conceptual Lecture (The Why)
Understanding BGP Policy
BGP policy is like international trade policy. Just as countries control imports/exports with tariffs, quotas, and regulations, BGP policies control route
advertisements with filters, preferences, and modifications.
The BGP Next-Hop Attribute
The NEXT_HOP attribute tells routers where to forward packets. It's like the "next shipping hub" in package delivery:
user@peer> show route receive-protocol bgp 10.0.0.1 192.168.0.0/16
# No output
user@router> show route advertising-protocol bgp 10.0.0.2 192.168.0.0/16
# No output - not advertising!
user@router> test policy BGP-EXPORT 192.168.0.0/16
Policy BGP-EXPORT: 0 prefix accepted, 1 prefix rejected
user@router> show route 192.168.0.0/16
# Route exists but not in BGP
# Add route to BGP
set routing-options static route 192.168.0.0/16 discard
set protocols bgp group ISP-PEERS export BGP-EXPORT
user@router> show route 8.8.8.8
8.8.8.8/32 *[BGP/170] via 10.0.1.2  # Using backup ISP!
 [BGP/170] via 10.0.0.2  # Primary not selected
user@router> show route 8.8.8.8 detail
8.8.8.8/32 (2 entries)
  *BGP Preference: 170
 Next hop: 10.0.1.2
 AS path: 65200 15169 I
 Local Preference: 100
 BGP Preference: 170
 Next hop: 10.0.0.2
 AS path: 65100 3356 15169 I
 Local Preference: 100
 # Same local-pref, shorter AS-PATH wins!
set policy-options policy-statement PREFER-PRIMARY term ISP1 from neighbor 10.0.0.2
set policy-options policy-statement PREFER-PRIMARY term ISP1 then local-preferen
[...truncated...]

## 60.3 Part 1: The Conceptual Lecture (The Why)

Part 1: The Conceptual Lecture (The Why)
The BGP Troubleshooting Challenge
BGP is like conducting a symphony orchestra where each musician (router) must play in perfect harmony. When something goes wrong, you need
to determine: Is it the sheet music (configuration)? Is a musician not following the conductor (policy)? Or is someone playing a different song
entirely (mismatch)?
BGP troubleshooting is particularly challenging because:
The BGP Troubleshooting Methodology
user@router> show route 198.41.0.4/32
## Route not in routing table
user@router> show route damping suppressed 198.41.0.4/32
inet.0: 1500 destinations, 1551 routes (1450 active, 0 holddown, 51 hidden)
198.41.0.4/32 [BGP ] 00:05:00, localpref 100
 Damped, Reuse in: 00:10:00  ## Critical route damped!
[edit policy-options]
user@router# set prefix-list NEVER-DAMP 198.41.0.4/32
user@router# set prefix-list NEVER-DAMP 192.5.5.241/32  ## Add all root servers
[edit policy-options policy-statement BGP-DAMPING-POLICY]
user@router# set term NEVER-DAMP from prefix-list NEVER-DAMP
user@router# insert term NEVER-DAMP before term AGGRESSIVE-CUSTOMER
user@router# set term NEVER-DAMP then damping no-damp
user@router# set term NEVER-DAMP then accept
user@router# commit
## Clear existing damping state
user@router> clear bgp damping 198.41.0.4/32
1. Distributed State: Each router maintains its own BGP state
2. Policy Complexity: Multiple policies interact in non-obvious ways
3. Silent Failures: BGP can establish sessions but still 
[...truncated...]

## 60.4 Part 3: Verification & Troubleshooting (The What-If)

Part 3: Verification & Troubleshooting (The What-If)
Essential Verification Commands
# Add IGP cost to MED
set protocols bgp group ISP-PEERS metric-out igp
policy-options {
 prefix-list OUR-NETWORKS {
 192.168.0.0/16;
 172.16.0.0/12;
 as-path CUSTOMER-AS "^65100$";
 as-path PEER-AS "^65200$";
 as-path BOGON-AS ".* (64512|65535) .*";
 
 policy-statement BGP-IMPORT-POLICY {
 term reject-bogons {
 from as-path BOGON-AS;
 then reject;
 term prefer-customer {
 from {
 protocol bgp;
 as-path CUSTOMER-AS;
 then {
 local-preference 150;
 accept;
 term standard-peer {
 from {
 protocol bgp;
 as-path PEER-AS;
 then {
 local-preference 100;
 accept;
 
 policy-statement BGP-EXPORT-POLICY {
 term advertise-our-networks {
 from {
 prefix-list OUR-NETWORKS;
 then {
 metric 100;
 origin igp;
 accept;
 term advertise-customer-routes {
 from {
 protocol bgp;
 as-path CUSTOMER-AS;
 then {
 metric 150;
 as-path-prepend "65001";
 accept;
 term reject-rest {
 then reject;


Troubleshooting Scenarios
Scenario 1: Next-Hop Unreachable in iBGP
Symptom: Routes hidden due to unreachable next-hop
Diagnostic Commands:
Solution:
Scenario 2: MED Not Influencing Path Selection
Symptom: Higher MED path being preferred
Diagnostic Commands:
# Show route with all BGP attributes
user@router> show route 8.8.8.8 detail
8.8.8.8/32 (2 entries, 1 announced)
 *BGP Preference: 170/-101
 Next hop type: Router, Next hop index: 612
 Address: 0x94d4d04
 Next-hop reference count: 150000
 Source: 10.0.0.2
 Next hop: 10.0.0.2 
[...truncated...]

## 60.5 Part 1: The Conceptual Lecture (The Why)

Part 1: The Conceptual Lecture (The Why)
The Fundamental Problem
Imagine you're building a communication network within a large company where every department needs to share information with every other
department. In a small company with 3 departments, you'd need 3 connections. But what happens when you have 100 departments? You'd need
n(n−1)

 connections, which equals 4,950 connections! This is the exact problem BGP faces within an autonomous system.
Understanding IBGP Full Mesh Requirements
BGP (Border Gateway Protocol) is the protocol that routers use to exchange routing information. When BGP runs between routers in the same
autonomous system (AS), we call it IBGP (Internal BGP). IBGP has a fundamental rule: routes learned from one IBGP peer are NOT advertised
to other IBGP peers. This is called the IBGP split-horizon rule.
Why does this rule exist? To prevent routing loops. Since IBGP doesn't modify the AS_PATH attribute (which is BGP's loop prevention mechanism),
it needs another way to prevent loops - hence the split-horizon rule.
Solution 1: Route Reflection
Route Reflection introduces a hierarchical model that breaks the split-horizon rule in a controlled manner. Think of it like creating a hub-and-spoke
communication system in our company analogy - instead of everyone talking to everyone, we designate team leaders (Route Reflectors) who
collect information from their team members and share it with other teams.
Route Reflector Concepts
Route Reflection Rules
Traditi
[...truncated...]

## 60.6 Part 3: Verification & Troubleshooting (The What-If)

Part 3: Verification & Troubleshooting (The What-If)
Essential Verification Commands
Troubleshooting Scenarios
policy-options {
 policy-statement MASTER-IMPORT-POLICY {
 term customers {
 from {
 neighbor [ 10.1.0.0/24 ];
 then {
 community add CUSTOMER-ROUTE;
 local-preference 150;
 next policy;
 term peers {
 from {
 neighbor [ 10.2.0.0/24 ];
 then {
 community add PEER-ROUTE;
 local-preference 100;
 next policy;
 term transit {
 from {
 neighbor [ 10.3.0.0/24 ];
 then {
 community add TRANSIT-ROUTE;
 local-preference 80;
 next policy;
 term filter-bogons {
 from {
 route-filter 0.0.0.0/0 prefix-length-range /25-/32 reject;
 route-filter 10.0.0.0/8 orlonger reject;
 route-filter 192.168.0.0/16 orlonger reject;
 term accept-rest {
 then accept;
# Show routes with communities
user@router> show route community 65001:100 detail
192.168.1.0/24 (1 entry)
 *BGP Preference: 170/-151
 Next hop: 10.1.0.2
 Communities: 65001:100 65001:150
 Local Preference: 150
 
# Show routes with specific local preference
user@router> show route detail | match "Local preference: 200"
 Local preference: 200
# Test policy with specific attributes
user@router> test policy COMPLEX-POLICY 192.168.1.0/24 neighbor 10.1.0.2 community [ 65001:100 65001:200 ]
Policy COMPLEX-POLICY: 1 prefix accepted
# Show all routes with their communities
user@router> show route extensive | match "Communities:|^[0-9]"
192.168.1.0/24
 Communities: 65001:100 no-export
10.0.0.0/24
 Communities: 65001:200 65001:150


Scenario 1:
[...truncated...]

## 60.7 Part 3: Verification & Troubleshooting (The What-If)

Part 3: Verification & Troubleshooting (The What-If)
Essential Verification Commands
For Route Reflection:
interfaces {
 lo0 {
 unit 0 {
 family inet {
 address 1.1.1.1/32;
 ge-0/0/0 {
 unit 0 {
 family inet {
 address 10.0.0.254/24;
routing-options {
 router-id 1.1.1.1;
 autonomous-system 65000;
protocols {
 bgp {
 group RR-CLIENTS {
 type internal;
 local-address 1.1.1.1;
 family inet {
 unicast;
 cluster 1.1.1.1; ## This makes it a Route Reflector
 neighbor 10.0.0.1; ## Client 1
 neighbor 10.0.0.2; ## Client 2
 neighbor 10.0.0.3; ## Client 3
 group INTERNAL-MESH {
 type internal;
 local-address 1.1.1.1;
 neighbor 2.2.2.2; ## Non-client peer (another RR)
 ospf {
 area 0.0.0.0 {
 interface lo0.0 passive;
 interface ge-0/0/0.0;
## 1. Verify BGP neighbor status
user@RR1> show bgp summary
Threading mode: BGP I/O
Groups: 2 Peers: 4 Down peers: 0
Table Tot Paths  Act Paths Suppressed History Damp State Pending
inet.0 10 5 0 0 0 0
Peer AS InPkt OutPkt OutQ Flaps Last Up/Dwn State
10.0.0.1 65000 142 145 0 0 1:03:27 4/4/1/0
10.0.0.2 65000 141 145 0 0 1:03:25 3/3/1/0
10.0.0.3 65000 140 145 0 0 1:03:23 3/3/1/0
2.2.2.2 65000 150 148 0 0 1:05:00 0/0/0/0
## 2. Verify route reflection is working
user@RR1> show route advertising-protocol bgp 10.0.0.1 detail
inet.0: 15 destinations, 20 routes (15 active, 0 holddown, 0 hidden)
* 192.168.1.0/24 (1 entry, 1 announced)
 BGP group RR-CLIENTS type Internal
 Nexthop: 10.0.0.2


For Confederations:
Common Troubleshooting Scenarios
Scenario 1: Route
[...truncated...]

## 60.8 Part 3: Verification & Troubleshooting (The What-If)

Part 3: Verification & Troubleshooting (The What-If)
Essential Policy Troubleshooting Commands
user@router# set term OUR-PREFIXES from route-filter 203.0.113.0/24 exact
user@router# set term OUR-PREFIXES then accept
## Term 2: Announce customer prefixes to everyone
user@router# set term CUSTOMER-TO-ALL from community CUSTOMER-COMM
user@router# set term CUSTOMER-TO-ALL then accept
## Term 3: Don't announce peer/transit to other peers/transit
user@router# set term NO-PEER-TO-PEER from community [ PEER-COMM TRANSIT-COMM ]
user@router# set term NO-PEER-TO-PEER to as-path [ PEER-AS TRANSIT-AS ]
user@router# set term NO-PEER-TO-PEER then reject
## Default - reject
user@router# set then reject
## Step 4: Apply policies to BGP
[edit protocols bgp]
user@router# set group CUSTOMERS import BGP-IMPORT
user@router# set group CUSTOMERS export BGP-EXPORT
user@router# set group PEERS import BGP-IMPORT
user@router# set group PEERS export BGP-EXPORT
## Using policy chains
[edit policy-options]
user@router# set policy-statement BASIC-SANITY term 1 from route-filter 0.0.0.0/0 exact
user@router# set policy-statement BASIC-SANITY term 1 then reject
user@router# set policy-statement BASIC-SANITY term 2 from route-filter 0.0.0.0/0 prefix-length-range /25-/32
user@router# set policy-statement BASIC-SANITY term 2 then reject
user@router# set policy-statement CUSTOMER-SPECIFIC term 1 from neighbor 192.168.1.1
user@router# set policy-statement CUSTOMER-SPECIFIC term 1 then local-preference 200
## Chain 
[...truncated...]



---

# SECTION 50: JNCIA — PDF EXTRACTED KNOWLEDGE

> **Source:** JNCIA study guide (auto-extracted)

router in the path) to use to get there. When a packet arrives at the router, the router looks at the packet's destination IP address. It then performs a "route lookup" in its routing table to find the best match. The rule is simple: the most specific match wins. A route to 192.168.1.0/24 is more specific than a route to 192.168.0.0/16 . A "default route," 0.0.0.0/0 , is the least specific match of all and acts as a catch-all for any traffic that doesn't match a more specific entry. You can view the main IPv4 routing table at any time in Operational Mode with: professor@JNCIA-ROUTER-01> show route 2. Three Ways to Learn a Route A router builds its routing table from three sources: 3. Configuring a Static Route Static routes are perfect for small, predictable networks or for defining a specific path that should always be used. The most common use case is creating a default route to send all internet-bound traffic to your ISP's router. Visual Aid: Configuration Hierarchy 🌳 Let's assume your internet provider has given you a router with the IP address 203.0.113.1 . Here is how you tell your Junos device to send all unknown traffic to it: Bash Now, if you run show route , you will see a new entry: 0.0.0.0/0 *[Static/5] via 203.0.113.1 This line tells you: 1. Directly Connected Networks: When you configure an IP address on an interface and that interface is "up, up," the router automatically adds a route for that network to its routing table. The router knows it can reach those ho
[...truncated...]

from condition is met. accept : The route is accepted and processed. If a route doesn't match any term in your policy, a default action (usually reject ) is taken. Therefore, your policy must have a term that explicitly accepts the routes you want. Use Case: Advertising a Default Route This is the classic JNCIA routing policy use case. The Scenario: You have a router that is connected to the internet. You have configured a static default route to your ISP: set routing-options static route 0.0.0.0/0 next-hop 203.0.113.1 . The Problem: By default, your router will not share this static route with its internal OSPF neighbors. This means all the other routers in your network don't know how to get to the internet. The Solution: We need to create an export policy for OSPF that specifically finds our static default route and "exports" it into OSPF, advertising it to all our internal routers. The Configuration: Bash Let's break this down: Now, all the OSPF routers inside your network will learn a default route pointing to your edge router, granting them internet access. You have successfully used policy to intelligently inject a route from one protocol into another. This is the foundation of advanced network control. Lesson 14: Securing Traffic with Stateless Firewall Filters While a routing policy controls the map (Control Plane), a firewall filter controls the traffic itself (Forwarding Plane). A stateless firewall filter is a list of rules that inspects each packet individually, w
[...truncated...]

You can have both families on the same interface simultaneously, which is known as a "dual-stack" configuration. Verification: The verification commands are also the same, you just add inet6 to the end. Routing with IPv6 Static Routes Configuring a static route for IPv6 follows the exact same logic as for IPv4. You just use the IPv6 address format and specify the correct IPv6 routing table, which is inet6.0 . Configuration Example: IPv4: 32 bits, written as four decimal numbers (e.g., 192.168.1.1 ). IPv6: 128 bits, written as eight 16-bit hexadecimal blocks, separated by colons. Example: 2001:0db8:85a3:0000:0000:8a2e:0370:7334 1. Leading Zero Omission: You can drop the leading zeros in any block. 0db8 becomes db8 0000 becomes 0 0370 becomes 370 2. The Double Colon :: : You can replace one consecutive sequence of all-zero blocks with a double colon :: . [edit interfaces ge-0/0/2 unit 0] +-- family inet { address 10.0.2.1/24; } <-- Our old IPv4 config +-- family inet6 { address 2001:db8:2::1/64; } <-- The new IPv6 config family inet is for IPv4. family inet6 is for IPv6. show interfaces terse inet6 show route table inet6.0 Bash OSPFv3 for Dynamic IPv6 Routing OSPF was updated to support IPv6 and is now called OSPFv3. The core concepts remain identical: it's a link-state protocol that uses areas, LSAs, and the SPF algorithm to calculate the best path. The configuration is nearly a mirror image of what we learned in Lesson 11. Configuration Example: Bash Verification: The verific
[...truncated...]

Guard While policies control the map, firewall filters control the actual traffic. A firewall filter is a set of rules applied to an interface that inspects each packet passing through Firewall filters are also made of terms , which are evaluated in order. 0.0.0.0/0 : The destination network (the default route). *[Static/5] : The route is active ( * ), it was learned via a Static configuration, and it has an administrative preference of 5. via 203.0.113.1 : To reach this destination, send packets to the next-hop router at this address. 1. Routing Policy: Controls the routing table. It influences which routes are accepted, rejected, or modified. It operates on the Control Plane. 2. Firewall Filters: Controls the data packets themselves. It permits or denies traffic as it passes through an interface. It operates on the Forwarding Plane. Security: Prevent a misconfigured peer from injecting bad routes into your network. Traffic Engineering: Influence the path traffic takes by making certain routes look more or less desirable. Scalability: Filter out unnecessary routes to keep your routing tables lean and efficient. from : Specifies the conditions to match. (e.g., "match all routes coming from neighbor 1.1.1.1" or "match all routes for network 10.0.0.0/8"). then : Specifies the action to take if the conditions are met. (e.g., accept the route, reject the route, or modify an attribute like the local-preference ). Policy: The guest list and rules. Term 1 from : "Is your name on the
[...truncated...]

they agree to exchange routing information. 3. Link-State Advertisements (LSAs): Each router generates LSAs, which are small packets describing its own links and their status (up/down) and cost (speed). 4. Database Synchronization: Routers flood these LSAs to all other routers within the same "area," so every router builds an identical Link-State Database (LSDB). 5. SPF Algorithm: Each router independently runs the Shortest Path First (SPF) algorithm (also known as Dijkstra's algorithm) on its copy of the database to calculate the best, loop-free path to every other network. The result is a fast, scalable, and resilient network. If a link fails, the routers connected to it send out updated LSAs, everyone recalculates their map, and traffic is rerouted within seconds. The Concept of OSPF Areas A large network can generate a lot of LSA traffic. To keep things manageable, OSPF uses the concept of areas. An area is a logical collection of routers. For the JNCIA, you primarily need to understand how to configure a single area network, typically Area 0. Basic OSPF Configuration Let's configure OSPF on our router. The goal is to enable OSPF on our interfaces so they can start discovering neighbors. Visual Aid: Configuration Hierarchy 🌳 Here are the set commands to create this simple OSPF configuration: Bash Verifying OSPF Operation Once configured, you need to verify it's working. These are the key operational mode commands: Area 0 (The Backbone): This is the most important area. Al
[...truncated...]

RE. The goal is to only permit essential management traffic and explicitly deny everything else. The Configuration: Bash Let's analyze this filter: Policing (Rate Limiting) A firewall filter can also be used to rate-limit traffic. This is known as "policing." You can create a policer that defines a certain bandwidth limit (e.g., 10 Mbps) and a burst size. In the then statement of a filter term, instead of accept , you would specify your policer. Any traffic that matches the term and exceeds the rate limit will be discarded. This is very useful for preventing a single, low-priority application from consuming all your bandwidth. Lesson 15: Prioritizing Traffic with Class of Service (CoS) Class of Service doesn't make your network faster or eliminate congestion. It manages congestion. It provides a set of tools to give preferential treatment to certain types of traffic, ensuring that the most important packets experience the least amount of delay and packet loss. discard : Silently drop the packet. The source never knows it was dropped. This is the most common action for unwanted traffic. reject : Drop the packet but send an "ICMP destination unreachable" message back to the source. This is useful for letting legitimate hosts know a service isn't available. count : Increment a counter specific to this term. This is essential for seeing if your rule is actually working. log : Send a summary of the packet to a special buffer for logging. This helps in troubleshooting. # Enter conf
[...truncated...]

sends a Router Solicitation (RS) message out to the local network, essentially asking, "Are there any routers here?" 3. The local router responds with a Router Advertisement (RA) message. This RA contains the network prefix for the local network (e.g., 2001:db8:abc::/64 ) and the default gateway address. 4. The client device takes the network prefix from the router and combines it with its own unique interface identifier (often derived from its MAC address using a process called EUI-64) to create its own globally unique public IPv6 address. In seconds, a new device can get on the network with a public IP address and a default gateway, all without any manual intervention. This is a massive improvement over IPv4's reliance on DHCP. IPv6 Tunneling: Bridging the Gap During the long transition from IPv4 to IPv6, it's common to have "islands" of IPv6 networks that need to communicate over the vast IPv4 internet. IPv6-in-IPv4 tunneling is the solution. It works by taking an entire IPv6 packet and encapsulating it inside an IPv4 packet, like putting a letter inside another, larger envelope. This allows the IPv6 packet to travel across the IPv4 network. When it reaches the other end of the "tunnel," the IPv4 "envelope" is removed, revealing the original IPv6 packet, which can then be delivered to its destination. This lesson has solidified your understanding of not just how to use IPv6, but why it was designed the way it was. You now grasp the efficiencies of its header, the different
[...truncated...]

Excellent. Thank you for providing the first video. I've reviewed its contents, and it gives us the perfect starting point for our JNCIA journey: the Junos Operating System (OS) Fundamentals. Before a single packet is sent or received, we must understand the "brain" that controls the networking device. For Juniper devices, that brain is the Junos OS. Think of it like the Windows or macOS for a computer; it's the foundational software on which everything else runs. Let's begin our first lesson. Lesson 1: Junos OS Fundamentals Based on the video, we'll break this down into three core areas: 1. Junos OS Design Philosophy & Architecture Most operating systems for network devices are "monolithic." This means all processes run in the same shared memory space. If one small process crashes (like the one that lets you type commands), it can crash the entire operating system, and the device stops forwarding traffic. This is a single point of failure and is highly undesirable in networking. Juniper took a different approach, rooted in the stability of the UNIX operating system. The core design philosophy of Junos OS is modularity and separation. Visual Aid: The Two Planes Imagine a Juniper router or switch is a two-story building. Each floor has a distinct and separate purpose. This separation is the key to Junos's stability. A problem on the control plane (e.g., a routing protocol bug) will not typically impact the forwarding plane's ability to continue sending packets based on the las
[...truncated...]

storage usage is show system storage . This will show you the various filesystems and their percentage of used space. Cleanup: The /var/log/ and /var/tmp/ directories are the most common places where old files accumulate. Log files are automatically compressed and rotated. You can use the clear log command to wipe them, but it's often better to manually delete old, archived log files ( .gz extension) that you no longer need. 2. Junos OS Upgrades ⬆️ Upgrading the Junos OS is a fundamental maintenance task. You do it to: The Upgrade Process: A Note on Unified ISSU (In-Service Software Upgrade): On higher-end, redundant platforms (e.g., a chassis with dual Routing Engines), Junos supports Unified ISSU. This is a remarkable feature that allows you to upgrade the OS with zero downtime. One RE is upgraded while the other handles traffic, and then they gracefully switch roles. While the full process is beyond the scope of JNCIA, it's important to know that this capability is a major advantage of the Junos architecture. Course Conclusion and Next Steps Professor, we have now completed a comprehensive overview of the core topics required for the JNCIA-Junos certification and, more importantly, for building a solid foundation in networking. Let's review our journey: You now possess the fundamental knowledge to configure, operate, and troubleshoot a Junos-based network. You have the tools to develop that "instinct" you were seeking. Lesson 10: Advanced Interface Configuration & Manageme
[...truncated...]

SRX Series Think of the stateless firewall filters we learned about in Lesson 14 as a security guard checking a simple list of names at a door. It's effective for basic access control. An SRX Series firewall is like an entire airport security checkpoint. It not only checks your ID but also understands your itinerary, scans your luggage for threats, and knows who you've been talking to. From Stateless to Stateful The most fundamental difference in an SRX is that it is a stateful firewall. Organization: You can't logically group users. The Marketing team is in the same flat network as the Engineering team and the guest Wi-Fi users. Traffic within a VLAN stays within that VLAN. A broadcast from a user in VLAN 10 will only be heard by other users in VLAN 10. For a device in VLAN 10 to communicate with a device in VLAN 20, the traffic must go through a Layer 3 device—a router. This is called inter-VLAN routing. Security: The Marketing team's traffic is now completely isolated from the Engineering team's traffic. Performance: Broadcasts are contained within each VLAN, reducing overall network noise. Flexibility: You can group users logically (by department, function, etc.) regardless of where they are physically plugged into the network. 1. Create the VLANs: Define the VLANs that will exist on the switch. 2. Assign Interfaces to VLANs: Configure each port to belong to a specific VLAN. # Enter configuration mode configure # 1. Create the VLANs and give them names and VLAN IDs set vl
[...truncated...]



---

# SECTION 55: JUNOS INTERMEDIATE ROUTING JIR — PDF EXTRACTED KNOWLEDGE

> **Source:** Junos Intermediate Routing JIR study guide (auto-extracted)

## 55.1 Module 8: Deploying BGP

Module 8: Deploying BGP
The iBGP Full Mesh Problem
As your network grows, the iBGP full mesh requirement becomes unmanageable:
Solution 1: Route Reflection
Route Reflectors (RR) break the iBGP rule by re-advertising iBGP routes to other iBGP peers:
Route Reflector Concepts
Three Types of Peers from RR Perspective:
set protocols bgp group ISP-A neighbor 198.51.100.1 export TO-ISP-PRIMARY
# eBGP to ISP-B (backup)
set protocols bgp group ISP-B type external  
set protocols bgp group ISP-B peer-as 702
set protocols bgp group ISP-B neighbor 198.51.100.5 description "ISP-B Backup"
set protocols bgp group ISP-B neighbor 198.51.100.5 import FROM-ISP-B
set protocols bgp group ISP-B neighbor 198.51.100.5 export TO-ISP-BACKUP
# Policies for primary/backup behavior
set policy-options policy-statement FROM-ISP-A term DEFAULT from route-filter 0.0.0.0/0 exact
set policy-options policy-statement FROM-ISP-A term DEFAULT then local-preference 200
set policy-options policy-statement FROM-ISP-A term DEFAULT then accept
set policy-options policy-statement FROM-ISP-B term DEFAULT from route-filter 0.0.0.0/0 exact
set policy-options policy-statement FROM-ISP-B term DEFAULT then local-preference 100
set policy-options policy-statement FROM-ISP-B term DEFAULT then accept
# Make backup path less attractive inbound
set policy-options policy-statement TO-ISP-BACKUP term PREPEND then as-path-prepend "65001 65001"
4 routers = 6 sessions
10 routers = 45 sessions  
20 routers = 190 sessions
n routers = n(n
[...truncated...]

## 55.2 Module 3: Fundamentals of OSPF

Module 3: Fundamentals of OSPF
What is OSPF? - The Neighborhood Watch Protocol
OSPF (Open Shortest Path First) is like creating a neighborhood watch program for routers. Instead of you manually telling each router about every
network (static routes), routers talk to each other and share information automatically.
The Real-World Analogy:
# Check all routes:
show route <destination> all
# Adjust preference:
set routing-options static route <destination> next-hop <gateway> preference 200
1. Plan Before Configuring:
What networks need static routes?
What's the next-hop for each?
Do I need redundancy?
2. Verify Each Step:
# After each route:
show route protocol static
ping <destination> rapid count 5
3. Think in Hierarchies:
Use aggregate routes for scalability
Use generated routes for flexibility
Use static routes for specific needs
# Bad:
set routing-options static route 192.168.1.0/24 next-hop 172.16.1.1
# (If 172.16.1.1 not directly connected)
# Good:
set routing-options static route 192.168.1.0/24 next-hop 172.16.1.1 resolve
# Problem:
set routing-options static route 10.0.0.0/8 next-hop 1.1.1.1
set routing-options static route 10.0.0.0/8 next-hop 2.2.2.2
# Both have same preference!
# Solution:
set routing-options static route 10.0.0.0/8 qualified-next-hop 1.1.1.1 preference 10
set routing-options static route 10.0.0.0/8 qualified-next-hop 2.2.2.2 preference 20
Static Routing = You calling each neighbor to tell them about a road closure
OSPF = Neighbors automatically sharing
[...truncated...]

## 55.3 Module 11: Load Balancing

Module 11: Load Balancing
Understanding Load Balancing - Traffic Distribution
Load balancing in routing is about utilizing multiple paths efficiently. Instead of having expensive backup links sitting idle, we distribute traffic across all
available paths.
The Evolution of Path Usage:
Types of Load Balancing
1. Per-Packet (Round-Robin)
2. Per-Flow (Hash-Based)
# Production Network (Default)
set interfaces ge-0/0/0 unit 0 family inet address 10.0.0.1/24
# DMZ Network
set routing-instances DMZ instance-type virtual-router
set routing-instances DMZ interface ge-0/0/1.0
set routing-instances DMZ routing-options static route 0.0.0.0/0 next-hop 192.168.1.1
# Guest Network
set routing-instances GUEST instance-type virtual-router
set routing-instances GUEST interface ge-0/0/2.0
set routing-instances GUEST protocols ospf area 0.0.0.0 interface ge-0/0/2.0
# Firewall filter between instances
set firewall family inet filter DMZ-TO-PROD term ALLOW-HTTP from source-prefix-list DMZ-SERVERS
set firewall family inet filter DMZ-TO-PROD term ALLOW-HTTP from protocol tcp
set firewall family inet filter DMZ-TO-PROD term ALLOW-HTTP from destination-port 80
set firewall family inet filter DMZ-TO-PROD term ALLOW-HTTP then accept
set firewall family inet filter DMZ-TO-PROD term DENY-ALL then discard
# Apply filter
set interfaces lt-0/0/0 unit 1 family inet filter input DMZ-TO-PROD
Traditional: Load Balanced:
Primary Path: ████████████ Path 1: ██████
Backup Path:  ____________ Path 2: ██████
(Backup un
[...truncated...]



---

# SECTION 70: JUNOS LAYER 2 VPNS JL2V — PDF EXTRACTED KNOWLEDGE

> **Source:** Junos Layer 2 VPNs JL2V study guide (auto-extracted)

## 70.1 unit 1000 {

unit 1000 {
 vlan-tags outer 1000 inner 100;  # S-VLAN 1000, C-VLAN 100
 family vpls;
## VPLS instance
[edit routing-instances VPLS-QINQ]
instance-type vpls;
interface ge-0/0/0.1000;
## VLANs are preserved as-is
[edit interfaces ge-0/0/0]

## 70.2 Part 2: The Junos CLI Masterclass (The How)

Part 2: The Junos CLI Masterclass (The How)
FEC 129 Configuration Structure
The configuration involves three main components:
FEC 129 (Autodiscovery):
All PEs: "I'll advertise what I have via BGP"
Result: Automatic discovery and connection
BGP: For autodiscovery and endpoint advertisement
LDP: For label signaling and pseudowire establishment
BGP's Strength: Scalable information distribution
"Hey network, I have CE customer-A at my location"
LDP's Strength: Efficient label allocation
"Now let's exchange labels for the actual data path"
1. BGP Advertisement Phase:
PE1 → BGP → "I have AGI:10.1.1.1:100 with SAII:1"
PE2 → BGP → "I have AGI:10.1.1.1:100 with SAII:2"
AGI (Attachment Group Identifier): Groups related circuits
SAII (Source Attachment Individual Identifier): Unique endpoint ID
TAII (Target Attachment Individual Identifier): Remote endpoint ID
2. Matching Process:
PE1 sees: "PE2 has SAII:2 for same AGI"
PE1 thinks: "My TAII:2 matches their SAII:2 - we should connect!"
3. LDP Signaling Phase:
PE1 → LDP → PE2: "Label mapping for pseudowire"
PE2 → LDP → PE1: "Label mapping for pseudowire"
1. BGP configuration for autodiscovery
2. L2VPN routing instance
3. FEC 129 specific parameters


Step-by-Step FEC 129 Configuration
Step 1: Configure BGP for L2VPN signaling:
Step 2: Configure the routing instance:
Step 3: Configure FEC 129 parameters:
Understanding Key Parameters
l2vpn-id: Unique identifier for the L2VPN domain
automatic-site-id: Let Junos handle SAII/TAII generation
Ma
[...truncated...]

## 70.3 Part 3: Verification & Troubleshooting (The What-If)

Part 3: Verification & Troubleshooting (The What-If)
Essential VPLS Verification Commands
Understanding VPLS Connection Output
Troubleshooting Scenario 1: VPLS Site Not Joining
Symptom: Remote PE not showing in VPLS connections
Diagnosis:
Cause: Mismatched vrf-target on PE3
Solution:
Troubleshooting Scenario 2: MAC Learning Issues
Symptom: Unicast flooding (all traffic treated as unknown)
## MAC aging time
set routing-instances VPLS-GOLD protocols vpls mac-table-aging-time 600
## Static MAC entry
set routing-instances VPLS-GOLD protocols vpls static-mac 00:11:22:33:44:55 interface ge-0/0/0.0
## Overall VPLS status
show vpls connections
## Detailed VPLS information
show vpls connections instance VPLS-GOLD extensive
## MAC table
show vpls mac-table instance VPLS-GOLD
## Statistics
show vpls statistics instance VPLS-GOLD
admin@PE1> show vpls connections instance VPLS-GOLD
Instance: VPLS-GOLD
  L2-id: 10.1.1.1:100
  Site-id: 1
  Number of local interfaces: 1
  Number of local interfaces up: 1
  Number of remote PEs: 3
  Number of remote PEs up: 3
  lsi.1048576 2 10.2.2.2 Up
  lsi.1048577 3 10.3.3.3 Up
  lsi.1048578 4 10.4.4.4 Up
Labels:
  Label-base Offset Size  Range
  262145 1 50 50
admin@PE1> show vpls connections instance VPLS-GOLD
  Number of remote PEs: 2  ## Should be 3!
admin@PE1> show route receive-protocol bgp 10.255.255.255 table bgp.l2vpn.0 | match VPLS-GOLD
## Missing routes from PE3
admin@PE3> show configuration routing-instances VPLS-GOLD
## Different vrf-target!
#
[...truncated...]

## 70.4 Part 1: The Conceptual Lecture (The Why)

Part 1: The Conceptual Lecture (The Why)
The Multipoint Challenge
Imagine you're running IT for a company with 50 branch offices. With point-to-point L2VPNs, you'd need 1,225 connections (n*(n-1)/2) for full
connectivity. This is the classic "n-squared problem."
VPLS solves this by creating a virtual switch in the service provider network:
How VPLS Works
VPLS emulates an Ethernet switch across an MPLS network:
VPLS vs Regular Pseudowire
Aspect
Pseudowire (L2VPN/L2Circuit)
VPLS
Topology
Point-to-point
Multipoint
MAC Learning
Broadcast
Not applicable
Flooded to all sites
Scalability
O(n²) circuits
O(n) sites
Use Case
Connecting 2 locations
Connecting multiple locations
The Two Signaling Approaches
 AGI: 10.2.2.2:200, SAII: 10.2.2.2:1, Remote-id: 1
 ## Different AGI values!
## Ensure all PEs use same l2vpn-id
set routing-instances FEC129-VPLS l2vpn-id l2vpn-id:65000:500
Traditional L2VPN (Point-to-Point):
Site A ←→ Site B
Site A ←→ Site C  
Site B ←→ Site C
(3 separate circuits for 3 sites)
VPLS (Multipoint):
Site A ←→ Virtual Switch ←→ Site B
 Site C
(All sites connect to one logical entity)
1. MAC Learning: Like a physical switch, VPLS learns MAC addresses
2. Forwarding: Unicast to specific PE, broadcast/multicast to all PEs
3. Loop Prevention: Split-horizon rule prevents loops
MAC Learning Process:
1. Host at Site A (MAC: AA:AA) sends frame
2. PE1 learns: MAC AA:AA is behind my local interface
3. PE1 floods frame to all remote PEs (PE2, PE3)
4. Remote PEs learn: MAC AA:AA is 
[...truncated...]

## 70.5 Part 3: Verification & Troubleshooting (The What-If)

Part 3: Verification & Troubleshooting (The What-If)
Essential Verification Commands by Service Type
Verifying Service Type Capabilities
What to Look For:
Common Troubleshooting Scenarios
Scenario 1: Wrong Encapsulation Type
Symptom: L2VPN/L2Circuit configured but no connectivity
Diagnostic Commands:
Cause: Encapsulation mismatch (EM status)
set routing-instances L2VPN-A protocols l2vpn site SITE1 site-identifier 1
set routing-instances L2VPN-A protocols l2vpn site SITE1 interface ge-0/0/1.0 remote-site-id 2
## L2Circuit
set protocols l2circuit neighbor 2.2.2.2 interface ge-0/0/1.0 virtual-circuit-id 100
## VPLS Instance
set routing-instances VPLS-A instance-type vpls
set routing-instances VPLS-A interface ge-0/0/2.100
set routing-instances VPLS-A route-distinguisher 1.1.1.1:200
set routing-instances VPLS-A vrf-target target:65000:200
set routing-instances VPLS-A protocols vpls site-range 10
set routing-instances VPLS-A protocols vpls site SITE1 site-identifier 1
## EVPN Instance
set routing-instances EVPN-A instance-type evpn
set routing-instances EVPN-A vlan-id 100
set routing-instances EVPN-A interface ge-0/0/2.100
set routing-instances EVPN-A route-distinguisher 1.1.1.1:300
set routing-instances EVPN-A vrf-target target:65000:300
set routing-instances EVPN-A protocols evpn
user@PE1> show route table bgp.l2vpn.0 
user@PE1> show route table bgp.evpn.0
user@PE1> show ldp session
BGP tables should exist if BGP families are configured correctly
LDP sessions should be establish
[...truncated...]

## 70.6 Part 1: The Conceptual Lecture (The Why)

Part 1: The Conceptual Lecture (The Why)
Understanding the Problem VPLS Solves
Imagine you're a large corporation with offices in New York, London, and Tokyo. Each office has hundreds of computers that need to communicate as if
they were all plugged into the same switch—sharing broadcasts, using the same IP subnet, and discovering each other through ARP. The challenge?
These offices are separated by thousands of miles and connected through a service provider's MPLS network.
This is where Virtual Private LAN Service (VPLS) comes in. VPLS creates the illusion that all your sites are connected to a single, giant Ethernet
switch spanning the globe.
What is VPLS?
VPLS is a multipoint Layer 2 VPN service that emulates an Ethernet LAN across an MPLS network. Unlike point-to-point pseudowires (which we
covered in L2VPN), VPLS connects multiple sites in a full-mesh topology, allowing any site to communicate directly with any other site.
Core VPLS Concepts
admin@PE1> show ldp neighbor
## Check for targeted LDP sessions
admin@PE1> show configuration protocols vpls
## Missing vpls-id or neighbor configuration
## Add all remote PE neighbors
set routing-instances VPLS-SILVER protocols vpls neighbor 10.2.2.2
set routing-instances VPLS-SILVER protocols vpls neighbor 10.3.3.3
## Ensure VPLS ID matches on all PEs
set routing-instances VPLS-SILVER protocols vpls vpls-id 200
Traditional L2VPN (Point-to-Point):
Site A <----pseudowire----> Site B
VPLS (Multipoint):
 Site A
 / | \
 /  |  \
 / | \
 
[...truncated...]



---

# SECTION 65: JUNOS MPLS FUNDAMENTALS JMF — PDF EXTRACTED KNOWLEDGE

> **Source:** Junos MPLS Fundamentals JMF study guide (auto-extracted)

## 65.1 Part 2: The Junos CLI Masterclass (The How)

Part 2: The Junos CLI Masterclass (The How)
Basic Bandwidth Reservation
Configure an LSP with bandwidth reservation:
Understanding Bandwidth Units
Junos accepts various bandwidth specifications:
Configuring Interface Bandwidth for RSVP
Define how much bandwidth RSVP can reserve:
Bandwidth Subscription (Overbooking)
Configure statistical multiplexing:
## Simple bandwidth reservation
[edit protocols mpls]
user@PE1# set label-switched-path BW-LSP to 192.168.1.4
user@PE1# set label-switched-path BW-LSP bandwidth 1g
## With specific priority
user@PE1# set label-switched-path PRIORITY-BW-LSP to 192.168.1.4
user@PE1# set label-switched-path PRIORITY-BW-LSP bandwidth 2g
user@PE1# set label-switched-path PRIORITY-BW-LSP priority 3 3
## Different ways to specify bandwidth
set label-switched-path LSP1 bandwidth 1000000000  ## Bits per second
set label-switched-path LSP2 bandwidth 1g ## Gigabits per second
set label-switched-path LSP3 bandwidth 1000m ## Megabits per second
set label-switched-path LSP4 bandwidth 1.5g ## Decimal values
## Special values
set label-switched-path LSP5 bandwidth 0 ## No reservation
set label-switched-path LSP6 bandwidth ct0 500m ## Class-type aware
## Method 1: Explicit bandwidth statement
[edit protocols rsvp interface ge-0/0/1.0]
user@PE1# set bandwidth 10g
## Method 2: Percentage of interface speed
user@PE1# set bandwidth percent 80
## Method 3: Different values for TE database vs reservable
user@PE1# set bandwidth 10g 8g
## First: Advertised in TED
## Seco
[...truncated...]

## 65.2 Part 2: The Junos CLI Masterclass (The How)

Part 2: The Junos CLI Masterclass (The How)
Basic Priority Configuration
Configure LSP with specific priorities:
1. Simple Three-Tier Model:
 Voice/Video: [0,0] - Never preempted
 Business Data: [3,3] - Medium priority
 Bulk/Backup: [7,7] - Best effort
2. Setup vs Hold Differentiation:
 Important LSP: [1,3] - Aggressive setup, moderate hold
 Normal LSP: [4,4] - Balanced
 Scavenger LSP: [7,0] - Weak setup, strong hold (weird!)
3. Cascading Priorities:
 Platinum: [0,0]
 Gold: [1,1]
 Silver: [2,2]
 Bronze: [3,3]
 Best Effort: [7,7]
Hard Preemption (Traditional):
1. New high-priority LSP needs bandwidth
2. IMMEDIATELY tear down low-priority LSP
3. Traffic blackholes until reroute
4. Service disruption!
Soft Preemption (Graceful):
1. New high-priority LSP needs bandwidth
2. Notify low-priority LSP: "Please move"
3. Low-priority LSP finds alternate path
4. Gracefully moves traffic
5. Then releases bandwidth
6. No service disruption!
10Gbps Link Status:
Priority 0 reserved: 2Gbps
Priority 3 reserved: 3Gbps  
Priority 7 reserved: 4Gbps
Available bandwidth view:
Priority 0 sees: 10Gbps (can preempt everyone)
Priority 3 sees: 6Gbps (can preempt priority 7)
Priority 7 sees: 1Gbps (can't preempt anyone)
## Simple priority assignment
[edit protocols mpls]
user@PE1# set label-switched-path VOICE-LSP to 192.168.1.4

Configuring Soft Preemption
Enable graceful preemption to avoid service disruption:
Priority-Based Bandwidth Pools
Configure bandwidth pools per priority:
Complete Priority Desi
[...truncated...]

## 65.3 Part 3: Verification & Troubleshooting (The What-If)

Part 3: Verification & Troubleshooting (The What-If)
Essential Facility Backup Verification
 priority 0 0;
 node-link-protection;
 label-switched-path DATA-PROTECTED {
 to 192.168.1.4;
 bandwidth 1g;
 priority 3 3;
 link-protection;
 label-switched-path BULK-PROTECTED {
 to 192.168.1.4;
 bandwidth 5g;
 priority 7 7;
 link-protection;
## Explicit bypass configuration (optional)
set protocols mpls {
 label-switched-path MANUAL-BYPASS-NODE {
 to 192.168.1.3;  ## Next-next-hop
 install 0.0.0.0/0;
 no-cspf;
 primary VIA-ALTERNATE {
 10.0.5.2 strict;
 10.0.6.2 strict;
 10.0.7.2 strict;
## Protected LSP with specific requirements
[edit protocols mpls label-switched-path PREMIUM-SERVICE]
user@PE1# set to 192.168.1.4
user@PE1# set bandwidth 2g
user@PE1# set admin-group include-all GOLD LOW-LATENCY
user@PE1# set node-link-protection
## Ensure bypasses meet minimum requirements
[edit protocols rsvp interface ge-0/0/1.0 node-link-protection]
user@PE1# set bandwidth 2g
user@PE1# set admin-group include-any SILVER GOLD
user@PE1# set max-bypasses 2
## Create classed bypasses
[edit protocols mpls]
user@PE1# set label-switched-path GOLD-BYPASS to 192.168.1.2
user@PE1# set label-switched-path GOLD-BYPASS admin-group include-all GOLD
user@PE1# set label-switched-path GOLD-BYPASS install 0.0.0.0/0
user@PE1# set label-switched-path SILVER-BYPASS to 192.168.1.2
user@PE1# set label-switched-path SILVER-BYPASS admin-group include-all SILVER
user@PE1# set label-switched-path SILVER-BYPASS install 0.0
[...truncated...]

## 65.4 Part 3: Verification & Troubleshooting (The What-If)

Part 3: Verification & Troubleshooting (The What-If)
Essential Priority Verification Commands
1. View LSP Priorities
2. Check Priority-Based Bandwidth Availability
[edit protocols mpls label-switched-path EMERGENCY]
user@PE1# set to 192.168.1.4
user@PE1# set priority 0 0
user@PE1# set no-soft-preemption  ## Immediate hard preemption
## Extended grace period for bulk transfers
[edit protocols mpls label-switched-path BULK-GRACEFUL]
user@PE1# set to 192.168.1.4
user@PE1# set priority 6 7
user@PE1# set soft-preemption
user@PE1# set soft-preemption-cleanup-timer 300  ## 5 minutes grace
## Install only high-priority LSPs in forwarding
[edit protocols mpls]
user@PE1# set prefer-standby
## Configure LSP preference based on priority
[edit protocols mpls label-switched-path VOICE]
user@PE1# set preference 5  ## Lower preference = more preferred
[edit protocols mpls label-switched-path BULK]
user@PE1# set preference 10
user@PE1> show mpls lsp detail
Ingress LSP: 5 sessions
192.168.1.4
  From: 192.168.1.1, State: Up, ActiveRoute: 1, LSPname: VOICE
  ActivePath:  (primary)
  Priorities: 0 0
  Bandwidth: 1Gbps
  
192.168.1.4
  From: 192.168.1.1, State: Up, ActiveRoute: 1, LSPname: BUSINESS-APPS
  ActivePath:  (primary)
  Priorities: 3 3
  Bandwidth: 3Gbps
user@PE1> show rsvp interface detail
ge-0/0/1.0
  Index: 329, State: Up
  ActiveResv: 4, Subscription: 100%
  Static BW: 10Gbps, Reservable BW: 10Gbps
  Available bandwidth:
 [0] 10Gbps [1] 9Gbps [2] 9Gbps [3] 6Gbps
 [4] 6Gbps [5] 6Gbps 
[...truncated...]

## 65.5 Part 1: The Conceptual Lecture (The Why)

Part 1: The Conceptual Lecture (The Why)
The Problem with Simple Bandwidth Reservation
Imagine an emergency room where patients are served first-come, first-served. A patient with a minor cut might occupy a bed while someone with a
heart attack waits. This is the problem with bandwidth reservation without priorities - critical traffic can be blocked by less important traffic that arrived
first.
Understanding RSVP Priority Levels
RSVP uses two priority values for each LSP:
The Preemption Model
Higher priority LSPs can preempt (kick out) lower priority ones:
Default Priority Behavior
By default, all LSPs use [7,7] - the lowest priority:
The Bandwidth Exhaustion Problem:
Time 09:00: 10Gbps link available
Time 09:15: Bulk backup LSP reserves 8Gbps (Priority 7)
Time 09:30: VoIP LSP needs 2Gbps (should be Priority 0)
Result: VoIP LSP fails! No bandwidth available.
Emergency services blocked by routine traffic!
Setup Priority: Used when establishing the LSP
Hold Priority: Used to maintain the LSP
Format: [Setup Priority, Hold Priority]
Range: 0-7 (0 = highest, 7 = lowest)
Think of it as:
Setup Priority = "How important is it to get established?"
Hold Priority = "How important is it to keep running?"
Preemption Rules:
1. Setup Priority must be ≤ Hold Priority
 (Can't establish weak but hold strong)
2. To preempt: New Setup Priority < Existing Hold Priority
Example:
Existing LSP: [5,5] (Setup=5, Hold=5)
New LSP: [3,3] wants bandwidth
Result: 3 < 5, so new LSP preempts existing
But if 
[...truncated...]

## 65.6 Module 9: RSVP-Constrained Shortest Path First, and Admin Groups

Module 9: RSVP-Constrained Shortest Path First, and Admin Groups
## Enable optimize timer to consolidate bandwidth
[edit protocols mpls]
user@PE1# set optimize-timer 3600
user@PE1# set label-switched-path all optimize-aggressive
## Or manually clear and re-signal LSPs
user@PE1> clear mpls lsp all
[edit protocols rsvp]
user@PE1# set traceoptions file rsvp-preempt
user@PE1# set traceoptions flag preemption detail
user@PE1# commit
user@PE1> show log rsvp-preempt
Nov 25 11:30:45 Preemption check for new LSP CRITICAL-DATA
Nov 25 11:30:45 Need 3Gbps at priority 1/1
Nov 25 11:30:45 Checking LSP BULK-TRANSFER: 4Gbps at 5/6
Nov 25 11:30:45 Setup pri 1 < Hold pri 6: Can preempt
Nov 25 11:30:45 Preempting BULK-TRANSFER to free 4Gbps
Nov 25 11:30:45 Soft-preemption notification sent
user@PE1> show mpls lsp statistics priority
Priority  Active LSPs  Bandwidth Reserved  Percentage
0 2 2.5 Gbps 15%
1 3 4.2 Gbps 25%
2 1 1.0 Gbps 6%
3 5 6.8 Gbps 41%
4 0 0 bps 0%
5 2 1.5 Gbps 9%
6 0 0 bps 0%
7 4 600 Mbps 4%
Total: 17 16.6 Gbps 100%
## Create test scenario
[edit protocols mpls]
user@PE1# set label-switched-path TEST-VICTIM to 192.168.1.4 priority 6 6 bandwidth 5g
user@PE1# commit
user@PE1> show mpls lsp name TEST-VICTIM
TEST-VICTIM 192.168.1.4 192.168.1.1 Up
## Now create preemptor
[edit protocols mpls]
user@PE1# set label-switched-path TEST-PREEMPTOR to 192.168.1.4 priority 2 2 bandwidth 8g
user@PE1# commit
## Check results
user@PE1> show mpls lsp
TEST-PREEMPTOR  192.168.1.4 192.168.1.1 Up
TES
[...truncated...]

## 65.7 Module 8: RSVP-LSP Priorities

Module 8: RSVP-LSP Priorities
## Enable LSP statistics
[edit protocols mpls]
user@PE1# set statistics file mpls-stats
user@PE1# set statistics interval 300
user@PE1# set label-switched-path ALL-LSPS statistics
user@PE1# commit
## View statistics
user@PE1> show mpls lsp statistics
LSP Name To Packets Bytes  Pkt Rate  Byte Rate
GOLD-SERVICE 192.168.1.4 12345678 15432098765 234 2916354
SILVER-SERVICE 192.168.1.4 8765432 8765432109 187 1876543
## Check TED bandwidth tracking
user@PE1> show ted database extensive local
NodeID: 192.168.1.1
  Protocol: OSPF(0.0.0.0)
 To: 192.168.1.2, Local: 10.0.1.1, Remote: 10.0.1.2
 Metric: 10, TE Metric: 10, IGP metric: 10
 Static BW: 10Gbps, Reservable BW: 9Gbps
 Available BW [priority] bps:
 [0] 9Gbps [1] 7Gbps [2] 7Gbps [3] 5.5Gbps
 [4] 5.5Gbps [5] 5.5Gbps [6] 5.5Gbps [7] 5.5Gbps
 Reserved BW [priority] bps:
 [0] 0bps [1] 2Gbps [2] 0bps [3] 1.5Gbps
 [4] 0bps [5] 0bps [6] 0bps [7] 0bps
## Verify: Reserved + Available = Reservable (per priority)
## Priority 1: 2G reserved + 7G available = 9G reservable ✓
## Create test to verify preemption works
[edit protocols mpls]
user@PE1# set label-switched-path TEST-LOW to 192.168.1.4 bandwidth 8g priority 7 7
user@PE1# commit
user@PE1> show mpls lsp
TEST-LOW 192.168.1.4 192.168.1.1 Up
## Now create high-priority LSP that needs same bandwidth
[edit protocols mpls]
user@PE1# set label-switched-path TEST-HIGH to 192.168.1.4 bandwidth 8g priority 0 0
user@PE1# commit
## Check results
user@PE1> show mpls lsp
T
[...truncated...]

## 65.8 Part 2: The Junos CLI Masterclass (The How)

Part 2: The Junos CLI Masterclass (The How)
Basic Fast Reroute Configuration
Enable one-to-one backup on an LSP:
Understanding Fast Reroute Options
Configure specific fast reroute behaviors:
Controlling Detour Computation
Fine-tune how detours are calculated:
Scalability Considerations:
Network: 100 routers, 1000 LSPs
Average path length: 5 hops
One-to-One Backup Creates:
- 1000 LSPs × 4 protection points = 4000 detour LSPs
- Control plane: 5000 total LSPs to manage
- Memory: ~50MB for state storage
- CPU: Continuous detour optimization
Resource Formula:
Detours = (Number of LSPs) × (Average Hops - 1)
## Simple fast-reroute enablement
[edit protocols mpls]
user@PE1# set label-switched-path PROTECTED-LSP to 192.168.1.4
user@PE1# set label-switched-path PROTECTED-LSP fast-reroute
## That's it! Junos handles the rest
## But let's see what this actually does...
## Fast reroute with bandwidth protection
[edit protocols mpls label-switched-path FRR-LSP]
user@PE1# set to 192.168.1.4
user@PE1# set bandwidth 1g
user@PE1# set fast-reroute
user@PE1# set fast-reroute bandwidth 1g
## Fast reroute with hop limit
user@PE1# set fast-reroute hop-limit 3
## Detour can be maximum 3 hops longer
## Fast reroute with admin group constraints
user@PE1# set fast-reroute include-any BACKUP-LINKS
user@PE1# set fast-reroute exclude EXPENSIVE
## Node protection (protect against node failure)
user@PE1# set fast-reroute node-protection
## Relaxed constraints for detour paths
[edit protocols mpls]
user@PE1#
[...truncated...]

## 65.9 Part 3: Verification & Troubleshooting (The What-If)

Part 3: Verification & Troubleshooting (The What-If)
Essential Bandwidth Verification Commands
1. Check Interface Bandwidth Status
2. View LSP Bandwidth Reservations
set protocols mpls label-switched-path BRONZE-SERVICE {
 to 192.168.1.4;
 bandwidth 500m;
 priority 5 5;
 admin-group include-any BRONZE;
set protocols mpls label-switched-path AUTO-ADJUST {
 to 192.168.1.4;
 auto-bandwidth {
 adjust-interval 300;  ## 5 minutes
 minimum-bandwidth 50m;
 maximum-bandwidth 2g;
 adjust-threshold 10;  ## 10% change triggers adjustment
## Shared bandwidth (for backup paths)
[edit protocols mpls]
user@PE1# set label-switched-path PRIMARY to 192.168.1.4 bandwidth 1g
user@PE1# set label-switched-path PRIMARY primary PRIMARY-PATH
user@PE1# set label-switched-path PRIMARY secondary BACKUP-PATH
user@PE1# set label-switched-path PRIMARY secondary BACKUP-PATH bandwidth 1g
user@PE1# set label-switched-path PRIMARY secondary BACKUP-PATH shared
## Bandwidth protection
user@PE1# set label-switched-path PROTECTED bandwidth 1g
user@PE1# set label-switched-path PROTECTED link-protection
user@PE1> show rsvp interface detail
ge-0/0/1.0
  Index: 329, State: Up
  ActiveResv: 3, Subscription: 125%
  Static BW: 10Gbps, Reservable BW: 9Gbps
  BC Model: MAM, BC0 BW: 9Gbps
  Reserved bandwidth:
 CT0: 3.5Gbps, CT1: 0bps, CT2: 0bps, CT3: 0bps
  Available bandwidth:
 HighPrio: 9Gbps, HighNonCT: 5.5Gbps
 [0] 9Gbps [1] 9Gbps [2] 9Gbps [3] 9Gbps
 [4] 5.5Gbps [5] 5.5Gbps [6] 5.5Gbps [7] 5.5Gbps
  Reserved bandwidth 
[...truncated...]

## 65.10 Part 2: The Junos CLI Masterclass (The How)

Part 2: The Junos CLI Masterclass (The How)
Understanding Junos MPLS Tables Architecture
Junos uses multiple tables for MPLS operation:
Configuring Static LSPs - Complete Example
Let's build a static LSP from PE1 to PE2:
Like programming each router individually
Use case: Testing, very small networks
2. LDP (Label Distribution Protocol)
Automatic label distribution
Follows IGP best path
Use case: Simple MPLS, foundation for L3VPN
3. RSVP-TE (Resource Reservation Protocol - Traffic Engineering)
Signaled paths with reservations
Can take non-shortest paths
Use case: Traffic engineering, bandwidth guarantees
4. BGP (Border Gateway Protocol)
Distributes labels with routes
Primarily for L3VPN
Use case: VPN services, inter-AS MPLS
FEC Examples:
- All packets to 192.168.1.4/32 → Label 100
- All packets in VPN-A → Label 200  
- All packets matching certain criteria → Label 300
1. LIB: "All possible labels I know" (like a phone book)
2. FIB: "Labels I'm actually using" (like speed dial)
LIB (all learned labels):
Prefix 192.168.1.4/32:
  - From LDP neighbor P2: Use label 200
  - From RSVP LSP: Use label 500
  - From static config: Use label 800
FIB (what's installed):
192.168.1.4/32 → Push label 500 (RSVP wins due to preference)
Routing Tables for MPLS:
- inet.0:  IPv4 routes (regular routing)
- inet.3:  RSVP-learned MPLS paths  
- mpls.0:  MPLS switching table (label → action)
- ldp.0: LDP-learned labels (internal)
- bgp.l3vpn.0: L3VPN routes (BGP+MPLS)
Topology with IPs:
[PE1]----[P1]
[...truncated...]

## 65.11 Part 2: The Junos CLI Masterclass (The How)

Part 2: The Junos CLI Masterclass (The How)
Basic Facility Backup Configuration
Enable facility backup (link protection):
Node Protection Configuration
Enable more comprehensive protection:
Bypass Tunnel Configuration
Manually configure bypass tunnels:
Node-Link Protection Strategy:
For each protected interface:
1. Try to create node-protecting bypass
2. If not possible, create link-protecting bypass
3. Dynamically choose based on failure type
Example:
[R1] connected to [R2] connected to [R3] and [R4]
Bypasses created:
- Node bypass: R1→R5→R3 (protects R2 failure)
- Link bypass: R1→R5→R2 (protects R1-R2 link)
If R2 fails completely: Use node bypass
If only R1-R2 link fails: Use link bypass (shorter)
## Enable link protection globally
[edit protocols rsvp]
user@PE1# set interface all link-protection
## Or per-interface
[edit protocols rsvp]
user@PE1# set interface ge-0/0/1.0 link-protection
## On the LSP (request protection)
[edit protocols mpls]
user@PE1# set label-switched-path FACILITY-LSP to 192.168.1.4
user@PE1# set label-switched-path FACILITY-LSP link-protection
## Enable node-link protection
[edit protocols rsvp]
user@PE1# set interface ge-0/0/1.0 node-link-protection
## Configure LSP to request node protection
[edit protocols mpls]
user@PE1# set label-switched-path NODE-PROTECTED to 192.168.1.4
user@PE1# set label-switched-path NODE-PROTECTED node-link-protection
## What this does:
## - Creates node-protecting bypass when possible
## - Falls back to link protection if
[...truncated...]



---

# SECTION 75: JUNOS SERVICE PROVIDER SWITCHING JSPX — PDF EXTRACTED KNOWLEDGE

> **Source:** Junos Service Provider Switching JSPX study guide (auto-extracted)

## 75.1 Part 2: The Junos CLI Masterclass (The How)

Part 2: The Junos CLI Masterclass (The How)
Basic Provider Bridging Configuration
Step 1: Configure Service Provider VLANs
Step 2: Configure Customer-Facing Interfaces (PE)
Why:
Step 3: Configure C-VLAN Based Mapping
Step 4: Configure Core-Facing Interfaces
Advanced VLAN Operations
VLAN Translation (Swap)
Customer sends VLAN 10 → Provider adds VLAN 1000 → [1000][10]
One tag in, two tags out
# Define S-VLANs for different customers
set vlans S-VLAN-1000 vlan-id 1000
set vlans S-VLAN-1000 description "Customer A - All Sites"
set vlans S-VLAN-2000 vlan-id 2000  
set vlans S-VLAN-2000 description "Customer B - All Sites"
# Customer A - Site 1 (Port-based Q-in-Q)
set interfaces ge-0/0/0 flexible-vlan-tagging
set interfaces ge-0/0/0 encapsulation extended-vlan-bridge
set interfaces ge-0/0/0 unit 1000 vlan-id 1000
set interfaces ge-0/0/0 unit 1000 input-vlan-map push
set interfaces ge-0/0/0 unit 1000 output-vlan-map pop
flexible-vlan-tagging : Enables multiple VLAN operations
extended-vlan-bridge : Supports Q-in-Q operations
input-vlan-map push : Adds S-VLAN on ingress
output-vlan-map pop : Removes S-VLAN on egress
# Map specific customer VLANs to S-VLANs
set interfaces ge-0/0/1 flexible-vlan-tagging
set interfaces ge-0/0/1 encapsulation extended-vlan-bridge
# Customer VLAN 10 → S-VLAN 1000
set interfaces ge-0/0/1 unit 10 vlan-id-list 10
set interfaces ge-0/0/1 unit 10 input-vlan-map push vlan-id 1000
set interfaces ge-0/0/1 unit 10 output-vlan-map pop
# Customer VLAN 20 → S-VLAN 20
[...truncated...]

## 75.2 Part 2: The Junos CLI Masterclass (The How)

Part 2: The Junos CLI Masterclass (The How)
Understanding VLAN Configuration in Junos
Junos uses two main configuration styles for VLANs:
Basic VLAN Configuration
Step 1: Create VLANs
Why: Each VLAN needs a name (for humans) and ID (for the protocol).
Step 2: Configure Access Ports
Why: Access ports need exactly one VLAN membership.
Step 3: Configure Trunk Ports
Why: Trunk ports need to know which VLANs to accept/forward.
MVRP Configuration
Step 1: Enable MVRP Globally
Step 2: Configure MVRP on Trunk Interfaces
Without IRB: With IRB:
VLAN 10 ←X→ VLAN 20 VLAN 10 ←→ IRB.10
(Cannot communicate) ↓ ↑
 Router 
 VLAN 20 ←→ IRB.20
 (Can route between VLANs)
1. Enterprise style (ELS): Newer, used on EX/QFX switches
2. Service Provider style: Used on MX routers (our focus for JNCIE-SP)
set vlans SALES vlan-id 10
set vlans ENGINEERING vlan-id 20
set vlans HR vlan-id 30
# Sales PC on port ge-0/0/1
set interfaces ge-0/0/1 unit 0 family ethernet-switching vlan members SALES
# Engineering Workstation on port ge-0/0/2  
set interfaces ge-0/0/2 unit 0 family ethernet-switching vlan members ENGINEERING
# HR Printer on port ge-0/0/3
set interfaces ge-0/0/3 unit 0 family ethernet-switching vlan members HR
# Trunk to another switch on ge-0/0/10
set interfaces ge-0/0/10 unit 0 family ethernet-switching interface-mode trunk
set interfaces ge-0/0/10 unit 0 family ethernet-switching vlan members [ SALES ENGINEERING HR ]
# Alternative: Allow all VLANs
set interfaces ge-0/0/10 unit 0 family ethernet-sw
[...truncated...]

## 75.3 Part 2: The Junos CLI Masterclass (The How)

Part 2: The Junos CLI Masterclass (The How)
Configuring BPDU Protection
Global BPDU Protection
Per-Interface BPDU Protection
Recovery from BPDU Protection
Configuring Loop Protection
Global Loop Protection
Per-Interface Loop Protection
One STP instance
Protection applies to all VLANs
Protection per MST instance
Different policies for different VLAN groups
Each VLAN has independent STP
Maximum granularity but resource intensive
# Enable BPDU protection on all edge ports
set protocols rstp bpdu-block-on-edge
# Or for specific protocol
set protocols stp bpdu-block-on-edge
set protocols mstp bpdu-block-on-edge
set protocols vstp bpdu-block-on-edge
# Configure edge port with BPDU protection
set protocols rstp interface ge-0/0/10 edge
set protocols rstp interface ge-0/0/10 bpdu-block
# Disable specific interfaces if needed
set protocols rstp interface ge-0/0/10 disable-bpdu-block-on-edge
# Configure automatic recovery
set protocols rstp bpdu-block disable-timeout 300
# Or manual recovery
clear ethernet-switching bpdu-error interface ge-0/0/10
# Enable loop protection globally
set protocols rstp loop-protection
# For other STP variants
set protocols mstp loop-protection
set protocols vstp loop-protection
# Enable on specific interfaces
set protocols rstp interface ge-0/0/0 loop-protection
set protocols rstp interface ge-0/0/1 loop-protection
# Disable on specific interface if globally enabled
set protocols rstp interface ge-0/0/2 no-loop-protection


Configuring Root Protection
Adva
[...truncated...]

## 75.4 Part 1: The Conceptual Lecture (The Why)

Part 1: The Conceptual Lecture (The Why)
The Fundamental Problem
Imagine you're a service provider connecting multiple customer sites. Customer A has three offices using VLANs 10, 20, and 30 internally. When they
send traffic through your network, you face several challenges:
vlan-id 100;
## Missing inner VLAN configuration!
set interfaces ge-0/0/10 flexible-vlan-tagging
set interfaces ge-0/0/10 encapsulation flexible-ethernet-services
set interfaces ge-0/0/10 unit 100 vlan-id 100
set interfaces ge-0/0/10 unit 100 family bridge vlan-id-list [10 20]
commit
user@router> set cli logical-system CUSTOMER-A-LS
Logical system: CUSTOMER-A-LS
user@CUSTOMER-A-LS> show configuration
## Should only see CUSTOMER-A config
user@CUSTOMER-A-LS> show interfaces terse | except ".32767"
## Should only see interfaces assigned to this LS
# From main system
set interfaces ge-0/0/5 unit 0 logical-system CUSTOMER-A-LS
# Or entire interface
set logical-systems CUSTOMER-A-LS interfaces ge-0/0/5 unit 0 family bridge
1. Naming Convention: Use clear prefixes (CUST-A-VLAN10 vs just VLAN10)
2. Document Overlaps: Track where VLAN IDs are reused across instances
3. Monitor Resources: Each instance consumes memory for MAC tables
4. Test Isolation: Regularly verify traffic doesn't leak between instances
5. Plan Interconnects: Design logical tunnel topology before implementation
1. VLAN ID Conflicts: Multiple customers want to use VLAN 10
2. VLAN Exhaustion: You only have 4094 VLAN IDs but thousands of customers
[...truncated...]

## 75.5 Part 2: The Junos CLI Masterclass (The How)

Part 2: The Junos CLI Masterclass (The How)
STP Configuration in Junos
Basic STP Configuration
Why: Edge ports transition immediately to forwarding (no loops possible with single host).
Configure Bridge Priority
Priority values: Must be multiples of 4096 (0, 4096, 8192... 61440)
RSTP Configuration
MSTP Configuration
Step 1: Configure MST Region
Maximum 64 instances (vs 4094 VLANs)
Reduces CPU/memory usage
Each VLAN can have different topology
Load balancing across redundant links
More resource intensive
# Enable STP globally
set protocols stp
# Configure STP on interfaces
set protocols stp interface ge-0/0/0
set protocols stp interface ge-0/0/1
set protocols stp interface ge-0/0/2
# Exclude edge ports (to PCs/servers)
set protocols stp interface ge-0/0/10 edge
# Set bridge priority (lower = more likely to be root)
set protocols stp bridge-priority 16384
# For specific VLAN in VSTP
set protocols vstp vlan 100 bridge-priority 16384
# Enable RSTP (recommended over STP)
set protocols rstp
# Configure interfaces
set protocols rstp interface ge-0/0/0
set protocols rstp interface ge-0/0/1
# Set interface cost (optional)
set protocols rstp interface ge-0/0/0 cost 2000
# Configure edge ports
set protocols rstp interface ge-0/0/10 edge
set protocols rstp interface ge-0/0/11 edge
# No-root-port (for edge interfaces)
set protocols rstp interface ge-0/0/10 no-root-port
# Define MST region
set protocols mstp configuration-name REGION1
set protocols mstp revision-level 1
# Map VLANs to inst
[...truncated...]

## 75.6 Part 3: Verification & Troubleshooting (The What-If)

Part 3: Verification & Troubleshooting (The What-If)
Essential Verification Commands
1. Verify VLAN Operations
2. Check Bridge Domain Status
3. Monitor Q-in-Q Traffic
4. Check MAC Learning with S-VLAN Context
## Or Using VLANs (older style)
vlans {
 S-VLAN-1000 {
 description "Customer A Primary";
 vlan-id 1000;
 ## Interfaces added automatically via unit configuration
 S-VLAN-1001 {
 description "Customer A Secondary";
 vlan-id 1001;
 S-VLAN-2000 {
 description "Customer B";
 vlan-id 2000;
user@pe> show interfaces ge-0/0/0.1000 | match vlan-map
  Input-vlan-map: push, Output-vlan-map: pop
  
user@pe> show interfaces ge-0/0/0.1000 extensive | match "VLAN-Tag"
 VLAN-Tag [ 0x8100.1000 ] 
 Input VLAN-Tag: Outer [ 0x88a8.1000 ] Inner [ 0x8100.* ]
user@pe> show bridge domain
Routing instance Bridge domain VLAN ID Interfaces
default-switch CUSTOMER-A-PRIMARY 1000 
 ge-0/0/0.1000
 ge-0/0/1.10
 ge-0/0/10.1000
user@pe> monitor traffic interface ge-0/0/0.1000 layer2-headers detail
15:42:31.123456 In
  Ethernet II, Src: 00:11:22:33:44:55, Dst: 00:aa:bb:cc:dd:ee
  802.1Q, S-VID: 1000, C-VID: 10
  ↑ Two VLAN tags visible
user@pe> show bridge mac-table bridge-domain CUSTOMER-A-PRIMARY
MAC flags : D - Dynamic, S - Static, L - Local
Routing instance: default-switch
Bridging domain: CUSTOMER-A-PRIMARY, VLAN: 1000
  MAC MAC Logical NH RTR
  address flags interface Index  ID


Common Troubleshooting Scenarios
Scenario 1: Q-in-Q Tags Not Being Added
Symptom: Customer traffic arrives but doesn't 
[...truncated...]

## 75.7 Part 2: The Junos CLI Masterclass (The How)

Part 2: The Junos CLI Masterclass (The How)
Configuring Ethernet Ring Protection
Step 1: Basic Ring Configuration
Key concepts:
Step 2: Configure Ring Nodes
# Define protection group
set protocols protection-group ethernet-ring RING-1 {
 ring-id 1;
 restoration-interval 5; ## Wait 5 minutes before restoring
 guard-interval 500; ## 500ms guard time
 
 ## Define east and west interfaces
 east-interface {
 control-channel ge-0/0/0.100;
 ring-protection-link-owner; ## This node owns RPL
 west-interface {
 control-channel ge-0/0/1.100;
 
 ## Data channels (VLANs to protect)
 data-channel {
 vlan [ 200-299 ];
ring-id : Unique identifier for ring
restoration-interval : Prevents flapping
control-channel : Carries R-APS messages
data-channel : VLANs protected by ring
## RPL Owner Node
set protocols protection-group ethernet-ring RING-1 {
 ring-id 1;
 east-interface {
 control-channel ge-0/0/0.100;
 ring-protection-link-owner; ## RPL owner
 west-interface {
 control-channel ge-0/0/1.100;
 data-channel {
 vlan [ 200-299 ];
## RPL Neighbor Node  
set protocols protection-group ethernet-ring RING-1 {
 ring-id 1;
 east-interface {
 control-channel ge-0/0/0.100;
 west-interface {
 control-channel ge-0/0/1.100;
 ring-protection-link-neighbor;  ## RPL neighbor


Step 3: Configure VLANs for ERP
Configuring Link Aggregation
Step 1: Basic LAG Configuration
 data-channel {
 vlan [ 200-299 ];
## Regular Ring Node
set protocols protection-group ethernet-ring RING-1 {
 ring-id 1;
 east-interface {
 
[...truncated...]

## 75.8 Part 1: The Conceptual Lecture (The Why)

Part 1: The Conceptual Lecture (The Why)
The Fundamental Problem VLANs Solve
Imagine a company with 3 departments sharing one floor: Sales, Engineering, and HR. If everyone connects to the same switch, several problems arise:
The Solution: Virtual LANs (VLANs) create multiple logical networks on the same physical infrastructure, like creating invisible walls in an open office.
What is a VLAN?
A VLAN is a logical grouping of devices that can communicate at Layer 2, regardless of their physical location. Think of it as creating multiple virtual
switches inside one physical switch.
How VLAN Tagging Works
user@switch> show ethernet-switching table | count
Count: 4096 lines <-- MAC table thrashing
# Disable one of the redundant links
set interfaces ge-0/0/3 disable
commit
user@switch> show firewall filter BLOCK-GUEST
user@switch> show interfaces ge-0/0/0 extensive | match filter
  Filters: Input: BLOCK-GUEST-WRONG-NAME <-- Wrong filter name!
delete interfaces ge-0/0/0 unit 0 family ethernet-switching filter
set interfaces ge-0/0/0 unit 0 family ethernet-switching filter input BLOCK-GUEST
commit
1. Security: Sales can see Engineering's prototype designs on the network
2. Broadcast Storms: HR's printer announcement reaches 300 computers instead of just 20
3. Performance: All departments compete for the same bandwidth
4. Flexibility: Moving someone to a different department requires rewiring
Without VLANs: With VLANs:
+------------------+ +------------------+
| | | VLAN 10: Sales |
|
[...truncated...]

## 75.9 Part 3: Verification & Troubleshooting (The What-If)

Part 3: Verification & Troubleshooting (The What-If)
Essential Verification Commands
 family bridge {
 interface-mode trunk;
 vlan-id-list [ 300 400 ];
 unit 1 {
 encapsulation ethernet;
 peer-unit 0;
 family bridge {
 interface-mode trunk;
 vlan-id-list [ 300 400 ];
## Routing Instances Configuration
routing-instances {
 CUSTOMER-A {
 instance-type virtual-switch;
 interface ge-0/0/0.0;
 interface ge-0/0/1.0;
 interface ge-0/0/10.100;
 interface irb.100;
 interface irb.110;
 interface lt-0/0/0.0;
 bridge-domains {
 SALES {
 vlan-id 10;
 routing-interface irb.100;
 ENGINEERING {
 vlan-id 20;
 routing-interface irb.110;
 INTERCONNECT {
 vlan-id 300;
 CUSTOMER-B {
 instance-type virtual-switch;
 interface ge-0/0/2.0;
 interface ge-0/0/10.200;
 interface irb.200;
 bridge-domains {
 RETAIL {
 vlan-id 10;  ## Same as Customer A - no conflict!
 routing-interface irb.200;
 WAREHOUSE {
 vlan-id 20;
 SHARED-SERVICES {
 instance-type virtual-switch;
 interface lt-0/0/0.1;
 bridge-domains {
 SHARED-VLAN {
 vlan-id 300;


1. View Routing Instances
2. Check Bridge Domains in Virtual Switch
3. View MAC Table for Specific Instance
4. Check Logical Tunnel Status
Common Troubleshooting Scenarios
Scenario 1: Traffic Not Passing Between Instances
Symptom: Customer A cannot reach shared services
Diagnostic Commands:
Cause: Logical tunnel not properly configured Solution:
user@router> show route instance
Instance Type
  Primary rib 
CUSTOMER-A virtual-switch 
CUSTOMER-B virtual-switch 
SHARED-SER
[...truncated...]

## 75.10 Part 1: The Conceptual Lecture (The Why)

Part 1: The Conceptual Lecture (The Why)
The Next-Level Redundancy Challenge
In Module 10, we solved link redundancy with LAG. But what happens when the entire switch fails?
The Problems:
1. Design Ring Topology Carefully:
- Place RPL at least-loaded link
- Consider traffic patterns
- Document ring layout and RPL location
2. LAG Best Practices:
- Use LACP active on at least one side
- Match speeds on all member links
- Configure consistent MTU
- Use minimum-links for resilience
3. Monitor Ring Health:
set protocols protection-group ethernet-ring RING-1 statistics
set system syslog file ring-events any info
set system syslog file ring-events match "R-APS|RPL"
4. Test Protection Switching:
# Manual switch test
request protection-group ethernet-ring RING-1 manual-switch east
# Clear manual switch
request protection-group ethernet-ring RING-1 clear
5. Combine Technologies:
- Use LAG for ring interfaces (resilient rings)
- Run ERP over LAG
- Add BFD for faster detection
Traditional LAG Limitation:
[Server]
  | | | |
  LAG0
  | | | |
[Switch A] ← If this fails, server loses all connectivity!
1. Single Point of Failure: One switch failure = total outage
2. Maintenance Windows: Can't upgrade switch without downtime
3. Geographic Limitation: All LAG members must connect to same device


Multi-Chassis LAG (MC-LAG): The Solution
MC-LAG allows a LAG to span multiple switches, providing device-level redundancy:
MC-LAG Components
1. ICL (Inter-Chassis Link)
The backbone connecting MC-LAG p
[...truncated...]

## 75.11 Part 1: The Conceptual Lecture (The Why)

Part 1: The Conceptual Lecture (The Why)
Beyond Basic STP: Protection Mechanisms
While Module 6 covered how STP prevents loops, Module 7 focuses on protecting your spanning-tree topology from both accidental misconfigurations
and deliberate attacks. Think of these features as security guards for your network topology.
user@switch> show spanning-tree interface ge-0/0/10
Interface Port ID State  Role
ge-0/0/10 128:521 LRN DESG <-- Still learning!
user@switch> show configuration protocols rstp interface ge-0/0/10
## No edge configuration
set protocols rstp interface ge-0/0/10 edge
set protocols rstp interface ge-0/0/10 no-root-port
commit
# Verify instant forwarding
show spanning-tree interface ge-0/0/10
State: FWD (should be immediate)
1. Always Use RSTP or MSTP: Original STP is too slow
delete protocols stp
set protocols rstp
2. Design Your Root Bridge: Don't let STP choose randomly
Primary root: Priority 8192
Backup root: Priority 16384
Others: Leave at 32768
3. Use Edge Ports: Speeds up host connections
set protocols rstp interface ge-0/0/[10-20] edge
4. Monitor Topology Changes: Frequent changes indicate problems
show spanning-tree statistics-information
5. Document Expected Topology: Draw which ports should block
Helps troubleshooting
Validates configuration
Identifies unauthorized changes


The New Problems We Face
Problem 1: Rogue Switches
Someone plugs an unauthorized switch into your network. This switch might:
Problem 2: Unidirectional Links
A fiber cable fails in one
[...truncated...]



---

# SECTION 80: LAYER 3 VPNS — PDF EXTRACTED KNOWLEDGE

> **Source:** Layer 3 VPNs study guide (auto-extracted)

## 80.1 Part 1: The Conceptual Lecture (The Why)

Part 1: The Conceptual Lecture (The Why)
The Fundamental Business Problem
Imagine two scenarios:
user@PE1> show security nat source translations
# No translations shown
user@PE1> monitor traffic interface ge-0/0/0.0
# Shows private source IPs going to Internet
user@PE1> show configuration security nat
# Check NAT configuration
user@PE1> show security nat source pool all
# Verify address pools
[edit security nat source rule-set VRF-TO-INTERNET]
set from routing-instance CUSTOMER-A  # Must specify VRF
set to interface ge-0/0/0.0
commit
user@PE1> show route table CUSTOMER-A.inet.0 8.8.8.8
# Route pointing to inet.0
user@PE1> show route table inet.0 8.8.8.8  
# Route pointing back to CUSTOMER-A.inet.0
# Loop detected!
user@PE1> traceroute 8.8.8.8 routing-instance CUSTOMER-A
# TTL expires, shows same hops repeating
user@PE1> show route table inet.0 | match CUSTOMER-A
# Check for incorrect route imports
## Use specific prefixes, not 0/0 in both directions
[edit routing-instances CUSTOMER-A routing-options static]
delete route 0.0.0.0/0 next-table inet.0
[edit routing-instances CUSTOMER-A routing-options static]  
set route 0.0.0.0/0 next-hop 200.1.1.1
## Or use policy to control what gets leaked
[edit policy-options policy-statement LEAK-TO-GLOBAL]
set term 1 from route-filter 10.0.0.0/8 orlonger
set term 1 then accept
set term 2 then reject
commit


The Technical Challenge
MPLS VPNs were designed to work within a single AS because:
Three Inter-AS Options
The IETF defined three opt
[...truncated...]

## 80.2 Part 2: The Junos CLI Masterclass (The How)

Part 2: The Junos CLI Masterclass (The How)
Method 1: Central Internet Gateway Configuration
This is the most common deployment model. We'll configure a PE router to provide Internet access to VPN sites.
Step 1: Configure the VRF with Default Route Generation
 Site A ----[PE1] [Internet GW]
 Site B ----[PE2]----[MPLS Core]----[PE-Central]
 | / |
 Site C ----[PE3] / |
 [VRF-A]  [Global Table]
 
All Internet traffic flows through PE-Central
 Site A ----[PE1]----[Internet]
 [MPLS]
 Site B ----[PE2]----[Internet]
 
Each PE has its own Internet connection
 [PE Routers]
 [VRF-Corporate]  [VRF-Internet]
 Corporate Routes  Internet Routes
 RT: 65000:100 RT: 65000:999
VRF Routing Table Global Routing Table
+------------------+ +------------------+
| 10.1.0.0/24 | | 0.0.0.0/0 (ISP)  |
| 10.2.0.0/24 |  <--> | 8.8.8.8/32 |
| 192.168.0.0/16 | | 200.1.1.0/24 |
+------------------+ +------------------+
 Private Public
 
 Route Leaking allows controlled exchange
Before NAT: After NAT:
Src: 10.1.1.100  ------>  Src: 200.1.1.50
Dst: 8.8.8.8 Dst: 8.8.8.8
(Private) (Public)
[edit routing-instances CUSTOMER-A]
set instance-type vrf


Why next-table? This creates a route that "jumps" from VRF to global table.
Step 2: Configure Reverse Route from Global to VRF
Step 3: Configure NAT for Internet-Bound Traffic
Step 4: Configure Firewall Filter (Security)
Method 2: Internet VRF Configuration
Step 1: Create Internet VRF
Step 2: Configure Route Leaking Between VRFs
set vrf-target target:65000:100
set vr
[...truncated...]

## 80.3 Part 1: The Conceptual Lecture (The Why)

Part 1: The Conceptual Lecture (The Why)
The Fundamental Problem
Picture a large corporation with three divisions: Sales, Engineering, and Corporate Services. Each division has its own private network (VRF -
Virtual Routing and Forwarding instance), completely isolated from the others for security. But here's the challenge: Corporate Services runs shared
resources (like email servers and printers) that both Sales and Engineering need to access.
Route leaking is like creating controlled doorways between these isolated rooms. Without it, you'd need to duplicate all shared resources in each
VRF, which is expensive and inefficient.
Understanding Route Leaking Concepts
Route leaking allows selective sharing of routes between:
Think of it as a sophisticated postal system where certain packages can cross between otherwise separate delivery zones:
user@CE1> show route 10.2.2.0/24
10.2.2.0/24 *[OSPF/10] via ge-0/0/1.0  # Backdoor link
 [OSPF/150] via ge-0/0/0.0 # MPLS path (not preferred)
user@CE1> show ospf route 10.2.2.0/24 detail
Route Type: Intra-area (via backdoor)
Route Type: Inter-area (via MPLS)
user@PE1> show ospf sham-link instance CUSTOMER-A
Sham link to 192.168.255.2, State: Down
  Error: Remote endpoint unreachable
user@PE1> show route table CUSTOMER-A.inet.0 192.168.255.2
# No route found
[edit policy-options policy-statement vrf-export]
term sham-endpoints {
 from {
 protocol direct;
 interface lo0.100;
 then {
 community add vpn-community;
 accept;
1. VRF-to-VRF: Betwe
[...truncated...]

## 80.4 Part 1: The Conceptual Lecture (The Why)

Part 1: The Conceptual Lecture (The Why)
The Control Plane: How Routes Are Distributed
Symptom: Customer can't reach remote sites
Diagnostic Commands:
# Check if routes are being exported
user@PE1> show route advertising-protocol bgp 192.168.1.2 table bgp.l3vpn
[No output - routes not being advertised]
# Check export policy
user@PE1> show configuration routing-instances CUSTOMER-A vrf-export
[Missing or incorrect]
Cause: Missing or incorrect Route Target configuration
Solution:
set routing-instances CUSTOMER-A vrf-target target:65000:100
commit
Symptom: Routes visible but ping fails
Diagnostic Commands:
# Check MPLS forwarding
user@PE1> show route forwarding-table family mpls
Label Type Next hop Interface
299792 VPN 10.1.1.1 ge-0/0/2.0
# Trace MPLS path
user@PE1> traceroute mpls ldp 192.168.1.2
  Probe options: ttl 64, retries 3, wait 10, paths 16, exp 7, fanout 16
  ttl Label  Protocol Address Previous Hop Probe Status
 1 299856  LDP 10.0.0.2 (null) Success
 2 299840  LDP 10.0.0.6 10.0.0.2 Success
 3 Unknown 192.168.1.2 10.0.0.6 Egress
Cause: MPLS not enabled on intermediate interfaces
Solution:
# On each P router
set interfaces ge-0/0/0 unit 0 family mpls
set protocols mpls interface ge-0/0/0.0
set protocols ldp interface ge-0/0/0.0
Symptom: Two customers using same IP range, routes getting mixed
Diagnostic Commands:
# Check Route Distinguisher
user@PE1> show route table bgp.l3vpn.0 10.1.0.0/24 detail
[Shows same RD for different customers]
Cause: Same Route Distinguisher u
[...truncated...]

## 80.5 Part 1: The Conceptual Lecture (The Why)

Part 1: The Conceptual Lecture (The Why)
Advanced L3VPN Failure Modes
While Module 17 covered basic troubleshooting, real-world L3VPN failures often involve complex interactions between multiple protocols. Think of
L3VPN as a multi-story building:
MPLS-Related Problems in L3VPN
MPLS issues are particularly insidious because the control plane might look perfect while the data plane fails silently.
Common MPLS Failure Patterns:
BGP-Related Problems in L3VPN
BGP issues in L3VPN are complex because we're dealing with multiple address families and route reflection:
Forwarding Plane Problems
The forwarding plane is where packets actually move. Problems here mean the control plane shows everything working, but packets get dropped:
[edit]
commit
 ┌────────────────────────────────┐  ← Application Layer
 │ Customer Applications │ (What users see)
 ├────────────────────────────────┤  
 │ VPN Services │  ← L3VPN Service Layer
 │ (VRFs, Route Targets) │ (VPN-specific issues)
 ├────────────────────────────────┤  
 │ BGP Control Plane │  ← BGP Layer
 │ (MP-BGP, Route Reflection) │ (Route propagation issues)
 ├────────────────────────────────┤
 │ MPLS Data Plane │  ← MPLS Layer
 │ (LDP/RSVP, Label Stack) │ (Label switching issues)
 ├────────────────────────────────┤
 │ IGP Infrastructure │  ← IGP Layer
 │ (OSPF/IS-IS) │ (Reachability issues)
 └────────────────────────────────┘
 Problems can occur at ANY layer or BETWEEN layers!
1. Label Distribution Failures
LDP session down but BGP still up
[...truncated...]

## 80.6 Part 2: The Junos CLI Masterclass (The How)

Part 2: The Junos CLI Masterclass (The How)
Configuration for Route Reflection
Step 1: Configure Route Reflector
Without RTC: With RTC:
PE1 (Hosts VRF-A, VRF-B) PE1 (Hosts VRF-A, VRF-B)
Receives: Receives:
- VRF-A routes ✓ - VRF-A routes ✓
- VRF-B routes ✓ - VRF-B routes ✓
- VRF-C routes ✗ (Wasted) - (VRF-C filtered at RR)
- VRF-D routes ✗ (Wasted) - (VRF-D filtered at RR)
- VRF-E routes ✗ (Wasted) - (VRF-E filtered at RR)
Memory saved: 60-90% in large deployments!
Traditional Flat Design: Hierarchical Design:
Every PE connects to every PE PE connects only to local hub
 PE1 ←→ PE2 Level 2: [SuperPE1]--[SuperPE2]
 ↕  ✕  ↕ | |
 PE3 ←→ PE4 Level 1:  PE1,PE2 PE3,PE4
Reduction: O(n²) to O(n)
PE1 → RR: "I only want routes with RT 65000:100 and 65000:200"
RR: "Acknowledged, filtering all others before sending"
Result: Reduced processing and bandwidth usage
Inefficient: Efficient:
PE1: VRF-A,B,C,D,E,F PE1: VRF-A,B (Regional)
PE2: VRF-A,B,C,D,E,F PE2: VRF-C,D (Regional)
PE3: VRF-A,B,C,D,E,F PE3: VRF-E,F (Regional)
Inter-region via Super-PE
Per-Route Memory:
- IPv4 Route: ~200 bytes
- VPNv4 Route: ~300 bytes
- With all attributes: ~500 bytes
1 Million routes = ~500MB just for routes!
Add FIB programming, adjacencies, etc = 2-3GB
CPU Impact:
- BGP Update processing: O(n*m) where n=routes, m=peers
- FIB Programming: O(n)
- Route Resolution: O(n*log n)
[edit protocols bgp group RR-CLIENTS]
set type internal;


Purpose: Establishes router as route reflector for VPNv4 routes with redundancy
[...truncated...]

## 80.7 Part 1: The Conceptual Lecture (The Why)

Part 1: The Conceptual Lecture (The Why)
The Fundamental Challenge
Imagine you're a bank with 100 branches, all connected via MPLS L3VPN. Each branch needs to:
The challenge: VPN traffic travels in a private, isolated routing table (VRF), while Internet traffic needs to reach the global routing table. How do you
provide Internet access to VPN sites without compromising security or creating routing loops?
user@RR> show route table bgp.rtarget.0 | match "65000:100|from PE1"
# Verify RT membership is received
user@RR> show configuration protocols bgp group PE-CLIENTS
# Check if family route-target is configured
[edit protocols bgp group PE-CLIENTS]
set family route-target
commit
user@PE1> show route table VPN-A.inet.0
# Some expected routes present, others missing
user@PE1> show route table bgp.rtarget.0 detail
65000:0:65000:100/96 (1 entry)
 State: <FlashAll>
 Route Preference: 170
 Source: 10.0.0.1
user@PE1> show route table bgp.l3vpn.0 extensive | match "Communities|prefix"
# Check if routes have expected RT communities
[edit routing-instances VPN-A]
set vrf-target target:65000:100
set vrf-target target:65000:101  # Add all required RTs
# Or manually configure RT filter
[edit routing-options route-target-filter]
set 65000:100 local
set 65000:101 local
commit
1. Communicate with headquarters (via VPN)
2. Access the public Internet (for web services)
Branch Office MPLS Core Data Center
[PC]---[CE]---[PE]---[P]---[P]---[PE]---[CE]---[Servers]
 |<-------- VPN Traffic (VRF) ------
[...truncated...]

## 80.8 Part 2: The Junos CLI Masterclass (The How)

Part 2: The Junos CLI Masterclass (The How)
2.1 MVPN Configuration Hierarchy in Junos
In Junos OS, MVPN configuration is hierarchical and builds on L3VPN concepts. Here's the structure:
Additionally, at the top-level (backbone) configuration:
Source A Receiver B
 | (PIM tree (PIM tree
 |  in VRF-A) in VRF-B)
  CE-A CE-B
  PE1 (label + encaps) PE2 (decaps + label removal)
 └───────────── Backbone Multicast Tree ──────────────────┘
 (Carries labeled packets)
[edit routing-instances <instance-name>]
  instance-type vrf # Already covered in L3VPN
  interface <interface> # Customer-facing interface
  routing-options {
 multicast {
 ...multicast-specific settings...
  protocols {
 pim {
 ...PIM configuration for the VRF...
 bgp {
 ...BGP for the VRF (learned routes)...
[edit]
protocols {
  pim {
 ...backbone PIM...
  bgp {
 group <peer-group> {
 family mvrpn {  # Special BGP address family for MVPN!


Key Insight: MVPN configuration is split:
2.2 Pre-Configuration Assumptions
Before we configure MVPN, the following must already be in place:
If any of these are missing, MVPN will not work. This is because MVPN relies on:
2.3 Step-by-Step Configuration Walkthrough
Let's build a complete, working MVPN configuration. We'll configure a scenario with two sites:
Scenario:
Assumption: L3VPN is already configured (VRF created, interfaces assigned, BGP unicast working).
Step 1: Enable Multicast Routing in the Backbone
The backbone must run PIM to support multicast trees.
Explanation:
Step 2:
[...truncated...]

