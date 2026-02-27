# 🤖 Model Upgrade Path — Junos AI NOC Bridge

## Current Model
- **Model:** `qwen2.5:14b` (Q4_K_M quantization, 9.0 GB)
- **Context Window:** 32,768 tokens
- **Strengths:** Good tool calling, solid JSON reasoning, Junos knowledge
- **Weaknesses:** Occasional hallucination, limited multi-step planning

## Upgrade Candidates

### Tier 1: Drop-in Replacements (Same Hardware)

| Model | Size | Context | Tool Calling | Notes |
|-------|------|---------|-------------|-------|
| `qwen3:14b` | ~9 GB | 32K+ | ✅ Better | When stable — improved reasoning, better function calling |
| `qwen2.5-coder:14b` | ~9 GB | 32K | ✅ Good | Better at config generation, CLI output parsing |
| `mistral-nemo:12b` | ~7 GB | 128K | ✅ Native | Huge context window, good instruction following |
| `llama3.1:8b` | ~5 GB | 128K | ✅ Good | Fast, 128K context, but smaller capacity |

### Tier 2: Quality Upgrade (Needs 24+ GB RAM)

| Model | Size | Context | Tool Calling | Notes |
|-------|------|---------|-------------|-------|
| `qwen2.5:32b` | ~20 GB | 32K | ✅ Excellent | Major reasoning upgrade, fits in 24GB |
| `llama3.3:70b` | ~40 GB | 128K | ✅ Excellent | Best open-source, needs 48GB+ |
| `deepseek-coder-v2:16b` | ~10 GB | 128K | ⚠️ Limited | Great for code, limited tool use |

### Tier 3: Cloud/API Options (No Hardware Limit)

| Provider | Model | Notes |
|----------|-------|-------|
| Groq Cloud | `llama3.3-70b` | Free tier, blazing fast, API-compatible |
| Together AI | `qwen2.5-72b` | Pay-per-use, excellent quality |
| OpenRouter | Various | Multi-model routing, competitive pricing |

## How to Upgrade

### Step 1: Pull the new model
```bash
ollama pull qwen3:14b
```

### Step 2: Update config.yaml
```yaml
ai:
  model: "qwen3:14b"
```

### Step 3: Test
```bash
python3 ollama_mcp_client.py
# Ask: "check BGP on PE1" — verify tool calling works
# Ask: "what is OSPF?" — verify knowledge retrieval works
# Run: audit — verify multi-step analysis works
```

### Step 4: Tune parameters
```yaml
ai:
  temperature: 0.15      # Start low, increase if responses too rigid
  top_p: 0.9             # Keep narrow for deterministic networking answers
  repeat_penalty: 1.1    # Prevent repetitive output
```

## Architecture Notes

The codebase is **model-agnostic** by design:
- All AI calls go through `ollama_chat()` which uses the Ollama REST API
- Tool schemas use OpenAI-compatible format (works with any Ollama model)
- System prompt is configurable in `config.yaml`
- Temperature, top_p, repeat_penalty all configurable
- Context window management adapts to `NUM_CTX` setting

To use a **cloud API** instead of local Ollama:
1. Replace `ollama_chat()` with an API client (httpx to OpenAI endpoint)
2. Update `OLLAMA_URL` to the cloud endpoint
3. Add API key to `config.yaml`

## Recommended Upgrade Timeline

1. **Now:** Stay with `qwen2.5:14b` — stable, proven
2. **When available:** Try `qwen3:14b` — likely better tool calling
3. **If budget allows:** `qwen2.5:32b` for significantly better reasoning
4. **For production:** Consider cloud API for reliability + 70B+ model quality
