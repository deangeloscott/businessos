---
id: seo.intelligence.ecosystem.official-contradiction-check
type: playbook
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
Check proposed SEO/AEO tactics against current authoritative platform rules and technical eligibility requirements while keeping policy status distinct from evidence strength.

## Business Outcome
Keep SEO/AEO strategy current and compatible with actually applicable external/business constraints without turning AURA into a permission or policy-enforcement runtime.

## Run When
Use when current authoritative policy/guidance could materially change whether or how an SEO/AEO tactic should be used, or when relevant official guidance has changed.

## Do Not Run When
Do not treat a publication, practitioner opinion, competitor behavior, or one business result as authoritative policy. Do not use private cross-business evidence unless broader reuse is actually supported.

## Process
1. [INTEGRATION] Identify the relevant platform/surface and retrieve current authoritative documentation or policy using the active harness's available tools.
2. [HYBRID] Compare the actual proposed implementation—not merely its label—to documented prohibited, restricted, eligibility, quality, or technical requirements.
3. [AI] Describe the policy status in the language the evidence supports, for example allowed, restricted/conditional, externally approval-dependent, prohibited, unclear, or outdated-policy mismatch. Do not convert AURA's own uncertainty into an invented permission class.
4. [AI] Preserve the distinction between an official statement that an outcome is uncertain/unsupported and an actual prohibition or eligibility condition.
5. [AI] When interpretation is materially ambiguous or high-consequence, surface the ambiguity to the appropriate human/legal/compliance/business owner rather than having AURA manufacture authority. Clearly prohibited or deceptive implementations should be identified as such from the actual applicable source/constraint.
6. [HYBRID] Preserve the exact SourceRecord/version/date supporting material policy conclusions. If the source is likely to change and future work benefits from awareness, remember refresh/monitoring intent; the harness/runtime owns any actual schedule or notification.

## Related operating knowledge
- Allowed/conditional tactics may benefit from evidence assessment or experiment design.
- Contradicted/obsolete tactics may warrant Learning deprecation when evidence supports it.
- A material live operational violation may warrant an Incident only when the Incident semantics genuinely fit.

These are model/user choices based on the situation, not deterministic runtime routes.

## Verification
- Validate canonical objects written and preserve SourceRecord/Observation lineage.
- Keep evidence strength, conclusion confidence, official-policy status, and practical consequence distinct.
- A later external state mutation is performed through the active model/harness when actually requested and capable. `ChangeEvent`/`VerificationRecord` may preserve durable facts about a real change/check when useful; they are not permission prerequisites.

## Measurement
- Strategy claims become stronger only through relevant observations, experiments, OutcomeEvaluations, replication, or authoritative policy evidence; popularity and confidence language are not outcome evidence.

## Learning
- Maintain SEO-specific strategy knowledge as SEO Domain Learning. Propose broader Business or System Learning only when evidence and applicability justify the broader scope.

## Failure / Fallback
- If an authoritative source cannot be retrieved automatically, use another appropriate source or create a real human/owner handoff when needed. Do not invent the missing policy or create an AURA action object for a tool limitation.
- If policy evidence remains contradictory or unclear, preserve the uncertainty rather than forcing a permissive/prohibitive conclusion.

## Completion Criteria
- Material policy conclusions are traceable to current authoritative evidence.
- Uncertainty, evidence strength, applicability, and practical consequence remain distinct.
- No tactic is promoted, deprecated, blocked, or claimed permissible/prohibited for a reason that cannot be traced to evidence or an actually applicable constraint.
