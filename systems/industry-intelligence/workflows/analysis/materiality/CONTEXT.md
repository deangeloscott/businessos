---
id: industry.analysis.materiality
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
# Materiality Assessment

## Purpose
Determine whether an external development is important enough to change business attention or decisions, without turning materiality into an internal event trigger.

## Business Outcome
Focus organizational attention on external changes that can plausibly matter while preserving uncertainty and avoiding noise-driven reaction.

## Run When
When a verified or sufficiently credible IndustryEvent could materially affect a current or foreseeable business decision and existing materiality analysis is missing, stale, or unresolved.

## Process
1. [AI] Identify potentially affected markets, audiences, products/services, capabilities, economics, compliance, channels, competitors, and timelines from the actual evidence and current business context.
2. [HYBRID] Assess magnitude, probability/uncertainty, timing, persistence, reversibility, and proximity to active Objectives without inventing precision.
3. [AI] Distinguish direct operational effect, customer-behavior effect, competitive effect, narrative/content relevance, and speculative second-order effects. Draw on impact-pathway operating knowledge when a multi-step causal chain materially affects the decision; it is not a required subworkflow.
4. [AI] Use any organization-defined materiality criteria or thresholds as decision context when they actually exist; do not invent a configured threshold framework merely to classify the event.
5. [AI] Generate plausible alternative interpretations and state what evidence would materially change the assessment.
6. [AI] State relevance, urgency where real, uncertainty, affected business mechanisms, and possible next considerations without assigning mandatory domain routes or responses.
7. [HYBRID] Persist or update an Industry Insight only when the interpreted materiality has durable organizational value. Keep the IndustryEvent itself factual; do not turn it into a scored decision or AURA runtime event.

## Verification
- Materiality conclusions are traceable to the IndustryEvent/evidence and active business context.
- Relevance, urgency, probability, and impact remain distinct.
- The assessment does not create execution authority, domain routing, or runtime event state.

## Completion Criteria
- Future work can understand whether and why the external development matters, what remains uncertain, and what business decisions it could affect without an internal event trigger.
