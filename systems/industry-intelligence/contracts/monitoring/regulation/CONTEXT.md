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
Track proposed, adopted, effective, amended, and enforced regulatory/standards developments with exact jurisdiction/status distinctions and no AURA-owned alert scheduler.

## Business Outcome
Give the organization reliable awareness of external regulatory change without converting monitoring into legal advice, approval state, or runtime event machinery.

## Run When
When a current business decision or monitoring intent needs regulatory/standards evidence that may have changed or remains unresolved.

## Process
1. [INTEGRATION] Retrieve authoritative regulator/legislative/standards sources plus qualified explanatory sources where they materially help interpretation.
2. [AI] Extract jurisdiction, affected entities, requirements/prohibitions, deadlines, procedural status, exceptions, effective dates, and enforcement information at the level the source supports.
3. [AI] Classify the real-world state as proposal, consultation, adoption, guidance, effective requirement, enforcement action, amendment, or another justified status. Preserve exact dates mechanically after the semantic status is resolved.
4. [AI] Identify uncertainty requiring qualified legal/compliance interpretation and do not present AURA/model analysis as legal advice.
5. [AI] Assess which active products/services, markets, claims, processes, or systems may be affected without asserting applicability beyond the evidence.
6. [HYBRID] Preserve SourceRecords, Observations, IndustryEvent state, and an Insight only when durable interpretation is useful. If a concrete legal/compliance/business decision is needed, surface that real need to the appropriate owner; do not manufacture a ContextUpdateProposal or approval lifecycle by default.
7. [AI] When future timing matters, preserve effective/deadline dates and monitoring intent. The active harness/runtime owns any real reminder, recurring check, or notification; AURA does not emit high-priority runtime events based on lead-time configuration.

## Verification
- Procedural/legal status and dates are traceable to authoritative evidence.
- Applicability/impact uncertainty remains explicit.
- Saved timing intent is not represented as an active schedule or alert.

## Completion Criteria
- The organization can tell what changed or may change, where/when it applies, what remains uncertain, and what real external deadline matters without relying on internal event or approval machinery.
