---
id: core.intelligence.record-platform-change
type: service
owner_system: core
reads:
- Business
- SourceRecord
- PlatformChange
writes:
- PlatformChange
capabilities:
  required:
  - none
  optional:
  - none
context:
- Business
---
# Record Verified Platform Change

## Purpose
Maintain current verified platform/topic state independently from BusinessOS software releases.

## Business Outcome
Let BusinessOS workflows adapt to external platform changes without accumulating duplicate snapshots or letting unverified internet claims rewrite operating logic.

## Run When
When authoritative evidence establishes or re-verifies a material platform/API/standard/policy/feature state relevant to installed BusinessOS work.

## Process
1. [HYBRID] Verify the platform/topic state against suitable authoritative evidence and preserve SourceRecord/evidence refs.
2. [DETERMINISTIC] Derive/reuse a stable semantic key for the platform/topic; use `scripts/record_platform_change.py`.
3. [HYBRID] Compare the later authoritative evidence with the current semantic state. Different prose alone is not a material change. If the material state is unchanged, call `scripts/record_platform_change.py --reverify-current ...`; refresh the current object's verification time/count/refs and preserve the later observed wording/provenance in verification history. Do not create a new canonical object.
4. [HYBRID] If dates, scope, requirements, availability, behavior, or another decision-relevant part of the verified state materially changed, call the helper normally so it creates a new current `PlatformChange`, supersedes/links the prior current version, and preserves history.
5. [HYBRID] Keep platform facts separate from inferred/measured business impact. Route deeper relevance/materiality/impact analysis to Industry Intelligence when installed.
6. [HYBRID] If the resulting business work is material but cannot safely/autonomously proceed, route to `core.attention.manage`; otherwise execute through normal Opportunity/Action/Verification governance.
7. [DETERMINISTIC] Archive old superseded versions through lifecycle maintenance when eligible; normal workflows should retrieve only current state.

## Verification
One semantic platform/topic has at most one current version; unchanged rechecks do not multiply files; changed state preserves supersession lineage; external knowledge changes do not silently self-modify BusinessOS code.
