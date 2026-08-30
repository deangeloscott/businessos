---
id: marketing.assets.landing-page
type: playbook
version: 1.5.0
owner_system: marketing-synthesis
artifact_role: customer_facing_production_root
risk: medium
autonomy_ceiling: 3
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
- ActionPacket
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
Design a landing-page persuasion structure that continues acquisition intent and moves the right visitor toward the desired action.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed landing page persuasion that matches audience awareness, offer, proof, and acquisition context.

## Run When
Run when an Opportunity or WorkRequest requires landing-page or homepage persuasion to remove a commercial persuasion gap or create the required conversion asset. This is the required Run root for a standalone customer-facing landing-page/homepage draft, including local unpublished drafts.

## Process
1. [AI] Reconstruct visitor source/intent, audience awareness, Offer, desired action, objections, proof, and current friction.
2. [AI] Define page promise/message match and hierarchy from first screen through decision: outcome → problem/context → mechanism/value → proof → objections/risk → offer/CTA.
3. [HYBRID] Determine necessary depth and sections from buyer questions rather than template length.
4. [AI] Specify copy, proof placement, CTA behavior, comparison/FAQ, and information needed for qualification.
5. [HYBRID] Separate persuasion issues from form/checkout/technical journey friction and route those to Customer Optimization.
6. [HYBRID] Verify claims/terms/tracking requirements and delegate design/media production to Content where needed. Preserve explicit reusable promises/constraints as `BusinessClaim`; keep derived Offer/Audience/Brand strategy labeled derived/candidate rather than `explicit_user`.
7. [DETERMINISTIC] After drafting, run `python3 scripts/build_claim_manifest.py <business-id> <asset-file>`, classify every returned candidate in the Asset `extensions.businessos.claim_manifest`, and resolve unsupported promise expansion before completion.
8. [DETERMINISTIC] Treat draft/publication state separately from intended audience. A local homepage/landing-page draft is still customer-facing and may not opt out of production governance merely because it is not yet published.
9. [HYBRID] Record version-specific production readiness separately from draft status and QA in the Asset `extensions.businessos.production_readiness`. Preserve unresolved business facts, missing authorization/capabilities, deployment not performed, and measurement pending rather than converting them into invented copy or a global “no blockers” claim. A truthful draft may pass current-version QA while readiness remains blocked.
10. [DETERMINISTIC] Execute every declared required subcontract. Record each completion with `scripts/record_contract_completion.py`; `marketing.landing-page.qa` must produce a JSON pass record. Use the ordinary `scripts/finalize_run.py` path before reporting the landing-page workflow complete (`scripts/complete_run.py` remains the lower-level interface), but do not describe Run completion as launch/deployment/outcome completion.

## Decision Rules
- Preserve the visitor's acquisition promise unless evidence supports intentionally reframing it.
- Include a section only if it resolves a material question, objection, proof need, qualification need, or decision step for this audience.
- If the page is persuasive but the conversion mechanism is broken or burdensome, keep the diagnosis with Customer Optimization rather than rewriting copy indefinitely.
- Define the primary conversion and any qualification/guardrail metric before deployment.

## Completion Evidence
A saved landing-page Asset that references this Run is not complete merely because copy exists or `validate_business.py` is schema-clean. Required subcontract evidence, including the QA pass record, must be recorded in the Run contract-execution manifest.

The completed result may still be a governed draft. The final readiness assessment must state whether that exact version is `not_assessed`, `blocked`, `ready`, or `not_applicable`, with deployment and measurement reported separately.
