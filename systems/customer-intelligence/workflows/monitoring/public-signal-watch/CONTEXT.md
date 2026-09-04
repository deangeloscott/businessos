---
id: customer.monitoring.public-signal-watch
type: workflow
owner_system: customer-intelligence
reads:
- Observation
- Insight
- SourceRecord
writes:
- SourceRecord
- Observation
- Insight
context:
- AudienceSegment
- ProductService
- Offer
- Market
---
# Public Customer Signal Watch

## Purpose
Review new public customer questions, praise, complaints, needs, and experience for meaningful changes without making AURA the monitoring runtime or treating every mention as important.

## Business Outcome
Keep customer understanding current enough to notice emerging opportunities or risks while avoiding duplicate evidence, alert noise, and cross-domain dispatch machinery.

## Run When
Use for a bounded public-signal review when the user requests it or saved monitoring intent indicates another check would be useful. Any recurring execution is owned by the active harness/runtime.

## Process
1. [HYBRID] Resolve the relevant themes/products/markets, current Customer Insights, prior checkpoint, and unresolved questions. The model/user decides what is relevant; AURA may persist the resulting monitoring intent.
2. [INTEGRATION] Retrieve new material from appropriate public/authorized sources with the active harness. Do not access private spaces or personal information beyond the user's actual authorization and legitimate task scope.
3. [DETERMINISTIC] Deduplicate mechanically identical/reposted material and compare exact checkpoints so old conversation is not repeatedly treated as new evidence.
4. [AI] Extract meaningful new questions, pains, sentiment shifts, use cases, before/after evidence, objections, feature needs, and changing language while keeping direct statements separate from inferred motivation.
5. [AI] Decide whether the new evidence merely adds examples, materially strengthens/weakens an Insight, supports a new Customer Insight, suggests useful work, or warrants no durable change.
6. [AI] Surface potentially useful proof/content/business implications as ordinary findings or recommendations. Other domain operating knowledge may be used when relevant, but this watch does not route signals through an AURA dispatcher.
7. [DETERMINISTIC] Persist only material SourceRecords/Observations/Insights selected by the model/user and update the relevant checkpoint. Do not emit runtime events merely because a public signal was observed.

## Verification
- Direct public evidence remains distinct from interpretation and active-customer applicability.
- Reposts/duplicate evidence do not inflate apparent prevalence.
- Saved cadence/checkpoint intent never claims a recurring task exists; the external runtime owns any scheduling.
- No cross-domain WorkRequest/event is manufactured merely because a signal might matter elsewhere.
