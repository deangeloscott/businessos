---
id: competitor.analysis.competitive-implications
type: workflow
owner_system: competitor-intelligence
reads:
- Competitor
- SourceRecord
- Observation
- Insight
writes:
- Observation
- Insight
context:
- Business
- Market
- AudienceSegment
- Offer
---
# Competitive Implication Analysis

## Purpose
Translate supported competitor changes, differences, strengths, and weaknesses into scoped implications for this business without turning Competitor Intelligence into a cross-domain router.

## Business Outcome
Make competitive evidence directly useful to business decisions while keeping observed facts, strategic inference, and any later intervention choice distinct.

## Run When
Use when a Competitor Insight could materially change a current business objective, offer, audience, customer decision, market position, or response hypothesis.

## Process
1. [AI] Resolve the relevant Competitor evidence/Insight and the specific business decision/context it could affect.
2. [AI] Identify plausible threat, opportunity, customer-expectation, differentiation, pricing/offer, content, search, journey, or other implications only where a real mechanism connects the evidence to this business.
3. [AI] Distinguish direct implication from speculative second-order effects and state the assumptions/unknowns that could change the conclusion.
4. [HYBRID] Reuse current Customer/Industry/SEO/other organizational evidence when it materially supports or contradicts the implication; do not create duplicate foreign-domain state merely to acknowledge relevance.
5. [AI] Assess timing, reversibility, decision value, and uncertainty from the observed competitive movement and actual business context rather than fear of competition.
6. [AI] Preserve the smallest useful scoped Insight/relationship that a future model can retrieve directly. If another domain-specific playbook would improve the current work, the active model/user may select it directly; no relevance signal, routing event, or delegated Opportunity is required.
7. [AI] When the conclusion depends on future evidence, preserve the unresolved question/date/monitoring intent only if future work materially benefits. The active harness/runtime owns any actual recurring check or notification.

## Verification
- Competitor fact, inferred strategy, business implication, and evidence of effectiveness remain distinct.
- Cross-domain evidence is reused without manufacturing duplicate Opportunities or routing state.
- Timing/monitoring intent is not represented as an active schedule.

## Completion Criteria
- The organization has a calibrated statement of what the competitor evidence may mean for this business, why, how certain it is, and what decision it could affect, ready for direct use by any capable model/domain method.
