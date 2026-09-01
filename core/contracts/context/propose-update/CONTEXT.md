---
id: core.context.propose-update
type: playbook
version: 2.1.0
owner_system: core
reads:
- Observation
- Insight
- Learning
- DecisionRecord
writes:
- ContextUpdateProposal
- DecisionRecord
capabilities:
  required:
  - none
  optional:
  - none
context:
- AudienceSegment
- Brand
- Business
- EconomicContext
- Market
- Objective
- Offer
- ProductService
---
# Propose Canonical Context Update

## Purpose
Preserve a credible but not-yet-resolved candidate change to durable organizational context without silently rewriting truth.

## Business Outcome
Keep context current while preserving evidence, uncertainty, prior state, and any real organizational decision that explains what ultimately changed.

## Run When
When credible evidence suggests that a Business, Brand, Offer, Audience, Market, Objective, economics, or other durable context fact may need to change and the unresolved distinction is important enough for future work to remember.

## Process
1. [AI] Identify the exact context object/field, current value, proposed value, and why the distinction matters.
2. [HYBRID] Link the strongest available evidence and distinguish factual synchronization, inference, preference/instruction change, and a real business decision.
3. [AI] Determine whether the evidence is strong enough to update factual state directly under the applicable truth/provenance rules. If so, update the canonical context without manufacturing a proposal.
4. [DETERMINISTIC] Persist a `ContextUpdateProposal` only when the unresolved candidate change itself has future organizational value. Its status describes the proposal's state (`proposed`, `applied`, `rejected`, `superseded`, or `withdrawn`); it is not a permission token.
5. [HYBRID] When a real organizational choice resolves the matter, persist a `DecisionRecord` only if future work materially benefits from remembering that decision, and link it through `decision_ref` when useful.
6. [DETERMINISTIC] Apply any resulting context update through the supported canonical persistence path, preserving prior/current/superseded state and affected references where applicable.

## Verification
- Evidence/provenance supports the resulting truth classification.
- A proposal remains distinct from established context until the underlying truth or organizational choice is actually resolved.
- A real decision is represented as a `DecisionRecord` only when a decision actually occurred.
- No unsupported inference is promoted to established business fact.

## Completion Criteria
- The organization can distinguish the prior state, candidate/current state, evidence basis, unresolved uncertainty, and any real decision that materially explains the resolution.
