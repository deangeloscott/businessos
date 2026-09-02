---
id: marketing.social.profile-optimization
type: workflow
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
- WorkRequest
- Asset
context:
- Brand
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Conversion-Oriented Social Profile Optimization

## Purpose
Implement an evidence-backed social profile that converts qualified profile interest into the intended next action.

## Business Outcome
Create a coherent profile surface where identity, bio, proof, pinned content, and destination work together.

## Run When
Run after a social profile audit identifies a material persuasion opportunity.

## Process
1. [AI] Define the profile’s one primary audience/value/CTA path and required variants only if the account truly serves incompatible audiences.
2. [AI] Draft display-name/bio/value proposition/CTA/link language within platform constraints and evidence.
3. [AI] Select eligible ProofRecords and pinned/featured content that establish the most important belief before action.
4. [HYBRID] Define profile-picture/banner/cover creative requirements and delegate production to Content rather than inventing generic visuals locally.
5. [DETERMINISTIC] Validate links, tracking, profile fields, permission/approval, and destination message match.
6. [INTEGRATION] Apply changes where authorized or create exact Manual Action; capture before/after ChangeEvent.
7. [DETERMINISTIC] Verify the live profile and measure profile→destination/action conversion over an appropriate window.
