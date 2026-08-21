---
id: marketing.assets.webinar
type: playbook
version: 1.3.0
owner_system: marketing-synthesis
risk: medium
autonomy_ceiling: 3
reads:
- Opportunity
- type: Insight
  owner_system: customer-intelligence
- type: Insight
  owner_system: competitor-intelligence
- Asset
- WorkRequest
- ProofRecord
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
subcontracts:
  required:
  - marketing.webinar.objective
  - marketing.webinar.teaching-architecture
  - marketing.webinar.persuasion-architecture
  - marketing.webinar.offer-transition
  - marketing.webinar.script
  - marketing.webinar.slide-brief
  - marketing.webinar.qa
  conditional:
  - id: marketing.webinar.registration
    when: the session requires registration
  - id: marketing.webinar.reminders
    when: registered attendees should receive reminders
  - id: marketing.webinar.follow-up
    when: post-session follow-up is permitted and valuable
---
# Webinar Persuasion

## Purpose
Design a webinar that creates genuine understanding/value while logically leading qualified attendees to an offer.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed webinar persuasion that matches audience awareness, offer, proof, and acquisition context.

## Run When
Run when an Opportunity or WorkRequest requires webinar persuasion to remove a commercial persuasion gap or create the required conversion asset.

## Process
1. [AI] Define audience starting beliefs, desired transformation, teaching promise, Offer, objections, and commercial action.
2. [AI] Structure value-first narrative: why topic matters → useful framework/demo/case → implications → transition to solution/offer → proof → fit/terms → CTA/Q&A.
3. [HYBRID] Ensure educational content stands on its own and is not merely withheld value disguised as teaching.
4. [AI] Define slide-level persuasive/teaching jobs and speaker logic; Content may own final slide production.
5. [HYBRID] Build objection/proof/FAQ plan and explicit compliance/claim checks.
6. [DETERMINISTIC] Define registration/attendance/conversion measurement and follow-up WorkRequests.
