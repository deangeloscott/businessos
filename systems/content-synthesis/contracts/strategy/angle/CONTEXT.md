---
id: content.strategy.angle
type: playbook
version: 1.1.0
owner_system: content-synthesis
risk: low
autonomy_ceiling: 4
reads:
- Opportunity
- WorkRequest
- Insight
- Learning
- Asset
writes:
- ActionPacket
- Asset
capabilities:
  required:
  - none
  optional:
  - analytics.read
  - social.observe
context:
- AudienceSegment
- Brand
---
# Angle Development

## Purpose
Find the most useful/interesting truthful framing of an idea for the defined audience and objective.

## Business Outcome
Create or improve angle development so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Run when an Opportunity or WorkRequest requires angle development and existing Assets do not already satisfy the communication need.

## Process
1. [AI] Identify the core Insight/fact and the audience job, awareness, prior knowledge, stakes, and consumption context.
2. [AI] Generate materially different angle families: explanatory, contrarian-with-evidence, story/case, comparison, problem-solution, framework, experiment/data, behind-the-scenes, timely implication, or other context-fit frame.
3. [HYBRID] Reject angles that depend on unsupported claims, false novelty, manipulative tension, or brand/compliance violations.
4. [AI] Evaluate each on relevance, differentiation, clarity, evidence availability, platform fit, likely attention, and ability to deliver actual value.
5. [HYBRID] Choose the angle that best serves objective/audience rather than the most sensational hook.
6. [AI] Specify promise, takeaway, evidence needed, exclusions, and likely CTA/content action.
