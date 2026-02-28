#!/bin/bash
# Distill IRS publications into Obsidian vault
#
# Usage:
#   ./scripts/distill.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VAULT_PATH="$PROJECT_ROOT/obsidian_db/turbo_tax"
PUBS_PATH="$PROJECT_ROOT/data/irs_publications"
AGENT_PROMPT_PATH="$PROJECT_ROOT/docs/AGENT_PROMPT.md"

# Ensure directories exist
mkdir -p "$VAULT_PATH"

# Check agent prompt exists
if [[ ! -f "$AGENT_PROMPT_PATH" ]]; then
    echo "Error: Agent prompt not found at $AGENT_PROMPT_PATH"
    exit 1
fi

# Check publications exist
if [[ ! -d "$PUBS_PATH" ]]; then
    echo "Error: Publications directory not found at $PUBS_PATH"
    echo "Run the parser first to generate publications."
    exit 1
fi

# Count available publications
PUB_COUNT=$(find "$PUBS_PATH" -name "*.md" -type f 2>/dev/null | wc -l)
if [[ "$PUB_COUNT" -eq 0 ]]; then
    echo "Error: No parsed publications found in $PUBS_PATH"
    exit 1
fi

# Setup MCP server
echo "Setting up Obsidian MCP server for vault: $VAULT_PATH"
qwen mcp add obsidian npx -y @mauricio.wolff/mcp-obsidian@latest "$VAULT_PATH" 2>/dev/null || true

# Print header
echo ""
echo "============================================================"
echo "IRS Tax Accountant Agent - Knowledge Distillation"
echo "============================================================"
echo "Vault: $VAULT_PATH"
echo "Publications: $PUB_COUNT files"
echo "============================================================"
echo ""

# Run the agent with prompt inline
qwen --yolo \
    --allowed-mcp-server-names obsidian \
    --prompt "$(cat "$AGENT_PROMPT_PATH")

---

## Knowledge Distillation Task

You have access to parsed IRS publications in the \`data/irs_publications/\` directory. Your task is to distill this knowledge into the Obsidian vault.

## Source Materials

The following parsed publications are available in \`$PUBS_PATH\`:

$(find "$PUBS_PATH" -name "*.md" -type f | sort | head -20 | xargs -I {} basename {})

Total: $PUB_COUNT publications

## Your Task

Please distill the IRS publications into the Obsidian vault by:

### Phase 1: Setup Vault Structure
1. Create the folder structure as defined in VAULT_STRUCTURE.md:
   - \`00 - Dashboard/\` with Map of Contents
   - \`01 - Tax Forms/\` organized by year
   - \`02 - Publications/\` for distilled publication notes
   - \`03 - Topics/\` for thematic notes
   - \`04 - Assets/\` for tables
   - \`00 - Templates/\` for note templates

### Phase 2: Create Core Notes
Start with a few key publications and create distilled notes:

1. **Publication 17** (Your Federal Income Tax) - This is the most comprehensive
   - Create summary note with key chapters linked to topics
   - Extract major topics into \`03 - Topics/\` notes

2. **Publication 501** (Dependents, Standard Deduction, Filing Information)
   - Create topic notes for: Filing Status, Dependents, Standard Deduction
   - Link these topics to each other

3. **Publication 590** (IRAs) and **Publication 596** (Earned Income Credit)
   - Create focused topic notes with rules and limits

### Phase 3: Build Backlinks
For every note you create:
- Link to 3-10 related notes minimum
- Link to source publication(s)
- Link to related forms
- Create reverse links in related notes

## Important Guidelines

1. **Read source first**: Use \`read_file\` to read publications from \`$PUBS_PATH/\`
2. **Write to vault**: Use Obsidian MCP tools to write to the vault
3. **Follow templates**: Use the note templates from the agent prompt
4. **Cite sources**: Always link to the source publication with \`[[Pub X]]\`
5. **Build connections**: Every note needs backlinks to related topics

## Start Small

Don't try to distill everything at once. Start with:
1. Creating the folder structure
2. Creating the Map of Contents
3. Distilling ONE publication (start with Pub 17)
4. Creating 2-3 topic notes from that publication
5. Building the backlinks between them

Remember: A note with 10 backlinks is more valuable than a note in 10 folders. Build connections, not hierarchies."
