---
id: marketing.webinar.qa
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
# Webinar End-to-End QA

## Purpose
Verify the complete webinar system—registration, session, teaching, slides, Offer, links, reminders, and follow-up—before live delivery.

## Business Outcome
Prevent a high-complexity conversion event from failing because individual components work but the end-to-end experience does not.

## Run When
Run before a live/automated webinar launch and after material changes.

## Process
1. [DETERMINISTIC] Verify event/session configuration, registration, confirmation, calendar/timezone, reminder links, webinar access, recording/replay, CTA destination, follow-up triggers, and tracking.
2. [HYBRID] Review teaching promise versus actual content, persuasion integrity, claim/proof support, Offer terms, urgency/guarantee, and Q&A boundaries.
3. [AI] Walk the experience as a registrant/attendee across major states and identify broken expectations or missing context.
4. [DETERMINISTIC] Check slide/media/demo files, presenter notes, backup plan, permissions, accessibility, and technical dependencies.
5. [AI] Confirm the CTA transition and follow-up do not contradict the teaching or customer-fit criteria.
6. [DETERMINISTIC] Run test registration/attendance/action events and verify downstream instrumentation.
7. [HYBRID] Block launch on material failures and record final readiness/owner for unresolved low-risk issues.
