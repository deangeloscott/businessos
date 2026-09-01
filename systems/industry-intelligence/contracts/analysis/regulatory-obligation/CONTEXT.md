---
id: industry.analysis.regulatory-obligation
type: playbook
owner_system: industry-intelligence
reads:
- IndustryEvent
- SourceRecord
- Observation
- Insight
writes:
- IndustryEvent
- Observation
- Insight
capabilities:
  required:
  - research.web.read
  optional:
  - news.read
  - rss.read
  - regulatory.read
  - research.paper.read
  - market_data.read
  - social.listen
  - webpage.snapshot
  - webpage.compare
  - alert.read
context:
- Business
- Market
- Objective
---
# Regulatory Requirement Extraction

## Purpose
Extract what a rule, regulator action, standard, or policy explicitly requires, permits, changes, and when.

## Business Outcome
Give the business a factual compliance-impact basis without substituting unsupported legal advice.

## Run When
Run when a regulatory/standards Event may affect the business, customers, claims, data, operations, or market access.

## Process
1. [INTEGRATION] Retrieve the authoritative legal/regulatory/standards text plus official guidance, dates, scope, and amendments.
2. [AI] Identify covered entities/products/activities, jurisdictions, thresholds, explicit obligations, prohibitions, permissions, exemptions, and deadlines.
3. [AI] Separate exact text/factual requirement from interpretation and implementation implication.
4. [DETERMINISTIC] Record citations/source locations for each material requirement and current status/effective date.
5. [HYBRID] Flag ambiguous legal interpretation, enforcement uncertainty, or high-stakes questions for qualified human/legal review rather than resolving by model confidence.
6. [AI] Map confirmed requirements to affected business context/policies and create ContextUpdateProposal where canonical constraints may need updating.
7. [DETERMINISTIC] Schedule future checks for rule changes, guidance, enforcement milestones, or expiry.
