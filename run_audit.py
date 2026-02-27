#!/usr/bin/env python3
"""Quick launcher: runs the bridge in audit-only mode.

Enhancement #10: Uses the new --audit-only CLI flag instead of monkey-patching input().
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Override sys.argv to pass --audit-only flag
sys.argv = [sys.argv[0], "--audit-only"]

import ollama_mcp_client
asyncio.run(ollama_mcp_client.main())
