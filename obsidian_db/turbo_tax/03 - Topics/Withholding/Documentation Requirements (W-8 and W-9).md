---
created: 2026-02-28
updated: 2026-02-28
type: topic
category: Withholding
tags:
  - topic
  - withholding
  - documentation
  - forms
---

# Documentation Requirements (W-8/W-9)

## Overview

Withholding agents must obtain valid documentation to determine:
1. Whether a payee is a U.S. or foreign person
2. The appropriate withholding rate (statutory, treaty, or exemption)
3. The payee's Chapter 4 status for FATCA purposes

## Form W-9 - U.S. Person Certification

### When Required
- Payee claims to be a U.S. person
- Required for Form 1099 reporting
- Required to avoid Chapter 3 withholding

### Information Required
- Name and business name (if applicable)
- Entity type (individual, corporation, partnership, etc.)
- Address
- Taxpayer Identification Number (TIN)
- Certification under penalties of perjury

### Backup Withholding
If Form W-9 is not provided or TIN is incorrect:
- 24% backup withholding applies
- Report on Form 1099

## Forms W-8 Series - Foreign Person Documentation

### Form W-8BEN (Individuals)

**Purpose:** Certificate of Foreign Status for **individuals**

**Required Information:**
- Name of individual
- Country of citizenship
- Permanent residence address
- Mailing address (if different)
- Foreign TIN (or U.S. TIN if claiming treaty benefits)
- Date of birth (if no foreign TIN)
- Treaty article for reduced rate (if claiming)

**Validity Period:**
- Generally valid for 3 years
- Expires on December 31 of the third year following signing

### Form W-8BEN-E (Entities)

**Purpose:** Certificate of Foreign Status for **entities**

**Required Information:**
- Entity name and type
- Country of incorporation/organization
- Permanent residence address
- Chapter 4 status (FFI status, NFFE type, etc.)
- GIIN (if an FFI)
- Treaty article for reduced rate (if claiming)
- Limitation on benefits certification

**Chapter 4 Status Options:**
- Participating FFI
- Registered deemed-compliant FFI
- Reporting Model 1 FFI
- Reporting Model 2 FFI
- Nonparticipating FFI
- Exempt beneficial owner
- Active NFFE
- Passive NFFE
- Owner-documented FFI

### Form W-8ECI

**Purpose:** Claim that income is **effectively connected** with U.S. trade or business

**Required Information:**
- Name and status (individual or entity)
- Address
- TIN (U.S. or foreign)
- Certification that income is ECI
- Certification that income is includible in gross income

**Key Point:** Withholding not required on ECI if valid Form W-8ECI provided.

### Form W-8EXP

**Purpose:** Certificate for **foreign governments, international organizations, and tax-exempt entities**

**Required Information:**
- Name and status
- Address
- Country of organization
- Type of entity (government, international organization, etc.)
- Chapter 4 status

**Exempt Recipients:**
- Foreign governments
- International organizations
- Foreign central banks of issue
- Foreign tax-exempt organizations

### Form W-8IMY

**Purpose:** Certificate for **foreign intermediaries, flow-through entities, and U.S. branches**

**Required Information:**
- Name and status (QI, NQI, WP, WT, etc.)
- GIIN (if QI, WP, or WT)
- Chapter 4 status
- Withholding statement allocation

**Must Associate:**
- Forms W-8 or W-9 for underlying payees
- Withholding statement with allocation information

## Reliability Standards

### Generally
Documentation is reliable if:
- Form is complete and valid
- Can determine portion of payment related to each form
- No actual knowledge or reason to know information is incorrect

### Standards of Knowledge (Chapter 4)
- Cannot rely on form if reason to know it's unreliable
- Must apply presumption rules if documentation is questionable

## Validity Periods

| Form Type | Validity Period |
|-----------|-----------------|
| Form W-8BEN (individual) | 3 years from signing |
| Form W-8BEN-E | 3 years from signing |
| Form W-8ECI | 3 years from signing |
| Form W-8EXP | 3 years from signing |
| Form W-8IMY | 3 years from signing |

**Expiration:** December 31 of the third year following the date of signing.

## Change in Circumstances

Documentation becomes invalid if:
- Payee changes status (U.S. to foreign or vice versa)
- Payee no longer qualifies for treaty benefits
- Payee's Chapter 4 status changes
- Form expires

**Withholding agent must:** Obtain new documentation or apply presumption rules.

## Electronic Documentation

### Third-Party Repositories
- May accept electronic Form W-8 from approved repository
- Must meet requirements of Reg. §1.1441-1(e)(4)(iv)(E)

### QI Documentation
- QIs may rely on KYC documentation under local law
- Documentation must meet QI agreement requirements

## Presumption Rules

If documentation is not obtained or is invalid:

### For Chapter 3
Presume payee is:
1. U.S. person (if U.S. indicia and no Form W-8)
2. Foreign person (if foreign indicia)
3. Undocumented (withhold at 30%)

### For Chapter 4
Presume payee is:
1. Nonparticipating FFI (if FFI with no documentation)
2. Passive NFFE with substantial U.S. owners (if NFFE with no documentation)

## Related Topics

- [[Withholding Agent]] - Who must obtain documentation
- [[Foreign Intermediaries]] - Form W-8IMY requirements
- [[FATCA Chapter 4 Withholding]] - Chapter 4 status certification
- [[Tax Treaties for Withholding]] - Treaty documentation
- [[Effectively Connected Income (ECI)]] - Form W-8ECI
- [[Forms 1042 and 1042-S Reporting]] - Using documentation for reporting

## Related Forms

- [[Form W-9]] - U.S. person certification
- [[Form W-8BEN]] - Individual foreign status
- [[Form W-8BEN-E]] - Entity foreign status
- [[Form W-8ECI]] - Effectively connected income
- [[Form W-8EXP]] - Exempt entities
- [[Form W-8IMY]] - Intermediaries

## Source

- [[Pub 515 - Withholding of Tax on Nonresident Aliens and Foreign Entities]]
- Instructions for Forms W-8BEN, W-8BEN-E, W-8ECI, W-8EXP, W-8IMY
- Regulations Sections 1.1441-1 through 1.1441-6
