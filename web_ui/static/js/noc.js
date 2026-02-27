/* ═══════════════════════════════════════════════════════════════
   Junos AI NOC — v21.1 JavaScript
   Dashboard, Topology (D3.js), Config Management, AI Chat,
   Templates, Logs, Scheduler, Workflows — Full MCP + Ollama
   ═══════════════════════════════════════════════════════════════ */

// ─── Global State ───
const state = {
    topology: null,
    devices: [],
    configs: {},
    stats: null,
    templates: [],
    scheduledTasks: [],
    workflows: [],
    currentWorkflow: { name: '', steps: [], variables: {} },
    currentLogFile: null,
    currentView: 'dashboard',
    topoSimulation: null,
    miniSimulation: null,
    pathSimulation: null,
    socket: null,
    theme: localStorage.getItem('noc-theme') || 'dark',
    chatHistory: [],
    // AI Copilot state
    copilotOpen: false,
    copilotHistory: [],
    auditTrail: [],
    aiInsightsCache: {},
    lastConfigViewed: null,
    // Phase 2-4 state
    remediations: [],
    predictions: null,
    lastQueryContext: null,
    liveDeviceData: null,
    // Feature module state
    pools: [],
    notifChannels: [],
    lastPingResults: [],
    capturedResults: []
};

// ─── Init ───
document.addEventListener('DOMContentLoaded', () => {
    setTheme(state.theme);
    initHeaderScroll();
    initSocket();
    initScrollReveal();
    initCardHoverEffects();
    initViewTransitions();
    initSmoothFocusEffects();
    initParallaxOrbs();
    initRippleButtons();
    loadAll();
});

// ═══════════════════════════════════════
//  Dynamic Animation System
// ═══════════════════════════════════════

// Intersection Observer for scroll-reveal animations
function initScrollReveal() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                // Stagger children if they have stagger-child class
                const children = entry.target.querySelectorAll('.stagger-child');
                children.forEach((child, i) => {
                    child.style.animationDelay = `${i * 60}ms`;
                    child.classList.add('revealed');
                });
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.reveal-on-scroll').forEach(el => observer.observe(el));
}

// Magnetic tilt effect on glass cards
function initCardHoverEffects() {
    document.addEventListener('mousemove', (e) => {
        const cards = document.querySelectorAll('.stat-card, .glass-card');
        cards.forEach(card => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            if (x >= 0 && x <= rect.width && y >= 0 && y <= rect.height) {
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                const rotateX = ((y - centerY) / centerY) * -2;
                const rotateY = ((x - centerX) / centerX) * 2;
                card.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-3px) scale(1.01)`;
            }
        });
    });

    document.addEventListener('mouseleave', (e) => {
        if (e.target.closest && (e.target.closest('.stat-card') || e.target.closest('.glass-card'))) {
            e.target.closest('.stat-card, .glass-card').style.transform = '';
        }
    }, true);

    // Reset transform on mouseout for individual cards
    document.addEventListener('mouseout', (e) => {
        const card = e.target.closest('.stat-card, .glass-card');
        if (card && !card.contains(e.relatedTarget)) {
            card.style.transform = '';
        }
    });
}

// Enhanced view switching with fluid transitions
function initViewTransitions() {
    // Observe view changes and re-trigger staggered card animations
    const viewObserver = new MutationObserver((mutations) => {
        mutations.forEach(mutation => {
            if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                const target = mutation.target;
                if (target.classList.contains('view') && target.classList.contains('active')) {
                    // Re-trigger card animations in the new view
                    requestAnimationFrame(() => {
                        triggerViewEntryAnimations(target);
                    });
                }
            }
        });
    });

    document.querySelectorAll('.view').forEach(view => {
        viewObserver.observe(view, { attributes: true, attributeFilter: ['class'] });
    });
}

// Re-trigger staggered card entry when view becomes active
function triggerViewEntryAnimations(viewEl) {
    const animatedElements = viewEl.querySelectorAll(
        '.card, .stat-card, .device-card, .pool-card, .ping-card, .config-item, .insight-card'
    );
    animatedElements.forEach((el, i) => {
        el.style.animation = 'none';
        el.offsetHeight; // force reflow
        el.style.animation = '';
        el.style.animationDelay = `${Math.min(i * 50, 400)}ms`;
    });

    // Also animate the view header
    const header = viewEl.querySelector('.view-header');
    if (header) {
        header.style.animation = 'none';
        header.offsetHeight;
        header.style.animation = 'slideDown 0.4s cubic-bezier(0.22, 1, 0.36, 1) both';
    }
}

// Smooth glass focus ring for inputs
function initSmoothFocusEffects() {
    document.addEventListener('focusin', (e) => {
        const input = e.target.closest('input, select, textarea');
        if (!input) return;
        input.style.transition = 'border-color 0.3s ease, box-shadow 0.3s ease, transform 0.2s ease';
        input.style.transform = 'scale(1.005)';
    });
    document.addEventListener('focusout', (e) => {
        const input = e.target.closest('input, select, textarea');
        if (!input) return;
        input.style.transform = '';
    });
}

// Parallax movement for background glass orbs
function initParallaxOrbs() {
    const orbs = document.querySelectorAll('.glass-orb');
    if (!orbs.length) return;

    let ticking = false;
    document.addEventListener('mousemove', (e) => {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(() => {
            const cx = e.clientX / window.innerWidth - 0.5;
            const cy = e.clientY / window.innerHeight - 0.5;
            orbs.forEach((orb, i) => {
                const depth = (i + 1) * 12;
                orb.style.transform = `translate(${cx * depth}px, ${cy * depth}px)`;
            });
            ticking = false;
        });
    });
}

// Material-style ripple on primary buttons
function initRippleButtons() {
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.btn-primary, .quick-action-btn, .toggle');
        if (!btn) return;

        const ripple = document.createElement('span');
        const rect = btn.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        ripple.style.cssText = `
            position: absolute; border-radius: 50%; pointer-events: none;
            width: ${size}px; height: ${size}px; left: ${x}px; top: ${y}px;
            background: rgba(255,255,255,0.25);
            transform: scale(0); animation: rippleExpand 0.5s ease-out forwards;
        `;
        btn.style.position = 'relative';
        btn.style.overflow = 'hidden';
        btn.appendChild(ripple);
        setTimeout(() => ripple.remove(), 600);
    });

    // Inject ripple keyframe if not present
    if (!document.getElementById('rippleStyle')) {
        const style = document.createElement('style');
        style.id = 'rippleStyle';
        style.textContent = `@keyframes rippleExpand { to { transform: scale(4); opacity: 0; } }`;
        document.head.appendChild(style);
    }
}

// ═══════════════════════════════════════
//  Theme
// ═══════════════════════════════════════
function setTheme(t) {
    state.theme = t;
    document.documentElement.setAttribute('data-theme', t);
    localStorage.setItem('noc-theme', t);
}

function toggleTheme() {
    // Smooth theme transition — fade through a brief overlay
    const overlay = document.createElement('div');
    overlay.style.cssText = `
        position: fixed; inset: 0; z-index: 99999;
        background: ${state.theme === 'dark' ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)'};
        pointer-events: none; opacity: 1;
        transition: opacity 0.4s ease;
    `;
    document.body.appendChild(overlay);
    requestAnimationFrame(() => {
        setTheme(state.theme === 'dark' ? 'light' : 'dark');
        overlay.style.opacity = '0';
        setTimeout(() => overlay.remove(), 450);
    });
    // re-render topology with updated colors
    if (state.topology && state.currentView === 'topology') setTimeout(() => renderTopology(), 50);
}

// ═══════════════════════════════════════
//  Navigation — Horizontal Glass Header
// ═══════════════════════════════════════

function switchView(view) {
    state.currentView = view;

    // Smooth cross-fade: exit current, enter next
    const allViews = document.querySelectorAll('.view');
    const nextView = document.getElementById('view-' + view);

    allViews.forEach(v => {
        if (v.classList.contains('active') && v !== nextView) {
            v.style.opacity = '0';
            v.style.transform = 'translateY(8px)';
            setTimeout(() => {
                v.classList.remove('active');
                v.style.opacity = '';
                v.style.transform = '';
            }, 150);
        }
    });

    if (nextView) {
        setTimeout(() => {
            nextView.classList.add('active');
        }, 80);
    }

    // Update nav active states — top-level .nav-btn
    document.querySelectorAll('.nav-btn[data-view]').forEach(b => b.classList.remove('active'));
    const navBtn = document.querySelector(`.nav-btn[data-view="${view}"]`);
    if (navBtn) navBtn.classList.add('active');

    // Update dropdown items
    document.querySelectorAll('.dropdown-item[data-view]').forEach(b => b.classList.remove('active'));
    const dropItem = document.querySelector(`.dropdown-item[data-view="${view}"]`);
    if (dropItem) {
        dropItem.classList.add('active');
        // Also highlight the parent dropdown trigger
        const parentDropdown = dropItem.closest('.nav-dropdown');
        if (parentDropdown) {
            const trigger = parentDropdown.querySelector('.nav-dropdown-trigger');
            if (trigger) trigger.classList.add('active');
        }
    }

    // Close mobile menu if open
    closeMobileMenu();

    if (view === 'topology' && state.topology) renderTopology();
    if (view === 'pathfinder' && state.topology) renderPathTopology();
    if (view === 'templates') renderTemplateList();
    if (view === 'scheduler') { loadScheduledTasks(); populateSchedulerRouters(); }
    if (view === 'workflows') renderWorkflowList();
    if (view === 'pools') { loadPools(); populatePoolDevices(); }
    if (view === 'ping') populatePingRouters();
    if (view === 'validation') populateValidationRouters();
    if (view === 'notifications') loadNotificationChannels();
    if (view === 'git-export') loadGitLog();
    if (view === 'compare') { loadCapturedResults(); populateCompareRouters(); }
    if (view === 'discovery') populateNewViewRouters('discoveryRouter');
    if (view === 'traffic') populateNewViewRouters('trafficRouter');
    if (view === 'security') populateNewViewRouters('securityRouter');
    if (view === 'dns') populateNewViewRouters('dnsRouter', 'dnsReverseRouter', 'dnsBatchRouter');
    if (view === 'capacity') populateCapacitySelectors();
    if (view === 'investigate') renderInvestigationView();
    if (view === 'remediate') renderRemediationView();
    if (view === 'predictive') renderPredictiveView();

    // AI Copilot: Update context awareness
    updateCopilotContext(view);
    logAuditAction('navigate', `Switched to ${view} view`);
}

// ─── Dropdown Navigation ───
function toggleNavDropdown(id) {
    const dropdown = document.getElementById(id);
    if (!dropdown) return;

    const wasOpen = dropdown.classList.contains('open');
    closeAllDropdowns();

    if (!wasOpen) {
        dropdown.classList.add('open');
        const backdrop = document.getElementById('dropdownBackdrop');
        if (backdrop) backdrop.classList.add('active');
    }
}

function closeAllDropdowns() {
    document.querySelectorAll('.nav-dropdown.open').forEach(d => d.classList.remove('open'));
    const backdrop = document.getElementById('dropdownBackdrop');
    if (backdrop) backdrop.classList.remove('active');
}

// ─── Mobile Menu ───
function toggleMobileMenu() {
    const nav = document.getElementById('mainNav');
    if (nav) nav.classList.toggle('mobile-open');
}

function closeMobileMenu() {
    const nav = document.getElementById('mainNav');
    if (nav) nav.classList.remove('mobile-open');
}

// ─── Header Scroll Effect ───
function initHeaderScroll() {
    const header = document.getElementById('mainHeader');
    if (!header) return;
    window.addEventListener('scroll', () => {
        header.classList.toggle('scrolled', window.scrollY > 20);
    }, { passive: true });
}

// Close dropdowns on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeAllDropdowns();
        closeMobileMenu();
        closeViewHelp();
    }
});

// ═══════════════════════════════════════
//  HELP SYSTEM — Per-View Contextual Help
// ═══════════════════════════════════════

const VIEW_HELP = {
    'dashboard': {
        purpose: 'Real-time network health overview combining live MCP device data with golden config topology analysis.',
        inputs: 'No input required — auto-loads on startup and refreshes every 30 seconds.',
        outputs: '6 stat cards (devices, links, BGP sessions, redundancy score, graph diameter, SPOFs), mini topology, role distribution chart, protocol health bars, and a full device inventory table.',
        tips: ['Use AI Health Check for a plain-English summary of network state', 'Device status shows Live / Down / Config-only based on MCP connectivity', 'Click "Expand →" on the topology card to enter the interactive topology view']
    },
    'topology': {
        purpose: 'Interactive D3.js force-directed topology map showing physical links, IS-IS adjacencies, and iBGP sessions.',
        inputs: 'Toggle IS-IS, iBGP, LDP layers. Switch layout (Force / Hierarchical / Radial / Circular). Click nodes for detail panels.',
        outputs: 'Draggable, zoomable topology. Node detail panel shows interfaces, IS-IS neighbors, and BGP sessions. AI bar provides redundancy and capacity analysis on demand.',
        tips: ['Click any node to open its protocol detail panel', 'Radial layout is best for hierarchical PE / P / RR networks', 'AI Redundancy analysis identifies single points of failure in real time']
    },
    'devices': {
        purpose: 'Complete device inventory with per-router protocol summary cards and quick-action buttons.',
        inputs: 'No input required — automatically populated from golden configs in the MCP store.',
        outputs: 'Device cards showing role, loopback IP, interface count, IS-IS / BGP / LDP status, and live MCP reachability badge.',
        tips: ['Cards show live MCP status when the MCP server is connected', 'Click a device name to jump to its golden config in the Config viewer']
    },
    'configs': {
        purpose: 'Browse, search, and AI-audit golden configurations fetched from MCP-connected routers.',
        inputs: 'Select a device from the list, or search across all configs using plain text or regex.',
        outputs: 'Config viewer with syntax highlighting. AI Audit highlights security issues, missing best practices, and anomalies with severity ratings.',
        tips: ['Enable Regex toggle for advanced pattern searches (e.g. "neighbor .*route-reflector")', 'AI Drift Check compares configs across all devices to find inconsistencies', 'Sync from MCP fetches fresh configs directly from live routers']
    },
    'pathfinder': {
        purpose: 'Computes IS-IS metric-based shortest paths between any two routers using Dijkstra\'s algorithm applied to golden config data.',
        inputs: 'Select source router and target router from the dropdowns, then click Find Path.',
        outputs: 'Ordered hop list with per-link IS-IS metrics and total path cost. Alternative equal-cost paths shown when available. Topology map highlights the computed route.',
        tips: ['Paths are computed offline from golden config IS-IS adjacencies', 'Multiple paths are shown if ECMP exists', 'Use this before a maintenance window to understand traffic impact']
    },
    'ai-chat': {
        purpose: 'Full conversational AI interface powered by the 7-layer Brain Engine with RAG knowledge base, chain-of-thought reasoning, and full topology context.',
        inputs: 'Type any question about your network, or use the quick-action buttons for structured analyses.',
        outputs: 'Streamed AI responses with expandable chain-of-thought reasoning panel, confidence scores, and actionable recommendations.',
        tips: ['The AI has full knowledge of your topology — ask specific device questions', 'Quick buttons run structured analyses like BGP Audit and SPOF Remediation', 'Shift+Enter adds a new line; Enter sends the message']
    },
    'templates': {
        purpose: 'Jinja2 template rendering engine for generating router configurations from variables, with one-click MCP deployment to live routers.',
        inputs: 'Select a template from the sidebar. Fill in YAML or JSON variables. Choose a target router for deployment.',
        outputs: 'Rendered configuration preview with line count. Deployment result from MCP commit with diff summary.',
        tips: ['Always preview the rendered output before deploying', 'Variables can be YAML or JSON format', 'The AI audits rendered configs for best-practice compliance before deployment']
    },
    'logs': {
        purpose: 'Browse and AI-analyze system log files from the NOC application and MCP server.',
        inputs: 'Select a log file. Set level filter (ERROR / WARNING / INFO / DEBUG), search text, and tail N lines, then click Apply.',
        outputs: 'Color-coded log view by severity. AI Analysis identifies error patterns, root causes, and recurring issues.',
        tips: ['Use ERROR filter to instantly surface failures', 'AI Analyze reads the full log and produces a structured summary', '"Tail 100" shows the most recent 100 entries for quick triage']
    },
    'scheduler': {
        purpose: 'Schedule recurring Junos commands to run automatically against selected routers at defined intervals via MCP.',
        inputs: 'Task name, interval (30s to daily), Junos command string, and target routers (multi-select).',
        outputs: 'Active tasks table with last-run time, execution count, and status. Results stored per execution for later review.',
        tips: ['5-minute intervals are ideal for health check commands', 'Tasks survive server restarts and resume automatically', 'Click a task row to view its most recent output']
    },
    'workflows': {
        purpose: 'Visual workflow builder to chain MCP operations, template renders, AI analyses, conditions, and notifications into automated playbooks.',
        inputs: 'Add steps from the type dropdown (MCP Command, Batch, Template, AI Analyze, Condition, Wait, REST Call, Python, Ping Sweep, Validate, Notify). Name the workflow and save.',
        outputs: 'Step-by-step execution results with per-step output. Workflows can be saved and re-executed on demand.',
        tips: ['Use Condition steps to branch on command output — e.g. "if BGP not Established, notify"', 'Chain: Ping Sweep → AI Analyze → Notify for a fully automated health check', 'Save workflows as reusable playbooks accessible from the sidebar']
    },
    'pools': {
        purpose: 'Organize devices into named logical groups (pools) by role, location, or function for targeted bulk operations.',
        inputs: 'Create pools manually with device selection, or click AI Recommend to auto-group devices based on topology roles.',
        outputs: 'Color-coded pool cards with member devices and tags. Pools can be used as targets in Workflows and the Scheduler.',
        tips: ['AI Recommend creates intelligent pools based on PE / P / RR detection from golden configs', 'Pools are persistent and survive server restarts', 'Use pools as Workflow targets to run commands against a logical group']
    },
    'ping': {
        purpose: 'ICMP-equivalent reachability testing via MCP — ping individual routers or sweep the entire fleet in parallel.',
        inputs: 'Select a target router for single ping, or click Sweep All for a fleet-wide parallel reachability check.',
        outputs: 'Per-device result cards (Reachable / Unreachable) with response time. AI Analysis correlates unreachable devices with topology to identify root cause.',
        tips: ['Sweep All runs all pings in parallel — results appear as they complete', 'AI Analyze correlates unreachable devices with IS-IS topology to find the likely failure point', 'Combine with Workflows to auto-alert on ping failures']
    },
    'validation': {
        purpose: 'Validate Junos command outputs against expected patterns — text match, regex, or negation — with AI compliance auditing.',
        inputs: 'Router, Junos command, expected pattern, and match type (Contains / Regex / Not Contains / Exact). Or run batch across all routers simultaneously.',
        outputs: 'Pass/Fail result per router with matched output snippet. AI Compliance Audit generates a full CIS-style compliance report.',
        tips: ['Regex mode supports full Python regex patterns', 'Batch Validate runs the same check across all devices simultaneously', 'AI Compliance generates a detailed report with specific Junos remediation commands']
    },
    'notifications': {
        purpose: 'Configure Slack, Mattermost, or generic webhook notification channels for automated NOC alerts with AI-generated summaries.',
        inputs: 'Add a channel (name, type, webhook URL). Test with custom severity, title, and message.',
        outputs: 'Active channel list with status. Test notification delivery confirmation. AI Summary generates an executive-level alert narrative from history.',
        tips: ['Workflows can trigger notifications as a step in an automated playbook', 'Supports multiple channels for routing different severity levels differently', 'Leave message blank in test — AI Summary will generate a contextual message']
    },
    'git-export': {
        purpose: 'Version-control golden configurations using Git, with AI-generated commit messages describing what changed.',
        inputs: 'Click Init Repo (first time only), then Export & Commit. Optionally provide a custom commit message.',
        outputs: 'Git commit with all config files. Commit history with change summary. AI-generated messages describe config diffs in plain English.',
        tips: ['Leave the commit message blank for AI to auto-generate a descriptive message', 'Commit history shows exactly which lines changed between syncs', 'Configs are stored in the /config_backups/git/ directory on the server']
    },
    'compare': {
        purpose: 'Capture Junos command outputs at different points in time and compare them side-by-side with AI diff analysis.',
        inputs: 'Name + router + command → Capture. Select two captured results from the dropdowns → Compare.',
        outputs: 'Side-by-side diff highlighting added (green) and removed (red) lines. AI analysis explains what changed and its operational impact.',
        tips: ['Capture before and after a maintenance window to validate changes', 'AI diff analysis flags unexpected changes and explains their significance', 'Captures are persistent and survive server restarts']
    },
    'discovery': {
        purpose: 'Infrastructure scanning via MCP — discovers interfaces, LLDP neighbors, ARP tables, and OS versions across the fleet.',
        inputs: 'Select a router for per-device discovery (Interfaces / Neighbors / Detail Stats). Or click Run Full Scan for a fleet-wide scan.',
        outputs: 'Raw discovery output from Junos. AI Infrastructure Analysis builds a complete physical connectivity map from the results.',
        tips: ['Full Scan executes all discovery commands across all devices simultaneously', 'LLDP Neighbors reveals actual physical cabling and undocumented connections', 'AI analysis identifies links not present in golden configs']
    },
    'traffic': {
        purpose: 'Protocol statistics, interface counters, flow analysis, and session tracking from live routers via MCP.',
        inputs: 'Select a router and choose an analysis type (Protocol Stats / Interface Counters / Flow Analysis / Sessions). Optionally filter by interface.',
        outputs: 'Raw Junos output. AI analysis with performance, security, or anomaly focus depending on the selected mode.',
        tips: ['Interface filter (e.g. ge-0/0/0) narrows output to a specific port', 'Security focus mode detects suspicious traffic patterns like unexpected sessions', 'Anomaly detection mode flags interface counters that deviate from baseline']
    },
    'security': {
        purpose: 'Comprehensive security audit suite — threat detection, firewall analysis, cleartext credential scanning, and CIS-style hardening reports.',
        inputs: 'Select a router for per-device Security Audit, Threat Detection, or Hardening Report. Fleet-wide Credential Scan runs across all devices automatically.',
        outputs: 'Security findings per device. AI analysis with severity-ranked issues. Hardening Report includes specific Junos config commands to fix each finding.',
        tips: ['Credential Scan checks ALL configs for cleartext passwords and weak community strings', 'Hardening Report generates actionable "set" commands — review before applying', 'Protocol Health Check validates BGP and IS-IS authentication across all sessions']
    },
    'dns': {
        purpose: 'DNS resolution testing from the router\'s perspective — forward lookups, reverse lookups, batch queries, and config audit across all routers.',
        inputs: 'Router + domain for forward lookup. Router + IP for reverse lookup. Comma-separated domains for batch lookup. AI Audit runs automatically across all routers.',
        outputs: 'DNS query results as seen from the router. AI Config Audit compares DNS configuration across all devices for consistency and redundancy.',
        tips: ['Testing from the router perspective reveals DNS reachability issues that client-side tests miss', 'AI Config Audit finds routers with missing, mismatched, or insecure DNS server configurations', 'Batch lookup tests multiple domains simultaneously from a single router']
    },
    'investigate': {
        purpose: 'AI-powered deep investigation engine using the 7-layer Brain Engine — classifies symptoms, gathers multi-source evidence, and produces root cause analysis.',
        inputs: 'Describe a network problem in plain English, or select a symptom category. The AI orchestrates multi-layer analysis automatically.',
        outputs: 'Step-by-step chain-of-thought reasoning, root cause identification with confidence score, affected devices, and ranked remediation options.',
        tips: ['Be specific: "PE1 is dropping BGP sessions to 10.0.0.1" yields better results than "BGP problem"', 'The Brain Engine runs Protocol Specialists in parallel for deep analysis', 'Investigation results feed directly into the Remediation Center']
    },
    'remediate': {
        purpose: 'AI-generated remediation playbooks with review-before-deploy — fixes network issues identified by the Investigation Engine.',
        inputs: 'Review AI-recommended fixes. Select remediation actions to apply. Approve deployment per router via MCP.',
        outputs: 'Junos "set" commands with expected outcome for each fix. MCP deployment result with commit confirmation. Rollback plan if needed.',
        tips: ['Always review the generated Junos diff before deploying to production', 'All remediations are logged in the Audit Trail for compliance', 'Rollback plan is generated alongside every fix — keep it handy']
    },
    'predictive': {
        purpose: 'Ensemble AI analysis combining topology graph metrics, protocol health scores, and historical patterns to forecast network risks before they cause outages.',
        inputs: 'No input required — click Generate to run the full ensemble analysis on all available network data.',
        outputs: 'Risk scores per device, failure probability forecast, protocol degradation trends, capacity bottleneck analysis, and preemptive recommendations.',
        tips: ['Run weekly for proactive network management', 'High-risk devices should be immediately investigated using the Investigation Engine', 'Capacity recommendations include both configuration changes and hardware upgrade suggestions']
    },
    'capacity': {
        purpose: 'What-if failure simulation, multi-path analysis, and AI-powered capacity planning to understand network resilience and growth requirements.',
        inputs: 'Select a node or link pair for failure simulation. Select source/target for multi-path analysis. Click Generate Capacity Plan for full AI analysis.',
        outputs: 'Impact of simulated failure (affected paths, traffic re-routing). All computed paths between node pairs with costs. AI capacity plan with bottleneck analysis and upgrade roadmap.',
        tips: ['Simulate the failure of your most critical core node first to understand blast radius', 'Multi-path shows all equal and unequal cost paths — useful for ECMP verification', 'AI Capacity Plan generates a full growth recommendation report based on current topology']
    }
};

function showViewHelp(viewName) {
    const help = VIEW_HELP[viewName];
    if (!help) return;

    const modal = document.getElementById('helpModal');
    const title = document.getElementById('helpModalTitle');
    const body = document.getElementById('helpModalBody');
    if (!modal || !title || !body) return;

    // Get h2 text for title
    const viewEl = document.getElementById(`view-${viewName}`);
    const h2 = viewEl ? viewEl.querySelector('h2') : null;
    title.textContent = h2 ? h2.textContent : viewName;

    const tipsHtml = (help.tips || []).map(t =>
        `<div class="help-tip"><span class="help-tip-dot"></span><span>${t}</span></div>`
    ).join('');

    body.innerHTML = `
        <div class="help-modal-section">
            <h4>Purpose</h4>
            <p>${help.purpose}</p>
        </div>
        <div class="help-divider"></div>
        <div class="help-modal-section">
            <h4>Inputs</h4>
            <p>${help.inputs}</p>
        </div>
        <div class="help-divider"></div>
        <div class="help-modal-section">
            <h4>Expected Output</h4>
            <p>${help.outputs}</p>
        </div>
        ${help.tips && help.tips.length ? `
        <div class="help-divider"></div>
        <div class="help-modal-section">
            <h4>Tips</h4>
            <div class="help-tips">${tipsHtml}</div>
        </div>` : ''}
    `;

    modal.style.display = 'flex';
    if (typeof lucide !== 'undefined') lucide.createIcons();
    logAuditAction('navigate', `Viewed help: ${viewName}`);
}

function closeViewHelp() {
    const modal = document.getElementById('helpModal');
    if (modal) modal.style.display = 'none';
}


// ═══════════════════════════════════════
//  AI COPILOT — Agentic Digital Partner
// ═══════════════════════════════════════

function toggleAICopilot() {
    state.copilotOpen = !state.copilotOpen;
    const sidebar = document.getElementById('aiCopilotSidebar');
    const overlay = document.getElementById('aiCopilotOverlay');
    if (sidebar) sidebar.classList.toggle('open', state.copilotOpen);
    if (overlay) overlay.classList.toggle('active', state.copilotOpen);
    if (state.copilotOpen) {
        updateCopilotContext(state.currentView);
        generateViewInsights(state.currentView);
        loadCopilotSuggestions(state.currentView);
        if (typeof lucide !== 'undefined') lucide.createIcons();
    }
}

function clearCopilotChat() {
    state.copilotHistory = [];
    const el = document.getElementById('copilotMessages');
    if (el) el.innerHTML = '';
}

function toggleCopilotSection(section) {
    const idMap = { audit: 'auditTrailBody', insights: 'insightsBody', suggestions: 'copilotSuggestionsBody' };
    const id = idMap[section] || 'insightsBody';
    const header = document.getElementById(id)?.previousElementSibling;
    const body = document.getElementById(id);
    if (header) header.classList.toggle('collapsed');
    if (body) body.classList.toggle('collapsed');
}

// ─── Audit Trail ───
function logAuditAction(type, text, aiNote) {
    const entry = {
        type,
        text,
        aiNote: aiNote || null,
        time: new Date()
    };
    state.auditTrail.unshift(entry);
    if (state.auditTrail.length > 50) state.auditTrail.pop();
    renderAuditTrail();
    // Auto-generate AI commentary for important actions
    if (!aiNote && ['deploy', 'execute', 'create', 'delete', 'config_view'].includes(type)) {
        generateAuditComment(entry, state.auditTrail.length - 1);
    }
}

function renderAuditTrail() {
    const body = document.getElementById('auditTrailBody');
    const count = document.getElementById('auditCount');
    if (!body) return;
    if (count) count.textContent = state.auditTrail.length;

    if (!state.auditTrail.length) {
        body.innerHTML = '<div class="audit-empty">No actions recorded yet. Start interacting with the NOC.</div>';
        return;
    }

    body.innerHTML = state.auditTrail.slice(0, 20).map(a => {
        const icons = {
            navigate: '<i data-lucide="compass" style="width:12px;height:12px"></i>',
            deploy: '<i data-lucide="upload" style="width:12px;height:12px"></i>',
            execute: '<i data-lucide="zap" style="width:12px;height:12px"></i>',
            create: '<i data-lucide="plus-circle" style="width:12px;height:12px"></i>',
            delete: '<i data-lucide="trash-2" style="width:12px;height:12px"></i>',
            config_view: '<i data-lucide="file-text" style="width:12px;height:12px"></i>',
            search: '<i data-lucide="search" style="width:12px;height:12px"></i>',
            ai: '<i data-lucide="bot" style="width:12px;height:12px"></i>',
            warning: '<i data-lucide="alert-triangle" style="width:12px;height:12px"></i>',
            ping: '<i data-lucide="radio" style="width:12px;height:12px"></i>',
            validate: '<i data-lucide="check-circle-2" style="width:12px;height:12px"></i>'
        };
        const icon = icons[a.type] || '<i data-lucide="pin" style="width:12px;height:12px"></i>';
        const timeStr = a.time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        const cls = a.aiNote ? 'audit-item ai-comment' : `audit-item ${a.type === 'warning' ? 'warning' : 'action'}`;

        return `<div class="${cls}">
            <div class="audit-icon">${icon}</div>
            <div class="audit-content">
                <div class="audit-text">${escapeHtml(a.text)}</div>
                ${a.aiNote ? `<div class="audit-ai-note"><i data-lucide="bot" style="width:11px;height:11px;display:inline-block;vertical-align:middle;margin-right:4px"></i>${escapeHtml(a.aiNote)}</div>` : ''}
                <div class="audit-time">${timeStr}</div>
            </div>
        </div>`;
    }).join('');
    // Re-initialize Lucide icons for dynamically added content
    if (typeof lucide !== 'undefined') lucide.createIcons();
}

async function generateAuditComment(entry, index) {
    try {
        const resp = await fetch('/api/ai/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                data: `User action: ${entry.text}\nCurrent view: ${state.currentView}\nNetwork: ${state.topology?.nodes?.length || 0} devices`,
                question: 'Provide a brief 1-sentence AI assessment of this user action. Be helpful and proactive. If there are risks, mention them concisely.',
                system: 'You are an AI NOC partner. Give a single concise sentence about this network operations action. Be direct, helpful, and mention any risks or suggestions. Do NOT use markdown formatting.'
            })
        });
        const data = await resp.json();
        if (data.analysis && state.auditTrail[0]?.text === entry.text) {
            state.auditTrail[0].aiNote = data.analysis.substring(0, 150);
            renderAuditTrail();
        }
    } catch (e) { /* AI unavailable, skip audit commentary */ }
}

// ─── Context Awareness ───
function updateCopilotContext(view) {
    const contextMap = {
        'dashboard': 'Watching: Dashboard — Monitoring network health',
        'topology': 'Watching: Topology — Analyzing network structure',
        'ai-chat': 'Active: Full AI Conversation Mode',
        'devices': 'Watching: Device Inventory',
        'configs': 'Watching: Configuration Management',
        'templates': 'Watching: Template Engine — Ready to audit deployments',
        'logs': 'Watching: Log Forensics — Scanning for anomalies',
        'scheduler': 'Watching: Task Scheduler — Monitoring active jobs',
        'workflows': 'Watching: Workflow Builder — Ready to validate steps',
        'pools': 'Watching: Device Pools',
        'ping': 'Watching: Reachability Testing',
        'pathfinder': 'Watching: Path Analysis',
        'validation': 'Watching: Data Validation',
        'notifications': 'Watching: Alert Channels',
        'git-export': 'Watching: Git Version Control',
        'compare': 'Watching: Result Comparison'
    };
    const el = document.getElementById('copilotContextText');
    if (el) el.textContent = contextMap[view] || `Watching: ${view}`;
}

// ─── AI Insights (auto-generated per view) ───
async function generateViewInsights(view) {
    const body = document.getElementById('insightsBody');
    if (!body) return;

    // Use cached if fresh (< 60s)
    // DISABLED: Always fetch fresh AI insights — no stale data
    // if (state.aiInsightsCache[view] && Date.now() - state.aiInsightsCache[view].time < 60000) {
    //     body.innerHTML = state.aiInsightsCache[view].html;
    //     return;
    // }

    body.innerHTML = '<div class="insight-card"><div class="copilot-typing"><span></span><span></span><span></span></div></div>';

    let insightData = '';
    let question = '';

    if (view === 'dashboard' && state.topology) {
        insightData = `Devices: ${state.topology.nodes?.length}, Links: ${state.topology.links?.length}, SPOFs: ${state.stats?.single_points_of_failure?.length || 0}, Redundancy: ${state.stats?.redundancy_score || 'unknown'}`;
        question = 'Give 2-3 bullet insights about this network health. Be concise. Any issues?';
    } else if (view === 'topology' && state.topology) {
        insightData = `Nodes: ${state.topology.nodes?.map(n => n.id + '(' + n.role + ')').join(', ')}`;
        question = 'Give 2 bullet topology design insights. Note any redundancy issues.';
    } else if (view === 'configs') {
        insightData = `Golden configs for ${state.topology?.nodes?.length || 0} routers available`;
        question = 'Give 2 bullet points about configuration management best practices for this network.';
    } else {
        // Generic insight
        body.innerHTML = `<div class="insight-card info">
            <div class="insight-card-header"><i data-lucide="info"></i> Tip</div>
            <div class="insight-card-body">Use the AI quick actions above or ask me anything about this view in the chat below.</div>
        </div>`;
        if (typeof lucide !== 'undefined') lucide.createIcons();
        return;
    }

    try {
        const resp = await fetch('/api/ai/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                data: insightData,
                question,
                system: 'You are an AI NOC partner. Give very concise bullet insights (2-3 max). Each bullet is max 15 words. Use • for bullets. No headers or markdown.'
            })
        });
        const data = await resp.json();
        const analysis = data.analysis || 'AI analysis unavailable';
        const bullets = analysis.split('\n').filter(l => l.trim()).slice(0, 3);

        const html = bullets.map((b, i) => {
            const types = ['success', 'info', 'warning'];
            const icons = ['check-circle', 'info', 'alert-triangle'];
            return `<div class="insight-card ${types[i % 3]}">
                <div class="insight-card-header"><i data-lucide="${icons[i % 3]}"></i></div>
                <div class="insight-card-body">${escapeHtml(b.replace(/^[•\-\*]\s*/, ''))}</div>
            </div>`;
        }).join('');

        body.innerHTML = html;
        state.aiInsightsCache[view] = { html, time: Date.now() };
        if (typeof lucide !== 'undefined') lucide.createIcons();
    } catch (e) {
        body.innerHTML = `<div class="insight-card info">
            <div class="insight-card-body">AI engine offline — insights unavailable</div>
        </div>`;
    }
}

// ─── Copilot Chat (sidebar mini-chat) ───
async function sendCopilotMessage() {
    const input = document.getElementById('copilotInput');
    const msg = input.value.trim();
    if (!msg) return;
    input.value = '';

    appendCopilotMessage('user', msg);
    state.copilotHistory.push({ role: 'user', content: msg });

    // Show typing
    const container = document.getElementById('copilotMessages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'copilot-msg ai copilot-typing-msg';
    typingDiv.innerHTML = '<div class="copilot-msg-avatar"><i data-lucide="sparkles" style="width:14px;height:14px"></i></div><div class="copilot-msg-bubble"><div class="copilot-typing"><span></span><span></span><span></span></div></div>';
    container.appendChild(typingDiv);
    container.scrollTop = container.scrollHeight;

    try {
        // Add context awareness to the message
        const context = `Current view: ${state.currentView}. Network: ${state.topology?.nodes?.length || 0} devices, ${state.topology?.links?.length || 0} links.`;

        // Use agentic endpoint for richer responses
        const resp = await fetch('/api/ai/chat-agentic', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: `[Context: ${context}] ${msg}`,
                history: state.copilotHistory.slice(-8)
            })
        });

        typingDiv.remove();

        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const data = await resp.json();

        let responseText = data.response || 'No response';
        // Add confidence badge to copilot responses
        let prefix = '';
        if (data.type === 'investigation') prefix = '<span class="copilot-badge brain"><i data-lucide="brain" style="width:12px;height:12px;display:inline-block;vertical-align:middle"></i> Brain</span> ';
        else if (data.type === 'knowledge') prefix = '<span class="copilot-badge rag"><i data-lucide="book-open" style="width:12px;height:12px;display:inline-block;vertical-align:middle"></i> RAG</span> ';
        else if (data.type === 'quick_status') prefix = '<span class="copilot-badge quick"><i data-lucide="zap" style="width:12px;height:12px;display:inline-block;vertical-align:middle"></i> Quick</span> ';

        const bubble = appendCopilotMessage('ai', prefix + responseText);
        state.copilotHistory.push({ role: 'assistant', content: responseText });
        state.lastQueryContext = { query: msg, type: data.type };

    } catch (e) {
        typingDiv.remove();
        appendCopilotMessage('ai', 'AI unavailable. Try the full AI Chat view.');
    }
}

function appendCopilotMessage(role, text) {
    const container = document.getElementById('copilotMessages');
    const div = document.createElement('div');
    div.className = `copilot-msg ${role}`;
    const avatar = role === 'ai' ? '<i data-lucide="sparkles" style="width:14px;height:14px"></i>' : '<i data-lucide="user" style="width:14px;height:14px"></i>';
    const bubble = document.createElement('div');
    bubble.className = 'copilot-msg-bubble';
    bubble.innerHTML = text ? formatChatText(text) : '';
    div.innerHTML = `<div class="copilot-msg-avatar">${avatar}</div>`;
    div.appendChild(bubble);
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
    if (typeof lucide !== 'undefined') lucide.createIcons();
    return bubble;
}

// ─── AI Quick Actions (embedded in each view) ───
async function aiQuickAction(view, action) {
    logAuditAction('ai', `AI quick action: ${action} on ${view}`);

    // Open copilot and show result there
    if (!state.copilotOpen) toggleAICopilot();

    const actionPrompts = {
        'dashboard|health': {
            data: () => `Network: ${state.topology?.nodes?.length || 0} devices, ${state.topology?.links?.length || 0} links. SPOFs: ${JSON.stringify(state.stats?.single_points_of_failure || [])}. Redundancy: ${state.stats?.redundancy_score || 'unknown'}. Diameter: ${state.stats?.diameter || 'unknown'}.`,
            question: 'Give a comprehensive network health assessment. Score the network 1-10 and list any urgent issues with recommendations.'
        },
        'dashboard|anomalies': {
            data: () => {
                const nodes = state.topology?.nodes || [];
                return `Nodes: ${nodes.map(n => `${n.id}(${n.role},BGP:${n.bgp_neighbors?.length||0},ISIS:${n.isis_interfaces?.length||0},LDP:${n.ldp},MPLS:${n.mpls})`).join('; ')}`;
            },
            question: 'Analyze for anomalies: devices missing expected protocols, unusual configurations, or inconsistencies. List specific findings.'
        },
        'dashboard|recommendations': {
            data: () => `Network stats: ${JSON.stringify(state.stats || {})}. Devices: ${state.topology?.nodes?.length || 0}`,
            question: 'Give 3-5 specific optimization recommendations for this network. Include capacity planning, redundancy improvements, and protocol tuning.'
        },
        'topology|redundancy': {
            data: () => `Topology: ${state.topology?.nodes?.length || 0} nodes, ${state.topology?.links?.length || 0} links. SPOFs: ${JSON.stringify(state.stats?.single_points_of_failure || [])}`,
            question: 'Analyze topology redundancy. Identify weakest links, suggest where to add redundant paths, and rate overall resilience.'
        },
        'topology|capacity': {
            data: () => {
                const nodes = state.topology?.nodes || [];
                return nodes.map(n => `${n.id}: ${(n.interfaces||[]).length} interfaces, ${n.bgp_neighbors?.length||0} BGP peers`).join('; ');
            },
            question: 'Analyze capacity: which nodes have the most connections, which are potential bottlenecks, and where should capacity be added?'
        },
        'configs|audit': {
            data: () => `Viewing config for: ${state.lastConfigViewed || 'none'}. Total routers: ${state.topology?.nodes?.length || 0}`,
            question: state.lastConfigViewed ?
                `Audit the configuration for ${state.lastConfigViewed}. Check for security issues, missing best practices, and optimization opportunities.` :
                'Suggest which configurations should be audited first and why.'
        },
        'configs|drift': {
            data: () => `Routers: ${(state.topology?.nodes || []).map(n => n.id).join(', ')}`,
            question: 'Explain how to detect configuration drift across these routers. What key areas should be compared? Suggest a drift detection strategy.'
        }
    };

    const key = `${view}|${action}`;
    const prompt = actionPrompts[key];

    if (!prompt) {
        appendCopilotMessage('ai', `Running ${action} analysis on ${view}...`);
        return;
    }

    appendCopilotMessage('user', `${action.charAt(0).toUpperCase() + action.slice(1)} analysis`);

    // Show typing
    const container = document.getElementById('copilotMessages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'copilot-msg ai copilot-typing-msg';
    typingDiv.innerHTML = '<div class="copilot-msg-avatar"><i data-lucide="sparkles" style="width:14px;height:14px"></i></div><div class="copilot-msg-bubble"><div class="copilot-typing"><span></span><span></span><span></span></div></div>';
    container.appendChild(typingDiv);
    container.scrollTop = container.scrollHeight;

    // Update the AI bar text
    const barText = document.getElementById(`${view}AIText`);
    if (barText) barText.textContent = `AI running ${action} analysis...`;

    try {
        const resp = await fetch('/api/ai/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                data: prompt.data(),
                question: prompt.question,
                system: 'You are an expert Junos network AI partner embedded in a NOC. Give specific, actionable analysis. Use bullet points. Be thorough but concise.'
            })
        });
        const data = await resp.json();
        typingDiv.remove();
        appendCopilotMessage('ai', data.analysis || data.error || 'No analysis available');

        if (barText) barText.textContent = `${action} analysis complete`;
        setTimeout(() => {
            if (barText) barText.textContent = `AI is watching ${view}`;
        }, 5000);

    } catch (e) {
        typingDiv.remove();
        appendCopilotMessage('ai', `AI analysis failed: ${e.message}`);
        if (barText) barText.textContent = `AI is watching ${view}`;
    }
}

// ─── Hook into existing actions for audit trail ───
const _originalLoadConfig = typeof loadConfig === 'function' ? loadConfig : null;

// ═══════════════════════════════════════
//  WebSocket
// ═══════════════════════════════════════
function initSocket() {
    try {
        state.socket = io({ transports: ['polling', 'websocket'], reconnectionAttempts: 3 });
        state.socket.on('connect', () => {
            const statusEl = document.getElementById('headerStatus') || document.getElementById('connectionStatus');
            if (statusEl) {
                const dot = statusEl.querySelector('.status-dot');
                if (dot) dot.classList.add('online');
                const txt = statusEl.querySelector('.status-label') || statusEl.querySelector('.status-text');
                if (txt) txt.textContent = 'Live';
            }
        });
        state.socket.on('disconnect', () => {
            const statusEl = document.getElementById('headerStatus') || document.getElementById('connectionStatus');
            if (statusEl) {
                const dot = statusEl.querySelector('.status-dot');
                if (dot) dot.classList.remove('online');
                const txt = statusEl.querySelector('.status-label') || statusEl.querySelector('.status-text');
                if (txt) txt.textContent = 'Offline';
            }
        });
        state.socket.on('topology_data', data => {
            state.topology = data;
            renderDashboard();
        });
        state.socket.on('path_result', data => {
            renderPathResult(data);
        });
        state.socket.on('chat_response', data => {
            appendChatMessage('ai', data.response || data.error);
        });

        // ── Brain Investigation WebSocket Events ──
        state.socket.on('brain_progress', data => {
            handleBrainProgress(data);
            // Handle remediation events
            if (data.event === 'remediation_start') {
                logAuditAction('deploy', `Remediation #${data.id} executing on ${data.router}...`);
            } else if (data.event === 'remediation_complete') {
                logAuditAction('validate', `Remediation #${data.id} completed on ${data.router}`);
            } else if (data.event === 'remediation_error') {
                logAuditAction('warning', `Remediation #${data.id} failed: ${data.error}`);
            }
        });
        state.socket.on('brain_log', data => {
            handleBrainLog(data);
        });
        state.socket.on('ai_thinking', data => {
            handleAiThinking(data);
        });
    } catch (e) {
        console.warn('WebSocket unavailable, using REST only');
    }
}

