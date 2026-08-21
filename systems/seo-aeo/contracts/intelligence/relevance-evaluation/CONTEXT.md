---
id: seo.intelligence.relevance-evaluation
type: detector
version: 1.1.0
owner_system: seo-aeo
risk: low
autonomy_ceiling: 4
reads:
- Insight
- Opportunity
writes:
- Observation
- Insight
- Opportunity
- WorkRequest
capabilities:
  required:
  - none
  optional:
  - none
events:
  consumes:
  - insight.activated
  - insight.updated
  - insight.contradicted
  emits:
  - intelligence.relevance.evaluated
context:
- AudienceSegment
- Market
- Objective
- Offer
---
# SEO/AEO Relevance Evaluation

## Purpose
Evaluate whether shared intelligence from another semantic domain materially affects valuable organic discovery without duplicating the upstream Insight or launching expensive work automatically.

## Business Outcome
Reuse organizational intelligence wherever it can improve decisions while preventing irrelevant fan-out and duplicate research.

## Run When
Run when a new, materially updated, or contradicted Insight is published for the active business, or when an operator explicitly asks whether an Insight matters to this domain.

## Do Not Run When
Do not run for Insights from another business, archived/stale intelligence with no current decision relevance, or when an existing domain Opportunity already fully incorporates the same evidence and no material change occurred.

## Process
1. [DETERMINISTIC] Confirm business ID, Insight status, owner system, subjects, market/audience/offer references, and freshness before semantic review.
2. [DETERMINISTIC] Apply cheap relevance filters against active markets, audiences, offers, Objectives, existing domain state, and current Opportunities.
3. [AI] Evaluate the domain mechanism: Ask whether the Insight could alter organic demand, search/answer intent, content/source requirements, search competitors, technical/indexing priorities, authority/local/AEO visibility, or organic conversion alignment. Validate with SEO observations before creating an SEO Opportunity.
4. [AI] Search existing domain Insights/Opportunities for the same interpretation or intervention before creating anything new.
5. [HYBRID] Choose one response: ignore, watch, attach evidence to existing state, perform bounded domain research, request an owner-domain refresh, create/update a domain Insight, create a candidate Opportunity, or escalate an Incident.
6. [HYBRID] Require a plausible domain-specific mechanism and sufficient expected value before creating an Opportunity; mere topical similarity is not enough.
7. [DETERMINISTIC] Persist only domain-owned outputs and retain the upstream Insight reference as lineage; emit the relevance result.

## Verification
- No copy of the upstream Insight is created.
- Any new Opportunity has exactly one domain owner and a distinct intervention mechanism.
- Any foreign-domain research result is published as Observation/provisional interpretation rather than a competing source of truth.

## Measurement
- Track proportion of routed Insights that produce useful evidence/Opportunities versus irrelevant/noisy fan-out and tune cheap filters accordingly.

## Learning
- Learn which upstream Insight classes reliably matter to this domain and use that only to improve relevance routing, not to override semantic ownership.

## Failure / Fallback
- If required upstream detail is stale or insufficient, request a refresh from the canonical owner; bounded local research is permitted for urgent continuity with provisional interpretation.

## Completion Criteria
- Relevance response is explicit and any next work is canonically represented.
- No duplicate Insight or fake delegated Opportunity has been created.
