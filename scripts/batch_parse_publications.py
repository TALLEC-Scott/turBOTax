"""Batch parse all IRS publications and save to markdown."""

import asyncio
import logging
from pathlib import Path

from turbo_tax.parser import IRSParser

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# IRS Publications to parse
PUBLICATIONS = {
    # 2025 Tax Year Publications
    "2025": [
        3,
        17,
        54,
        225,
        334,
        501,
        502,
        503,
        504,
        505,
        514,
        515,
        517,
        519,
        525,
        526,
        527,
        530,
        537,
        544,
        547,
        551,
        554,
        557,
        559,
        560,
        570,
        575,
        590,
        596,
        907,
        908,
        915,
        925,
        936,
        939,
        969,
        970,
        974,
        1040,
        1212,
        4681,
    ],
    # 2026 Tax Year Publications (already released)
    "2026": [15, 509, 571, 926],
}

# Publications with hyphenated names (special cases)
SPECIAL_NAMES = {
    590: "590a",  # 590-A
}


async def parse_publication(
    parser: IRSParser,
    pub_number: int,
    year: str,
    output_dir: Path,
) -> bool:
    """Parse a single publication and save to markdown.

    Returns True if successful, False otherwise.
    """
    # Handle special naming
    pub_name = SPECIAL_NAMES.get(pub_number, str(pub_number))
    pdf_url = f"https://www.irs.gov/pub/irs-pdf/p{pub_name}.pdf"

    output_file = output_dir / f"pub_{pub_number}_{year}.md"

    # Skip if already parsed
    if output_file.exists():
        logger.info("  [SKIP] Pub %s already exists", pub_number)
        return True

    try:
        logger.info("  [PARSING] Pub %s (%s)...", pub_number, year)
        doc = await parser.parse_url(pdf_url)

        # Create markdown content
        content_parts = [
            f"# Publication {pub_number} - {doc.title or 'IRS Publication'}",
            "",
            f"**Tax Year:** {year}",
            f"**Source:** {pdf_url}",
            f"**Document Type:** {doc.document_type}",
            "",
            "---",
            "",
        ]

        # Add summary if available
        if doc.summary:
            content_parts.extend(
                [
                    "## Summary",
                    "",
                    doc.summary,
                    "",
                ]
            )

        # Add sections
        if doc.sections:
            content_parts.append("## Contents")
            content_parts.append("")
            for section in doc.sections:
                content_parts.append(section.to_markdown())
                content_parts.append("")

        # Add tables
        if doc.tables:
            content_parts.append("## Tables")
            content_parts.append("")
            for i, table in enumerate(doc.tables):
                content_parts.append(f"### Table {i + 1}")
                content_parts.append("")
                content_parts.append(table.to_markdown())
                content_parts.append("")

        # Add full text
        if doc.full_text:
            content_parts.append("## Full Text")
            content_parts.append("")
            content_parts.append(doc.full_text)

        # Write to file
        output_file.write_text("\n".join(content_parts))
        logger.info("  [SAVED] %s", output_file)
        return True

    except Exception as e:
        logger.exception("  [ERROR] Pub %s", pub_number)
        return False


async def main() -> None:
    """Parse all IRS publications."""
    output_dir = Path("data/irs_publications")
    output_dir.mkdir(parents=True, exist_ok=True)

    parser = IRSParser()

    total = 0
    success = 0
    failed = []

    for year, pub_numbers in PUBLICATIONS.items():
        logger.info("\n%s", "=" * 60)
        logger.info("Parsing %s Publications (%d total)", year, len(pub_numbers))
        logger.info("=" * 60)

        for pub_number in pub_numbers:
            total += 1
            result = await parse_publication(parser, pub_number, year, output_dir)
            if result:
                success += 1
            else:
                failed.append((pub_number, year))

    await parser.close()

    # Summary
    logger.info("\n%s", "=" * 60)
    logger.info("SUMMARY")
    logger.info("=" * 60)
    logger.info("Total: %d", total)
    logger.info("Success: %d", success)
    logger.info("Failed: %d", len(failed))

    if failed:
        logger.info("\nFailed publications:")
        for pub_num, year in failed:
            logger.info("  - Pub %d (%s)", pub_num, year)


if __name__ == "__main__":
    asyncio.run(main())