// ═══════════════════════════════════════
//  Data Loading
// ═══════════════════════════════════════
async function api(endpoint) {
    const res = await fetch('/api/' + endpoint);
    return res.json();
}

async function loadAll() {
    try {
        const [topo, devices, stats] = await Promise.all([
            api('topology'),
            api('devices'),
            api('network-stats')
        ]);
        state.topology = topo;
        state.devices = devices;
        state.stats = stats;
        renderDashboard();
        populatePathSelectors();
        renderConfigList();
        renderDevicesGrid();
        // Load secondary data
        loadTemplates();
        loadLogFiles();
        loadScheduledTasks();
        loadWorkflows();
        checkHealth();
        // Check if first-run bootstrap needed
        checkBootstrap();
        // Poll live MCP device status (non-blocking)
        pollLiveDeviceStatus();
    } catch (e) {
        console.error('Failed to load data:', e);
        // Even if main load fails, still check bootstrap — might help user fix the issue
        checkBootstrap();
    }
}

// ─── Live MCP Device Polling ───
async function pollLiveDeviceStatus() {
    try {
        const resp = await fetch('/api/mcp/live-devices');
        const data = await resp.json();
        state.liveDeviceData = data;
        updateDataSourceIndicator(data);
        updateDeviceStatuses(data);
    } catch (e) {
        console.warn('Live device poll failed:', e);
        updateDataSourceIndicator({ data_source: 'offline', mcp_connected: false });
    }
}

function updateDataSourceIndicator(data) {
    const statusEl = document.getElementById('connectionStatus');
    if (!statusEl) return;
    const dot = statusEl.querySelector('.status-dot');
    const txt = statusEl.querySelector('.status-text');
    const liveCount = (data.live_devices || []).length;
    const downCount = (data.unreachable || []).length;

    if (data.data_source === 'live' && data.mcp_connected && liveCount > 0) {
        if (dot) { dot.classList.add('online'); dot.classList.remove('config-only'); }
        if (txt) txt.textContent = 'Live';
        statusEl.title = `MCP Connected — ${liveCount} reachable, ${downCount} unreachable`;
    } else if (data.data_source === 'live' && data.mcp_connected && downCount > 0) {
        if (dot) { dot.classList.remove('online'); dot.classList.add('config-only'); }
        if (txt) txt.textContent = 'MCP Up';
        statusEl.title = `MCP server connected — ${downCount} devices unreachable`;
    } else {
        if (dot) { dot.classList.remove('online'); dot.classList.add('config-only'); }
        if (txt) txt.textContent = 'Offline';
        statusEl.title = 'MCP unreachable — showing golden config data only';
    }

    // Update the dashboard subtitle to show data source
    const subtitleEl = document.querySelector('#view-dashboard .view-subtitle');
    if (subtitleEl) {
        if (data.data_source === 'live' && liveCount > 0) {
            subtitleEl.innerHTML = `<span class="data-source-badge live"><i data-lucide="radio" style="width:12px;height:12px;display:inline-block;vertical-align:middle"></i> Live MCP</span> ${liveCount} devices reachable` +
                (downCount > 0 ? ` <span class="data-source-badge offline">${downCount} unreachable</span>` : '');
        } else if (data.data_source === 'live' && downCount > 0) {
            subtitleEl.innerHTML = `<span class="data-source-badge offline"><i data-lucide="server" style="width:12px;height:12px;display:inline-block;vertical-align:middle"></i> MCP Connected</span> ${downCount} devices unreachable — showing topology from golden configs`;
        } else {
            subtitleEl.innerHTML = `<span class="data-source-badge offline"><i data-lucide="hard-drive" style="width:12px;height:12px;display:inline-block;vertical-align:middle"></i> Offline</span> Showing golden config data — MCP not connected`;
        }
        if (typeof lucide !== 'undefined') lucide.createIcons();
    }
}

