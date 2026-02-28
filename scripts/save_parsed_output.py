"""Parse IRS document and save output to data directory."""

import asyncio
from pathlib import Path

from turbo_tax.parser import IRSParser


async def main() -> None:
    """Parse IRS document and save to files."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    # Parse Form 1040
    url = "https://www.irs.gov/pub/irs-pdf/f1040.pdf"

    print(f"Parsing: {url}")
    parser = IRSParser()
    doc = await parser.parse_url(url)
    await parser.close()

    # Save as JSON
    json_path = data_dir / "f1040_parsed.json"
    json_path.write_text(doc.model_dump_json(indent=2))
    print(f"Saved JSON: {json_path}")

    # Save as Markdown
    md_path = data_dir / "f1040_parsed.md"
    md_path.write_text(doc.to_markdown())
    print(f"Saved Markdown: {md_path}")

    # Save full text
    if doc.full_text:
        text_path = data_dir / "f1040_full_text.md"
        text_path.write_text(doc.full_text)
        print(f"Saved full text: {text_path}")

    print("\nDone!")


if __name__ == "__main__":
    asyncio.run(main())
