---
id: customer-optimization.intervention.service-recovery
type: workflow
owner_system: customer-optimization
reads:
- CustomerJourney
- Opportunity
- type: Insight
  owner_system: customer-intelligence
- MetricObservation
writes: []
context:
- EconomicContext
- Offer
workflows:
  required:
  - customer-optimization.service-recovery.triage
  - customer-optimization.service-recovery.prevention
---
# Service Recovery

## Purpose
Resolve significant customer failures in a way that restores appropriate value/trust and reduces recurrence.

## Business Outcome
Recover from real service failures proportionately and learn from the underlying mechanism without turning AURA into an incident/authorization runtime.

## Run When
Use when a material customer failure, broken promise, support/service breakdown, or recovery need requires coordinated understanding and response. An Opportunity may provide context but is not required.

## Process
1. [HYBRID] Determine severity, affected customers, promised versus actual state, immediate harm, and whether a separate real Incident meaning is worth preserving.
2. [HUMAN] Stabilize urgent customer impact and establish a real accountable organizational owner when high-touch judgment/action is needed; do not confuse this with an AURA semantic owner.
3. [AI] Reconstruct what happened from system/process/customer evidence without blaming the customer or frontline staff prematurely.
4. [HYBRID] Define a remedy proportional to harm, contract, business policy, and actual constraints; communicate facts, responsibility, next steps, and timing honestly.
5. [HYBRID] If remediation/refund/credit/workflow/customer communication is within the user's request and the host has real capability/permission, execute it through the external systems. Otherwise provide the precise action/handoff needed; use a WorkRequest only if that real durable handoff must survive the current interaction.
6. [HYBRID] Verify the customer's resulting state/outcome when practical and identify the root cause/prevention improvement. Use relevant operating knowledge directly rather than routing Learning to an internal owner.
7. [AI] Preserve only durable meaning future work needs: for example the material Incident/ChangeEvent, customer evidence, updated process, outcome, or Learning. Do not create Experiment/Metric/Outcome objects merely because service recovery occurred.

## Verification
- Remedy and communication reflect what actually happened and what the organization can truly provide.
- External remediation is not claimed unless it was actually executed/observed.
- Prevention Learning is evidence-supported and scoped to this organization.
- No generic approval or lifecycle bundle is required.

## Completion Criteria
- The customer failure has an evidence-backed recovery response and, where possible, a prevention path, with actual execution/outcome state represented truthfully.
