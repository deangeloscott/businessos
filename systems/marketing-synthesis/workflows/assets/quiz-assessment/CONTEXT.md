---
id: marketing.assets.quiz-assessment
type: workflow
owner_system: marketing-synthesis
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
Create a diagnostic experience that gives the participant useful feedback while qualifying or segmenting toward a relevant next action.

## Business Outcome
Increase the likelihood of the desired commercial action through an evidence-backed assessment that matches audience context, Offer, and the real limits of what the questions can establish.

## Run When
Use when a quiz or assessment can provide genuine participant value or support a qualified next action. An Opportunity or real durable WorkRequest may provide context but is not required.

## Process
1. Define participant value, decision/diagnostic construct, target audience, required segmentation, and downstream action.
2. Ensure questions genuinely measure or usefully proxy the construct rather than forcing answers toward the Offer.
3. Design question sequence, response scales, branching, scoring logic, and result categories only to the complexity required by the construct and experience.
4. Specify deterministic scoring/branching clearly enough to implement and test boundary cases when the assessment actually requires deterministic behavior.
5. Write result explanations and recommendations that reflect the answers and disclose material limitations.
6. Map qualified segments to an appropriate Offer/next step without misrepresenting the assessment as clinical, scientific, or validated unless that is actually established. Use the active harness's real implementation/design capabilities directly when building the experience; persist a WorkRequest only for a real durable organizational handoff.

## Proportionate Scope
Use the fewest questions, branches, scores, and result categories that can produce useful participant feedback and the intended segmentation. Add complexity only when it materially improves validity or usefulness.

## Verification
- The assessment provides real participant value rather than disguised lead capture.
- Questions and scoring support the stated construct at the claimed level of rigor.
- Results and recommendations preserve uncertainty and do not overstate diagnostic validity.
