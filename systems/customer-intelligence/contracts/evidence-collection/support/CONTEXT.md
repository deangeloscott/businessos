---
id: customer.evidence-collection.support
type: playbook
owner_system: customer-intelligence
reads:
- SourceRecord
- Observation
- Insight
writes:
- SourceRecord
- Observation
- Insight
capabilities:
  required:
  - support.ticket.read
  optional:
  - crm.contact.read
  - analytics.read
context:
- AudienceSegment
- Market
- Offer
- ProductService
---
# Support Intelligence Mining

## Purpose
Turn support interactions into customer understanding without confusing operational frequency with strategic importance.

## Business Outcome
Reduce uncertainty about customers through support intelligence mining, so downstream decisions reflect current customer evidence rather than assumption.

## Run When
Run when a decision requires current support intelligence mining and existing Customer Insights are missing, stale, too broad, or insufficiently supported.

## Process
1. [DETERMINISTIC] Select the relevant time window, product/offer, segment, channel, and ticket/contact categories.
2. [INTEGRATION] Retrieve ticket text, disposition, timestamps, resolution metadata, and customer stage subject to access policy.
3. [DETERMINISTIC] Remove exact duplicates/system messages and preserve raw references.
4. [AI] Classify customer-described problem, expectation, confusion, desired outcome, sentiment, severity, and repeated language.
5. [HYBRID] Separate one-off defects, documentation gaps, systemic friction, expectation mismatch, and strategic unmet needs.
6. [DETERMINISTIC] Compare frequency, affected-customer rate, recurrence, time trend, and segment concentration.
7. [AI] Cross-check with existing Customer Insights and Customer Optimization journey evidence before making broad conclusions.
8. [HYBRID] Publish Observations/Insights and route operational friction evidence to Customer Optimization when relevant.
