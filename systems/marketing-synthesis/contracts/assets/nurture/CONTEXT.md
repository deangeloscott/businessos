---
id: marketing.assets.nurture
type: playbook
version: 1.1.0
owner_system: marketing-synthesis
artifact_role: customer_facing_production_root
risk: low
autonomy_ceiling: 3
reads:
- Opportunity
- type: Insight
  owner_system: customer-intelligence
- type: Insight
  owner_system: competitor-intelligence
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
  - email.send
  - social.ad.publish
  - cms.page.publish
  - experiment.run
  - tracking.read
context:
- AudienceSegment
- Brand
- Offer
---
# Lead Nurture Strategy

## Purpose
Move not-yet-ready prospects toward a better-informed decision over time rather than repeatedly asking for the sale.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed lead nurture strategy that matches audience awareness, offer, proof, and acquisition context.

## Run When
Run when an Opportunity or WorkRequest requires lead nurture strategy to remove a commercial persuasion gap or create the required conversion asset.

## Process
1. [AI] Define entry source, awareness, reason not ready, likely information/experience needed, buying horizon, and exit criteria.
2. [AI] Build content/message progression across education, proof, comparison, objection resolution, use cases, customer outcomes, and appropriate offers.
3. [HYBRID] Personalize/branch only on reliable signals; avoid pretending to know motives not evidenced.
4. [AI] Determine cadence based on decision cycle and value delivery rather than maximum contact frequency.
5. [DETERMINISTIC] Define lifecycle state transitions, suppression on conversion, and handoff to Customer Optimization/Sales where applicable.
6. [HYBRID] Measure progression to qualified intent rather than opens alone.
