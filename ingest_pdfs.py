#!/usr/bin/env python3
"""
PDF Knowledge Ingester v1.0 — Extract Juniper study material into KNOWLEDGE_BASE.md

Reads the 7 Juniper PDF study guides in /files/ and appends high-value content
to the Knowledge Base. Uses smart section detection to avoid duplicating
content that's already in the KB.

Usage:
    python3 ingest_pdfs.py              # Preview what will be added
    python3 ingest_pdfs.py --apply      # Actually append to KNOWLEDGE_BASE.md
"""

import os
import re
import sys
import fitz  # PyMuPDF

KB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "KNOWLEDGE_BASE.md")
PDF_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files")

# Topics to extract from each PDF — maps PDF filename pattern to extraction config
PDF_CONFIGS = {
    "JNCIA": {
        "section_id": 50,
        "topics": [
            "routing table", "routing instance", "static route", "routing policy",
            "firewall filter", "class of service", "junos architecture",
        ],
        "skip_sections": ["table of contents", "index", "appendix", "copyright"],
    },
    "Junos Intermediate Routing JIR": {
        "section_id": 55,
        "topics": [
            "ospf", "isis", "is-is", "bgp", "routing policy", "firewall filter",
            "route preference", "routing instance", "load balancing",
        ],
        "skip_sections": ["table of contents", "index", "appendix", "copyright"],
    },
    "Advanced Junos Service Provider Routing": {
        "section_id": 60,
        "topics": [
            "mpls", "rsvp", "traffic engineering", "cspf", "fast reroute",
            "bgp", "multicast", "pim", "mvpn", "igmp", "multiprotocol bgp",
            "vpn", "l3vpn", "inter-as",
        ],
        "skip_sections": ["table of contents", "index", "appendix", "copyright"],
    },
    "Junos MPLS Fundamentals JMF": {
        "section_id": 65,
        "topics": [
            "mpls", "label", "lsp", "rsvp", "ldp", "penultimate hop",
            "fast reroute", "frr", "bypass", "link protection", "node protection",
            "cspf", "traffic engineering", "explicit route", "ero", "rro",
            "bandwidth", "priority", "preemption",
        ],
        "skip_sections": ["table of contents", "index", "appendix", "copyright"],
    },
    "Junos Layer 2 VPNs JL2V": {
        "section_id": 70,
        "topics": [
            "l2vpn", "l2circuit", "vpls", "pseudowire", "martini",
            "kompella", "evpn", "ethernet segment", "esi", "multihoming",
            "mac learning", "mac mobility", "split horizon", "designated forwarder",
            "route type", "evi", "vxlan",
        ],
        "skip_sections": ["table of contents", "index", "appendix", "copyright"],
    },
    "Junos Service Provider Switching JSPX": {
        "section_id": 75,
        "topics": [
            "vlan", "spanning tree", "rstp", "mstp", "lacp", "lag",
            "aggregated ethernet", "storm control", "irb", "bridge domain",
            "ethernet switching", "mac table", "bpdu",
        ],
        "skip_sections": ["table of contents", "index", "appendix", "copyright"],
    },
    "Layer 3 VPNs": {
        "section_id": 80,
        "topics": [
            "l3vpn", "vrf", "route distinguisher", "route target",
            "inter-as", "option a", "option b", "option c",
            "carrier of carrier", "csc", "hub spoke", "hub-spoke",
            "extranet", "internet access", "vpn gateway",
            "bgp free core", "label allocation",
        ],
        "skip_sections": ["table of contents", "index", "appendix", "copyright"],
    },
}


