#!/bin/bash
# Turbo Tax Agent - Podman Compose wrapper
#
# Usage:
#   ./scripts/container.sh build          # Build the image
#   ./scripts/container.sh distill [N]    # Distill publication N (default: 17)
#   ./scripts/container.sh distill-all    # Distill all publications
#   ./scripts/container.sh "question"     # Ask a question
#
# Requires: .env file with OPENAI_API_KEY

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Check for .env file
if [[ ! -f ".env" ]]; then
    if [[ -f ".env.example" ]]; then
        echo "Creating .env from .env.example..."
        cp .env.example .env
        echo "Please edit .env with your API key, then run again."
        exit 1
    else
        echo "Error: .env file not found. Please create it with OPENAI_API_KEY."
        exit 1
    fi
fi

# Main
case "${1:-}" in
    build)
        podman-compose build
        ;;
    distill)
        podman-compose run --rm distill "${2:-17}"
        ;;
    distill-all)
        podman-compose run --rm distill-all
        ;;
    "")
        echo "Usage: $0 {build|distill [N]|distill-all|\"question\"}"
        exit 1
        ;;
    *)
        # Treat as a question/prompt
        podman-compose run --rm agent bash -c "qwen --yolo --model \$OPENAI_MODEL --auth-type openai --allowed-mcp-server-names obsidian --prompt '$1'"
        ;;
esac
