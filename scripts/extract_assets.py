"""Extract structured tables from parsed IRS publications to CSV assets.

This script identifies and extracts tabular data from the parsed IRS
publications (markdown files from Docling) and saves them as clean CSV
files in the Obsidian vault's Assets folder.

Tables extracted include:
- Tax tables (income -> tax by filing status)
- Standard deduction amounts
- EIC tables
- Filing requirement thresholds
- Contribution limits
- Any other structured numerical data

Usage:
    uv run python scripts/extract_assets.py
    uv run python scripts/extract_assets.py --pub 17
    uv run python scripts/extract_assets.py --list-tables
"""

import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import httpx


def get_data_dir() -> Path:
    """Get the path to parsed IRS publications."""
    # Check for container path first
    container_data = Path("/app/data/irs_publications")
    if container_data.exists():
        return container_data
    return (Path(__file__).parent.parent / "data" / "irs_publications").resolve()


def get_vault_dir() -> Path:
    """Get the path to the Obsidian vault."""
    # Check for container path first
    container_vault = Path("/app/vault")
    if container_vault.exists():
        return container_vault
    return (Path(__file__).parent.parent / "obsidian_db" / "turbo_tax").resolve()


def get_assets_dir() -> Path:
    """Get the path to the Assets folder."""
    assets = get_vault_dir() / "04 - Assets"
    assets.mkdir(parents=True, exist_ok=True)
    return assets


def get_topics_dir() -> Path:
    """Get the path to the Topics folder."""
    return get_vault_dir() / "03 - Topics"


def list_publications() -> list[Path]:
    """List all parsed publication files."""
    data_dir = get_data_dir()
    return sorted(data_dir.glob("pub_*.md"))


def extract_tables_with_llm(pub_path: Path, model: str, base_url: str, api_key: str) -> list[dict]:
    """Use LLM to identify and extract tables from a publication.

    Returns list of dicts with:
    - name: table name (for filename)
    - description: what the table contains
    - summary: 1-2 sentence summary for the index
    - related_topics: list of topic names this table relates to
    - headers: list of column headers
    - rows: list of row data
    """
    content = pub_path.read_text()

    # Truncate if too long
    max_chars = 50000
    if len(content) > max_chars:
        content = content[:max_chars] + "\n\n... [TRUNCATED] ..."

    prompt = f"""You are extracting structured tables from an IRS publication for conversion to CSV format.

The publication is: {pub_path.name}

Below is the parsed markdown content. Identify ALL tables that contain:
- Tax brackets or tax tables
- Standard deduction amounts
- Filing thresholds
- Credit amounts (EIC, Child Tax Credit, etc.)
- Contribution limits (IRA, 401k, etc.)
- Any numerical thresholds, limits, or calculations

For EACH table found, output a JSON object with:
- "name": A short filename-safe name (e.g., "standard_deduction_2025", "tax_table_single")
- "description": What the table contains (detailed)
- "summary": A 1-2 sentence summary for the index page
- "related_topics": Array of topic names this relates to (e.g., ["Filing Status", "Standard Deduction"])
- "headers": Array of column names
- "rows": Array of arrays with the data values

Output ONLY valid JSON array. If no tables found, output [].

Content:
{content}
"""

    try:
        with httpx.Client(timeout=600.0) as client:
            response = client.post(
                f"{base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1,
                },
            )
            response.raise_for_status()
            result = response.json()

        llm_content = result["choices"][0]["message"]["content"]

        # Extract JSON from response
        json_match = re.search(r"\[.*\]", llm_content, re.DOTALL)
        if json_match:
            tables = json.loads(json_match.group())
            return tables

    except Exception as e:
        print(f"  Error calling LLM: {e}")

    return []


def sanitize_filename(name: str) -> str:
    """Convert a name to a safe filename."""
    name = re.sub(r"[^a-z0-9_]", "_", name.lower())
    name = re.sub(r"_+", "_", name).strip("_")
    return name


def save_table_as_csv(table: dict, output_dir: Path) -> Path | None:
    """Save a table as CSV file."""
    name = sanitize_filename(table.get("name", "unknown_table"))
    csv_path = output_dir / f"{name}.csv"

    headers = table.get("headers", [])
    rows = table.get("rows", [])

    if not headers or not rows:
        return None

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    return csv_path


