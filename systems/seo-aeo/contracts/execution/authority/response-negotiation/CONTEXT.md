---
id: seo.execution.authority.response-negotiation
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
# Outreach Response and Negotiation

## Purpose
Handle replies to authority outreach while protecting brand, editorial integrity, budget, and policy boundaries.

## Business Outcome
Improve valuable organic discovery through outreach response and negotiation, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Outreach Response and Negotiation**, or when an authorized incident response requires it.

## Process
1. [AI] Classify response: positive, question, request, paid offer, condition, rejection, opt-out, wrong contact, or ambiguous.
2. [INTEGRATION] Retrieve opportunity strategy and allowed concessions/material costs.
3. [HUMAN] Answer factual questions from approved evidence; escalate unknown claims, legal terms, paid arrangements, or reputational concerns.
4. [AI] Evaluate requested placement/terms against editorial legitimacy, disclosure rules, business value, and tactic classification.
5. [HYBRID] Agree, counter, decline, or escalate; never conceal sponsorship or misrepresent relationships.
6. [DETERMINISTIC] Record resolution, resulting asset/link/mention, cost, conditions, and future relationship notes.


