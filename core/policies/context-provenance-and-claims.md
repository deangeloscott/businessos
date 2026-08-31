# Context Provenance & Business Claim Policy

AURA must distinguish **what the organization actually established** from useful strategy or language a model derived. Models may synthesize strategy freely; they may not relabel their own synthesis as organization truth.

## Authority classes

- `explicit_user` — directly grounded in an authoritative user statement through the supported deterministic grounding path.
- `verified_first_party` — established by a reliable first-party source.
- `external_evidence` — observed outside the active business; not an active-business fact by itself.
- `derived_inference` — a reasoned interpretation of known facts/evidence.
- `candidate_strategy` — a proposed positioning, audience, offer, message, tactic, or operating choice not yet adopted as business truth.
- `unknown` — not established.

## Explicit business claims

`BusinessClaim` is canonical organizational memory for reusable customer-facing claims, promises, constraints, and prohibitions that need to remain safe across future work.

For conversational setup, `bootstrap_explicit_context.py` may persist:
- `approved_claims`: exact or conservative statements the organization authorizes as true/promisable;
- `claim_constraints`: explicit constraints, prohibitions, or established absence statements.

The deterministic helper grounds them to the verbatim source. Do not hand-author a model claim and stamp it `explicit_user` afterward.

## Derived context

Agent-created Brand, AudienceSegment, Offer, positioning, messaging, and similar strategic objects are normally `derived_inference` or `candidate_strategy`, even when their basis includes explicit facts. Their lineage may point to BusinessClaim, Business, Market, ProductService, Objective, research, outcomes, or other relevant canonical evidence.

Example:
- User: “We provide written estimates.” → approved `BusinessClaim`.
- Model: “Transparency should be the core positioning.” → `candidate_strategy` unless the organization adopts it as something stronger.

## Claim expansion boundary

Creative copy may restate a supported claim but may not enlarge it into a new commitment.

Approved: “We provide written estimates.” may support “Request a written estimate.” It does not automatically support “We provide separate written repair and replacement estimates for both options.”

Quantifiers, guarantees, availability, timing, price, discounts, financing, warranties, certifications, comparative/superlative language, and process commitments require support when they materially enlarge the business promise.

## Customer-facing Asset claim manifest

For customer-facing Content/Marketing Assets, use `scripts/build_claim_manifest.py <business-id> <asset-file>` after drafting when deterministic claim checking is applicable. `customer_facing` describes intended audience/use, not publication status: an unpublished homepage, landing page, email, ad, proposal, webinar, or similar outward draft is still customer-facing.

Set `extensions.businessos.customer_facing: false` only for genuinely internal support Assets such as research, analysis, strategy, planning, or an internal brief.

Text-native artifacts AURA can inspect are scanned directly. For newly produced opaque/rendered media such as images, PDFs/presentations, audio, or video, preserve a compact claim-surface sidecar when material outward claims cannot otherwise be inspected deterministically. The sidecar may include:
- `artifact_ref` for the governed artifact;
- `visible_text`;
- `spoken_text`;
- `material_visual_claims`;
- or a substantive `no_material_claims_reason`.

Use `scripts/build_claim_manifest.py <business-id> <asset-file> --claim-surface <sidecar-ref>` when a sidecar is needed. The sidecar is an auditable representation, not proof that it matches the final render; substantive QA should inspect the actual artifact.

Each business-specific/promise-like candidate in the claim manifest is classified as:
- `approved_business_claim` with substantively supporting trusted canonical refs;
- `general_guidance` only when it is genuinely not a claim about the active business;
- `placeholder` when visibly marked as a placeholder.

A trusted support reference is not a permission token. Its canonical content must actually support the predicate. If wording materially enlarges the supported promise, narrow it, frame it honestly as provisional/general where appropriate, or establish the missing business truth.

`validate_business.py` may re-scan persisted customer-facing Assets and reject unsupported manifest entries. This protects AURA’s truth boundary; it does not govern how the model/harness performed the drafting work.

## Run provenance is optional

A valid customer-facing Asset does **not** require a Run, AURA contract, contract chain, or execution ledger. Capable humans/models may create valid work directly.

When an Asset is linked to a Run, that receipt must describe the method and results truthfully. If the Run claims `aura_playbook`, the selected playbook’s conformance/evidence requirements also apply. External Skill, model-created, and ad-hoc work must not fabricate AURA contract provenance.

`origin: imported` or `origin: preexisting` describes where an Asset came from. It does not forbid AURA from later linking real work performed on that Asset to a truthful work receipt.

## Existing customer-facing surfaces

Editing an existing outward surface is not a loophole for unsupported claims. The same active-business truth boundary applies whether work creates, removes, or edits copy.

AURA does **not** require a universal pre-edit snapshot, mutation manifest, ChangeEvent, or verification ceremony. Preserve before/after evidence, a material ChangeEvent, or a VerificationRecord only when doing so genuinely improves organizational truth, troubleshooting, measurement, or continuity. Runtime/tool mechanics belong to the active harness.