def create_companion_md(table: dict, assets_dir: Path, pub_name: str) -> Path:
    """Create a companion markdown file for a CSV with metadata and backlinks."""
    name = sanitize_filename(table.get("name", "unknown_table"))
    md_path = assets_dir / f"{name}.md"

    description = table.get("description", "Tax data table")
    related_topics = table.get("related_topics", [])
    summary = table.get("summary", description)

    # Format related topics as wikilinks
    topic_links = [f"  - [[{t}]]" for t in related_topics]
    topics_section = "\n".join(topic_links) if topic_links else "  - None"

    today = datetime.now().strftime("%Y-%m-%d")

    content = f"""---
type: table
created: {today}
updated: {today}
source: {pub_name}
related_topics:
{chr(10).join(f"  - [[{t}]]" for t in related_topics) if related_topics else "  - []"}
---

# {name.replace("_", " ").title()}

{description}

## Data

[[{name}.csv]]

## Related Topics

{topics_section}
"""

    md_path.write_text(content)
    return md_path


def update_assets_index(assets_dir: Path, tables: list[dict]) -> None:
    """Update the _index.md file with summaries and links."""
    index_path = assets_dir / "_index.md"

    # Group tables by category based on name/description
    categories = {
        "Filing Requirements": [],
        "Deductions": [],
        "Credits": [],
        "Income": [],
        "Retirement": [],
        "Other": [],
    }

    for table in tables:
        name = sanitize_filename(table.get("name", "unknown_table"))
        summary = table.get("summary", table.get("description", "Tax data table"))

        # Categorize based on keywords
        name_lower = name.lower()
        if "filing" in name_lower or "requirement" in name_lower:
            cat = "Filing Requirements"
        elif "deduction" in name_lower or "standard" in name_lower:
            cat = "Deductions"
        elif "credit" in name_lower or "eic" in name_lower or "ctc" in name_lower:
            cat = "Credits"
        elif "income" in name_lower or "bracket" in name_lower or "tax_table" in name_lower:
            cat = "Income"
        elif "ira" in name_lower or "401" in name_lower or "retirement" in name_lower:
            cat = "Retirement"
        else:
            cat = "Other"

        categories[cat].append((name, summary))

    # Build index content
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [
        "---",
        f"created: {today}",
        f"updated: {today}",
        "type: index",
        "tags:",
        "  - index",
        "  - assets",
        "---",
        "",
        "# Assets Index",
        "",
        "Supporting files including tables, images, and data files.",
        "",
    ]

    for category, items in categories.items():
        if items:
            lines.append(f"## {category}")
            lines.append("")
            for name, summary in items:
                lines.append(f"- [[{name}|{name.replace('_', ' ').title()}]] - {summary}")
            lines.append("")

    index_path.write_text("\n".join(lines))


def find_topic_note(topic_name: str) -> Path | None:
    """Find a topic note by name."""
    topics_dir = get_topics_dir()
    if not topics_dir.exists():
        return None

    # Try exact match first
    topic_path = topics_dir / f"{topic_name}.md"
    if topic_path.exists():
        return topic_path

    # Try case-insensitive match
    for md_file in topics_dir.glob("*.md"):
        if md_file.stem.lower() == topic_name.lower():
            return md_file

    return None


def update_topic_with_table_link(topic_path: Path, table_name: str, table_description: str) -> None:
    """Add a link to a table in a topic note."""
    content = topic_path.read_text()

    # Check if this table is already linked
    if f"[[04 - Assets/{table_name}" in content or f"[[{table_name}" in content:
        return

    # Find or create Related Tables section
    if "## Related Tables" in content:
        # Add to existing section
        lines = content.split("\n")
        new_lines = []
        in_tables_section = False
        added = False

        for line in lines:
            new_lines.append(line)
            if line.strip() == "## Related Tables":
                in_tables_section = True
            elif in_tables_section and line.startswith("## ") and not added:
                # Reached next section, add before it
                new_lines.insert(-1, f"- [[04 - Assets/{table_name}|{table_name.replace('_', ' ').title()}]] - {table_description}")
                added = True
                in_tables_section = False
            elif in_tables_section and not line.strip() and not added:
                # Empty line in tables section, add link before it
                new_lines.append(f"- [[04 - Assets/{table_name}|{table_name.replace('_', ' ').title()}]] - {table_description}")
                added = True

        if not added:
            # Add at end of tables section
            new_lines.append(f"- [[04 - Assets/{table_name}|{table_name.replace('_', ' ').title()}]] - {table_description}")

        content = "\n".join(new_lines)
    else:
        # Add new section before any final content
        section = f"""
## Related Tables

- [[04 - Assets/{table_name}|{table_name.replace('_', ' ').title()}]] - {table_description}
"""
        # Find a good place to insert (before the last heading or at end)
        lines = content.rstrip().split("\n")
        insert_pos = len(lines)

        # Look for existing sections to insert after
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].startswith("## ") and i < len(lines) - 1:
                insert_pos = i + 1
                break

        lines.insert(insert_pos, section.strip())
        content = "\n".join(lines)

    topic_path.write_text(content)


