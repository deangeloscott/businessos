---
id: content.production.case-study
type: workflow
owner_system: content-synthesis
reads:
- Insight
- Opportunity
- WorkRequest
- ProofRecord
- Asset
- PlatformProfile
writes:
- Asset
context:
- Brand
- AudienceSegment
- Objective
- Offer
---
# Customer Case Study

## Purpose
Turn verified customer evidence and ProofRecords into a useful, accurate account of context, intervention, mechanism, and outcome.

## Business Outcome
Create credible proof and education without exaggerating attribution or exposing customer information beyond permission.

## Run When
Use when sufficient verified customer proof exists for a case study or success story.

## Process
1. [DETERMINISTIC] Resolve ProofRecords, permission/usage restrictions, customer/account context, relevant product/service, and primary SourceRecords.
2. [AI] Define audience question and select the case only if it is relevant/representative enough for that communication job.
3. [AI] Structure starting situation → constraints/problem → decision/process → what was actually done → observed outcome → mechanism/lesson → limitations.
4. [AI] Separate measured results from customer attribution and business interpretation; preserve timeframe/baseline/conditions.
5. [HYBRID] Remove confidential/sensitive identifiers and obtain any actually required customer/organizational permission for naming, logos, quotes, screenshots, or results.
6. [AI] Include concrete evidence/examples and avoid unsupported “because of us” causal language.
7. [DETERMINISTIC] Preserve the useful Asset with linked ProofRecord/source lineage and claim mapping. Derivative-production or QA methods may be used when they materially improve the final use; they are not required internal handoffs.
