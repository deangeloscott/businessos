---
id: industry.monitoring.social-discussion
type: workflow
owner_system: industry-intelligence
reads:
- IndustryEvent
- SourceRecord
- Observation
- Insight
writes:
- SourceRecord
- Observation
- IndustryEvent
context:
- Market
- ProductService
---
# Industry Social Discussion Monitoring

## Purpose
Review public industry/category discussion for meaningful emerging narratives, questions, risks, and developments while filtering memes, isolated virality, and repeated copies of the same story.

## Business Outcome
Give Industry Intelligence an early evidence surface for developments worth verifying without mistaking social attention for factual truth or making AURA the monitoring runtime.

## Run When
Use for a bounded public-discussion review when requested, when saved monitoring intent indicates another check would be useful, or when a current decision could be changed by emerging industry conversation. The active harness/runtime owns any recurrence.

## Process
1. [DETERMINISTIC] Load saved watch topics/markets, prior IndustryEvents, known narratives, checkpoints, and source references that are relevant to the current review.
2. [INTEGRATION] Retrieve relevant new public discussions/feed items since the useful checkpoint with source, timestamp, thread/context, and visible spread/engagement indicators where available.
3. [HYBRID] Collapse mechanically identical reposts/URLs deterministically, then use model judgment to distinguish syndication, copied claims, related conversation, and genuinely independent evidence.
4. [AI] Identify candidate developments, changing narratives, questions, concerns, claims, and emerging terminology while keeping observed discussion separate from factual truth.
5. [HYBRID] Cross-check material factual claims against stronger/primary sources before updating an IndustryEvent; unresolved social claims remain bounded Observations/hypotheses.
6. [AI] Judge whether a signal belongs to an existing real-world event, suggests a distinct event worth investigating, represents a durable narrative shift, or is merely conversation without material external meaning.
7. [HYBRID] Persist only useful SourceRecords/Observations and, when justified, update/create a durable IndustryEvent. Verification/materiality methods may be useful next if the model/user chooses them; this review does not automatically route work or create runtime events.

## Verification
- Social prevalence is not treated as factual or causal proof.
- Duplicate/repeated discussion is not counted as independent evidence.
- Event identity/materiality are model judgments supported by evidence.
- AURA may preserve monitoring intent/checkpoints but does not own scheduling or notification delivery.

## Completion Criteria
- The organization has the smallest useful evidence-backed view of emerging industry discussion, with material unknowns and any worthwhile next investigation clear without a monitoring daemon or routing lifecycle.
