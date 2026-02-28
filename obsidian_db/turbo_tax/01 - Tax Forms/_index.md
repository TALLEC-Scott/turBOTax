---
created: 2026-02-28
updated: 2026-02-28
type: index
tags:
  - index
  - tax-forms
---

# Tax Forms Index

IRS tax forms organized by tax year.

## 2025 Forms

```dataview
TABLE form_number as "Form", form_title as "Title", status as "Status"
FROM "01 - Tax Forms/2025"
SORT form_number
```

## 2024 Forms

```dataview
TABLE form_number as "Form", form_title as "Title", status as "Status"
FROM "01 - Tax Forms/2024"
SORT form_number
```

## Form Categories

### Individual Forms
- [[Form 1040]] - U.S. Individual Income Tax Return
- [[Form 1040-SR]] - U.S. Tax Return for Seniors
- [[Form 1040-NR]] - U.S. Nonresident Alien Income Tax Return

### Schedules
- [[Schedule A]] - Itemized Deductions
- [[Schedule B]] - Interest and Ordinary Dividends
- [[Schedule C]] - Profit or Loss from Business
- [[Schedule D]] - Capital Gains and Losses
- [[Schedule E]] - Supplemental Income and Loss
- [[Schedule F]] - Profit or Loss from Farming

### Information Returns
- [[Form W-2]] - Wage and Tax Statement
- [[Form 1099]] Series - Various income types

## Related Publications

- [[Pub 17]] - Your Federal Income Tax (comprehensive guide)
- [[Form instructions]] are linked from each form
