---
id: seo.diagnosis.technical-opportunity
type: workflow
owner_system: seo-aeo
reads:
- OrganicDemandUnit
- SEOAssetState
- Asset
- OrganicCompetitorState
- Competitor
- MetricObservation
- ChangeEvent
- Observation
writes:
- Opportunity
context:
- AudienceSegment
- Market
- Objective
- Offer
---
# Technical SEO Opportunity Diagnosis

## Purpose
Turn crawl, indexing, rendering, performance, architecture, and related technical evidence into a root-cause diagnosis worth acting on.

## Business Outcome
Identify systemic technical problems that materially affect valuable organic discovery without creating duplicate per-URL work or treating symptom volume as severity.

## Run When
Use when current technical evidence suggests a material discovery problem and the model/user needs to determine the affected scope, plausible shared mechanism, business importance, and most useful next technical method.

## Process
1. Group observations by plausible shared template, component, configuration, deployment, URL pattern, infrastructure layer, or other common cause before considering per-URL interventions.
2. Relate affected Assets to business value, demand, traffic, index state, conversions, backlinks, and relevant change history only where those dimensions help establish materiality or mechanism.
3. Separate intentional states from defects and distinguish symptoms from root cause. Symptom count alone does not establish severity or one common mechanism.
4. Prefer systemic root-cause fixes when one supported mechanism explains many affected Assets; preserve targeted exceptions when evidence shows the cases are genuinely different.
5. Select the relevant technical Workflow or another sound method based on the diagnosis. Do not require an Opportunity object merely to continue the work; preserve one only when durable organizational coordination benefits from it.
6. For broad or severe conditions, increase validation, rollback, representative sampling, and recovery evidence in proportion to the stakes rather than switching into a separate AURA incident-control lifecycle.

## Proportionate Scope
Sample enough representative and high-value cases to establish the likely mechanism and blast radius. Expand toward broader/full-site analysis when heterogeneity, severity, uncertainty, or potential systemic impact makes additional evidence likely to change the conclusion.

## Verification
- Root cause, affected scope, intentionality, severity, and business impact remain separately supported.
- Technical remediation remains the work of the active model/user/harness using the real systems and tools available.
- Do not create thousands of duplicate tasks when one systemic cause explains the evidence.

## Deterministic Local-Site Evidence
When scoped evidence is a local or first-party website export, use the repository's deterministic site-evidence helpers where they materially improve fact capture. Keep consequences, severity, and visibility implications as inference unless separately measured.
