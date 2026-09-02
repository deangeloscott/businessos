---
id: seo.execution.technical.core-web-vitals
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
writes:
- SEOAssetState
- ChangeEvent
- Asset
---
# Core Web Vitals

## Purpose
Improve real-user loading, interaction, and visual stability when it materially affects experience/business outcomes.

## Business Outcome
Improve valuable organic discovery through core web vitals, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Core Web Vitals**, or when an authorized incident response requires it.

## Process
1. [AI] Collect field data where available and lab diagnostics for representative templates.
2. [HYBRID] Segment by page type, device, geography, connection, and template to separate systemic from isolated issues.
3. [HYBRID] Attribute LCP/INP/CLS contributors to specific resources/components/third parties.
4. [HYBRID] Prioritize fixes by user/business impact and template leverage, not score chasing.
5. [AI] Implement with guardrails for functionality, content, analytics, and monetization.
6. [HYBRID] Verify lab regression immediately and define SEO monitoring for field data across its reporting window.