function updateDeviceStatuses(data) {
    if (!state.topology || !state.topology.nodes) return;
    // Merge live status into topology nodes
    const liveMap = {};
    for (const d of (data.live_devices || [])) liveMap[d.name] = d.status;
    for (const d of (data.unreachable || [])) liveMap[d.name] = 'unreachable';
    state.topology.nodes.forEach(n => {
        if (liveMap[n.id]) n.live_status = liveMap[n.id];
        else n.live_status = data.data_source === 'live' ? 'unknown' : 'config-only';
    });
    // Re-render device table with live statuses
    renderDeviceTable(state.topology.nodes);
}

// ─── Health Check ───
async function checkHealth() {
    try {
        const h = await api('health');
        const statusEl = document.getElementById('connectionStatus');
        if (statusEl) {
            const dot = statusEl.querySelector('.status-dot');
            const txt = statusEl.querySelector('.status-text');
            if (h.mcp === 'connected') {
                if (dot) dot.classList.add('online');
                if (txt) txt.textContent = 'Live';
            } else {
                if (dot) dot.classList.remove('online');
                if (txt) txt.textContent = 'Offline';
            }
        }
    } catch (e) { /* ignore */ }
}

// ═══════════════════════════════════════
//  Dashboard
// ═══════════════════════════════════════
function renderDashboard() {
    if (!state.topology) return;
    const t = state.topology;
    const s = state.stats || {};

    // Stats cards
    setText('totalDevices', t.nodes ? t.nodes.length : 0);
    setText('totalLinks', t.links ? t.links.length : 0);

    const bgpCount = t.nodes ? t.nodes.reduce((sum, n) => sum + (n.bgp_neighbors || []).length, 0) : 0;
    setText('totalBGP', bgpCount);

    const rs = s.redundancy_score;
    const rsEl = document.getElementById('redundancyScore');
    if (rsEl) rsEl.textContent = rs !== undefined ? (rs * 100).toFixed(0) + '%' : '—';

    setText('graphDiameter', s.diameter || 0);
    setText('spofCount', s.single_points_of_failure ? s.single_points_of_failure.length : 0);

    // Role donut chart
    renderRoleChart(t.nodes || []);
    // Protocol bars
    renderProtocolBars(t.nodes || []);
    // Mini topology
    renderMiniTopology(t);
    // Device table
    renderDeviceTable(t.nodes || []);
}

function setText(id, val) {
    const el = document.getElementById(id);
    if (!el) return;
    // Animate numeric values
    const numVal = parseFloat(val);
    if (!isNaN(numVal) && typeof val !== 'string') {
        animateValue(el, numVal);
    } else {
        el.textContent = val;
    }
}

function animateValue(el, target) {
    const isPercent = String(target).includes('%');
    const numTarget = parseFloat(target);
    const start = parseFloat(el.textContent) || 0;
    const duration = 800;
    const startTime = performance.now();
    
    function update(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
        const current = start + (numTarget - start) * eased;
        
        if (Number.isInteger(numTarget)) {
            el.textContent = Math.round(current);
        } else {
            el.textContent = current.toFixed(numTarget < 10 ? 1 : 0);
        }
        if (isPercent) el.textContent += '%';
        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            // Pop effect on completion
            el.classList.add('updated');
            setTimeout(() => el.classList.remove('updated'), 400);
        }
    }
    requestAnimationFrame(update);
}

// ─── Donut Chart (SVG) ───
function renderRoleChart(nodes) {
    const container = document.getElementById('roleChart');
    if (!container) return;
    const roles = {};
    nodes.forEach(n => { roles[n.role || 'unknown'] = (roles[n.role || 'unknown'] || 0) + 1; });

    const colors = { PE: '#01A982', P: '#0D5FFF', 'Route Reflector': '#7630EA', unknown: '#64748B' };
    const data = Object.entries(roles);
    const total = nodes.length;
    const size = 160;
    const r = size / 2 - 10;
    const ir = r - 22;

    let svg = `<svg viewBox="0 0 ${size} ${size}" width="${size}" height="${size}">`;
    let angle = -Math.PI / 2;

    data.forEach(([role, count]) => {
        const pct = count / total;
        const a1 = angle;
        const a2 = angle + pct * 2 * Math.PI;
        const large = pct > 0.5 ? 1 : 0;
        const x1 = size/2 + r * Math.cos(a1);
        const y1 = size/2 + r * Math.sin(a1);
        const x2 = size/2 + r * Math.cos(a2);
        const y2 = size/2 + r * Math.sin(a2);
        const ix1 = size/2 + ir * Math.cos(a1);
        const iy1 = size/2 + ir * Math.sin(a1);
        const ix2 = size/2 + ir * Math.cos(a2);
        const iy2 = size/2 + ir * Math.sin(a2);

        svg += `<path d="M${x1},${y1} A${r},${r} 0 ${large} 1 ${x2},${y2} L${ix2},${iy2} A${ir},${ir} 0 ${large} 0 ${ix1},${iy1} Z" fill="${colors[role] || '#64748B'}" opacity="0.85"/>`;
        angle = a2;
    });

    svg += `<text x="${size/2}" y="${size/2 - 6}" text-anchor="middle" fill="var(--text-primary)" font-size="24" font-weight="800">${total}</text>`;
    svg += `<text x="${size/2}" y="${size/2 + 14}" text-anchor="middle" fill="var(--text-tertiary)" font-size="10" font-weight="500">DEVICES</text>`;
    svg += '</svg>';

    // Legend below
    let legend = '<div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:16px;justify-content:center">';
    data.forEach(([role, count]) => {
        legend += `<div style="display:flex;align-items:center;gap:6px;font-size:0.78rem;color:var(--text-secondary)"><span style="width:10px;height:10px;border-radius:50%;background:${colors[role]||'#64748B'}"></span>${role} (${count})</div>`;
    });
    legend += '</div>';

    container.innerHTML = svg + legend;
}

// ─── Protocol bars ───
function renderProtocolBars(nodes) {
    const container = document.getElementById('protocolBars');
    if (!container) return;
    const total = nodes.length;
    const counts = { 'IS-IS L2': 0, 'iBGP': 0, 'LDP': 0, 'MPLS': 0, 'VPN': 0 };

    nodes.forEach(n => {
        if (n.isis_interfaces && n.isis_interfaces.length > 0) counts['IS-IS L2']++;
        if (n.bgp_neighbors && n.bgp_neighbors.length > 0) counts['iBGP']++;
        if (n.ldp) counts['LDP']++;
        if (n.mpls) counts['MPLS']++;
        if (n.vpn) counts['VPN']++;
    });

    const colors = { 'IS-IS L2': '#01A982', 'iBGP': '#7630EA', 'LDP': '#0D5FFF', 'MPLS': '#00E8CF', 'VPN': '#FF8300' };

    container.innerHTML = Object.entries(counts).map(([proto, count]) => {
        const pct = total > 0 ? (count / total * 100) : 0;
        return `<div class="proto-bar">
            <div class="proto-bar-header"><span>${proto}</span><span style="color:var(--text-tertiary)">${count}/${total}</span></div>
            <div class="proto-bar-track"><div class="proto-bar-fill" style="width:${pct}%;background:${colors[proto]}"></div></div>
        </div>`;
    }).join('');
}

// ─── Device Table ───
function renderDeviceTable(nodes) {
    const tbody = document.getElementById('deviceTableBody');
    if (!tbody) return;
    tbody.innerHTML = nodes.map(n => {
        const roleClass = n.role === 'PE' ? 'badge-pe' : (n.role === 'Route Reflector' ? 'badge-rr' : 'badge-p');
        const liveStatus = n.live_status || 'config-only';
        const statusClass = liveStatus === 'live' ? 'badge-online' : (liveStatus === 'unreachable' ? 'badge-offline' : 'badge-config');
        const statusLabel = liveStatus === 'live' ? 'Live' : (liveStatus === 'unreachable' ? 'Down' : 'Config');
        return `<tr>
            <td><strong>${n.id}</strong></td>
            <td><span class="badge ${roleClass}">${n.role || 'P'}</span></td>
            <td style="font-family:var(--font-mono);font-size:0.8rem">${n.loopback || '—'}</td>
            <td>${(n.interfaces || []).length}</td>
            <td><span class="badge ${n.isis_interfaces && n.isis_interfaces.length ? 'badge-yes' : 'badge-no'}">${n.isis_interfaces ? n.isis_interfaces.length : 0}</span></td>
            <td><span class="badge ${n.bgp_neighbors && n.bgp_neighbors.length ? 'badge-yes' : 'badge-no'}">${n.bgp_neighbors ? n.bgp_neighbors.length : 0}</span></td>
            <td><span class="badge ${n.ldp ? 'badge-yes' : 'badge-no'}">${n.ldp ? 'Yes' : '—'}</span></td>
            <td><span class="badge ${statusClass}">${statusLabel}</span></td>
        </tr>`;
    }).join('');
}

function filterDeviceTable() {
    const q = document.getElementById('deviceFilter').value.toLowerCase();
    const rows = document.querySelectorAll('#deviceTableBody tr');
    rows.forEach(r => {
        r.style.display = r.textContent.toLowerCase().includes(q) ? '' : 'none';
    });
}

// ═══════════════════════════════════════
//  Topology Visualization (D3.js)
// ═══════════════════════════════════════
function renderTopology() {
    if (!state.topology) return;
    const svg = d3.select('#topologySVG');
    svg.selectAll('*').remove();
    const container = svg.node().parentElement;
    const width = container.clientWidth;
    const height = container.clientHeight;
    svg.attr('viewBox', `0 0 ${width} ${height}`);

    const nodes = state.topology.nodes.map(d => ({ ...d }));
    const links = buildLinks(state.topology);

    // Zoom
    const g = svg.append('g');
    const zoom = d3.zoom().scaleExtent([0.3, 4]).on('zoom', e => g.attr('transform', e.transform));
    svg.call(zoom);

    // Arrow marker
    svg.append('defs').append('marker')
        .attr('id', 'arrowhead').attr('viewBox', '0 -5 10 10')
        .attr('refX', 30).attr('refY', 0).attr('markerWidth', 6).attr('markerHeight', 6)
        .attr('orient', 'auto')
        .append('path').attr('d', 'M0,-5L10,0L0,5').attr('fill', 'var(--link-bgp)');

    // Links
    const showBGP = document.getElementById('showBGP')?.checked;
    const showISIS = document.getElementById('showISIS')?.checked;

    const linkG = g.append('g').attr('class', 'links');

    if (showISIS !== false) {
        linkG.selectAll('.topo-link-physical')
            .data(links.filter(l => l.type === 'physical'))
            .join('line')
            .attr('class', 'topo-link topo-link-physical')
            .attr('stroke-width', l => Math.max(1.5, 4 - (l.metric || 10) / 50));
    }

    if (showBGP) {
        linkG.selectAll('.topo-link-bgp')
            .data(links.filter(l => l.type === 'bgp'))
            .join('line')
            .attr('class', 'topo-link topo-link-bgp')
            .attr('marker-end', 'url(#arrowhead)');
    }

    // Nodes
    const nodeG = g.selectAll('.topo-node')
        .data(nodes)
        .join('g')
        .attr('class', 'topo-node')
        .call(d3.drag()
            .on('start', dragStarted)
            .on('drag', dragged)
            .on('end', dragEnded)
        )
        .on('click', (e, d) => showNodeDetail(d));

    const nodeColor = d => d.role === 'PE' ? '#01A982' : (d.role === 'Route Reflector' ? '#7630EA' : '#0D5FFF');

    // Outer glow
    nodeG.append('circle')
        .attr('r', 24)
        .attr('fill', d => nodeColor(d))
        .attr('opacity', 0.08);

    // Main circle
    nodeG.append('circle')
        .attr('r', 18)
        .attr('fill', d => nodeColor(d))
        .attr('opacity', 0.2)
        .attr('stroke', d => nodeColor(d))
        .attr('stroke-width', 2);

    // Inner circle
    nodeG.append('circle')
        .attr('r', 10)
        .attr('fill', d => nodeColor(d))
        .attr('opacity', 0.6);

    // RR ring
    nodeG.filter(d => d.role === 'Route Reflector')
        .append('circle')
        .attr('r', 26)
        .attr('class', 'rr-ring')
        .style('transform-origin', '0 0');

    // VPN badge
    nodeG.filter(d => d.vpn)
        .append('text')
        .attr('class', 'vpn-badge')
        .attr('y', -26)
        .text('VPN');

    // Labels
    if (document.getElementById('showLabels')?.checked !== false) {
        nodeG.append('text')
            .attr('class', 'node-label')
            .attr('y', 1)
            .text(d => d.id);

        nodeG.append('text')
            .attr('class', 'node-loopback')
            .attr('y', 30)
            .text(d => d.loopback || '');
    }

    // Simulation
    const sim = d3.forceSimulation(nodes)
        .force('link', d3.forceLink(links).id(d => d.id).distance(l => l.type === 'bgp' ? 200 : 120))
        .force('charge', d3.forceManyBody().strength(-500))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('collision', d3.forceCollide().radius(40))
        .on('tick', () => {
            linkG.selectAll('line')
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);
            nodeG.attr('transform', d => `translate(${d.x},${d.y})`);
        });

    state.topoSimulation = sim;

    // Tooltip
    let tooltip = document.querySelector('.topo-tooltip');
    if (!tooltip) {
        tooltip = document.createElement('div');
        tooltip.className = 'topo-tooltip';
        document.body.appendChild(tooltip);
    }

    nodeG.on('mouseenter', (e, d) => {
        tooltip.innerHTML = `<strong>${d.id}</strong> · ${d.role || 'P'}<br>Loopback: ${d.loopback || '—'}`;
        tooltip.style.display = 'block';
    })
    .on('mousemove', e => {
        tooltip.style.left = (e.pageX + 14) + 'px';
        tooltip.style.top = (e.pageY - 10) + 'px';
    })
    .on('mouseleave', () => { tooltip.style.display = 'none'; });

    function dragStarted(e, d) { if (!e.active) sim.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; }
    function dragged(e, d) { d.fx = e.x; d.fy = e.y; }
    function dragEnded(e, d) { if (!e.active) sim.alphaTarget(0); d.fx = null; d.fy = null; }
}

function buildLinks(topo) {
    const links = [];
    const nodeIds = new Set((topo.nodes || []).map(n => n.id));

    // Physical links from topology
    if (topo.links) {
        topo.links.forEach(l => {
            if (nodeIds.has(l.source || l.source?.id) && nodeIds.has(l.target || l.target?.id)) {
                links.push({ source: l.source, target: l.target, type: 'physical', metric: l.metric || 10, interface: l.interface });
            }
        });
    }

    // BGP links
    if (topo.nodes) {
        topo.nodes.forEach(n => {
            (n.bgp_neighbors || []).forEach(nbr => {
                const targetNode = topo.nodes.find(t => t.loopback === nbr);
                if (targetNode && !links.find(l => l.type === 'bgp' && ((l.source === n.id && l.target === targetNode.id) || (l.source === targetNode.id && l.target === n.id)))) {
                    links.push({ source: n.id, target: targetNode.id, type: 'bgp' });
                }
            });
        });
    }

    return links;
}

function updateTopoLayers() {
    if (state.currentView === 'topology') renderTopology();
}

function changeTopoLayout(layout) {
    if (!state.topoSimulation || !state.topology) return;
    const svg = document.getElementById('topologySVG');
    const w = svg.clientWidth;
    const h = svg.clientHeight;
    const nodes = state.topology.nodes;

    if (layout === 'circular') {
        nodes.forEach((n, i) => {
            const angle = (2 * Math.PI * i) / nodes.length;
            n.fx = w / 2 + Math.cos(angle) * Math.min(w, h) * 0.35;
            n.fy = h / 2 + Math.sin(angle) * Math.min(w, h) * 0.35;
        });
        state.topoSimulation.alpha(0.3).restart();
        setTimeout(() => nodes.forEach(n => { n.fx = null; n.fy = null; }), 2000);
    } else if (layout === 'hierarchical') {
        const levels = { PE: 2, P: 1, 'Route Reflector': 0 };
        const groups = {};
        nodes.forEach(n => {
            const lv = levels[n.role] ?? 1;
            if (!groups[lv]) groups[lv] = [];
            groups[lv].push(n);
        });
        Object.entries(groups).forEach(([lv, group]) => {
            group.forEach((n, i) => {
                n.fx = w * (i + 1) / (group.length + 1);
                n.fy = h * (Number(lv) + 1) / 4;
            });
        });
        state.topoSimulation.alpha(0.3).restart();
        setTimeout(() => nodes.forEach(n => { n.fx = null; n.fy = null; }), 3000);
    } else if (layout === 'radial') {
        const rr = nodes.filter(n => n.role === 'Route Reflector');
        const pe = nodes.filter(n => n.role === 'PE');
        const p = nodes.filter(n => n.role === 'P' && n.role !== 'Route Reflector');
        const cx = w / 2, cy = h / 2;

        rr.forEach((n, i) => {
            const a = (2 * Math.PI * i) / Math.max(rr.length, 1);
            n.fx = cx + Math.cos(a) * 60; n.fy = cy + Math.sin(a) * 60;
        });
        p.forEach((n, i) => {
            const a = (2 * Math.PI * i) / Math.max(p.length, 1);
            n.fx = cx + Math.cos(a) * 160; n.fy = cy + Math.sin(a) * 160;
        });
        pe.forEach((n, i) => {
            const a = (2 * Math.PI * i) / Math.max(pe.length, 1);
            n.fx = cx + Math.cos(a) * 260; n.fy = cy + Math.sin(a) * 260;
        });
        state.topoSimulation.alpha(0.3).restart();
        setTimeout(() => nodes.forEach(n => { n.fx = null; n.fy = null; }), 3000);
    } else {
        nodes.forEach(n => { n.fx = null; n.fy = null; });
        state.topoSimulation.alpha(1).restart();
    }
}

function resetTopology() {
    if (state.topology) renderTopology();
}

// ─── Mini Topology for Dashboard ───
function renderMiniTopology(topo) {
    const container = document.getElementById('miniTopology');
    if (!container || !topo || !topo.nodes) return;
    container.innerHTML = '';

    const svgEl = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svgEl.setAttribute('width', '100%');
    svgEl.setAttribute('height', '100%');
    container.appendChild(svgEl);

    const svg = d3.select(svgEl);
    const width = container.clientWidth || 600;
    const height = container.clientHeight || 340;
    svg.attr('viewBox', `0 0 ${width} ${height}`);

    const nodes = topo.nodes.map(d => ({ ...d }));
    const links = buildLinks(topo);

    const g = svg.append('g');

    const linkEl = g.selectAll('line')
        .data(links.filter(l => l.type === 'physical'))
        .join('line')
        .attr('stroke', 'var(--link-physical)')
        .attr('stroke-width', 1.5);

    const nodeColor = d => d.role === 'PE' ? '#01A982' : (d.role === 'Route Reflector' ? '#7630EA' : '#0D5FFF');

    const nodeEl = g.selectAll('g')
        .data(nodes)
        .join('g');

    nodeEl.append('circle').attr('r', 12).attr('fill', d => nodeColor(d)).attr('opacity', 0.15);
    nodeEl.append('circle').attr('r', 8).attr('fill', d => nodeColor(d)).attr('opacity', 0.5).attr('stroke', d => nodeColor(d)).attr('stroke-width', 1.5);

    nodeEl.append('text')
        .attr('text-anchor', 'middle')
        .attr('dominant-baseline', 'central')
        .attr('font-size', '8')
        .attr('font-weight', '600')
        .attr('fill', 'var(--text-primary)')
        .text(d => d.id);

    const sim = d3.forceSimulation(nodes)
        .force('link', d3.forceLink(links.filter(l => l.type === 'physical')).id(d => d.id).distance(70))
        .force('charge', d3.forceManyBody().strength(-250))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('collision', d3.forceCollide().radius(25))
        .on('tick', () => {
            linkEl.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
                  .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
            nodeEl.attr('transform', d => `translate(${d.x},${d.y})`);
        });

    state.miniSimulation = sim;
}

// ─── Node Detail Panel ───
function showNodeDetail(node) {
    const panel = document.getElementById('nodeDetailPanel');
    const content = document.getElementById('nodeDetailContent');
    if (!panel || !content) return;

    const roleColor = node.role === 'PE' ? 'var(--hpe-green)' : (node.role === 'Route Reflector' ? 'var(--hpe-purple)' : 'var(--hpe-blue)');

    let html = `<div class="detail-title">${node.id}</div>`;
    html += `<div class="detail-role" style="color:${roleColor}">${node.role || 'P Router'}</div>`;

    html += `<div class="detail-section"><h4>Identity</h4><div class="detail-grid">
        <div class="detail-item"><span>Loopback</span><span>${node.loopback || '—'}</span></div>
        <div class="detail-item"><span>Interfaces</span><span>${(node.interfaces || []).length}</span></div>
    </div></div>`;

    if (node.isis_interfaces && node.isis_interfaces.length > 0) {
        html += `<div class="detail-section"><h4>IS-IS Interfaces</h4><ul class="detail-list">`;
        node.isis_interfaces.forEach(i => { html += `<li>${i}</li>`; });
        html += '</ul></div>';
    }

    if (node.bgp_neighbors && node.bgp_neighbors.length > 0) {
        html += `<div class="detail-section"><h4>BGP Neighbors</h4><ul class="detail-list">`;
        node.bgp_neighbors.forEach(n => { html += `<li>${n}</li>`; });
        html += '</ul></div>';
    }

    html += `<div class="detail-section"><h4>Protocols</h4><div class="detail-grid">
        <div class="detail-item"><span>LDP</span><span>${node.ldp ? 'Yes' : '—'}</span></div>
        <div class="detail-item"><span>MPLS</span><span>${node.mpls ? 'Yes' : '—'}</span></div>
        <div class="detail-item"><span>VPN</span><span>${node.vpn || '—'}</span></div>
        <div class="detail-item"><span>RSVP</span><span>${node.rsvp ? 'Yes' : '—'}</span></div>
    </div></div>`;

    html += `<div style="margin-top:16px;display:flex;gap:8px">
        <button class="btn-outline" onclick="loadConfig('${node.id}');switchView('configs')">View Config</button>
    </div>`;

    content.innerHTML = html;
    panel.classList.add('visible');
}

function closeNodeDetail() {
    document.getElementById('nodeDetailPanel')?.classList.remove('visible');
}

