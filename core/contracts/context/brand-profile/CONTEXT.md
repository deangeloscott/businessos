---
id: core.context.brand-profile
type: playbook
owner_system: core
reads:
- Brand
- Asset
- Observation
writes:
- Brand
- ContextUpdateProposal
capabilities:
  required:
  - none
  optional:
  - document.read
  - webpage.fetch
context:
- Business
- Brand
---
# Capture Brand Profile

## Purpose
Preserve durable organization Brand guidance and evidence-backed Brand context so future work can express the organization consistently without inventing rules from isolated examples.

## Business Outcome
Make relevant outputs reflect this organization's established voice, positioning, visual/content rules, references, and prohibitions while keeping Brand truth distinct from optional working preferences and public inference.

## Run When
Use when the organization explicitly provides/changes Brand guidance, when authoritative Brand materials should be normalized into durable context, or when resolving Brand context would materially improve current/future work.

## Process
1. [HYBRID] Gather relevant explicit instructions, brand guidelines, approved/rejected examples, reference Assets, and authoritative first-party materials. Distinguish mandatory Brand rules from optional work/expression preferences; PreferenceProfile remains the home for reusable optional choices.
2. [AI] Normalize only supported meaning into voice, positioning, visual identity, content style, channel guidance, reference assets, prohibited styles, claims, and other durable Brand fields. Do not invent requirements because they seem conventional or because one historical asset happened to use them.
3. [AI] Resolve conflicts using the actual evidence/authority available: explicit current organization instruction generally outranks inference; authoritative current guidelines generally outrank isolated historical examples. Preserve material unresolved conflict/uncertainty rather than silently choosing.
4. [AI] Decide whether newly observed material establishes current Brand truth, remains inference/candidate guidance, or indicates an unresolved possible change to existing Brand context. Use `ContextUpdateProposal` only when that unresolved candidate change is itself worth remembering; it is not a required approval/change-control step.
5. [DETERMINISTIC] Persist/validate the Brand or proposal chosen by the model/user against schema, business isolation, exact references, provenance, and outward-claim constraints where applicable. Deterministic AURA does not decide whether two pieces of Brand language mean the same thing.
6. [AI] Make the resulting Brand context understandable enough that future Content, Marketing, SEO, sales-support, or other relevant work can apply the established guidance without needing the original conversation.

## Verification
- Explicit Brand truth, inferred patterns, optional preferences, and outward BusinessClaims remain distinct.
- A Brand object is not required merely to start or continue unrelated organizational work.
- ContextUpdateProposal is used only for materially useful unresolved change memory, not as a permission gate.
- A downstream model can understand established Brand guidance and its provenance without treating unsupported public patterns as organization truth.
