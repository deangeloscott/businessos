# Context Provenance & Business Claim Policy

AURA must distinguish **what the organization actually established** from useful strategy or language a model derived. Models may synthesize strategy freely; they may not relabel their own synthesis as organization truth.

## Authority classes

- `explicit_user` — directly grounded in an authoritative user statement through preserved source/provenance.
- `verified_first_party` — established by a reliable first-party source.
- `external_evidence` — observed outside the active business; not an active-business fact by itself.
- `derived_inference` — a reasoned interpretation of known facts/evidence.
- `candidate_strategy` — a proposed positioning, audience, offer, message, tactic, or operating choice not yet adopted as business truth.
- `unknown` — not established.

These labels preserve organizational epistemic state. They are not a permission system or substitute for model judgment.

## Explicit business claims

`BusinessClaim` is canonical organizational memory for reusable customer-facing claims, promises, constraints, and prohibitions that need to remain safe across future work.

For conversational setup, `bootstrap_explicit_context.py` may persist:
- `approved_claims`: exact or conservative statements the organization authorizes as true/promisable;
- `claim_constraints`: explicit constraints, prohibitions, or established absence statements.

Preserve the source that established explicit claims. Do not hand-author a model claim and stamp it `explicit_user` afterward.

## Derived context

Agent-created Brand, AudienceSegment, Offer, positioning, messaging, and similar strategic objects are normally `derived_inference` or `candidate_strategy`, even when their basis includes explicit facts. Their lineage may point to BusinessClaim, Business, Market, ProductService, Objective, research, outcomes, or other relevant canonical evidence.

Example:
- User: “We provide written estimates.” → approved `BusinessClaim`.
- Model: “Transparency should be the core positioning.” → `candidate_strategy` unless the organization adopts it as something stronger.

## Claim expansion boundary

Creative copy may restate a supported claim but should not silently enlarge it into a new commitment.

Approved: “We provide written estimates.” may support “Request a written estimate.” It does not automatically establish “We provide separate written repair and replacement estimates for both options.”

Quantifiers, guarantees, availability, timing, price, discounts, financing, warranties, certifications, comparative/superlative language, and process commitments deserve particular care when they materially enlarge the business promise. The capable model/user should judge whether the current organization truth actually supports the intended claim.

AURA should not attempt to make this semantic decision through stemming, token overlap, regex phrase lists, or other deterministic language rules.

## Optional claim-review metadata

For important customer-facing Content/Marketing Assets, a model/human may preserve an `extensions.businessos.claim_manifest` when doing so improves auditability, collaboration, or future reuse. It is optional organizational metadata, not required conformance paperwork.

When a manifest is used:
- `approved_business_claim` entries should reference trusted organization truth through `support_refs`;
- `general_guidance` may identify language that does not purport to establish an active-business fact;
- `placeholder` may identify deliberately unresolved copy or proof.

Deterministic validation may check that declared support references exist and are trusted. It must not decide whether the natural-language predicate is substantively equivalent to those sources. That semantic grounding belongs to the active model/user.

For opaque/rendered media, a compact claim-surface sidecar can be useful when future work needs a text representation of visible/spoken/material claims and the actual artifact is inconvenient to inspect. It is optional and never proof that it matches the final render; substantive QA should inspect the real artifact when the consequence warrants it.

`scripts/build_claim_manifest.py` is only a review aid. Its candidate surfacing does not classify truth, authorize wording, or override model judgment.

## Customer-facing status

`customer_facing` describes intended audience/use, not publication status: an unpublished homepage, landing page, email, ad, proposal, webinar, or similar outward draft is still customer-facing.

Set `extensions.businessos.customer_facing: false` only for genuinely internal support Assets such as research, analysis, strategy, planning, or an internal brief.

## Run provenance is optional

A valid customer-facing Asset does **not** require a Run, AURA Playbook/Workflow, claim manifest, or execution ledger. Capable humans/models may create valid work directly.

When an Asset is linked to a Run, that receipt should describe the method and material results truthfully. Naming an AURA Playbook or Workflow means it materially framed the work; the receipt is not a conformance certificate or execution authority. External Skill, model-created, and ad-hoc work remain legitimate and must not fabricate AURA provenance.

`origin: imported` or `origin: preexisting` describes where an Asset came from. It does not forbid AURA from later linking real work performed on that Asset to a truthful work receipt.

## Existing customer-facing surfaces

Editing an existing outward surface is not a loophole for unsupported claims. The same active-business truth boundary applies whether work creates, removes, or edits copy.

AURA does **not** require a universal pre-edit snapshot, mutation manifest, ChangeEvent, or verification ceremony. Preserve before/after evidence, a material ChangeEvent, or a VerificationRecord only when doing so genuinely improves organizational truth, troubleshooting, measurement, or continuity. Runtime/tool mechanics belong to the active harness.