// ═══════════════════════════════════════
//  Devices Grid
// ═══════════════════════════════════════
function renderDevicesGrid() {
    const grid = document.getElementById('devicesGrid');
    if (!grid || !state.topology) return;

    grid.innerHTML = (state.topology.nodes || []).map(n => {
        const roleClass = n.role === 'PE' ? 'role-pe' : (n.role === 'Route Reflector' ? 'role-rr' : 'role-p');
        const roleStyle = n.role === 'PE' ? 'badge-pe' : (n.role === 'Route Reflector' ? 'badge-rr' : 'badge-p');
        return `<div class="device-card ${roleClass}">
            <div class="device-card-header">
                <span class="device-name">${n.id}</span>
                <span class="badge ${roleStyle}">${n.role || 'P'}</span>
            </div>
            <div class="device-meta">
                <div class="device-meta-item"><span class="label">Loopback</span><span class="value">${n.loopback || '—'}</span></div>
                <div class="device-meta-item"><span class="label">Interfaces</span><span class="value">${(n.interfaces || []).length}</span></div>
                <div class="device-meta-item"><span class="label">IS-IS</span><span class="value">${n.isis_interfaces ? n.isis_interfaces.length + ' intf' : '—'}</span></div>
                <div class="device-meta-item"><span class="label">BGP Peers</span><span class="value">${n.bgp_neighbors ? n.bgp_neighbors.length : 0}</span></div>
            </div>
            <div style="display:flex;gap:4px;flex-wrap:wrap">
                ${n.ldp ? '<span class="badge badge-yes">LDP</span>' : ''}
                ${n.mpls ? '<span class="badge badge-yes">MPLS</span>' : ''}
                ${n.vpn ? '<span class="badge badge-pe">VPN</span>' : ''}
                ${n.rsvp ? '<span class="badge badge-yes">RSVP</span>' : ''}
            </div>
            <div class="device-actions">
                <button class="btn-outline" onclick="loadConfig('${n.id}');switchView('configs')">Config</button>
            </div>
        </div>`;
    }).join('');
}

// ═══════════════════════════════════════
//  Config Management
// ═══════════════════════════════════════
function renderConfigList() {
    const list = document.getElementById('configList');
    if (!list || !state.topology) return;

    list.innerHTML = (state.topology.nodes || []).map(n =>
        `<div class="config-item" data-router="${n.id}" onclick="loadConfig('${n.id}')">${n.id}</div>`
    ).join('');
}

async function loadConfig(routerName) {
    state.lastConfigViewed = routerName;
    logAuditAction('config_view', `Viewed config: ${routerName}`);
    // highlight in list
    document.querySelectorAll('.config-item').forEach(i => i.classList.remove('active'));
    const item = document.querySelector(`.config-item[data-router="${routerName}"]`);
    if (item) item.classList.add('active');

    const viewer = document.getElementById('configViewer');
    viewer.innerHTML = '<div class="loading" style="margin:20px;height:400px"></div>';

    try {
        const data = await api(`golden-configs/${routerName}`);
        if (data.error) {
            viewer.innerHTML = `<div class="empty-state"><p>${data.error}</p></div>`;
        } else {
            const config = data.config || '';
            viewer.innerHTML = `<div style="padding:12px 20px;border-bottom:1px solid var(--border-subtle);display:flex;justify-content:space-between;align-items:center">
                <strong>${routerName}.conf</strong>
                <span style="font-size:0.75rem;color:var(--text-tertiary)">${config.split('\n').length} lines</span>
            </div><pre>${escapeHtml(config)}</pre>`;
        }
    } catch (e) {
        viewer.innerHTML = `<div class="empty-state"><p>Failed to load config</p></div>`;
    }
}

async function searchConfigs() {
    const q = document.getElementById('configSearchInput').value;
    if (!q) return;
    const regex = document.getElementById('regexToggle')?.checked;

    const resultsEl = document.getElementById('searchResults');
    const body = document.getElementById('searchResultsBody');
    resultsEl.style.display = 'block';
    body.innerHTML = '<div class="loading" style="height:60px;margin:12px"></div>';

    try {
        const data = await api(`config-search?q=${encodeURIComponent(q)}&regex=${regex}`);
        if (data.results && data.results.length > 0) {
            body.innerHTML = data.results.map(r =>
                `<div class="search-match">
                    <div class="search-match-header">
                        <span class="search-match-router">${r.router}</span>
                        <span class="search-match-line">Line ${r.line_number}</span>
                    </div>
                    <div class="search-match-context">${escapeHtml(r.line)}</div>
                </div>`
            ).join('');
        } else {
            body.innerHTML = '<div class="empty-state"><p>No matches found</p></div>';
        }
    } catch (e) {
        body.innerHTML = '<div class="empty-state"><p>Search failed</p></div>';
    }
}

// ═══════════════════════════════════════
//  PATH FINDER
// ═══════════════════════════════════════
function populatePathSelectors() {
    if (!state.topology || !state.topology.nodes) return;
    const sourceEl = document.getElementById('pathSource');
    const targetEl = document.getElementById('pathTarget');
    if (!sourceEl || !targetEl) return;

    const opts = state.topology.nodes.map(n => `<option value="${n.id}">${n.id} (${n.loopback || ''})</option>`).join('');
    sourceEl.innerHTML = opts;
    targetEl.innerHTML = opts;
    if (state.topology.nodes.length > 1) targetEl.selectedIndex = state.topology.nodes.length - 1;
}

async function findShortestPath() {
    const source = document.getElementById('pathSource')?.value;
    const target = document.getElementById('pathTarget')?.value;
    if (!source || !target) return;

    const results = document.getElementById('pathResults');
    results.innerHTML = '<div class="loading" style="height:80px;margin:12px"></div>';

    try {
        const data = await api(`shortest-path?source=${source}&target=${target}`);
        renderPathResult(data);
    } catch (e) {
        results.innerHTML = '<div class="empty-state"><p>Failed to find path</p></div>';
    }
}

function renderPathResult(data) {
    const results = document.getElementById('pathResults');
    if (!results) return;

    if (data.error) {
        results.innerHTML = `<div class="path-result-card"><p style="color:var(--hpe-rose)">${data.error}</p></div>`;
        return;
    }

    const path = data.path || [];
    const cost = data.total_cost || 0;

    let html = `<div class="path-result-card">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
            <h3>Shortest Path Found</h3>
            <span style="font-size:0.85rem;color:var(--text-tertiary)">Total IS-IS Cost: <strong style="color:var(--hpe-green)">${cost}</strong></span>
        </div>
        <div class="path-hops">`;

    path.forEach((hop, i) => {
        const cls = i === 0 ? 'source' : (i === path.length - 1 ? 'target' : '');
        html += `<div class="path-hop"><span class="path-node ${cls}">${hop}</span>`;
        if (i < path.length - 1) html += `<span class="path-arrow-small">→</span>`;
        html += '</div>';
    });

    html += `</div>
        <p style="font-size:0.8rem;color:var(--text-tertiary)">Path length: ${path.length} hops (${path.length - 1} links)</p>
    </div>`;

    results.innerHTML = html;
    renderPathTopology(path);
}

function renderPathTopology(highlightPath) {
    if (!state.topology) return;
    const svg = d3.select('#pathTopologySVG');
    svg.selectAll('*').remove();

    const container = svg.node().parentElement;
    const width = container.clientWidth;
    const height = container.clientHeight || 400;
    svg.attr('viewBox', `0 0 ${width} ${height}`);

    const nodes = state.topology.nodes.map(d => ({ ...d }));
    const links = buildLinks(state.topology).filter(l => l.type === 'physical');

    const g = svg.append('g');
    svg.call(d3.zoom().scaleExtent([0.3, 4]).on('zoom', e => g.attr('transform', e.transform)));

    const pathSet = new Set(highlightPath || []);
    const pathEdges = new Set();
    if (highlightPath) {
        for (let i = 0; i < highlightPath.length - 1; i++) {
            pathEdges.add(`${highlightPath[i]}-${highlightPath[i + 1]}`);
            pathEdges.add(`${highlightPath[i + 1]}-${highlightPath[i]}`);
        }
    }

    const linkEl = g.selectAll('line').data(links).join('line')
        .attr('class', d => {
            const src = typeof d.source === 'object' ? d.source.id : d.source;
            const tgt = typeof d.target === 'object' ? d.target.id : d.target;
            return pathEdges.has(`${src}-${tgt}`) ? 'topo-link topo-link-highlight' : 'topo-link topo-link-physical';
        });

    const nodeColor = d => {
        if (highlightPath && pathSet.has(d.id)) return '#01A982';
        return d.role === 'PE' ? '#01A982' : (d.role === 'Route Reflector' ? '#7630EA' : '#0D5FFF');
    };

    const nodeEl = g.selectAll('g.topo-node').data(nodes).join('g').attr('class', 'topo-node');
    nodeEl.append('circle').attr('r', d => pathSet.has(d.id) ? 16 : 12)
        .attr('fill', d => nodeColor(d))
        .attr('opacity', d => pathSet.has(d.id) ? 0.5 : 0.15)
        .attr('stroke', d => nodeColor(d))
        .attr('stroke-width', d => pathSet.has(d.id) ? 2.5 : 1.5);

    nodeEl.append('text')
        .attr('text-anchor', 'middle').attr('dominant-baseline', 'central')
        .attr('font-size', '10').attr('font-weight', '600').attr('fill', 'var(--text-primary)')
        .text(d => d.id);

    const sim = d3.forceSimulation(nodes)
        .force('link', d3.forceLink(links).id(d => d.id).distance(100))
        .force('charge', d3.forceManyBody().strength(-350))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('collision', d3.forceCollide().radius(30))
        .on('tick', () => {
            linkEl.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
                  .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
            nodeEl.attr('transform', d => `translate(${d.x},${d.y})`);
        });

    state.pathSimulation = sim;
}

// ═══════════════════════════════════════
//  AI Chat (Agentic — Brain + RAG + MCP)
// ═══════════════════════════════════════

// Build chain-of-thought steps array from API response metadata
function buildCotSteps(data) {
    const steps = [];
    const type = data.type || 'general';

    // Classify step — always present
    steps.push({ label: 'Classify', text: `Query classified as: ${type}` });

    if (type === 'knowledge') {
        steps.push({ label: 'Retrieve', text: `Searched RAG knowledge base — ${data.sources?.length || 0} sources found` });
        if (data.sources?.length) {
            const headings = data.sources.slice(0, 2).map(s => s.heading || s.source).filter(Boolean).join(', ');
            if (headings) steps.push({ label: 'Sources', text: headings });
        }
        steps.push({ label: 'Synthesize', text: 'Generated response grounded in knowledge base context' });
    } else if (type === 'investigation') {
        steps.push({ label: 'Investigate', text: 'Initiated 7-layer Brain Engine investigation' });
        if (data.layers_completed) {
            data.layers_completed.forEach(l => steps.push({ label: l.charAt(0).toUpperCase() + l.slice(1), text: `Layer ${l} analysis complete` }));
        } else {
            ['Perception', 'Analysis', 'Validation', 'Synthesis'].forEach(l =>
                steps.push({ label: l, text: `${l} layer processed` })
            );
        }
        if (data.devices_checked?.length) {
            steps.push({ label: 'MCP', text: `Queried ${data.devices_checked.length} device(s): ${data.devices_checked.slice(0, 3).join(', ')}` });
        }
        if (data.duration_ms) {
            steps.push({ label: 'Complete', text: `Investigation finished in ${(data.duration_ms / 1000).toFixed(1)}s` });
        }
    } else if (type === 'quick_status') {
        steps.push({ label: 'Status', text: 'Fetched live device status from MCP server' });
        steps.push({ label: 'Synthesize', text: 'Compiled status summary from topology data' });
    } else if (type === 'config') {
        steps.push({ label: 'Safety', text: 'Ran config change safety review' });
        if (data.requires_approval) steps.push({ label: 'Approval', text: 'Change requires explicit operator approval before deployment' });
        steps.push({ label: 'Synthesize', text: 'Generated configuration commands with rollback plan' });
    } else {
        steps.push({ label: 'Context', text: 'Loaded network topology and device context' });
        steps.push({ label: 'Synthesize', text: 'Generated response using network-aware reasoning' });
    }

    if (data.confidence !== undefined) {
        steps.push({ label: 'Confidence', text: `Response confidence: ${Math.round(data.confidence * 100)}%` });
    }

    return steps;
}

async function sendChat() {
    const input = document.getElementById('chatInput');
    const msg = input.value.trim();
    if (!msg) return;
    input.value = '';

    appendChatMessage('user', msg);
    state.chatHistory.push({ role: 'user', content: msg });
    showTypingIndicator();

    try {
        // Primary path: Agentic chat with Brain + RAG routing
        const resp = await fetch('/api/ai/chat-agentic', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg, history: state.chatHistory.slice(-10) })
        });

        removeTypingIndicator();

        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const data = await resp.json();

        if (data.error) {
            appendChatMessage('ai', `Error: ${data.error}`);
            return;
        }

        const response = data.response || 'No response';
        const responseType = data.type || 'general';

        // Build enriched response with metadata badges
        let enrichedHtml = response;
        let metaBadges = '';

        if (responseType === 'knowledge' && data.sources && data.sources.length > 0) {
            metaBadges += '<div class="chat-meta-badges">';
            metaBadges += '<span class="meta-badge rag"><i data-lucide="book-open" class="meta-icon"></i> RAG Knowledge</span>';
            for (const src of data.sources.slice(0, 3)) {
                if (src.heading) metaBadges += `<span class="meta-badge source">${src.heading}</span>`;
            }
            metaBadges += '</div>';
        } else if (responseType === 'investigation') {
            metaBadges += '<div class="chat-meta-badges">';
            metaBadges += '<span class="meta-badge brain"><i data-lucide="brain" class="meta-icon"></i> Brain Investigation</span>';
            if (data.devices_checked) {
                metaBadges += `<span class="meta-badge devices">${data.devices_checked.length} devices</span>`;
            }
            if (data.duration_ms) {
                metaBadges += `<span class="meta-badge info">⏱ ${(data.duration_ms/1000).toFixed(1)}s</span>`;
            }
            metaBadges += '</div>';

            // Tool Call Visualization Cards
            if (data.devices_checked && data.devices_checked.length > 0) {
                enrichedHtml = renderToolCallCards(data) + enrichedHtml;
            }
        } else if (responseType === 'quick_status') {
            metaBadges += '<div class="chat-meta-badges">';
            metaBadges += '<span class="meta-badge quick"><i data-lucide="zap" class="meta-icon"></i> Quick Status</span>';
            metaBadges += '</div>';
        } else if (responseType === 'config') {
            metaBadges += '<div class="chat-meta-badges">';
            metaBadges += '<span class="meta-badge config"><i data-lucide="settings" class="meta-icon"></i> Config Mode</span>';
            if (data.requires_approval) metaBadges += '<span class="meta-badge warning"><i data-lucide="alert-triangle" class="meta-icon"></i> Review Required</span>';
            metaBadges += '</div>';
        }

        appendChatMessage('ai', metaBadges + enrichedHtml, buildCotSteps(data), data.confidence);
        state.chatHistory.push({ role: 'assistant', content: response });
        state.lastQueryContext = { query: msg, type: responseType };

        // Fetch confidence score and append badge
        fetchConfidenceBadge(data);

    } catch (e) {
        removeTypingIndicator();
        // Fallback: try streaming endpoint
        try {
            const resp = await fetch('/api/ai/stream', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: msg, history: state.chatHistory.slice(-10) })
            });

            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);

            const { bubble, cursor } = startStreamingMessage();
            const reader = resp.body.getReader();
            const decoder = new TextDecoder();
            let accumulated = '';
            let buffer = '';

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');
                buffer = lines.pop();
                for (const line of lines) {
                    const trimmed = line.trim();
                    if (!trimmed.startsWith('data:')) continue;
                    const payload = trimmed.slice(5).trim();
                    if (!payload) continue;
                    try {
                        const parsed = JSON.parse(payload);
                        if (parsed.error) { accumulated += `\n[Error] ${parsed.error}`; break; }
                        if (parsed.done) break;
                        if (parsed.token) { accumulated += parsed.token; appendStreamToken(bubble, accumulated); }
                    } catch (_) {}
                }
            }

            finalizeStreamMessage(bubble, cursor, accumulated);
            state.chatHistory.push({ role: 'assistant', content: accumulated });

        } catch (_) {
            // Final fallback: non-streaming endpoint
            try {
                const resp2 = await fetch('/api/ai/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: msg, history: state.chatHistory.slice(-10) })
                });
                const data = await resp2.json();
                if (data.error && data.fallback) {
                    appendChatMessage('ai', generateLocalResponse(msg));
                } else if (data.error) {
                    appendChatMessage('ai', `Error: ${data.error}`);
                } else {
                    const response = data.response || 'No response';
                    appendChatMessage('ai', response);
                    state.chatHistory.push({ role: 'assistant', content: response });
                }
            } catch (__) {
                appendChatMessage('ai', generateLocalResponse(msg));
            }
        }
    }
}

function startStreamingMessage() {
    const container = document.getElementById('chatMessages');
    const welcome = container.querySelector('.chat-welcome');
    if (welcome) welcome.remove();

    const div = document.createElement('div');
    div.className = 'chat-message ai streaming';
    const bubble = document.createElement('div');
    bubble.className = 'msg-bubble';
    bubble.innerHTML = '<span class="stream-content"></span>';
    const cursor = document.createElement('span');
    cursor.className = 'streaming-cursor';
    cursor.textContent = '▎';
    bubble.appendChild(cursor);

    div.innerHTML = '<div class="msg-avatar"><i data-lucide="bot" style="width:18px;height:18px"></i></div>';
    div.appendChild(bubble);
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;

    return { bubble, cursor };
}

function appendStreamToken(bubble, accumulated) {
    const content = bubble.querySelector('.stream-content');
    if (content) {
        content.innerHTML = formatChatText(accumulated);
    }
    const container = document.getElementById('chatMessages');
    container.scrollTop = container.scrollHeight;
}

function finalizeStreamMessage(bubble, cursor, fullText) {
    if (cursor) cursor.remove();
    const content = bubble.querySelector('.stream-content');
    if (content) {
        content.innerHTML = formatChatText(fullText);
    }
    const msgDiv = bubble.closest('.chat-message');
    if (msgDiv) msgDiv.classList.remove('streaming');
}

function sendQuickChat(msg) {
    const input = document.getElementById('chatInput');
    input.value = msg;
    sendChat();
}

function appendChatMessage(role, text, cotSteps, confidence) {
    removeTypingIndicator();
    // Remove any active CoT panel ref
    const activeCot = document.getElementById('activeCotPanel');
    if (activeCot) activeCot.removeAttribute('id');

    const container = document.getElementById('chatMessages');
    const welcome = container.querySelector('.chat-welcome');
    if (welcome) welcome.remove();

    const div = document.createElement('div');
    div.className = `chat-message ${role}`;

    const avatar = role === 'ai'
        ? '<i data-lucide="bot" style="width:18px;height:18px"></i>'
        : '<i data-lucide="user" style="width:18px;height:18px"></i>';

    let cotHtml = '';
    if (role === 'ai' && cotSteps && cotSteps.length > 0) {
        const stepsHtml = cotSteps.map(s => `
            <div class="cot-step done">
                <svg class="cot-step-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                <span class="cot-step-label">${s.label}</span>
                <span class="cot-step-text">${s.text}</span>
            </div>`).join('');

        const confPct = Math.round((confidence || 0.85) * 100);
        const confBar = confidence ? `
            <div class="cot-confidence-bar">
                <div class="cot-confidence-label"><span>Confidence</span><span>${confPct}%</span></div>
                <div class="cot-confidence-track"><div class="cot-confidence-fill" style="width:${confPct}%"></div></div>
            </div>` : '';

        cotHtml = `
            <div class="cot-panel done open">
                <div class="cot-panel-header" onclick="this.closest('.cot-panel').classList.toggle('open')">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:13px;height:13px">
                        <path d="M12 2a10 10 0 100 20A10 10 0 0012 2z"/><path d="M12 6v6l4 2"/>
                    </svg>
                    <span>Reasoning trace (${cotSteps.length} steps)</span>
                    <svg class="cot-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                </div>
                <div class="cot-body">${stepsHtml}${confBar}</div>
            </div>`;
    }

    div.innerHTML = `<div class="msg-avatar">${avatar}</div><div class="msg-bubble">${cotHtml}${formatChatText(text)}</div>`;

    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
    if (typeof lucide !== 'undefined') lucide.createIcons();
}

function showTypingIndicator() {
    const container = document.getElementById('chatMessages');

    // Create typing message with embedded live CoT panel
    const div = document.createElement('div');
    div.className = 'chat-message ai typing';
    div.innerHTML = `
        <div class="msg-avatar"><i data-lucide="bot" style="width:18px;height:18px"></i></div>
        <div class="msg-bubble">
            <div class="cot-panel open thinking" id="activeCotPanel">
                <div class="cot-panel-header">
                    <span class="cot-pulse"></span>
                    <span>Reasoning in progress...</span>
                    <svg class="cot-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                </div>
                <div class="cot-body"></div>
            </div>
            <div class="typing-indicator"><span></span><span></span><span></span></div>
        </div>
    `;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
    if (typeof lucide !== 'undefined') lucide.createIcons();
}

function removeTypingIndicator() {
    document.querySelector('.chat-message.typing')?.remove();
}

