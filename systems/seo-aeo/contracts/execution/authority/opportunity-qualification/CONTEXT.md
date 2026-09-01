---
id: seo.execution.authority.opportunity-qualification
type: playbook
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
# Authority Opportunity Qualification

## Purpose
Decide whether an off-page opportunity is worth pursuing and which legitimate strategy fits it.

## Business Outcome
Improve valuable organic discovery through authority opportunity qualification, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Authority Opportunity Qualification**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Verify the source/site/page exists, is relevant, and has a real audience or ecosystem function.
2. [HYBRID] Inspect editorial patterns, outbound links, ownership, spam indicators, paid-placement signals, conflicts, and policy risk.
3. [AI] Determine what value the brand can legitimately provide to earn a mention/link/citation.
4. [HYBRID] Estimate business relevance, target-page fit, likelihood, material cost, reputational risk, and strategic leverage.
5. [AI] Classify tactic as established/emerging/experimental/prohibited using system policy.
6. [HUMAN] Approve, defer, reject, or route to the correct acquisition playbook with an interpretable rationale.


