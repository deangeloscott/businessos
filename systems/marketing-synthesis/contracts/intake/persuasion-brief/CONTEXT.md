---
id: marketing.intake.persuasion-brief
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
# Persuasion Brief

## Purpose
Translate a Marketing Opportunity or delegated commercial WorkRequest into the complete persuasion problem before asset creation.

## Business Outcome
Give strategy/asset production a precise definition of audience, desired action, awareness, offer, barrier, proof, constraints, and measurement.

## Run When
Run before material marketing synthesis when an equivalent approved brief is not already present.

## Process
1. [DETERMINISTIC] Resolve the originating Opportunity/WorkRequest, Offer, AudienceSegment, acquisition context, Customer/Competitor Insights, relevant ProofRecords, current Assets, and objective/economics.
2. [AI] State the exact desired commercial action and the persuasion barrier preventing the right person from taking it.
3. [AI] Define audience awareness/sophistication, existing beliefs, desired outcome, decision criteria, objections, alternatives, proof needs, and message continuity from the prior touchpoint.
4. [AI] Separate persuasion problems from journey friction, product/service failure, missing customer knowledge, or sales process issues and route those domains instead of masking them with copy.
5. [HYBRID] Identify claim, compliance, offer-term, price/guarantee, brand, and customer-quality constraints.
6. [DETERMINISTIC] Define asset/campaign requirements, success metric, baseline where available, tracking, approval, and test conditions.
7. [AI] Produce a concise persuasion brief referencing canonical evidence rather than duplicating upstream research.
