#!/usr/bin/env python3
"""
Knowledge Base Vector Store v2.0 — Enhanced RAG Engine for Junos AI Brain

Chunks the KNOWLEDGE_BASE.md into semantic sections, embeds them using
a local Ollama embedding model, stores vectors in a local pickle file,
and provides semantic retrieval at query time.

v2.0 Enhancements over v1.0:
  - Heading-anchored embeddings: each chunk is embedded with its section/heading
    prefix so the embedding model knows what the chunk is ABOUT
  - Multi-query retrieval: generates 2-3 query variants and merges results
    with deduplication for better recall
  - Minimum score threshold: filters out low-relevance noise (default 0.55)
  - Section-aware keyword boosting: protocol keyword in query + section title
    gets a score boost for more accurate retrieval

Architecture:
  1. CHUNK: Split KB into ~200-400 token chunks by section/subsection
  2. ANCHOR: Prepend section + heading context to each chunk before embedding
  3. EMBED: Use nomic-embed-text via Ollama API to vectorize each anchored chunk
  4. STORE: Save embeddings + metadata to .pkl file (auto-rebuilds on KB change)
  5. RETRIEVE: Multi-query embed → cosine similarity + keyword boost → threshold → top-K

Usage:
  from kb_vectorstore import KBVectorStore
  store = await KBVectorStore.create()       # builds/loads automatically
  chunks = await store.retrieve("BGP flap", top_k=5)  # semantic search
"""

import os
import re
import json
import time
import pickle
import hashlib
import asyncio
import numpy as np
import httpx

# ── Configuration ────────────────────────────────────────────
OLLAMA_URL = "http://127.0.0.1:11434"
EMBED_MODEL = "nomic-embed-text"           # 274MB, 768-dim, fast
KB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "KNOWLEDGE_BASE.md")
VECTOR_STORE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kb_vectors.pkl")

# Chunking parameters
MIN_CHUNK_CHARS = 100       # Skip chunks smaller than this
MAX_CHUNK_CHARS = 2000      # Split chunks larger than this
OVERLAP_CHARS = 150         # Overlap between split chunks for context continuity

# v2.0 Retrieval parameters
MIN_RELEVANCE_SCORE = 0.55  # Filter out chunks below this cosine similarity
KEYWORD_BOOST = 0.12        # Score boost when query keyword matches section name
STORE_VERSION = "2.0"       # Cache version — forces rebuild on version change

# Protocol keyword map for section-aware boosting (Enhancement D)
PROTOCOL_KEYWORDS = {
    "ospf": ["ospf", "adjacency", "neighbor", "lsa", "area", "dr", "bdr", "spf", "hello"],
    "bgp": ["bgp", "ibgp", "ebgp", "as-path", "local-pref", "med", "route-reflect", "confederation"],
    "ldp": ["ldp", "label", "fec", "session-protection", "igp-sync"],
    "mpls": ["mpls", "rsvp", "lsp", "label-switch", "fast-reroute", "frr", "bypass", "cspf", "traffic-engineering", "mpls-te"],
    "isis": ["isis", "is-is", "net", "level-1", "level-2", "pdu", "tlv"],
    "evpn": ["evpn", "evi", "esi", "ethernet-segment", "multihom", "mac-mobility", "route-type", "layer 2 vpn and evpn"],
    "vpls": ["vpls", "pseudowire", "split-horizon", "mac-learn"],
    "l3vpn": ["l3vpn", "l3 vpn", "layer 3 vpn", "vrf", "vpn-ipv4", "route-distinguisher", "route-target", "mp-bgp", "inter-as"],
    "l2vpn": ["l2vpn", "l2 vpn", "layer 2 vpn", "l2circuit", "pseudowire", "virtual-circuit"],
    "cos": ["cos", "class-of-service", "dscp", "scheduler", "forwarding-class", "policer"],
    "firewall": ["firewall", "filter", "protect-re", "policer", "discard", "reject"],
    "vrrp": ["vrrp", "virtual-router", "preempt", "priority"],
    "stp": ["stp", "rstp", "mstp", "spanning-tree", "bpdu", "root-bridge"],
    "lag": ["lag", "lacp", "ae", "aggregated", "bundle"],
    "ha": ["gres", "nsr", "issu", "nonstop", "graceful", "redundancy"],
    "segment-routing": ["segment-routing", "spring", "sid", "srgb", "node-segment"],
    "multicast": ["multicast", "pim", "igmp", "rendezvous", "rp", "mvpn"],
    "tunnel": ["gre", "ipsec", "tunnel", "ip-ip", "ike"],
}