def extract_from_publication(
    pub_path: Path,
    model: str,
    base_url: str,
    api_key: str,
    use_llm: bool = True,
) -> list[dict]:
    """Extract tables from a single publication.

    Returns list of table dicts that were created.
    """
    print(f"\nProcessing: {pub_path.name}")

    assets_dir = get_assets_dir()
    created_tables = []

    if use_llm:
        tables = extract_tables_with_llm(pub_path, model, base_url, api_key)

        for table in tables:
            name = sanitize_filename(table.get("name", "unknown_table"))

            # Save CSV
            csv_path = save_table_as_csv(table, assets_dir)
            if csv_path:
                print(f"  Created: {name}.csv")

                # Create companion markdown
                md_path = create_companion_md(table, assets_dir, pub_path.name)
                print(f"  Created: {name}.md")

                # Update related topic notes
                related_topics = table.get("related_topics", [])
                description = table.get("summary", table.get("description", ""))
                for topic_name in related_topics:
                    topic_path = find_topic_note(topic_name)
                    if topic_path:
                        update_topic_with_table_link(topic_path, name, description)
                        print(f"  Updated topic: {topic_name}")

                created_tables.append(table)

    return created_tables


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract structured tables from IRS publications to CSV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Extract tables from all publications
    uv run python scripts/extract_assets.py

    # Extract from specific publication
    uv run python scripts/extract_assets.py --pub 17

    # List tables found without extracting
    uv run python scripts/extract_assets.py --list-tables
        """,
    )

    parser.add_argument(
        "--pub",
        type=str,
        help="Extract from specific publication number (e.g., 17, 501)",
    )

    parser.add_argument(
        "--list-tables",
        action="store_true",
        help="List tables found without extracting",
    )

    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="Use pattern matching only, skip LLM extraction",
    )

    args = parser.parse_args()

    # Get API configuration
    api_key = os.environ.get("OPENAI_API_KEY", "dummy")
    base_url = os.environ.get("OPENAI_BASE_URL", "http://localhost:8000/v1")
    model = os.environ.get("OPENAI_MODEL", "glm-5-fp8")

    # Get publications to process
    if args.pub:
        pub_files = []
        for p in list_publications():
            if f"pub_{args.pub}_" in p.name:
                pub_files.append(p)
        if not pub_files:
            print(f"Publication {args.pub} not found")
            sys.exit(1)
    else:
        pub_files = list_publications()

    print(f"Found {len(pub_files)} publications to process")

    if args.list_tables:
        # Just list tables found (pattern matching, no LLM)
        for pub_path in pub_files:
            content = pub_path.read_text()
            # Count markdown tables
            table_count = content.count("\n|")

            print(f"\n{pub_path.name}:")
            print(f"  Approximate tables: {table_count // 3}")

        return

    # Extract tables
    all_tables = []

    for pub_path in pub_files:
        tables = extract_from_publication(
            pub_path,
            model,
            base_url,
            api_key,
            use_llm=not args.no_llm,
        )
        all_tables.extend(tables)

    # Update index with summaries
    if all_tables:
        update_assets_index(get_assets_dir(), all_tables)
        print(f"\nUpdated _index.md with {len(all_tables)} tables")

    print(f"\nExtracted {len(all_tables)} tables to {get_assets_dir()}")


if __name__ == "__main__":
    main()
