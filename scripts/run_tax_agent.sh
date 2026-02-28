#!/bin/bash
# Run IRS Tax Accountant Agent in Qwen Code with Obsidian MCP
#
# Usage:
#   ./scripts/run_tax_agent.sh
#   ./scripts/run_tax_agent.sh "Explain the Child Tax Credit"
#   ./scripts/run_tax_agent.sh --interactive
#   ./scripts/run_tax_agent.sh --distill

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VAULT_PATH="$PROJECT_ROOT/obsidian_db/turbo_tax"
AGENT_PROMPT_PATH="$PROJECT_ROOT/docs/AGENT_PROMPT.md"

# Ensure vault exists
mkdir -p "$VAULT_PATH"

# Check agent prompt exists
if [[ ! -f "$AGENT_PROMPT_PATH" ]]; then
    echo "Error: Agent prompt not found at $AGENT_PROMPT_PATH"
    exit 1
fi

# Setup MCP server
echo "Setting up Obsidian MCP server for vault: $VAULT_PATH"
qwen mcp add obsidian npx -y @mauricio.wolff/mcp-obsidian@latest "$VAULT_PATH" 2>/dev/null || true

# Build system context
SYSTEM_CONTEXT=$(cat <<'EOF'
# IRS Tax Accountant Agent

You are operating as the IRS Tax Accountant Agent. Your system prompt follows.

---

## Vault Structure Reference

See: /udir/stallec/home/turbo-tax/docs/VAULT_STRUCTURE.md

EOF
)

# Load agent prompt
AGENT_PROMPT=$(cat "$AGENT_PROMPT_PATH")

# Parse arguments
INTERACTIVE=""
PROMPT="${1:-}"

if [[ "$PROMPT" == "--interactive" ]]; then
    INTERACTIVE="--prompt-interactive"
    PROMPT=""
elif [[ "$PROMPT" == "--distill" ]]; then
    PROMPT="Please review the parsed IRS publications in data/irs_publications/ and distill key knowledge into the Obsidian vault. Start with Publication 17."
elif [[ "$PROMPT" == "--help" ]] || [[ "$PROMPT" == "-h" ]]; then
    echo "Usage: $0 [OPTIONS] [PROMPT]"
    echo ""
    echo "Options:"
    echo "  --interactive    Run in interactive mode"
    echo "  --distill        Distill IRS publications into vault"
    echo "  --help           Show this help"
    echo ""
    echo "Examples:"
    echo "  $0                                    # Review vault and suggest improvements"
    echo "  $0 \"Explain the Child Tax Credit\"    # Ask a tax question"
    echo "  $0 --interactive                      # Interactive mode"
    echo "  $0 --distill                          # Distill publications"
    exit 0
fi

# Default prompt if none provided
if [[ -z "$PROMPT" ]]; then
    PROMPT="Please introduce yourself as the IRS Tax Accountant Agent and:
1. Review the current state of the Obsidian vault
2. List what notes currently exist
3. Suggest what notes should be created or improved
4. Offer to help with any tax questions or documentation

Remember to follow the backlink philosophy: build connections, not hierarchies."
fi

# Combine prompts
FULL_PROMPT="${SYSTEM_CONTEXT}
${AGENT_PROMPT}

---

## User Request

${PROMPT}"

# Print header
echo ""
echo "============================================================"
echo "IRS Tax Accountant Agent"
echo "============================================================"
echo "Vault: $VAULT_PATH"
echo "Mode: $([ -n "$INTERACTIVE" ] && echo "Interactive" || echo "One-shot")"
echo "============================================================"
echo ""

# Run the agent
qwen --yolo \
    --allowed-mcp-server-names obsidian \
    $INTERACTIVE \
    --prompt "$FULL_PROMPT"
