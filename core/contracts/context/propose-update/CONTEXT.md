---
id: core.context.propose-update
type: playbook
version: 2.0.0
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
Represent credible evidence that materially changes or conflicts with durable Business Context without silently rewriting organizational truth.

## Business Outcome
Keep durable context current while preserving evidence, uncertainty, supersession, and real organizational decisions.

## Run When
When credible evidence suggests that a Business, Brand, Offer, Audience, Market, Objective, economics, or other durable context fact should change and the change is material enough to preserve explicitly.

## Process
1. [AI] Identify the exact context object/field, current value, proposed value, and why the distinction matters.
2. [HYBRID] Link the strongest available evidence and distinguish factual synchronization, inference, preference/instruction change, and a business decision.
3. [AI] Determine whether the evidence is strong enough to update factual state directly under the applicable truth/provenance rules or whether a proposal is useful because the matter remains uncertain or requires an actual organizational choice.
4. [DETERMINISTIC] Persist a ContextUpdateProposal only when preserving the unresolved proposed change has future value. Do not create one merely to force ordinary factual maintenance through ceremony.
5. [HYBRID] When a real organizational decision is made, persist it as a DecisionRecord when future work materially benefits from remembering it. AURA does not create a separate permission token.
6. [DETERMINISTIC] Apply the resulting context update through the supported canonical persistence path, preserving prior/current/superseded state and affected references where applicable.

## Verification
- Evidence/provenance supports the resulting truth classification.
- A real decision is represented as a DecisionRecord only when a decision actually occurred.
- No unsupported inference is promoted to established business fact.

## Completion Criteria
- The organization can distinguish the prior state, proposed/current state, evidence basis, unresolved uncertainty, and any real decision that materially explains the change.
