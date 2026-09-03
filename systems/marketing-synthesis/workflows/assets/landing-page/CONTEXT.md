---
id: marketing.assets.landing-page
type: workflow
owner_system: marketing-synthesis
reads:
- Opportunity
- type: Insight
  domain: customer-intelligence
- type: Insight
  domain: competitor-intelligence
- Asset
- WorkRequest
- ProofRecord
writes:
- Asset
context:
- AudienceSegment
- Brand
- Offer
---
# Landing Page Persuasion

## Purpose
Create a landing page or homepage that continues acquisition intent and moves the right visitor toward the desired action without overstating business truth.

## Business Outcome
Increase the likelihood of qualified conversion through an evidence-backed page matched to audience awareness, Offer, proof, acquisition context, and the real conversion experience.

## Run When
Use when the organization needs landing-page or homepage persuasion to remove a commercial persuasion gap or create/improve an outward conversion asset. An Opportunity, prior Asset, or real WorkRequest may provide context but is not required.

## Process
1. Reconstruct visitor source/intent, audience awareness, Offer, desired action, objections, proof, and current friction from the smallest useful organizational evidence.
2. Define page promise/message match and hierarchy from first screen through decision: outcome → problem/context → mechanism/value → proof → objections/risk → Offer/CTA, adapting the sequence to the actual buyer questions rather than treating it as a rigid template.
3. Determine necessary depth and sections from buyer questions rather than template length. Use relevant landing-page operating knowledge—such as message match, information architecture, copy, proof/objection handling, form/CTA design, or QA—only where it materially improves the requested result.
4. Draft the page copy and specify proof placement, CTA behavior, comparison/FAQ, qualification information, and useful design/media requirements.
5. Separate persuasion problems from form, checkout, technical, product, or other journey friction. Use the relevant operating knowledge or host capability directly instead of routing the problem to another AURA service.
6. Verify customer-facing claims and Offer terms against current organizational truth/evidence. Preserve explicit reusable promises/constraints as `BusinessClaim`; keep model-derived Offer/Audience/Brand strategy labeled as inference/candidate strategy unless the organization establishes it more strongly.
7. When deterministic claim checking is applicable, use the repository's claim-checking helper or another sound verification method to surface unsupported promise expansion. This protects outward truth; it does not require a Run or AURA execution ledger.
8. Keep artifact quality, publication state, and measured business outcome separate. A local unpublished page is still customer-facing for claim rigor, but being a draft does not imply deployment or outcome.
9. Preserve the finished/current-version `Asset` and only the additional durable evidence, decisions, readiness notes, changes, or measurements that future work materially benefits from. If publication is explicitly requested and the harness has the real capability/permission, publish through the host; otherwise return the usable artifact without manufacturing an authorization or handoff object.

## Proportionate Scope
Use only the research, page depth, proof, sections, design guidance, and QA needed to support the actual visitor decision and requested fidelity. Expand when the Offer or acquisition context is complex, high-stakes, or uncertain; do not add sections merely to satisfy a page template.

## Verification
- The page matches the acquisition promise and the real Offer/audience context.
- Material outward claims are supported, honestly provisional/general, or visibly placeholders rather than invented business facts.
- Copy, proof, CTA, structure, and conversion experience have been substantively reviewed; schema validity alone is not quality proof.
- Relevant Workflows are reusable operating knowledge, not required execution stages.
- Draft/publication, QA quality, external deployment, and business outcome remain separate facts.
- No Run, contract-execution manifest, WorkRequest, ChangeEvent, or VerificationRecord is required merely to create a valid landing-page Asset.

## Completion Criteria
- The requested page is a usable, evidence-bounded Asset at the appropriate fidelity for the user's request, with material limitations explicit. If this AURA Workflow is claimed as the method used, its substantive landing-page/claim-quality requirements must actually have been satisfied; a Run is still optional.
