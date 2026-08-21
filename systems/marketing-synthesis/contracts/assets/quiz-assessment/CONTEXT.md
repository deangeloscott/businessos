---
id: marketing.assets.quiz-assessment
type: playbook
version: 1.1.0
owner_system: marketing-synthesis
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
# Quiz / Assessment Conversion Asset

## Purpose
Create a diagnostic experience that gives the participant useful feedback while qualifying/segmenting toward a relevant next action.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed quiz / assessment conversion asset that matches audience awareness, offer, proof, and acquisition context.

## Run When
Run when an Opportunity or WorkRequest requires quiz / assessment conversion asset to remove a commercial persuasion gap or create the required conversion asset.

## Process
1. [AI] Define user value, decision/diagnostic construct, target audience, required segmentation, and downstream action.
2. [HYBRID] Ensure questions genuinely measure/usefully proxy the construct rather than forcing answers toward the Offer.
3. [AI] Design question sequence, response scales, branching, scoring logic, and result categories.
4. [DETERMINISTIC] Specify scoring/branching deterministically and test boundary cases.
5. [AI] Write result explanations and recommendations that reflect answers and disclose limitations.
6. [HYBRID] Map qualified segments to appropriate Offer/next step without misrepresenting the assessment as clinical/scientific unless validated.
