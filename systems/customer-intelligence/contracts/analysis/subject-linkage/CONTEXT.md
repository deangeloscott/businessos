---
id: customer.analysis.subject-linkage
type: playbook
owner_system: customer-intelligence
reads:
- SourceRecord
- Observation
writes:
- Observation
capabilities:
  required:
  - none
  optional:
  - crm.contact.read
context:
- AudienceSegment
---
# Customer Subject Linkage

## Purpose
Link a public or first-party customer signal to an existing authorized CRM/customer record only when the identity match is sufficiently explicit and useful.

## Business Outcome
Preserve a coherent history of known customer experience across allowed sources without creating a shadow identity database or speculative personal profile.

## Run When
Run when a signal may belong to a known customer/contact and linking it would materially improve service, longitudinal customer understanding, or proof provenance.

## Process
1. [DETERMINISTIC] Confirm that identity linkage is permitted for the source, business purpose, jurisdiction/policy, and active business; reject linkage whose purpose is merely invasive profiling.
2. [INTEGRATION] Retrieve only the minimum authorized CRM/contact identifiers needed for matching; do not copy unrelated personal data into the Business OS.
3. [DETERMINISTIC] Prefer explicit identifiers supplied by the person or exact first-party mappings; do not treat similar names, usernames, photos, location, or inferred demographics as sufficient identity proof.
4. [HYBRID] Classify the match as confirmed, unresolved, or rejected with the evidence used; unresolved matches remain unlinked.
5. [DETERMINISTIC] Create a linkage Observation referencing the CRM/system-of-record subject identifier and original source/Observation rather than creating a new Person object.
6. [HYBRID] Do not infer sensitive traits, relationships, private interests, or cross-platform identities beyond the evidence needed for the authorized business purpose.
7. [DETERMINISTIC] Preserve confidence, provenance, and correction path so an incorrect linkage can be superseded without rewriting source history.
