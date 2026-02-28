"""Test script to parse IRS documents."""

import asyncio

from turbo_tax.parser import IRSParser


async def main() -> None:
    """Parse an IRS document and print results."""
    # Test URLs - 2025 tax documents
    test_urls = [
        "https://www.irs.gov/pub/irs-pdf/f1040.pdf",  # Form 1040
        # Form 1040 Instructions (large file):
        # "https://www.irs.gov/pub/irs-pdf/i1040gi.pdf",
    ]

    parser = IRSParser()

    for url in test_urls:
        print(f"\n{'=' * 60}")
        print(f"Parsing: {url}")
        print("=" * 60)

        try:
            doc = await parser.parse_url(url)

            print(f"\nTitle: {doc.title}")
            print(f"Type: {doc.document_type}")
            print(f"Form Number: {doc.form_number}")
            print(f"Tax Year: {doc.tax_year}")
            print(f"Page Count: {doc.page_count}")
            print(f"Sections Found: {len(doc.sections)}")
            print(f"Tables Found: {len(doc.tables)}")

            # Print first few sections
            if doc.sections:
                print("\n--- First 5 Sections ---")
                for section in doc.sections[:5]:
                    print(f"  [{section.level}] {section.title}")

            # Print table info
            if doc.tables:
                print("\n--- Tables ---")
                for i, table in enumerate(doc.tables[:3]):
                    rows = len(table.rows)
                    cols = len(table.headers)
                    print(f"  Table {i + 1}: {cols} cols, {rows} rows")
                    if table.headers:
                        print(f"    Headers: {table.headers[:3]}...")

            # Print first 500 chars of text
            if doc.full_text:
                print("\n--- Preview (first 500 chars) ---")
                print(doc.full_text[:500])

        except Exception as e:
            print(f"Error parsing {url}: {e}")
            raise

    await parser.close()
    print("\nDone!")


if __name__ == "__main__":
    asyncio.run(main())
