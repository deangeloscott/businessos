---
id: marketing.intake.persuasion-brief
type: workflow
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
writes:
- Asset
context:
- Brand
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Persuasion Brief

## Purpose
Define the persuasion problem precisely enough that a capable model can create strong marketing work without rediscovering the audience, offer, barriers, proof, and commercial context.

## Business Outcome
Improve marketing quality and consistency by carrying forward the evidence and constraints that materially shape persuasion while leaving creative execution and method choice flexible.

## Run When
Use before material persuasion/marketing production when the current task lacks a sufficiently clear, current persuasion problem definition. An Opportunity may provide context but is not required merely to create a useful brief.

## Process
1. [HYBRID] Reuse the relevant Offer, AudienceSegment, Brand context, Objectives/economics, Customer/Competitor Insights, ProofRecords, current Assets, acquisition/prior-touch context, and any existing useful brief. Load only what can materially change the work.
2. [AI] State the exact desired commercial action and the persuasion barrier preventing the right person from taking it.
3. [AI] Define audience awareness/sophistication, current beliefs, desired outcome, decision criteria, objections, alternatives, proof needs, and message continuity from the prior touchpoint at the confidence the evidence supports.
4. [AI] Separate persuasion problems from journey friction, product/service failure, missing customer knowledge, or sales/operational issues. Surface the real issue rather than masking it with copy; another domain method may be useful, but no internal routing object is required.
5. [HYBRID] Identify material claim/evidence, legal/compliance, offer-term, price/guarantee, brand, customer-quality, channel, and real organizational constraints. Do not invent a generic approval requirement.
6. [AI] Define the asset/campaign job, must-preserve facts/proof, desired action, success/guardrail measurements, and testable uncertainty only where they improve the actual work.
7. [AI] Produce a concise persuasion brief that references durable evidence rather than duplicating upstream research. Persist it as an internal organization-owned `Asset` only when future sessions/actors materially benefit; otherwise use it directly in the current task.
8. [AI] If a real cross-person/model/session handoff must survive the current runtime, preserve that separately through `core.continuity.manage-handoff`. This playbook does not create a WorkRequest merely to pass context to another AURA playbook.

## Verification
- Customer beliefs/motivations are evidence-calibrated rather than inferred from conversion response alone.
- Company claims, offer terms, proof, pricing, guarantees, and constraints remain grounded in current organizational truth.
- The brief is specific enough to improve production without prescribing unnecessary creative choices.
- No generic approval, routing, return-contract, or WorkRequest lifecycle is required.

## Completion Criteria
- A capable model can produce the intended marketing asset/campaign without reconstructing the persuasion problem, and any persisted brief is useful organizational knowledge rather than internal delegation state.
