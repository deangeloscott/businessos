---
id: content.opportunity.independent-content
type: workflow
owner_system: content-synthesis
reads:
- Insight
- Asset
- MetricObservation
- Opportunity
writes:
- Opportunity
context:
- AudienceSegment
- Objective
---
# Independent Content Opportunity

## Purpose
Identify when communication itself is a valuable business intervention rather than delegated production.

## Business Outcome
Create or improve independent content opportunity so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Run when an Opportunity or WorkRequest requires independent content opportunity and existing Assets do not already satisfy the communication need.

## Process
1. [AI] Start from Business Objectives, audience information needs, active Insights, existing Assets, and observed content/platform performance.
2. [AI] Define the unmet communication job and why solving it could create business value independent of another domain Opportunity.
3. [HYBRID] Check for an existing Opportunity and distinguish content opportunity from SEO, persuasion, or customer-journey problems.
4. [AI] Identify likely audience, desired content action, platform/context, format candidates, and differentiation/evidence needs.
5. [HYBRID] Estimate value, confidence, urgency, leverage, production cost, and dependencies.
6. [DETERMINISTIC] Create/update one Content Opportunity and route to strategy when qualified.
