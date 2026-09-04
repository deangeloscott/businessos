---
id: customer.analysis.win-loss
type: workflow
owner_system: customer-intelligence
reads:
- SourceRecord
- Observation
- Insight
writes:
- SourceRecord
- Observation
- Insight
context:
- AudienceSegment
- Market
- Objective
- Offer
- ProductService
---
# Win/Loss Analysis

## Purpose
Explain why qualified opportunities are won or lost using direct and behavioral evidence, not CRM reason codes alone.

## Business Outcome
Reduce uncertainty about customers through win/loss analysis, so future decisions reflect current customer evidence rather than assumption.

## Run When
Use when a decision requires current win/loss analysis and existing Customer Insights are missing, stale, too broad, or insufficiently supported.

## Process
1. [DETERMINISTIC] Define comparable won/lost cohort, period, segment, offer, deal size, channel, and minimum evidence coverage.
2. [INTEGRATION] Retrieve CRM outcomes, customer communications/calls, competitor references, pricing/discount context, stage duration, and available post-decision interviews. Draw on evidence-coverage operating knowledge when it materially improves source completeness.
3. [AI] Extract direct customer decision reasons and separate them from seller inference. Theme-coding and decision-driver methods may help when evidence volume/complexity warrants them; they are not required stages.
4. [HYBRID] Build multi-cause decision interpretations with primary/contributing factors and unknown where evidence is absent.
5. [DETERMINISTIC] Compare rates and factor prevalence across wins/losses while checking selection/sample bias.
6. [AI] Identify decision criteria, competitive alternatives, proof gaps, expectation mismatches, and segment-specific patterns.
7. [HYBRID] Test candidate explanations against contradictory cases and behavior rather than reporting correlation as cause.
8. [HYBRID] Preserve scoped Customer Insights and useful competitor/journey/process observations directly in organizational memory. Other operating areas may reuse that evidence when relevant; do not create an internal routing handoff merely because the implication crosses domains.

## Decision Rules
- Treat CRM loss/win reason fields as evidence about seller/system coding unless the reason is traceable to the buyer.
- Use `unknown` when evidence does not support a reason; do not force complete attribution.
- Publish segment-specific Insights instead of one global conclusion when factor prevalence or mechanism differs materially by segment, Offer, or stage.
- Do not infer causal importance from factor frequency alone; compare wins/losses and contradictory cases, and state when sampling prevents a reliable comparison.
