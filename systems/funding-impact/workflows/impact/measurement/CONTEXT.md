---
id: funding.impact.measurement
type: workflow
owner_system: funding-impact
reads:
- Business
- ProductService
- Objective
- MetricDefinition
- MetricObservation
- ProofRecord
writes:
- MetricDefinition
- MetricObservation
- Objective
- Learning
context:
- Business
- ProductService
- Objective
---
# Impact Measurement

## Purpose
Decide which outcomes show whether the organization's work is making the intended difference, and set up a practical way to measure them.

## Business Outcome
A small set of meaningful outcome measures the organization can actually collect, used to improve programs and to report credibly to funders and supporters.

## Run When
Use when the organization cannot clearly show its results, a funder asks for outcomes or an evaluation plan, or measures exist but do not inform decisions. Revisit when programs change.

## Process
1. [AI] Start from the organization's most important goals and how its programs are meant to produce change: who is served, what they receive, what changes for them in the short and longer term. Write this as a simple theory of change or logic model.
2. [AI] Separate outputs (what was delivered, such as meals served or sessions held) from outcomes (what changed, such as food security or skills gained). Reporting only outputs does not show impact.
3. [HYBRID] Choose the vital few outcomes closest to the organization's own work and most useful for decisions. Resist measuring everything or only what is easy. Note the assumptions in the theory of change that have the least evidence.
4. [AI] For each outcome, define the measure, data source, how and when it is collected, who collects it, a baseline if available, and a realistic target. Include qualitative evidence such as participant feedback where numbers alone mislead.
5. [HYBRID] Involve the people served where possible in defining what success means. Collect personal data only as needed, with consent, and protect it.
6. [DETERMINISTIC] Save each measure as a MetricDefinition and record results as MetricObservations with their source and period, linked to the related goals so progress shows where the organization tracks its goals.
7. [AI] Plan how results will be reviewed and used to adjust programs, not only reported.

## Proportionate Scope
A small organization may start with two or three outcomes and simple surveys or counts. Larger programs may justify more rigorous evaluation; say what each level of evidence can and cannot show.

## Verification
- Outputs and outcomes are distinct; each outcome has a feasible measure and source.
- Measures are saved and linked to goals so progress is visible over time.
- Claims about cause are no stronger than the evidence supports.