# ══════════════════════════════════════════════════════════════
#  CHUNKING ENGINE
# ══════════════════════════════════════════════════════════════

def chunk_knowledge_base(kb_text: str) -> list[dict]:
    """
    Split the knowledge base into semantically meaningful chunks.
    
    Strategy:
    - Split on ## headings (subsections) as primary boundaries
    - Each chunk gets metadata: section_id, heading, source
    - Large chunks get further split with overlap
    - Tiny chunks get merged with their parent
    
    Returns list of dicts: [{text, heading, section, chunk_id}, ...]
    """
    chunks = []
    
    # First, identify all sections and subsections
    lines = kb_text.split('\n')
    current_section = "Preamble"
    current_heading = "Introduction"
    current_lines = []
    
    for line in lines:
        # Top-level section (# SECTION ...)
        if re.match(r'^# SECTION \d+', line):
            # Save previous chunk
            if current_lines:
                _add_chunk(chunks, current_lines, current_section, current_heading)
            current_section = line.strip('# \n')
            current_heading = current_section
            current_lines = [line]
        # Subsection (## ...)
        elif re.match(r'^## ', line):
            # Save previous chunk
            if current_lines:
                _add_chunk(chunks, current_lines, current_section, current_heading)
            current_heading = line.strip('# \n')
            current_lines = [line]
        # Sub-subsection (### ...) — start new chunk but keep section context
        elif re.match(r'^### ', line):
            if current_lines:
                _add_chunk(chunks, current_lines, current_section, current_heading)
            sub_heading = line.strip('# \n')
            current_heading = sub_heading
            current_lines = [line]
        else:
            current_lines.append(line)
    
    # Don't forget the last chunk
    if current_lines:
        _add_chunk(chunks, current_lines, current_section, current_heading)
    
    # Post-process: split large chunks, merge tiny ones
    processed = []
    for chunk in chunks:
        text = chunk['text']
        if len(text) < MIN_CHUNK_CHARS:
            # Merge with previous chunk if possible
            if processed:
                processed[-1]['text'] += '\n' + text
                processed[-1]['heading'] += ' + ' + chunk['heading']
            continue
        
        if len(text) > MAX_CHUNK_CHARS:
            # Split into overlapping sub-chunks
            sub_chunks = _split_large_chunk(text, chunk, MAX_CHUNK_CHARS, OVERLAP_CHARS)
            processed.extend(sub_chunks)
        else:
            processed.append(chunk)
    
    # Assign unique IDs
    for i, chunk in enumerate(processed):
        chunk['chunk_id'] = i
    
    return processed


def _add_chunk(chunks: list, lines: list, section: str, heading: str):
    """Add a chunk from accumulated lines."""
    text = '\n'.join(lines).strip()
    if text:
        chunks.append({
            'text': text,
            'heading': heading,
            'section': section,
        })


def _split_large_chunk(text: str, parent: dict, max_size: int, overlap: int) -> list[dict]:
    """Split a large chunk into overlapping sub-chunks at paragraph boundaries."""
    paragraphs = re.split(r'\n\n+', text)
    sub_chunks = []
    current_text = ""
    part = 1
    
    for para in paragraphs:
        if len(current_text) + len(para) > max_size and current_text:
            sub_chunks.append({
                'text': current_text.strip(),
                'heading': f"{parent['heading']} (part {part})",
                'section': parent['section'],
            })
            # Start new chunk with overlap from end of previous
            overlap_text = current_text[-overlap:] if len(current_text) > overlap else current_text
            current_text = overlap_text + '\n\n' + para
            part += 1
        else:
            current_text += ('\n\n' if current_text else '') + para
    
    if current_text.strip():
        sub_chunks.append({
            'text': current_text.strip(),
            'heading': f"{parent['heading']} (part {part})" if part > 1 else parent['heading'],
            'section': parent['section'],
        })
    
    return sub_chunks


