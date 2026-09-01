---
id: marketing.webinar.follow-up
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
# Webinar Follow-Up Sequence

## Purpose
Follow up based on attendance/engagement/action so people receive the appropriate next step after the webinar.

## Business Outcome
Convert appropriate attendees while continuing to deliver value to people not yet ready.

## Run When
Use after a webinar session for replay/attendee/no-show follow-up where consent permits.

## Process
1. [HYBRID] Segment by attended/no-show, duration/engagement, CTA action, purchase/booked status, questions, and relevant qualification signals using the real event/customer data available.
2. [AI] Define follow-up jobs by segment: replay/context, key lesson, question/objection, proof, Offer reminder, deadline if real, or non-commercial nurture.
3. [AI] Suppress commercial follow-up for converted/ineligible/unsubscribed people and avoid punishing no-shows with artificial pressure.
4. [AI] Use session Q&A/behavior as evidence for message relevance without inferring motive too confidently.
5. [HYBRID] Build branching/suppression, correct replay/CTA links, Offer version, and expiration conditions appropriate to the real communication system.
6. [HYBRID] Validate claims/urgency and frequency.
7. [HYBRID] Preserve the useful follow-up sequence as Assets and evaluate follow-up-to-qualified-action/revenue when data exists. Material customer/message evidence may be remembered once in the appropriate canonical evidence/Insight state; do not route it through internal AURA services. If the user asks to send/schedule and the active harness has the real capability and permission, execute directly; otherwise persist a WorkRequest only for a real durable handoff.
