#!/bin/bash
# Extract structured tables from IRS publications to CSV assets
# Usage: extract-assets-entrypoint.sh [pub_number]
#
# Examples:
#   extract-assets-entrypoint.sh         # Extract from all publications
#   extract-assets-entrypoint.sh 17      # Extract from Pub 17 only
#   extract-assets-entrypoint.sh --list  # List tables found
set -e

PUB_NUM="${1:-}"
LIST_MODE=""

if [[ "$PUB_NUM" == "--list" ]] || [[ "$PUB_NUM" == "-l" ]]; then
    LIST_MODE="--list-tables"
    PUB_NUM=""
fi

echo "=========================================="
echo "IRS Publication Table Extractor"
echo "=========================================="
echo "Model: $OPENAI_MODEL"
echo "Base URL: $OPENAI_BASE_URL"
echo ""

# Run the extraction script
cd /app

if [[ -n "$PUB_NUM" ]]; then
    echo "Extracting tables from Publication $PUB_NUM..."
    uv run python scripts/extract_assets.py --pub "$PUB_NUM"
elif [[ -n "$LIST_MODE" ]]; then
    echo "Listing tables found in all publications..."
    uv run python scripts/extract_assets.py --list-tables
else
    echo "Extracting tables from all publications..."
    uv run python scripts/extract_assets.py
fi

echo ""
echo "=========================================="
echo "Extraction complete!"
echo "Assets saved to: /app/vault/04 - Assets/"
echo "=========================================="
