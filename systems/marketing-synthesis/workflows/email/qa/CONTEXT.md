---
id: marketing.email.qa
type: workflow
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
- Asset
context:
- Brand
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Email Sequence QA

## Purpose
Verify the available email sequence, logic, content, links, consent assumptions, and terminal behavior before sending or activation.

## Business Outcome
Catch material automation, personalization, Offer, consent, or message defects before they affect prospects/customers.

## Run When
Use when a commercial email sequence or configured automation needs end-to-end QA.

## Process
1. [HYBRID] Inspect the actual available sequence/configuration and verify audience/entry assumptions, sender, consent/suppression, sequence order, delays, branches, exits, Offer version, and tracking where those elements really exist.
2. [HYBRID] Review every message for claim/proof support, tone, personalization, urgency, real legal/platform constraints, and alignment with its assigned job.
3. [HYBRID] Test dynamic fields/fallbacks, links, forms/calendar/pages, rendering, unsubscribe/preferences, and reply handling where the host/external system exposes them. Do not pretend a planned automation has been configured.
4. [AI] Inspect the sequence as one conversation for repetition, contradictions, missing context, inappropriate frequency, or too many asks.
5. [HYBRID] Exercise important behavior branches such as conversion, no action, reply, unsubscribe, and failure when a real configured system is available; otherwise review the proposed branch logic as design only.
6. [AI] Report material defects and lower-severity improvements. Consent/logic/Offer defects may justify recommending against activation of that version, but AURA does not own send/launch authorization.
7. [HYBRID] If activation/sending is explicitly requested and the harness has real capability/permission, perform it through the external email/CRM system and verify the live version when practical. Otherwise preserve the usable Asset and state that activation remains unperformed.

## Verification
- QA distinguishes planned sequence logic from configuration actually observed in an external system.
- Claims, personalization, consent, frequency, urgency, and Offer terms stay within current evidence and real constraints.
- AURA does not create WorkRequests, runtime schedules, or launch gates merely because QA found remaining work.

## Completion Criteria
- The sequence/configuration inspected has a clear evidence-backed QA result, with untested or unconfigured parts stated honestly and external activation reported separately.
