---
id: seo.incidents.manual-action-or-policy
type: incident
version: 1.1.0
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
events:
  consumes:
  - none
  emits:
  - seo.incident.updated
---
# Manual Action / Policy Incident

## Purpose
Handle search/platform policy notices or credible evidence of a policy-related visibility problem with documented remediation.

## Business Outcome
Improve valuable organic discovery through manual action / policy incident, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run immediately when monitoring or an operator identifies a plausible **manual action / policy incident**. Incident routing overrides normal optimization until containment is complete.

## Process
1. [HYBRID] Capture the exact notice/source, affected property/scope, cited behavior, dates, and current tactics that may relate.
2. [HYBRID] Pause potentially implicated autonomous tactics and preserve evidence/history.
3. [AI] Audit affected patterns against current official policy and classify confirmed violation, possible issue, unrelated issue, or unknown.
4. [HYBRID] Remove/remediate problematic implementation comprehensively rather than hiding it or creating circumvention.
5. [HYBRID] Verify remediation across templates/content/links/data and prepare required reconsideration/appeal information through official process where applicable.
6. [AI] Update tactic classification/playbooks and monitor recovery; require human/compliance review for material policy incidents.


