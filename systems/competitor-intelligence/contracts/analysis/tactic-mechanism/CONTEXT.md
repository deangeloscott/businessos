---
id: competitor.analysis.tactic-mechanism
type: playbook
owner_system: competitor-intelligence
reads:
- Competitor
- SourceRecord
- Observation
- Insight
writes:
- Observation
- Insight
capabilities:
  required:
  - research.web.read
  optional:
  - webpage.snapshot
  - webpage.compare
  - advertising.observe
  - social.observe
  - review.read
  - search.observe
  - document.read
context:
- Business
- Market
- AudienceSegment
- Offer
---
# Competitor Tactic Mechanism Extraction

## Purpose
Determine the plausible mechanism behind a competitor tactic and what parts may transfer to this business.

## Business Outcome
Turn competitor activity into testable learning without copying execution or assuming visible success proves causality.

## Run When
Run after a tactic is observed and appears important enough to investigate.

## Process
1. [AI] Describe the tactic in functional terms: audience, trigger, message/action, channel, sequence, and intended behavior.
2. [AI] Separate the underlying mechanism from competitor-specific brand, distribution, budget, audience, asset, or operational advantages.
3. [AI] Identify evidence that the tactic is actually producing results versus merely being present.
4. [AI] Generate competing explanations for observed success, including selection, paid amplification, existing brand, timing, or other concurrent changes.
5. [HYBRID] Determine which mechanism components are ethically/legal/operationally transferable and which are not.
6. [AI] Convert the mechanism into a business-specific experiment/hypothesis rather than a copy instruction.
7. [AI] Publish a scoped Insight/Learning candidate with evidence and uncertainty.