# ══════════════════════════════════════════════════════════════
#  EMBEDDING ENGINE
# ══════════════════════════════════════════════════════════════

async def embed_text(text: str, _retries: int = 3) -> np.ndarray:
    """Embed a single text using Ollama's embedding API (with retry + backoff)."""
    last_exc = None
    for attempt in range(1, _retries + 1):
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                resp = await client.post(f"{OLLAMA_URL}/api/embed", json={
                    "model": EMBED_MODEL,
                    "input": text,
                })
                data = resp.json()
                # Ollama returns {"embeddings": [[...]]}
                return np.array(data["embeddings"][0], dtype=np.float32)
        except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.TimeoutException) as exc:
            last_exc = exc
            if attempt < _retries:
                wait = 2 ** attempt  # 2s, 4s
                await asyncio.sleep(wait)
    raise last_exc  # type: ignore[misc]


async def embed_batch(texts: list[str], batch_size: int = 10, _retries: int = 3) -> list[np.ndarray]:
    """Embed multiple texts in batches for efficiency (with retry + backoff)."""
    all_embeddings = []
    total = len(texts)
    
    for i in range(0, total, batch_size):
        batch = texts[i:i + batch_size]
        last_exc = None
        for attempt in range(1, _retries + 1):
            try:
                async with httpx.AsyncClient(timeout=120.0) as client:
                    resp = await client.post(f"{OLLAMA_URL}/api/embed", json={
                        "model": EMBED_MODEL,
                        "input": batch,
                    })
                    data = resp.json()
                    for emb in data["embeddings"]:
                        all_embeddings.append(np.array(emb, dtype=np.float32))
                    break  # success — exit retry loop
            except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.TimeoutException) as exc:
                last_exc = exc
                if attempt < _retries:
                    wait = 2 ** attempt
                    await asyncio.sleep(wait)
        else:
            # All retries exhausted for this batch
            raise last_exc  # type: ignore[misc]
        
        done = min(i + batch_size, total)
        if total > batch_size:
            print(f"      ▸ Embedded {done}/{total} chunks...")
    
    return all_embeddings


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    dot = np.dot(a, b)
    norm = np.linalg.norm(a) * np.linalg.norm(b)
    if norm == 0:
        return 0.0
    return float(dot / norm)


