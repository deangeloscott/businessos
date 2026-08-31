---
id: customer-optimization.checkout.payment-failure
type: playbook
version: 1.3.0
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
capabilities:
  required:
  - analytics.read
  optional:
  - product_analytics.read
  - crm.contact.read
  - crm.opportunity.read
  - checkout.read
  - billing.read
  - support.ticket.read
  - customer_success.read
  - scheduling.read
  - experiment.run
  - workflow.update
  - email.send
context:
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Checkout Payment Failure Diagnosis

## Purpose
Identify and resolve avoidable payment failures without hiding legitimate declines or creating unsafe payment workarounds.

## Business Outcome
Recover qualified purchases and reduce payment frustration while preserving fraud/security/compliance controls.

## Run When
Run when checkout payment failures or retries materially affect purchase completion.

## Process
1. [DETERMINISTIC] Segment failures by processor/status/error, payment method, device, geography, amount/plan, new/returning, retry behavior, and time while respecting sensitive data boundaries.
2. [AI] Distinguish technical integration, validation, authentication, issuer decline, fraud/risk control, customer input, payment-method availability, pricing/term surprise, and unknown causes.
3. [DETERMINISTIC] Compare successful versus failed flows and inspect recent deployment/provider changes.
4. [HYBRID] Do not bypass legitimate fraud/authentication controls or expose restricted payment data.
5. [AI] Design fixes appropriate to cause: clearer error/recovery, retry timing, alternate approved method, technical repair, expectation setting, or human support.
6. [DETERMINISTIC] Verify payment path changes in safe/test environment where possible and monitor failure/recovery/chargeback guardrails.
7. [AI] Publish Journey Insight/Learning for recurring mechanisms.
