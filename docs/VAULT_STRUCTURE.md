# Obsidian Vault Structure - Turbo Tax

This document details the Obsidian vault structure for organizing parsed IRS documents.

## Overview

The vault follows a **PARA-inspired structure** with numbered prefixes for consistent sorting. Folders are organized by **document type** (not topic) to reduce decision fatigue, while links and tags handle topic discovery [1][4].

**Key Principles:**
- Max 2-3 folder levels (2 clicks to any note)
- Numbered prefixes (00-, 01-, etc.) for consistent sorting
- YAML frontmatter for Dataview queries
- Templates for consistency
- Links and MOCs (Maps of Content) for topic discovery

## Folder Structure

```
obsidian_db/turbo_tax/
│
├── 00 - Dashboard/                    # Central hub with links to everything
│   ├── Map of Contents.md             # Main navigation hub
│   ├── Quick Reference.md             # Common forms and deadlines
│   └── Recent Updates.md              # Dataview query for recent changes
│
├── 01 - Tax Forms/                    # Forms organized by tax year
│   ├── 2024/
│   │   ├── Form 1040.md
│   │   ├── Form 1040 Instructions.md
│   │   ├── Schedule A - Itemized Deductions.md
│   │   ├── Schedule B - Interest and Dividends.md
│   │   ├── Schedule C - Profit or Loss from Business.md
│   │   ├── Schedule D - Capital Gains and Losses.md
│   │   ├── Schedule E - Supplemental Income.md
│   │   └── ...
│   ├── 2023/
│   │   └── ...
│   └── _index.md                      # Forms MOC
│
├── 02 - Publications/                 # IRS Publications
│   ├── Pub 17 - Your Federal Income Tax.md
│   ├── Pub 501 - Dependents.md
│   ├── Pub 502 - Medical and Dental Expenses.md
│   ├── Pub 503 - Child and Dependent Care Expenses.md
│   ├── Pub 504 - Divorced or Separated Individuals.md
│   ├── Pub 505 - Tax Withholding and Estimated Tax.md
│   ├── Pub 525 - Taxable and Nontaxable Income.md
│   ├── Pub 526 - Charitable Contributions.md
│   ├── Pub 590 - Individual Retirement Arrangements.md
│   ├── Pub 596 - Earned Income Credit.md
│   ├── Pub 970 - Tax Benefits for Education.md
│   └── _index.md                      # Publications MOC
│
├── 03 - Topics/                       # Thematic notes linking documents
│   ├── Deductions/
│   │   ├── Standard Deduction.md
│   │   ├── Itemized Deductions.md
│   │   └── Above-the-Line Deductions.md
│   ├── Credits/
│   │   ├── Child Tax Credit.md
│   │   ├── Earned Income Credit.md
│   │   ├── Education Credits.md
│   │   └── Foreign Tax Credit.md
│   ├── Income/
│   │   ├── Wages and Salaries.md
│   │   ├── Self-Employment Income.md
│   │   ├── Investment Income.md
│   │   └── Rental Income.md
│   ├── Filing Status/
│   │   ├── Single.md
│   │   ├── Married Filing Jointly.md
│   │   ├── Married Filing Separately.md
│   │   ├── Head of Household.md
│   │   └── Qualifying Surviving Spouse.md
│   ├── Dependents/
│   │   ├── Qualifying Child.md
│   │   └── Qualifying Relative.md
│   ├── Retirement/
│   │   ├── IRAs.md
│   │   ├── 401k Plans.md
│   │   └── Social Security Benefits.md
│   ├── Business/
│   │   ├── Self-Employment.md
│   │   ├── Business Expenses.md
│   │   └── Home Office.md
│   └── _index.md                      # Topics MOC
│
├── 04 - Assets/                       # Supporting files
│   ├── images/
│   │   └── form_diagrams/
│   └── tables/
│       ├── 2024/
│       │   ├── tax_brackets_2024.csv
│       │   ├── standard_deduction_2024.csv
│       │   └── eic_table_2024.csv
│       └── ...
│
├── 05 - Archives/                     # Obsolete/superseded documents
│   └── 2022/
│       └── ...
│
├── 00 - Templates/                    # Note templates
│   ├── Tax Form.md
│   ├── Publication.md
│   ├── Instructions.md
│   ├── Topic.md
│   └── Table.md
│
└── 000 - Meta/                        # Vault metadata
    ├── Changelog.md
    ├── Sync Log.md
    └── Parser Errors.md
```

---

## Note Templates

### Tax Form Template

