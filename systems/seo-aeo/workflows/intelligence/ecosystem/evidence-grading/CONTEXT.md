---
id: seo.intelligence.ecosystem.evidence-grading
type: workflow
owner_system: seo-aeo
reads:
- type: Insight
  owner_system: seo-aeo
- Learning
- Observation
- SourceRecord
- OutcomeEvaluation
- Experiment
writes:
- Insight
- Learning
evidence_inputs:
- eligible s
updates:
  Insight:
  - updated evidence links confidence
---
# SEO Strategy Evidence Assessment

## Purpose
Assess the strength, relevance, confidence, applicability, and uncertainty of evidence supporting or contradicting an SEO/AEO strategy claim without collapsing those dimensions into one grade.

## Business Outcome
Keep SEO/AEO strategy current, evidence-backed, and connected to measurable organic/business outcomes without creating a parallel strategy store or importing private Learning from another organization.

## Run When
Use when a candidate SEO strategy claim is created or material new evidence could change its assessment.

## Do Not Run When
Do not treat a publication, practitioner opinion, competitor behavior, one business result, or model confidence as a validated tactic by itself. Do not read another organization's private AURA state as evidence for the active organization.

## Process
1. [HYBRID] Gather relevant official evidence, primary measurements, independent replications, active-organization evidence/Learning, experiments/outcomes, and credible counterevidence for the exact claim.
2. [AI] Assess source authority for the fact type, methodological quality, sample size/diversity, controls, recency, platform specificity, reproducibility, and whether the observed outcome is a business result or only a proxy.
3. [AI] Describe evidence strength at the resolution useful for the decision—for example direct/authoritative, strongly replicated, strong organization-specific evidence, credible emerging evidence, plausible hypothesis, speculative, or contradicted/obsolete. Keep policy prohibition/status separate from evidence strength.
4. [AI] Record applicability conditions and distinguish platform-documented behavior, external inference, public/general evidence, and active-organization evidence. Deterministic AURA validates references/provenance; the capable model judges semantic applicability.
5. [AI] Set conclusion confidence independently from evidence strength and preserve unresolved contradictions or causal ambiguity.
6. [HYBRID] Create/update the candidate Insight or organization-owned SEO Domain Learning at the narrowest justified maturity. Never promote a tactic merely because wording sounds confident or it is popular.

## Related operating knowledge
- Current authoritative policy/constraint evidence may be checked with `seo.intelligence.ecosystem.official-contradiction-check` when useful.
- Testable uncertain claims may use `seo.learning.strategy-experiment-design` when experimentation would materially improve the decision.
- Mature organization-owned tactic Learning may use `seo.learning.tactic-registry` to keep evidence/applicability coherent.
- If the organization wants to turn strong Learning into reusable process knowledge, `core.learning.workflow-evolution` is available. Cross-organization sharing uses explicit Innovation Exchange/export/adoption or deliberate AURA product-development work.

These are optional operating methods selected by the model/user, not runtime routes.

## Verification
- Source/Observation lineage remains inspectable.
- Evidence strength, conclusion confidence, policy status, applicability, and practical consequence remain distinct.
- No private state from another organization is implicitly consumed.
- Any later external mutation is performed by the active host when requested/capable; optional ChangeEvent/VerificationRecord state is memory, not permission.

## Measurement
- Strategy claims strengthen only through relevant observations, experiments, OutcomeEvaluations, replication, or authoritative evidence—not popularity or confidence language alone.

## Learning
- Keep SEO tactic knowledge as organization-owned SEO Domain Learning. Broader organization-wide guidance may become Business Learning when supported. Cross-organization reuse requires an explicit sharing/product-development boundary.

## Failure / Fallback
- If a source cannot be retrieved, use another valid source/method when practical or preserve the unresolved evidence need honestly.
- If evidence remains contradictory or insufficient, preserve uncertainty and keep the claim at the narrowest supported maturity.

## Completion Criteria
- SEO strategy evidence is calibrated, traceable, organization-isolated, and scoped to what the evidence actually supports.
