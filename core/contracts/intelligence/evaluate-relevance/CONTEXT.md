---
id: core.intelligence.evaluate-relevance
type: playbook
version: 1.1.0
owner_system: core
risk: low
autonomy_ceiling: 4
reads:
- Insight
- Opportunity
writes:
- Observation
- WorkRequest
- Opportunity
capabilities:
  required:
  - none
  optional:
  - none
events:
  consumes:
  - none
  emits:
  - intelligence.relevance.evaluated
context:
- AudienceSegment
- Market
- Objective
- Offer
---
# Evaluate Cross-System Relevance

## Purpose
Determine whether a newly published Insight materially intersects a specialized system without launching expensive work by default.

## Business Outcome
Route shared intelligence only where it can materially improve a domain decision, while avoiding irrelevant fan-out and duplicated research.
## Run When
When a system receives a new/updated/contradicted Insight event or deliberately evaluates foreign-domain intelligence.

## Process
1. [DETERMINISTIC] Apply cheap filters first: business, market, audience, offer, topic/entity, active objective, and status/freshness.
2. [AI] If plausibly relevant, identify the receiving domain mechanism that could make the Insight matter.
3. [AI] Determine whether existing domain evidence/Opportunity already incorporates the information.
4. [HYBRID] Choose exactly one response: ignore, watch, research further, attach as evidence, update existing Opportunity, create candidate Opportunity, or escalate Incident.
5. [HYBRID] Require stronger evidence/value before starting expensive research or action than for watch/attach decisions.
6. [DETERMINISTIC] Persist any relationship/request/Opportunity and emit only the necessary next event.
