---
id: marketing.assets.sales-letter
type: workflow
owner_system: marketing-synthesis
reads:
- Opportunity
- type: Insight
  owner_system: customer-intelligence
- type: Insight
  owner_system: competitor-intelligence
- Asset
- WorkRequest
- ProofRecord
writes:
- Asset
context:
- AudienceSegment
- Brand
- Offer
---
# Sales Letter

## Purpose
Create long-form written persuasion appropriate to audience sophistication and Offer complexity.

## Business Outcome
Increase the likelihood of the desired commercial action through an evidence-backed sales letter that matches audience awareness, Offer, proof, and acquisition context.

## Run When
Use when a sales letter is useful to remove a commercial persuasion gap or create the required conversion asset. An Opportunity or real durable WorkRequest may provide context but is not required.

## Process
1. Define audience/awareness/intent, Offer, problem/outcome, objections, proof, and desired action.
2. Choose argument architecture appropriate to market sophistication rather than formulaically applying one copy template.
3. Draft with concrete claims, evidence, examples, transition logic, objections, value, terms, risk, and CTA.
4. Audit every major promise against proof and canonical Offer/Brand constraints.
5. Remove inflated language, redundant persuasion, and pressure unsupported by customer reality.
6. Test message continuity and readability. Use relevant Content operating knowledge and the active harness's real document/design capabilities directly when production beyond text is needed; persist a WorkRequest only for a real durable organizational handoff.

## Proportionate Scope
Match length, proof depth, objection handling, examples, and production detail to the buyer's awareness, Offer complexity, stakes, and evidence. Long-form is justified by the decision work required, not by the format name.

## Verification
- Major claims and Offer terms remain grounded in current truth/evidence.
- Length and persuasion depth are justified by the decision rather than a copy formula.
- A WorkRequest is reserved for a real durable handoff, not internal continuation.
