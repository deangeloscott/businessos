---
id: marketing.vsl.persuasion-architecture
type: playbook
version: 1.3.0
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
---
# VSL Persuasion Architecture

## Purpose
Design the ordered belief progression that moves a qualified viewer from current understanding to the Offer and action.

## Business Outcome
Create a VSL whose length and sequence are driven by the persuasion problem rather than a stock script formula.

## Run When
Run before scripting a VSL.

## Process
1. [AI] Define viewer starting state, source context, desired action, Offer, mechanism, objections, proof needs, and decision risk.
2. [AI] Identify the beliefs/questions that must change in order and distinguish prerequisites from optional detail.
3. [AI] Structure hook/context → problem/outcome → mechanism/insight → solution/Offer fit → proof/demo → objections/risk → terms/CTA, changing order when audience evidence requires it.
4. [AI] Decide where demonstrations/stories/examples are better than explanation and where the Offer should first be introduced.
5. [HYBRID] Remove manufactured drama, false problem inflation, or withholding of decision-critical Offer facts.
6. [AI] Define expected duration by content required, not an arbitrary target.
7. [DETERMINISTIC] Produce beat architecture with proof/visual requirements.
