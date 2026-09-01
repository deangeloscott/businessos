---
id: marketing.strategy.cta
type: playbook
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
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
Use when a Marketing asset/campaign needs a primary commercial next step. An Opportunity or real durable WorkRequest may provide context but is not required.

## Process
1. [AI] Define the desired business outcome and the smallest meaningful customer commitment that advances toward it.
2. [HYBRID] Resolve journey mechanics, availability, eligibility, capacity, sales motion, Offer terms, and tracking requirements from real business context where available.
3. [AI] Match CTA commitment level to audience intent/awareness and identify when a lower-friction intermediate action is more appropriate.
4. [AI] Define CTA promise, what happens next, required expectation setting, and any qualification/disqualification needed before action.
5. [HYBRID] Avoid dark patterns, vague consent, false urgency, or action labels that hide meaningful consequences.
6. [AI] Remove competing CTAs or explicitly rank secondary actions when they must exist.
7. [HYBRID] Define useful CTA measurement and use relevant Customer Optimization operating knowledge directly when real journey/form mechanics need work. Preserve the CTA guidance as a Marketing-owned strategy Asset; create a WorkRequest only for a real durable organizational handoff.
