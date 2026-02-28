# Turbo Tax - IRS Document Parsing Agent

## Project Overview

Turbo Tax is a Python project that parses IRS documents (forms, publications, instructions) from the web using Docling, extracts structured information, and writes organized notes to an Obsidian vault.

**Architecture:**
```
IRS Website (PDF/HTML) → Docling Parser → Extraction Agent → Obsidian Vault (Markdown)
```

**Current Status:**
- ✅ Phase 1: Core Parser implemented (`src/turbo_tax/parser/`)
- 🚧 Phase 2: Extraction Agent (planned)
- 🚧 Phase 3: Obsidian Integration (planned)

## Tech Stack

- **Python:** 3.13+
- **Package Manager:** uv
- **Document Parsing:** Docling (IBM's document understanding library)
- **Validation:** Pydantic
- **HTTP Client:** httpx
- **Linting/Formatting:** Ruff
- **Testing:** pytest + pytest-asyncio
- **Pre-commit:** ruff + standard hooks

## Project Structure

```
turbo-tax/
├── src/turbo_tax/
│   ├── __init__.py
│   └── parser/              # Phase 1: Docling-based IRS parser
│       ├── __init__.py
│       ├── models.py        # Pydantic models (DocumentType, Table, Section, ParsedDocument)
│       └── parser.py        # IRSParser class
├── scripts/                 # Development/test scripts
│   ├── test_parse_irs.py
│   └── save_parsed_output.py
├── tests/                   # Unit tests
│   └── test_parser.py
├── obsidian_db/turbo_tax/   # Obsidian vault for output
├── data/                    # Parsed output (JSON, Markdown)
├── SPEC.md                  # Full project specification
└── pyproject.toml           # Project configuration
```

## Commands

```bash
# Run tests
uv run pytest -v

# Run linter
uv run ruff check .

# Run formatter
uv run ruff format .

# Parse an IRS document (from script)
uv run python scripts/save_parsed_output.py

# Test parsing interactively
uv run python scripts/test_parse_irs.py

# Install pre-commit hooks (already done)
uv run pre-commit install
```

## Key Classes

### `IRSParser` (src/turbo_tax/parser/parser.py)
```python
parser = IRSParser()
doc = await parser.parse_url("https://www.irs.gov/pub/irs-pdf/f1040.pdf")
# Returns ParsedDocument with: title, document_type, form_number, tax_year, sections, tables, full_text
```

### Data Models (src/turbo_tax/parser/models.py)
- `DocumentType`: FORM, INSTRUCTIONS, PUBLICATION, SCHEDULE, UNKNOWN
- `ParsedDocument`: Main container for parsed content
- `Section`: Document sections with title, level, content
- `Table`: Extracted tables with headers/rows, can export to markdown/CSV

## IRS Document Sources

- Forms: `https://www.irs.gov/pub/irs-pdf/f{form_number}.pdf`
- Instructions: `https://www.irs.gov/pub/irs-pdf/i{form_number}.pdf`
- Publications: `https://www.irs.gov/pub/irs-pdf/p{pub_number}.pdf`
- Index: `https://www.irs.gov/forms-instructions-and-publications`

## Development Conventions

- Use `uv run` for all Python commands
- Commit messages follow conventional format: `feat:`, `fix:`, `chore:`
- Ruff handles all linting/formatting with extensive rule set (see pyproject.toml)
- Tests go in `tests/` directory
- Scripts go in `scripts/` directory

## Obsidian Vault Location

`obsidian_db/turbo_tax/` - This is where extracted documents should be written.

## Next Steps

1. Build extraction agent (`src/turbo_tax/agent/`)
2. Implement Obsidian vault writer
3. Add CLI interface
