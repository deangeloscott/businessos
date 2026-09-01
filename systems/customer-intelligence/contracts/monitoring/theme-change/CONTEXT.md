---
id: customer.monitoring.theme-change
type: playbook
owner_system: customer-intelligence
reads:
- Observation
- Insight
- SourceRecord
writes:
- Insight
- Observation
capabilities:
  required:
  - none
  optional:
  - customer_feedback.read
  - crm.opportunity.read
  - support.ticket.read
  - review.read
  - community.read
---
# Customer Theme Change Review

## Purpose
Review whether customer concerns, language, criteria, expectations, or use-context have materially changed without overreacting to noise or source-mix artifacts.

## Business Outcome
Keep customer understanding current enough that important decisions use present evidence rather than stale assumptions, without creating an AURA notification/event layer.

## Run When
Use when a current decision or saved monitoring intent makes it useful to compare recent customer evidence with prior evidence, especially when existing Customer Insights may be stale, broad, contradictory, or insufficiently supported. Any recurring execution is owned by the active harness/runtime.

## Process
1. [HYBRID] Define the comparison scope and evidence windows relevant to the current decision, then retrieve/reuse the strongest available customer evidence for those periods. The model/user decides the semantic scope; deterministic code may handle dates, counts, and exact source coverage once defined.
2. [AI] Compare theme prevalence, intensity, language, segment/market mix, new or disappearing themes, and decision criteria against current Customer Insights.
3. [HYBRID] Separate plausible real customer change from seasonality, source-mix changes, campaign effects, collection-method changes, sample differences, or other confounders.
4. [AI] Judge whether existing Insights should remain unchanged, be strengthened/weakened, narrowed/broadened, contradicted, superseded, or whether no durable conclusion is yet justified.
5. [AI] State what changed, why it matters to the current decision, confidence, affected scope, and what remains uncertain. If another business method becomes useful, the capable model may use it directly; this review does not notify or route other AURA systems.
6. [HYBRID] Persist only material Observations/Insight updates that future work would benefit from, preserving prior evidence/lineage as appropriate. Do not emit runtime events because an Insight changed.
7. [AI] When future comparison matters, preserve semantic review intent or the condition/date worth revisiting. The active harness/runtime owns any actual recurring check or notification.

## Verification
- Apparent theme changes account for material source/sample/method differences.
- Direct customer evidence remains distinguishable from inferred motivation or business implication.
- Insight updates preserve enough evidence/lineage to understand why the interpretation changed.
- No event, WorkRequest, or notification is manufactured merely because a customer theme changed.

## Completion Criteria
- The organization has an evidence-calibrated understanding of whether material customer themes changed and which durable Customer Insights, if any, should change with them.