```markdown
---
created: {{date}}
updated: {{date}}
type: tax-form
form_number: {{form_number}}
form_title: {{title}}
tax_year: {{tax_year}}
revision_date: {{revision_date}}
source_url: {{source_url}}
tags:
  - tax-form
  - {{tax_year}}
  - {{category}}
status: extracted
aliases:
  - "{{form_number}}"
  - "{{form_number}} {{tax_year}}"
---

# {{form_number}} - {{title}}

## Overview

{{overview}}

## Filing Requirements

{{filing_requirements}}

## Key Lines

| Line | Description | Notes |
|------|-------------|-------|
| 1    | ...         | ...   |

## Instructions Summary

{{instructions_summary}}

## Related Forms

- [[Form W-2]] - Wage and Tax Statement
- [[Schedule A]] - Itemized Deductions
- [[Form 1040 Instructions {{tax_year}}]]

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
tags:
  - publication
  - {{category}}
status: extracted
aliases:
  - "Pub {{pub_number}}"
  - "Publication {{pub_number}}"
---

# Publication {{pub_number}} - {{title}}

## Summary

{{summary}}

## Key Topics

```dataview
LIST
FROM [[#]]
WHERE type = "topic"
SORT file.name
```

## Important Rules

1. {{rule_1}}
2. {{rule_2}}

## Examples

### Example 1: {{example_title}}

{{example_content}}

## Tables

| Description | Link |
|-------------|------|
| {{table_name}} | [[{{table_link}}]] |

## Related Publications

- [[Publication X]] - Topic
- [[Publication Y]] - Topic

## Source

- IRS Website: {{source_url}}
```

### Topic Template

```markdown
---
created: {{date}}
updated: {{date}}
type: topic
category: {{category}}
tags:
  - topic
  - {{category}}
---

# {{title}}

## Overview

{{overview}}

## Key Rules

{{key_rules}}

## Related Forms

```dataview
TABLE form_number, tax_year
FROM #tax-form
WHERE contains(related_topics, this.file.link)
SORT tax_year DESC
```

## Related Publications

```dataview
TABLE publication_number, title
FROM #publication
WHERE contains(related_topics, this.file.link)
SORT publication_number
```

## Common Questions

### Q: {{question}}
**A:** {{answer}}

## References

- [[Publication X]] - Section Y
- [[Form Z Instructions]] - Page N
```

---

## YAML Frontmatter Properties

### Standard Properties

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `created` | date | Note creation date | `2024-01-15` |
| `updated` | date | Last modified date | `2024-02-20` |
| `type` | string | Note type | `tax-form`, `publication`, `topic` |
| `status` | string | Processing status | `extracted`, `reviewed`, `error` |
| `tags` | list | Category tags | `[tax-form, 2024, individual]` |
| `aliases` | list | Alternative names | `["Form 1040", "1040"]` |

### Tax Form Properties

| Property | Type | Description |
|----------|------|-------------|
| `form_number` | string | Form identifier (e.g., `1040`, `1040-SR`) |
| `form_title` | string | Official form title |
| `tax_year` | string | Tax year the form applies to |
| `revision_date` | date | IRS revision date |
| `source_url` | string | IRS.gov PDF URL |
| `category` | string | Form category (`individual`, `business`, `estate`) |

### Publication Properties

| Property | Type | Description |
|----------|------|-------------|
| `publication_number` | string | Publication number (e.g., `17`, `501`) |
| `title` | string | Official publication title |
| `tax_year` | string | Tax year coverage |
| `source_url` | string | IRS.gov source URL |

---

## Dataview Queries

### Dashboard Queries

**Recent Updates:**
```dataview
TABLE file.name as "Document", updated as "Updated", type as "Type"
FROM ""
WHERE updated >= date(today) - dur(7 days)
SORT updated DESC
LIMIT 20
```

**All Tax Forms for 2024:**
```dataview
TABLE form_number as "Form", form_title as "Title", status as "Status"
FROM "01 - Tax Forms/2024"
SORT form_number
```

**Publications by Number:**
```dataview
TABLE publication_number as "Pub #", title as "Title", tax_year as "Year"
FROM "02 - Publications"
SORT publication_number
```

**Forms by Category:**
```dataview
LIST
FROM #tax-form
WHERE category = "individual"
SORT form_number
```

**Forms Needing Review:**
```dataview
TABLE form_number, updated
FROM #tax-form
WHERE status = "extracted"
SORT updated DESC
```

### Topic Navigation

**All Topics:**
```dataview
TABLE category, file.links as "Related Docs"
FROM "03 - Topics"
SORT category, file.name
```

**Forms Related to Deductions:**
```dataview
TABLE form_number, tax_year
FROM #tax-form
WHERE contains(file.outlinks, [[Deductions]])
SORT tax_year DESC
```

---

## Maps of Content (MOCs)

### Main Map of Contents

```markdown
# Map of Contents

## Quick Access

- [[Quick Reference]] - Common forms and deadlines
- [[Recent Updates]] - What's new

## Documents by Type

| Type | Count | Link |
|------|-------|------|
| Tax Forms | `$= dv.pages('"01 - Tax Forms"').length` | [[01 - Tax Forms/_index\|Tax Forms]] |
| Publications | `$= dv.pages('"02 - Publications"').length` | [[02 - Publications/_index\|Publications]] |
| Topics | `$= dv.pages('"03 - Topics"').length` | [[03 - Topics/_index\|Topics]] |

## Browse by Topic

- [[03 - Topics/Deductions|Deductions]]
- [[03 - Topics/Credits|Credits]]
- [[03 - Topics/Income|Income Types]]
- [[03 - Topics/Filing Status|Filing Status]]
- [[03 - Topics/Dependents|Dependents]]
- [[03 - Topics/Retirement|Retirement]]
- [[03 - Topics/Business|Business]]

## Recent Activity

```dataview
TABLE file.name as "Document", updated as "Updated"
FROM ""
WHERE updated >= date(today) - dur(30 days)
SORT updated DESC
LIMIT 10
```
```

---

## Backlinks Strategy

**Backlinks are the core of Obsidian's knowledge graph.** Unlike folders which organize by location, backlinks create connections between ideas. Every note should actively link to related content, and backlinks will automatically show the reverse relationship.

### Why Backlinks Over Folders

| Folders | Backlinks |
|---------|-----------|
| One location per note | Multiple connections per note |
| Manual organization | Automatic discovery |
| Rigid hierarchy | Flexible network |
| Hard to find cross-topic info | See all related content instantly |

### Backlink Fundamentals

**Every note you create should:**
1. **Link outward** - Connect to 3-5 related notes
2. **Be linkable** - Use descriptive titles others will reference
3. **Surface via backlinks** - Let reverse connections build your knowledge graph

**View backlinks:** At the bottom of every note, Obsidian shows "Backlinks" - all notes that reference the current note.

### Strategic Linking Patterns

#### 1. Form → Related Forms
```markdown
# Form 1040

## Related Forms
- [[Schedule A]] - For itemized deductions
- [[Schedule B]] - For interest/dividends over $1,500
- [[Schedule C]] - For self-employment income
- [[Schedule D]] - For capital gains/losses
- [[Form W-2]] - Income source
- [[Form 1099]] - Various income types
```

#### 2. Topic → All Relevant Documents
```markdown
# Child Tax Credit

## Applicable Forms
- [[Form 1040]] - Line 19
- [[Form 1040-SR]] - Line 19
- [[Schedule 8812]] - Additional credits

## Publications
- [[Pub 972]] - Child Tax Credit
- [[Pub 17]] - Chapter 34

## Related Topics
- [[Credits]] - Parent topic
- [[Dependents]] - Qualifying child rules
```

#### 3. Publication → Forms and Topics
```markdown
# Pub 17 - Your Federal Income Tax

## Forms Covered
- [[Form 1040]]
- [[Form 1040-SR]]
- [[Form 1040-NR]]

## Key Topics
- [[Filing Status]]
- [[Dependents]]
- [[Income]]
- [[Deductions]]
- [[Credits]]
```

#### 4. Cross-Reference Everything
```markdown
# When discussing Itemized Deductions:

Itemized deductions ([[Schedule A]]) are an alternative to the
[[Standard Deduction]]. See [[Pub 501]] for limitations and
[[Pub 17 Chapter 22]] for detailed rules.
```

### Backlink-Driven Discovery

**Example: Checking what references Schedule A:**

When viewing `Schedule A.md`, the backlinks panel shows:
```
Backlinks (5)
├── Form 1040.md
│   └── "...file [[Schedule A]] for itemized..."
├── Deductions.md
│   └── "...use [[Schedule A]] to claim..."
├── Pub 501.md
│   └── "...limitations on [[Schedule A]] deductions..."
├── Itemized Deductions.md
│   └── "...file [[Schedule A]] with Form 1040..."
└── Tax Planning 2024.md
    └── "...maximize [[Schedule A]] deductions..."
```

**This reveals:**
- Where Schedule A is mentioned
- Context of each reference
- Related documents you might not have considered

### Linking Best Practices

#### Do Link To:
- Related forms (form → schedule → instructions)
- Parent topics (Child Tax Credit → Credits)
- Source publications (form → Pub 17, Pub 501, etc.)
- Definitions (first mention of technical term)
- Examples and edge cases

#### Don't Link To:
- Every occurrence (link once, usually first)
- Unrelated content (creates noise in backlinks)
- Nonexistent notes (unless you plan to create them)

#### Use Aliases for Readable Links:
```markdown
[[Form 1040|1040]]
[[Schedule A|Itemized Deductions Form]]
[[Pub 17#Chapter 5|Filing Status Rules]]
```

### Building the Knowledge Graph

**Strong backlink networks form naturally when you:**

1. **Start from publications** - Publications cover broad ground and link to many forms
2. **Create topic hubs** - Topics aggregate related forms/publications
3. **Reference consistently** - Always link the same way (`[[Form 1040]]` not `[[1040]]`)
4. **Review backlinks** - Check what links to your note; add missing reverse links

**Example Knowledge Graph Path:**
```
Form 1040 ←→ Schedule A ←→ Itemized Deductions
     ↓           ↓
     ←← Pub 17 ←←
                    ↓
              Deductions (topic)
                    ↓
              Standard Deduction
```

### Graph View Usage

Open Graph View (Ctrl/Cmd + G) to visualize:

- **Local graph** - Shows connections around current note
- **Global graph** - Shows entire vault structure
- **Filters** - Show only forms, only publications, by year, etc.

**Good graphs show:**
- Clusters around topics (Credits, Deductions, Income)
- Strong connections between forms and schedules
- Publications as hubs with many outward links

### Backlink Queries with Dataview

**Show what links to current note:**
```dataview
LIST file.link
FROM ""
WHERE contains(file.outlinks, this.file.link)
SORT file.name
```

**Find orphan notes (no incoming links):**
```dataview
LIST
FROM ""
WHERE length(file.inlinks) = 0 AND type != "template"
```

**Most connected notes:**
```dataview
TABLE length(file.inlinks) as "Incoming", length(file.outlinks) as "Outgoing"
FROM ""
SORT length(file.inlinks) DESC
LIMIT 10
```

### Summary: The Backlink Mindset

| Traditional Thinking | Backlink Thinking |
|---------------------|-------------------|
| "Where should I file this?" | "What should this link to?" |
| Organize by folder | Connect by links |
| One home per note | Many paths to each note |
| Search to find | Follow links to discover |

**Remember:** A note with 10 backlinks is more valuable than a note in 10 folders. Build connections, not hierarchies.

---

## Tagging System

### Tag Hierarchy

```
#tax-form           # Individual tax forms
#tax-form/business  # Business tax forms
#tax-form/estate    # Estate and trust forms
#publication        # IRS publications
#topic              # Topic notes
#status/extracted   # Processing status
#status/reviewed
#status/error
#priority/high      # Review priority
#priority/medium
#priority/low
#year/2024          # Tax year
#year/2025
```

### Tag Usage Examples

```markdown
---
tags:
  - tax-form
  - year/2024
  - status/reviewed
---
```

---

## Naming Conventions

### Files

| Type | Pattern | Example |
|------|---------|---------|
| Tax Form | `Form {number}` | `Form 1040.md` |
| Schedule | `Schedule {letter} - {title}` | `Schedule A - Itemized Deductions.md` |
| Publication | `Pub {number} - {title}` | `Pub 17 - Your Federal Income Tax.md` |
| Instructions | `Form {number} Instructions` | `Form 1040 Instructions.md` |
| Topic | `{Topic Name}` | `Child Tax Credit.md` |
| Table | `{description}_{year}.csv` | `tax_brackets_2024.csv` |

### Folders

- Use numbered prefixes: `01 - Tax Forms/`
- Capitalize words: `Deductions/` not `deductions/`
- Keep names short but descriptive

---

## MCP Integration

The Qwen Code agent interacts with the vault via MCP tools:

### Write a Note

```python
# Using filesystem MCP
mcp__filesystem__write_file(
    path="/path/to/vault/01 - Tax Forms/2024/Form 1040.md",
    content=note_content
)
```

### Read a Note

```python
mcp__filesystem__read_file(
    path="/path/to/vault/02 - Publications/Pub 17 - Your Federal Income Tax.md"
)
```

### List Directory

```python
mcp__filesystem__list_directory(
    path="/path/to/vault/01 - Tax Forms/2024"
)
```

### Using Obsidian MCP

```python
# With @mauricio.wolff/mcp-obsidian
# Tool names will be prefixed with mcp__obsidian__
```

---

## Maintenance

### Regular Tasks

1. **Weekly:** Review `status: extracted` notes, mark as `reviewed`
2. **Monthly:** Archive old tax year folders
3. **Annually:** Create new tax year folder, update templates

### Quality Checks

```dataview
# Notes missing required properties
LIST
FROM #tax-form
WHERE !form_number OR !tax_year

# Outdated notes (not updated in 90 days)
TABLE file.name, updated
FROM #tax-form
WHERE updated <= date(today) - dur(90 days)
```

---

## Sources

- [1] https://github.com/voidashi/obsidian-vault-template
- [2] https://forum.obsidian.md/t/obsidian-properties-best-practices-and-why/63891
- [3] https://www.youtube.com/watch?v=MyR6R55lGRk
- [4] https://www.excellentphysician.com/post/how-i-organize-my-obsidian-vault
- [5] https://blacksmithgu.github.io/obsidian-dataview/queries/structure/
- [6] https://github.com/seburbandev/obsidian-dataview-cheatsheet
