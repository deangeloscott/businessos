---
id: marketing.ads.angle-matrix
type: playbook
version: 1.4.0
owner_system: marketing-synthesis
risk: medium
autonomy_ceiling: 2
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
- ActionPacket
- WorkRequest
- Asset
capabilities:
  required:
  - none
  optional:
  - creative.text.generate
  - advertising.observe
  - research.web.read
  - tracking.read
  - conversion.read
  - marketing.performance.read
  - experiment.run
  - cms.page.publish
  - email.send
  - social.ad.publish
context:
- Brand
- AudienceSegment
- Offer
- Objective
- EconomicContext
- PreferenceProfile
---
# Advertising Angle Matrix

## Purpose
Generate distinct evidence-backed persuasion hypotheses for an ad campaign rather than cosmetic creative variants.

## Business Outcome
Test materially different reasons a qualified audience may act so performance produces useful marketing learning instead of merely selecting a prettier execution.

## Run When
Run when an advertising campaign requires this persuasion or QA sub-process; media buying/targeting execution remains outside this OS.

## Process
1. [AI] Resolve Customer Insights, Offer, awareness/knowledge state, funnel/journey role, source/channel context, competitor/current-field patterns when available, proof, owned prior performance, and applicable Brand/operator marketing doctrine.
2. [AI] Generate distinct angles from evidence-backed pains/outcomes, motivations, mechanisms, proof, objections, comparisons, triggers, desired gains, loss/risk reduction, certainty/control, speed/effort, financial outcomes, status/identity, or other supported decision drivers—not synonym changes or a forced taxonomy.
3. [AI] State the hypothesis, audience belief/decision barrier, communication job, and expected mechanism each angle is intended to change.
4. [HYBRID] When current external creative patterns inform an angle, separate transferable mechanism from copied expression and distinguish performance proxies (engagement, longevity, prevalence, view counts) from direct business-outcome evidence.
5. [HYBRID] Reject angles that require unsupported claims, fabricated urgency/scarcity, unapproved Offer terms, sensitive-trait exploitation, or acquisition of poor-fit customers.
6. [AI] Match each angle to appropriate proof/creative demonstration, destination message requirement, and placement/context.
7. [DETERMINISTIC] Select a testable subset that maximizes learning under available traffic/budget without inventing traffic/budget assumptions; media buying remains outside Marketing Synthesis.
8. [AI] Produce the angle matrix with expected mechanism, evidence basis/uncertainty, and measurement/guardrail requirements.
