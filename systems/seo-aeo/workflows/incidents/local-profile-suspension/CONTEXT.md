---
id: seo.incidents.local-profile-suspension
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- MetricObservation
- ChangeEvent
- Opportunity
- Observation
writes:
- Incident
evidence_inputs:
- location/profile data, local-result observations, and local competitors
---
# Local Profile Suspension Incident

## Purpose
Diagnose and resolve a material local-profile suspension or restriction while avoiding speculative changes that can worsen eligibility, identity, or reinstatement problems.

## Business Outcome
Restore legitimate local discovery and customer access as efficiently as practical while preserving the evidence, decisions, correspondence, root cause, and reusable context future work may need.

## Run When
Use when an important local business profile appears suspended, restricted, disabled, or otherwise unavailable and the issue is material enough to warrant focused incident-level attention.

## Process
1. [HYBRID] Confirm the affected profile/location, exact observed state, notice or reason if provided, recent relevant changes, and established business eligibility facts.
2. [AI] Identify which further profile edits or automated actions could plausibly interfere with diagnosis or reinstatement and recommend avoiding them when justified. The active user/harness controls actual operational behavior; AURA does not freeze automation or override other work.
3. [HYBRID] Compare name, address/service-area, categories, ownership, duplicates, website, and other implicated fields against real organization truth and current platform requirements.
4. [AI] Determine the strongest supported cause or unresolved possibilities. Avoid repeated speculative edits merely to see whether something changes.
5. [HYBRID] Correct factual or eligibility problems through the real authorized platform/account controls available and assemble appropriate verifiable evidence.
6. [HYBRID] Use the platform’s official reinstatement, verification, support, or appeal process when applicable and preserve material correspondence/status when future continuity benefits.
7. [HYBRID] After restoration or resolution, verify profile, site, citation, and identity consistency and preserve material root cause/prevention Learning when supported.

## Verification
- Location eligibility and public business facts are established before profile changes are recommended or made.
- Recommendations to pause edits and actions actually paused remain distinct.
- AURA does not create a separate incident-routing priority system, autonomy tier, or runtime freeze control.
- Incident state exists for durable organizational continuity, not because every profile issue needs an Incident object.
