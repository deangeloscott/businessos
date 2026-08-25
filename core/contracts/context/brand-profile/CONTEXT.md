---
id: core.context.brand-profile
type: playbook
version: 1.5.0
owner_system: core
risk: medium
autonomy_ceiling: 2
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
Turn explicit brand preferences, approved examples, and observable first-party patterns into durable generation constraints for every installed module.

## Business Outcome
Make outputs consistently look, sound, and behave like this specific brand instead of a generic business using the same underlying Business OS.

## Run When
When a business provides or changes brand voice, visual rules, content preferences, channel conventions, approved references, or prohibited styles. During fresh-business onboarding, explicit organization-level brand guidance should become canonical Brand state before downstream customer-facing work begins.

## Process
1. [HYBRID] Collect explicit instructions, brand guidelines, approved examples, rejected examples, reference Assets, and channel-specific preferences; distinguish mandatory rules from preferences. If these are supplied during fresh-business onboarding, create a small structured Brand manifest and pass it through `bootstrap_explicit_context.py --brand-profile-file ...` (or the supported `brand` facts field) so the Brand exists before residual/downstream Runs. Do not flatten voice/style/audience guidance into BusinessClaim constraints merely to avoid creating Brand state.
2. [AI] Normalize the guidance into voice, positioning, visual identity, content style, channel preferences, reference assets, prohibited styles, claims, and other durable brand rules without inventing unsupported requirements.
3. [AI] Resolve conflicts by authority and recency: explicit current business instruction outranks inferred patterns; approved guidelines outrank isolated historical examples; unresolved conflicts remain visible.
4. [HYBRID] Determine whether each change is a factual synchronization, explicit brand decision, or inference. Existing canonical Brand decisions that are only inferred require a ContextUpdateProposal rather than silent overwrite.
5. [DETERMINISTIC] Validate the resulting Brand object or proposal against schema, business isolation, references, and approved-claim constraints.
6. [AI] Summarize the active brand rules in operational terms that downstream Content, Marketing, SEO, and other installed modules can apply directly, including notable do/don't examples.

## Verification
A downstream job reading the Brand object can distinguish required rules, preferred expression, references, and prohibited behavior without needing the original conversation that established them.