def extract_pdf_text(pdf_path: str) -> str:
    """Extract all text from a PDF using PyMuPDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text() + "\n\n"
    doc.close()
    return text


def extract_relevant_sections(text: str, topics: list, skip_sections: list) -> list:
    """Extract paragraphs/sections relevant to the given topics.
    
    Uses a sliding-window approach: splits the full text into ~1000-word chunks,
    scores each chunk by topic-keyword density, and keeps the best ones.
    
    Returns list of (heading, content) tuples.
    """
    sections = []
    topic_pattern = re.compile('|'.join(re.escape(t) for t in topics), re.IGNORECASE)
    skip_pattern = re.compile('|'.join(re.escape(s) for s in skip_sections), re.IGNORECASE) if skip_sections else None
    
    # Try to split on Module/Chapter/Part headings first
    module_splits = re.split(
        r'\n(?=(?:Module|Chapter|Part|Section|Unit)\s+\d)',
        text,
        flags=re.IGNORECASE
    )
    
    # If that doesn't produce enough splits, use fixed-size chunking
    if len(module_splits) < 5:
        # Split into ~800 word chunks with 100-word overlap
        words = text.split()
        chunk_size = 800
        overlap = 100
        module_splits = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            module_splits.append(chunk)
    
    for chunk in module_splits:
        chunk = chunk.strip()
        if len(chunk) < 100:
            continue
        
        # Skip unwanted sections
        if skip_pattern and skip_pattern.search(chunk[:200]):
            continue
        
        # Score by topic keyword density
        matches = topic_pattern.findall(chunk)
        if not matches:
            continue
        
        # Need at least 2 topic matches per chunk to be considered relevant
        if len(matches) < 2:
            continue
        
        # Extract a heading from the first line(s)
        lines = chunk.split('\n')
        heading = ""
        for line in lines[:5]:
            line = line.strip()
            if len(line) > 10 and len(line) < 150:
                heading = line
                break
        
        # Clean the chunk
        cleaned = clean_extracted_text(chunk)
        if len(cleaned) < 200:
            continue
        
        # Score: matches per 1000 chars
        density = len(matches) / (len(cleaned) / 1000)
        
        sections.append((heading, cleaned, density))
    
    # Sort by density (most relevant first) and keep top N
    sections.sort(key=lambda x: x[2], reverse=True)
    max_sections = 12  # Keep top 12 per PDF (most relevant by density)
    
    return [(h, c) for h, c, _ in sections[:max_sections]]


def clean_extracted_text(text: str) -> str:
    """Clean up PDF extraction artifacts."""
    # Remove excessive whitespace
    text = re.sub(r' {3,}', ' ', text)
    # Remove page break artifacts
    text = re.sub(r'\f', '\n', text)
    # Remove orphan numbers (page numbers)
    text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
    # Normalize line breaks
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    # Remove very short lines (likely headers/footers)
    lines = text.split('\n')
    lines = [l for l in lines if len(l.strip()) > 3 or l.strip() == '']
    return '\n'.join(lines)


def load_existing_kb():
    """Load existing KB to check for duplicate content."""
    if os.path.exists(KB_PATH):
        with open(KB_PATH, "r") as f:
            return f.read()
    return ""


def is_duplicate(content: str, existing_kb: str, threshold: float = 0.6) -> bool:
    """Check if content is already substantially in the KB.
    Uses simple word overlap ratio.
    """
    content_words = set(content.lower().split())
    kb_words = set(existing_kb.lower().split())
    
    if not content_words:
        return True
    
    overlap = len(content_words & kb_words) / len(content_words)
    return overlap > threshold


def main():
    apply = "--apply" in sys.argv
    
    existing_kb = load_existing_kb()
    
    print("=" * 60)
    print("⊞ Juniper PDF Knowledge Ingester v1.0")
    print("=" * 60)
    
    # Find PDFs
    if not os.path.exists(PDF_DIR):
        print(f"✗ PDF directory not found: {PDF_DIR}")
        return
    
    pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]
    print(f"↻ Found {len(pdf_files)} PDFs in {PDF_DIR}")
    
    all_new_sections = []
    
    for pdf_file in sorted(pdf_files):
        pdf_path = os.path.join(PDF_DIR, pdf_file)
        
        # Find matching config
        config = None
        config_name = None
        for name, cfg in PDF_CONFIGS.items():
            if name.lower() in pdf_file.lower() or pdf_file.lower().startswith(name.lower()):
                config = cfg
                config_name = name
                break
        
        if not config:
            print(f"   ▲  Skipping {pdf_file} (no extraction config)")
            continue
        
        print(f"\n▸ Processing: {pdf_file}")
        
        # Extract text
        raw_text = extract_pdf_text(pdf_path)
        clean_text = clean_extracted_text(raw_text)
        print(f"   ▪ Extracted {len(raw_text):,} chars ({len(clean_text.split()):,} words)")
        
        # Find relevant sections
        sections = extract_relevant_sections(clean_text, config["topics"], config.get("skip_sections", []))
        print(f"   ⊕ Found {len(sections)} relevant sections")
        
        # Filter duplicates
        new_sections = []
        for heading, content in sections:
            if not is_duplicate(content, existing_kb):
                new_sections.append((heading, content))
        
        print(f"   ● {len(new_sections)} new sections (after dedup)")
        
        if new_sections:
            section_id = config["section_id"]
            all_new_sections.append((config_name, section_id, new_sections))
    
    # Summary
    total_new = sum(len(s[2]) for s in all_new_sections)
    total_chars = sum(sum(len(c) for _, c in s[2]) for s in all_new_sections)
    
    print(f"\n{'=' * 60}")
    print(f"◫ Total: {total_new} new sections, ~{total_chars:,} chars")
    
    if not total_new:
        print("ℹ️  No new content to add. KB is already comprehensive!")
        return
    
    if not apply:
        print(f"\n▲  DRY RUN — Run with --apply to append to {KB_PATH}")
        print(f"   Preview of first 3 sections per PDF:")
        for name, sid, sections in all_new_sections:
            print(f"\n   ▸ {name} (Section {sid}):")
            for heading, content in sections[:3]:
                preview = content[:150].replace('\n', ' ')
                print(f"      • {heading[:60] if heading else '(no heading)'}: {preview}...")
        return
    
    # Apply: append to KB
    print(f"\n✍️  Appending to {KB_PATH}...")
    
    with open(KB_PATH, "a") as f:
        for name, sid, sections in all_new_sections:
            f.write(f"\n\n---\n\n# SECTION {sid}: {name.upper()} — PDF EXTRACTED KNOWLEDGE\n\n")
            f.write(f"> **Source:** {name} study guide (auto-extracted)\n\n")
            
            for i, (heading, content) in enumerate(sections):
                if heading:
                    f.write(f"## {sid}.{i+1} {heading}\n\n")
                # Wrap content in a readable format
                # Limit each section to ~1500 chars to keep KB manageable
                trimmed = content[:1500]
                if len(content) > 1500:
                    trimmed += "\n[...truncated...]"
                f.write(f"{trimmed}\n\n")
    
    # Count final KB size
    with open(KB_PATH, "r") as f:
        final_kb = f.read()
    
    print(f"● KB updated: {len(final_kb):,} chars, {len(final_kb.splitlines()):,} lines")
    print(f"▲  Run the app to auto-rebuild the RAG vector store with new content.")


if __name__ == "__main__":
    main()
