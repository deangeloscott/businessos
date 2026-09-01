---
id: industry.monitoring.technology
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
- PlatformChange
capabilities:
  required:
  - research.web.read
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
---
# Technology & Platform Monitoring

## Purpose
Detect technology/platform changes that alter capabilities, customer expectations, channel behavior, or business risk.

## Business Outcome
Improve the business response to external change through timely, evidence-backed technology & platform monitoring.

## Run When
Run when a decision or monitoring signal requires current technology & platform monitoring and existing Industry Intelligence is missing, stale, or unresolved.

## Process
1. [INTEGRATION] Monitor primary vendor/platform announcements, technical documentation, release notes, and credible independent evidence.
2. [AI] Extract what capability/policy/interface changed, availability, affected users/markets, timing, and migration/deprecation requirements.
3. [HYBRID] Separate announced future capability from generally available current state and marketing claims from verified functionality.
4. [AI] Map business/customer/competitor/channel implications and dependencies.
5. [HYBRID] Assess urgency based on effective dates, competitive impact, operational exposure, and strategic upside.
6. [DETERMINISTIC] For platform/vendor topics, create/update the current PlatformChange through the shared versioned state path; unchanged rechecks refresh verification rather than creating duplicates. Create/update IndustryEvent/Insight as needed and notify affected systems only for meaningful deltas.
