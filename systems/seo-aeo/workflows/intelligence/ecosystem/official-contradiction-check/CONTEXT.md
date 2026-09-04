---
id: seo.intelligence.ecosystem.official-contradiction-check
type: workflow
owner_system: seo-aeo
reads:
- type: Insight
  domain: seo-aeo
- Learning
- SourceRecord
- Observation
writes:
- Learning
- Observation
- Incident
evidence_inputs:
- Core policy
- business policy constraints
---
# SEO Official Policy / Guidance Contradiction Check

## Purpose
Check proposed SEO/AEO tactics against current authoritative platform rules and technical eligibility requirements while keeping policy status distinct from evidence strength.

## Business Outcome
Keep SEO/AEO strategy compatible with actually applicable external/business constraints without turning AURA into a permission runtime or importing another organization's private Learning.

## Run When
Use when current authoritative policy/guidance could materially change whether or how an SEO/AEO tactic should be used, or when relevant official guidance has changed.

## Do Not Run When
Do not treat a publication, practitioner opinion, competitor behavior, or one business result as authoritative policy. Do not use another organization's private AURA state as policy/evidence for the active organization.

## Process
1. [INTEGRATION] Identify the relevant platform/surface and retrieve current authoritative documentation or policy using the active harness's available tools.
2. [AI] Compare the actual proposed implementation—not merely its label—to documented prohibited, restricted, eligibility, quality, or technical requirements.
3. [AI] Describe the policy status in the language the evidence supports, for example allowed, restricted/conditional, externally approval-dependent, prohibited, unclear, or outdated-policy mismatch. Do not convert AURA's own uncertainty into an invented permission class.
4. [AI] Preserve the distinction between an official statement that an outcome is uncertain/unsupported and an actual prohibition or eligibility condition.
5. [AI] When interpretation is materially ambiguous or high-consequence, surface the ambiguity to the appropriate real human/legal/compliance/business owner rather than having AURA manufacture authority. Clearly prohibited or deceptive implementations should be identified as such from the applicable source/constraint.
6. [HYBRID] Preserve the exact SourceRecord/version/date supporting material policy conclusions. If future rechecking matters, preserve the reason/date/condition worth revisiting; the harness/runtime owns any actual schedule or notification.

## Related operating knowledge
- Allowed/conditional tactics may benefit from evidence assessment or experiment design.
- Contradicted/obsolete tactics may warrant organization-owned Learning changes when evidence supports them.
- A material live operational violation may warrant an Incident only when the Incident meaning genuinely fits.

These are model/user choices based on the situation, not deterministic runtime routes.

## Verification
- Material policy conclusions are traceable to current authoritative evidence.
- Evidence strength, material uncertainty, official-policy status, applicability, and practical consequence remain distinct.
- No private state from another organization is implicitly consumed.
- A later external state mutation is performed through the active model/harness when actually requested and capable; optional ChangeEvent/VerificationRecord state is memory, not permission.

## Measurement
- Strategy claims strengthen only through relevant observations, experiments, OutcomeEvaluations, replication, or authoritative evidence—not popularity or confidence language alone.

## Learning
- Keep SEO-specific operating knowledge as organization-owned SEO Domain Learning; use Business Learning only for genuinely organization-wide guidance. Cross-organization reuse requires explicit sharing/adoption or deliberate AURA product-development work.

## Failure / Fallback
- If an authoritative source cannot be retrieved automatically, use another appropriate source or preserve the unresolved evidence need honestly.
- If policy evidence remains contradictory or unclear, preserve the uncertainty rather than forcing a permissive/prohibitive conclusion.

## Completion Criteria
- Material policy conclusions are current, traceable, organization-isolated, and no tactic is treated as permissible/prohibited for a reason that cannot be traced to an actually applicable constraint.
