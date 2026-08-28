# Context Provenance & Business Claim Policy

BusinessOS must distinguish **what the business/user actually established** from **useful strategy the agent derived**. A model may create useful Brand, AudienceSegment, Offer, positioning, messaging, or other strategic context, but it may not label its own synthesis as `explicit_user` truth.

## Authority classes
Use these meanings consistently:
- `explicit_user` — directly grounded in an authoritative user statement and persisted through a supported deterministic grounding path.
- `verified_first_party` — established by an authorized first-party system/source.
- `external_evidence` — observed outside the active business; never an active-business fact by itself.
- `derived_inference` — reasonable interpretation derived from known facts/evidence; useful but not directly stated.
- `candidate_strategy` — proposed positioning, audience framing, offer framing, message, tactic, or operating choice that has not been adopted as active-business truth.
- `unknown` — not established.

## Explicit business claims
`BusinessClaim` is the canonical object for explicit user-authorized customer-facing claims, promises, constraints, and prohibitions that need to be reused safely by any BusinessOS workflow that creates or mutates customer-facing material.

For conversational setup, prefer `bootstrap_explicit_context.py` with:
- `approved_claims`: exact/conservative statements the business authorizes as true/promisable.
- `claim_constraints`: explicit constraints/prohibitions/known absence statements that generated work must respect.

The helper grounds these statements to the verbatim source and persists them as `BusinessClaim` objects. Do not hand-author an object and add `grounding_method: bootstrap_explicit_context` afterward; that metadata does not make a model-authored object explicit-user truth.

## Derived context
Brand, AudienceSegment, and Offer objects created by an agent during strategy/production are normally `derived_inference` or `candidate_strategy`, even when they cite explicit source facts. Explicit organization-supplied Brand instructions may be persisted as `explicit_user` only through the deterministic `bootstrap_explicit_context.py` grounding path; do not hand-stamp an assembled Brand as explicit. Their lineage/basis may include `BusinessClaim`, Business, Market, ProductService, Objective, research, or other canonical objects.

Examples:
- User: “We provide written estimates.” → approved `BusinessClaim`.
- Agent: “Transparency should be the core positioning.” → `candidate_strategy`, not explicit-user truth.
- User: “Do not use urgency or discounts.” → constraint `BusinessClaim`.
- Agent: “Homeowners fear being pressured.” → derived/candidate audience interpretation unless sourced or explicitly stated.

## Claim expansion boundary
Creative copy may restate an approved claim, but it may not enlarge it into a new commitment.

Examples:
- Approved: “We provide written estimates.” → allowed: “Request a written estimate.”
- Not automatically allowed: “We provide separate written repair and replacement estimates for both options.”
- Generation instruction: “Do not use pressure tactics.” does **not** establish the public business promise “We are a no-pressure company.”

Quantifiers, guarantees, availability, timing, price, discounts, financing, warranties, certifications, comparative/superlative language, and process commitments require their own support when they materially change the promise.

## Customer-facing Asset claim manifest
For Content/Marketing Assets with a customer-facing file, run `scripts/build_claim_manifest.py <business-id> <asset-file>` after drafting. `customer_facing` describes the **intended audience/use**, not whether the artifact has been published. A local draft of a homepage, landing page, email, ad, proposal, webinar, or similar outward asset is still customer-facing even while status=`draft` and publication is unauthorized. Set `extensions.businessos.customer_facing: false` only for genuinely internal support Assets such as an internal brief, strategy note, analysis, research packet, or planning artifact. Marketing Synthesis Assets default customer-facing and may opt out only for an explicitly internal support role. Otherwise customer-facing is the safe default.

Claim governance is **format-independent**. Text-native artifacts that AURA can inspect without OCR are scanned directly. Newly produced opaque/rendered media (for example raster images, PDFs/presentations, audio, or video) must save a compact JSON claim-surface sidecar and reference it as `extensions.businessos.claim_surface_ref`. The sidecar contains:
- `artifact_ref` for the exact governed file,
- `visible_text` for audience-readable copy,
- `spoken_text` for narration/dialogue,
- `material_visual_claims` for factual/product implications carried by the visual itself,
- or a substantive `no_material_claims_reason` when the asset genuinely contains none.

Example sidecar:
```json
{
  "format_version": "1.0",
  "artifact_ref": "instances/example/assets/example.png",
  "visible_text": ["Compare the options before deciding."],
  "spoken_text": [],
  "material_visual_claims": ["The diagram is an illustrative workflow, not a depiction of product automation."]
}
```

Use `scripts/build_claim_manifest.py <business-id> <asset-file> --claim-surface <sidecar-ref>` for opaque/rendered media. The sidecar is an auditable representation, not evidence that the render matches it. Final QA must inspect the actual artifact and verify parity; a safe sidecar paired with contradictory pixels, slides, audio, or video is a failure.

Every business-specific/promise-like candidate returned by the scanner must be classified in the canonical Asset's `extensions.businessos.claim_manifest` as one of:
- `approved_business_claim` with canonical support refs,
- `general_guidance` (must not be a claim about the active business), or
- `placeholder` (must be visibly placeholder-marked).

`validate_business.py` re-scans the saved artifact or its declared claim surface and rejects missing/unsupported manifest entries. A trusted support reference is **not** a permission token: the referenced canonical text must substantively authorize the customer-facing predicate, not merely exist or share the business name/market. A claim manifest is a QA control, not a replacement for judgment: if a statement or visual implication materially enlarges the supported promise, narrow it, visibly frame it as illustrative/general where truthful, or obtain authorization.

### Claim manifest example
```json
{
  "customer_facing": true,
  "claim_manifest": [
    {
      "text": "We provide written estimates.",
      "classification": "approved_business_claim",
      "support_refs": ["clm_example_written-estimates"]
    },
    {
      "text": "Compare the options before deciding.",
      "classification": "general_guidance",
      "support_refs": []
    },
    {
      "text": "Call [PHONE NUMBER].",
      "classification": "placeholder",
      "support_refs": []
    }
  ]
}
```
The `text` must match the saved artifact statement returned by the scanner. A customer-facing Asset created by Content/Marketing must also carry `extensions.businessos.run_ref` to a Run whose root contract is explicitly marked `artifact_role: customer_facing_production_root`, plus a `contract_chain` containing that root and its required subcontracts. The completed Run must include the actual customer-facing Asset file in root completion evidence; a strategy/helper packet alone cannot prove production. Imported/pre-existing Assets may explicitly mark `origin: imported` or `origin: preexisting` **only when they genuinely predate the producing Run and therefore have no producing `run_ref`**. Work generated during the current execution must never be relabeled imported/preexisting merely because it is unpublished, local, or awaiting review.

## Existing customer-facing mutations
The Asset claim manifest above protects newly produced Content/Marketing Assets. Existing customer-facing surfaces edited by SEO, Customer Optimization, Content, Marketing, Core, or another workflow must additionally follow `core/policies/customer-facing-mutations.md`. That delta-based control scans only statements introduced by the current mutation, so a technical edit cannot silently create a new active-business capability or promise.
