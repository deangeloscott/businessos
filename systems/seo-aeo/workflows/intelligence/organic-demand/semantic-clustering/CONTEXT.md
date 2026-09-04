---
id: seo.intelligence.organic-demand.semantic-clustering
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- MetricObservation
- OrganicDemandUnit
writes:
- OrganicDemandUnit
context:
- AudienceSegment
- Market
- Objective
- Offer
- ProductService
evidence_inputs:
- Market search answer evidence
- records topic intent evidence
updates:
  OrganicDemandUnit:
  - business_value
  - demand_evidence
---
# Semantic Demand Clustering

## Purpose
Group demand by shared underlying need while preserving distinct intents, audiences, constraints, or destinations that deserve separate treatment.

## Business Outcome
Create a useful demand map that reduces duplicate thinking and content while still allowing the organization to serve genuinely different customer tasks well.

## Run When
Use when many queries, prompts, questions, or OrganicDemandUnits need to be organized into coherent needs or when existing clusters appear to collapse meaningful distinctions.

## Process
1. [HYBRID] Represent demand with the evidence that can change grouping: wording, entities, inferred intent, audience, stage, market, result/answer overlap, constraints, business pathway, and current destination where relevant.
2. [AI] Form candidate clusters from shared user need and semantic/result evidence rather than keyword similarity alone.
3. [AI] Split clusters when similar wording hides materially different tasks, audiences, locations, comparison contexts, constraints, journey stages, or conversion destinations.
4. [AI] Merge superficial wording variants when one strong answer or asset can satisfy them naturally without awkward keyword-specific treatment.
5. [AI] Name and organize clusters in language useful to customers and operators. Hierarchy is a convenience for understanding, not a rigid ontology the model must obey.
6. [AI] Relate clusters to owned assets, missing experiences, competitor coverage, or other work only when that mapping improves a real decision.
7. [HYBRID] Persist cluster membership and rationale when future work benefits; allow later evidence or capable-model judgment to reorganize it without treating the prior taxonomy as immutable truth.

## Verification
- Semantic similarity does not erase materially different user tasks.
- Minor wording differences do not create unnecessary separate assets or durable objects.
- Cluster structure remains revisable as evidence and model understanding improve.
- Opportunity generation or competitor refresh is optional rather than a required lifecycle stage.
