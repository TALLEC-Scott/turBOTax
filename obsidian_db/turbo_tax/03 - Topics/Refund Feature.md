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

# Refund Feature

## Overview

A **refund feature** is a provision in an annuity contract that guarantees payments to a beneficiary or estate if the annuitant dies before receiving a specified amount or number of payments. When present, you must reduce your [[Investment in the Contract]] by the value of this feature.

## When a Refund Feature Exists

An annuity has a refund feature when:

1. The [[Expected Return]] depends on the life of one or more individuals
2. The contract provides payments to a beneficiary or estate if a specified amount or number of payments hasn't been made before death
3. The payments are a refund of the amount paid for the annuity contract

## Calculating the Value

Use Table III or Table VII from [[Pub 939 - General Rule for Pensions and Annuities]]:

1. Find the applicable percentage based on:
   - Age at annuity starting date
   - Number of years payments are guaranteed

2. Multiply the percentage by the **guaranteed amount** (the lesser of net cost or total guaranteed return)

```
Value of Refund Feature = Percentage × Guaranteed Amount
```

## Zero Value Situations

### Joint and Survivor Annuity

Value is zero if ALL of the following apply:
- Both annuitants are age 74 or younger
- Payments are guaranteed for less than 2½ years
- Survivor's annuity is at least 50% of the first annuitant's

### Single-Life Annuity

Value is zero if:
- Payments guaranteed for less than 2½ years, AND
- Annuitant is:
  - Age 57 or younger (using unisex Table VII), OR
  - Age 42 or younger if male (using old Table III), OR
  - Age 47 or younger if female (using old Table III)

## Effect on Investment in Contract

```
Investment in Contract = Net Cost - Value of Refund Feature
```

The reduction for the refund feature lowers your investment, which increases the taxable portion of your annuity payments.

## Multiple Beneficiaries

For contracts with multiple beneficiaries or complex survivor arrangements, you may need to write to the IRS for assistance in figuring the refund feature value.

## Related Topics

- [[General Rule]] - Method requiring refund feature adjustment
- [[Investment in the Contract]] - Reduced by refund feature value
- [[Expected Return]] - Total expected payments under contract
- [[Exclusion Percentage]] - Affected by reduced investment
- [[Annuity Starting Date]] - Date used for age in table lookup
- [[Joint and Survivor Annuities]] - Common annuity type with refund features
- [[Pension and Annuity Income]] - Overall taxation of retirement income

## Related Publications

- [[Pub 939 - General Rule for Pensions and Annuities]] - Contains Tables III and VII

## Examples
## Related Tables

- [[04 - Assets/refund_feature_adjustment_example|Refund Feature Adjustment Example]] - Demonstrates how to calculate the adjustment required for the value of a refund feature when there are multiple annuitants.
- [[04 - Assets/refund_feature_calculation_example|Refund Feature Calculation Example]] - Demonstrates the calculation of investment in a contract adjusted for the value of a refund feature, using a $21,053 net cost annuity at age 65.

**Example 1**: Age 65, single-life annuity purchased for $21,053 with refund feature guaranteeing return of full cost. Annual payment $1,200. Guaranteed for 17.54 years (rounded to 18). Table VII shows 15% for age 65, 18-year guarantee. Value of refund feature = 15% × $21,053 = $3,158. Investment in contract = $17,895.

**Example 2**: Surviving spouse age 48, child receives temporary annuity. Guaranteed amount $9,162, but after subtracting child's expected return, net guaranteed is $3,762. Table VII shows 0% for 2-year duration at age 48. No adjustment needed.

**Example 3**: Joint and survivor annuity, both annuitants under age 75, survivor gets 50%, guaranteed less than 2½ years. Value of refund feature = $0 (zero value rules apply).