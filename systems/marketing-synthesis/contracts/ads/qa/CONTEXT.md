---
id: marketing.ads.qa
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
# Advertising Launch QA

## Purpose
Verify ads, creative, claims, Offer, destinations, tracking, and variant mapping before activation.

## Business Outcome
Prevent spend and customer harm caused by broken or misleading ad execution.

## Run When
Run when an advertising campaign requires this persuasion or QA sub-process; media buying/targeting execution remains outside this OS.

## Process
1. [DETERMINISTIC] Verify final copy/creative version, audience/placement context supplied by acquisition operator, destination, Offer, CTA, tracking, and variant IDs.
2. [HYBRID] Validate claims/proof, sensitive content, urgency/scarcity, comparisons, testimonial context, and applicable platform/compliance requirements.
3. [AI] Check hook/creative/copy coherence and qualified audience intent.
4. [DETERMINISTIC] Click/test destinations, links, forms/events, dynamic parameters, and responsive creative rendering where possible.
5. [AI] Confirm each variant represents its intended hypothesis and is not accidentally changing multiple unrelated variables.
6. [DETERMINISTIC] Block activation on material errors and provide exact correction requirements.
7. [DETERMINISTIC] Verify live creative/destination after activation and monitoring instrumentation.
