---
id: marketing.ads.angle-matrix
type: playbook
version: 1.3.0
owner_system: marketing-synthesis
risk: medium
autonomy_ceiling: 2
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
- ActionPacket
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
# Advertising Angle Matrix

## Purpose
Generate distinct persuasion hypotheses for an ad campaign rather than cosmetic creative variants.

## Business Outcome
Test materially different reasons a qualified audience may act so performance produces useful marketing learning.

## Run When
Run when an advertising campaign requires this persuasion or QA sub-process; media buying/targeting execution remains outside this OS.

## Process
1. [AI] Resolve Customer Insights, Offer, awareness, source/channel context, competitor positioning, proof, and prior performance.
2. [AI] Generate distinct angles based on different pains/outcomes/mechanisms/proof/objections/comparisons/triggers—not synonym changes.
3. [AI] State the hypothesis and audience belief each angle is intended to change.
4. [HYBRID] Reject angles that require unsupported claims, exploit sensitive traits, or attract poor-fit customers.
5. [AI] Match each angle to appropriate proof/creative demonstration and destination message requirement.
6. [DETERMINISTIC] Select a testable subset that maximizes learning under available traffic/budget; media buying remains outside Marketing Synthesis.
7. [AI] Produce angle matrix with expected mechanism and measurement.
