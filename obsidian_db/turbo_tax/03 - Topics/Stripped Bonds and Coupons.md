---
created: 2026-02-28
updated: 2026-02-28
type: topic
category: Investment Income
tags:
  - topic
  - investment-income
  - oid
  - debt-instruments
  - strips
---

# Stripped Bonds and Coupons

## Overview

Stripped bonds and coupons are debt instruments where the interest and principal components have been separated. Each component becomes a separate security with its own OID calculations. The Treasury's STRIPS program is the most common example.

## What Are Stripped Securities?

### Stripped Coupon
- The right to receive an interest payment from a bond
- Separated from the principal obligation
- Becomes a zero-coupon security

### Stripped Principal
- The right to receive principal at maturity
- Separated from the interest coupons
- Also becomes a zero-coupon security

## STRIPS Program

**Separate Trading of Registered Interest and Principal of Securities**

- U.S. Treasury program allowing separation of Treasury securities
- Creates zero-coupon securities from Treasury bonds/notes
- Listed in Section II of the OID Tables
- Also includes Government-Sponsored Enterprise STRIPS

## Tax Treatment

### OID Calculation
- Stripped components are treated as OID instruments
- Use constant yield method
- Issue price = purchase price of stripped component
- Stated redemption price = amount to be received

### Zero Coupon Bonds
- No periodic interest payments
- All return comes from difference between purchase price and redemption value
- Must accrue OID annually

## OID Tables - Section II

Section II contains:
- Stripped coupons and principal from U.S. Treasury securities
- Government-Sponsored Enterprise stripped components
- Debt instruments backed by Treasury securities

Information shown:
- CUSIP number
- Maturity date
- Issue date
- Total OID per $1,000 redemption price for calendar year

## Calculations

### For Instruments Listed in OID Tables
1. Find the instrument in Section II
2. Use the annual OID amount listed
3. Adjust for actual principal/face amount

### For Instruments Not Listed
1. Determine the yield to maturity
2. Use constant yield method
3. Accrue OID daily over the holding period

## Reporting

### Form 1099-OID
- Box 1: OID on corporate stripped securities
- Box 8: OID on Treasury stripped securities

### Schedule B
Report OID and any interest received (if applicable)

## Related Topics

- [[Original Issue Discount (OID)]] - Core concept
- [[OID Tables]] - Section II data source
- [[Inflation-Indexed Debt Instruments]] - May have stripped components
- [[U.S. Treasury Bills]] - Source securities for STRIPS
- [[Zero Coupon Bonds]] - Type of stripped security

## Related Forms

| Form | Relevance |
|------|-----------|
| [[Form 1099-OID]] | Reports OID on stripped securities |
| [[Schedule B (Form 1040)]] | Interest and OID reporting |
| [[Form 8949]] | Disposition reporting |

## References

- [[Pub 1212 - Guide to Original Issue Discount (OID) Instruments]] - Detailed calculation rules
- [[Pub 550 - Investment Income and Expenses]] - Investment rules
- TreasuryDirect.gov - STRIPS program information
