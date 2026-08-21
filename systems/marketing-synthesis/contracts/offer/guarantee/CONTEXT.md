---
id: marketing.offer.guarantee
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
# Offer Guarantee Design

## Purpose
Turn validated risk-reversal strategy into precise proposed guarantee terms the business can actually administer.

## Business Outcome
Create a clear customer assurance with enforceable conditions and measurable business risk.

## Run When
Run after guarantee/risk-reversal analysis identifies a viable Offer change.

## Process
1. [AI] State the customer risk being reversed and the exact business-controlled promise.
2. [DETERMINISTIC] Define eligibility, customer obligations, covered outcome/milestone, evidence required, timeframe, remedy, exclusions, request process, and business owner.
3. [HYBRID] Test edge cases, ambiguity, abuse potential, legal/compliance, delivery variability, and operational ability to adjudicate consistently.
4. [AI] Rewrite conditions in plain language that does not negate the headline promise through hidden complexity.
5. [DETERMINISTIC] Model worst-case/expected economic exposure and required tracking.
6. [AI] Define how the guarantee should be presented without implying broader certainty than its terms.
7. [DETERMINISTIC] Submit proposed guarantee through ContextUpdateProposal and approval before any marketing use.
