---
id: customer-optimization.service-recovery.prevention
type: workflow
owner_system: customer-optimization
reads:
- CustomerJourney
- Observation
- Insight
- Opportunity
- MetricObservation
- Experiment
writes:
- Observation
- Insight
- Opportunity
context:
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Service Failure Prevention Review

## Purpose
Turn recurring or material service recovery cases into systemic journey/process improvements.

## Business Outcome
Reduce recurrence rather than repeatedly handling the same customer failure case-by-case.

## Run When
Run after a material recovery is stabilized or when similar incidents/complaints recur.

## Process
1. [DETERMINISTIC] Aggregate linked recovery cases, incidents, process state, affected journey transition, recent changes, and recurrence pattern.
2. [AI] Identify primary/contributing system/process/ownership/product/communication causes and escape points where the issue should have been prevented/detected.
3. [AI] Distinguish one-off execution error from structural process/design weakness.
4. [AI] Design prevention/detection changes beginning upstream of the customer-facing failure.
5. [HYBRID] Identify the real product/engineering/sales/finance/legal/operations owner when those functions must act, and use relevant operating knowledge/expertise directly rather than routing work through an AURA domain.
6. [DETERMINISTIC] Define the corrective change, verification method, recurrence metric, and monitoring intent. The real system/harness owns implementation and any recurring monitoring loop.
7. [AI] When post-change evidence becomes available, evaluate recurrence and preserve Learning only when the evidence supports a reusable lesson.
