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
- [[Qualifying Child]] - Tests for qualifying child status
- [[Qualifying Relative]] - Tests for qualifying relative status
- [[Qualifying Person]] - Who qualifies for dependent care credit
- [[Child Tax Credit]] - Credit for children under 17
- [[Credit for Other Dependents]] - Credit for other qualifying dependents

### Deductions
- [[Standard Deduction]] - Fixed deduction amounts
- [[Itemized Deductions]] - Schedule A deductions
- [[Medical and Dental Expenses]] - Medical expense deduction rules
- [[Health Insurance Premiums]] - Insurance premium deductibility
- [[Long-Term Care]] - Long-term care deduction rules
- [[Capital Medical Expenses]] - Home modifications and equipment
- [[Tax Withholding and Estimated Tax]] - Pay-as-you-go system
- [[Rental Expenses]] - Deductible costs for rental properties

### Charitable Contributions
- [[Qualified Organizations]] - Which organizations can receive deductible contributions
- [[Noncash Contributions]] - Property donations and valuation
- [[Vehicle Donations]] - Cars, boats, and airplanes
- [[Conservation Contributions]] - Conservation easements and historic structures
- [[Charitable Contribution Limits]] - AGI percentage limits (60%, 50%, 30%, 20%)
- [[Volunteer Expense Deductions]] - Out-of-pocket expenses for charity work
- [[Form 8283]] - Noncash charitable contributions reporting

### Credits
- [[Tax Credits]] - Overview of all tax credits
- [[Child Tax Credit]] - Up to $2,000 per qualifying child
- [[Child and Dependent Care Credit]] - For childcare expenses
- [[Earned Income Credit]] - Refundable credit for working families
- [[Credit for Other Dependents]] - $500 for other dependents

### Income
- [[Interest Income]] - Taxable and tax-exempt interest
- [[Social Security Benefits]] - Taxability of benefits
- [[Tips and Tip Reporting]] - Tip income reporting
- [[Supplemental Wages]] - Bonuses and supplemental pay
- [[Military Pay and Allowances]] - Military compensation
- [[Combat Zone Exclusion]] - Nontaxable combat pay
- [[Rental Income]] - Types and reporting requirements

### Employment Tax
- [[Social Security and Medicare Taxes]] - FICA taxes
- [[Federal Unemployment Tax (FUTA)]]
- [[Federal Income Tax Withholding]] - Employer obligations
- [[Tax Deposits]] - Employment tax deposits
- [[Semiweekly Deposit Rules]] - Semiweekly deposit schedule
- [[Employee Classification]] - Employee vs. contractor
- [[Employer Identification Number]] - EIN requirements
- [[Third-Party Payer Arrangements]] - Reporting requirements
- [[Household Employer Tax Rules]] - Nanny tax and household employees

### Tax Administration
- [[Tax Calendars]] - Filing deadlines and calendar overview
- [[Excise Tax Calendar]] - Excise tax filing and deposit dates

### Rental Property
- [[Rental Income]] - Types and reporting requirements
- [[Rental Expenses]] - Deductible costs for rental properties
- [[MACRS Depreciation]] - Depreciation methods and recovery periods
- [[Bonus Depreciation]] - 100% special allowance for 2025
- [[Basis of Rental Property]] - Cost and adjusted basis rules
- [[Repairs vs Improvements]] - Capitalization vs. expensing
- [[Points on Rental Mortgages]] - Mortgage points deduction
- [[Vacation Home Rules]] - Personal use limitations
- [[Personal Use of Rental Property]] - What counts as personal use
- [[Condominium Rental Rules]] - Condo-specific rules
- [[Cooperative Housing Rental]] - Co-op depreciation
- [[Property Changed to Rental Use]] - Conversion rules

### Property Dispositions
- [[Sales and Exchanges]] - Determining when a disposition occurs
- [[Foreclosures and Repossessions]] - Property dispositions through foreclosure
- [[Abandonments]] - Voluntary relinquishment of property
- [[Involuntary Conversions]] - Condemnations and casualties
- [[Like-Kind Exchange]] - Tax-deferred exchanges
- [[Bargain Sales]] - Sales below fair market value
- [[Capital Assets]] - Property classification for gains/losses
- [[Noncapital Assets]] - Business property and inventory
- [[Related Party Sales]] - Special rules for related persons
- [[Sale of Business]] - Allocating purchase price
- [[Classes of Assets]] - Asset classification for acquisitions
- [[Holding Period]] - Determining short vs. long-term

### Business Property
- [[Section 1231 Gains and Losses]] - Business property treatment
- [[Depreciation Recapture]] - Ordinary income on depreciated property
- [[Section 1245 Property]] - Personal property recapture
- [[Section 1250 Property]] - Real property recapture

### Capital Gains and Losses
- [[Capital Gains Tax Rates]] - Preferential rates for long-term gains
- [[Capital Loss Treatment]] - Deduction and carryover rules
- [[Information Returns for Dispositions]] - Forms 1099-B, 1099-S, 1099-DA

### Retirement
- [[IRAs]] - Traditional and Roth IRA rules
- [[Qualified Domestic Relations Order]] - Dividing retirement plans in divorce

### Divorce and Separation
- [[Alimony]] - Tax treatment of spousal support payments
- [[Child Support]] - Nondeductible support payments
- [[Children of Divorced Parents]] - Rules for claiming dependents
- [[Community Property]] - Special rules for community property states
- [[Injured Spouse]] - Recovering your share of a joint refund
- [[Innocent Spouse Relief]] - Relief from joint tax liability
- [[Property Settlements]] - Tax-free transfers between spouses
- [[Qualified Domestic Relations Order]] - Dividing retirement plans

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
- [[Foreign Tax Credit Carryover]] - Carryback and carryforward rules
- [[Foreign Tax Redetermination]] - Changes in foreign tax liability
- [[Foreign Currency and Exchange Rates]] - Currency translation rules
- [[GILTI]] - Global Intangible Low-Taxed Income
- [[Controlled Foreign Corporation]] - CFC rules for U.S. shareholders
- [[Separate Limit Income Categories]] - FTC basket categories
- [[Passive Category Income]] - Passive income FTC rules
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

