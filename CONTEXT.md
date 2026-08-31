# ViralTrac AURA — Agent Interface

You are working with **ViralTrac AURA (Agentic Understanding and Reinforcement Architecture)**. AURA gives the active model/harness durable organization-owned memory and reusable operational knowledge. It is not the model, harness, universal orchestrator, permission system, scheduler, or business decision-maker.

## Core behavior

For ordinary organizational work, follow this loop:

1. **Resolve the organization and request.** Identify exactly one active `business_id` for business-specific work and preserve the user's complete requested outcome.
2. **Retrieve what matters.** Load only the relevant durable Business Context, evidence/provenance, preferences/instructions, prior decisions, assets/results, unresolved work, outcomes, and Learning. Reuse current organizational knowledge before asking repeat questions or repeating research.
3. **Choose a method intelligently.** If an AURA SOP is a strong fit, surface/use it. The model/user may choose an AURA SOP, an external Skill, a model-created method, or an ad-hoc method. Do not force work into an AURA contract merely so AURA can record it.
4. **Work normally.** Use the active harness's actual tools, models, subagents, concurrency, permissions, scheduling, retries, and live capabilities. AURA must not downgrade or replace capabilities the host already provides.
5. **Persist material organizational meaning.** Save information when forgetting it would materially hurt future organizational work. Preserve durable facts, evidence, decisions, reusable instructions/preferences, material assets/results, meaningful handoffs, unresolved work, outcomes, and evidence-supported Learning. Do not save hidden reasoning, full transcripts, routine tool calls, temporary calculations, subagent chatter, retries, or transient runtime capability state.
6. **Preserve epistemic truth.** Keep explicit user facts, verified first-party facts, external evidence, derived inference, candidate strategy, and unknown distinct. Never fabricate business facts, claims, tool actions, permissions, outcomes, or evidence. Unknown/not-found is not absent.
7. **Validate what AURA owns.** Persisted state must be schema-valid, provenance-aware, reference-valid, and isolated to the correct business. If an AURA SOP was selected and completion is claimed, also satisfy that SOP's essential process/evidence/QA requirements.
8. **Continue from memory.** Future work should be able to understand what materially happened without needing the original conversation or hidden reasoning.

## Persistence test

Before creating durable AURA state, ask:

> Would a capable future model working for this organization materially benefit from knowing this after the current session/runtime is gone?

Then consider:
- **Durability:** will it matter beyond the immediate operation?
- **Materiality:** would forgetting it reduce future quality, continuity, truth, or efficiency?
- **Uniqueness:** is it new/current organizational meaning rather than transient or redundant information?

If the answer is no, do not persist it merely because a schema or helper exists.

## Canonical records

Use canonical objects for what they actually mean:
- `Business`, `Brand`, `ProductService`, `Offer`, `AudienceSegment`, `Market`, `Objective`, `EconomicContext`, and `BusinessClaim` — durable business context/truth.
- `SourceRecord`, `SourceProfile`, `Observation`, `Insight`, and `ProofRecord` — evidence and interpretation with provenance.
- `DecisionRecord` — a real durable organizational decision. Its absence does **not** mean future action is forbidden.
- `Opportunity` and `Initiative` — optional prioritization/coordination state when useful, not mandatory lifecycle stages.
- `WorkRequest` — a durable real handoff worth remembering, not a mirror of subagents/tools/runtime routing.
- `AttentionItem` — a material condition worth future awareness, deduplicated and lifecycle-managed; AURA owns the meaning, not notification delivery.
- `ChangeEvent` — an optional durable record of a material change when future work benefits from remembering it.
- `VerificationRecord` — optional durable evidence that something was verified when the task/SOP/consequence warrants it.
- `Asset`, measurement objects, `OutcomeEvaluation`, and `Learning` — durable results, measurement, outcomes, and evidence-supported learning.

Do not invent canonical records to satisfy write quotas. Declared SOP writes are possible durable outputs when the work genuinely produces that meaning.

## SOPs and contracts

Contract IDs identify AURA playbooks/services. They are not executable programs and are not mandatory for all work. If an AURA SOP is selected, resolve its contract, read the minimum required context, follow its essential invariants, and use its declared provider-neutral capabilities as method requirements—not as AURA-owned runtime capability truth.

AURA playbook completion/conformance applies only to work actually performed through that playbook. External Skill, model-created, and ad-hoc work may still create truthful organization-owned work receipts and durable results without fabricated contract execution.

## Runs / work receipts

A Run is a bounded organization-owned work receipt for continuity. New Runs explicitly identify the real method type:
- `aura_playbook`
- `external_skill`
- `model_created`
- `ad_hoc`

A Run should retain material evidence/result/decision references, a concise summary, unresolved work, attribution, and timestamps. It must not become a transcript or hidden-reasoning archive. Contract execution/completion manifests exist only for `aura_playbook` Runs.

## Real constraints

Respect the user's request and any actual business, legal, regulatory, platform, account, contractual, or organizational constraints that apply. Those are facts/instructions/decisions external to AURA's authority. AURA does not create generic risk tiers, autonomy ceilings, Approval objects, or ActionPacket permission gates.

A request to analyze does not silently become a request to publish or mutate external state. Likewise, if the user has actually requested execution and the harness has the capability and no real constraint blocks it, AURA should not invent an internal permission ceremony that prevents the work.

## Customer-facing truth

For outward-facing assets, preserve the claim/provenance boundary in `core/policies/context-provenance-and-claims.md`. Do not convert hypotheses, competitor patterns, placeholder copy, or inferred business details into established company claims. Artifact quality/QA, deployment, and measured outcome are separate facts.

## Monitoring

AURA may remember what should be monitored, why, materiality criteria, cadence intent, last meaningful state, and relevant findings. The harness/runtime owns actual scheduling, polling, retries, event delivery, and notification channels. Never claim a schedule is active merely because AURA stores a cadence.

## Product boundary

During ordinary business work, do not modify AURA product source (`core/`, `systems/`, `scripts/`, schemas, tests, manifests) to work around an execution problem. Product changes belong to explicit AURA development/repair work. Preserve `LICENSE.md`, `PUBLISHER.json`, `BRANDING.md`, and required source-available provenance when redistributing/customizing the product.

## Practical entry

- Resolve the active workspace/business with the existing deterministic helpers when useful.
- Use generated navigation/registries to find an AURA SOP when one is useful; do not require the user to choose an internal module or contract before stating their outcome.
- Use `scripts/create_run.py` when a bounded durable work receipt is useful; identify the actual method rather than fabricating a contract.
- Use supported canonical persistence helpers for durable results rather than manually inventing IDs/timestamps/provenance.
- Use `scripts/validate_business.py <business-id>` for organization-owned state integrity after persistence.
- Use AURA SOP-specific completion/finalization only when an AURA SOP was actually selected.

The desired user experience is:

**understand → retrieve → work → remember → continue**

not:

**request → bureaucracy → permission calculation → work**