function formatChatText(text) {
    return text
        .replace(/```([\s\S]*?)```/g, '<pre>$1</pre>')
        .replace(/`([^`]+)`/g, '<code style="background:var(--bg-code);padding:2px 6px;border-radius:4px;font-family:var(--font-mono);font-size:0.85em">$1</code>')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.+?)\*/g, '<em>$1</em>')
        .replace(/^### (.+)$/gm, '<h4>$1</h4>')
        .replace(/^## (.+)$/gm, '<h3>$1</h3>')
        .replace(/^# (.+)$/gm, '<h2>$1</h2>')
        .replace(/^- (.+)$/gm, '• $1')
        .replace(/^\d+\. (.+)$/gm, '<span style="color:var(--hpe-green)">→</span> $1')
        .replace(/\n/g, '<br>');
}

// ═══════════════════════════════════════
//  Brain Investigation Handlers
// ═══════════════════════════════════════
const _brainLayers = ['perception', 'execution', 'analysis', 'validation', 'synthesis'];

function handleBrainProgress(data) {
    const event = data.event;
    let progressBar = document.getElementById('brainProgressBar');

    if (event === 'investigation_start') {
        // Show brain progress bar in chat
        if (!progressBar) {
            const container = document.getElementById('chatMessages');
            const div = document.createElement('div');
            div.id = 'brainProgressWrapper';
            div.className = 'brain-progress-wrapper';
            div.innerHTML = `
                <div class="brain-progress-header">
                    <span class="brain-icon"><i data-lucide="brain" style="width:16px;height:16px"></i></span>
                    <span>Brain Investigation: <strong>${data.query || ''}</strong></span>
                    <span class="brain-mode">${data.mode || 'full'}</span>
                </div>
                <div class="brain-layers">
                    ${_brainLayers.map(l => `<div class="brain-layer" data-layer="${l}"><span class="layer-dot"></span>${l}</div>`).join('')}
                </div>
                <div class="brain-progress-bar" id="brainProgressBar"><div class="brain-progress-fill"></div></div>
                <div class="brain-log-mini" id="brainLogMini"></div>
            `;
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        }
    } else if (event === 'layer_change') {
        const layerIdx = _brainLayers.indexOf(data.layer);
        if (layerIdx >= 0) {
            const pct = ((layerIdx + 1) / _brainLayers.length) * 100;
            const fill = document.querySelector('.brain-progress-fill');
            if (fill) fill.style.width = pct + '%';
            // Highlight active layer
            document.querySelectorAll('.brain-layer').forEach((el, i) => {
                el.classList.toggle('active', i === layerIdx);
                el.classList.toggle('done', i < layerIdx);
            });
        }
    } else if (event === 'investigation_complete') {
        const fill = document.querySelector('.brain-progress-fill');
        if (fill) fill.style.width = '100%';
        document.querySelectorAll('.brain-layer').forEach(el => el.classList.add('done'));
        setTimeout(() => {
            const wrapper = document.getElementById('brainProgressWrapper');
            if (wrapper) wrapper.classList.add('complete');
        }, 500);
    } else if (event === 'investigation_error') {
        const wrapper = document.getElementById('brainProgressWrapper');
        if (wrapper) wrapper.classList.add('error');
    }
}

function handleBrainLog(data) {
    const logEl = document.getElementById('brainLogMini');
    if (!logEl) return;
    const line = document.createElement('div');
    line.className = 'brain-log-line';
    line.textContent = data.message || '';
    logEl.appendChild(line);
    // Keep only last 5 lines visible
    while (logEl.children.length > 5) logEl.removeChild(logEl.firstChild);
    logEl.scrollTop = logEl.scrollHeight;
}

function handleAiThinking(data) {
    const stage = data.stage;
    if (stage === 'complete') {
        // Mark active CoT step as done
        const cotPanel = document.querySelector('.cot-panel:not(.done)');
        if (cotPanel) {
            cotPanel.classList.add('done');
            cotPanel.classList.remove('thinking');
            const pulse = cotPanel.querySelector('.cot-pulse');
            if (pulse) pulse.style.display = 'none';
        }
        return;
    }

    // Map backend stages to human-readable CoT steps
    const STAGE_MAP = {
        'classifying':          { label: 'Classify',  text: 'Determining query intent and routing path...' },
        'rag_retrieval':        { label: 'Retrieve',  text: 'Searching RAG knowledge base for relevant context...' },
        'brain_investigation':  { label: 'Investigate', text: 'Running 7-layer Brain Engine investigation...' },
        'status_check':         { label: 'Status',    text: 'Fetching live device status from MCP...' },
        'config_safety_check':  { label: 'Safety',    text: 'Running safety review before config change...' },
        'general_response':     { label: 'Synthesize', text: 'Generating final response with network context...' },
        'topology_analysis':    { label: 'Topology',  text: 'Analyzing topology graph and path metrics...' },
        'protocol_analysis':    { label: 'Protocols', text: 'Running protocol specialist analysis (ISIS/BGP/LDP)...' },
        'specialist_analysis':  { label: 'Specialist', text: 'Running deep protocol specialist analysis...' },
        'confidence':           { label: 'Confidence', text: 'Computing confidence score and validation...' },
    };

    const info = STAGE_MAP[stage] || { label: stage, text: `Processing: ${stage}...` };

    // Update typing indicator with current stage text
    const typingBubble = document.querySelector('.chat-message.typing .msg-bubble');
    if (typingBubble) {
        typingBubble.innerHTML = `
            <div class="typing-indicator"><span></span><span></span><span></span></div>
            <div class="thinking-stage">${info.label}: ${info.text}</div>
        `;
    }

    // Update or create the CoT panel on the most recent AI message being built
    let cotPanel = document.getElementById('activeCotPanel');
    if (!cotPanel) return; // Panel created in sendChat before the request

    const stepEl = document.createElement('div');
    stepEl.className = 'cot-step active';
    stepEl.innerHTML = `
        <svg class="cot-step-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12M2 12h3M19 12h3M4.22 19.78l2.12-2.12M17.66 6.34l2.12-2.12"/>
        </svg>
        <span class="cot-step-label">${info.label}</span>
        <span class="cot-step-text">${info.text}</span>
    `;

    // Mark previously active step as done
    const prevActive = cotPanel.querySelectorAll('.cot-step.active');
    prevActive.forEach(el => {
        el.classList.remove('active');
        el.classList.add('done');
        el.querySelector('.cot-step-icon').innerHTML = `<polyline points="20 6 9 17 4 12"/>`;
    });

    const body = cotPanel.querySelector('.cot-body');
    if (body) {
        body.appendChild(stepEl);
        body.scrollTop = body.scrollHeight;
    }
}

// ── Quick Investigation from Dashboard ──
async function runQuickInvestigation(query) {
    switchView('ai-chat');
    const input = document.getElementById('chatInput');
    if (input) {
        input.value = query;
        sendChat();
    }
}

// ── Load Quick Actions ──
async function loadQuickActions(view, device) {
    try {
        const resp = await fetch('/api/ai/quick-actions', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ view: view || state.currentView, device: device || '' })
        });
        const data = await resp.json();
        const container = document.getElementById('quickActions');
        if (!container || !data.actions) return;
        container.innerHTML = data.actions.map(a =>
            `<button class="quick-action-btn" onclick="runQuickInvestigation(\`${a.query}\`)">
                ${a.label}
            </button>`
        ).join('');
    } catch (_) {}
}

function generateLocalResponse(msg) {
    const lower = msg.toLowerCase();
    if (lower.includes('topology') || lower.includes('summary')) {
        if (!state.topology) return 'Topology data not yet loaded. Please wait...';
        const t = state.topology;
        return `**Network Topology Summary**\n\n• Devices: ${t.nodes?.length || 0}\n• Physical Links: ${t.links?.length || 0}\n• PE Routers: ${t.nodes?.filter(n => n.role === 'PE').length || 0}\n• P Routers: ${t.nodes?.filter(n => n.role === 'P').length || 0}\n• Route Reflectors: ${t.nodes?.filter(n => n.role === 'Route Reflector').length || 0}`;
    }
    if (lower.includes('spof') || lower.includes('single point') || lower.includes('failure')) {
        if (!state.stats) return 'Stats not loaded yet.';
        const spofs = state.stats.single_points_of_failure || [];
        return spofs.length === 0
            ? 'No single points of failure detected. The network has good redundancy.'
            : `**Single Points of Failure Detected:**\n\n${spofs.map(s => `• ${s}`).join('\n')}\n\nConsider adding redundant links.`;
    }
    if (lower.includes('bgp')) {
        if (!state.topology) return 'Data loading...';
        const bgpNodes = state.topology.nodes?.filter(n => n.bgp_neighbors?.length > 0) || [];
        return `**BGP Session Overview**\n\n${bgpNodes.map(n => `• ${n.id}: ${n.bgp_neighbors.length} peer(s) → ${n.bgp_neighbors.join(', ')}`).join('\n')}`;
    }
    return `AI engine offline — using local fallback.\n\nTry: topology summary, SPOF analysis, BGP status`;
}

// ═══════════════════════════════════════
//  Templates Engine
// ═══════════════════════════════════════
async function loadTemplates() {
    try {
        state.templates = await api('templates');
    } catch (e) { state.templates = []; }
}

function renderTemplateList() {
    const list = document.getElementById('templateList');
    if (!list) return;
    list.innerHTML = state.templates.map(t =>
        `<div class="config-item" onclick="selectTemplate('${t.name}')">${t.name}<span class="badge badge-p" style="margin-left:auto;font-size:0.7rem">${t.lines} lines</span></div>`
    ).join('');
    // Populate deploy router selector
    const sel = document.getElementById('templateDeployRouter');
    if (sel && state.topology) {
        sel.innerHTML = state.topology.nodes.map(n => `<option value="${n.id}">${n.id}</option>`).join('');
    }
}

function selectTemplate(name) {
    const tmpl = state.templates.find(t => t.name === name);
    if (!tmpl) return;
    state.selectedTemplate = name;
    document.getElementById('templateSource').textContent = tmpl.content;
    document.querySelectorAll('#templateList .config-item').forEach(i => i.classList.remove('active'));
    event.target.closest('.config-item')?.classList.add('active');
    document.getElementById('templateOutput').style.display = 'none';
    document.getElementById('templateDeployResult').style.display = 'none';
}

async function renderTemplate() {
    if (!state.selectedTemplate) return alert('Select a template first');
    let vars = {};
    const varsInput = document.getElementById('templateVars').value.trim();
    if (varsInput) {
        try { vars = JSON.parse(varsInput); }
        catch (e) { return alert('Invalid JSON in variables field: ' + e.message); }
    }
    try {
        const resp = await fetch('/api/templates/render', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ template: state.selectedTemplate, variables: vars })
        });
        const data = await resp.json();
        if (data.error) return alert(data.error);
        document.getElementById('templateRendered').textContent = data.rendered;
        document.getElementById('templateOutputLines').textContent = data.lines + ' lines';
        document.getElementById('templateOutput').style.display = '';
    } catch (e) { alert('Render failed: ' + e.message); }
}

async function deployTemplate() {
    if (!state.selectedTemplate) return alert('Select a template first');
    const router = document.getElementById('templateDeployRouter').value;
    if (!router) return alert('Select a target router');
    if (!confirm(`Deploy template "${state.selectedTemplate}" to ${router}?`)) return;
    logAuditAction('deploy', `Deploying template "${state.selectedTemplate}" → ${router}`);
    let vars = {};
    const varsInput = document.getElementById('templateVars').value.trim();
    if (varsInput) { try { vars = JSON.parse(varsInput); } catch (e) {} }
    try {
        const resp = await fetch('/api/templates/deploy', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ template: state.selectedTemplate, variables: vars, router, comment: `NOC Template: ${state.selectedTemplate}` })
        });
        const data = await resp.json();
        document.getElementById('deployResultContent').textContent = data.deploy_result || data.error || JSON.stringify(data, null, 2);
        document.getElementById('templateDeployResult').style.display = '';
    } catch (e) { alert('Deploy failed: ' + e.message); }
}

// ═══════════════════════════════════════
//  Log Viewer
// ═══════════════════════════════════════
async function loadLogFiles() {
    try {
        const logs = await api('logs');
        const list = document.getElementById('logFileList');
        if (!list) return;
        list.innerHTML = logs.map(l =>
            `<div class="config-item" onclick="loadLogFile('${l.filename}')">${l.filename}<span class="badge badge-p" style="margin-left:auto;font-size:0.7rem">${l.lines} lines</span></div>`
        ).join('');
    } catch (e) { /* ignore */ }
}

async function loadLogFile(filename) {
    state.currentLogFile = filename;
    document.querySelectorAll('#logFileList .config-item').forEach(i => i.classList.remove('active'));
    event?.target?.closest('.config-item')?.classList.add('active');
    await reloadLog();
}

async function reloadLog() {
    if (!state.currentLogFile) return;
    const viewer = document.getElementById('logViewer');
    viewer.innerHTML = '<div class="loading" style="height:400px;margin:12px"></div>';
    const level = document.getElementById('logLevelFilter')?.value || '';
    const search = document.getElementById('logSearchInput')?.value || '';
    const tail = document.getElementById('logTailLines')?.value || 0;
    try {
        const params = new URLSearchParams();
        if (level) params.set('level', level);
        if (search) params.set('search', search);
        if (tail > 0) params.set('tail', tail);
        const data = await api(`logs/${state.currentLogFile}?${params.toString()}`);
        const lines = data.lines || [];
        viewer.innerHTML = `<div style="padding:8px 16px;border-bottom:1px solid var(--border-subtle);font-size:0.8rem;color:var(--text-tertiary)">
            ${state.currentLogFile} — ${data.filtered_lines} / ${data.total_lines} lines
        </div><pre class="log-content">${lines.map(l => colorizeLogLine(l)).join('\n')}</pre>`;
    } catch (e) {
        viewer.innerHTML = `<div class="empty-state"><p>Failed to load log: ${e.message}</p></div>`;
    }
}

function colorizeLogLine(line) {
    const esc = escapeHtml(line);
    if (esc.includes('[ERROR]')) return `<span style="color:var(--hpe-rose)">${esc}</span>`;
    if (esc.includes('[WARNING]')) return `<span style="color:var(--hpe-amber)">${esc}</span>`;
    if (esc.includes('[INFO]')) return `<span style="color:var(--text-secondary)">${esc}</span>`;
    if (esc.includes('[DEBUG]')) return `<span style="color:var(--text-tertiary)">${esc}</span>`;
    return esc;
}

async function analyzeLog() {
    if (!state.currentLogFile) return alert('Select a log file first');
    const analysisEl = document.getElementById('logAnalysis');
    const contentEl = document.getElementById('logAnalysisContent');
    analysisEl.style.display = '';
    contentEl.innerHTML = '<div class="loading" style="height:80px"></div>';
    try {
        const logData = await api(`logs/${state.currentLogFile}?tail=200`);
        const lines = (logData.lines || []).join('\n');
        const resp = await fetch('/api/ai/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                data: lines,
                question: 'Analyze these network logs. Identify errors, warnings, patterns, anomalies, and provide recommendations.',
                system: 'You are a Junos network operations expert. Analyze system logs and identify issues, trends, and actionable recommendations.'
            })
        });
        const data = await resp.json();
        contentEl.innerHTML = formatChatText(data.analysis || data.error || 'No analysis available');
    } catch (e) {
        contentEl.innerHTML = `<p style="color:var(--hpe-rose)">AI analysis failed: ${e.message}. Ensure Ollama is running.</p>`;
    }
}

// ═══════════════════════════════════════
//  Scheduler
// ═══════════════════════════════════════
async function loadScheduledTasks() {
    try {
        state.scheduledTasks = await api('scheduled-tasks');
        renderSchedulerTable();
    } catch (e) { state.scheduledTasks = []; }
}

function populateSchedulerRouters() {
    const sel = document.getElementById('schedRouters');
    if (!sel || !state.topology) return;
    sel.innerHTML = state.topology.nodes.map(n =>
        `<option value="${n.id}" selected>${n.id}</option>`
    ).join('');
}

function renderSchedulerTable() {
    const tbody = document.getElementById('schedulerTableBody');
    if (!tbody) return;
    if (!state.scheduledTasks.length) {
        tbody.innerHTML = '<tr><td colspan="8" class="empty-state" style="padding:40px">No scheduled tasks yet</td></tr>';
        return;
    }
    tbody.innerHTML = state.scheduledTasks.map(t => {
        const routers = JSON.parse(t.target_routers || '[]');
        const statusClass = t.enabled ? 'badge-yes' : 'badge-no';
        return `<tr>
            <td><strong>${escapeHtml(t.name)}</strong></td>
            <td style="font-family:var(--font-mono);font-size:0.8rem">${escapeHtml(t.command)}</td>
            <td>${t.schedule}</td>
            <td>${routers.join(', ')}</td>
            <td style="font-size:0.75rem">${t.last_run ? new Date(t.last_run).toLocaleString() : '—'}</td>
            <td>${t.run_count || 0}</td>
            <td><span class="badge ${statusClass}">${t.enabled ? 'Active' : 'Paused'}</span></td>
            <td>
                <button class="btn-sm" onclick="toggleTask(${t.id})">${t.enabled ? '<i data-lucide="pause" style="width:12px;height:12px"></i>' : '<i data-lucide="play" style="width:12px;height:12px"></i>'}</button>
                <button class="btn-sm" onclick="runTaskNow(${t.id})"><i data-lucide="zap" style="width:12px;height:12px"></i></button>
                <button class="btn-sm" onclick="deleteTask(${t.id})"><i data-lucide="trash-2" style="width:12px;height:12px"></i></button>
            </td>
        </tr>`;
    }).join('');
    if (typeof lucide !== 'undefined') lucide.createIcons();
}

async function createScheduledTask() {
    const name = document.getElementById('schedName').value.trim();
    const command = document.getElementById('schedCommand').value.trim();
    const schedule = document.getElementById('schedInterval').value;
    const routerSel = document.getElementById('schedRouters');
    const routers = Array.from(routerSel.selectedOptions).map(o => o.value);
    if (!name || !command) return alert('Name and command are required');
    if (!routers.length) return alert('Select at least one router');
    logAuditAction('create', `Creating scheduled task: "${name}" on ${routers.length} router(s)`);
    try {
        await fetch('/api/scheduled-tasks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, command, schedule, routers, task_type: 'command' })
        });
        document.getElementById('schedName').value = '';
        document.getElementById('schedCommand').value = '';
        loadScheduledTasks();
    } catch (e) { alert('Failed: ' + e.message); }
}

async function toggleTask(id) {
    await fetch(`/api/scheduled-tasks/${id}/toggle`, { method: 'POST' });
    loadScheduledTasks();
}

async function runTaskNow(id) {
    const resp = await fetch(`/api/scheduled-tasks/${id}/run`, { method: 'POST' });
    const data = await resp.json();
    alert(`Task ran: ${data.status}\nDuration: ${data.duration_ms}ms\n\n${(data.result || '').substring(0, 500)}`);
    loadScheduledTasks();
}

async function deleteTask(id) {
    if (!confirm('Delete this scheduled task?')) return;
    await fetch(`/api/scheduled-tasks/${id}`, { method: 'DELETE' });
    loadScheduledTasks();
}

// ═══════════════════════════════════════
//  Workflows
// ═══════════════════════════════════════
async function loadWorkflows() {
    try {
        state.workflows = await api('workflows');
    } catch (e) { state.workflows = []; }
}

function renderWorkflowList() {
    const list = document.getElementById('workflowList');
    if (!list) return;
    list.innerHTML = state.workflows.map(w =>
        `<div class="config-item" onclick="loadWorkflow('${escapeHtml(w.name)}')">${escapeHtml(w.name)}<span class="badge badge-p" style="margin-left:auto;font-size:0.7rem">${(w.steps || []).length} steps</span></div>`
    ).join('');
}

function newWorkflow() {
    state.currentWorkflow = { name: '', steps: [], variables: {} };
    document.getElementById('workflowName').value = '';
    renderWorkflowSteps();
    document.getElementById('workflowResults').style.display = 'none';
}

function loadWorkflow(name) {
    const wf = state.workflows.find(w => w.name === name);
    if (!wf) return;
    state.currentWorkflow = JSON.parse(JSON.stringify(wf));
    document.getElementById('workflowName').value = wf.name;
    renderWorkflowSteps();
}

function addWorkflowStep() {
    const type = document.getElementById('stepType').value;
    const step = { type, name: `Step ${state.currentWorkflow.steps.length + 1}: ${type}` };
    
    if (type === 'command') { step.router = ''; step.command = ''; }
    else if (type === 'batch') { step.routers = []; step.command = ''; }
    else if (type === 'template') { step.template = ''; step.variables = {}; }
    else if (type === 'deploy') { step.router = ''; step.config = ''; step.commit_comment = 'Workflow'; }
    else if (type === 'ai_analyze') { step.data = ''; step.question = ''; }
    else if (type === 'condition') { step.check_step = 1; step.pattern = ''; }
    else if (type === 'wait') { step.seconds = 5; }
    else if (type === 'rest_call') { step.url = ''; step.method = 'GET'; step.headers = {}; step.body = ''; step.ai_analyze_response = false; }
    else if (type === 'python_snippet') { step.code = ''; }
    else if (type === 'ping_sweep') { step.routers = []; }
    else if (type === 'validate') { step.router = ''; step.command = ''; step.pattern = ''; }
    else if (type === 'notify') { step.channel_id = ''; step.title = ''; step.message = ''; }
    
    state.currentWorkflow.steps.push(step);
    renderWorkflowSteps();
}

function removeWorkflowStep(idx) {
    state.currentWorkflow.steps.splice(idx, 1);
    renderWorkflowSteps();
}

function renderWorkflowSteps() {
    const container = document.getElementById('workflowSteps');
    if (!container) return;
    const steps = state.currentWorkflow.steps;
    if (!steps.length) {
        container.innerHTML = '<div class="empty-state"><p>Add steps to build your workflow</p></div>';
        return;
    }
    const nodes = state.topology?.nodes || [];
    const routerOpts = nodes.map(n => `<option value="${n.id}">${n.id}</option>`).join('');
    const tmplOpts = state.templates.map(t => `<option value="${t.name}">${t.name}</option>`).join('');
    
    container.innerHTML = steps.map((step, i) => {
        const typeColors = { command: 'var(--hpe-green)', batch: 'var(--hpe-blue)', template: 'var(--hpe-purple)',
            deploy: 'var(--hpe-orange)', ai_analyze: 'var(--hpe-teal)', condition: 'var(--hpe-amber)', wait: 'var(--text-tertiary)' };
        const color = typeColors[step.type] || 'var(--text-primary)';
        let fields = '';
        if (step.type === 'command') {
            fields = `<select class="step-input" onchange="state.currentWorkflow.steps[${i}].router=this.value" title="Router">${routerOpts}</select>
                <input class="step-input" placeholder="Command" value="${escapeHtml(step.command || '')}" onchange="state.currentWorkflow.steps[${i}].command=this.value">`;
        } else if (step.type === 'batch') {
            fields = `<input class="step-input" placeholder="Command" value="${escapeHtml(step.command || '')}" onchange="state.currentWorkflow.steps[${i}].command=this.value">
                <small>All routers will be targeted</small>`;
        } else if (step.type === 'template') {
            fields = `<select class="step-input" onchange="state.currentWorkflow.steps[${i}].template=this.value" title="Template">${tmplOpts}</select>`;
        } else if (step.type === 'deploy') {
            fields = `<select class="step-input" onchange="state.currentWorkflow.steps[${i}].router=this.value" title="Router">${routerOpts}</select>
                <input class="step-input" placeholder="Config or $step_N ref" value="${escapeHtml(step.config || '')}" onchange="state.currentWorkflow.steps[${i}].config=this.value">`;
        } else if (step.type === 'ai_analyze') {
            fields = `<input class="step-input" placeholder="Data or $step_N ref" value="${escapeHtml(step.data || '')}" onchange="state.currentWorkflow.steps[${i}].data=this.value">
                <input class="step-input" placeholder="Question" value="${escapeHtml(step.question || '')}" onchange="state.currentWorkflow.steps[${i}].question=this.value">`;
        } else if (step.type === 'condition') {
            fields = `<input class="step-input" type="number" placeholder="Check step #" value="${step.check_step || 1}" onchange="state.currentWorkflow.steps[${i}].check_step=this.value" style="width:100px">
                <input class="step-input" placeholder="Regex pattern" value="${escapeHtml(step.pattern || '')}" onchange="state.currentWorkflow.steps[${i}].pattern=this.value">`;
        } else if (step.type === 'wait') {
            fields = `<input class="step-input" type="number" placeholder="Seconds" value="${step.seconds || 5}" onchange="state.currentWorkflow.steps[${i}].seconds=parseInt(this.value)" style="width:100px">`;
        }
        return `<div class="workflow-step-card" style="border-left:3px solid ${color}">
            <div class="step-header">
                <span class="step-number">${i + 1}</span>
                <span class="step-type" style="color:${color}">${step.type.toUpperCase()}</span>
                <input class="step-name-input" value="${escapeHtml(step.name || '')}" onchange="state.currentWorkflow.steps[${i}].name=this.value">
                <button class="btn-sm" onclick="removeWorkflowStep(${i})"><i data-lucide="x" style="width:12px;height:12px"></i></button>
            </div>
            <div class="step-fields">${fields}</div>
        </div>`;
    }).join('<div class="step-connector">↓</div>');
    if (typeof lucide !== 'undefined') lucide.createIcons();
}

async function saveCurrentWorkflow() {
    const name = document.getElementById('workflowName').value.trim();
    if (!name) return alert('Enter a workflow name');
    state.currentWorkflow.name = name;
    await fetch('/api/workflows', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(state.currentWorkflow)
    });
    loadWorkflows();
    setTimeout(renderWorkflowList, 300);
}

async function executeCurrentWorkflow() {
    if (!state.currentWorkflow.steps.length) return alert('Add steps first');
    const name = document.getElementById('workflowName').value.trim() || 'Unnamed';
    state.currentWorkflow.name = name;
    logAuditAction('execute', `Executing workflow: "${name}" (${state.currentWorkflow.steps.length} steps)`);
    
    // Set batch routers for batch steps
    state.currentWorkflow.steps.forEach(s => {
        if (s.type === 'batch' && (!s.routers || !s.routers.length)) {
            s.routers = (state.topology?.nodes || []).map(n => n.id);
        }
    });
    
    const resultsEl = document.getElementById('workflowResults');
    const body = document.getElementById('workflowResultsBody');
    resultsEl.style.display = '';
    body.innerHTML = '<div class="loading" style="height:80px"></div>';
    
    try {
        const resp = await fetch('/api/workflows/execute', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(state.currentWorkflow)
        });
        const data = await resp.json();
        if (data.error) { body.innerHTML = `<p style="color:var(--hpe-rose)">${data.error}</p>`; return; }
        body.innerHTML = (data.results || []).map((r, i) => {
            const statusColor = r.status === 'success' ? 'var(--hpe-green)' : (r.status === 'error' ? 'var(--hpe-rose)' : 'var(--hpe-amber)');
            return `<div class="workflow-result-item">
                <div class="workflow-result-header">
                    <span style="color:${statusColor}">● Step ${r.step}: ${escapeHtml(r.name)}</span>
                    <span style="font-size:0.75rem;color:var(--text-tertiary)">${r.duration_ms}ms</span>
                </div>
                <pre class="workflow-result-output">${escapeHtml((r.output || '').substring(0, 2000))}</pre>
            </div>`;
        }).join('');
    } catch (e) { body.innerHTML = `<p style="color:var(--hpe-rose)">Execution failed: ${e.message}</p>`; }
}

// ═══════════════════════════════════════
//  MCP Direct Commands
// ═══════════════════════════════════════
async function executeMCPCommand(router, command) {
    try {
        const resp = await fetch('/api/mcp/execute', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ router, command })
        });
        return await resp.json();
    } catch (e) { return { error: e.message }; }
}

async function fetchLiveConfig(router) {
    try {
        const data = await api(`mcp/live-config/${router}`);
        return data;
    } catch (e) { return { error: e.message }; }
}

// ═══════════════════════════════════════
//  Result Comparison (Feature #13)
// ═══════════════════════════════════════
function populateCompareRouters() {
    const sel = document.getElementById('captureRouter');
    if (!sel || !state.topology) return;
    sel.innerHTML = state.topology.nodes.map(n => `<option value="${n.id}">${n.id}</option>`).join('');
}

async function captureResult() {
    const name = document.getElementById('captureName').value.trim();
    const router = document.getElementById('captureRouter').value;
    const command = document.getElementById('captureCommand').value.trim();
    if (!name || !router || !command) return alert('All fields required');
    try {
        const resp = await fetch('/api/results/capture', {
            method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name, router, command})
        });
        const data = await resp.json();
        if (data.error) return alert(data.error);
        alert(`Captured "${name}": ${data.lines} lines`);
        document.getElementById('captureName').value = '';
        document.getElementById('captureCommand').value = '';
        loadCapturedResults();
    } catch (e) { alert('Capture failed: ' + e.message); }
}

async function loadCapturedResults() {
    try {
        state.capturedResults = await api('results');
        renderCapturedResults();
        populateCompareSelectors();
    } catch (e) { state.capturedResults = []; }
}

function renderCapturedResults() {
    const tbody = document.getElementById('capturedResultsBody');
    if (!tbody) return;
    if (!state.capturedResults || !state.capturedResults.length) {
        tbody.innerHTML = '<tr><td colspan="6" class="empty-state" style="padding:40px">No captured results yet</td></tr>';
        return;
    }
    tbody.innerHTML = state.capturedResults.map(r => `<tr>
        <td><strong>${escapeHtml(r.name)}</strong></td>
        <td>${escapeHtml(r.router)}</td>
        <td style="font-family:var(--font-mono);font-size:0.8rem">${escapeHtml(r.command)}</td>
        <td>${r.lines}</td>
        <td style="font-size:0.75rem">${r.captured_at ? new Date(r.captured_at).toLocaleString() : '—'}</td>
        <td><button class="btn-sm" onclick="deleteResult('${escapeHtml(r.name)}')"><i data-lucide="trash-2" style="width:12px;height:12px"></i></button></td>
    </tr>`).join('');
    if (typeof lucide !== 'undefined') lucide.createIcons();
}

function populateCompareSelectors() {
    const selA = document.getElementById('compareA');
    const selB = document.getElementById('compareB');
    if (!selA || !selB) return;
    const opts = (state.capturedResults || []).map(r => `<option value="${escapeHtml(r.name)}">${escapeHtml(r.name)} (${r.router})</option>`).join('');
    selA.innerHTML = opts;
    selB.innerHTML = opts;
    if (state.capturedResults && state.capturedResults.length > 1) selB.selectedIndex = 1;
}

async function compareResults() {
    const a = document.getElementById('compareA').value;
    const b = document.getElementById('compareB').value;
    if (!a || !b) return alert('Select two results to compare');
    if (a === b) return alert('Select different results');
    const el = document.getElementById('compareOutput');
    const body = document.getElementById('compareOutputBody');
    el.style.display = '';
    body.innerHTML = '<div class="loading" style="height:120px"></div>';
    try {
        const resp = await fetch('/api/results/compare', {
            method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({result_a: a, result_b: b})
        });
        const data = await resp.json();
        if (data.error) { body.innerHTML = `<p style="color:var(--hpe-rose)">${escapeHtml(data.error)}</p>`; return; }
        const diffHtml = (data.diff || '').split('\n').map(l => {
            if (l.startsWith('+') && !l.startsWith('+++')) return `<span style="color:var(--hpe-green)">${escapeHtml(l)}</span>`;
            if (l.startsWith('-') && !l.startsWith('---')) return `<span style="color:var(--hpe-rose)">${escapeHtml(l)}</span>`;
            if (l.startsWith('@@')) return `<span style="color:var(--hpe-blue)">${escapeHtml(l)}</span>`;
            return escapeHtml(l);
        }).join('\n');
        body.innerHTML = `
            <div class="compare-header">
                <div class="compare-side">
                    <strong>${escapeHtml(data.result_a?.name || a)}</strong>
                    <span class="badge badge-p">${data.result_a?.router || ''}</span>
                    <span style="font-size:0.75rem;color:var(--text-tertiary)">${data.result_a?.lines || 0} lines</span>
                </div>
                <div class="compare-stats">
                    <span class="badge badge-yes">+${data.additions || 0}</span>
                    <span class="badge badge-no">-${data.deletions || 0}</span>
                </div>
                <div class="compare-side">
                    <strong>${escapeHtml(data.result_b?.name || b)}</strong>
                    <span class="badge badge-p">${data.result_b?.router || ''}</span>
                    <span style="font-size:0.75rem;color:var(--text-tertiary)">${data.result_b?.lines || 0} lines</span>
                </div>
            </div>
            <pre class="diff-output">${diffHtml || '<span style="color:var(--text-tertiary)">No differences found</span>'}</pre>
            ${data.ai_analysis ? `<div class="ai-diff-analysis"><h4><i data-lucide="bot" class="card-header-icon"></i> AI Analysis</h4>${formatChatText(data.ai_analysis)}</div>` : ''}
        `;
        if (typeof lucide !== 'undefined') lucide.createIcons();
    } catch (e) { body.innerHTML = `<p style="color:var(--hpe-rose)">Compare failed: ${e.message}</p>`; }
}

async function deleteResult(name) {
    if (!confirm(`Delete result "${name}"?`)) return;
    await fetch(`/api/results/${encodeURIComponent(name)}`, {method: 'DELETE'});
    loadCapturedResults();
}

// ══════════════════════════════════════════════════════════════════════════════
//  DEVICE POOLS (Feature #10)
// ══════════════════════════════════════════════════════════════════════════════

async function loadPools() {
    try {
        const pools = await api('pools');
        state.pools = pools;
        renderPoolsGrid(pools);
    } catch (e) { console.error('loadPools error:', e); }
}

function renderPoolsGrid(pools) {
    const grid = document.getElementById('poolsGrid');
    if (!grid) return;
    if (!pools || pools.length === 0) {
        grid.innerHTML = '<div class="empty-state" style="padding:60px"><p>No device pools yet. Create one or let AI recommend optimal groupings.</p></div>';
        return;
    }
    grid.innerHTML = pools.map(p => {
        const devices = typeof p.devices === 'string' ? JSON.parse(p.devices) : (p.devices || []);
        const tags = typeof p.tags === 'string' ? JSON.parse(p.tags) : (p.tags || []);
        return `<div class="pool-card card" style="border-left:4px solid ${escapeHtml(p.color || '#01A982')}">
            <div class="card-header">
                <h3 style="display:flex;align-items:center;gap:8px">
                    <span style="width:12px;height:12px;border-radius:50%;background:${escapeHtml(p.color || '#01A982')};display:inline-block"></span>
                    ${escapeHtml(p.name)}
                </h3>
                <button class="btn-sm" onclick="deletePool(${p.id})" title="Delete pool"><i data-lucide="trash-2" style="width:14px;height:14px"></i></button>
            </div>
            <div class="card-body">
                <p style="color:var(--text-secondary);font-size:0.85rem;margin-bottom:8px">${escapeHtml(p.description || '')}</p>
                <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px">
                    ${devices.map(d => `<span class="badge badge-pe">${escapeHtml(d)}</span>`).join('')}
                </div>
                <div style="display:flex;flex-wrap:wrap;gap:4px">
                    ${tags.map(t => `<span class="badge badge-yes" style="font-size:0.7rem">${escapeHtml(t)}</span>`).join('')}
                </div>
                <div style="font-size:0.7rem;color:var(--text-tertiary);margin-top:8px">${devices.length} device${devices.length !== 1 ? 's' : ''}</div>
            </div>
        </div>`;
    }).join('');
    if (typeof lucide !== 'undefined') lucide.createIcons();
}

function populatePoolDevices() {
    const sel = document.getElementById('poolDevices');
    if (!sel || !state.topology) return;
    sel.innerHTML = state.topology.nodes.map(n => `<option value="${n.id}">${n.id} (${n.role || 'unknown'})</option>`).join('');
}

function showCreatePoolModal() {
    populatePoolDevices();
    document.getElementById('createPoolModal').style.display = 'flex';
}

function hideCreatePoolModal() {
    document.getElementById('createPoolModal').style.display = 'none';
}

async function createPool() {
    const name = document.getElementById('poolName')?.value.trim();
    const desc = document.getElementById('poolDesc')?.value.trim();
    const color = document.getElementById('poolColor')?.value || '#01A982';
    const sel = document.getElementById('poolDevices');
    const devices = sel ? Array.from(sel.selectedOptions).map(o => o.value) : [];
    const tagsRaw = document.getElementById('poolTags')?.value || '';
    const tags = tagsRaw.split(',').map(t => t.trim()).filter(Boolean);
    if (!name) return alert('Pool name is required');
    try {
        await apiPost('pools', { name, description: desc, color, devices, tags });
        hideCreatePoolModal();
        document.getElementById('poolName').value = '';
        document.getElementById('poolDesc').value = '';
        document.getElementById('poolTags').value = '';
        loadPools();
    } catch (e) { alert('Create pool failed: ' + e.message); }
}

async function deletePool(id) {
    if (!confirm('Delete this pool?')) return;
    await fetch(`/api/pools/${id}`, { method: 'DELETE' });
    loadPools();
}

async function aiRecommendPools() {
    const el = document.getElementById('aiPoolRecommendations');
    const body = document.getElementById('aiPoolRecBody');
    if (!el || !body) return;
    el.style.display = '';
    body.innerHTML = '<div class="loading" style="height:120px"></div>';
    try {
        const data = await apiPost('pools/ai-recommend', {});
        if (data.recommendations) {
            body.innerHTML = data.recommendations.map(r => `
                <div class="pool-rec" style="border-left:4px solid ${escapeHtml(r.color || '#01A982')};padding:12px;margin-bottom:12px;background:var(--glass-bg);border-radius:8px">
                    <h4>${escapeHtml(r.name)}</h4>
                    <p style="font-size:0.85rem;color:var(--text-secondary)">${escapeHtml(r.description || '')}</p>
                    <div style="margin:8px 0">${(r.devices || []).map(d => `<span class="badge badge-pe">${escapeHtml(d)}</span>`).join(' ')}</div>
                    <p style="font-size:0.8rem;color:var(--text-tertiary)">${escapeHtml(r.reasoning || '')}</p>
                    <button class="btn-sm btn-primary" onclick="applyPoolRecommendation(${JSON.stringify(r).replace(/"/g, '&quot;')})">Apply</button>
                </div>
            `).join('');
        } else {
            body.innerHTML = `<div>${formatChatText(data.analysis || data.error || 'No recommendations')}</div>`;
        }
    } catch (e) { body.innerHTML = `<p style="color:var(--hpe-rose)">AI recommendation failed: ${e.message}</p>`; }
}

async function applyPoolRecommendation(rec) {
    try {
        await apiPost('pools', { name: rec.name, description: rec.description, color: rec.color, devices: rec.devices, tags: rec.tags || [] });
        loadPools();
    } catch (e) { alert('Apply failed: ' + e.message); }
}

// ══════════════════════════════════════════════════════════════════════════════
//  PING / REACHABILITY (Feature #7)
// ══════════════════════════════════════════════════════════════════════════════

function populatePingRouters() {
    const sel = document.getElementById('pingSingleRouter');
    if (!sel || !state.topology) return;
    sel.innerHTML = state.topology.nodes.map(n => `<option value="${n.id}">${n.id}</option>`).join('');
}

async function pingSingleRouter() {
    const router = document.getElementById('pingSingleRouter')?.value;
    if (!router) return;
    const grid = document.getElementById('pingResults');
    if (grid) grid.innerHTML = '<div class="loading" style="height:80px"></div>';
    try {
        const data = await api(`ping/${encodeURIComponent(router)}`);
        state.lastPingResults = [data];
        renderPingResults([data]);
    } catch (e) { if (grid) grid.innerHTML = `<p style="color:var(--hpe-rose)">Ping failed: ${e.message}</p>`; }
}

async function pingSweepAll() {
    const grid = document.getElementById('pingResults');
    if (grid) grid.innerHTML = '<div class="loading" style="height:120px"></div>';
    try {
        const data = await apiPost('ping/sweep', {});
        state.lastPingResults = data.results || [];
        renderPingResults(data.results || [], data.total_ms);
    } catch (e) { if (grid) grid.innerHTML = `<p style="color:var(--hpe-rose)">Sweep failed: ${e.message}</p>`; }
}

function renderPingResults(results, totalMs) {
    const grid = document.getElementById('pingResults');
    if (!grid) return;
    if (!results.length) { grid.innerHTML = '<div class="empty-state"><p>No results</p></div>'; return; }
    grid.innerHTML = `
        ${totalMs ? `<div style="margin-bottom:12px;font-size:0.85rem;color:var(--text-secondary)">Sweep completed in ${totalMs}ms</div>` : ''}
        <div class="ping-results-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px">
            ${results.map(r => `
                <div class="card" style="border-left:4px solid ${r.reachable ? 'var(--hpe-green)' : 'var(--hpe-rose)'}">
                    <div class="card-body" style="padding:12px">
                        <div style="display:flex;align-items:center;justify-content:space-between">
                            <strong>${escapeHtml(r.router)}</strong>
                            <span class="badge ${r.reachable ? 'badge-yes' : 'badge-no'}">${r.reachable ? 'UP' : 'DOWN'}</span>
                        </div>
                        ${r.latency_ms != null ? `<div style="font-size:0.8rem;color:var(--text-tertiary);margin-top:4px">${r.latency_ms}ms</div>` : ''}
                        ${r.error ? `<div style="font-size:0.8rem;color:var(--hpe-rose);margin-top:4px">${escapeHtml(r.error)}</div>` : ''}
                    </div>
                </div>
            `).join('')}
        </div>`;
}

async function aiAnalyzePing() {
    const el = document.getElementById('pingAIAnalysis');
    const body = document.getElementById('pingAIContent');
    if (!el || !body) return;
    if (!state.lastPingResults || !state.lastPingResults.length) return alert('Run a ping sweep first');
    el.style.display = '';
    body.innerHTML = '<div class="loading" style="height:80px"></div>';
    try {
        const data = await apiPost('ping/ai-analyze', { results: state.lastPingResults });
        body.innerHTML = formatChatText(data.analysis || 'No analysis available');
    } catch (e) { body.innerHTML = `<p style="color:var(--hpe-rose)">AI analysis failed: ${e.message}</p>`; }
}

// ══════════════════════════════════════════════════════════════════════════════
//  DATA VALIDATION (Feature #9)
// ══════════════════════════════════════════════════════════════════════════════

function populateValidationRouters() {
    const sel = document.getElementById('valRouter');
    if (!sel || !state.topology) return;
    sel.innerHTML = state.topology.nodes.map(n => `<option value="${n.id}">${n.id}</option>`).join('');
}

async function runValidation() {
    const router = document.getElementById('valRouter')?.value;
    const command = document.getElementById('valCommand')?.value.trim();
    const pattern = document.getElementById('valPattern')?.value.trim();
    const matchType = document.getElementById('valMatchType')?.value || 'contains';
    if (!router || !command || !pattern) return alert('All fields required');
    const el = document.getElementById('validationResults');
    const body = document.getElementById('validationResultsBody');
    if (el) el.style.display = '';
    if (body) body.innerHTML = '<div class="loading" style="height:80px"></div>';
    try {
        const data = await apiPost('validate', { router, command, pattern, match_type: matchType });
        if (body) body.innerHTML = `
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px">
                <span class="badge ${data.passed ? 'badge-yes' : 'badge-no'}" style="font-size:1rem;padding:6px 16px">${data.passed ? 'PASS' : 'FAIL'}</span>
                <strong>${escapeHtml(data.router)}</strong>
                <code style="font-size:0.8rem">${escapeHtml(data.command)}</code>
            </div>
            <pre class="code-output" style="max-height:300px;overflow:auto">${escapeHtml(data.output || '')}</pre>`;
    } catch (e) { if (body) body.innerHTML = `<p style="color:var(--hpe-rose)">${e.message}</p>`; }
}

async function runBatchValidation() {
    const command = document.getElementById('valCommand')?.value.trim();
    const pattern = document.getElementById('valPattern')?.value.trim();
    const matchType = document.getElementById('valMatchType')?.value || 'contains';
    if (!command || !pattern) return alert('Command and pattern required');
    const routers = state.topology ? state.topology.nodes.map(n => n.id) : [];
    if (!routers.length) return alert('No routers available');
    const el = document.getElementById('validationResults');
    const body = document.getElementById('validationResultsBody');
    if (el) el.style.display = '';
    if (body) body.innerHTML = '<div class="loading" style="height:120px"></div>';
    try {
        const data = await apiPost('validate/batch', { routers, command, pattern, match_type: matchType });
        if (body) body.innerHTML = `
            <div style="margin-bottom:12px">
                <span class="badge badge-yes">${data.passed || 0} passed</span>
                <span class="badge badge-no">${data.failed || 0} failed</span>
                <span style="font-size:0.85rem;color:var(--text-secondary);margin-left:8px">out of ${data.total || 0}</span>
            </div>
            <table class="data-table"><thead><tr><th>Router</th><th>Status</th><th>Output</th></tr></thead>
            <tbody>${(data.results || []).map(r => `<tr>
                <td><strong>${escapeHtml(r.router)}</strong></td>
                <td><span class="badge ${r.passed ? 'badge-yes' : 'badge-no'}">${r.passed ? 'PASS' : 'FAIL'}</span></td>
                <td style="font-size:0.75rem;font-family:var(--font-mono)">${escapeHtml((r.output || r.error || '').substring(0, 200))}</td>
            </tr>`).join('')}</tbody></table>`;
    } catch (e) { if (body) body.innerHTML = `<p style="color:var(--hpe-rose)">${e.message}</p>`; }
}

async function runAICompliance() {
    const router = document.getElementById('valRouter')?.value;
    if (!router) return alert('Select a router');
    const el = document.getElementById('complianceResults');
    const body = document.getElementById('complianceResultsBody');
    if (el) el.style.display = '';
    if (body) body.innerHTML = '<div class="loading" style="height:120px"></div>';
    try {
        const data = await apiPost('validate/ai-compliance', { router });
        if (body) body.innerHTML = `<h4 style="margin-bottom:12px">${escapeHtml(router)} — Compliance Audit</h4>${formatChatText(data.compliance || 'No report available')}`;
    } catch (e) { if (body) body.innerHTML = `<p style="color:var(--hpe-rose)">Compliance check failed: ${e.message}</p>`; }
}

// ══════════════════════════════════════════════════════════════════════════════
//  NOTIFICATIONS (Feature #8)
// ══════════════════════════════════════════════════════════════════════════════

async function loadNotificationChannels() {
    try {
        const channels = await api('notifications/channels');
        state.notifChannels = channels;
        renderNotifChannels(channels);
        populateNotifTestChannel(channels);
    } catch (e) { console.error('loadNotificationChannels error:', e); }
}

function renderNotifChannels(channels) {
    const grid = document.getElementById('notifChannels');
    if (!grid) return;
    if (!channels || channels.length === 0) {
        grid.innerHTML = '<div class="empty-state" style="padding:60px"><p>No notification channels configured. Add a Slack, Mattermost, or Webhook channel.</p></div>';
        return;
    }
    const typeIcons = { slack: 'hash', mattermost: 'message-square', webhook: 'globe' };
    grid.innerHTML = channels.map(c => `
        <div class="card" style="border-left:4px solid ${c.enabled ? 'var(--hpe-green)' : 'var(--text-tertiary)'}">
            <div class="card-header">
                <h3 style="display:flex;align-items:center;gap:8px">
                    <i data-lucide="${typeIcons[c.channel_type] || 'bell'}" style="width:16px;height:16px"></i>
                    ${escapeHtml(c.name)}
                </h3>
                <button class="btn-sm" onclick="deleteChannel(${c.id})" title="Delete"><i data-lucide="trash-2" style="width:14px;height:14px"></i></button>
            </div>
            <div class="card-body">
                <div><span class="badge badge-p">${escapeHtml(c.channel_type)}</span>
                    <span class="badge ${c.enabled ? 'badge-yes' : 'badge-no'}">${c.enabled ? 'Enabled' : 'Disabled'}</span></div>
                <div style="font-size:0.75rem;color:var(--text-tertiary);margin-top:6px;word-break:break-all">${escapeHtml(c.webhook_url || 'No URL')}</div>
            </div>
        </div>
    `).join('');
    if (typeof lucide !== 'undefined') lucide.createIcons();
}

function populateNotifTestChannel(channels) {
    const sel = document.getElementById('notifTestChannel');
    if (!sel) return;
    sel.innerHTML = (channels || []).map(c => `<option value="${c.id}">${escapeHtml(c.name)} (${c.channel_type})</option>`).join('');
}

function showCreateChannelModal() {
    document.getElementById('createChannelModal').style.display = 'flex';
}

function hideCreateChannelModal() {
    document.getElementById('createChannelModal').style.display = 'none';
}

async function createChannel() {
    const name = document.getElementById('channelName')?.value.trim();
    const channelType = document.getElementById('channelType')?.value || 'webhook';
    const webhookUrl = document.getElementById('channelWebhook')?.value.trim();
    if (!name) return alert('Channel name is required');
    try {
        await apiPost('notifications/channels', { name, channel_type: channelType, webhook_url: webhookUrl });
        hideCreateChannelModal();
        document.getElementById('channelName').value = '';
        document.getElementById('channelWebhook').value = '';
        loadNotificationChannels();
    } catch (e) { alert('Create channel failed: ' + e.message); }
}

async function deleteChannel(id) {
    if (!confirm('Delete this notification channel?')) return;
    await fetch(`/api/notifications/channels/${id}`, { method: 'DELETE' });
    loadNotificationChannels();
}

async function sendTestNotification() {
    const channelId = document.getElementById('notifTestChannel')?.value;
    const severity = document.getElementById('notifSeverity')?.value || 'info';
    const title = document.getElementById('notifTitle')?.value.trim() || 'Test Alert';
    const message = document.getElementById('notifMessage')?.value.trim();
    if (!channelId || !message) return alert('Select channel and enter message');
    try {
        const data = await apiPost('notifications/send', { channel_id: parseInt(channelId), title, message, severity });
        alert(data.status === 'sent' ? 'Notification sent successfully!' : `Notification ${data.status}: ${data.response}`);
    } catch (e) { alert('Send failed: ' + e.message); }
}

async function loadNotificationHistory() {
    const el = document.getElementById('notifHistory');
    const body = document.getElementById('notifHistoryBody');
    if (!el || !body) return;
    el.style.display = '';
    body.innerHTML = '<div class="loading" style="height:80px"></div>';
    try {
        const history = await api('notifications/history');
        if (!history.length) { body.innerHTML = '<p class="empty-state">No notification history</p>'; return; }
        body.innerHTML = `<table class="data-table"><thead><tr><th>Time</th><th>Title</th><th>Severity</th><th>Status</th></tr></thead>
        <tbody>${history.map(h => `<tr>
            <td style="font-size:0.75rem">${h.sent_at ? new Date(h.sent_at).toLocaleString() : '—'}</td>
            <td>${escapeHtml(h.title)}</td>
            <td><span class="badge ${h.severity === 'critical' ? 'badge-no' : h.severity === 'warning' ? 'badge-warn' : 'badge-yes'}">${escapeHtml(h.severity)}</span></td>
            <td><span class="badge ${h.status === 'sent' ? 'badge-yes' : 'badge-no'}">${escapeHtml(h.status)}</span></td>
        </tr>`).join('')}</tbody></table>`;
    } catch (e) { body.innerHTML = `<p style="color:var(--hpe-rose)">Failed to load history: ${e.message}</p>`; }
}

async function aiSummarizeAlerts() {
    if (!state.notifChannels) return alert('Load channels first');
    try {
        const history = await api('notifications/history');
        if (!history.length) return alert('No notification history to summarize');
        const data = await apiPost('notifications/ai-summary', { events: history });
        alert(data.summary || 'No summary generated');
    } catch (e) { alert('AI summary failed: ' + e.message); }
}

// ══════════════════════════════════════════════════════════════════════════════
//  GIT CONFIG EXPORT (Feature #11)
// ══════════════════════════════════════════════════════════════════════════════

async function loadGitLog() {
    const body = document.getElementById('gitLogBody');
    if (!body) return;
    body.innerHTML = '<div class="loading" style="height:80px"></div>';
    try {
        const data = await api('git-export/log');
        if (data.error) {
            body.innerHTML = `<div class="empty-state"><p>Git repo not initialized. Click "Init Repo" to start.</p></div>`;
            return;
        }
        const log = data.log || '';
        if (!log.trim()) {
            body.innerHTML = '<div class="empty-state"><p>No commits yet. Export configs to create the first commit.</p></div>';
            return;
        }
        body.innerHTML = `<pre class="code-output" style="max-height:400px;overflow:auto">${escapeHtml(log)}</pre>`;
    } catch (e) {
        body.innerHTML = `<div class="empty-state"><p>Git repo not initialized. Click "Init Repo" to start.</p></div>`;
    }
}

async function gitInitRepo() {
    try {
        const data = await apiPost('git-export/init', {});
        alert(data.status === 'initialized' ? 'Git repo initialized!' : data.error || 'Init failed');
        loadGitLog();
    } catch (e) { alert('Init failed: ' + e.message); }
}

async function gitExportConfigs() {
    const msg = document.getElementById('gitCommitMsg')?.value.trim() || '';
    const resultEl = document.getElementById('gitExportResult');
    const body = document.getElementById('gitExportResultBody');
    if (resultEl) resultEl.style.display = '';
    if (body) body.innerHTML = '<div class="loading" style="height:80px"></div>';
    try {
        const data = await apiPost('git-export/export', { message: msg });
        if (body) {
            if (data.status === 'no_changes') {
                body.innerHTML = '<p style="color:var(--text-secondary)">No config changes to commit.</p>';
            } else {
                body.innerHTML = `
                    <div style="margin-bottom:8px"><span class="badge badge-yes">Committed</span></div>
                    <p><strong>Message:</strong> ${escapeHtml(data.message)}</p>
                    ${data.changes?.length ? `<p><strong>Changed files:</strong> ${data.changes.map(f => escapeHtml(f)).join(', ')}</p>` : ''}
                    <pre class="code-output" style="margin-top:8px">${escapeHtml(data.log || '')}</pre>`;
            }
        }
        document.getElementById('gitCommitMsg').value = '';
        loadGitLog();
    } catch (e) { if (body) body.innerHTML = `<p style="color:var(--hpe-rose)">Export failed: ${e.message}</p>`; }
}

// ══════════════════════════════════════════════════════════════════════════════
//  BOOTSTRAP — Zero-config onboarding: detect first run, sync configs from MCP
// ══════════════════════════════════════════════════════════════════════════════

async function checkBootstrap() {
    try {
        const status = await api('bootstrap/status');
        const banner = document.getElementById('bootstrapBanner');
        if (!banner) return;
        if (!status.bootstrapped && !localStorage.getItem('noc-bootstrap-dismissed')) {
            banner.style.display = 'block';
            const msg = document.getElementById('bootstrapMsg');
            if (msg) {
                if (status.device_count === 0) {
                    msg.textContent = 'No devices found. Make sure your MCP server is running and devices.json is configured.';
                } else if (status.config_count === 0) {
                    msg.textContent = `Found ${status.device_count} devices but no configurations synced. Click "Sync All Configs" to pull live configs from your routers.`;
                } else {
                    msg.textContent = `${status.config_count}/${status.device_count} configs synced. Missing: ${status.missing_configs.join(', ')}. Click sync to complete setup.`;
                }
            }
            if (typeof lucide !== 'undefined') lucide.createIcons();
        }
    } catch (e) { /* MCP not reachable — no banner */ }
}

async function bootstrapSync() {
    const btn = document.getElementById('bootstrapSyncBtn');
    const prog = document.getElementById('bootstrapProgress');
    const progText = document.getElementById('bootstrapProgressText');
    if (btn) btn.disabled = true;
    if (prog) prog.style.display = 'block';
    if (progText) progText.textContent = 'Connecting to MCP server and pulling configs from all routers...';
    try {
        const data = await apiPost('bootstrap/sync', {});
        if (progText) progText.textContent = data.message || `Synced ${data.synced}/${data.total} configs.`;
        if (data.synced > 0) {
            // Reload everything now that we have configs
            setTimeout(async () => {
                await loadAll();
                const banner = document.getElementById('bootstrapBanner');
                if (banner && data.failed === 0) banner.style.display = 'none';
            }, 500);
        }
    } catch (e) {
        if (progText) progText.textContent = `Sync failed: ${e.message}. Check that MCP server is running.`;
    }
    if (btn) btn.disabled = false;
}

function dismissBootstrap() {
    const banner = document.getElementById('bootstrapBanner');
    if (banner) banner.style.display = 'none';
    localStorage.setItem('noc-bootstrap-dismissed', 'true');
}

// ══════════════════════════════════════════════════════════════════════════════
//  NEW FEATURE MODULES — Discovery, Traffic, Security, DNS, Capacity
// ══════════════════════════════════════════════════════════════════════════════

// ─── Shared: Populate router selects for new views ───
function populateNewViewRouters(...selectIds) {
    if (!state.topology) return;
    const opts = state.topology.nodes.map(n => `<option value="${n.id}">${n.id}</option>`).join('');
    selectIds.forEach(id => {
        const sel = document.getElementById(id);
        if (sel) sel.innerHTML = opts;
    });
}

function populateCapacitySelectors() {
    if (!state.topology) return;
    const opts = state.topology.nodes.map(n => `<option value="${n.id}">${n.id}</option>`).join('');
    ['whatifNode', 'whatifLinkSrc', 'whatifLinkDst', 'multipathSrc', 'multipathDst'].forEach(id => {
        const sel = document.getElementById(id);
        if (sel) {
            if (id === 'whatifNode') {
                sel.innerHTML = '<option value="">-- Select node --</option>' + opts;
            } else {
                sel.innerHTML = opts;
            }
        }
    });
}


// ══════════════════════════════════════════════════════════
//  AI INVESTIGATION VIEW
// ══════════════════════════════════════════════════════════

async function renderInvestigationView() {
    const container = document.getElementById('view-investigate');
    if (!container) return;

    // Check brain status
    let brainStatus = { brain_available: false, rag_available: false };
    try {
        const resp = await fetch('/api/brain/status');
        brainStatus = await resp.json();
    } catch (_) {}

    // Load investigation history
    let history = [];
    try {
        const resp = await fetch('/api/brain/history');
        history = await resp.json();
    } catch (_) {}

    const devices = state.topology ? state.topology.nodes.map(n => n.id) : [];

    container.innerHTML = `
        <div class="view-header">
            <div class="view-header-top">
                <h2>AI Investigation Center</h2>
                <button class="help-icon-btn" onclick="showViewHelp('investigate')" title="What is this view?"><i data-lucide="help-circle" class="help-icon"></i></button>
            </div>
            <div class="brain-status-pills">
                <span class="status-pill ${brainStatus.brain_available ? 'online' : 'offline'}">
                    <i data-lucide="brain" class="status-pill-icon"></i> Brain ${brainStatus.brain_available ? 'Ready' : 'Offline'}
                </span>
                <span class="status-pill ${brainStatus.rag_available ? 'online' : 'offline'}">
                    <i data-lucide="book-open" class="status-pill-icon"></i> RAG ${brainStatus.rag_available ? 'Ready' : 'Offline'}
                </span>
                <span class="status-pill ${brainStatus.reasoning_available ? 'online' : 'offline'}">
                    <i data-lucide="crosshair" class="status-pill-icon"></i> Reasoning ${brainStatus.reasoning_available ? 'Ready' : 'Offline'}
                </span>
                ${brainStatus.smart_scripts ? `<span class="status-pill info"><i data-lucide="scroll-text" class="status-pill-icon"></i> ${brainStatus.smart_scripts} Scripts</span>` : ''}
            </div>
        </div>

        <div class="investigate-grid">
            <div class="investigate-input-card card">
                <h3><i data-lucide="search" class="card-header-icon"></i> New Investigation</h3>
                <textarea id="investigateQuery" class="investigate-textarea" placeholder="Describe what you want to investigate... e.g., 'Why is PE1 BGP session to PE2 flapping?'" rows="3"></textarea>
                <div class="investigate-controls">
                    <select id="investigateMode">
                        <option value="full">Full Investigation</option>
                        <option value="quick">Quick Analysis</option>
                    </select>
                    <select id="investigateDevices" multiple>
                        ${devices.map(d => `<option value="${d}" selected>${d}</option>`).join('')}
                    </select>
                    <button class="btn-primary" onclick="startInvestigation()">
                        <i data-lucide="search" style="width:16px;height:16px"></i> Investigate
                    </button>
                </div>
                <div id="investigateResult" class="investigate-result" style="display:none"></div>
            </div>

            <div class="investigate-quick-actions card">
                <h3><i data-lucide="zap" class="card-header-icon"></i> Quick Actions</h3>
                <div id="investigateQuickActions" class="quick-actions-grid"></div>
            </div>

            <div class="investigate-history card">
                <h3><i data-lucide="clipboard-list" class="card-header-icon"></i> Recent Investigations</h3>
                <div class="history-list">
                    ${history.length === 0 ? '<p class="text-muted">No investigations yet</p>' :
                      history.map(h => `
                        <div class="history-item" onclick="loadInvestigation(${h.id})">
                            <div class="history-query">${h.query || 'Unknown'}</div>
                            <div class="history-meta">
                                <span>${h.mode || 'full'}</span>
                                <span>${h.duration_ms ? (h.duration_ms / 1000).toFixed(1) + 's' : ''}</span>
                                <span>${h.created_at || ''}</span>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `;

    if (typeof lucide !== 'undefined') lucide.createIcons();

    // Load quick actions
    try {
        const resp = await fetch('/api/ai/quick-actions', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ view: 'investigate' })
        });
        const data = await resp.json();
        const qaContainer = document.getElementById('investigateQuickActions');
        if (qaContainer && data.actions) {
            qaContainer.innerHTML = data.actions.map(a =>
                `<button class="quick-action-btn" onclick="document.getElementById('investigateQuery').value=\`${a.query}\`;startInvestigation()">
                    ${a.label}
                </button>`
            ).join('');
        }
    } catch (_) {}
}

