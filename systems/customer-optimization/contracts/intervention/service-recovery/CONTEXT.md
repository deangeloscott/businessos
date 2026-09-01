---
id: customer-optimization.intervention.service-recovery
type: playbook
owner_system: customer-optimization
reads:
- CustomerJourney
- Opportunity
- type: Insight
  owner_system: customer-intelligence
- MetricObservation
writes:
- WorkRequest
- ChangeEvent
- Experiment
- MetricObservation
- OutcomeEvaluation
capabilities:
  required:
  - none
  optional:
  - analytics.read
  - product_analytics.read
  - crm.contact.read
  - crm.contact.update
  - crm.opportunity.read
  - checkout.read
  - checkout.update
  - billing.read
  - support.ticket.read
  - customer_success.read
  - scheduling.read
  - email.send
  - workflow.update
  - experiment.run
context:
- EconomicContext
- Offer
subcontracts:
  required:
  - customer-optimization.service-recovery.triage
  - customer-optimization.service-recovery.prevention
---
# Service Recovery

## Purpose
Resolve significant customer failures in a way that restores appropriate value/trust and prevents recurrence.

## Business Outcome
Improve customer progression and value realization through service recovery, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires service recovery to improve a defined customer transition or outcome.

## Process
1. [HYBRID] Determine severity, affected customers, promised vs actual state, immediate harm, and whether an Incident is required.
2. [HUMAN] Stabilize urgent customer impact and establish accountable owner where high-touch judgment is needed.
3. [AI] Reconstruct what happened from system/process/customer evidence without blaming the customer or frontline staff prematurely.
4. [HYBRID] Define remedy proportional to harm/contract/business policy and communicate facts, responsibility, next steps, and timing honestly.
5. [INTEGRATION] Execute operational remediation/refund/credit/workflow actions only with authorization.
6. [HYBRID] Verify customer state and satisfaction/outcome, then route root-cause/process Learning to the correct owner.
