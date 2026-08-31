---
id: seo.intelligence.ecosystem.official-contradiction-check
type: playbook
version: 1.1.0
owner_system: seo-aeo
reads:
- type: Insight
  owner_system: seo-aeo
- Learning
- SourceRecord
- Observation
writes:
- Learning
- Observation
- Incident
capabilities:
  required:
  - research.web.read
  optional:
  - document.read
evidence_inputs:
- Core policy
- business policy constraints
---
# SEO Official Policy / Guidance Contradiction Check

## Purpose
Check proposed SEO/AEO tactics against current authoritative platform rules, technical eligibility requirements, and Core/business policy while keeping policy status distinct from evidence strength.

## Business Outcome
Keep SEO/AEO strategy current, evidence-governed, policy-safe, and connected to measurable organic and business outcomes without creating a parallel strategy-evidence store.

## Run When
Run before promoting or executing a materially risky tactic and whenever relevant official policy/guidance changes.

## Do Not Run When
Do not treat a publication, practitioner opinion, competitor behavior, or one business result as a validated tactic by itself. Do not use private cross-business evidence unless Core System Learning governance explicitly permits it.

## Process
1. [INTEGRATION] Identify the platforms/surfaces targeted and retrieve the current authoritative documentation or policy from the source map.
2. [HYBRID] Compare the actual proposed implementation—not merely its marketing label—to documented prohibited, spam, eligibility, quality, or technical requirements.
3. [AI] Classify policy status independently as allowed, restricted, approval_required, prohibited, unclear, or outdated-policy mismatch.
4. [HYBRID] Preserve the distinction between an official statement that an outcome is uncertain/unsupported and an actual prohibition.
5. [HUMAN] Escalate ambiguous high-impact policy interpretations; block deceptive or prohibited implementations under Core/business policy regardless of evidence that they might produce short-term results.
6. [DETERMINISTIC] Attach the exact SourceRecord/version/date supporting the policy assessment and schedule re-review when the source is likely to change.

## Decisions / Routing
- Allowed/restricted claims → evidence assessment / experiment design as appropriate.
- Prohibited claim → `seo.learning.tactic-deprecation` or Core policy enforcement.
- Operationally urgent violation → relevant Incident workflow.

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
