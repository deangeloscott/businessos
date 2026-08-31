---
id: marketing.strategy.cta
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
# Commercial CTA Strategy

## Purpose
Choose and phrase the next commercial action that best advances qualified prospects without unnecessary friction or premature commitment.

## Business Outcome
Increase qualified progression by aligning the CTA with awareness, Offer, journey mechanics, and customer intent.

## Run When
Run when a Marketing asset/campaign needs a primary commercial next step.

## Process
1. [AI] Define the desired business outcome and the smallest meaningful customer commitment that advances toward it.
2. [DETERMINISTIC] Resolve journey mechanics, availability, eligibility, capacity, sales motion, Offer terms, and tracking requirements.
3. [AI] Match CTA commitment level to audience intent/awareness and identify when a lower-friction intermediate action is more appropriate.
4. [AI] Define CTA promise, what happens next, required expectation setting, and any qualification/disqualification needed before action.
5. [HYBRID] Avoid dark patterns, vague consent, false urgency, or action labels that hide meaningful consequences.
6. [AI] Remove competing CTAs or explicitly rank secondary actions when they must exist.
7. [DETERMINISTIC] Specify CTA event/measurement and route journey/form mechanics to Customer Optimization where needed.
