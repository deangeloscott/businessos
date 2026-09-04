---
id: marketing.ads.copy
type: workflow
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
- Asset
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
1. [AI] Resolve chosen angle, audience, Offer, channel/placement constraints, proof, and destination from the current organizational context or a real handoff when one exists.
2. [AI] Write opening/primary text/headline/CTA as required, making the audience-relevant value/tension specific quickly.
3. [AI] Include enough mechanism/proof/context to qualify attention for the placement rather than maximizing curiosity alone.
4. [HYBRID] Validate claims, comparisons, urgency, Offer terms, restricted/sensitive targeting implications, and platform policy constraints.
5. [AI] Ensure destination message can fulfill the ad promise and identify any useful landing-page adaptation directly; do not create an internal WorkRequest merely because another AURA method may help.
6. [AI] Produce materially different copy only when testing a new hypothesis or execution variable with a clear reason.
7. [AI] Preserve the useful copy/variant Asset and evidence linkage when future work benefits from it.
