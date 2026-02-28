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

### Filing Status
- [[Filing Status]] - Overview of five filing statuses
- [[Single]] - Filing as unmarried
- [[Married Filing Jointly]] - Joint filing benefits
- [[Married Filing Separately]] - Separate filing rules
- [[Head of Household]] - Benefits for unmarried with dependents
- [[Qualifying Surviving Spouse]] - Widow(er) filing status

### Dependents
- [[Dependents]] - Qualifying child and qualifying relative tests
- [[Child Tax Credit]] - Credit for children under 17
- [[Credit for Other Dependents]] - Credit for other qualifying dependents

### Deductions
- [[Standard Deduction]] - Fixed deduction amounts
- [[Itemized Deductions]] - Schedule A deductions
- [[Tax Withholding and Estimated Tax]] - Pay-as-you-go system

### Credits
- [[Tax Credits]] - Overview of all tax credits
- [[Child Tax Credit]] - Up to $2,000 per qualifying child
- [[Earned Income Credit]] - Refundable credit for working families
- [[Credit for Other Dependents]] - $500 for other dependents

### Income
- [[Interest Income]] - Taxable and tax-exempt interest
- [[Social Security Benefits]] - Taxability of benefits
- [[Tips and Tip Reporting]] - Tip income reporting
- [[Supplemental Wages]] - Bonuses and supplemental pay
- [[Military Pay and Allowances]] - Military compensation
- [[Combat Zone Exclusion]] - Nontaxable combat pay

### Employment Tax
- [[Social Security and Medicare Taxes]] - FICA taxes
- [[Federal Unemployment Tax (FUTA)]]
- [[Federal Income Tax Withholding]] - Employer obligations
- [[Tax Deposits]] - Employment tax deposits
- [[Employee Classification]] - Employee vs. contractor
- [[Employer Identification Number]] - EIN requirements
- [[Third-Party Payer Arrangements]] - Reporting requirements

### Retirement
- [[IRAs]] - Traditional and Roth IRA rules

### Special Situations (Military)
- [[Moving Expenses]] - Military PCS deductions
- [[Sale of Home Exclusion]] - Military home sale rules
- [[Tax Forgiveness for Deceased Servicemembers]]

### International (Expats)
- [[Foreign Earned Income Exclusion]] - Exclude foreign income from U.S. tax
- [[Foreign Housing Exclusion and Deduction]] - Housing cost benefits abroad
- [[Bona Fide Residence Test]] - Qualification test for FEIE
- [[Physical Presence Test]] - Alternative test for FEIE
- [[Tax Home]] - Definition for international taxpayers
- [[Foreign Tax Credit]] - Credit for foreign taxes paid
- [[Tax Treaties]] - Treaty benefits and procedures
- [[Self-Employment Tax Abroad]] - SE tax for expats
- [[Filing Requirements for Expats]] - Filing obligations and extensions

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

## Topics by Publication

### From [[Pub 17 - Your Federal Income Tax]]
- [[Filing Status]]
- [[Dependents]]
- [[Standard Deduction]]
- [[Itemized Deductions]]
- [[Tax Credits]]
- [[Child Tax Credit]]
- [[Earned Income Credit]]
- [[IRAs]]
- [[Social Security Benefits]]
- [[Interest Income]]
- [[Tax Withholding and Estimated Tax]]

### From [[Pub 15 - Employer's Tax Guide]]
- [[Federal Income Tax Withholding]]
- [[Social Security and Medicare Taxes]]
- [[Federal Unemployment Tax (FUTA)]]
- [[Tax Deposits]]
- [[Employee Classification]]
- [[Tips and Tip Reporting]]
- [[Supplemental Wages]]

### From [[Pub 3 - Armed Forces Tax Guide]]
- [[Combat Zone Exclusion]]
- [[Military Pay and Allowances]]
- [[Moving Expenses]]
- [[Sale of Home Exclusion]]
- [[Tax Forgiveness for Deceased Servicemembers]]

### From [[Pub 225 - Farmer's Tax Guide]]
- [[Farm Income]]
- [[Farm Business Expenses]]
- [[Depreciation for Farmers]]
- [[Section 179 Deduction]]
- [[Self-Employment Tax]]
- [[Farm Employment Taxes]]
- [[Soil and Water Conservation Deduction]]
- [[Income Averaging for Farmers]]
- [[Fuel Tax Credits]]
- [[Farm Recordkeeping]]
- [[Cash vs Accrual Accounting for Farmers]]
- [[Farm Property Dispositions]]
- [[Farm Casualty Losses]]
- [[Agricultural Program Payments]]
- [[Installment Sales for Farmers]]
- [[Schedule F (Form 1040)]]
