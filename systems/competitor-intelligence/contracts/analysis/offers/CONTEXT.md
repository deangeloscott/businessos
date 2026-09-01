---
id: competitor.analysis.offers
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
context:
- AudienceSegment
- Business
- EconomicContext
- Market
- Objective
- Offer
- ProductService
---
# Offer Intelligence

## Purpose
Understand how competitors package commercial value, risk reversal, incentives, CTA, and buying path.

## Business Outcome
Improve competitive decisions through evidence-backed offer intelligence, without mistaking observed activity for proven effectiveness.

## Run When
Run when a decision requires current offer intelligence and canonical competitor intelligence is missing, stale, contradictory, or insufficiently specific.

## Process
1. [INTEGRATION] Capture current offer pages, promotions, trials, demos, guarantees, bundles, bonuses, terms, and primary CTAs.
2. [AI] Decompose product/service, price, terms, incentive, risk reversal, proof, eligibility, urgency/scarcity, and next action.
3. [HYBRID] Distinguish persistent offer from limited promotion or personalized sales term.
4. [DETERMINISTIC] Compare with prior state and competitor set.
5. [AI] Identify apparent audience/stage fit and strategic intent.
6. [HYBRID] Use customer/win-loss evidence before claiming an offer is effective or preferable.
7. [DETERMINISTIC] Update competitor Observations/Insights and notify relevant systems if materially changed.
