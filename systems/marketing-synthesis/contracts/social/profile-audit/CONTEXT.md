---
id: marketing.social.profile-audit
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
# Conversion-Oriented Social Profile Audit

## Purpose
Evaluate whether a social profile clearly communicates who the business helps, why it matters, why to trust it, and what qualified visitors should do next.

## Business Outcome
Improve qualified progression from profile visits without treating the profile as generic branding decoration.

## Run When
Use when a social profile is a meaningful acquisition/conversion surface or performance/message has changed.

## Process
1. [HYBRID] Resolve the profile’s platform, AudienceSegment, Brand, Offer, acquisition role, desired action, current Assets, and relevant platform context available to the model/harness.
2. [AI] Audit profile image/identity recognition, display name/handle clarity, bio/value proposition, proof, CTA, link destination, pinned/featured content, and message continuity from common entry content.
3. [AI] Identify ambiguity about audience, outcome, differentiation, credibility, or next step and separate profile persuasion from downstream landing/journey friction.
4. [HYBRID] Check platform field/character/link constraints and broken/stale links using the strongest available current source/tool when useful.
5. [HYBRID] Verify claims/proof and ensure platform conventions do not override brand accuracy/accessibility.
6. [AI] Prioritize the smallest profile changes likely to improve qualified action, labeling hypotheses and unknowns honestly rather than inventing uplift.
7. [AI] Produce the useful output directly: a corrected/optimized profile draft or recommendation Asset, plus baseline measurements when they materially help evaluation. Create a `WorkRequest` only when implementation genuinely needs a durable handoff to another owner. Do not create an execution packet or permission object.

## Verification
- Recommendations are traceable to the actual profile, business context, and relevant evidence.
- Customer-facing claims stay within established business truth.
- Baseline/performance values are recorded only when actually observed.
- AURA does not substitute an internal action object for the real implementation tool or owner.
