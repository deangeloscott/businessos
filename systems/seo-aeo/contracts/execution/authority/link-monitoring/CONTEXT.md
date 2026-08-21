---
id: seo.execution.authority.link-monitoring
type: playbook
version: 1.1.0
owner_system: seo-aeo
risk: medium
autonomy_ceiling: 2
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
# Link and Mention Monitoring

## Purpose
Detect new, changed, lost, redirected, or harmful external references and decide whether action is needed.

## Business Outcome
Improve valuable organic discovery through link and mention monitoring, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Link and Mention Monitoring**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Ingest new/lost backlink and mention observations; compare with prior state.
2. [HYBRID] Verify live status, destination, context, anchor, redirects, and whether loss is real or provider noise.
3. [AI] Classify positive acquisition, natural loss, recoverable loss, changed destination, spam/noise, or reputational issue.
4. [HYBRID] Create Opportunities only when recovery/correction has plausible value; avoid reacting to every low-value lost link.
5. [HYBRID] Update asset/competitor/authority state and attribution to prior outreach or PR actions.
6. [HYBRID] Escalate suspicious sitewide patterns or policy/security concerns to Incident handling.


