---
id: marketing.landing-page.qa
type: playbook
version: 1.4.0
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
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
  - tracking.read
  - conversion.read
  - marketing.performance.read
  - experiment.run
  - cms.page.publish
  - email.send
  - social.ad.publish
context:
- Brand
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Landing Page Persuasion QA

## Purpose
Verify the final rendered landing page preserves message match, evidence, Offer accuracy, persuasion flow, and action integrity.

## Business Outcome
Prevent conversion assets from becoming materially worse during design, CMS implementation, responsive changes, or tracking setup.

## Run When
Run before launch and after material landing-page changes.

## Process
1. [DETERMINISTIC] Load final rendered page on required breakpoints and compare with approved architecture/copy/Offer version.
2. [AI] Evaluate source-message match, opening clarity, section sequence, proof/objection placement, Offer/fit transparency, and CTA understanding.
3. [DETERMINISTIC] Check links, forms/CTA destinations, tracking, responsive visibility, prices/terms, proof assets, and required legal/compliance elements.
4. [HYBRID] Re-run claim validation on rendered text/images and confirm no design edit removed qualifiers or changed meaning.
5. [AI] Identify persuasion problems versus UX/technical friction and route Customer Optimization issues.
6. [DETERMINISTIC] Block launch on material errors; capture pass/fail and before-state baseline. Scope QA `blockers` to unresolved defects in the inspected artifact/version. Record unresolved launch facts, authorization, capabilities, deployment, and outcome state in the Asset production-readiness assessment rather than making QA pass/fail impersonate global launch readiness.
7. [DETERMINISTIC] After launch verify live page/version and measurement instrumentation.
8. [DETERMINISTIC] Save a JSON pass/fail record under the active Run (for example `runtime/runs/<business-id>/<run-id>/artifacts/landing-page-qa.json`) with `contract_id: "marketing.landing-page.qa"`, `status: "pass"|"fail"`, checks performed, unresolved artifact/QA blockers, and tested Asset/version. Record completion with `scripts/record_contract_completion.py`; do not substitute a generic claim grep for this integrated QA record or call an honest draft production-ready merely because its current-version QA passed.
