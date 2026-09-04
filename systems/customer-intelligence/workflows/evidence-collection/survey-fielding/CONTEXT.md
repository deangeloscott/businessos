---
id: customer.evidence-collection.survey-fielding
type: workflow
owner_system: customer-intelligence
reads:
- Asset
writes:
- SourceRecord
- Observation
context:
- AudienceSegment
- Objective
---
# Customer Survey Fielding

## Purpose
Launch and monitor a customer survey while protecting sample quality and response integrity.

## Business Outcome
Produce interpretable survey evidence with documented response coverage and limitations.

## Run When
Run after a finalized survey instrument and sample plan are ready and the actual organization/channel constraints for contacting participants are satisfied.

## Process
1. [DETERMINISTIC] Verify instrument version, audience/sample, consent language, routing, tracking, and collection window before launch.
2. [INTEGRATION] Distribute through the intended channels while respecting real consent, suppression, platform, account, legal, and organizational constraints; do not repeatedly contact suppressed or ineligible people.
3. [DETERMINISTIC] Monitor starts, completions, drop-off, duplicate/invalid responses, segment coverage, and channel mix.
4. [AI] Detect signs of systematic nonresponse or confusing questions and determine whether corrective action is warranted.
5. [HYBRID] Do not change material questions mid-field without versioning and documenting comparability effects.
6. [DETERMINISTIC] Close collection according to stopping/coverage rules and preserve instrument/sample metadata.
7. [AI] Publish SourceRecords/Observations with response limitations before substantive interpretation.
