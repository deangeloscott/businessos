---
id: core.intelligence.ecosystem-radar
type: playbook
version: 1.0.0
owner_system: core
risk: low
autonomy_ceiling: 4
reads:
- Business
- Objective
- Market
- ProductService
- SourceProfile
- SourceRecord
- Observation
- Insight
- Learning
- Opportunity
writes:
- WorkRequest
- Observation
- Insight
- Opportunity
capabilities:
  required:
  - research.web.read
  optional:
  - news.read
  - regulatory.read
  - research.paper.read
  - document.read
  - search.observe
  - community.read
  - social.listen
  - social.observe
  - rss.read
  - creator_content.observe
schedule:
  class: recurring
  default: weekly
  configurable: true
subcontracts:
  required:
  - id: core.intelligence.ecosystem.source-discovery
  - id: core.intelligence.ecosystem.evidence-triangulation
  - id: core.intelligence.ecosystem.route-learning
---
# External Ecosystem Intelligence Radar

## Purpose
Run one governed external-learning cycle that discovers meaningful outside developments, verifies what the evidence actually supports, and routes only relevant findings to their canonical domain owners.

## Business Outcome
Keep BusinessOS current with useful external knowledge without chasing noise, duplicating domain intelligence, or allowing internet popularity to rewrite operating guidance.

## Run When
Run on the configured recurrence, on demand, after a material external change, or when stale external assumptions could affect an active business decision.

## Do Not Run When
Do not use this contract as an always-on daemon. The schedule is execution intent for a capable host/harness; without scheduling support, run the same workflow on demand.

## Process
1. [DETERMINISTIC] Load active Business Context, Objectives, installed systems, current domain Learnings/Insights, prior radar state, and SourceProfiles; reuse fresh owner-domain research instead of fetching the same evidence again.
2. [AI] Define the smallest decision-relevant discovery envelope for this cycle, including domain mechanisms that could change important business decisions and a bounded allowance for open discovery beyond known sources.
3. [HYBRID] Run `core.intelligence.ecosystem.source-discovery`; preserve inspected material as SourceRecords/Observations under the research-evidence policy and keep snippets/unvisited results as discovery leads only.
4. [HYBRID] Cluster semantically equivalent signals and claims, then run `core.intelligence.ecosystem.evidence-triangulation` for material candidates so original provenance, independence, contradictions, freshness, novelty, methodology, and uncertainty are explicit.
5. [AI] Resolve only the relevant installed semantic owner(s) and their ecosystem-radar/process-map entry when available; invoke those domain radars to interpret domain meaning and active-business applicability without hard-coupling Core to omitted editions or fanning every signal to every system.
6. [HYBRID] Run `core.intelligence.ecosystem.route-learning` to choose ignore, watch, investigate, test, adopt through existing governed learning/action paths, or block/deprecate as evidence and policy justify.
7. [DETERMINISTIC] Persist the resulting canonical references and WorkRequests/Opportunities, update source attention history only through `core.intelligence.ecosystem.maintain-source-profile`, and record what was checked so the next cycle can perform incremental discovery.
8. [AI] Return a compact prioritized radar: important verified changes, promising hypotheses worth testing, items to watch, invalidated/noisy claims, and the evidence/reason behind each disposition.

## Verification
- Every material conclusion has inspectable provenance and distinguishes independent evidence from echo/republication.
- Domain owners, not Core, determine domain-specific meaning and experimentation.
- A recurring run remains portable because BusinessOS declares cadence but does not implement the scheduler.

## Completion Criteria
- Material discoveries are either safely closed, watched, routed for more evidence, converted to a candidate Opportunity/experiment route, or linked to an existing Learning with no unowned important signal.
