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
Design an interpretable test of a message, offer presentation, proof approach, creative concept, or persuasion structure and, when actually requested, run it through the active harness.

## Business Outcome
Improve commercial decisions through causal or otherwise defensible evidence rather than treating marketing convention or one winning asset as truth.

## Run When
When an uncertain marketing hypothesis is material enough that a bounded test can improve the decision. An Opportunity or durable handoff may supply context but is not required merely to design an experiment.

## Process
1. [AI] State one primary marketing hypothesis, expected behavioral mechanism, eligible population, and business decision/outcome the test should inform.
2. [HYBRID] Select the smallest meaningful treatment difference; avoid changing multiple major dimensions when causal interpretation matters.
3. [HYBRID] Define assignment/control/baseline or another defensible comparison, sample/window requirements, success metrics, guardrails, stopping rules, and planned segmentation appropriate to the actual setting.
4. [HYBRID] Identify operational, customer, ethical, legal/platform, contamination, and interpretation risks plus recovery/rollback considerations when relevant.
5. [HYBRID] Confirm the needed measurement and implementation evidence is realistically obtainable through the active environment. AURA capability declarations do not prove live availability.
6. [DETERMINISTIC] Persist the Experiment before observing results when durable experiment state will be useful. Link it to the relevant hypothesis, Opportunity/Learning/Asset/evidence as appropriate; do not require an Action object.
7. [INTEGRATION] If running the experiment is inside the user's current request and the active harness has the necessary real capability/access, execute the bounded test through that system. Otherwise return the complete experiment design or create a real durable handoff only when another actor genuinely needs to execute it. Do not create a Manual Action Packet or internal permission object.
8. [HYBRID] Verify implementation state when needed for interpretation and later use observed results through appropriate measurement/OutcomeEvaluation methods rather than treating launch as success.

## Verification
- The test can answer the stated marketing decision at the level of confidence claimed.
- Treatment, comparison, metrics, guardrails, and interpretation limits are explicit.
- User request scope and real external constraints govern execution; AURA does not manufacture authorization.

## Completion Criteria
- A defensible Experiment/design exists and any claimed execution is grounded in actual host state, with no ActionPacket, Manual Action Packet, or mandatory runtime route.
