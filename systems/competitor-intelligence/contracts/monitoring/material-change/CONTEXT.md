---
id: competitor.monitoring.material-change
type: playbook
version: 1.1.0
owner_system: competitor-intelligence
reads:
- Competitor
- SourceRecord
- Observation
writes:
- Competitor
- SourceRecord
- Observation
- Insight
capabilities:
  required:
  - webpage.snapshot
  - webpage.compare
  optional:
  - research.web.read
  - advertising.observe
  - social.observe
events:
  consumes:
  - none
  emits:
  - competitor.insight.updated
schedule:
  class: recurring
  default: daily
  configurable: true
context:
- Objective
---
# Competitor Material-Change Monitoring

## Purpose
Detect decision-relevant competitor changes with snapshot comparison and semantic review.

## Business Outcome
Improve competitive decisions through evidence-backed competitor material-change monitoring, without mistaking observed activity for proven effectiveness.

## Run When
Run when a decision requires current competitor material-change monitoring and canonical competitor intelligence is missing, stale, contradictory, or insufficiently specific.

## Process
1. [DETERMINISTIC] Refresh prioritized competitor sources at configured cadence and compare snapshots/hashes/state.
2. [DETERMINISTIC] Suppress unchanged/boilerplate/personalization noise using structural and content comparison.
3. [AI] Classify changed content into pricing, packaging, product, offer, positioning, messaging, funnel, campaign, partnership, or other strategic class.
4. [HYBRID] Assess materiality against active Objectives/markets/audiences and existing competitor state.
5. [AI] Determine whether the change updates a factual Competitor field, creates an Observation only, or warrants a new/updated Insight.
6. [DETERMINISTIC] Persist material changes and emit competitor.updated/insight.updated.
