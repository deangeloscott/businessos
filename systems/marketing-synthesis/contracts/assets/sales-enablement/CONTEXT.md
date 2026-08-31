---
id: marketing.assets.sales-enablement
type: playbook
version: 1.1.0
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
- WorkRequest
- Asset
capabilities:
  required:
  - none
  optional:
  - creative.text.generate
  - email.send
  - social.ad.publish
  - cms.page.publish
  - experiment.run
  - tracking.read
context:
- AudienceSegment
- Brand
- Offer
---
# Sales Enablement Asset

## Purpose
Create persuasive evidence/tools that help sellers and buyers resolve real decision questions consistently.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed sales enablement asset that matches audience awareness, offer, proof, and acquisition context.

## Run When
Run when an Opportunity or WorkRequest requires sales enablement asset to remove a commercial persuasion gap or create the required conversion asset.

## Process
1. [AI] Identify sales-stage decision, recurring objection/question, buying roles, competitor context, and evidence gap from Customer/Sales Insights.
2. [AI] Choose asset: one-pager, battlecard, ROI model, case library, proof sheet, comparison, implementation guide, objection guide, deck section, or email template.
3. [HYBRID] Separate verified competitor/customer facts from suggested seller language and prohibit unsupported competitive claims.
4. [AI] Design for fast retrieval/use during actual sales workflow, including when not to use the asset.
5. [DETERMINISTIC] Version proof/pricing/terms dependencies so stale assets can be detected.
6. [HYBRID] Route visual/document production to Content and measure usage/outcome where data permits.