async function startInvestigation() {
    const query = document.getElementById('investigateQuery')?.value?.trim();
    if (!query) return;
    const mode = document.getElementById('investigateMode')?.value || 'full';
    const deviceSelect = document.getElementById('investigateDevices');
    const devices = deviceSelect ? Array.from(deviceSelect.selectedOptions).map(o => o.value) : [];

    const resultDiv = document.getElementById('investigateResult');
    if (resultDiv) {
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = '<div class="loading-investigation"><div class="typing-indicator"><span></span><span></span><span></span></div> Running investigation...</div>';
    }

    try {
        const resp = await fetch('/api/brain/investigate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query, mode, devices })
        });
        const data = await resp.json();
        if (resultDiv) {
            if (data.error) {
                resultDiv.innerHTML = `<div class="investigate-error">${data.error}</div>`;
            } else {
                resultDiv.innerHTML = `
                    <div class="investigate-success">
                        <div class="investigate-meta">
                            <span class="meta-badge brain"><i data-lucide="brain" class="meta-icon"></i> ${data.engine || 'Brain'}</span>
                            <span class="meta-badge">${data.mode}</span>
                            <span class="meta-badge">${data.duration_ms ? (data.duration_ms / 1000).toFixed(1) + 's' : ''}</span>
                            <span class="meta-badge">${(data.devices || []).length} devices</span>
                        </div>
                        <div class="investigate-response">${formatChatText(data.response || 'No response')}</div>
                    </div>
                `;
            }
        }
    } catch (e) {
        if (resultDiv) resultDiv.innerHTML = `<div class="investigate-error">${e.message}</div>`;
    }
}

