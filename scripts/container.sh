#!/bin/bash
# Run Turbo Tax agent in Podman container (non-interactive)
#
# Usage:
#   OPENAI_API_KEY=your-key ./scripts/container.sh "question"
#   ./scripts/container.sh build
#   ./scripts/container.sh distill

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
IMAGE_NAME="turbo-tax-agent"

# API Configuration
API_BASE_URL="${OPENAI_BASE_URL:-http://px106.prod.exalead.com:8000/v1}"
API_MODEL="${OPENAI_MODEL:-glm-5-fp8}"

# Build the container
build() {
    echo "Building container image: $IMAGE_NAME"
    podman build -t "$IMAGE_NAME" -f "$PROJECT_ROOT/Containerfile" "$PROJECT_ROOT"
}

# Run with a prompt (non-interactive)
run() {
    local prompt="$1"

    if [[ -z "$OPENAI_API_KEY" ]]; then
        echo "Error: OPENAI_API_KEY environment variable not set"
        echo "Usage: OPENAI_API_KEY=your-key $0 \"question\""
        exit 1
    fi

    podman run --rm \
        --network host \
        -v "$PROJECT_ROOT/docs:/app/docs:ro,Z" \
        -v "$PROJECT_ROOT/obsidian_db/turbo_tax:/app/vault:Z" \
        -v "$PROJECT_ROOT/data:/app/data:ro,Z" \
        -e OPENAI_API_KEY="$OPENAI_API_KEY" \
        -e OPENAI_BASE_URL="$API_BASE_URL" \
        "$IMAGE_NAME" \
        bash -c "qwen --yolo --model $API_MODEL --auth-type openai --allowed-mcp-server-names obsidian --prompt '$prompt'"
}

# Distill a publication
distill() {
    local pub_num="${1:-17}"
    local pub_file=$(ls "$PROJECT_ROOT/data/irs_publications/pub_${pub_num}"_*.md 2>/dev/null | head -1)
    if [[ -z "$pub_file" ]]; then
        echo "Error: Publication $pub_num not found"
        echo "Available: $(ls "$PROJECT_ROOT/data/irs_publications"/*.md 2>/dev/null | xargs -I {} basename {} | sed 's/pub_//; s/_[0-9]*.md//' | sort -n | tr '\n' ' ')"
        exit 1
    fi
    local pub_name=$(basename "$pub_file")
    echo "Distilling: $pub_name"
    run "Read /app/data/irs_publications/$pub_name and distill it into the vault at /app/vault. Create notes in 02 - Publications/ and 03 - Topics/ with wiki-link backlinks. Each note should link to 3-10 related notes."
}

# Show usage
usage() {
    echo "Usage: OPENAI_API_KEY=your-key $0 {build|distill [N]|\"question\"}"
    echo ""
    echo "Commands:"
    echo "  build           Build the container image"
    echo "  distill [N]     Distill publication N (default: 17)"
    echo "  \"question\"      Ask a question"
    echo ""
    echo "Environment Variables:"
    echo "  OPENAI_API_KEY     Your API key (required)"
    echo "  OPENAI_BASE_URL    API endpoint (default: http://px106.prod.exalead.com:8000/v1)"
    echo "  OPENAI_MODEL       Model name (default: glm-5-fp8)"
    echo ""
    echo "Examples:"
    echo "  OPENAI_API_KEY=xxx $0 build"
    echo "  OPENAI_API_KEY=xxx $0 distill"
    echo "  OPENAI_API_KEY=xxx $0 \"Explain the Child Tax Credit\""
}

# Main
if [[ "${1:-}" == "build" ]]; then
    build
elif [[ "${1:-}" == "distill" ]]; then
    distill "${2:-17}"
elif [[ -n "${1:-}" ]]; then
    run "$1"
else
    usage
    exit 1
fi
