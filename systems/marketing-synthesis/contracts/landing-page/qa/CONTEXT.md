---
id: marketing.landing-page.qa
type: playbook
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
- Asset
capabilities:
  required:
  - none
  optional:
  - tracking.read
  - conversion.read
  - cms.page.publish
context:
- Brand
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Landing Page Persuasion QA

## Purpose
Verify the requested landing-page version preserves message match, evidence, Offer accuracy, persuasion flow, action integrity, and usable rendering.

## Business Outcome
Catch material conversion, truth, usability, or implementation defects before they hurt the intended audience or measurement.

## Run When
Use on a substantive landing-page/homepage draft or live implementation when end-to-end QA can materially improve readiness or identify defects.

## Process
1. [HYBRID] Inspect the actual available artifact/render at relevant breakpoints and compare it with the intended audience, acquisition context, message architecture, current Offer, and supporting evidence. If a final render is not available, QA only what actually exists and state that limitation.
2. [AI] Evaluate source-message match, opening clarity, section sequence, proof/objection placement, Offer/fit transparency, and CTA understanding.
3. [HYBRID] Check links, forms/CTA destinations, responsive visibility, prices/terms, proof assets, tracking, accessibility, and real legal/platform requirements where the available artifact/capabilities permit those checks.
4. [HYBRID] Apply the customer-facing claim policy to rendered text/images or an appropriate claim surface and confirm no design/edit enlarged unsupported promises or removed material qualifiers.
5. [AI] Distinguish persuasion defects from UX, form, checkout, technical, product, or other journey friction. Use relevant operating knowledge directly rather than routing issues to another AURA service.
6. [AI] Report material defects, lower-severity improvements, and the evidence/check behind each conclusion. A material defect may justify a recommendation not to launch that version, but AURA does not own launch authorization.
7. [HYBRID] If the user explicitly requests publication/deployment and the harness has real capability/permission, verify the live version and measurement instrumentation after the external change when practical. Otherwise do not imply deployment occurred.
8. [AI] Update/preserve the Asset's useful QA/readiness information when future work benefits from it. A separate Run-local pass file, contract-completion record, pre-edit snapshot, or generic VerificationRecord is not required merely to prove QA happened.

## Verification
- QA reflects the artifact/version actually inspected rather than an assumed final render.
- Material outward claims and Offer terms remain supported.
- Artifact quality/readiness, external deployment, and later business outcome remain separate facts.
- QA can recommend against release because of a real defect without acting as an AURA permission gate.

## Completion Criteria
- The inspected version has a clear evidence-backed QA result and actionable defects/improvements, with any untested surfaces or deployment state stated honestly. No Run is required.
