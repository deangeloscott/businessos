---
id: marketing.webinar.reminders
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
# Webinar Reminder Sequence

## Purpose
Create a reminder sequence that helps registered people attend without spam or manufactured urgency.

## Business Outcome
Improve qualified attendance by reinforcing relevance and removing logistical uncertainty.

## Run When
Use after registration when reminder communication is appropriate.

## Process
1. [AI] Define the minimum reminder moments based on lead time, event time, audience behavior, and consent/channel rules.
2. [AI] Give each reminder a distinct job: confirmation/value, preparation, calendar/logistics, last practical reminder, or start-now access.
3. [AI] Reinforce one useful reason to attend rather than repeating the same promotional copy.
4. [HYBRID] Include correct date/time/timezone/access link/calendar/contact information and suppression for cancellations/unsubscribes where applicable.
5. [HYBRID] Avoid excessive frequency, fake scarcity, or urgency unrelated to a real event start.
6. [HYBRID] Test links/dynamic fields and delivery timing when the real communication system is available; the active runtime owns actual scheduling and sending.
7. [AI] Preserve the reminder sequence as Assets. If the user asks to schedule/send and the active harness has the real capability and permission, execute through that surface directly; otherwise provide the useful deliverable or persist a WorkRequest only for a real durable handoff to a separate executor.
