#!/bin/bash
# Distill a single IRS publication into the Obsidian vault
# Usage: distill-entrypoint.sh <pub_number>
set -e

PUB_NUM="${1:-17}"
PUB_FILE=$(ls /app/data/irs_publications/pub_${PUB_NUM}_*.md 2>/dev/null | head -1)

if [[ -z "$PUB_FILE" ]]; then
    echo "Error: Publication $PUB_NUM not found"
    echo "Available publications:"
    ls /app/data/irs_publications/*.md | xargs -I {} basename {} | sed 's/pub_//; s/_[0-9]*.md//' | sort -n
    exit 1
fi

PUB_NAME=$(basename "$PUB_FILE")
echo "Distilling: $PUB_NAME"

qwen --yolo \
    --model "$OPENAI_MODEL" \
    --auth-type openai \
    --allowed-mcp-server-names obsidian \
    --prompt "Read /app/data/irs_publications/$PUB_NAME and distill it into the vault at /app/vault. Create notes in 02 - Publications/ and 03 - Topics/ with wiki-link backlinks. Each note should link to 3-10 related notes."
