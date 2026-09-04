---
id: industry.analysis.event-verification
type: workflow
owner_system: industry-intelligence
reads:
- IndustryEvent
- Observation
- SourceRecord
- Insight
writes:
- IndustryEvent
- Observation
- Insight
- WorkRequest
context:
- Business
- Market
- Objective
- ProductService
---
# Industry Event Verification

## Purpose
Verify high-impact event claims before AURA treats them as decision-relevant facts.

## Business Outcome
Improve the business response to external change through timely, evidence-backed industry event verification.

## Run When
Run when a decision or monitoring signal requires current industry event verification and existing Industry Intelligence is missing, stale, or unresolved.

## Process
1. [AI] Decompose the event into atomic factual claims that matter to downstream decisions.
2. [HYBRID] Assign the appropriate authoritative source type to each claim rather than relying on generic source reputation.
3. [INTEGRATION] Retrieve primary/independent corroboration and current status/date.
4. [HYBRID] Resolve discrepancies by directness, authority for the fact, freshness, and whether sources refer to different event stages.
5. [AI] Classify each claim confirmed, partially confirmed, disputed, outdated, or unverified.
6. [HYBRID] Update the IndustryEvent factual summary, status, source/observation links, and unresolved points without collapsing verification into a numeric confidence score. Preserve interpretation separately when it becomes a durable Insight.
