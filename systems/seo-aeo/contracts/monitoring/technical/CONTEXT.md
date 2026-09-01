---
id: seo.monitoring.technical
type: playbook
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- MetricObservation
- ChangeEvent
- Opportunity
- Observation
writes:
- MetricObservation
- Opportunity
- Incident
- SEOAssetState
capabilities:
  required:
  - crawler.run
  optional:
  - webpage.fetch
  - cms.page.read
  - cms.page.update
  - search.index.inspect
updates:
  SEOAssetState:
  - organic_performance
---
# Technical Health Monitoring

## Purpose
Review technical conditions that may materially affect discovery, user experience, or SEO measurement without making AURA a crawler/uptime runtime.

## Business Outcome
Keep decision-relevant technical SEO evidence current enough to distinguish isolated symptoms, shared root causes, intentional states, and critical sitewide problems.

## Run When
Use for a bounded technical-health check when the user requests it, saved monitoring intent indicates another review would be useful, or a material deployment/site/search change warrants inspection. Any recurring crawling/uptime execution belongs to the active harness/runtime.

## Process
1. [INTEGRATION] Run the crawler/direct checks available to the active harness at a scope proportionate to site size, risk, and the current question.
2. [HYBRID] Inspect uptime/status, redirects, robots/noindex, canonicals, sitemaps, rendering, internal links, structured data, performance, security indicators, and template changes only where relevant.
3. [AI] Group recurring URL symptoms into plausible shared root causes and distinguish observation from causal conclusion.
4. [HYBRID] Compare with known material ChangeEvents/deployments when timing evidence can help explain a condition.
5. [AI] Decide whether a material problem warrants deeper Technical diagnosis, an Incident, an Opportunity, or simply an SEOAssetState/Observation update. Monitoring does not route those methods automatically.
6. [AI] Preserve intentional/accepted states and a future review intent only when forgetting them would cause repeated false alarms; a review date is organizational intent, not a scheduled task.

## Verification
- Claimed technical problems are based on inspected current evidence.
- Root cause and severity remain calibrated to evidence rather than inferred from one symptom.
- AURA does not own uptime polling, crawl scheduling, alert delivery, or automatic remediation.
