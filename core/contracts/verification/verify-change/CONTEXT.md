---
id: core.verification.verify-change
type: service
version: 2.0.0
owner_system: core
reads:
- ChangeEvent
- DecisionRecord
writes:
- VerificationRecord
- ChangeEvent
capabilities:
  required:
  - none
  optional:
  - none
events:
  consumes:
  - none
  emits:
  - core.object.updated
---
# Verify Material Change

## Purpose
Establish whether an important claimed post-state is actually true when independent verification is useful to the task, selected SOP, or consequence.

## Business Outcome
Prevent false success without making independent verification a universal prerequisite for all work.

## Run When
When a material ChangeEvent or task needs independent evidence of the resulting state.

## Do Not Run When
- Do not create VerificationRecord merely because a tool call occurred.
- Do not confuse implementation verification with measurement of the later business outcome.

## Process
1. [AI] Determine the material claim that needs verification from the ChangeEvent, task, decision, or selected SOP.
2. [HYBRID] Define the smallest observable post-state evidence that would establish, refute, or leave that claim inconclusive.
3. [INTEGRATION/HUMAN] Re-read or independently observe the relevant state through the best available host capability or credible human evidence.
4. [HYBRID] Compare expected and observed state, including unintended effects when material.
5. [HYBRID] Classify the result as passed, partial, failed, or inconclusive without inventing certainty.
6. [DETERMINISTIC] Persist a VerificationRecord when the result has future organizational value and update the related ChangeEvent when appropriate.

## Verification
- The VerificationRecord points to real evidence and the correct business/change.
- The verification method is sufficiently independent for the claim being made.

## Completion Criteria
- Future work can tell what was checked, what evidence was observed, and what conclusion is justified without requiring an ActionPacket or runtime transcript.
