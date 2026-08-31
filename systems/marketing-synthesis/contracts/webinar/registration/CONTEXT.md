---
id: marketing.webinar.registration
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
# Webinar Registration Experience

## Purpose
Design the registration persuasion and expectation-setting needed to attract the right attendees.

## Business Outcome
Increase qualified registration while making the webinar promise, audience, logistics, and next steps clear.

## Run When
Run when a webinar requires registration rather than direct access.

## Process
1. [AI] Define target registrant, webinar promise/learning outcome, credibility/proof, who it is for/not for, and attendance reason now.
2. [AI] Draft registration-page/message hierarchy and CTA without overpromising what the session delivers.
3. [HYBRID] Minimize fields and route form mechanics/friction to Customer Optimization; keep only required qualification/operations data.
4. [DETERMINISTIC] Specify date/time/timezone, duration, presenter, privacy/consent, calendar, confirmation, replay policy, and tracking.
5. [AI] Design confirmation state that reinforces value and tells the registrant exactly what to do next.
6. [DETERMINISTIC] Verify event/session details and registration→attendance instrumentation.
7. [AI] Create landing-page/email/content WorkRequests as needed.
