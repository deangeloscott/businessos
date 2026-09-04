---
id: marketing.ads.qa
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
# Advertising Launch QA

## Purpose
Verify ads, creative, claims, Offer, destinations, tracking, and variant mapping before activation.

## Business Outcome
Prevent spend and customer harm caused by broken or misleading ad execution.

## Run When
Use when an advertising campaign needs a final persuasion/execution QA review; media buying/targeting execution remains outside this method unless the active harness separately has that capability and the user requests it.

## Process
1. [DETERMINISTIC] Verify final copy/creative version, audience/placement context, destination, Offer, CTA, tracking, and variant IDs.
2. [HYBRID] Validate claims/proof, sensitive content, urgency/scarcity, comparisons, testimonial context, and applicable platform/compliance requirements.
3. [AI] Check hook/creative/copy coherence and qualified audience intent.
4. [DETERMINISTIC] Click/test destinations, links, forms/events, dynamic parameters, and responsive creative rendering where possible.
5. [AI] Confirm each variant represents its intended hypothesis and is not accidentally changing multiple unrelated variables.
6. [HYBRID] Return a clear readiness assessment and exact correction requirements for any material defects. Recommend against activation while material defects remain; the user/active advertising runtime and real permissions own the activation decision.
7. [HYBRID] After activation, verify live creative/destination and instrumentation when the user requests it and the active harness can inspect the real state. Preserve the QA result in the Asset or a VerificationRecord only when future work materially benefits from remembering it.