def cosine_similarity_batch(query_vec: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    """Compute cosine similarity between query and all rows in matrix. Returns array of scores."""
    # Normalize
    query_norm = query_vec / (np.linalg.norm(query_vec) + 1e-10)
    norms = np.linalg.norm(matrix, axis=1, keepdims=True) + 1e-10
    matrix_norm = matrix / norms
    # Dot product = cosine similarity (both normalized)
    return matrix_norm @ query_norm


def _keyword_in_text(keyword: str, text: str) -> bool:
    """Check if a keyword appears in text using word-boundary matching.
    
    For multi-word keywords (e.g., 'layer 3 vpn'), use substring matching.
    For single-word keywords, use word-boundary regex to avoid false positives
    like 'te' matching 'filter' or 'structure'.
    """
    if ' ' in keyword:
        # Multi-word: simple substring is fine
        return keyword in text
    # Single word: require word boundaries
    return bool(re.search(r'\b' + re.escape(keyword) + r'\b', text))


# ══════════════════════════════════════════════════════════════
#  VECTOR STORE
# ══════════════════════════════════════════════════════════════

class KBVectorStore:
    """
    Persistent vector store for the Junos Knowledge Base.
    
    Auto-rebuilds when KNOWLEDGE_BASE.md changes (checksum-based).
    Provides semantic retrieval for any query.
    """
    
    def __init__(self):
        self.chunks: list[dict] = []           # [{text, heading, section, chunk_id}, ...]
        self.embeddings: np.ndarray = None     # (N, dim) matrix
        self.kb_hash: str = ""                 # SHA256 of the KB file
        self.embed_model: str = EMBED_MODEL
        self.store_version: str = STORE_VERSION
        self.built_at: str = ""
        self.dim: int = 0
    
    @classmethod
    async def create(cls, force_rebuild: bool = False) -> 'KBVectorStore':
        """Factory method — builds or loads the vector store."""
        store = cls()
        await store._init(force_rebuild)
        return store
    
    async def _init(self, force_rebuild: bool = False):
        """Initialize: load from cache or rebuild from KB."""
        # Check if KB exists
        if not os.path.exists(KB_PATH):
            print("   ▲  No KNOWLEDGE_BASE.md found — vector store empty")
            return
        
        # Compute current KB hash (include expert examples if present)
        with open(KB_PATH, 'r') as f:
            kb_text = f.read()
        
        # v13.0: Also include EXPERT_EXAMPLES.md in the vector store
        expert_examples_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "EXPERT_EXAMPLES.md")
        expert_text = ""
        if os.path.exists(expert_examples_path):
            with open(expert_examples_path, 'r') as f:
                expert_text = f.read()
            kb_text += "\n\n# EXPERT TROUBLESHOOTING EXAMPLES\n\n" + expert_text
        
        # v14.0: Also include JUNOS_DEEP_KNOWLEDGE.md (protocol FSMs, scripting, cascade patterns)
        deep_knowledge_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "JUNOS_DEEP_KNOWLEDGE.md")
        deep_text = ""
        if os.path.exists(deep_knowledge_path):
            with open(deep_knowledge_path, 'r') as f:
                deep_text = f.read()
            kb_text += "\n\n# JUNOS DEEP KNOWLEDGE — PROTOCOL STATE MACHINES\n\n" + deep_text
            print(f"   ⊞ Including JUNOS_DEEP_KNOWLEDGE.md: {len(deep_text)} chars")
        
        current_hash = hashlib.sha256(kb_text.encode()).hexdigest()
        
        # Try loading cached store
        if not force_rebuild and os.path.exists(VECTOR_STORE_PATH):
            try:
                self._load_cache()
                if self.kb_hash == current_hash:
                    print(f"   ● Vector store loaded from cache: {len(self.chunks)} chunks, {self.dim}-dim")
                    return
                else:
                    print("   ↻ Knowledge Base changed — rebuilding vectors...")
            except Exception as e:
                print(f"   ▲  Cache corrupted ({e}) — rebuilding...")
        else:
            print("   ▸ Building vector store for the first time...")
        
        # Rebuild
        await self._build(kb_text, current_hash)
    
    async def _build(self, kb_text: str, kb_hash: str):
        """Chunk the KB, embed all chunks with heading-anchored context, save to cache."""
        start_time = time.time()
        
        # Step 1: Chunk
        print("      ◇ Chunking knowledge base...")
        self.chunks = chunk_knowledge_base(kb_text)
        print(f"      ● Created {len(self.chunks)} chunks")
        
        # Step 2: Embed — ENHANCEMENT A: Heading-anchored embeddings
        # Prepend section + heading context to each chunk before embedding
        # so the embedding model knows WHAT the chunk is about, not just the raw text.
        # This dramatically improves retrieval for protocol-specific queries.
        print(f"      ▸ Embedding with {EMBED_MODEL} (heading-anchored v2.0)...")
        anchored_texts = []
        for c in self.chunks:
            anchor = f"Topic: {c['section']} | {c['heading']}\n\n{c['text']}"
            anchored_texts.append(anchor)
        
        embeddings = await embed_batch(anchored_texts)
        
        self.embeddings = np.stack(embeddings)
        self.dim = self.embeddings.shape[1]
        self.kb_hash = kb_hash
        self.store_version = STORE_VERSION
        self.built_at = time.strftime("%Y-%m-%d %H:%M:%S")
        
        elapsed = time.time() - start_time
        print(f"      ● Vector store built: {len(self.chunks)} chunks × {self.dim}-dim in {elapsed:.1f}s")
        
        # Step 3: Save cache
        self._save_cache()
    
    def _save_cache(self):
        """Persist the vector store to disk."""
        data = {
            'chunks': self.chunks,
            'embeddings': self.embeddings,
            'kb_hash': self.kb_hash,
            'embed_model': self.embed_model,
            'built_at': self.built_at,
            'dim': self.dim,
            'store_version': self.store_version,
        }
        with open(VECTOR_STORE_PATH, 'wb') as f:
            pickle.dump(data, f)
        size_kb = os.path.getsize(VECTOR_STORE_PATH) / 1024
        print(f"      ⊟ Cached to {VECTOR_STORE_PATH} ({size_kb:.0f} KB)")
    
    def _load_cache(self):
        """Load the vector store from disk."""
        with open(VECTOR_STORE_PATH, 'rb') as f:
            data = pickle.load(f)
        # v2.0: Check store version — force rebuild if version mismatch
        cached_version = data.get('store_version', '1.0')
        if cached_version != STORE_VERSION:
            raise ValueError(f"Store version mismatch: cached={cached_version}, current={STORE_VERSION}")
        self.chunks = data['chunks']
        self.embeddings = data['embeddings']
        self.kb_hash = data['kb_hash']
        self.embed_model = data.get('embed_model', EMBED_MODEL)
        self.built_at = data.get('built_at', 'unknown')
        self.dim = data.get('dim', self.embeddings.shape[1] if self.embeddings is not None else 0)
        self.store_version = cached_version
    
    async def retrieve(self, query: str, top_k: int = 6, min_score: float = MIN_RELEVANCE_SCORE) -> list[dict]:
        """
        Enhanced semantic retrieval with keyword boosting and score threshold.
        
        v2.0 Enhancements:
          - ENHANCEMENT C: Min-score threshold filters out noise chunks
          - ENHANCEMENT D: Section-aware keyword boost — if query contains protocol
            keywords that match a chunk's section/heading, boost the cosine score
        
        Returns list of dicts: [{text, heading, section, score, chunk_id}, ...]
        sorted by descending similarity score, filtered by min_score.
        """
        if self.embeddings is None or len(self.chunks) == 0:
            return []
        
        # Embed the query with heading-anchor format to match how chunks were embedded
        query_anchored = f"Topic: query\n\n{query}"
        query_vec = await embed_text(query_anchored)
        
        # Compute cosine similarities
        scores = cosine_similarity_batch(query_vec, self.embeddings)
        
        # ── Enhancement D: Section-aware keyword boost ──
        # Extract protocol keywords from query and boost chunks whose
        # section/heading matches those keywords
        query_lower = query.lower()
        query_words = set(re.findall(r'[a-z0-9\-]+', query_lower))
        
        boosted_scores = scores.copy()
        for idx, chunk in enumerate(self.chunks):
            chunk_section_lower = chunk.get('section', '').lower()
            chunk_heading_lower = chunk.get('heading', '').lower()
            chunk_context = chunk_section_lower + ' ' + chunk_heading_lower
            
            boost = 0.0
            # Check each protocol keyword group
            for protocol, keywords in PROTOCOL_KEYWORDS.items():
                # Does the query mention this protocol?
                # Use word boundary or substring for multi-word keywords
                query_mentions_protocol = any(
                    _keyword_in_text(kw, query_lower) for kw in keywords
                )
                if query_mentions_protocol:
                    # Does this chunk's section/heading also mention it?
                    heading_matches = any(
                        _keyword_in_text(kw, chunk_context) for kw in keywords
                    )
                    if heading_matches:
                        boost = max(boost, KEYWORD_BOOST)
                        # Extra boost if BOTH section AND heading match
                        section_match = any(
                            _keyword_in_text(kw, chunk_section_lower) for kw in keywords
                        )
                        heading_match = any(
                            _keyword_in_text(kw, chunk_heading_lower) for kw in keywords
                        )
                        if section_match and heading_match:
                            boost = max(boost, KEYWORD_BOOST * 1.5)
            
            # Direct word overlap between query and heading (at least 2 words)
            heading_words = set(re.findall(r'[a-z0-9\-]+', chunk_context))
            overlap = query_words & heading_words
            if len(overlap) >= 3:
                boost = max(boost, KEYWORD_BOOST)
            elif len(overlap) >= 2:
                boost = max(boost, KEYWORD_BOOST * 0.6)
            
            boosted_scores[idx] += boost
        
        # ── Get top candidates (more than top_k, then filter by threshold) ──
        candidate_count = min(top_k * 3, len(self.chunks))
        top_indices = np.argsort(boosted_scores)[::-1][:candidate_count]
        
        # ── Enhancement C: Min-score threshold ──
        results = []
        for idx in top_indices:
            score = float(boosted_scores[idx])
            if score < min_score:
                continue
            chunk = self.chunks[idx].copy()
            chunk['score'] = score
            chunk['raw_cosine'] = float(scores[idx])  # Original cosine without boost
            results.append(chunk)
            if len(results) >= top_k:
                break
        
        return results
    
    async def retrieve_for_protocol(self, protocol: str, context: str = "", top_k: int = 5) -> str:
        """
        Enhanced multi-query retrieval for protocol-specific analysis.
        
        v2.0 ENHANCEMENT B: Generates 2-3 query variants covering different
        aspects (troubleshooting, configuration, concepts) and merges/deduplicates
        results for better recall.
        
        Returns formatted text ready for injection into AI prompt.
        """
        # Build multiple query variants for better recall
        queries = [
            f"Junos {protocol} troubleshooting analysis diagnosis",
            f"Junos {protocol} configuration best practices commands",
        ]
        if context:
            queries.append(f"Junos {protocol} {context}")
        
        # Retrieve for each query variant
        seen_chunk_ids = set()
        merged_results = []
        
        for query in queries:
            results = await self.retrieve(query, top_k=top_k)
            for r in results:
                cid = r.get('chunk_id', id(r))
                if cid not in seen_chunk_ids:
                    seen_chunk_ids.add(cid)
                    merged_results.append(r)
        
        # Sort merged results by score descending, take top_k
        # E28: Per-protocol sub-index boost — chunks whose heading mentions
        # the target protocol get a score boost to surface protocol-specific KB
        protocol_lower = protocol.lower()
        protocol_aliases = {
            "ospf": ["ospf", "open shortest path"],
            "bgp": ["bgp", "border gateway"],
            "ldp": ["ldp", "label distribution"],
            "mpls": ["mpls", "label switching", "lsp"],
            "isis": ["is-is", "isis", "intermediate system"],
            "evpn": ["evpn", "ethernet vpn", "l2vpn", "vpls"],
            "system": ["system", "chassis", "alarm", "health", "core dump"],
            "bfd": ["bfd", "bidirectional forwarding"],
        }
        aliases = protocol_aliases.get(protocol_lower, [protocol_lower])
        
        for r in merged_results:
            heading_lower = r.get('heading', '').lower()
            text_lower = r.get('text', '')[:200].lower()
            if any(alias in heading_lower for alias in aliases):
                r['score'] = min(r['score'] * 1.25, 1.0)  # 25% boost, capped at 1.0
            elif any(alias in text_lower for alias in aliases):
                r['score'] = min(r['score'] * 1.10, 1.0)  # 10% boost for body match
        
        merged_results.sort(key=lambda x: x['score'], reverse=True)
        merged_results = merged_results[:top_k]
        
        if not merged_results:
            return ""
        
        # Format for AI consumption
        sections = []
        for r in merged_results:
            sections.append(f"### {r['heading']} (relevance: {r['score']:.2f})\n{r['text']}")
        
        return "\n\n---\n\n".join(sections)
    
    async def batch_pre_embed(self, queries: list[str]) -> list[np.ndarray]:
        """Enhancement #3: Pre-embed multiple queries in a single batch call.
        
        Instead of each specialist making 2-3 sequential embedding calls,
        all specialist queries are collected and embedded in one batch.
        This reduces ~10-15 serial HTTP calls to 1 batch call.
        
        Returns list of query vectors in the same order as input queries.
        """
        if not queries:
            return []
        
        # Anchor queries the same way retrieve() does
        anchored = [f"Topic: query\n\n{q}" for q in queries]
        return await embed_batch(anchored)
    
    async def retrieve_with_vector(self, query_vec: np.ndarray, query_text: str,
                                     top_k: int = 6, 
                                     min_score: float = MIN_RELEVANCE_SCORE) -> list[dict]:
        """Retrieve using a pre-computed query vector (Enhancement #3).
        
        Same logic as retrieve() but skips the embedding step — uses the
        pre-computed vector from batch_pre_embed() instead.
        """
        if self.embeddings is None or len(self.chunks) == 0:
            return []
        
        # Compute cosine similarities
        scores = cosine_similarity_batch(query_vec, self.embeddings)
        
        # Keyword boosting (same as retrieve())
        query_lower = query_text.lower()
        query_words = set(re.findall(r'[a-z0-9\-]+', query_lower))
        
        boosted_scores = scores.copy()
        for idx, chunk in enumerate(self.chunks):
            chunk_section_lower = chunk.get('section', '').lower()
            chunk_heading_lower = chunk.get('heading', '').lower()
            chunk_context = chunk_section_lower + ' ' + chunk_heading_lower
            
            boost = 0.0
            for protocol, keywords in PROTOCOL_KEYWORDS.items():
                query_mentions_protocol = any(
                    _keyword_in_text(kw, query_lower) for kw in keywords
                )
                if query_mentions_protocol:
                    heading_matches = any(
                        _keyword_in_text(kw, chunk_context) for kw in keywords
                    )
                    if heading_matches:
                        boost = max(boost, KEYWORD_BOOST)
                        section_match = any(
                            _keyword_in_text(kw, chunk_section_lower) for kw in keywords
                        )
                        heading_match = any(
                            _keyword_in_text(kw, chunk_heading_lower) for kw in keywords
                        )
                        if section_match and heading_match:
                            boost = max(boost, KEYWORD_BOOST * 1.5)
            
            heading_words = set(re.findall(r'[a-z0-9\-]+', chunk_context))
            overlap = query_words & heading_words
            if len(overlap) >= 3:
                boost = max(boost, KEYWORD_BOOST)
            elif len(overlap) >= 2:
                boost = max(boost, KEYWORD_BOOST * 0.6)
            
            boosted_scores[idx] += boost
        
        candidate_count = min(top_k * 3, len(self.chunks))
        top_indices = np.argsort(boosted_scores)[::-1][:candidate_count]
        
        results = []
        for idx in top_indices:
            score = float(boosted_scores[idx])
            if score < min_score:
                continue
            chunk = self.chunks[idx].copy()
            chunk['score'] = score
            chunk['raw_cosine'] = float(scores[idx])
            results.append(chunk)
            if len(results) >= top_k:
                break
        
        return results
    
    async def retrieve_for_protocol_with_vectors(
        self, protocol: str, query_vectors: dict[str, np.ndarray],
        top_k: int = 5
    ) -> str:
        """Enhancement #3: Protocol retrieval using pre-computed query vectors.
        
        Like retrieve_for_protocol() but skips embedding — uses vectors from
        batch_pre_embed() instead.
        
        Args:
            protocol: Protocol name (e.g., "OSPF", "BGP")
            query_vectors: Dict mapping query text -> pre-computed vector
            top_k: Number of results to return
        """
        seen_chunk_ids = set()
        merged_results = []
        
        for query_text, query_vec in query_vectors.items():
            results = await self.retrieve_with_vector(
                query_vec, query_text, top_k=top_k
            )
            for r in results:
                cid = r.get('chunk_id', id(r))
                if cid not in seen_chunk_ids:
                    seen_chunk_ids.add(cid)
                    merged_results.append(r)
        
        merged_results.sort(key=lambda x: x['score'], reverse=True)
        merged_results = merged_results[:top_k]
        
        if not merged_results:
            return ""
        
        sections = []
        for r in merged_results:
            sections.append(f"### {r['heading']} (relevance: {r['score']:.2f})\n{r['text']}")
        
        return "\n\n---\n\n".join(sections)
    
    async def retrieve_combined(self, query: str, top_k: int = 8, max_chars: int = 6000) -> str:
        """
        Multi-query retrieval with formatted output for AI context injection.
        Respects a max character limit to avoid context overflow.
        
        v2.0: Uses enhanced retrieve() with min-score threshold and keyword boost.
        """
        results = await self.retrieve(query, top_k=top_k)
        
        if not results:
            return ""
        
        combined = ""
        for r in results:
            score_info = f"relevance: {r['score']:.2f}"
            if 'raw_cosine' in r and abs(r['score'] - r['raw_cosine']) > 0.001:
                score_info += f", cosine: {r['raw_cosine']:.2f}, boosted"
            section_text = f"### {r['heading']} ({score_info})\n{r['text']}\n\n---\n\n"
            if len(combined) + len(section_text) > max_chars:
                break
            combined += section_text
        
        return combined
    
    def stats(self) -> dict:
        """Return stats about the vector store."""
        return {
            'store_version': getattr(self, 'store_version', '1.0'),
            'chunks': len(self.chunks),
            'dimensions': self.dim,
            'embed_model': self.embed_model,
            'built_at': self.built_at,
            'kb_hash_short': self.kb_hash[:12] if self.kb_hash else 'none',
            'cache_exists': os.path.exists(VECTOR_STORE_PATH),
            'cache_size_kb': os.path.getsize(VECTOR_STORE_PATH) / 1024 if os.path.exists(VECTOR_STORE_PATH) else 0,
            'min_relevance_score': MIN_RELEVANCE_SCORE,
            'keyword_boost': KEYWORD_BOOST,
            'heading_anchored': True,
            'multi_query': True,
        }


