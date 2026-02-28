#!/usr/bin/env python3
"""Run IRS Tax Accountant Agent in Qwen Code with Obsidian MCP.

This script spawns a Qwen Code agent in yolo mode with:
- The IRS Tax Accountant Agent system prompt
- Obsidian MCP server connected to the vault
- Full access to manipulate the vault

Usage:
    uv run python scripts/run_tax_agent.py
    uv run python scripts/run_tax_agent.py "Explain the Child Tax Credit"
    uv run python scripts/run_tax_agent.py --interactive
"""

import argparse
import subprocess
import sys
from pathlib import Path


def get_agent_prompt() -> str:
    """Load the agent prompt from the docs folder."""
    prompt_path = Path(__file__).parent.parent / "docs" / "AGENT_PROMPT.md"
    if not prompt_path.exists():
        print(f"Error: Agent prompt not found at {prompt_path}")
        sys.exit(1)
    return prompt_path.read_text()


def get_vault_path() -> Path:
    """Get the absolute path to the Obsidian vault."""
    vault_path = Path(__file__).parent.parent / "obsidian_db" / "turbo_tax"
    vault_path.mkdir(parents=True, exist_ok=True)
    return vault_path.resolve()


def setup_mcp_server(vault_path: Path) -> None:
    """Configure the Obsidian MCP server."""
    print(f"Setting up Obsidian MCP server for vault: {vault_path}")

    # Add Obsidian MCP server
    result = subprocess.run(
        [
            "qwen",
            "mcp",
            "add",
            "obsidian",
            "npx",
            "-y",
            "@mauricio.wolff/mcp-obsidian@latest",
            str(vault_path),
        ],
        capture_output=True,
        text=True,
    )

    # It's okay if it already exists
    if result.returncode != 0 and "already" not in result.stderr.lower():
        print(f"Warning: {result.stderr}")


def build_system_context() -> str:
    """Build the system context with vault structure info."""
    vault_structure_path = Path(__file__).parent.parent / "docs" / "VAULT_STRUCTURE.md"
    
    context_parts = [
        "# IRS Tax Accountant Agent",
        "",
        "You are operating as the IRS Tax Accountant Agent. Your system prompt follows.",
        "",
        "---",
        "",
    ]
    
    # Add vault structure info
    if vault_structure_path.exists():
        context_parts.append("## Vault Structure Reference")
        context_parts.append("")
        context_parts.append(f"See: {vault_structure_path}")
        context_parts.append("")
    
    return "\n".join(context_parts)


def get_parsed_publications_dir() -> Path:
    """Get the path to parsed IRS publications."""
    return (Path(__file__).parent.parent / "data" / "irs_publications").resolve()


def build_distillation_prompt(publications_dir: Path) -> str:
    """Build the knowledge distillation prompt."""
    # List available publications
    pubs = list(publications_dir.glob("pub_*.md"))
    pub_list = "\n".join(f"  - {p.name}" for p in sorted(pubs)[:20])
    if len(pubs) > 20:
        pub_list += f"\n  - ... and {len(pubs) - 20} more"
    
    return f"""# Knowledge Distillation Task

You have access to parsed IRS publications in the `data/irs_publications/` directory. Your task is to distill this knowledge into the Obsidian vault.

## Source Materials

The following parsed publications are available in `{publications_dir}`:

{pub_list}

## Your Task

Please distill the IRS publications into the Obsidian vault by:

### Phase 1: Setup Vault Structure
1. Create the folder structure as defined in VAULT_STRUCTURE.md:
   - `00 - Dashboard/` with Map of Contents
   - `01 - Tax Forms/` organized by year
   - `02 - Publications/` for distilled publication notes
   - `03 - Topics/` for thematic notes
   - `04 - Assets/` for tables
   - `00 - Templates/` for note templates

### Phase 2: Create Core Notes
Start with a few key publications and create distilled notes:

1. **Publication 17** (Your Federal Income Tax) - This is the most comprehensive
   - Create summary note with key chapters linked to topics
   - Extract major topics into `03 - Topics/` notes

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

1. **Read source first**: Use `read_file` to read publications from `{publications_dir}/`
2. **Write to vault**: Use Obsidian MCP tools to write to `obsidian_db/turbo_tax/`
3. **Follow templates**: Use the note templates from AGENT_PROMPT.md
4. **Cite sources**: Always link to the source publication with `[[Pub X]]`
5. **Build connections**: Every note needs backlinks to related topics

## Start Small

Don't try to distill everything at once. Start with:
1. Creating the folder structure
2. Creating the Map of Contents
3. Distilling ONE publication (start with Pub 17)
4. Creating 2-3 topic notes from that publication
5. Building the backlinks between them

Then we can continue with more publications in follow-up prompts.

Remember: A note with 10 backlinks is more valuable than a note in 10 folders. Build connections, not hierarchies."""


