"""IRS Document Parser using Docling."""

import logging
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx
from docling.document_converter import DocumentConverter

from turbo_tax.parser.models import (
    DocumentType,
    ParsedDocument,
    Section,
    Table,
)

logger = logging.getLogger(__name__)

# IRS document patterns
FORM_PATTERN = re.compile(r"Form\s+(\d+[A-Z\-]*)", re.IGNORECASE)
SCHEDULE_PATTERN = re.compile(r"Schedule\s+([A-Z])", re.IGNORECASE)
PUBLICATION_PATTERN = re.compile(r"Publication\s+(\d+)", re.IGNORECASE)
INSTRUCTIONS_PATTERN = re.compile(r"Instructions\s+for", re.IGNORECASE)
TAX_YEAR_PATTERN = re.compile(r"\b(20\d{2})\b")


class IRSParser:
    """Parse IRS documents using Docling."""

    def __init__(
        self,
        cache_dir: Path | None = None,
        timeout: int = 300,
    ) -> None:
        """Initialize the parser.

        Args:
            cache_dir: Directory for caching downloaded documents.
            timeout: Timeout in seconds for downloads.
        """
        self.converter = DocumentConverter()
        self.cache_dir = cache_dir or Path(".cache/docling")
        self.timeout = timeout
        self._http_client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._http_client is None:
            self._http_client = httpx.AsyncClient(
                timeout=self.timeout,
                follow_redirects=True,
            )
        return self._http_client

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._http_client:
            await self._http_client.aclose()
            self._http_client = None

    def _extract_form_number(self, title: str | None, url: str) -> str | None:
        """Extract form number from title or URL."""
        # Try title first
        if title:
            for pattern in [FORM_PATTERN, SCHEDULE_PATTERN, PUBLICATION_PATTERN]:
                match = pattern.search(title)
                if match:
                    return match.group(0)

        # Try URL
        url_path = urlparse(url).path
        filename = Path(url_path).stem

        # Handle IRS PDF naming conventions
        # f1040.pdf -> Form 1040
        # f1040sa.pdf -> Schedule A
        # p17.pdf -> Publication 17
        # i1040.pdf -> Instructions for 1040
        if filename.startswith("f") and not filename.startswith("f1040s"):
            # It's a form
            form_num = filename[1:]
            return f"Form {form_num.upper()}"
        if filename.startswith("f1040s"):
            # It's a schedule (f1040sa, f1040sb, etc.)
            schedule_letter = filename[-1].upper()
            return f"Schedule {schedule_letter}"
        if filename.startswith("i"):
            # It's instructions
            form_num = filename[1:]
            return f"Instructions for Form {form_num.upper()}"
        if filename.startswith("p"):
            # It's a publication
            pub_num = filename[1:]
            return f"Publication {pub_num}"

        return None

    def _classify_document(
        self,
        title: str | None,
        url: str,
        form_number: str | None,
    ) -> DocumentType:
        """Classify document type from title/URL."""
        url_lower = url.lower()
        title_lower = (title or "").lower()

        # Check for instructions
        if (
            ("i" in url_lower or "instructions" in title_lower)
            and form_number
            and "instructions" in form_number.lower()
        ):
            return DocumentType.INSTRUCTIONS

        # Check for publication
        if url_lower.startswith("p") or "publication" in title_lower:
            return DocumentType.PUBLICATION

        # Check for schedule
        if form_number and "schedule" in form_number.lower():
            return DocumentType.SCHEDULE

        # Default to form
        if form_number:
            return DocumentType.FORM

        return DocumentType.UNKNOWN

    def _extract_tax_year(self, title: str | None, content: str) -> int | None:
        """Extract tax year from document."""
        # Look in title first
        if title:
            match = TAX_YEAR_PATTERN.search(title)
            if match:
                return int(match.group(1))

        # Look in first 1000 chars of content
        match = TAX_YEAR_PATTERN.search(content[:1000])
        if match:
            return int(match.group(1))

        return None

    def _convert_table(self, docling_table: Any) -> Table:
        """Convert Docling table to our Table model."""
        table_data = docling_table.export_to_dataframe()

        headers = list(table_data.columns)
        headers = [str(h) for h in headers]

        rows = []
        for _, row in table_data.iterrows():
            rows.append([str(cell) for cell in row])

        return Table(
            title=None,
            headers=headers,
            rows=rows,
        )

    def _extract_sections(self, docling_doc: Any) -> list[Section]:
        """Extract sections from Docling document."""
        sections: list[Section] = []

        # Get text export for structure analysis
        text = docling_doc.export_to_markdown()

        # Split into lines and find headers
        lines = text.split("\n")
        current_section: Section | None = None
        current_content: list[str] = []

        for line in lines:
            # Check for markdown headers
            if line.startswith("#"):
                header_match = re.match(r"^(#+)\s+(.+)$", line)
                if header_match:
                    level = len(header_match.group(1))
                    title = header_match.group(2).strip()

                    # Save previous section
                    if current_section:
                        current_section.content = "\n".join(current_content).strip()
                        sections.append(current_section)

                    current_section = Section(
                        title=title,
                        level=level,
                    )
                    current_content = []
            elif current_section:
                current_content.append(line)

        # Save last section
        if current_section:
            current_section.content = "\n".join(current_content).strip()
            sections.append(current_section)

        return sections

    async def parse_url(self, url: str) -> ParsedDocument:
        """Parse an IRS document from URL.

        Args:
            url: URL to the IRS document (PDF or HTML).

        Returns:
            ParsedDocument with extracted content.
        """
        logger.info("Parsing document from URL: %s", url)

        # Use Docling to convert the document
        result = self.converter.convert(url)
        docling_doc = result.document

        # Export to different formats
        markdown_text = docling_doc.export_to_markdown()
        doc_dict = result.document.export_to_dict()

        # Extract title
        title = doc_dict.get("title") or doc_dict.get("name")

        # Extract form number
        form_number = self._extract_form_number(title, url)

        # Classify document type
        doc_type = self._classify_document(title, url, form_number)

        # Extract tax year
        tax_year = self._extract_tax_year(title, markdown_text)

        # Extract tables
        tables: list[Table] = []
        if hasattr(docling_doc, "tables"):
            tables.extend(self._convert_table(t) for t in docling_doc.tables)

        # Extract sections
        sections = self._extract_sections(docling_doc)

        # Get page count
        page_count = doc_dict.get("page_count")

        return ParsedDocument(
            source_url=url,
            title=title,
            document_type=doc_type,
            form_number=form_number,
            tax_year=tax_year,
            sections=sections,
            tables=tables,
            full_text=markdown_text,
            page_count=page_count,
        )

    def parse_file(self, file_path: Path) -> ParsedDocument:
        """Parse an IRS document from a local file.

        Args:
            file_path: Path to the document file.

        Returns:
            ParsedDocument with extracted content.
        """
        logger.info("Parsing document from file: %s", file_path)

        result = self.converter.convert(str(file_path))
        docling_doc = result.document

        markdown_text = docling_doc.export_to_markdown()
        doc_dict = result.document.export_to_dict()

        title = doc_dict.get("title") or doc_dict.get("name") or file_path.stem
        url = f"file://{file_path.absolute()}"

        form_number = self._extract_form_number(title, url)
        doc_type = self._classify_document(title, url, form_number)
        tax_year = self._extract_tax_year(title, markdown_text)

        tables: list[Table] = []
        if hasattr(docling_doc, "tables"):
            tables.extend(self._convert_table(t) for t in docling_doc.tables)

        sections = self._extract_sections(docling_doc)
        page_count = doc_dict.get("page_count")

        return ParsedDocument(
            source_url=url,
            title=title,
            document_type=doc_type,
            form_number=form_number,
            tax_year=tax_year,
            sections=sections,
            tables=tables,
            full_text=markdown_text,
            page_count=page_count,
        )
