---
id: industry.research.monitoring-plan
type: workflow
owner_system: industry-intelligence
reads:
- IndustryEvent
- SourceRecord
- Observation
- Insight
writes:
- IndustryEvent
- Observation
- Insight
context:
- Business
- Market
- Objective
---
# Industry Monitoring Plan

## Purpose
Define which external developments are worth revisiting, which evidence surfaces matter, and how freshness or future conditions should affect later review without making AURA the scheduler.

## Business Outcome
Focus organizational attention on changes capable of altering a business decision instead of maximizing news volume or creating a permanent monitoring machine.

## Run When
Use when onboarding a business/market, priorities change, existing monitoring knowledge produces too much noise or misses important developments, or a current decision needs a clearer external-watch strategy.

## Process
1. [AI] Map Objectives, Markets, Products/Services, Offers, customer dependencies, compliance exposure, and known strategic risks to external event/change classes that could materially change a decision.
2. [AI] Define the monitored themes/entities, authoritative source classes, discovery surfaces, geographic scope, languages, and expected change velocity that matter for those decisions.
3. [AI] Define materiality cues and the kinds of change that warrant renewed attention for regulation, technology, research, economics, culture, category, supply, platforms, and major company activity. Avoid generic urgency scores or automatic escalation rules.
4. [HYBRID] Separate authoritative sources that establish facts from broad discovery sources and social early signals; preserve source-quality knowledge when it will improve future retrieval or verification.
5. [HYBRID] Decide how fresh evidence needs to be and what future date, event, threshold, unresolved question, or change condition would make another review useful. Cadence may be a convenient expression of review intent, but it is not proof that a recurring job exists.
6. [AI] Remove low-value watch areas, duplicated sources, and monitoring that cannot plausibly change a decision; identify important blind spots and the evidence needed to close them.
7. [HYBRID] Preserve the useful monitoring intent, source knowledge, checkpoints, and material future conditions in AURA. The active harness/runtime owns any real timer, recurring search, notification, or scheduled task and may use this knowledge when configuring those mechanisms.

## Verification
- Every watch area is tied to a plausible decision consequence rather than general curiosity.
- Authoritative evidence, discovery signals, and social prevalence remain distinct.
- Freshness/recheck intent is explicit without claiming that AURA owns or has created a schedule.
- Low-value monitoring is removed rather than retained for completeness.

## Completion Criteria
- Future models can tell what external change matters, where to look, how current the evidence must be, and what would justify another review, while the host remains responsible for any actual recurrence or notification.
