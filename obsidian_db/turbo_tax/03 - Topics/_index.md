---
created: 2026-02-28
updated: 2026-02-28
type: index
tags:
  - index
  - topics
---

# Topics Index

Thematic notes connecting forms, publications, and tax concepts.

## Browse by Category

### [[03 - Topics/Filing Status\|Filing Status]]
- [[Single]]
- [[Married Filing Jointly]]
- [[Married Filing Separately]]
- [[Head of Household]]
- [[Qualifying Surviving Spouse]]

### [[03 - Topics/Dependents\|Dependents]]
- [[Qualifying Child]]
- [[Qualifying Relative]]
- [[Dependents]]

### [[03 - Topics/Deductions\|Deductions]]
- [[Standard Deduction]]
- [[Itemized Deductions]]
- [[Above-the-Line Deductions]]

### [[03 - Topics/Credits\|Credits]]
- [[Child Tax Credit]]
- [[Earned Income Credit]]
- [[Education Credits]]
- [[Child and Dependent Care Credit]]

### [[03 - Topics/Income\|Income]]
- [[Wages and Salaries]]
- [[Self-Employment Income]]
- [[Investment Income]]
- [[Rental Income]]

### [[03 - Topics/Retirement\|Retirement]]
- [[IRAs]]
- [[401k Plans]]
- [[Social Security Benefits]]

### [[03 - Topics/Business\|Business]]
- [[Self-Employment]]
- [[Business Expenses]]
- [[Home Office]]

## All Topics

```dataview
TABLE category, file.links as "Related Docs"
FROM "03 - Topics"
WHERE type = "topic"
SORT category, file.name
```

## Most Connected Topics

```dataview
TABLE length(file.inlinks) as "Incoming Links", length(file.outlinks) as "Outgoing Links"
FROM "03 - Topics"
WHERE type = "topic"
SORT length(file.inlinks) DESC
LIMIT 10
```
