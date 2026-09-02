---
id: customer-optimization.monitoring.churn-risk
type: workflow
owner_system: customer-optimization
reads:
- CustomerJourney
- Observation
- Insight
- Opportunity
- MetricObservation
- Experiment
writes:
- Observation
- Insight
- Opportunity
context:
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Customer Churn Risk Monitoring

## Purpose
Review observable lifecycle conditions that may indicate elevated churn risk so the business can investigate and respond appropriately, while keeping likelihood of loss separate from the value/consequence at risk.

## Business Outcome
Surface actionable, interpretable churn-risk evidence early enough for responsible response without opaque/sensitive profiling or treating account value as churn probability.

## Run When
Use for a bounded churn-risk review when the user requests it, when saved monitoring intent indicates another review would be useful, or when new customer evidence could materially change an existing risk assessment. Any recurring execution/reminder belongs to the active harness/runtime.

## Process
1. [HYBRID] Reuse supported Journey/Customer Insights/Learnings and current evidence to choose interpretable risk indicators relevant to this business, such as missed value milestones, unresolved failures, usage/adoption decline, support escalation, renewal issues, billing/process problems, or explicit feedback. Do not assume a generic indicator is predictive here without evidence.
2. [DETERMINISTIC] Calculate the observable indicator state from available operational evidence and compare it with prior saved observations/checkpoints when those exist. Repeated unchanged evidence should not create duplicate canonical findings.
3. [AI] Judge the plausible mechanism and distinguish data anomaly, expected seasonality, healthy lower usage, lifecycle differences, deliberate reduced need, or actual deterioration.
4. [AI] Keep risk likelihood/evidence separate from consequence/value-at-risk. Revenue, LTV, margin, strategic importance, or customer value may help prioritize attention only after risk is supported; high account value must never increase inferred churn probability by itself.
5. [AI] Do not infer sensitive traits or use opaque scores without interpretable contributing factors. Preserve uncertainty and prefer cohort/process understanding when individual profiling is unnecessary.
6. [AI] Determine whether the evidence warrants investigation, human/customer-success outreach, service recovery, education, product/process correction, commercial/renewal review, an Opportunity, continued observation, or no action. Prioritize restoration of customer value over manipulative retention.
7. [HYBRID] Persist a scoped Observation/Insight and, only when a durable intervention candidate is genuinely justified, an Opportunity with contributing evidence, uncertainty, and separately calculated value-at-risk where useful. Do not create a generic Action or runtime alert object merely because an indicator crossed a threshold.
8. [HYBRID] When later outcome evidence becomes available, compare whether the risk resolved and whether customer value was restored; update reusable Learning only at the scope justified by repeated/credible evidence.

## Verification
- Churn likelihood and value-at-risk remain separate.
- Every material risk conclusion is traceable to interpretable evidence.
- AURA may remember monitoring intent/checkpoints but does not own the recurring job, alert delivery, or outreach execution.
- No sensitive or opaque profiling is introduced merely to improve prediction.

## Completion Criteria
- The organization has an evidence-calibrated view of material churn risk and the most appropriate next response, if any, without an AURA-owned alerting or autonomous retention loop.
