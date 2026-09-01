---
id: marketing.landing-page.message-match
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
# Landing Page Message Match

## Purpose
Ensure the landing page immediately continues the promise, intent, and expectations created by its acquisition source.

## Business Outcome
Reduce qualified visitor loss caused by disconnect between source message and destination.

## Run When
Use before writing/revising a landing page when traffic arrives from known ads, search, social, email, referrals, or campaigns.

## Process
1. [HYBRID] Resolve acquisition sources/queries/messages, target AudienceSegment, Offer, and desired action from available evidence.
2. [AI] Identify the promise, problem, outcome, proof expectation, awareness, and CTA implied before the click.
3. [AI] Define what the visitor must see/understand in the first screen/section to know they are in the right place.
4. [AI] Identify source-specific differences that require dynamic/variant pages rather than one generic headline.
5. [HYBRID] Prevent bait-and-switch between attention message and actual Offer/terms.
6. [AI] Specify the landing-page opening message hierarchy and continuity requirements.
7. [HYBRID] Preserve useful source-to-page variant/tracking relationships in the relevant Asset when future work benefits from them. Do not create a WorkRequest merely to move into copy, architecture, or testing methods.