### From [[Pub 502 - Medical and Dental Expenses]]
- [[Medical and Dental Expenses]]
- [[Health Insurance Premiums]]
- [[Long-Term Care]]
- [[Capital Medical Expenses]]

### From [[Pub 503 - Child and Dependent Care Expenses]]
- [[Child and Dependent Care Credit]]
- [[Qualifying Person]]
- [[Work-Related Expenses]]
- [[Dependent Care Benefits]]
- [[Household Employer Tax Rules]]

### From [[Pub 504 - Divorced or Separated Individuals]]
- [[Alimony]] - Tax treatment of spousal support
- [[Child Support]] - Nondeductible support payments
- [[Children of Divorced Parents]] - Custodial parent rules
- [[Community Property]] - Community property state rules
- [[Injured Spouse]] - Recovering your share of a joint refund
- [[Innocent Spouse Relief]] - Relief from joint liability
- [[Property Settlements]] - Tax-free transfers between spouses
- [[Qualified Domestic Relations Order]] - Dividing retirement plans

### From [[Pub 509 - Tax Calendars]]
- [[Tax Calendars]] - Overview of tax calendar types
- [[Semiweekly Deposit Rules]] - Payroll tax deposit schedule
- [[Excise Tax Calendar]] - Excise tax deadlines
- [[Tax Deposits]] - Employment tax deposit requirements
- [[Estimated Tax Payments]] - Individual and corporate estimated taxes
- [[Information Returns]] - Forms 1099 and W-2 filing deadlines
- [[Tips and Tip Reporting]] - Monthly tip reporting deadlines

### From [[Pub 514 - Foreign Tax Credit for Individuals]]
- [[Foreign Tax Credit]] - Credit vs. deduction, eligibility, limitations
- [[GILTI]] - Global Intangible Low-Taxed Income for CFC shareholders
- [[Controlled Foreign Corporation]] - CFC status and reporting requirements
- [[Foreign Tax Credit Carryover]] - 1-year carryback, 10-year carryforward
- [[Passive Category Income]] - Passive income basket for FTC
- [[Foreign Currency and Exchange Rates]] - Translating foreign taxes to USD
- [[Foreign Tax Redetermination]] - Changes in foreign tax liability
- [[Separate Limit Income Categories]] - Different FTC limitation baskets

### From [[Pub 526 - Charitable Contributions]]
- [[Charitable Contributions]] - Deduction requirements, timing, and reporting
- [[Qualified Organizations]] - 50% limit and 30% limit organizations
- [[Noncash Contributions]] - Property donations, valuation, and substantiation
- [[Vehicle Donations]] - Cars, boats, airplanes, and Form 1098-C
- [[Conservation Contributions]] - Easements, historic structures, enhanced limits
- [[Qualified Charitable Distributions]] - IRA donations for those 70½ and older
- [[Charitable Contribution Limits]] - AGI percentage limits and carryovers
- [[Volunteer Expense Deductions]] - Car, travel, and uniform expenses
- [[Form 8283]] - Reporting noncash contributions over $500

### From [[Pub 527 - Residential Rental Property]]
- [[Rental Income]] - Types of rental income and when to report
- [[Rental Expenses]] - Deductible rental costs and timing
- [[MACRS Depreciation]] - Depreciation methods, recovery periods, conventions
- [[Bonus Depreciation]] - 100% special allowance for 2025
- [[Basis of Rental Property]] - Cost basis, adjusted basis, allocation rules
- [[Repairs vs Improvements]] - When to deduct vs. capitalize
- [[Points on Rental Mortgages]] - OID rules and deduction methods
- [[Vacation Home Rules]] - Personal use limits and expense allocation
- [[Personal Use of Rental Property]] - What counts as personal use
- [[Condominium Rental Rules]] - Condo-specific deductions and depreciation
- [[Cooperative Housing Rental]] - Stock depreciation and pass-through deductions
- [[Property Changed to Rental Use]] - Basis rules for converted property

### From [[Pub 544 - Sales and Other Dispositions of Assets]]
- [[Sales and Exchanges]] - Determining when a disposition occurs
- [[Foreclosures and Repossessions]] - Property dispositions through foreclosure
- [[Abandonments]] - Voluntary relinquishment of property
- [[Involuntary Conversions]] - Condemnations and casualties
- [[Like-Kind Exchange]] - Tax-deferred exchanges
- [[Bargain Sales]] - Sales below fair market value
- [[Capital Assets]] - Property classification for gains/losses
- [[Noncapital Assets]] - Business property and inventory
- [[Related Party Sales]] - Special rules for related persons
- [[Sale of Business]] - Allocating purchase price
- [[Classes of Assets]] - Asset classification for acquisitions
- [[Section 1231 Gains and Losses]] - Business property treatment
- [[Depreciation Recapture]] - Ordinary income on depreciated property
- [[Section 1245 Property]] - Personal property recapture
- [[Section 1250 Property]] - Real property recapture
- [[Capital Gains Tax Rates]] - Preferential rates for long-term gains
- [[Capital Loss Treatment]] - Deduction and carryover rules
- [[Holding Period]] - Determining short vs. long-term
- [[Information Returns for Dispositions]] - Forms 1099-B, 1099-S, 1099-DA
