---
id: seo.execution.aeo.competitive-answer-share
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- Observation
writes:
- SEOAssetState
- ChangeEvent
- Asset
evidence_inputs:
- prompt/question observations, answer text, citations, mentions, and competing sources
---
# Competitive Answer Share

## Purpose
Measure relative brand/competitor representation across a controlled prompt universe.

## Business Outcome
Improve valuable organic discovery through competitive answer share, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Competitive Answer Share**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Define the measurement universe and weighting by prompt business value so low-value questions do not dominate the score.
2. [AI] Classify each observation for owned brand mention, recommendation, citation, link, rank/order/group where meaningful, and competitor equivalents.
3. [DETERMINISTIC] Calculate separate interpretable metrics for mention share, recommendation share, citation share, prompt coverage, and high-value prompt coverage.
4. [HYBRID] Segment by intent, awareness stage, topic, market, and surface.
5. [HYBRID] Inspect large changes for prompt-universe drift or sampling changes before attributing them to optimization.
6. [AI] Generate Opportunities from important competitive gaps with the underlying observations attached.


