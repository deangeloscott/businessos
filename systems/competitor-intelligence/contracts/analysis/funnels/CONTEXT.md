---
id: competitor.analysis.funnels
type: playbook
owner_system: competitor-intelligence
reads:
- Competitor
- type: Insight
  owner_system: customer-intelligence
- Observation
- SourceRecord
writes:
- Competitor
- Observation
- Insight
capabilities:
  required:
  - research.web.read
  optional:
  - webpage.snapshot
  - webpage.compare
  - advertising.observe
  - review.read
  - crm.opportunity.read
  - social.observe
  - browser.interact
  - crawler.run
  - email.read
context:
- AudienceSegment
- Business
- Market
- Objective
- Offer
- ProductService
subcontracts:
  required:
  - competitor.analysis.funnel-capture
  - competitor.analysis.funnel-comparison
---
# Funnel Intelligence

## Purpose
Map observable competitor acquisition/conversion pathways and major friction/strategy signals using actual legitimate traversal where relevant.

## Business Outcome
Improve competitive decisions through evidence-backed funnel intelligence without mistaking observed activity for proven effectiveness.

## Run When
Run when a decision requires current funnel intelligence and canonical competitor intelligence is missing, stale, contradictory, or insufficiently specific.

## Process
1. [HYBRID] Define the customer entry point/channel, research depth, scenario, and observable scope; do not fabricate hidden internal steps.
2. [HYBRID] Use the Funnel Capture subprocess to traverse legitimate public/consented acquisition paths and preserve actual observed steps rather than inferring the funnel from static pages alone.
3. [DETERMINISTIC] Normalize steps, fields, gates, CTAs, redirects, timing, follow-up, pricing visibility, access boundaries, and major proof/objection elements across captured paths.
4. [AI] Infer intended audience/stage and conversion strategy while clearly marking unobservable assumptions and differences caused by market, device, identity, or path.
5. [HYBRID] Identify materially distinctive friction-reduction, qualification, education, persuasion, or handoff patterns and compare like with like.
6. [HYBRID] Do not label a funnel high-performing without independent performance evidence; distinguish a sophisticated/observable funnel from an effective one.
7. [DETERMINISTIC] Publish reusable funnel Observations/Insights and preserve partial/blocked branches for future refresh.

## Verification
The funnel model is grounded in reproducible observed paths and clearly distinguishes public interaction evidence from inference and private unknowns.
