---
id: content.intelligence.trend-scan-plan
type: workflow
owner_system: content-synthesis
reads:
- Insight
- Opportunity
- WorkRequest
- ProofRecord
- Asset
- PlatformProfile
writes:
- Asset
- WorkRequest
context:
- Brand
- AudienceSegment
- Objective
- Offer
---
# Content Trend Scan Plan

## Purpose
Define what creator/content signals should be monitored to discover useful creative patterns without chasing every viral item.

## Business Outcome
Focus Content Intelligence on mechanisms relevant to the business’s audiences and communication objectives.

## Run When
Run when establishing or refreshing creator/trend monitoring for a niche, platform, or format.

## Process
1. [AI] Define target audiences, platforms/formats, subject areas, adjacent/non-adjacent inspiration spaces, and decisions the monitoring should improve.
2. [AI] Select creator/account/source sets representing strong relevant execution plus deliberately different niches useful for mechanism transfer.
3. [AI] Define performance signals relative to creator/account baseline, not universal raw-view thresholds.
4. [HYBRID] Identify platform bias, paid amplification, celebrity/brand effects, recency, and other confounders to collect.
5. [DETERMINISTIC] Set cadence, observation window, freshness, deduplication, and sampling rules.
6. [AI] Define which patterns warrant deeper extraction/validation versus simple watchlist status.
7. [DETERMINISTIC] Produce monitoring WorkRequests/schedules and review criteria.
