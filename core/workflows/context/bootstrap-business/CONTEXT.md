---
id: core.context.bootstrap-business
type: workflow
owner_system: core
reads: []
writes:
- Business
- Brand
- PreferenceProfile
- ProductService
- Offer
- AudienceSegment
- Market
- Objective
- SourceRecord
- Observation
- ContextUpdateProposal
context: []
workflows:
  conditional:
  - id: core.context.owned-business-discovery
    when: Additional first-party/owned-surface discovery can materially improve the current work or the user asks AURA to map the business more broadly.
---
# Bootstrap Business Context

## Purpose
Establish the smallest useful, truthful organization context from explicit user/first-party evidence without turning onboarding into a prerequisite workflow.

## Business Outcome
Let a new AURA workspace begin useful work from minimal identity while preserving evidence, uncertainty, and reusable context that future work genuinely needs.

## Run When
Use when initializing a new organization or deliberately rebuilding/enriching its base context from authoritative sources.

## Process
1. [HYBRID] Resolve the organization identity and preserve the user's exact supplied statements/files. If the instance does not exist, initialize it with `scripts/init_business.py`; the organization name alone is sufficient canonical Business identity. Use `scripts/bootstrap_explicit_context.py` when explicit user/first-party facts should become durable context. Explicit Brand guidance belongs in Brand; reusable work/expression preferences belong in PreferenceProfile; one-task constraints remain with the current request.
2. [AI] Decide what additional first-party context, if any, would materially improve the user's current request or future reuse. Do **not** require broad onboarding merely because more fields or playbooks exist. `core.data.query-business-truth` or `core.context.owned-business-discovery` may be useful methods when the active harness has appropriate authoritative sources or owned-surface anchors; they are optional, not bootstrap gates.
3. [AI] Structure only meaning supported by the supplied/inspected source material into Business, Brand, ProductService, Offer, AudienceSegment, Market, Objective, or other appropriate context. Keep observation, inference, candidate strategy, public perception, contradiction/staleness, and unknown distinct. Omit unknown fields rather than inventing geography, pricing, margins, KPIs, audiences, offers, promises, positioning, targets, or performance.
4. [AI] Ask only for an unresolved fact that could materially change the requested result, business truth, actual constraint, economics, Brand meaning, or consequential business decision and cannot be safely resolved from available authoritative context. Reuse durable answers instead of asking them again.
5. [HYBRID] Persist context only at the scope/authority actually established. Use a `ContextUpdateProposal` only when an unresolved candidate change to existing durable context is itself worth remembering; do not create proposals as routine onboarding paperwork or as permission tokens.
6. [DETERMINISTIC] Validate schema, business isolation, exact references/IDs, and source provenance with `scripts/validate_business.py <business-id> --require-context`. Deterministic AURA validates mechanics; it does not reinterpret natural-language business meaning.
7. [AI] Return a concise view of what is established, provisional, contradictory, or unknown when useful, then continue the user's original request normally. The active model/user chooses whatever method is best next; bootstrap does not route residual work into a named AURA playbook, create a Run, or stop the user at an internal module menu.

## Verification
- The organization has at least a truthful canonical Business identity and any additional durable context actually established by evidence.
- No broad discovery, PreferenceProfile, Run, ContextUpdateProposal, or downstream playbook was required merely to complete initialization.
- Unknown/not-found state was not converted into absence or invented business truth.
