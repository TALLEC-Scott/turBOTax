---
created: 2026-02-28
updated: 2026-02-28
type: dashboard
tags:
  - moc
  - dashboard
---

# Map of Contents

The central navigation hub for the Turbo Tax knowledge base.

## Quick Access

- [[Quick Reference]] - Common forms and deadlines
- [[Recent Updates]] - What's new

## Documents by Type

| Type | Description | Link |
|------|-------------|------|
| Tax Forms | Forms organized by tax year | [[01 - Tax Forms/_index\|Tax Forms]] |
| Publications | IRS Publications distilled | [[02 - Publications/_index\|Publications]] |
| Topics | Thematic notes | [[03 - Topics/_index\|Topics]] |

## Browse by Topic

- [[03 - Topics/Filing Status|Filing Status]]
- [[03 - Topics/Dependents|Dependents]]
- [[03 - Topics/Deductions|Deductions]]
- [[03 - Topics/Credits|Credits]]
- [[03 - Topics/Income|Income Types]]
- [[03 - Topics/Retirement|Retirement]]
- [[03 - Topics/Business|Business]]

## Core Publications

- [[Pub 17]] - Your Federal Income Tax (comprehensive guide)
- [[Pub 501]] - Dependents, Standard Deduction, Filing Information
- [[Pub 590]] - Individual Retirement Arrangements
- [[Pub 596]] - Earned Income Credit

## Key Forms

- [[Form 1040]] - U.S. Individual Income Tax Return
- [[Schedule A]] - Itemized Deductions
- [[Schedule B]] - Interest and Dividends
- [[Schedule C]] - Profit or Loss from Business
- [[Schedule D]] - Capital Gains and Losses

## Recent Activity

```dataview
TABLE file.name as "Document", updated as "Updated"
FROM ""
WHERE updated >= date(today) - dur(30 days)
SORT updated DESC
LIMIT 10
```
