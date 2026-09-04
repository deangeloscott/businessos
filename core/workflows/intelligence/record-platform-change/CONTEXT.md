---
id: core.intelligence.record-platform-change
type: workflow
owner_system: core
reads:
- Business
- SourceRecord
- PlatformChange
writes:
- PlatformChange
context:
- Business
---
# Record Verified Platform Change

## Purpose
Maintain a current, evidence-backed record of an external platform/topic state that future organizational work may need, independently from AURA software releases or runtime routing.

## Business Outcome
Let future work reuse verified external platform knowledge without accumulating duplicate snapshots or allowing unverified claims to rewrite operating guidance.

## Run When
When authoritative or otherwise sufficiently credible evidence establishes, changes, or re-verifies a platform/API/standard/policy/feature state that has durable organizational value.

## Process
1. [HYBRID] Verify the platform/topic state against evidence appropriate to the fact being claimed and preserve SourceRecord/evidence refs.
2. [AI] Define the real-world platform/topic identity at the narrowest stable level useful for future work. The persistence helper may mechanically slug/hash those model/user-supplied identifiers; it does not decide semantic identity.
3. [AI] Compare later evidence with the current material state. Different wording alone is not a change. If the real state is materially equivalent, call `scripts/record_platform_change.py --reverify-current ...` so later evidence/provenance can be preserved without multiplying current objects.
4. [AI] If dates, scope, requirements, availability, behavior, or another decision-relevant aspect materially changed, call the helper normally so the new current PlatformChange supersedes the prior version and preserves useful history.
5. [AI] Keep the verified external platform fact separate from inferred or measured impact on this organization. Use whatever domain operating knowledge or business analysis is actually relevant; AURA does not automatically route the PlatformChange to another system or next action.
6. [HYBRID] Surface an AttentionItem only when the changed state creates a material unresolved condition worth future organizational awareness. Otherwise simply retain the verified state for reuse.
7. [DETERMINISTIC] Lifecycle maintenance may archive eligible superseded historical versions after current references remain valid; this is storage hygiene, not a runtime event lifecycle.

## Verification
- One model/user-defined platform/topic identity has at most one current version.
- Unchanged rechecks do not multiply current objects, and material changes preserve supersession lineage.
- Semantic equivalence/material change decisions are evidence-backed model/user judgments rather than deterministic string comparison.
- External knowledge changes do not silently self-modify AURA code or create mandatory downstream work.

## Completion Criteria
- Future work can retrieve the best current verified platform/topic state, its evidence, verification history, and material prior state when useful without relying on routing, Action, or event machinery.
