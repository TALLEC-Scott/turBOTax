---
created: 2026-02-28
updated: 2026-02-28
type: topic
category: Retirement
tags:
  - topic
  - retirement
  - annuities
  - pensions
---

# Expected Return

## Overview

Your **expected return** is the total amount you and other eligible annuitants can expect to receive under the annuity contract. It is the denominator in calculating the [[Exclusion Percentage]] under the [[General Rule]].

## Determining Age

For purposes of figuring expected return, a person's age is the age at the birthday **nearest to the [[Annuity Starting Date]]**.

## Calculation by Annuity Type

### Fixed Period Annuity

Multiply the number of payments by the payment amount.

```
Expected Return = Number of Payments × Payment Amount
```

**Example**: 180 monthly payments of $500 = $90,000 expected return.

### Single-Life Annuity

Multiply the annual payment by a multiple from actuarial Tables I or V (in [[Pub 939 - General Rule for Pensions and Annuities]]).

```
Expected Return = Annual Payment × Multiple from Table
```

**Example**: $500/month ($6,000/year) at age 66. Multiple from Table V is 19.2. Expected return = $115,200.

**Adjustments for payment frequency**: If payments are quarterly, semiannually, or annually, adjust the multiple per the tables.

### Joint and Survivor Annuities

Use Tables II or VI based on combined life expectancies of both annuitants.

**Same payment to survivor**:
```
Expected Return = Annual Payment × Multiple from Table II or VI
```

**Different payment to survivor**: Calculate separately:
1. Find combined multiple from Table VI
2. Find primary annuitant's multiple from Table V
3. Difference = survivor's multiple
4. Calculate each expected return separately and add together

### Annuity for Shorter of Life or Specified Period

Use Tables IV or VIII for temporary life annuities based on:
- Age at annuity starting date
- Number of years in specified period

**Example**: $200/month for 5 years or until death, age 65. Multiple from Table VIII is 4.9. Expected return = $11,760.

## Actuarial Tables

The tables in [[Pub 939 - General Rule for Pensions and Annuities]] include:

| Table | Purpose |
|-------|---------|
| Table I | Single-life annuity (old, sex-based) |
| Table II | Joint and survivor (old, sex-based) |
| Table III | Value of refund feature |
| Table IV | Temporary life annuity (old) |
| Table V | Single-life annuity (unisex) |
| Table VI | Joint and survivor (unisex) |
| Table VII | Value of refund feature (unisex) |
| Table VIII | Temporary life annuity (unisex) |

## Relationship to Exclusion

```
Investment in Contract
──────────────────────── = Exclusion Percentage
    Expected Return
```

The larger your expected return relative to investment, the smaller your tax-free portion.

## Related Topics

- [[General Rule]] - Method using expected return
- [[Investment in the Contract]] - The numerator in the exclusion ratio
- [[Exclusion Percentage]] - The result of the ratio
- [[Annuity Starting Date]] - The date for determining age and calculation
- [[Variable Annuities]] - Different method for expected return
- [[Pension and Annuity Income]] - Overall taxation of retirement income
- [[Joint and Survivor Annuities]] - Special rules for multiple annuitants

## Related Publications

- [[Pub 939 - General Rule for Pensions and Annuities]] - Contains all actuarial tables
- [[Pub 575 - Pension and Annuity Income]] - Simplified Method alternative

## Examples

**Example 1**: Single-life annuity, age 66, $500/month. Multiple = 19.2. Expected return = $6,000 × 19.2 = $115,200.

**Example 2**: Joint and survivor, ages 70 and 67, $500/month. Multiple from Table VI = 22.0. Expected return = $6,000 × 22.0 = $132,000.

**Example 3**: Different payments ($500 to primary, $350 to survivor). Primary's portion: $6,000 × 16.0 = $96,000. Survivor's portion: $4,200 × 6.0 = $25,200. Total = $121,200.
