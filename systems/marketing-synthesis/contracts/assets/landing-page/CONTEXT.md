---
id: marketing.assets.landing-page
type: playbook
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
- ProofRecord
writes:
- Asset
capabilities:
  required:
  - none
  optional:
  - creative.text.generate
  - cms.page.publish
  - experiment.run
  - tracking.read
context:
- AudienceSegment
- Brand
- Offer
subcontracts:
  required:
  - marketing.intake.persuasion-brief
  - marketing.landing-page.message-match
  - marketing.landing-page.information-architecture
  - marketing.landing-page.copy
  - marketing.landing-page.proof-objections
  - marketing.landing-page.form-cta
  - marketing.landing-page.qa
---
# Landing Page Persuasion

## Purpose
Create a landing page or homepage that continues acquisition intent and moves the right visitor toward the desired action without overstating business truth.

## Business Outcome
Increase the likelihood of qualified conversion through an evidence-backed page matched to audience awareness, Offer, proof, acquisition context, and the real conversion experience.

## Run When
Use when the organization needs landing-page or homepage persuasion to remove a commercial persuasion gap or create/improve an outward conversion asset. An Opportunity, prior Asset, or real WorkRequest may provide context but is not required.

## Process
1. [AI] Reconstruct visitor source/intent, audience awareness, Offer, desired action, objections, proof, and current friction from the smallest useful organizational evidence.
2. [AI] Define page promise/message match and hierarchy from first screen through decision: outcome → problem/context → mechanism/value → proof → objections/risk → Offer/CTA.
3. [AI] Determine necessary depth and sections from buyer questions rather than template length; use the authored landing-page submethods as relevant quality/composition knowledge.
4. [AI] Draft the page copy and specify proof placement, CTA behavior, comparison/FAQ, qualification information, and useful design/media requirements.
5. [AI] Separate persuasion problems from form, checkout, technical, product, or other journey friction. Use the relevant operating knowledge or host capability directly instead of routing the problem to another AURA service.
6. [HYBRID] Verify customer-facing claims and Offer terms against current organizational truth/evidence. Preserve explicit reusable promises/constraints as `BusinessClaim`; keep model-derived Offer/Audience/Brand strategy labeled as inference/candidate strategy unless the organization establishes it more strongly.
7. [DETERMINISTIC] When deterministic claim checking is applicable, run `python3 scripts/build_claim_manifest.py <business-id> <asset-file>` (or an appropriate claim-surface sidecar for opaque media), classify the returned candidates, and resolve unsupported promise expansion. This protects outward truth; it does not require a Run or AURA execution ledger.
8. [HYBRID] Keep artifact quality, publication state, and measured business outcome separate. A local unpublished page is still customer-facing for claim rigor, but being a draft does not imply deployment or outcome.
9. [AI] Preserve the finished/current-version `Asset` and only the additional durable evidence, decisions, readiness notes, changes, or measurements that future work materially benefits from. If publication is explicitly requested and the harness has the real capability/permission, publish through the host; otherwise return the usable artifact without manufacturing an authorization or handoff object.

## Verification
- The page matches the acquisition promise and the real Offer/audience context.
- Material outward claims are supported, honestly provisional/general, or visibly placeholders rather than invented business facts.
- Copy, proof, CTA, structure, and conversion experience have been substantively reviewed; schema validity alone is not quality proof.
- Draft/publication, QA quality, external deployment, and business outcome remain separate facts.
- No Run, contract-execution manifest, WorkRequest, ChangeEvent, or VerificationRecord is required merely to create a valid landing-page Asset.

## Completion Criteria
- The requested page is a usable, evidence-bounded Asset at the appropriate fidelity for the user's request, with material limitations explicit. If this AURA playbook is claimed as the method used, its substantive landing-page/claim-quality requirements must actually have been satisfied; a Run is still optional.
