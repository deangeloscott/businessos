---
id: marketing.ads.message-match
type: workflow
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
- Asset
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
Use when an advertising campaign needs ad-to-destination continuity checked or designed; media buying/targeting execution remains outside this method unless separately available and requested.

## Process
1. [HYBRID] Map every relevant ad angle/copy variant to its intended destination/version using the available campaign and Asset context.
2. [AI] Compare audience, promise, mechanism, proof, Offer, urgency, and CTA expectations between ad and first landing experience.
3. [AI] Identify mismatches likely to create confusion, distrust, or irrelevant traffic.
4. [AI] Decide whether to revise the ad, destination, or create a dedicated variant based on which intent should remain truthful and useful.
5. [HYBRID] Reject bait-and-switch where the high-performing ad promise cannot be honestly fulfilled.
6. [HYBRID] Preserve ad-to-destination relationships, useful variant/version references, and tracking identifiers in the relevant Asset/strategy state when future work benefits from them.
7. [AI] Include message match in launch QA and performance diagnosis as useful operating knowledge. Do not create a WorkRequest merely to move between ad and landing-page methods.
