---
id: marketing.ads.copy
type: playbook
version: 1.3.0
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
- WorkRequest
- Asset
capabilities:
  required:
  - none
  optional:
  - creative.text.generate
  - tracking.read
  - conversion.read
  - marketing.performance.read
  - experiment.run
  - cms.page.publish
  - email.send
  - social.ad.publish
context:
- Brand
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Advertising Copy

## Purpose
Write concise ad copy that earns qualified attention and creates accurate intent for the destination.

## Business Outcome
Generate clicks/views/actions from the right people without bait-and-switch or unsupported promises.

## Run When
Run when an advertising campaign requires this persuasion or QA sub-process; media buying/targeting execution remains outside this OS.

## Process
1. [DETERMINISTIC] Resolve chosen angle, audience, Offer, channel/placement constraints, proof, and destination.
2. [AI] Write opening/primary text/headline/CTA as required, making the audience-relevant value/tension specific quickly.
3. [AI] Include enough mechanism/proof/context to qualify attention for the placement rather than maximizing curiosity alone.
4. [HYBRID] Validate claims, comparisons, urgency, Offer terms, restricted/sensitive targeting implications, and platform policy constraints.
5. [AI] Ensure destination message can fulfill the ad promise and identify required landing-page variant.
6. [AI] Produce materially different copy only when testing a new hypothesis or execution variable with a clear reason.
7. [DETERMINISTIC] Link variants to angle/test IDs and claim evidence.
