---
id: competitor.analysis.funnel-capture
type: workflow
owner_system: competitor-intelligence
reads:
- Competitor
- SourceRecord
- Observation
- Insight
writes:
- Observation
- Insight
context:
- Business
- Market
- AudienceSegment
- Offer
---
# Competitor Funnel Capture

## Purpose
Experience and document the legitimately observable path a prospect can take through a competitor acquisition flow.

## Business Outcome
Create comparable funnel evidence from actual observable interactions without deceptive research or unsupported assumptions about private performance.

## Run When
Run when a priority competitor funnel must be understood or refreshed.

## Process
1. [AI] Define the public/consented entry points, customer scenario, research depth, and the specific funnel questions that matter to the business decision.
2. [INTEGRATION] Discover and traverse relevant entry paths such as ads/search/social/profile/site, then interact through landing pages, buttons, dynamic steps, forms, lead magnets, booking/demo/trial/checkout, and onboarding previews where legitimately accessible. Use crawl/site discovery to find material paths when warranted.
3. [HYBRID] Before submitting identity/contact/business information, follow `core/policies/external-research-interaction.md` and resolve the effective profile with `scripts/resolve_research_profile.py`. Reuse truthful authorized values already known; if the user supplies a durable missing value, persist it at the correct scope instead of asking again next time. Never invent identity/company/purchase facts merely to unlock the next step.
4. [INTEGRATION] Where legitimately subscribed/registered and authorized, capture follow-up received in the permitted research mailbox plus visible terms and downstream redirects. Do not infer messages or private steps not actually observed.
5. [DETERMINISTIC] Preserve sequence, URLs/assets, timestamps, screenshots/snapshots, submitted field names/authorized values where appropriate, branching conditions, required fields, approvals, and access boundaries.
6. [AI] Record observable persuasion, proof, friction, qualification, handoff mechanics, and unresolved branches without inferring conversion rates or private performance.
7. [HYBRID] Stop at unauthorized/private/restricted areas, prohibited scraping, impersonation, deceptive transactions, or approval-gated actions not approved; mark the downstream state unknown/blocked rather than bypassing the boundary.
8. [DETERMINISTIC] Save a dated funnel Observation set suitable for comparison, including which branches were observed, partial, blocked, or not relevant.

## Verification
A reviewer can reproduce the legitimate observed path, distinguish interaction from inference, and see exactly where truthful/authorized research stopped.
