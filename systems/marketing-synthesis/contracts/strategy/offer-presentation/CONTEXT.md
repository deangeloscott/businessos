---
id: marketing.strategy.offer-presentation
type: playbook
owner_system: marketing-synthesis
reads:
- type: Insight
  owner_system: customer-intelligence
- type: Insight
  owner_system: competitor-intelligence
- Asset
- MetricObservation
writes:
- Insight
- Opportunity
- WorkRequest
capabilities:
  required:
  - none
  optional:
  - marketing.performance.read
  - conversion.read
  - analytics.read
context:
- AudienceSegment
- Brand
- Objective
- Offer
subcontracts:
  conditional:
  - id: marketing.offer.diagnosis
    when: evidence suggests the actual Offer structure, not only presentation, is limiting response
---
# Offer Presentation Strategy

## Purpose
Present an existing canonical Offer so value, terms, risk, proof, and next action are understandable and compelling.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed offer presentation strategy that matches audience awareness, offer, proof, and acquisition context.

## Run When
Run when an Opportunity or WorkRequest requires offer presentation strategy to remove a commercial persuasion gap or create the required conversion asset.

## Process
1. [DETERMINISTIC] Load canonical Offer truth: included products/services, pricing/terms, eligibility, bonuses, guarantees, availability, and conversion action.
2. [AI] Map the Offer to customer desired outcomes, decision criteria, objections, perceived risks, and alternatives.
3. [AI] Determine presentation order and emphasis: value/outcome, mechanism, inclusions, proof, risk reversal, price/terms, fit, CTA.
4. [HYBRID] Ensure no copy changes the actual commercial terms; proposed price/guarantee/offer changes require business authority.
5. [AI] Identify information/proof gaps that prevent credible presentation.
6. [HYBRID] Produce asset-ready offer presentation guidance and Context Change Proposal only when a real offer change is recommended.
