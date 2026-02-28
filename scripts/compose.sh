#!/bin/bash
# Run Turbo Tax agent via Docker Compose
#
# Usage:
#   ./scripts/compose.sh build     # Build the image
#   ./scripts/compose.sh run       # Interactive shell
#   ./scripts/compose.sh distill   # Distill Pub 17
#   ./scripts/compose.sh distill 501  # Distill specific pub
#   ./scripts/compose.sh ask "question"  # Ask a question

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

case "${1:-}" in
    build)
        docker compose build
        ;;
    run)
        docker compose run --rm agent
        ;;
    distill)
        pub_num="${2:-17}"
        pub_file=$(ls data/irs_publications/pub_${pub_num}_*.md 2>/dev/null | head -1)
        if [[ -z "$pub_file" ]]; then
            echo "Error: Publication $pub_num not found"
            exit 1
        fi
        pub_name=$(basename "$pub_file")
        echo "Distilling: $pub_name"
        docker compose run --rm agent bash -c "qwen --yolo --allowed-mcp-server-names obsidian --prompt 'Read /app/data/irs_publications/$pub_name and distill it into the vault at /app/vault. Create notes with wiki-link backlinks.'"
        ;;
    ask)
        if [[ -z "$2" ]]; then
            echo "Usage: $0 ask \"your question\""
            exit 1
        fi
        docker compose run --rm agent bash -c "qwen --yolo --allowed-mcp-server-names obsidian --prompt '$2'"
        ;;
    *)
        echo "Usage: $0 {build|run|distill|ask}"
        echo ""
        echo "Commands:"
        echo "  build          Build the image"
        echo "  run            Interactive shell"
        echo "  distill [N]    Distell publication N (default: 17)"
        echo "  ask \"prompt\"   Ask a question"
        ;;
esac
