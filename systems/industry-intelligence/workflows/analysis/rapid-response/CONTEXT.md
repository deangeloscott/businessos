---
id: industry.analysis.rapid-response
type: workflow
owner_system: industry-intelligence
reads:
- IndustryEvent
- Observation
- SourceRecord
- Insight
writes:
- IndustryEvent
- Observation
- Insight
context:
- AudienceSegment
- Business
- Market
- Objective
- Offer
- ProductService
---
# Rapid Response Intelligence

## Purpose
Produce the smallest verified, decision-useful understanding of a fast-moving external development when time and uncertainty matter.

## Business Outcome
Help the organization respond intelligently to external change without trading away evidence quality or creating an AURA notification/handoff control layer.

## Run When
Use when a developing external event could materially change a near-term business decision or communication and current Industry Intelligence is missing, stale, or unresolved.

## Process
1. [AI] Define the exact decision, what must be known now, what can remain uncertain, and how quickly the answer loses value.
2. [INTEGRATION] Retrieve the strongest available current primary/authoritative evidence first, preserving publication/event/retrieval time where it matters.
3. [AI] Separate confirmed facts, credible-but-unconfirmed reports, unknowns, interpretations, scenarios, and speculation.
4. [HYBRID] Draw on factual-summary and impact-pathway methods when they materially improve the answer, using them to determine business implications, timing, and relevant compliance/reputation sensitivity without claiming certainty beyond the evidence. Neither is a mandatory prerequisite or downstream stage.
5. [AI] Produce a concise reusable Insight with the decision-relevant facts, implications, evidence refs, uncertainty, and what would materially change the conclusion. Other domain methods may be useful immediately, but the active model/user chooses them directly.
6. [HYBRID] When important facts are still developing, preserve the unresolved question, future milestone/date, or monitoring intent that would justify another check. The active harness/runtime owns any actual reminder, recurring check, or notification.
7. [AI] When later authoritative evidence changes the real-world understanding, update/supersede the durable Event/Insight at the scope justified by that evidence; semantic change is not a deterministic string-diff transition.

## Verification
- Time pressure does not collapse confirmed facts and plausible reports into one truth state.
- Every material current claim is traceable to appropriately current evidence.
- Follow-up intent is not represented as an active schedule or notification.
- No WorkRequest, downstream notification, or routing packet is required for another capable model/domain method to use the result.

## Completion Criteria
- The organization has a compact current answer good enough for the time-sensitive decision, knows the material uncertainty, and can continue directly with whatever method/action is appropriate without an AURA handoff or Workflow-composition layer.
