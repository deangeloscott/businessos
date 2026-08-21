---
id: customer.evidence-collection.sales-lost
type: playbook
version: 1.1.0
owner_system: customer-intelligence
risk: low
autonomy_ceiling: 4
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
  - crm.opportunity.read
  optional:
  - crm.contact.read
  - analytics.read
context:
- AudienceSegment
- Market
- Offer
- ProductService
---
# Sales & Lost-Deal Mining

## Purpose
Extract customer-stated buying criteria, objections, alternatives, and loss reasons from sales evidence while separating seller assumptions.

## Business Outcome
Reduce uncertainty about customers through sales & lost-deal mining, so downstream decisions reflect current customer evidence rather than assumption.

## Run When
Run when a decision requires current sales & lost-deal mining and existing Customer Insights are missing, stale, too broad, or insufficiently supported.

## Process
1. [DETERMINISTIC] Select a defined cohort by period, segment, offer, stage outcome, and data-quality criteria.
2. [INTEGRATION] Retrieve CRM outcomes, loss reasons, relevant notes, emails/call references, and deal attributes.
3. [AI] Separate customer-stated evidence from salesperson-entered interpretation; label unsupported CRM reason codes accordingly.
4. [AI] Normalize reasons into a controlled taxonomy while preserving raw customer language and multi-cause relationships.
5. [HYBRID] Distinguish primary decision driver, contributing reasons, stated alternative, timing/budget/process causes, and unknowns.
6. [DETERMINISTIC] Compare frequencies/rates across segments, offer, rep, stage, and competitor while controlling for missing-data coverage.
7. [AI] Identify themes that materially affect buying decisions and contradictions between stated reasons and behavioral evidence.
8. [HYBRID] Publish Customer Insights at justified scope and create research gaps when loss-reason quality is inadequate.
