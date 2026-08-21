---
id: core.coordination.multi-domain-request
type: playbook
version: 1.0.0
owner_system: core
risk: low
autonomy_ceiling: 4
reads:
- Business
- Objective
- Insight
- Opportunity
- Asset
- WorkRequest
writes:
- WorkRequest
- Initiative
capabilities:
  required:
  - none
  optional:
  - none
events:
  consumes:
  - none
  emits:
  - core.work.requested
  - core.object.updated
context:
- Business
- Objective
subcontracts:
  conditional:
  - id: core.coordination.create-initiative
    when: Multiple independently owned Opportunities require shared sequencing or combined outcome management.
---
# Coordinate Multi-Domain Request

## Purpose
Decompose one user request that intentionally spans several business responsibilities into correctly owned, sequenced work without duplicating intelligence or Opportunities.

## Business Outcome
Make compound requests feel like one coherent job to the user while preserving semantic ownership, reuse, lineage, and efficient context inside BusinessOS.

## Run When
When fulfilling the requested result inherently requires two or more distinct installed domain responsibilities, such as research → content → campaign work.

## Do Not Run When
Do not create cross-domain coordination for one atomic job plus delegated production; use a WorkRequest for simple delegation instead.

## Process
1. [AI] Define the user's final outcome and decompose it into the smallest meaningful domain-owned results; distinguish independent business Opportunities from production/execution delegated in service of another Opportunity.
2. [DETERMINISTIC] Resolve installed semantic owners and valid entry contracts for each result. Mark requested responsibilities owned by omitted modules as explicit scope gaps rather than silently reassigning them.
3. [HYBRID] Reuse current canonical Business Context, evidence, Insights, Opportunities, Proof, Assets, and prior work before requesting new research or generation.
4. [AI] Build the dependency order and handoff conditions: what must be learned/decided first, what can run independently, and what downstream work requires upstream evidence or approval.
5. [HYBRID] Create bounded WorkRequests to the proper owners with only the required inputs, expected output, lineage, acceptance criteria, and return route; each atomic job receives its own minimal Context Plan and capability preflight.
6. [HYBRID] Evaluate returned work against the parent outcome, resolve contradictions or missing dependencies, and request only the smallest necessary correction/refresh rather than restarting the whole chain.
7. [HYBRID] When several independently valid Opportunities need shared sequencing/resources/outcome evaluation, invoke `core.coordination.create-initiative`; otherwise preserve delegation under the originating Opportunity.
8. [AI] Return one coherent user-facing result that explains what was completed, what remains blocked/awaiting approval, and which evidence/Opportunity caused each material downstream action.

## Verification
- Each domain result has one canonical owner; fan-out and delegation are not conflated; cross-system lineage remains inspectable.

## Failure / Fallback
- If a required module is absent, complete only the portions legitimately owned by installed modules and surface the missing-owner boundary plus any safe manual/bounded evidence fallback.

## Completion Criteria
- The compound request is represented as an ordered set of correctly owned jobs and handoffs with no duplicate semantic state.
