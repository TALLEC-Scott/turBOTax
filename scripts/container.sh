#!/bin/bash
# Build and run the Turbo Tax agent in a Podman container
#
# Mounts:
#   - docs/     -> /app/docs (read-only, contains AGENT_PROMPT.md)
#   - vault/    -> /app/vault (read-write, Obsidian vault)
#   - config/   -> /app/.config/qwen (read-write, qwen config)
#   - data/     -> /app/data (read-only, IRS publications)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
IMAGE_NAME="turbo-tax-agent"
CONTAINER_NAME="turbo-tax"

# Build the container
build() {
    echo "Building container image: $IMAGE_NAME"
    podman build -t "$IMAGE_NAME" -f "$PROJECT_ROOT/Containerfile" "$PROJECT_ROOT"
}

# Run the container interactively
run() {
    echo "Running container: $CONTAINER_NAME"
    podman run -it --rm \
        --name "$CONTAINER_NAME" \
        -v "$PROJECT_ROOT/docs:/app/docs:ro,Z" \
        -v "$PROJECT_ROOT/obsidian_db/turbo_tax:/app/vault:Z" \
        -v "$PROJECT_ROOT/config:/app/.config/qwen:Z" \
        -v "$PROJECT_ROOT/data:/app/data:ro,Z" \
        "$IMAGE_NAME" \
        bash
}

# Run the distill agent
distill() {
    local pub_num="${1:-17}"
    echo "Running distill agent for Pub $pub_num"

    # Find the actual publication file
    local pub_file=$(ls "$PROJECT_ROOT/data/irs_publications/pub_${pub_num}"_*.md 2>/dev/null | head -1)
    if [[ -z "$pub_file" ]]; then
        echo "Error: Publication $pub_num not found"
        exit 1
    fi
    local pub_name=$(basename "$pub_file")

    podman run -it --rm \
        --name "$CONTAINER_NAME" \
        -v "$PROJECT_ROOT/docs:/app/docs:ro,Z" \
        -v "$PROJECT_ROOT/obsidian_db/turbo_tax:/app/vault:Z" \
        -v "$PROJECT_ROOT/config:/app/.config/qwen:Z" \
        -v "$PROJECT_ROOT/data:/app/data:ro,Z" \
        "$IMAGE_NAME" \
        bash -c "cd /app && qwen --yolo --allowed-mcp-server-names obsidian --prompt 'Read the publication at /app/data/irs_publications/$pub_name and distill it into the Obsidian vault at /app/vault. Create notes in 02 - Publications/ and 03 - Topics/ with wiki-link backlinks. Each note should link to 3-10 related notes.'"
}

# Run with a custom prompt
ask() {
    local prompt="$1"
    if [[ -z "$prompt" ]]; then
        echo "Usage: $0 ask \"your question\""
        exit 1
    fi

    podman run -it --rm \
        --name "$CONTAINER_NAME" \
        -v "$PROJECT_ROOT/docs:/app/docs:ro,Z" \
        -v "$PROJECT_ROOT/obsidian_db/turbo_tax:/app/vault:Z" \
        -v "$PROJECT_ROOT/config:/app/.config/qwen:Z" \
        -v "$PROJECT_ROOT/data:/app/data:ro,Z" \
        "$IMAGE_NAME" \
        bash -c "cd /app && qwen --yolo --allowed-mcp-server-names obsidian --prompt '$prompt'"
}

# Show usage
usage() {
    echo "Usage: $0 {build|run|distill|ask}"
    echo ""
    echo "Commands:"
    echo "  build           Build the container image"
    echo "  run             Run the container interactively"
    echo "  distill [N]     Distill publication N (default: 17)"
    echo "  ask \"prompt\"    Run with custom prompt"
    echo ""
    echo "Mounts:"
    echo "  docs/  -> /app/docs (read-only)"
    echo "  vault/ -> /app/vault (read-write)"
    echo "  config/ -> /app/.config/qwen (read-write)"
    echo "  data/  -> /app/data (read-only)"
}

# Main
case "${1:-}" in
    build)
        build
        ;;
    run)
        run
        ;;
    distill)
        distill "${2:-17}"
        ;;
    ask)
        ask "$2"
        ;;
    *)
        usage
        exit 1
        ;;
esac
