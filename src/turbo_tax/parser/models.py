"""Data models for parsed IRS documents."""

from enum import StrEnum

from pydantic import BaseModel, Field


class DocumentType(StrEnum):
    """Type of IRS document."""

    FORM = "form"
    INSTRUCTIONS = "instructions"
    PUBLICATION = "publication"
    SCHEDULE = "schedule"
    UNKNOWN = "unknown"


class Table(BaseModel):
    """A table extracted from a document."""

    title: str | None = None
    headers: list[str] = Field(default_factory=list)
    rows: list[list[str]] = Field(default_factory=list)
    page_number: int | None = None

    def to_markdown(self) -> str:
        """Convert table to markdown format."""
        if not self.headers and not self.rows:
            return ""

        lines = []

        if self.title:
            lines.append(f"**{self.title}**\n")

        if self.headers:
            lines.append("| " + " | ".join(self.headers) + " |")
            lines.append("| " + " | ".join("---" for _ in self.headers) + " |")

        lines.extend("| " + " | ".join(row) + " |" for row in self.rows)

        return "\n".join(lines)

    def to_csv(self) -> str:
        """Convert table to CSV format."""
        lines = []

        if self.headers:
            lines.append(",".join(self.headers))

        lines.extend(",".join(row) for row in self.rows)

        return "\n".join(lines)


class Section(BaseModel):
    """A section or heading within a document."""

    title: str
    level: int = 1
    content: str = ""
    page_number: int | None = None
    subsections: list["Section"] = Field(default_factory=list)

    def to_markdown(self) -> str:
        """Convert section to markdown format."""
        prefix = "#" * self.level
        lines = [f"{prefix} {self.title}"]

        if self.content:
            lines.append("")
            lines.append(self.content)

        for subsection in self.subsections:
            lines.append("")
            lines.append(subsection.to_markdown())

        return "\n".join(lines)


class ParsedDocument(BaseModel):
    """A parsed IRS document."""

    source_url: str
    title: str | None = None
    document_type: DocumentType = DocumentType.UNKNOWN
    form_number: str | None = None
    tax_year: int | None = None
    revision_date: str | None = None
    summary: str | None = None

    sections: list[Section] = Field(default_factory=list)
    tables: list[Table] = Field(default_factory=list)

    full_text: str | None = None
    page_count: int | None = None

    def to_markdown(self) -> str:
        """Convert document to markdown format."""
        lines = []

        if self.title:
            lines.append(f"# {self.title}")
            lines.append("")

        if self.summary:
            lines.append("## Summary")
            lines.append("")
            lines.append(self.summary)
            lines.append("")

        if self.sections:
            lines.append("## Contents")
            lines.append("")
            for section in self.sections:
                lines.append(section.to_markdown())
                lines.append("")

        if self.tables:
            lines.append("## Tables")
            lines.append("")
            for table in self.tables:
                lines.append(table.to_markdown())
                lines.append("")

        return "\n".join(lines)


class ExtractedContent(BaseModel):
    """Extracted and structured content ready for Obsidian."""

    document: ParsedDocument

    # Extracted metadata
    overview: str | None = None
    key_topics: list[str] = Field(default_factory=list)
    filing_requirements: list[str] = Field(default_factory=list)
    related_forms: list[str] = Field(default_factory=list)

    # Generated content
    obsidian_note: str | None = None
