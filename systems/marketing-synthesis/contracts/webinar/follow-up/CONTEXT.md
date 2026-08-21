---
id: marketing.webinar.follow-up
type: playbook
version: 1.3.0
owner_system: marketing-synthesis
risk: medium
autonomy_ceiling: 2
reads:
- Opportunity
- Insight
- ProofRecord
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
# Webinar Follow-Up Sequence

## Purpose
Follow up based on attendance/engagement/action so people receive the appropriate next step after the webinar.

## Business Outcome
Convert appropriate attendees while continuing to deliver value to people not yet ready.

## Run When
Run after a webinar session and for replay/attendee/no-show follow-up where consent permits.

## Process
1. [DETERMINISTIC] Segment by attended/no-show, duration/engagement, CTA action, purchase/booked status, questions, and relevant qualification signals.
2. [AI] Define follow-up jobs by segment: replay/context, key lesson, question/objection, proof, Offer reminder, deadline if real, or non-commercial nurture.
3. [AI] Suppress commercial follow-up for converted/ineligible/unsubscribed people and avoid punishing no-shows with artificial pressure.
4. [AI] Use session Q&A/behavior as evidence for message relevance without inferring motive too confidently.
5. [DETERMINISTIC] Build branching/suppression, correct replay/CTA links, Offer version, and expiration conditions.
6. [HYBRID] Validate claims/urgency and frequency.
7. [DETERMINISTIC] Measure follow-up→qualified action/revenue and return customer/message evidence to relevant systems.
