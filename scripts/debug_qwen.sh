#!/bin/bash
# Debug script to test qwen CLI behavior

set -x

echo "=== Test 1: Simple qwen command ==="
timeout 10 qwen --yolo --prompt "Say hello"

echo ""
echo "=== Test 2: qwen with MCP (obsidian) ==="
timeout 30 qwen --yolo --allowed-mcp-server-names obsidian --prompt "List files in vault"

echo ""
echo "=== Test 3: qwen with medium prompt ==="
PROMPT="Read the file data/irs_publications/pub_17_2025.md and tell me the first 3 chapters."
timeout 60 qwen --yolo --prompt "$PROMPT"

echo ""
echo "=== Test 4: qwen with MCP and file read ==="
timeout 60 qwen --yolo --allowed-mcp-server-names obsidian --prompt "Read the first 100 lines of data/irs_publications/pub_17_2025.md and summarize it"

echo ""
echo "=== All tests completed ==="
