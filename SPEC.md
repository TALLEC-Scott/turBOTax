# Turbo Tax - IRS Document Parsing Agent

## Overview

Build an agent that parses IRS documents (forms, publications, instructions) from the web using Docling, extracts structured information, and writes organized notes to an Obsidian vault.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   IRS Website   │────▶│    Docling      │────▶│     Agent       │
│  (PDF/HTML)     │     │    Parser       │     │   (Orchestrator)│
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │  Obsidian Vault │
                                                │  (Markdown)     │
                                                └─────────────────┘
```

## Components

### 1. Docling Parser Module (`src/turbo_tax/parser/`)

Responsible for fetching and parsing IRS documents.

**Features:**
- Parse PDF and HTML documents from IRS website
- Extract structured content (text, tables, sections)
- Handle multi-page documents with proper chunking
- Export to structured JSON/Markdown

**Key Classes:**
```python
class IRSParser:
    """Parse IRS documents using Docling."""

    async def parse_url(url: str) -> ParsedDocument
    async def parse_pdf(file_path: Path) -> ParsedDocument
    def extract_tables(doc: ParsedDocument) -> list[Table]
    def extract_sections(doc: ParsedDocument) -> list[Section]
```

### 2. Extraction Agent (`src/turbo_tax/agent/`)

Orchestrates parsing and extracts relevant information.

**Responsibilities:**
- Identify document type (form, publication, instructions)
- Extract key information (form numbers, tax years, instructions)
- Generate summaries and structured data
- Create Obsidian-compatible markdown

**Key Classes:**
```python
class ExtractionAgent:
    """Agent for extracting and structuring IRS document content."""

    async def process_document(url: str) -> ExtractedContent
    def classify_document(content: ParsedDocument) -> DocumentType
    def generate_summary(content: ParsedDocument) -> str
    def to_obsidian_note(content: ExtractedContent) -> ObsidianNote
```

### 3. Obsidian Vault Writer (`src/turbo_tax/vault/`)

Writes structured notes to the Obsidian vault.

**Features:**
- Create notes with proper YAML frontmatter
- Organize by document type and year
- Handle attachments (images, tables as CSV)
- Update existing notes (incremental updates)

## Obsidian Vault Structure

```
vault/
├── 00 - Templates/
│   ├── Tax Form.md
│   ├── Publication.md
│   └── Instructions.md
├── 01 - Tax Forms/
│   ├── 2024/
│   │   ├── Form 1040.md
│   │   ├── Form 1040 Instructions.md
│   │   └── Schedule A.md
│   └── 2023/
│       └── ...
├── 02 - Publications/
│   ├── Publication 17 - Your Federal Income Tax.md
│   ├── Publication 501 - Dependents.md
│   └── ...
├── 03 - Topics/
│   ├── Deductions.md
│   ├── Credits.md
│   └── Filing Status.md
├── 04 - Assets/
│   ├── images/
│   └── tables/
└── Map of Contents.md
```

## Note Templates

### Tax Form Template

```markdown
---
created: {{date}}
updated: {{date}}
type: tax-form
form_number: {{form_number}}
tax_year: {{tax_year}}
revision_date: {{revision_date}}
source_url: {{source_url}}
tags: [tax-form, {{tax_year}}, {{category}}]
status: extracted
---

# {{form_number}} - {{title}}

## Overview

{{overview}}

## Filing Requirements

{{filing_requirements}}

## Instructions

{{instructions_summary}}

## Related Forms

- [[Related Form 1]]
- [[Related Form 2]]

## Attachments

- [Form PDF]({{pdf_path}})
- [Instructions PDF]({{instructions_pdf_path}})

## Source

- IRS Website: {{source_url}}
- Last Updated: {{revision_date}}
```

### Publication Template

```markdown
---
created: {{date}}
updated: {{date}}
type: publication
publication_number: {{pub_number}}
title: {{title}}
tax_year: {{tax_year}}
source_url: {{source_url}}
tags: [publication, {{category}}]
status: extracted
---

# {{pub_number}} - {{title}}

## Summary

{{summary}}

## Key Topics

{{key_topics}}

## Important Rules

{{important_rules}}

## Examples

{{examples}}

## Tables

{{tables}}

## Related Publications

- [[Publication X]]
- [[Publication Y]]

## Source

- IRS Website: {{source_url}}
```

## MCP Tool Integration

The agent will use filesystem MCP to write to the Obsidian vault:

```python
# Write note to vault
mcp__filesystem__write_file(
    path="vault/01 - Tax Forms/2024/Form 1040.md",
    content=note_content
)

# Create attachments
mcp__filesystem__write_file(
    path="vault/04 - Assets/tables/form_1040_schedule.csv",
    content=table_csv
)
```

## Initial Test URLs

Start with these IRS documents for testing:

1. **Form 1040 (Individual Income Tax Return)**
   - PDF: `https://www.irs.gov/pub/irs-pdf/f1040.pdf`
   - Instructions: `https://www.irs.gov/pub/irs-pdf/i1040.pdf`

2. **Publication 17 (Your Federal Income Tax)**
   - HTML: `https://www.irs.gov/publications/p17`
   - PDF: `https://www.irs.gov/pub/irs-pdf/p17.pdf`

3. **Form 1040 Schedule A (Itemized Deductions)**
   - PDF: `https://www.irs.gov/pub/irs-pdf/f1040sa.pdf`

## Implementation Phases

### Phase 1: Core Parser (Week 1)
- [ ] Set up Docling integration
- [ ] Implement IRSParser class
- [ ] Handle PDF and HTML parsing
- [ ] Extract tables and sections

### Phase 2: Extraction Agent (Week 2)
- [ ] Implement document classification
- [ ] Create extraction prompts
- [ ] Generate structured summaries
- [ ] Handle multi-document workflows

### Phase 3: Obsidian Integration (Week 3)
- [ ] Create vault structure
- [ ] Implement note templates
- [ ] Write notes via filesystem
- [ ] Handle attachments

### Phase 4: Testing & Refinement (Week 4)
- [ ] Test with various document types
- [ ] Improve extraction accuracy
- [ ] Add error handling
- [ ] Document usage

## Dependencies

```toml
[project]
dependencies = [
    "docling>=2.0.0",
    "httpx>=0.27.0",
    "pydantic>=2.0.0",
    "pyyaml>=6.0.0",
]

[dependency-groups]
dev = [
    "pytest>=9.0.0",
    "pytest-asyncio>=0.23.0",
    "ruff>=0.15.0",
    "pre-commit>=4.5.0",
]
```

## CLI Usage

```bash
# Parse a single IRS document
uv run turbo-tax parse https://www.irs.gov/pub/irs-pdf/f1040.pdf

# Parse and write to vault
uv run turbo-tax parse https://www.irs.gov/pub/irs-pdf/f1040.pdf --vault ./vault

# Batch process from file
uv run turbo-tax batch urls.txt --vault ./vault

# List available forms
uv run turbo-tax list-forms --year 2024
```

## Configuration

```yaml
# config.yaml
vault:
  path: ./vault
  templates: ./vault/00 - Templates

parser:
  cache_dir: ./.cache/docling
  model: docling-default

agent:
  max_retries: 3
  timeout: 300

irs:
  base_url: https://www.irs.gov
  forms_index: /forms-instructions-and-publications
```