# ══════════════════════════════════════════════════════════════
#  STANDALONE TEST
# ══════════════════════════════════════════════════════════════

async def _test():
    """Test the v2.0 enhanced vector store with accuracy validation queries."""
    print("=" * 60)
    print("  ⊕ KB Vector Store v2.0 — Enhanced Test Mode")
    print("=" * 60)
    
    store = await KBVectorStore.create()
    stats = store.stats()
    print(f"\n◫ Store stats: {json.dumps(stats, indent=2)}")
    
    # These are the 5 accuracy-validation queries from Enhancement analysis
    # that previously returned WRONG results with v1.0
    validation_queries = [
        ("EVPN route types multihoming", "Should hit EVPN/L2VPN sections (38)"),
        ("OSPF area types stub NSSA backbone", "Should hit OSPF area sections (30.4)"),
        ("BGP route reflection cluster", "Should hit BGP sections (32)"),
        ("L3VPN Inter-AS option A B C", "Should hit L3VPN sections (37)"),
        ("LDP IGP synchronization", "Should hit LDP sections (36)"),
    ]
    
    print("\n" + "─" * 60)
    print("  ◎ Accuracy Validation (v2.0 vs v1.0 regression tests)")
    print("─" * 60)
    
    for query, expected in validation_queries:
        print(f"\n⊕ Query: \"{query}\"")
        print(f"   Expected: {expected}")
        results = await store.retrieve(query, top_k=3)
        for i, r in enumerate(results, 1):
            boost_flag = ""
            if 'raw_cosine' in r and abs(r['score'] - r['raw_cosine']) > 0.001:
                boost_flag = f" [boosted from {r['raw_cosine']:.3f}]"
            preview = r['text'][:100].replace('\n', ' ')
            print(f"   {i}. [{r['score']:.3f}]{boost_flag} {r['heading']}")
            print(f"      section: {r['section']}")
            print(f"      └─ {preview}...")
    
    # Multi-query protocol retrieval test
    print("\n" + "─" * 60)
    print("  ↻ Multi-Query Protocol Retrieval (Enhancement B)")
    print("─" * 60)
    
    for protocol in ["EVPN L2VPN", "OSPF", "BGP"]:
        print(f"\n⊛ Protocol: {protocol}")
        result_text = await store.retrieve_for_protocol(protocol, "troubleshooting", top_k=3)
        # Count sections returned
        sections_found = result_text.count("### ")
        print(f"   Sections retrieved: {sections_found}")
        # Show headings only
        for line in result_text.split('\n'):
            if line.startswith('### '):
                print(f"   ├─ {line}")
    
    print("\n● v2.0 Enhanced test complete!")


if __name__ == "__main__":
    asyncio.run(_test())
