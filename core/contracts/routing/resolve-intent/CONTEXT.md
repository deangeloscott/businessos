---
id: core.routing.resolve-intent
type: service
version: 1.0.0
owner_system: core
risk: low
autonomy_ceiling: 4
reads:
- Business
- Objective
- Opportunity
writes: []
capabilities:
  required:
  - none
  optional:
  - none
events:
  consumes:
  - none
  emits:
  - none
context:
- Business
- Objective
---
# Resolve User Intent

## Purpose
Interpret a natural-language business request when deterministic routing cannot identify a sufficiently confident direct job.

## Business Outcome
Let users ask for outcomes and problems in ordinary language without needing to know BusinessOS systems, contracts, or internal terminology.

## Run When
When the direct router is uncertain, the request expresses a broad goal/problem, or one request may require several installed systems.

## Do Not Run When
Do not add semantic routing overhead when a high-confidence direct task already maps to one valid installed entry contract.

## Process
1. [DETERMINISTIC] Read the user request, installed modules, direct-router result/candidates, active business identity, and any current Objective relevant to the request.
2. [AI] Identify the requested outcome and classify the intent as direct task, diagnosis/investigation, broad goal/prioritization, multi-domain job, or information request; do not force ambiguity into an atomic contract.
3. [AI] Determine whether the request names a clear semantic owner/job, whether diagnosis must precede intervention, and whether multiple independent domain responsibilities are present.
4. [HYBRID] Choose the smallest valid route: a high-confidence installed atomic/composite contract; `core.diagnosis.business-problem` for broad unexplained symptoms; `core.opportunity.discover-next-best-work` for broad goals/prioritization; or `core.coordination.multi-domain-request` for genuinely cross-domain requested work.
5. [DETERMINISTIC] Verify the selected contract exists and its owner is installed. If the proper semantic owner is absent, return module-not-installed rather than letting another module impersonate it.
6. [AI] Ask a clarifying question only when unresolved ambiguity would materially change the route and cannot be resolved from current business context or bounded research; never ask the user to name an internal BusinessOS module or contract.
7. [DETERMINISTIC] Pass the resolved entry contract to Process Planning and minimal Context Planning; preserve the route, confidence, candidate owner(s), and reason in bounded Run state when persistence is available.

## Verification
- The selected route exists, belongs to an installed owner, and matches the user's requested outcome/problem more closely than an arbitrary lexical fallback.

## Failure / Fallback
- If semantic reasoning is unavailable, present the small set of plausible installed routes with their business meanings and choose the safest broad Core entry rather than guessing an unrelated atomic job.

## Completion Criteria
- One valid next route (or an explicit module/scope gap) is selected without requiring the user to understand BusinessOS internals.
