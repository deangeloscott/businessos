---
id: customer.intelligence.ecosystem-radar
type: workflow
owner_system: customer-intelligence
reads:
- SourceProfile
- SourceRecord
- Observation
- Insight
- Learning
- Opportunity
writes:
- Observation
- Insight
context:
- Business
- AudienceSegment
- Market
- Objective
- ProductService
workflows:
  required:
  - id: core.intelligence.ecosystem.source-discovery
  - id: core.intelligence.ecosystem.evidence-triangulation
  conditional:
  - id: customer.analysis.insight-refresh
    when: New evidence may materially strengthen, narrow, contradict, or supersede an existing Customer Insight.
---
# Customer Signal Ecosystem Radar

## Purpose
Detect changing customer needs, language, objections, expectations, desired outcomes, category behaviors, and use cases from external and first-party evidence without mistaking market conversation for active-customer truth.

## Business Outcome
Keep customer understanding current enough to improve decisions while preserving segment, source, and evidence boundaries.

## Run When
Use on demand for customer-signal refresh or when external/first-party evidence suggests customer behavior or expectations may be changing.

## Process
1. [HYBRID] Reuse current Customer Insights, evidence coverage, segments, SourceProfiles, and recent first-party/public observations before launching new retrieval.
2. [AI] Discover decision-relevant signals across reviews, communities, social discussion, research, category conversations, sales/support/survey evidence when available, and adjacent emerging use cases. Search depth and sources follow the actual question rather than a fixed domain sweep.
3. [HYBRID] Preserve direct statements as Observations and use Core triangulation to distinguish independent customer evidence from reposted narratives, influencer interpretation, survey/report repetition, and speculation.
4. [AI] Separate expressed customer language/behavior from inferred motivation, and test whether apparent change is actually segment, market, journey-stage, time, channel, or sampling/method composition.
5. [HYBRID] Compare external-market signals with active-business first-party evidence when applicability matters. External prevalence does not establish that this organization's customers share the same pattern.
6. [AI] Decide whether existing Customer Insights should be retained, narrowed, strengthened, contradicted, superseded, or left unresolved. `customer.analysis.insight-refresh` may be useful operating knowledge; it is not an automatic lifecycle route.
7. [AI] State material implications or useful next research/work as recommendations. The active model/harness may continue through relevant methods directly; this radar does not create WorkRequests for internal delegation or route implications into other systems as canonical control state.
8. [DETERMINISTIC] Persist only material Observation/Insight content and exact evidence references selected by the model/user. Reusable Customer Learning changes require evidence appropriate to that Learning and are not automatic consequences of a radar cycle.

## Verification
- Customer observation, interpretation, and active-business applicability remain distinct.
- Frequency claims remain scoped to measured or sampled populations.
- Any semantic Insight merge/change reflects model judgment rather than deterministic text matching.

## Completion Criteria
- Material customer changes are evidence-backed, segment-scoped, freshness-aware, and understandable without requiring an AURA routing lifecycle.
