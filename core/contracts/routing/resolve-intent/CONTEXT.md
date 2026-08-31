---
id: core.routing.resolve-intent
type: service
version: 1.1.0
owner_system: core
reads:
- Business
- Objective
- Opportunity
- SourceProfile
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
When the direct router is uncertain, the request expresses a broad goal/problem, asks AURA to durably follow/deeply understand a public or authorized subject, or one request may require several installed systems.

## Do Not Run When
Do not add semantic routing overhead when a high-confidence direct task already maps to one valid installed entry contract.

## Process
1. [DETERMINISTIC] Read the user request, installed modules, direct-router result/candidates, active business identity, existing relevant SourceProfiles, and any current Objective relevant to the request.
2. [AI] Identify the requested outcome and classify the intent as direct task, diagnosis/investigation, durable subject watch/refresh, broad goal/prioritization, multi-domain job, or information request; do not force ambiguity into an atomic contract.
3. [AI] Determine whether the request names a clear semantic owner/job, whether diagnosis must precede intervention, whether the user is asking for cumulative monitoring/research state rather than a one-time answer, and whether multiple independent domain responsibilities are present.
4. [HYBRID] Choose the smallest valid route: a high-confidence installed atomic/composite contract; `core.intelligence.subject-monitoring` when the user wants AURA to follow, keep current, or build cumulative cross-source understanding of a decision-relevant public/authorized subject; `core.diagnosis.business-problem` for broad unexplained symptoms; `core.opportunity.discover-next-best-work` for broad goals/prioritization; or `core.coordination.multi-domain-request` for genuinely cross-domain requested work. Do not route an ordinary one-time fact lookup into persistent monitoring unless durability actually adds value or the user asked for it.
5. [DETERMINISTIC] Verify the selected contract exists and its owner is installed. If the proper semantic owner is absent, return module-not-installed rather than letting another module impersonate it. When selecting shared subject monitoring, preserve the later domain handoff boundary rather than treating Core as the semantic owner of competitor/customer/industry/search/content conclusions.
6. [AI] Ask a clarifying question only when unresolved ambiguity would materially change the route and cannot be resolved from current business context or bounded research; never ask the user to name an internal BusinessOS module or contract.
7. [DETERMINISTIC] Pass the resolved entry contract to Process Planning and minimal Context Planning; preserve the route, confidence, candidate owner(s), and reason in bounded Run state when persistence is available.

## Verification
- The selected route exists, belongs to an installed owner, and matches the user's requested outcome/problem more closely than an arbitrary lexical fallback.
- Persistent subject monitoring is selected because the request benefits from durable source/subject state, not merely because it contains words such as “track” or “monitor.”

## Failure / Fallback
- If semantic reasoning is unavailable, present the small set of plausible installed routes with their business meanings and choose the safest broad Core entry rather than guessing an unrelated atomic job.

## Completion Criteria
- One valid next route (or an explicit module/scope gap) is selected without requiring the user to understand BusinessOS internals.
