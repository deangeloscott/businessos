---
id: competitor.analysis.packaging
type: playbook
owner_system: competitor-intelligence
reads:
- Competitor
- type: Insight
  owner_system: customer-intelligence
- Observation
- SourceRecord
writes:
- Competitor
- Observation
- Insight
capabilities:
  required:
  - research.web.read
  optional:
  - webpage.snapshot
  - webpage.compare
  - advertising.observe
  - review.read
  - crm.opportunity.read
  - social.observe
context:
- AudienceSegment
- Business
- EconomicContext
- Market
- Objective
- Offer
- ProductService
---
# Packaging Intelligence

## Purpose
Understand how competitors bundle capabilities, service levels, access, and constraints across offers.

## Business Outcome
Improve competitive decisions through evidence-backed packaging intelligence, without mistaking observed activity for proven effectiveness.

## Run When
Run when a decision requires current packaging intelligence and canonical competitor intelligence is missing, stale, contradictory, or insufficiently specific.

## Process
1. [INTEGRATION] Capture plan/product/package tables and associated feature/limit/service descriptions.
2. [AI] Normalize package components into comparable capability/outcome/service dimensions while preserving unique constructs.
3. [HYBRID] Distinguish base product functionality, add-ons, implementation/services, support, limits, and contractual requirements.
4. [DETERMINISTIC] Compare packages across competitor and prior state; identify additions/removals/rebundling.
5. [AI] Identify apparent segment targeting and upsell/land-expand design with evidence.
6. [HYBRID] Avoid labeling packaging as superior/inferior without customer decision or performance evidence.
7. [DETERMINISTIC] Publish Observations/Insights and update canonical Competitor summary.
