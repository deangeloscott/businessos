---
id: seo.incidents.ranking-collapse
type: incident
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- MetricObservation
- ChangeEvent
- Opportunity
- Observation
writes:
- Incident
capabilities:
  required:
  - analytics.read
  optional:
  - search.performance.read
  - search.index.inspect
  - crawler.run
  - cms.page.read
evidence_inputs:
- rank/visibility time series query-page mappings
---
# Ranking Collapse Incident

## Purpose
Rapidly understand and recover from a broad or high-value ranking/visibility collapse without turning AURA into an incident-control runtime.

## Business Outcome
Restore valuable organic discovery faster by separating real collapse from measurement noise, identifying plausible causes, and preserving an evidence-backed incident record and recovery learning.

## Run When
Use when current evidence or the user indicates a plausible broad/high-value ranking collapse that needs focused diagnosis and response.

## Process
1. [HYBRID] Verify that the apparent collapse is real, not a measurement/provider artifact, and quantify affected pages/topics/markets/devices plus the earliest supported timing.
2. [HYBRID] Compare the timing with relevant deployments/ChangeEvents, index/technical state, migrations, policy/manual-action notices, security issues, competitor/SERP changes, demand shifts, and known ecosystem developments.
3. [AI] Identify changes that could plausibly worsen the incident if continued and recommend pausing/reversing them when evidence and reversibility justify it. AURA records the recommendation/context; the active user/harness owns the actual operational change.
4. [AI] Rank reversible likely causes and favor restoring known-good access/index/canonical/tracking state before speculative content rewrites when the evidence supports that path.
5. [HYBRID] Execute recovery through the active harness/user using the real tools, permissions, and organizational constraints available; preserve material actions/results in the Incident only when future continuity benefits from them.
6. [HYBRID] Re-check the affected evidence after changes and preserve the root cause, recovery result, unresolved uncertainty, and reusable Learning when supported. AURA does not own a background recovery monitor or an autonomy toggle.

## Verification
- Separate demand, ranking, indexing, SERP-layout, seasonality, measurement, and tracking effects before assigning a cause.
- Containment/recovery recommendations are evidence-backed and clearly distinguished from actions actually executed.
- Incident state records organizational meaning; it does not suspend or resume the host runtime.

## Completion Criteria
- The organization has a defensible diagnosis, appropriate recovery/containment actions have been executed or clearly identified by the real owner, and future work can understand what happened and what was learned without an AURA control plane.
