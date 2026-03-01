---
created: 2026-02-28
updated: 2026-02-28
type: topic
category: Income
tags:
  - topic
  - income
  - installment-sales
  - calculations
---

# Gross Profit Percentage

## Overview

The **gross profit percentage** is the ratio used in [[Installment Sales]] to determine how much of each payment represents taxable gain. It is applied to each payment (excluding interest) received during the installment period.

## Formula

```
Gross Profit Percentage = Gross Profit ÷ Contract Price
```

## Calculating Gross Profit

**Gross Profit** = Selling Price − Adjusted Basis for Installment Sale Purposes

**Adjusted Basis for Installment Sale** = Adjusted Basis + Selling Expenses + Depreciation Recapture

### Components

| Component | Description |
|-----------|-------------|
| **Selling Price** | Total cost to buyer: cash, FMV of property received, debts assumed, seller expenses paid by buyer |
| **Adjusted Basis** | Original basis adjusted for improvements and depreciation |
| **Selling Expenses** | Commissions, legal fees, other sale costs |
| **Depreciation Recapture** | Amount recaptured as ordinary income under Sections 1245, 1250 |

## Calculating Contract Price

**Contract Price** = Selling Price − Mortgages/Debts Assumed + Excess of Liabilities Over Basis

When the buyer assumes a mortgage:
- If mortgage ≤ your installment sale basis: Contract price = Selling price − Mortgage
- If mortgage > your installment sale basis: Add the excess to the contract price

## Example

You sell property for $100,000:
- Adjusted basis: $40,000
- Selling expenses: $5,000
- Depreciation recapture: $0
- Buyer assumes $20,000 mortgage

**Calculation:**
1. Installment sale basis = $40,000 + $5,000 + $0 = $45,000
2. Gross profit = $100,000 − $45,000 = $55,000
3. Contract price = $100,000 − $20,000 = $80,000
4. Gross profit percentage = $55,000 ÷ $80,000 = 68.75%

## Application to Payments

Each payment received (excluding interest) is multiplied by the gross profit percentage:

**Installment Sale Income** = Payment Received × Gross Profit Percentage

**Tax-Free Return of Basis** = Payment Received × (1 − Gross Profit Percentage)

## Related Topics

- [[Installment Sales]] - Overall method and requirements
- [[Installment Obligation]] - Buyer's payment obligation
- [[Depreciation Recapture]] - Treatment of recaptured depreciation
- [[Contract Price]] - Detailed calculation rules
- [[Selling Price]] - What's included
- [[Adjusted Basis]] - How to determine basis

## Related Forms

| Form | Purpose |
|------|---------|
| [[Form 6252]] | Line 19 shows gross profit percentage |
| [[Form 4797]] | For depreciation recapture calculation |

## When Percentage Changes

The gross profit percentage generally remains constant, but must be recalculated if:
1. **Selling price reduced** - New percentage for remaining payments
2. **Contingent payments** - Special rules under Section 453(i)

## Selling Price Reduced Example

Original sale: $100,000 selling price, $55,000 gross profit, $80,000 contract price (68.75%)

Year 3: Selling price reduced to $85,000
- Received $20,000 payments already (reported $13,750 gain)
- New gross profit = $85,000 − $45,000 = $40,000
- Less gain already reported: $40,000 − $13,750 = $26,250 remaining
- Future installments: $45,000 remaining payments
- New gross profit percentage = $26,250 ÷ $45,000 = 58.33%

## Related Publications

- [[Pub 537 - Installment Sales]] - Worksheets A and B for calculations
- [[Pub 551 - Basis of Assets]] - Determining adjusted basis
- [[Pub 544 - Sales and Other Dispositions of Assets]] - Depreciation recapture

## Common Questions

### Q: What if gross profit is zero or negative?
**A:** You cannot use the installment method. The entire transaction results in no gain or a loss (deducted in year of sale).

### Q: How do I handle depreciation recapture in the percentage?
**A:** Depreciation recapture is included in your installment sale basis but must be reported as ordinary income in the year of sale—it is not spread over installments.

### Q: What if the contract price is zero?
**A:** If the mortgage equals or exceeds the selling price, special rules apply. See [[Installment Sales]] for mortgage exceeding basis rules.

## References
## Related Tables

- [[04 - Assets/gross_profit_percentage_worksheet_example|Gross Profit Percentage Worksheet Example]] - This table provides a filled-in example of Worksheet B, showing how to calculate a new gross profit percentage of 46.67% after reducing the selling price to $85,000.

- IRC Section 453(b) - Definition of gross profit
- [[Pub 537 - Installment Sales]] - Worksheet A for calculation