def run_agent(
    prompt: str | None = None,
    interactive: bool = False,
    vault_path: Path | None = None,
    distill: bool = False,
) -> None:
    """Run the Qwen Code agent."""
    
    if vault_path is None:
        vault_path = get_vault_path()
    
    # Setup MCP server
    setup_mcp_server(vault_path)
    
    # Load agent prompt
    agent_prompt = get_agent_prompt()
    
    # Build the full context
    system_context = build_system_context()
    
    # Default prompt if none provided
    if prompt is None:
        if distill:
            publications_dir = get_parsed_publications_dir()
            prompt = build_distillation_prompt(publications_dir)
        else:
            prompt = """Please introduce yourself as the IRS Tax Accountant Agent and:

1. Review the current state of the Obsidian vault
2. List what notes currently exist
3. Suggest what notes should be created or improved
4. Offer to help with any tax questions or documentation

Remember to follow the backlink philosophy: build connections, not hierarchies."""
    
    # Combine system prompt with user prompt
    full_prompt = f"""{system_context}

{agent_prompt}

---

## User Request

{prompt}"""
    
    print("\n" + "=" * 60)
    print("IRS Tax Accountant Agent")
    print("=" * 60)
    print(f"Vault: {vault_path}")
    print(f"Mode: {'Interactive' if interactive else 'One-shot'}")
    print("=" * 60 + "\n")
    
    # Build command
    cmd = [
        "qwen",
        "--yolo",
        "--allowed-mcp-server-names", "obsidian",
        "--prompt", full_prompt,
    ]

    if interactive:
        cmd.append("--prompt-interactive")
    
    # Run the agent
    subprocess.run(cmd)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run IRS Tax Accountant Agent in Qwen Code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Run with default prompt (review vault and suggest improvements)
    uv run python scripts/run_tax_agent.py

    # Distill IRS publications into the vault
    uv run python scripts/run_tax_agent.py --distill

    # Ask a specific tax question
    uv run python scripts/run_tax_agent.py "Explain the Child Tax Credit"

    # Create documentation
    uv run python scripts/run_tax_agent.py "Create a note about Itemized Deductions"

    # Interactive mode (continues after initial prompt)
    uv run python scripts/run_tax_agent.py --interactive

    # Distill + Interactive mode
    uv run python scripts/run_tax_agent.py --distill --interactive

    # Custom vault path
    uv run python scripts/run_tax_agent.py --vault /path/to/vault "List all notes"
        """,
    )
    
    parser.add_argument(
        "prompt",
        nargs="?",
        help="The prompt/question for the agent",
    )
    
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Run in interactive mode (continues after initial prompt)",
    )
    
    parser.add_argument(
        "--vault",
        type=Path,
        help="Path to Obsidian vault (default: obsidian_db/turbo_tax)",
    )
    
    parser.add_argument(
        "-d", "--distill",
        action="store_true",
        help="Distill IRS publications from data/irs_publications/ into the vault",
    )
    
    args = parser.parse_args()
    
    run_agent(
        prompt=args.prompt,
        interactive=args.interactive,
        vault_path=args.vault,
        distill=args.distill,
    )


if __name__ == "__main__":
    main()
