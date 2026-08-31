---
id: customer.evidence-collection.interview-participants
type: playbook
version: 1.3.0
owner_system: customer-intelligence
reads:
- SourceRecord
- Observation
writes: []
capabilities:
  required:
  - crm.contact.read
  optional:
  - customer_feedback.read
context:
- AudienceSegment
- Objective
---
# Customer Interview Participant Selection

## Purpose
Select interview participants from the correct population and contrast groups.

## Business Outcome
Ensure interview evidence covers the customer situations needed for the decision instead of only easy-to-reach advocates.

## Run When
Run after sample design when interview participants must be selected and recruited.

## Process
1. [DETERMINISTIC] Apply the sample-design inclusion/exclusion criteria to available contacts or research pools.
2. [AI] Balance priority segments and contrast cases based on the decision, not equal quotas by default.
3. [HYBRID] Identify overrepresentation of promoters, power users, active accounts, or highly responsive contacts.
4. [DETERMINISTIC] Remove duplicates and respect contact/consent/research restrictions.
5. [AI] Prioritize participants that fill the most material evidence gaps while preserving comparison validity.
6. [DETERMINISTIC] Produce a recruitment list with group/segment rationale and alternates.
7. [AI] Record unresolved coverage gaps that should constrain later conclusions.
