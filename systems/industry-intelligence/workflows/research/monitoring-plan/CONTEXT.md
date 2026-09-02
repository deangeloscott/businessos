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
Define what external developments matter, where to monitor them, and how quickly they must be surfaced.

## Business Outcome
Focus monitoring on changes capable of altering a business decision instead of maximizing news volume.

## Run When
Run when onboarding a business/market, priorities change, or monitoring produces too much noise or misses important events.

## Process
1. [AI] Map Objectives, Markets, Products/Services, Offers, customer dependencies, compliance exposure, and known strategic risks to event classes that could matter.
2. [AI] Define monitored themes/entities, authoritative source classes, geographic scope, languages, and expected change velocity.
3. [AI] Set materiality cues and escalation thresholds for regulation, technology, research, economics, culture, category, supply, platform, and major company activity.
4. [HYBRID] Separate must-monitor authoritative sources from broad discovery sources and social early signals.
5. [DETERMINISTIC] Define cadence, freshness targets, dedup window, source health checks, and event follow-up rules.
6. [AI] Identify blind spots and low-value monitoring that should be removed.
7. [DETERMINISTIC] Produce monitoring work/schedules and review the plan when business context changes.
