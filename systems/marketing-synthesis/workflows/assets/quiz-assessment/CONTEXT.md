---
id: marketing.assets.quiz-assessment
type: workflow
owner_system: marketing-synthesis
artifact_role: customer_facing_production_root
reads:
- Opportunity
- type: Insight
  owner_system: customer-intelligence
- type: Insight
  owner_system: competitor-intelligence
- Asset
- WorkRequest
writes:
- Asset
context:
- AudienceSegment
- Brand
- Offer
---
# Quiz / Assessment Conversion Asset

## Purpose
Create a diagnostic experience that gives the participant useful feedback while qualifying/segmenting toward a relevant next action.

## Business Outcome
Increase the likelihood of the desired commercial action through an evidence-backed quiz / assessment conversion asset that matches audience awareness, Offer, proof, and acquisition context.

## Run When
Use when a quiz or assessment is useful to remove a commercial persuasion gap or support a qualified next action. An Opportunity or real durable WorkRequest may provide context but is not required.

## Process
1. [AI] Define user value, decision/diagnostic construct, target audience, required segmentation, and downstream action.
2. [HYBRID] Ensure questions genuinely measure or usefully proxy the construct rather than forcing answers toward the Offer.
3. [AI] Design question sequence, response scales, branching, scoring logic, and result categories.
4. [DETERMINISTIC] Specify scoring/branching clearly enough to implement and test boundary cases when the assessment requires deterministic behavior.
5. [AI] Write result explanations and recommendations that reflect answers and disclose limitations.
6. [HYBRID] Map qualified segments to an appropriate Offer/next step without misrepresenting the assessment as clinical/scientific unless validated. Use the active harness's real implementation/design capabilities directly when building the experience; persist a WorkRequest only for a real durable organizational handoff.