async function loadInvestigation(id) {
    try {
        const resp = await fetch(`/api/brain/history/${id}`);
        const data = await resp.json();
        if (data.query) {
            document.getElementById('investigateQuery').value = data.query;
        }
        const resultDiv = document.getElementById('investigateResult');
        if (resultDiv && data.response) {
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = `
                <div class="investigate-success">
                    <div class="investigate-meta">
                        <span class="meta-badge"><i data-lucide="folder" class="meta-icon"></i> Saved</span>
                        <span class="meta-badge">${data.mode || 'full'}</span>
                        <span class="meta-badge">${data.duration_ms ? (data.duration_ms / 1000).toFixed(1) + 's' : ''}</span>
                        <span class="meta-badge">${data.created_at || ''}</span>
                    </div>
                    <div class="investigate-response">${formatChatText(data.response)}</div>
                </div>
            `;
        }
    } catch (_) {}
}

// ══════════════════════════════════════════════════════════
//  NETWORK DISCOVERY
// ══════════════════════════════════════════════════════════

async function runDiscoveryScan() {
    const out = document.getElementById('discoveryOutput');
    const pre = document.getElementById('discoveryResults');
    const ai = document.getElementById('discoveryAI');
    out.style.display = 'block';
    ai.style.display = 'none';
    pre.textContent = 'Running full infrastructure scan across all routers...';
    logAuditAction('discovery', 'Running full infrastructure scan');
    try {
        const data = await apiPost('discovery/full-scan', {});
        state.lastDiscoveryData = data;
        pre.textContent = JSON.stringify(data, null, 2);
        if (typeof lucide !== 'undefined') lucide.createIcons();
    } catch (e) { pre.textContent = 'Scan failed: ' + e.message; }
}

async function discoverInterfaces() {
    const router = document.getElementById('discoveryRouter').value;
    if (!router) return;
    const out = document.getElementById('discoveryOutput');
    const pre = document.getElementById('discoveryResults');
    out.style.display = 'block';
    pre.textContent = `Discovering interfaces on ${router}...`;
    try {
        const data = await api(`discovery/interfaces/${router}`);
        state.lastDiscoveryData = data;
        pre.textContent = JSON.stringify(data, null, 2);
    } catch (e) { pre.textContent = 'Error: ' + e.message; }
}

async function discoverNeighbors() {
    const router = document.getElementById('discoveryRouter').value;
    if (!router) return;
    const out = document.getElementById('discoveryOutput');
    const pre = document.getElementById('discoveryResults');
    out.style.display = 'block';
    pre.textContent = `Discovering neighbors on ${router}...`;
    try {
        const data = await api(`discovery/neighbors/${router}`);
        state.lastDiscoveryData = data;
        pre.textContent = JSON.stringify(data, null, 2);
    } catch (e) { pre.textContent = 'Error: ' + e.message; }
}

async function discoverInterfaceDetail() {
    const router = document.getElementById('discoveryRouter').value;
    if (!router) return;
    const out = document.getElementById('discoveryOutput');
    const pre = document.getElementById('discoveryResults');
    out.style.display = 'block';
    pre.textContent = `Fetching detailed interface stats for ${router}...`;
    try {
        const data = await api(`discovery/interfaces/${router}/detail`);
        state.lastDiscoveryData = data;
        pre.textContent = JSON.stringify(data, null, 2);
    } catch (e) { pre.textContent = 'Error: ' + e.message; }
}

async function aiAnalyzeDiscovery() {
    if (!state.lastDiscoveryData) return;
    const ai = document.getElementById('discoveryAI');
    const content = document.getElementById('discoveryAIContent');
    ai.style.display = 'block';
    content.innerHTML = '<div class="loading" style="height:80px"></div>';
    logAuditAction('discovery', 'AI analyzing discovery data');
    try {
        const data = await apiPost('discovery/ai-map', { scan_data: state.lastDiscoveryData });
        content.innerHTML = formatChatText(data.analysis || 'No analysis returned');
        if (typeof lucide !== 'undefined') lucide.createIcons();
    } catch (e) { content.innerHTML = `<p style="color:var(--hpe-rose)">AI analysis failed: ${e.message}</p>`; }
}

// ══════════════════════════════════════════════════════════
//  TRAFFIC ANALYSIS
// ══════════════════════════════════════════════════════════

async function getProtocolStats() {
    const router = document.getElementById('trafficRouter').value;
    if (!router) return;
    const out = document.getElementById('trafficOutput');
    const pre = document.getElementById('trafficResults');
    out.style.display = 'block';
    document.getElementById('trafficAI').style.display = 'none';
    pre.textContent = `Fetching protocol statistics from ${router}...`;
    try {
        const data = await api(`traffic/protocol-stats/${router}`);
        state.lastTrafficData = data;
        pre.textContent = JSON.stringify(data, null, 2);
    } catch (e) { pre.textContent = 'Error: ' + e.message; }
}

async function getInterfaceCounters() {
    const router = document.getElementById('trafficRouter').value;
    if (!router) return;
    const iface = document.getElementById('trafficInterface').value;
    const out = document.getElementById('trafficOutput');
    const pre = document.getElementById('trafficResults');
    out.style.display = 'block';
    pre.textContent = `Fetching interface counters from ${router}...`;
    try {
        let url = `traffic/interface-counters/${router}`;
        if (iface) url += `?interface=${encodeURIComponent(iface)}`;
        const data = await api(url);
        state.lastTrafficData = data;
        pre.textContent = JSON.stringify(data, null, 2);
    } catch (e) { pre.textContent = 'Error: ' + e.message; }
}

async function getFlowAnalysis() {
    const router = document.getElementById('trafficRouter').value;
    if (!router) return;
    const out = document.getElementById('trafficOutput');
    const pre = document.getElementById('trafficResults');
    out.style.display = 'block';
    pre.textContent = `Analyzing traffic flows on ${router}...`;
    try {
        const data = await api(`traffic/flow-analysis/${router}`);
        state.lastTrafficData = data;
        pre.textContent = JSON.stringify(data, null, 2);
    } catch (e) { pre.textContent = 'Error: ' + e.message; }
}

async function getSessionTable() {
    const router = document.getElementById('trafficRouter').value;
    if (!router) return;
    const out = document.getElementById('trafficOutput');
    const pre = document.getElementById('trafficResults');
    out.style.display = 'block';
    pre.textContent = `Fetching active sessions from ${router}...`;
    try {
        const data = await api(`traffic/session-table/${router}`);
        state.lastTrafficData = data;
        pre.textContent = JSON.stringify(data, null, 2);
    } catch (e) { pre.textContent = 'Error: ' + e.message; }
}

async function aiAnalyzeTraffic() {
    if (!state.lastTrafficData) return;
    const aiType = document.getElementById('trafficAIType').value;
    const ai = document.getElementById('trafficAI');
    const content = document.getElementById('trafficAIContent');
    ai.style.display = 'block';
    content.innerHTML = '<div class="loading" style="height:80px"></div>';
    logAuditAction('traffic', `AI ${aiType} traffic analysis`);
    try {
        const data = await apiPost('traffic/ai-analyze', {
            traffic_data: state.lastTrafficData, type: aiType
        });
        content.innerHTML = formatChatText(data.analysis || 'No analysis returned');
        if (typeof lucide !== 'undefined') lucide.createIcons();
    } catch (e) { content.innerHTML = `<p style="color:var(--hpe-rose)">AI analysis failed: ${e.message}</p>`; }
}

// ══════════════════════════════════════════════════════════
//  SECURITY CENTER
// ══════════════════════════════════════════════════════════

async function runSecurityAudit() {
    const router = document.getElementById('securityRouter').value;
    if (!router) return;
    const out = document.getElementById('securityOutput');
    const pre = document.getElementById('securityRawData');
    const ai = document.getElementById('securityAI');
    out.style.display = 'block';
    ai.style.display = 'none';
    pre.textContent = `Running comprehensive security audit on ${router}...`;
    logAuditAction('security', `Security audit on ${router}`);
    try {
        const data = await api(`security/audit/${router}`);
        state.lastSecurityData = data;
        pre.textContent = JSON.stringify(data, null, 2);
    } catch (e) { pre.textContent = 'Error: ' + e.message; }
}

async function runThreatCheck() {
    const router = document.getElementById('securityRouter').value;
    if (!router) return;
    const ai = document.getElementById('securityAI');
    const content = document.getElementById('securityAIContent');
    const out = document.getElementById('securityOutput');
    out.style.display = 'none';
    ai.style.display = 'block';
    content.innerHTML = '<div class="loading" style="height:120px"></div>';
    logAuditAction('security', `Threat detection scan on ${router}`);
    try {
        const data = await apiPost('security/threat-check', { router });
        content.innerHTML = formatChatText(data.threat_analysis || 'No analysis returned');
        // Also show raw data
        if (data.raw_data) {
            const out2 = document.getElementById('securityOutput');
            const pre = document.getElementById('securityRawData');
            out2.style.display = 'block';
            pre.textContent = JSON.stringify(data.raw_data, null, 2);
        }
        if (typeof lucide !== 'undefined') lucide.createIcons();
    } catch (e) { content.innerHTML = `<p style="color:var(--hpe-rose)">Threat check failed: ${e.message}</p>`; }
}

async function runHardeningReport() {
    const router = document.getElementById('securityRouter').value;
    if (!router) return;
    const ai = document.getElementById('securityAI');
    const content = document.getElementById('securityAIContent');
    ai.style.display = 'block';
    content.innerHTML = '<div class="loading" style="height:120px"></div>';
    logAuditAction('security', `CIS hardening report for ${router}`);
    try {
        const data = await apiPost('security/hardening-report', { router });
        content.innerHTML = formatChatText(data.hardening_report || 'No report returned');
        if (typeof lucide !== 'undefined') lucide.createIcons();
    } catch (e) { content.innerHTML = `<p style="color:var(--hpe-rose)">Hardening report failed: ${e.message}</p>`; }
}

async function runCredentialScan() {
    const ai = document.getElementById('securityAI');
    const content = document.getElementById('securityAIContent');
    ai.style.display = 'block';
    content.innerHTML = '<div class="loading" style="height:120px"></div>';
    logAuditAction('security', 'Credential scan across all routers');
    try {
        const data = await apiPost('security/credential-scan', {});
        content.innerHTML = formatChatText(data.analysis || 'No analysis returned');
        if (typeof lucide !== 'undefined') lucide.createIcons();
    } catch (e) { content.innerHTML = `<p style="color:var(--hpe-rose)">Credential scan failed: ${e.message}</p>`; }
}

async function runProtocolHealthCheck() {
    const out = document.getElementById('securityOutput');
    const pre = document.getElementById('securityRawData');
    out.style.display = 'block';
    pre.textContent = 'Running protocol health check across all routers...';
    logAuditAction('security', 'Protocol health check');
    try {
        const data = await api('monitor/protocol-health');
        pre.textContent = JSON.stringify(data, null, 2);
    } catch (e) { pre.textContent = 'Error: ' + e.message; }
}

// ══════════════════════════════════════════════════════════
//  DNS DIAGNOSTICS
// ══════════════════════════════════════════════════════════

async function dnsLookup() {
    const router = document.getElementById('dnsRouter').value;
    const domain = document.getElementById('dnsDomain').value;
    if (!router || !domain) return;
    const out = document.getElementById('dnsOutput');
    const pre = document.getElementById('dnsResults');
    out.style.display = 'block';
    document.getElementById('dnsAI').style.display = 'none';
    pre.textContent = `Performing DNS lookup for ${domain} from ${router}...`;
    logAuditAction('dns', `DNS lookup: ${domain} via ${router}`);
    try {
        const data = await api(`dns/lookup/${router}?domain=${encodeURIComponent(domain)}`);
        pre.textContent = JSON.stringify(data, null, 2);
    } catch (e) { pre.textContent = 'Error: ' + e.message; }
}

async function dnsReverseLookup() {
    const router = document.getElementById('dnsReverseRouter').value;
    const ip = document.getElementById('dnsReverseIP').value;
    if (!router || !ip) return;
    const out = document.getElementById('dnsOutput');
    const pre = document.getElementById('dnsResults');
    out.style.display = 'block';
    pre.textContent = `Performing reverse DNS for ${ip} from ${router}...`;
    logAuditAction('dns', `Reverse DNS: ${ip} via ${router}`);
    try {
        const data = await api(`dns/reverse/${router}?ip=${encodeURIComponent(ip)}`);
        pre.textContent = JSON.stringify(data, null, 2);
    } catch (e) { pre.textContent = 'Error: ' + e.message; }
}

async function dnsBatchLookup() {
    const router = document.getElementById('dnsBatchRouter').value;
    const domainsStr = document.getElementById('dnsBatchDomains').value;
    if (!router || !domainsStr) return;
    const domains = domainsStr.split(',').map(d => d.trim()).filter(d => d);
    const out = document.getElementById('dnsOutput');
    const pre = document.getElementById('dnsResults');
    out.style.display = 'block';
    pre.textContent = `Batch DNS lookup: ${domains.length} domains from ${router}...`;
    logAuditAction('dns', `Batch DNS: ${domains.length} domains`);
    try {
        const data = await apiPost('dns/batch', { router, domains });
        pre.textContent = JSON.stringify(data, null, 2);
    } catch (e) { pre.textContent = 'Error: ' + e.message; }
}

