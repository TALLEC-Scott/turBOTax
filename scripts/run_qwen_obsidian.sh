#!/bin/bash
# Run Qwen Code agent in yolo mode with Obsidian MCP server

VAULT_PATH="${1:-$(pwd)/obsidian_db/turbo_tax}"
PROMPT="${2:-List all files in the Obsidian vault and summarize what's there}"

set -e

echo "=== Setting up Obsidian MCP server ==="
echo "Vault path: $VAULT_PATH"

# Add Obsidian MCP server (will prompt if already exists, that's fine)
qwen mcp add obsidian npx -y @mauricio.wolff/mcp-obsidian@latest "$VAULT_PATH" 2>/dev/null || true

echo ""
echo "=== Running Qwen Code in YOLO mode ==="
echo "Prompt: $PROMPT"
echo ""

# Run Qwen Code in yolo mode with the prompt
qwen --yolo --allowed-mcp-server-names obsidian "$PROMPT"
