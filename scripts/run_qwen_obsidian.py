#!/usr/bin/env python3
"""Run Qwen Code agent in yolo mode with Obsidian MCP server.

Usage:
    uv run python scripts/run_qwen_obsidian.py [vault_path] [prompt]

Examples:
    uv run python scripts/run_qwen_obsidian.py
    uv run python scripts/run_qwen_obsidian.py ./obsidian_db/turbo_tax "List all notes"
    uv run python scripts/run_qwen_obsidian.py /path/to/vault "Create a summary note"
"""

import subprocess
import sys
from pathlib import Path


def main() -> None:
    vault_path = sys.argv[1] if len(sys.argv) > 1 else "obsidian_db/turbo_tax"
    prompt = (
        sys.argv[2]
        if len(sys.argv) > 2
        else "List all files in the Obsidian vault and summarize what's there"
    )

    vault = Path(vault_path).resolve()
    if not vault.exists():
        print(f"Creating vault directory: {vault}")
        vault.mkdir(parents=True, exist_ok=True)

    print("=== Setting up Obsidian MCP server ===")
    print(f"Vault path: {vault}")

    # Add Obsidian MCP server
    add_cmd = [
        "qwen",
        "mcp",
        "add",
        "obsidian",
        "npx",
        "-y",
        "@mauricio.wolff/mcp-obsidian@latest",
        str(vault),
    ]

    result = subprocess.run(add_cmd, capture_output=True, text=True)
    if result.returncode != 0 and "already exists" not in result.stderr.lower():
        print(f"Warning: {result.stderr}")

    print("\n=== Running Qwen Code in YOLO mode ===")
    print(f"Prompt: {prompt}\n")

    # Run Qwen Code in yolo mode
    run_cmd = [
        "qwen",
        "--yolo",
        "--allowed-mcp-server-names",
        "obsidian",
        prompt,
    ]

    subprocess.run(run_cmd)


if __name__ == "__main__":
    main()
