---
id: marketing.assets.sales-enablement
type: workflow
owner_system: marketing-synthesis
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
Create persuasive evidence and tools that help sellers and buyers resolve real decision questions consistently.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed sales enablement matched to the actual sales stage, buyer roles, Offer, proof, and competitive context.

## Run When
Use when a sales-enablement asset can resolve a recurring material buying or selling question. An Opportunity or real durable WorkRequest may provide context but is not required.

## Process
1. Identify the sales-stage decision, recurring objection/question, buying roles, competitor context, and evidence gap from Customer/Sales evidence.
2. Choose the smallest useful asset for that decision: one-pager, battlecard, ROI model, case library, proof sheet, comparison, implementation guide, objection guide, deck section, email template, or another suitable form.
3. Separate verified competitor/customer facts from suggested seller language and prohibit unsupported competitive claims.
4. Design for fast retrieval and use during the actual sales workflow, including when not to use the asset.
5. Version material proof, pricing, terms, and other freshness-sensitive dependencies so future users can detect when the asset needs review.
6. Use relevant Content operating knowledge and the active harness's real visual/document capabilities directly for final production, and evaluate usage/outcome when useful data exists. Persist a WorkRequest only for a real durable organizational handoff.

## Proportionate Scope
Build only the evidence, comparison depth, calculations, or presentation detail needed to resolve the recurring decision. Expand when the buying committee, economics, or competitive stakes justify it; avoid creating a large collateral library without a real use case.

## Verification
- Material claims and competitive statements remain supported and current enough for the decision.
- The asset has a specific job in the real sales workflow and states important limitations or non-use cases.
- Freshness-sensitive dependencies are visible enough to prevent stale material from masquerading as current truth.
