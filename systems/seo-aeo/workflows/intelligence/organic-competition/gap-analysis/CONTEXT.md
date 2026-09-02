---
id: seo.intelligence.organic-competition.gap-analysis
type: workflow
owner_system: seo-aeo
reads:
- OrganicDemandUnit
- Observation
- OrganicCompetitorState
- Competitor
writes:
- OrganicCompetitorState
- MetricObservation
- Observation
- Competitor
context:
- AudienceSegment
- Market
- Objective
- Offer
- ProductService
---
# Competitive Gap Analysis

## Purpose
Convert competitor and market observations into specific business-relevant gaps without turning every difference into an Opportunity or copying what competitors do.

## Business Outcome
Identify where the organization can credibly create more useful organic/search/answer value because competitors outperform, the market repeatedly rewards a useful pattern, or important customer demand remains underserved.

## Run When
Use when competitor evidence is sufficient to compare the organization's current coverage or capability against meaningful demand and a gap decision would be useful.

## Process
1. [HYBRID] Compare owned demand, assets, current performance, and business priorities with relevant search, answer, and business-competitor evidence.
2. [AI] Identify materially useful gaps such as underserved demand, missing evidence or asset types, authority/source weaknesses, format/task mismatches, or areas where competitors are also weak.
3. [AI] Determine why the observed difference may matter. Separate a competitor having something from evidence that users, search surfaces, or the business actually benefit from it.
4. [HYBRID] Judge whether the organization can credibly produce a better, different, or more useful solution given its real expertise, Offer, audience, resources, and constraints.
5. [AI] Reject imitation opportunities that lack audience/business fit, depend on unsupported claims or prohibited tactics, or would merely add redundant content.
6. [AI] Rank the remaining gaps by business relevance, user value, mechanism plausibility, leverage, evidence strength, and effort only to the resolution useful for the decision.
7. [HYBRID] Preserve the supporting competitor/demand evidence and the resulting gap conclusion when future work benefits. Create an Opportunity only when the unresolved strategic possibility itself is worth remembering.

## Verification
- Competitor prevalence is not treated as proof of effectiveness.
- Gaps remain tied to real demand, customer utility, or a credible business/discovery mechanism.
- The analysis can validly conclude that no intervention is justified.
- Follow-on work is chosen directly by the capable model/user rather than routed through a required qualification lifecycle.
