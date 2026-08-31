---
id: seo.execution.authority.outreach
type: playbook
version: 1.1.0
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
writes:
- SEOAssetState
- ChangeEvent
- Asset
capabilities:
  required:
  - backlink.read
  optional:
  - research.web.read
  - crm.contact.read
  - email.send
evidence_inputs:
- backlink/referring-domain/mention evidence and prospect records
---
# Authority Outreach

## Purpose
Execute personalized, ethical outreach for already-qualified authority opportunities.

## Business Outcome
Improve valuable organic discovery through authority outreach, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Authority Outreach**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Load the qualified opportunity, exact source/page/contact, value proposition, owned asset, constraints, and prior contact history.
2. [HYBRID] Choose the recipient/channel and confirm communication is lawful/appropriate for the market and relationship.
3. [AI] Generate a concise message grounded in the recipient's actual page/audience and the specific value being offered.
4. [HYBRID] Run factual, brand, compliance, personalization, duplicate-contact, and prohibited-claim checks.
5. [INTEGRATION] Route according to MessagingProvider/autonomy: draft for human, queue for approval, or send when explicitly authorized.
6. [INTEGRATION] Record send time/message/version and schedule a limited follow-up sequence; stop on opt-out, negative response, or completion.


