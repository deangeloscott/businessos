---
id: marketing.ads.message-match
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
# Ad-to-Destination Message Match

## Purpose
Ensure the destination immediately continues the specific promise and intent created by each ad angle.

## Business Outcome
Reduce wasted qualified traffic caused by ad/landing-page disconnect.

## Run When
Run when an advertising campaign requires this persuasion or QA sub-process; media buying/targeting execution remains outside this OS.

## Process
1. [DETERMINISTIC] Map every active ad angle/copy variant to its intended destination/version.
2. [AI] Compare audience, promise, mechanism, proof, offer, urgency, and CTA expectations between ad and first landing experience.
3. [AI] Identify mismatches likely to create confusion, distrust, or irrelevant traffic.
4. [AI] Decide whether to revise the ad, destination, or create a dedicated variant based on which intent should remain canonical.
5. [HYBRID] Reject bait-and-switch where the high-performing ad promise cannot be honestly fulfilled.
6. [DETERMINISTIC] Link ad→destination versions and tracking IDs.
7. [DETERMINISTIC] Include message-match in launch QA and performance diagnosis.
