"""Tests for parser models."""

from turbo_tax.parser.models import DocumentType, ParsedDocument, Section, Table


class TestTable:
    """Tests for Table model."""

    def test_to_markdown_empty(self) -> None:
        """Test markdown conversion with empty table."""
        table = Table()
        assert table.to_markdown() == ""

    def test_to_markdown_with_headers(self) -> None:
        """Test markdown conversion with headers and rows."""
        table = Table(
            title="Test Table",
            headers=["Column A", "Column B"],
            rows=[["Value 1", "Value 2"], ["Value 3", "Value 4"]],
        )
        md = table.to_markdown()
        assert "**Test Table**" in md
        assert "| Column A | Column B |" in md
        assert "| Value 1 | Value 2 |" in md

    def test_to_csv(self) -> None:
        """Test CSV conversion."""
        table = Table(
            headers=["A", "B"],
            rows=[["1", "2"], ["3", "4"]],
        )
        csv = table.to_csv()
        assert "A,B" in csv
        assert "1,2" in csv
        assert "3,4" in csv


class TestSection:
    """Tests for Section model."""

    def test_to_markdown_simple(self) -> None:
        """Test markdown conversion of simple section."""
        section = Section(title="Introduction", level=1, content="Some content.")
        md = section.to_markdown()
        assert "# Introduction" in md
        assert "Some content." in md

    def test_to_markdown_nested(self) -> None:
        """Test markdown conversion with nested sections."""
        section = Section(
            title="Main",
            level=1,
            content="Main content.",
            subsections=[
                Section(title="Sub", level=2, content="Sub content."),
            ],
        )
        md = section.to_markdown()
        assert "# Main" in md
        assert "## Sub" in md


class TestParsedDocument:
    """Tests for ParsedDocument model."""

    def test_basic_document(self) -> None:
        """Test basic document creation."""
        doc = ParsedDocument(
            source_url="https://example.com/form.pdf",
            title="Form 1040",
            document_type=DocumentType.FORM,
            form_number="Form 1040",
            tax_year=2024,
        )
        assert doc.source_url == "https://example.com/form.pdf"
        assert doc.document_type == DocumentType.FORM

    def test_to_markdown(self) -> None:
        """Test document markdown conversion."""
        doc = ParsedDocument(
            source_url="https://example.com/form.pdf",
            title="Form 1040",
            summary="A summary.",
            sections=[
                Section(title="Part 1", level=2, content="Content."),
            ],
            tables=[
                Table(headers=["A"], rows=[["1"]]),
            ],
        )
        md = doc.to_markdown()
        assert "# Form 1040" in md
        assert "## Summary" in md
        assert "## Contents" in md
        assert "## Tables" in md
