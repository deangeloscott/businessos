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
- Asset
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
Increase the likelihood of the desired commercial action through evidence-backed Offer presentation that matches audience awareness, Offer, proof, and acquisition context.

## Run When
Use when an existing Offer needs clearer or stronger commercial presentation. An Opportunity or real durable WorkRequest may provide context but is not required.

## Process
1. [HYBRID] Load canonical Offer truth: included products/services, pricing/terms, eligibility, bonuses, guarantees, availability, and conversion action.
2. [AI] Map the Offer to customer desired outcomes, decision criteria, objections, perceived risks, and alternatives.
3. [AI] Determine presentation order and emphasis: value/outcome, mechanism, inclusions, proof, risk reversal, price/terms, fit, CTA.
4. [HYBRID] Ensure presentation does not silently change actual commercial terms. If the organization wants to consider a real Offer change, use `marketing.offer.diagnosis` or direct business reasoning as useful; proposing a change is not adopting it.
5. [AI] Identify information/proof gaps that prevent credible presentation.
6. [AI] Preserve asset-ready Offer presentation guidance as a Marketing-owned strategy Asset.
7. [HYBRID] If the organization actually establishes a new Offer term/structure, update canonical Offer truth through the normal current-context path with provenance. Keep unresolved ideas labeled as candidate strategy; do not manufacture a ContextUpdateProposal, WorkRequest, approval object, or Opportunity merely because a change was considered.
