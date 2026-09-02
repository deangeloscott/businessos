---
id: seo.diagnosis.ranking-decay
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
- Incident
context:
- AudienceSegment
- Market
- Objective
- Offer
evidence_inputs:
- rank/visibility time series query-page mappings
---
# Ranking Visibility Loss Diagnosis & Recovery

## Purpose
Determine whether valuable organic visibility has materially declined, explain the most plausible mechanism, and guide proportionate recovery without treating every fluctuation as actionable.

## Business Outcome
Protect valuable organic discovery by separating real ranking loss from demand, indexing, SERP, seasonality, tracking, and measurement effects and by acting on the strongest supported cause rather than reflexively rewriting content.

## Run When
Use when current evidence or the user indicates a meaningful loss of ranking or search visibility. The same Workflow applies from localized decay to a broad/high-value collapse; severity changes urgency and depth, not the underlying reasoning method.

## Process
1. [HYBRID] Verify the apparent decline using appropriate recent/prior/YoY/rolling windows while retaining query, page, topic, market, device, surface, and timestamp context. Rule out measurement/provider/tracking artifacts before diagnosing a ranking problem.
2. [HYBRID] Determine whether the change is material relative to normal volatility and business value, then define the affected scope: page-specific, query/topic cluster, template/sitewide, market/device-specific, competitor displacement, or unresolved.
3. [AI] Separate changes in demand, ranking/visibility, indexing, SERP layout/features, seasonality, and measurement. Do not infer ranking loss merely from organic-traffic loss.
4. [HYBRID] Compare timing and scope with relevant page/site changes, deployments, migrations, technical/index state, canonical/access issues, policy/manual-action notices, security problems, competitor/SERP movement, authority/freshness/cannibalization, demand shifts, and material ecosystem developments.
5. [AI] Rank plausible causes by evidence, explanatory power, reversibility, and business impact. Preserve uncertainty when evidence does not yet distinguish causes; do not automatically rewrite content until a content mechanism is actually plausible.
6. [AI] For broad or high-value collapse, prioritize containment and reversible common causes. Recommend pausing or reversing recent harmful-looking changes when evidence and reversibility justify it, favoring restoration of known-good access/index/canonical/tracking state over speculative changes. The active user/harness owns real execution.
7. [HYBRID] Carry out or recommend the smallest useful intervention supported by the diagnosis, then re-check the affected evidence after enough time for the mechanism to respond. Preserve an Opportunity when there is a valuable addressable improvement; preserve an Incident only when the event is severe enough that durable cross-session visibility materially helps.
8. [AI] Record material root cause, recovery action/result, unresolved uncertainty, and reusable Learning when supported. AURA does not own a background recovery monitor or runtime pause/resume control.

## Verification
- Demand, ranking, indexing, SERP-layout, seasonality, tracking, and measurement effects are separated before assigning cause.
- Severity and business impact are evidence-backed rather than inferred from a label such as “collapse.”
- Containment/recovery recommendations are distinguished from actions actually executed.
- Recovery claims use subsequent evidence and do not overstate causality.
