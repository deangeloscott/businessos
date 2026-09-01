---
id: core.opportunity.qualify
type: playbook
owner_system: core
reads:
- Insight
- Opportunity
writes:
- Opportunity
capabilities:
  required:
  - none
  optional:
  - none
context:
- EconomicContext
- Objective
---
# Qualify Opportunity

## Purpose
Turn a diagnosed condition and plausible intervention into a comparable, evidence-backed business opportunity without making Opportunity state an execution or permission lifecycle.

## Business Outcome
Help allocate attention toward interventions likely to create business value while preserving uncertainty about impact, cost, and feasibility when those facts are not known.

## Run When
When evidence supports preserving a plausible intervention opportunity for comparison, prioritization, or future execution.

## Do Not Run When
Do not create an Opportunity for delegated production work, transient ideas with no durable value, or conditions with no plausible intervention.

## Process
1. [AI] Retrieve potentially overlapping current Opportunities and decide semantic equivalence from the underlying condition/intervention, not keyword overlap. Update an existing Opportunity when it genuinely represents the same intervention.
2. [AI] State the diagnosed condition, business mechanism, affected entities, and what intervention could plausibly change.
3. [HYBRID] Link Objectives and estimate expected value only to the precision supported by evidence. Separate evidence that the condition exists from evidence the intervention will work, and separate external benchmarks from active-business measurements.
4. [HYBRID] Assess confidence, urgency where real, strategic leverage, material risks/constraints, dependencies, reversibility, and automation feasibility. Record implementation/resource cost only when known or evidence-backed; otherwise keep it unknown rather than inventing staffing, days, cost, or ROI timing.
5. [AI] Do not automatically penalize an opportunity using conventional manual-development effort assumptions when execution may be automated. Real blockers and known resource commitments still matter.
6. [HYBRID] Apply a consistent interpretable priority framework when comparison is useful. Any deterministic arithmetic may calculate explicitly chosen components; the model/user owns the semantic inputs and business judgment.
7. [AI] Choose the narrowest current status/maturity that truthfully describes what is known and decided. Status records organizational state; it does not authorize execution.
8. [DETERMINISTIC] Persist the Opportunity and validate its evidence/references. Do not emit an AURA runtime event merely because it was qualified or reprioritized.

## Verification
- Company-specific expected-value claims are supported by company-specific inputs or clearly expressed as scenarios/hypotheses.
- Semantic identity, business value, and prioritization judgments remain inspectable rather than hidden in deterministic routing.
- Opportunity state does not create execution authority.

## Failure / Fallback
- If evidence is insufficient to qualify the intervention responsibly, preserve the unresolved evidence need or keep the Opportunity at the narrowest supported state instead of manufacturing a Manual Action Packet or false precision.

## Completion Criteria
- The Opportunity provides a useful, evidence-calibrated basis for future comparison or action without pretending that qualification itself is a decision to execute.
