---
id: marketing.assets.sales-enablement
type: workflow
owner_system: marketing-synthesis
artifact_role: customer_facing_production_root
reads:
- Opportunity
- type: Insight
  owner_system: customer-intelligence
- type: Insight
  owner_system: competitor-intelligence
- Asset
- WorkRequest
writes:
- Asset
context:
- AudienceSegment
- Brand
- Offer
---
# Sales Enablement Asset

## Purpose
Create persuasive evidence/tools that help sellers and buyers resolve real decision questions consistently.

## Business Outcome
Increase the likelihood of the desired commercial action through an evidence-backed sales enablement asset that matches audience awareness, Offer, proof, and acquisition context.

## Run When
Use when a sales-enablement asset can resolve a recurring material buying/sales question. An Opportunity or real durable WorkRequest may provide context but is not required.

## Process
1. [AI] Identify sales-stage decision, recurring objection/question, buying roles, competitor context, and evidence gap from Customer/Sales evidence.
2. [AI] Choose asset: one-pager, battlecard, ROI model, case library, proof sheet, comparison, implementation guide, objection guide, deck section, or email template.
3. [HYBRID] Separate verified competitor/customer facts from suggested seller language and prohibit unsupported competitive claims.
4. [AI] Design for fast retrieval/use during actual sales workflow, including when not to use the asset.
5. [DETERMINISTIC] Version proof/pricing/terms dependencies so stale assets can be detected.
6. [HYBRID] Use relevant Content operating knowledge and the active harness's real visual/document capabilities directly for final production, and evaluate usage/outcome when useful data exists. Persist a WorkRequest only for a real durable organizational handoff.
