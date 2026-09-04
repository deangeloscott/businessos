---
id: industry.analysis.threat
type: workflow
owner_system: industry-intelligence
reads:
- IndustryEvent
- Observation
- SourceRecord
- Insight
writes:
- IndustryEvent
- Observation
- Insight
- WorkRequest
context:
- AudienceSegment
- Business
- Market
- Objective
- Offer
- ProductService
---
# Threat Analysis

## Purpose
Assess external developments that could damage business outcomes, compliance, customer trust, capability, or market position.

## Business Outcome
Improve the business response to external change through timely, evidence-backed threat analysis.

## Run When
Run when a decision or monitoring signal requires current threat analysis and existing Industry Intelligence is missing, stale, or unresolved.

## Process
1. [AI] Define the threatened business outcome/assets/audiences and causal mechanism.
2. [HYBRID] Estimate probability, impact range, onset, duration, detectability, reversibility, and dependencies.
3. [AI] Identify leading indicators and conditions that would escalate/de-escalate the threat.
4. [HYBRID] Compare current preparedness/capabilities and possible exposure; route true incidents to the appropriate owner.
5. [AI] Identify domain owners capable of prevention, mitigation, communication, or monitoring.
6. [DETERMINISTIC] Publish threat Insight with urgency/confidence and trigger events according to risk policy.
