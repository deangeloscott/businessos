---
id: core.intelligence.request-refresh
type: playbook
version: 1.1.0
owner_system: core
risk: low
autonomy_ceiling: 4
reads:
- Insight
- SourceRecord
- WorkRequest
writes:
- WorkRequest
capabilities:
  required:
  - none
  optional:
  - none
events:
  consumes:
  - none
  emits:
  - intelligence.refresh.requested
---
# Request Intelligence Refresh

## Purpose
Ask the canonical semantic owner to refresh stale, incomplete, contradictory, or insufficiently specific intelligence instead of building a duplicate research store.

## Business Outcome
Get fresher or more specific owner-domain intelligence without creating a competing research store in the requesting system.
## Run When
When a consumer needs owner-domain intelligence that exists but is not decision-sufficient.

## Process
1. [AI] State the exact decision that depends on the intelligence and why current material is insufficient.
2. [DETERMINISTIC] Check whether a refresh WorkRequest for the same scope is already active.
3. [AI] Specify subject, scope, freshness need, required evidence/precision, deadline/urgency, and what would count as sufficient answer.
4. [DETERMINISTIC] Route the request to the canonical owner system using the ownership registry.
5. [HYBRID] If urgency prevents waiting, authorize bounded provisional research by the consumer while marking non-owner interpretations provisional.
6. [DETERMINISTIC] Persist WorkRequest and emit intelligence.refresh.requested.
