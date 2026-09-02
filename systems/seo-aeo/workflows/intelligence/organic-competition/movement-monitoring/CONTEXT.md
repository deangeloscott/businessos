---
id: seo.intelligence.organic-competition.movement-monitoring
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
# Competitor Movement Monitoring

## Purpose
Detect material changes in competitor visibility, assets, authority, answers, reputation, and Offers that could change the organization's organic-discovery decisions.

## Business Outcome
Recognize meaningful competitive movement early enough to protect or create attention, traffic, answer visibility, leads, and other business opportunities without reacting to ordinary volatility or copying competitors blindly.

## Run When
Use when fresh competitor comparison is useful because important visibility changed, a meaningful competitor changed its assets or strategy, or recurring monitoring is invoked by the user/runtime. AURA may remember monitoring intent; the harness/runtime owns recurrence.

## Process
1. [HYBRID] Refresh the search, answer, authority, local/reputation, and high-priority competitor observations that materially matter to the current business objective rather than re-measuring every known competitor surface.
2. [HYBRID] Detect changes such as new or substantially revised assets, site migrations, acquired/lost references, review/local shifts, new Offers, or sustained search/answer gains.
3. [AI] Separate provider noise, ordinary volatility, seasonality, and one-off movement from changes that are sustained or strategically meaningful.
4. [AI] Compare competitor movement with owned and market-wide performance so a competitor-specific change is not confused with a broader demand, platform, or measurement shift.
5. [AI] Interpret what the movement may mean for the organization: lost/gained exposure, a newly proven audience need, a useful asset pattern, an authority/source change, a possible tactical hypothesis, or no material consequence. Visibility movement is an upstream signal, not automatic proof of competitor revenue or causal superiority.
6. [HYBRID] Preserve a material alert, Opportunity, Insight, or Learning only when future work benefits from remembering it. Novel tactics may use evidence-assessment methods when that would materially improve confidence; they are not automatically routed through a pipeline.

## Verification
- Material movement is distinguished from noise and market-wide change.
- Observed visibility, assets, mentions, links, and reputation signals are not presented as competitor revenue or proven causality.
- Upstream visibility signals may still be treated as meaningful when they plausibly change exposure and downstream opportunity.
- Follow-on work is selected directly by the capable model/user based on the actual mechanism.
