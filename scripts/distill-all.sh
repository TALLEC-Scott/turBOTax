#!/bin/bash
# Distill all IRS publications into the Obsidian vault
set -e

LOG_DIR="/app/logs"
mkdir -p "$LOG_DIR"

echo "Starting distillation of all IRS publications..."
echo "Log directory: $LOG_DIR"
echo ""

# Get all publication files sorted by number
PUB_FILES=$(ls /app/data/irs_publications/pub_*.md 2>/dev/null | sort -V)
TOTAL=$(echo "$PUB_FILES" | wc -l)
CURRENT=0

for PUB_FILE in $PUB_FILES; do
    CURRENT=$((CURRENT + 1))
    PUB_NAME=$(basename "$PUB_FILE")
    PUB_NUM=$(echo "$PUB_NAME" | sed 's/pub_//; s/_[0-9]*.md//')
    
    echo "[$CURRENT/$TOTAL] Distilling: $PUB_NAME"
    echo "[$(date -Iseconds)] Starting: $PUB_NAME" >> "$LOG_DIR/distill.log"
    
    if qwen --yolo \
        --model "$OPENAI_MODEL" \
        --auth-type openai \
        --allowed-mcp-server-names obsidian \
        --prompt "Read /app/data/irs_publications/$PUB_NAME and distill it into the vault at /app/vault. Create notes in 02 - Publications/ and 03 - Topics/ with wiki-link backlinks. Each note should link to 3-10 related notes."; then
        echo "[$(date -Iseconds)] Completed: $PUB_NAME" >> "$LOG_DIR/distill.log"
    else
        echo "[$(date -Iseconds)] FAILED: $PUB_NAME" >> "$LOG_DIR/distill.log"
    fi
    
    echo ""
done

echo "Distillation complete. See $LOG_DIR/distill.log for details."
