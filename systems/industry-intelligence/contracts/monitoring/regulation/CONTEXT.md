---
id: industry.monitoring.regulation
type: playbook
owner_system: industry-intelligence
reads:
- SourceRecord
- Observation
- Insight
writes:
- SourceRecord
- Observation
- IndustryEvent
- Insight
capabilities:
  required:
  - regulatory.read
  optional:
  - research.web.read
  - news.read
  - alert.read
  - market_data.read
context:
- Business
- Market
- Objective
- ProductService
subcontracts:
  conditional:
  - id: industry.analysis.regulatory-obligation
    when: a regulation or standard may materially apply
---
# Regulatory Monitoring

## Purpose
Track proposed, adopted, effective, and enforced regulatory changes with exact jurisdiction/status distinctions.

## Business Outcome
Improve the business response to external change through timely, evidence-backed regulatory monitoring.

## Run When
Run when a decision or monitoring signal requires current regulatory monitoring and existing Industry Intelligence is missing, stale, or unresolved.

## Process
1. [INTEGRATION] Retrieve authoritative regulator/legislative/standards sources plus qualified explanatory sources where needed.
2. [AI] Extract jurisdiction, affected entities, requirements/prohibitions, deadlines, current procedural status, exceptions, and enforcement information.
3. [DETERMINISTIC] Distinguish proposal, consultation, adoption, effective date, guidance, enforcement action, and amendment; preserve dates exactly.
4. [HYBRID] Identify uncertainty requiring legal/compliance interpretation and do not present nonlegal analysis as legal advice.
5. [AI] Map potential affected products, audiences, markets, claims, processes, and systems.
6. [HYBRID] Create Industry Insight and Context/Compliance review proposal when the change becomes operative/confirmed.
7. [DETERMINISTIC] Emit high-priority events before effective dates based on configured lead time.
