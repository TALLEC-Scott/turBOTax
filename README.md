# Turbo Tax

This is an experimental Knowledge Graph based agent for IRS Q&A done in a weekend for the Mistral AI World Hackathon 2026

## Screenshots

### Obsidian Vault

<img width="500" height="500" alt="Tax Assistant Web Interface" src="https://github.com/user-attachments/assets/aa65d06d-4595-4240-a3cf-b7e166f9f22e" />

### Web Interface

<img width="500" height="500" alt="Obsidian Vault Knowledge Graph" src="https://github.com/user-attachments/assets/cddf0d2e-3e15-4993-812e-168dff6267a2" />

## Features

- **Document Parsing**: Parse IRS PDFs and HTML using Docling
- **AI-Powered Extraction**: LLM agents extract and structure content
- **Knowledge Graph**: Explore relationships between tax topics via wikilinks
- **Interactive Frontend**: React UI with Cytoscape graph visualization
- **Obsidian Integration**: Auto-generated markdown notes with frontmatter

## Quick Start

### Prerequisites

- Python 3.13+
- Node.js 18+ (for frontend)
- [uv](https://docs.astral.sh/uv/) package manager

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/TALLEC-Scott/turbo-tax.git
   cd turbo-tax
   ```

2. Install Python dependencies:
   ```bash
   uv sync
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your LLM API credentials
   ```

4. Install frontend dependencies:
   ```bash
   cd frontend && npm install
   ```

### Run

**Backend:**
```bash
uv run uvicorn src.turbo_tax.api.server:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend && npm run dev
```

The application will be available at `http://localhost:5173`

## Project Structure

```
turbo-tax/
├── src/turbo_tax/
│   ├── parser/          # Docling-based IRS document parser
│   └── api/             # FastAPI backend with tool-calling agent
├── frontend/            # React + TypeScript frontend
├── scripts/             # Automation and distillation scripts
├── tests/               # Unit tests
├── obsidian_db/         # Generated Obsidian vault
└── data/                # Parsed document outputs
```

## Usage

### Parse IRS Documents

```python
from turbo_tax.parser import IRSParser

parser = IRSParser()
doc = await parser.parse_url("https://www.irs.gov/pub/irs-pdf/f1040.pdf")
print(doc.to_markdown())
```

### Run Distillation Pipeline

Process publications and extract structured content:

```bash
# Single publication
podman-compose run --rm distill 17

# All publications
podman-compose run --rm distill-all
```

### API Endpoints

| Endpoint | Description |
|----------|-------------|
| `WS /ws/chat` | WebSocket chat with streaming tool calls |
| `GET /api/vault/stats` | Vault statistics |
| `GET /api/vault/indices` | List index files |

## Development

```bash
# Run tests
uv run pytest -v

# Lint and format
uv run ruff check .
uv run ruff format .

# Run all checks
uv run pytest -v && uv run ruff check .
```

## Docker

Build and run with Podman:

```bash
# Build image
podman-compose build

# Interactive agent session
podman-compose run --rm agent

# Extract tables from publications
podman-compose run --rm extract-assets 17
```

## IRS Document URLs

| Type | URL Pattern |
|------|-------------|
| Forms | `https://www.irs.gov/pub/irs-pdf/f{number}.pdf` |
| Instructions | `https://www.irs.gov/pub/irs-pdf/i{number}.pdf` |
| Publications | `https://www.irs.gov/pub/irs-pdf/p{number}.pdf` |

## Obsidian Vault Structure

The knowledge base is stored in an Obsidian vault at `obsidian_db/turbo_tax/`. Notes are organized by type and connected via wikilinks to form a navigable knowledge graph.

### Directory Layout

```
obsidian_db/turbo_tax/
├── 00 - Templates/         # Note templates for generation
├── 01 - Tax Forms/         # Tax forms organized by year
│   └── _index.md
├── 02 - Publications/      # IRS publications (47+ publications)
│   ├── Pub 17 - Your Federal Income Tax.md
│   ├── Pub 501 - Dependents, Standard Deduction, and Filing Information.md
│   └── ...
├── 03 - Topics/            # Thematic topic notes (200+ topics)
│   ├── Earned Income Credit.md
│   ├── Standard Deduction.md
│   └── ...
└── 04 - Assets/            # Extracted tables and reference data
    ├── standard_deduction_2025.csv
    └── eic_eligibility_rules_summary_2025.csv
```

### Note Types

Notes are classified by `type` in YAML frontmatter:

| Type | Location | Description |
|------|----------|-------------|
| `publication` | `02 - Publications/` | IRS publications (Pub 17, Pub 501, etc.) |
| `tax-form` | `01 - Tax Forms/` | Tax forms organized by tax year |
| `topic` | `03 - Topics/` | Thematic notes connecting related concepts |
| `index` | `*_index.md` | Index files organizing content by category |
| `asset` | `04 - Assets/` | Extracted tables as CSV/Markdown |

### Frontmatter Examples

**Publication:**
```yaml
---
type: publication
publication_number: "17"
title: "Your Federal Income Tax"
tax_year: 2025
source: https://www.irs.gov/pub/irs-pdf/p17.pdf
tags: [publication, individuals]
---
```

**Topic:**
```yaml
---
type: topic
category: Credits
tags: [credits, refundable, low-income]
---
```

### Topic Categories

| Category | Examples |
|----------|----------|
| Filing Status | Single, Married Filing Jointly, Head of Household |
| Dependents | Qualifying Child, Qualifying Relative |
| Deductions | Standard Deduction, Itemized Deductions |
| Credits | Child Tax Credit, Earned Income Credit |
| Income | Interest Income, Social Security Benefits |
| Employment Tax | FICA, FUTA, Withholding |
| International | Foreign Earned Income Exclusion, Foreign Tax Credit |

### Knowledge Graph

Notes are interconnected via wikilinks:

```markdown
# From Earned Income Credit.md

## Related Topics
- [[Qualifying Child]]
- [[Tax Credits]]

## Related Publications
- [[Pub 596 - Earned Income Credit]]
- [[Pub 17 - Your Federal Income Tax]]

## Related Forms
- [[Form 1040]]
- [[Schedule EIC]]
```

The agent uses index files (`type: index`) as entry points for graph-based exploration, following wikilinks to discover related content.

## Tech Stack

**Backend:** Python 3.13, FastAPI, Docling, Pydantic, httpx

**Frontend:** React 19, TypeScript, Vite, Cytoscape.js

**AI:** OpenAI-compatible LLM API

## License

MIT
