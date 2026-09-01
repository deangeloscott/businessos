---
id: marketing.vsl.offer-cta
type: playbook
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
# VSL Offer and CTA Section

## Purpose
Design the exact transition from education/persuasion into Offer, terms, fit, risk, and next action.

## Business Outcome
Make the commercial decision clear and credible without an abrupt or manipulative pitch.

## Run When
Run when the VSL requires an Offer/CTA segment.

## Process
1. [AI] Identify the belief/understanding that should already be established before the Offer transition.
2. [AI] Introduce the Offer as the logical means of applying the mechanism/outcome and clearly define who it is/is not for.
3. [DETERMINISTIC] Present approved scope, terms, price/payment, guarantee/risk reversal, availability, and next-step facts accurately.
4. [AI] Select proof specifically supporting Offer fit/results/risk rather than repeating earlier generic proof.
5. [AI] Resolve final objections likely to block action and explain what happens after the CTA.
6. [HYBRID] Validate urgency/scarcity and avoid stacking invented value or hidden conditions.
7. [DETERMINISTIC] Define CTA/tracking and link to the exact destination/journey state.
