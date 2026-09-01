---
id: seo.intelligence.ecosystem.evidence-grading
type: playbook
owner_system: seo-aeo
reads:
- type: Insight
  owner_system: seo-aeo
- Learning
- Observation
- SourceRecord
- OutcomeEvaluation
- Experiment
- type: Learning
  owner_scope: system
writes:
- Insight
- Learning
capabilities:
  required:
  - research.web.read
  optional:
  - document.read
  - search.observe
  - analytics.read
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
Keep SEO/AEO strategy current, evidence-governed, policy-safe, and connected to measurable organic and business outcomes without creating a parallel strategy-evidence store.

## Run When
Run when a candidate SEO strategy claim is created or material new evidence could change its assessment.

## Do Not Run When
Do not treat a publication, practitioner opinion, competitor behavior, or one business result as a validated tactic by itself. Do not use private cross-business evidence unless Core System Learning governance explicitly permits it.

## Process
1. [HYBRID] Gather direct official evidence, primary measurements, independent replications, active-business evidence, eligible System Learnings, and credible counterevidence relevant to the exact claim.
2. [AI] Assess source authority for the fact type, methodological quality, sample size/diversity, controls, recency, platform specificity, reproducibility, and whether the observed outcome is a business result or only a proxy.
3. [HYBRID] Assign an evidence-strength assessment such as direct/authoritative, strong replicated, strong business-specific, credible emerging, plausible hypothesis, speculative, or contradicted/obsolete; do not use policy prohibition as an evidence grade.
4. [DETERMINISTIC] Record applicability conditions and separate statements such as platform-documented behavior, industry inference, active-business evidence, and eligible cross-business generalization.
5. [HYBRID] Set conclusion confidence independently from evidence strength and record unresolved contradictions or causal ambiguity.
6. [HYBRID] Create/update the candidate Insight or SEO Domain Learning at the narrowest justified maturity; never promote to Standard solely because wording sounds confident or a tactic is popular.

## Decisions / Routing
- Route policy/risk classification → `seo.intelligence.ecosystem.official-contradiction-check`.
- Route testable uncertain claims → `seo.learning.strategy-experiment-design`.
- Route sufficiently mature domain learning → `seo.learning.tactic-registry`.

## Verification
- Validate every canonical object written, preserve SourceRecord/Observation lineage, and keep evidence strength, conclusion confidence, policy status, and risk as separate dimensions.
- Any later external state mutation must use an ActionPacket, ChangeEvent, and independent VerificationRecord.

## Measurement
- Strategy claims become stronger only through relevant observations, experiments, OutcomeEvaluations, replication, or authoritative policy evidence; popularity and confidence language are not outcome evidence.

## Learning
- Maintain SEO-specific strategy knowledge as SEO Domain Learning. Propose broader Business or System Learning only when evidence and applicability justify the broader scope.

## Failure / Fallback
- If a source cannot be retrieved automatically, create a manual evidence-retrieval Action or use another authoritative source; do not invent the missing evidence.
- If evidence remains contradictory or insufficient, preserve the uncertainty and keep the claim at hypothesis/experimental maturity instead of forcing a conclusion.

## Completion Criteria
- Outputs use current Core Observation/Insight/Experiment/Learning objects rather than legacy strategy-evidence object.
- Source provenance, contradictory evidence, applicability, confidence, risk, and policy status remain inspectable.
- No tactic is promoted, deprecated, or blocked for a reason that cannot be traced to evidence or policy.
