---
id: marketing.experimentation.message-test
type: playbook
owner_system: marketing-synthesis
reads:
- Opportunity
- MetricDefinition
- Learning
- Asset
writes:
- Experiment
capabilities:
  required:
  - none
  optional:
  - experiment.run
  - marketing.performance.read
  - conversion.read
---
# Marketing Experiment Design

## Purpose
Design interpretable tests of messages, offers, proof, creative concepts, or persuasion structures.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed marketing experiment design that matches audience awareness, offer, proof, and acquisition context.

## Run When
Run when an Opportunity or WorkRequest requires marketing experiment design to remove a commercial persuasion gap or create the required conversion asset.

## Process
1. [AI] State one primary marketing hypothesis, expected behavioral mechanism, target population, and business outcome.
2. [HYBRID] Select the smallest meaningful treatment difference; avoid changing multiple major dimensions when causal interpretation matters.
3. [DETERMINISTIC] Define assignment/control/baseline, sample/window requirements, success metrics, guardrails, stopping rules, and segmentation before launch.
4. [HYBRID] Check operational/ethical/compliance risks and whether audience exposure is appropriate.
5. [DETERMINISTIC] Validate tracking and experiment implementation capability.
6. [INTEGRATION] Launch when authorized or create a Manual Action Packet.
7. [DETERMINISTIC] Persist Experiment linked to Opportunity/Actions.
