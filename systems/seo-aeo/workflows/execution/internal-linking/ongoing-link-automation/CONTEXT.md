---
id: seo.execution.internal-linking.ongoing-link-automation
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
writes:
- SEOAssetState
- ChangeEvent
- Asset
evidence_inputs:
- backlink/referring-domain/mention evidence and prospect records
---
# Ongoing Internal Link Automation

## Purpose
Continuously propose or execute high-confidence internal links as content changes, with controls against spam and duplication.

## Business Outcome
Improve valuable organic discovery through ongoing internal link automation, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Ongoing Internal Link Automation**, or when an authorized incident response requires it.

## Process
1. [HYBRID] On new/updated asset events, extract primary intent, entities, audience, and journey role.
2. [HYBRID] Search the asset graph for semantically and strategically relevant source/target relationships.
3. [DETERMINISTIC] Filter existing links, conflicting intent, low-value templates, restricted areas, and excessive repetition.
4. [HYBRID] Score candidates by user usefulness, business priority, topical relevance, graph value, and confidence.
5. [AI] Route by autonomy tier: recommend, prepare, or execute; cap changes per asset/run where uncertainty remains.
6. [DETERMINISTIC] Verify rendered links, record Change Events, and learn from accepted/rejected suggestions and performance.


