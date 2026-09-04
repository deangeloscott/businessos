---
id: industry.analysis.event-evolution
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
- Business
- Market
- Objective
- ProductService
---
# Event Evolution Tracking

## Purpose
Maintain one coherent evolving event state as new facts, dates, interpretations, and impacts emerge.

## Business Outcome
Improve the business response to external change through timely, evidence-backed event evolution tracking.

## Run When
Use when a decision or monitoring signal requires current event evolution tracking and existing Industry Intelligence is missing, stale, or unresolved.

## Process
1. [HYBRID] Compare new observations with the current IndustryEvent claims/status/timeline. Exact dates/refs can be compared deterministically; whether evidence represents the same event or changes its meaning is model judgment. Timeline, update-diff, and follow-up methods may help when the event complexity warrants them; they are not required stages.
2. [AI] Classify new evidence as confirmation, clarification, contradiction, escalation, de-escalation, new phase, or unrelated event.
3. [HYBRID] Update current factual event summary/status without erasing historical states or contradictory evidence.
4. [AI] Reassess materiality, urgency, affected organizational areas, and active Insights when the event meaning changes. Keep those interpretations in Insights/decisions rather than turning them into routing/scoring fields on IndustryEvent.
5. [AI] Update or create durable Insight/Observation meaning only when the changed event materially affects future organizational understanding. Do not emit dependency/runtime events merely because related organizational records may need reconsideration.
6. [HYBRID] Close/archive only when decision relevance has ended and residual monitoring needs are explicit.

## Verification
- IndustryEvent history remains evidence-backed and prior states are not silently overwritten.
- Semantic event identity, phase, and business materiality remain model/user judgments.
- No runtime event bus, routed WorkRequest, or mandatory downstream lifecycle is created from an event update.
