---
id: marketing.social.profile-audit
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
# Conversion-Oriented Social Profile Audit

## Purpose
Evaluate whether a social profile clearly communicates who the business helps, why it matters, why to trust it, and what qualified visitors should do next.

## Business Outcome
Improve qualified progression from profile visits without treating the profile as generic branding decoration.

## Run When
Run when a social profile is a meaningful acquisition/conversion surface or performance/message has changed.

## Process
1. [DETERMINISTIC] Resolve the profile’s platform, AudienceSegment, Brand, Offer, acquisition role, desired action, current Assets, and PlatformProfile.
2. [AI] Audit profile image/identity recognition, display name/handle clarity, bio/value proposition, proof, CTA, link destination, pinned/featured content, and message continuity from common entry content.
3. [AI] Identify ambiguity about audience, outcome, differentiation, credibility, or next step and separate profile persuasion from downstream landing/journey friction.
4. [DETERMINISTIC] Check platform field/character/link constraints and broken/stale links.
5. [HYBRID] Verify claims/proof and ensure platform conventions do not override brand accuracy/accessibility.
6. [AI] Prioritize the smallest profile changes likely to improve qualified action.
7. [DETERMINISTIC] Produce an optimization ActionPacket and baseline metrics.