async function dnsConfigAudit() {
    const ai = document.getElementById('dnsAI');
    const content = document.getElementById('dnsAIContent');
    ai.style.display = 'block';
    content.innerHTML = '<div class="loading" style="height:120px"></div>';
    logAuditAction('dns', 'AI DNS config audit across all routers');
    try {
        const data = await apiPost('dns/config-audit', {});
        content.innerHTML = formatChatText(data.analysis || 'No analysis returned');
        // Also show raw configs
        if (data.configs) {
            const out = document.getElementById('dnsOutput');
            const pre = document.getElementById('dnsResults');
            out.style.display = 'block';
            pre.textContent = JSON.stringify(data.configs, null, 2);
        }
        if (typeof lucide !== 'undefined') lucide.createIcons();
    } catch (e) { content.innerHTML = `<p style="color:var(--hpe-rose)">DNS audit failed: ${e.message}</p>`; }
}

// ══════════════════════════════════════════════════════════
//  CAPACITY PLANNING & WHAT-IF
// ══════════════════════════════════════════════════════════

async function runWhatIf() {
    const node = document.getElementById('whatifNode').value;
    const linkSrc = document.getElementById('whatifLinkSrc').value;
    const linkDst = document.getElementById('whatifLinkDst').value;
    const body = {};
    if (node) body.failed_node = node;
    else if (linkSrc && linkDst) body.failed_link = { source: linkSrc, target: linkDst };
    else return;
    const out = document.getElementById('capacityOutput');
    const pre = document.getElementById('capacityRawResults');
    const ai = document.getElementById('capacityAI');
    const content = document.getElementById('capacityAIContent');
    out.style.display = 'block';
    pre.textContent = 'Simulating failure...';
    logAuditAction('capacity', `What-if: ${node || `${linkSrc}-${linkDst}`}`);
    try {
        const data = await apiPost('path/what-if', body);
        pre.textContent = JSON.stringify(data.impact, null, 2);
        if (data.ai_analysis) {
            ai.style.display = 'block';
            content.innerHTML = formatChatText(data.ai_analysis);
            if (typeof lucide !== 'undefined') lucide.createIcons();
        }
    } catch (e) { pre.textContent = 'Error: ' + e.message; }
}

async function runMultiPath() {
    const src = document.getElementById('multipathSrc').value;
    const dst = document.getElementById('multipathDst').value;
    if (!src || !dst) return;
    const out = document.getElementById('capacityOutput');
    const pre = document.getElementById('capacityRawResults');
    out.style.display = 'block';
    document.getElementById('capacityAI').style.display = 'none';
    pre.textContent = `Computing all paths from ${src} to ${dst}...`;
    logAuditAction('capacity', `Multi-path: ${src} -> ${dst}`);
    try {
        const data = await apiPost('path/multi-algorithm', { source: src, target: dst });
        let text = `Dijkstra Shortest Path:\n  Path: ${(data.algorithms?.dijkstra?.path || []).join(' -> ')}\n  Cost: ${data.algorithms?.dijkstra?.cost || 'N/A'}\n\n`;
        text += `K-Shortest Paths:\n`;
        (data.algorithms?.k_shortest || []).forEach((p, i) => {
            text += `  [${i+1}] ${p.path.join(' -> ')}  (cost: ${p.cost})\n`;
        });
        text += `\nTopology: ${data.topology_stats?.nodes || 0} nodes, ${data.topology_stats?.links || 0} links`;
        if (data.topology_stats?.spof?.length) {
            text += `\nSingle Points of Failure: ${data.topology_stats.spof.join(', ')}`;
        }
        pre.textContent = text;
    } catch (e) { pre.textContent = 'Error: ' + e.message; }
}

async function runCapacityPlan() {
    const ai = document.getElementById('capacityAI');
    const content = document.getElementById('capacityAIContent');
    ai.style.display = 'block';
    content.innerHTML = '<div class="loading" style="height:120px"></div>';
    logAuditAction('capacity', 'AI capacity plan generation');
    try {
        const data = await apiPost('path/capacity-plan', {});
        content.innerHTML = formatChatText(data.capacity_plan || 'No plan returned');
        // Show stats
        if (data.stats) {
            const out = document.getElementById('capacityOutput');
            const pre = document.getElementById('capacityRawResults');
            out.style.display = 'block';
            pre.textContent = JSON.stringify(data.stats, null, 2);
        }
        if (typeof lucide !== 'undefined') lucide.createIcons();
    } catch (e) { content.innerHTML = `<p style="color:var(--hpe-rose)">Capacity plan failed: ${e.message}</p>`; }
}

// ═══════════════════════════════════════
//  Phase 2 — Tool Call Viz + Confidence
// ═══════════════════════════════════════

function renderToolCallCards(data) {
    const devices = data.devices_checked || [];
    const duration = data.duration_ms ? `${(data.duration_ms/1000).toFixed(1)}s` : '';
    let html = '<div class="tool-call-cards">';
    html += '<div class="tool-call-header"><i data-lucide="wrench" style="width:14px;height:14px"></i> Tool Calls Executed</div>';
    html += '<div class="tool-call-grid">';
    for (const dev of devices.slice(0, 8)) {
        html += `<div class="tool-call-card">
            <div class="tool-card-icon"><i data-lucide="server" style="width:14px;height:14px"></i></div>
            <div class="tool-card-info">
                <div class="tool-card-device">${escapeHtml(dev)}</div>
                <div class="tool-card-status">Probed</div>
            </div>
        </div>`;
    }
    if (devices.length > 8) {
        html += `<div class="tool-call-card more">+${devices.length - 8} more</div>`;
    }
    html += '</div>';
    if (duration) html += `<div class="tool-call-duration">Total: ${duration}</div>`;
    html += '</div>';
    return html;
}

async function fetchConfidenceBadge(data) {
    try {
        const resp = await fetch('/api/ai/confidence-score', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                type: data.type || 'general',
                response: (data.response || '').substring(0, 1000),
                sources: data.sources || [],
                devices_checked: data.devices_checked || []
            })
        });
        const score = await resp.json();
        // Insert confidence badge into the last AI message
        const messages = document.querySelectorAll('.chat-message.ai .msg-bubble');
        const lastMsg = messages[messages.length - 1];
        if (lastMsg) {
            const badgeClass = score.level === 'high' ? 'confidence-high' :
                               score.level === 'medium' ? 'confidence-medium' : 'confidence-low';
            const badge = document.createElement('div');
            badge.className = `confidence-badge ${badgeClass}`;
            badge.innerHTML = `<span class="confidence-score">${score.score}%</span> confidence`;
            badge.title = score.factors?.join(', ') || '';
            // Insert after meta badges if they exist, else prepend
            const metaBadges = lastMsg.querySelector('.chat-meta-badges');
            if (metaBadges) {
                metaBadges.appendChild(badge);
            } else {
                lastMsg.insertBefore(badge, lastMsg.firstChild);
            }
        }
    } catch (_) { /* confidence scoring unavailable */ }
}

// ─── Copilot Proactive Suggestions ───
async function loadCopilotSuggestions(view) {
    const container = document.getElementById('copilotSuggestionsBody');
    if (!container) return;

    container.innerHTML = '<div class="copilot-typing"><span></span><span></span><span></span></div>';

    try {
        const resp = await fetch('/api/ai/copilot-suggest', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                view,
                context: { last_query: state.lastQueryContext?.query || '' }
            })
        });
        const data = await resp.json();
        const suggestions = data.suggestions || [];

        if (!suggestions.length) {
            container.innerHTML = '<div class="suggestion-empty">No suggestions right now.</div>';
            return;
        }

        container.innerHTML = suggestions.map(s => {
            const typeClass = s.type === 'warning' ? 'warning' : (s.type === 'info' ? 'info' : 'suggestion');
            return `<div class="copilot-suggestion ${typeClass}" onclick="runQuickInvestigation(\`${escapeHtml(s.action)}\`); toggleAICopilot();">
                <div class="suggestion-icon"><i data-lucide="${s.icon || 'lightbulb'}" style="width:14px;height:14px"></i></div>
                <div class="suggestion-content">
                    <div class="suggestion-title">${escapeHtml(s.title)}</div>
                    <div class="suggestion-desc">${escapeHtml(s.description)}</div>
                </div>
            </div>`;
        }).join('');
        if (typeof lucide !== 'undefined') lucide.createIcons();
    } catch (e) {
        container.innerHTML = '<div class="suggestion-empty">Suggestions unavailable</div>';
    }
}

// ═══════════════════════════════════════
//  Phase 3 — Remediation Dashboard
// ═══════════════════════════════════════

function renderRemediationView() {
    const el = document.getElementById('view-remediate');
    if (!el) return;

    el.innerHTML = `
        <div class="view-header">
            <div class="view-header-top">
                <h2>Remediation Center</h2>
                <button class="help-icon-btn" onclick="showViewHelp('remediate')" title="What is this view?"><i data-lucide="help-circle" class="help-icon"></i></button>
            </div>
            <p class="view-subtitle">AI-powered fix proposals with approval gates — Nothing executes without your approval</p>
        </div>
        <div class="remediation-layout">
            <div class="card remediation-propose-card">
                <div class="card-header"><h3><i data-lucide="wrench" class="card-header-icon"></i> Propose Remediation</h3></div>
                <div class="card-body">
                    <div class="form-group">
                        <label>Issue Description</label>
                        <textarea id="remIssue" rows="3" placeholder="Describe the issue to fix (e.g., 'PE1 is missing IS-IS authentication')..." style="width:100%;padding:10px;background:var(--bg-input);border:1px solid var(--border-default);border-radius:var(--radius-sm);color:var(--text-primary);font-family:var(--font-sans);resize:vertical;"></textarea>
                    </div>
                    <div class="form-group">
                        <label>Target Router (optional)</label>
                        <select id="remRouter" style="padding:8px 12px;background:var(--bg-input);border:1px solid var(--border-default);border-radius:var(--radius-sm);color:var(--text-primary);">
                            <option value="">-- Auto-detect --</option>
                        </select>
                    </div>
                    <button class="btn-primary" onclick="proposeRemediation()" style="margin-top:8px;width:100%;">
                        <i data-lucide="sparkles" class="btn-icon"></i> Generate AI Remediation
                    </button>
                </div>
            </div>
            <div class="card">
                <div class="card-header">
                    <h3><i data-lucide="clipboard-list" class="card-header-icon"></i> Remediation Queue</h3>
                    <button class="btn-primary btn-deploy" onclick="loadRemediations()"><i data-lucide="refresh-cw" class="btn-icon"></i> Refresh</button>
                </div>
                <div class="card-body" id="remediationList">
                    <div class="empty-state"><p>Loading remediations...</p></div>
                </div>
            </div>
        </div>
        <div class="card" id="remDetailCard" style="display:none;">
            <div class="card-header"><h3 id="remDetailTitle">Remediation Details</h3></div>
            <div class="card-body" id="remDetailBody"></div>
        </div>
    `;

    // Populate router selector
    if (state.topology) {
        const sel = document.getElementById('remRouter');
        state.topology.nodes.forEach(n => {
            sel.innerHTML += `<option value="${n.id}">${n.id}</option>`;
        });
    }
    loadRemediations();
    if (typeof lucide !== 'undefined') lucide.createIcons();
}

async function proposeRemediation() {
    const issue = document.getElementById('remIssue')?.value?.trim();
    const router = document.getElementById('remRouter')?.value || '';
    if (!issue) return alert('Please describe the issue to fix.');

    const btn = event.target.closest('button');
    btn.disabled = true;
    btn.innerHTML = '<div class="loading" style="height:18px;width:18px;display:inline-block"></div> Generating...';

    try {
        const data = await apiPost('remediate/propose', { issue, router });
        if (data.error) { alert(data.error); return; }
        document.getElementById('remIssue').value = '';
        showRemediationDetail(data);
        loadRemediations();
        logAuditAction('ai', `AI remediation proposed: ${data.title}`);
    } catch (e) {
        alert('Failed to generate remediation: ' + e.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i data-lucide="sparkles" class="btn-icon"></i> Generate AI Remediation';
        if (typeof lucide !== 'undefined') lucide.createIcons();
    }
}

async function loadRemediations() {
    try {
        const data = await api('remediate/list');
        state.remediations = data;
        const el = document.getElementById('remediationList');
        if (!el) return;
        if (!data.length) {
            el.innerHTML = '<div class="empty-state"><p>No remediation proposals yet. Describe an issue above to get AI-generated fix commands.</p></div>';
            return;
        }
        el.innerHTML = data.map(r => {
            const statusColors = { pending: 'var(--hpe-amber)', approved: 'var(--hpe-blue)', executed: 'var(--hpe-green)', rejected: 'var(--text-tertiary)', failed: 'var(--hpe-rose)' };
            const riskColors = { low: 'var(--hpe-green)', medium: 'var(--hpe-amber)', high: 'var(--hpe-rose)' };
            return `<div class="remediation-item" onclick="viewRemediation(${r.id})">
                <div class="rem-status-dot" style="background:${statusColors[r.status] || 'var(--text-tertiary)'}"></div>
                <div class="rem-info">
                    <div class="rem-title">${escapeHtml(r.title)}</div>
                    <div class="rem-meta">
                        <span class="rem-router">${r.target_router || 'N/A'}</span>
                        <span class="rem-risk" style="color:${riskColors[r.risk_level] || ''}">● ${r.risk_level}</span>
                        <span class="rem-time">${new Date(r.created_at).toLocaleString()}</span>
                    </div>
                </div>
                <span class="rem-status-badge" style="color:${statusColors[r.status] || ''}">${r.status}</span>
            </div>`;
        }).join('');
    } catch (_) {}
}

async function viewRemediation(id) {
    try {
        const data = await api(`remediate/${id}`);
        showRemediationDetail(data);
    } catch (e) { alert('Failed to load: ' + e.message); }
}

function showRemediationDetail(data) {
    const card = document.getElementById('remDetailCard');
    const title = document.getElementById('remDetailTitle');
    const body = document.getElementById('remDetailBody');
    if (!card || !body) return;
    card.style.display = '';
    title.textContent = data.title || 'Remediation Details';

    const commands = Array.isArray(data.commands) ? data.commands : [];
    const rollback = Array.isArray(data.rollback_commands) ? data.rollback_commands : [];
    const riskClass = data.risk_level === 'high' ? 'hpe-rose' : (data.risk_level === 'medium' ? 'hpe-amber' : 'hpe-green');

    body.innerHTML = `
        <div class="rem-detail-meta">
            <span class="meta-badge ${data.risk_level === 'high' ? 'warning' : (data.risk_level === 'medium' ? 'quick' : 'config')}">
                Risk: ${data.risk_level || 'unknown'}
            </span>
            <span class="meta-badge info">Status: ${data.status || 'pending'}</span>
            ${data.target_router ? `<span class="meta-badge devices">Router: ${data.target_router}</span>` : ''}
        </div>
        ${data.impact ? `<p class="rem-impact"><strong>Impact:</strong> ${escapeHtml(data.impact)}</p>` : ''}
        <div class="rem-commands-section">
            <h4>Commands to Apply (${commands.length})</h4>
            <pre class="config-pre">${commands.map(c => escapeHtml(c)).join('\n') || 'None'}</pre>
        </div>
        <div class="rem-commands-section">
            <h4>Rollback Commands (${rollback.length})</h4>
            <pre class="config-pre">${rollback.map(c => escapeHtml(c)).join('\n') || 'None'}</pre>
        </div>
        ${data.status === 'pending' ? `
            <div class="rem-actions">
                <button class="btn-primary" onclick="approveRemediation(${data.id})" style="flex:1"><i data-lucide="check-circle" class="btn-icon"></i> Approve</button>
                <button class="btn-primary" onclick="rejectRemediation(${data.id})" style="flex:1;background:var(--hpe-rose)"><i data-lucide="x-circle" class="btn-icon"></i> Reject</button>
            </div>
        ` : ''}
        ${data.status === 'approved' ? `
            <div class="rem-actions">
                <button class="btn-primary" onclick="executeRemediation(${data.id})" style="flex:1;background:var(--hpe-purple)">
                    <i data-lucide="play" class="btn-icon"></i> Execute on ${data.target_router || 'Router'}
                </button>
            </div>
        ` : ''}
        ${data.result ? `<div class="rem-result"><h4>Execution Result</h4><pre class="config-pre">${escapeHtml(String(data.result))}</pre></div>` : ''}
    `;
    if (typeof lucide !== 'undefined') lucide.createIcons();
    card.scrollIntoView({ behavior: 'smooth' });
}

async function approveRemediation(id) {
    if (!confirm('Approve this remediation for execution?')) return;
    try {
        await apiPost(`remediate/${id}/approve`, {});
        logAuditAction('validate', `Approved remediation #${id}`);
        viewRemediation(id);
        loadRemediations();
    } catch (e) { alert(e.message); }
}

async function rejectRemediation(id) {
    if (!confirm('Reject this remediation?')) return;
    try {
        await apiPost(`remediate/${id}/reject`, {});
        logAuditAction('warning', `Rejected remediation #${id}`);
        viewRemediation(id);
        loadRemediations();
    } catch (e) { alert(e.message); }
}

async function executeRemediation(id) {
    if (!confirm('EXECUTE this remediation on the live router? This cannot be undone automatically.')) return;
    try {
        const data = await apiPost(`remediate/${id}/execute`, {});
        logAuditAction('deploy', `Executed remediation #${id} on ${data.router}`);
        viewRemediation(id);
        loadRemediations();
    } catch (e) { alert('Execution failed: ' + e.message); }
}

// ═══════════════════════════════════════
//  Phase 4 — Predictive + Ensemble
// ═══════════════════════════════════════

function renderPredictiveView() {
    const el = document.getElementById('view-predictive');
    if (!el) return;

    el.innerHTML = `
        <div class="view-header">
            <div class="view-header-top">
                <h2>Predictive Intelligence</h2>
                <button class="help-icon-btn" onclick="showViewHelp('predictive')" title="What is this view?"><i data-lucide="help-circle" class="help-icon"></i></button>
            </div>
            <p class="view-subtitle">AI failure prediction &amp; multi-model ensemble analysis</p>
        </div>
        <div class="dashboard-grid" style="grid-template-columns: 1fr 1fr;">
            <div class="card">
                <div class="card-header">
                    <h3><i data-lucide="trending-up" class="card-header-icon"></i> Predictive Failure Analysis</h3>
                    <button class="btn-primary btn-deploy" onclick="runPrediction()"><i data-lucide="trending-up" class="btn-icon"></i> Run Prediction</button>
                </div>
                <div class="card-body" id="predictionResult">
                    <p class="text-muted">AI analyzes investigation history and current network state to predict potential failures before they happen.</p>
                </div>
            </div>
            <div class="card">
                <div class="card-header">
                    <h3><i data-lucide="users" class="card-header-icon"></i> Multi-Model Ensemble</h3>
                </div>
                <div class="card-body">
                    <div class="form-group">
                        <label>Question for Ensemble</label>
                        <textarea id="ensembleQuestion" rows="3" placeholder="Ask a complex question — multiple AI models will analyze and vote on the answer..." style="width:100%;padding:10px;background:var(--bg-input);border:1px solid var(--border-default);border-radius:var(--radius-sm);color:var(--text-primary);font-family:var(--font-sans);resize:vertical;"></textarea>
                    </div>
                    <button class="btn-primary" onclick="runEnsemble()" style="width:100%;margin-top:8px;">
                        <i data-lucide="users" class="btn-icon"></i> Query Ensemble
                    </button>
                </div>
            </div>
        </div>
        <div class="card" id="ensembleResultCard" style="display:none;">
            <div class="card-header"><h3>Ensemble Results</h3></div>
            <div class="card-body" id="ensembleResult"></div>
        </div>
    `;
    if (typeof lucide !== 'undefined') lucide.createIcons();
}

async function runPrediction() {
    const el = document.getElementById('predictionResult');
    if (!el) return;
    el.innerHTML = '<div class="loading" style="height:120px"></div>';

    try {
        const data = await apiPost('brain/predict', { scope: 'all' });
        if (data.error) { el.innerHTML = `<p style="color:var(--hpe-rose)">${data.error}</p>`; return; }

        el.innerHTML = `
            <div class="prediction-meta">
                <span class="meta-badge brain"><i data-lucide="trending-up" class="meta-icon"></i> Predictive AI</span>
                <span class="meta-badge devices">${data.network_size} devices</span>
                <span class="meta-badge info">${data.history_entries} history entries</span>
                ${data.spofs?.length ? `<span class="meta-badge warning"><i data-lucide="alert-triangle" class="meta-icon"></i> ${data.spofs.length} SPOFs</span>` : ''}
            </div>
            <div class="ai-analysis-content" style="margin-top:12px;">${formatChatText(data.prediction || 'No prediction available')}</div>
        `;
        if (typeof lucide !== 'undefined') lucide.createIcons();
        logAuditAction('ai', 'Ran predictive failure analysis');
    } catch (e) {
        el.innerHTML = `<p style="color:var(--hpe-rose)">Prediction failed: ${e.message}</p>`;
    }
}

async function runEnsemble() {
    const question = document.getElementById('ensembleQuestion')?.value?.trim();
    if (!question) return alert('Enter a question for the ensemble.');

    const card = document.getElementById('ensembleResultCard');
    const el = document.getElementById('ensembleResult');
    card.style.display = '';
    el.innerHTML = '<div class="loading" style="height:120px"></div>';

    try {
        const data = await apiPost('ai/ensemble', { question, context: '' });
        if (data.error) { el.innerHTML = `<p style="color:var(--hpe-rose)">${data.error}</p>`; return; }

        const results = data.all_results || [];
        let modelsHtml = results.map(r => {
            const cls = r.success ? (r.confidence >= 80 ? 'confidence-high' : (r.confidence >= 60 ? 'confidence-medium' : 'confidence-low')) : 'confidence-low';
            const isConsensus = r.model === data.consensus_model;
            return `<div class="ensemble-model-card ${isConsensus ? 'consensus' : ''}">
                <div class="ensemble-model-header">
                    <span class="ensemble-model-name">${escapeHtml(r.model)}</span>
                    ${isConsensus ? '<span class="meta-badge config"><i data-lucide="award" class="meta-icon"></i> Consensus</span>' : ''}
                    <span class="confidence-badge ${cls}">${r.confidence}%</span>
                </div>
                <div class="ensemble-model-answer">${r.success ? formatChatText(r.answer.substring(0, 500)) : `<span style="color:var(--hpe-rose)">Failed: ${escapeHtml(r.answer)}</span>`}</div>
            </div>`;
        }).join('');

        el.innerHTML = `
            <div class="ensemble-summary">
                <span class="meta-badge brain"><i data-lucide="users" class="meta-icon"></i> Ensemble Consensus</span>
                <span class="meta-badge devices">${data.models_succeeded}/${data.models_queried} models</span>
                <span class="confidence-badge ${data.average_confidence >= 80 ? 'confidence-high' : (data.average_confidence >= 60 ? 'confidence-medium' : 'confidence-low')}">
                    Avg: ${data.average_confidence}%
                </span>
            </div>
            <div class="ensemble-consensus-answer" style="margin:16px 0;">
                ${formatChatText(data.consensus || '')}
            </div>
            <h4 style="margin:16px 0 8px;color:var(--text-secondary);font-size:0.85rem;">Individual Model Responses</h4>
            <div class="ensemble-models-grid">${modelsHtml}</div>
        `;
        if (typeof lucide !== 'undefined') lucide.createIcons();
        logAuditAction('ai', `Ensemble query: ${question.substring(0, 50)}...`);
    } catch (e) {
        el.innerHTML = `<p style="color:var(--hpe-rose)">Ensemble failed: ${e.message}</p>`;
    }
}

// ─── Helper: POST to API ───
async function apiPost(path, body) {
    const resp = await fetch(`/api/${path}`, {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(body)
    });
    if (!resp.ok) throw new Error(`${resp.status} ${resp.statusText}`);
    return resp.json();
}

// ═══════════════════════════════════════
//  UTILITY — escapeHtml (XSS prevention)
// ═══════════════════════════════════════
function escapeHtml(str) {
    if (str == null) return '';
    const s = String(str);
    const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
    return s.replace(/[&<>"']/g, c => map[c]);
}
