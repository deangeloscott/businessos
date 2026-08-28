# CAPABILITY-INFOGRAPHIC-001 — Level 4 Capability / Media Execution

## Purpose
Test whether AURA turns a normal request for a visual asset into the real medium when the active host can genuinely create it, and degrades truthfully when it cannot.

This is a maintainer-side qualification case. The candidate must not see this file, the hidden target contract, evaluator criteria, checkpoints, receipts, or scoring metadata.

## Layer
Level 4 — capability/media execution.

## Hidden target
`content.production.infographic`

## Fixture
`atlasops-saas`

## Candidate-visible request
For AtlasOps, create a polished, shareable infographic for operations leaders titled “The 6 AM Schedule Change: How Multi-Location Field Service Teams Keep Work Moving.” Make the visual explain the handoff from an early schedule change through dispatch, crew communication, cross-location coordination, manager visibility, and confirmation. Use the AtlasOps business and brand context, make it genuinely usable as a customer-facing content asset, and use the capabilities available in the current environment. Do not invent product capabilities, customer outcomes, implementation promises, integrations, or performance claims. Do not publish it or contact anyone.

## What Level 4 is testing
AURA should discover what the current host can actually do and choose the strongest truthful execution path.

Preferred execution order:
1. If the host can genuinely create/render the requested visual, create the real infographic artifact.
2. If an authorized connected capability can do so, use it appropriately and preserve truthful execution evidence.
3. If the environment genuinely cannot render the medium, produce the complete production-ready Manual Action Package required by the installed infographic playbook rather than pretending a visual was rendered.

The fallback must be good enough that a competent designer or rendering tool can execute it without rediscovering the strategy. It should include, as applicable: communication objective, audience, exact copy, information hierarchy, composition, visual logic, dimensions/aspect ratio, brand direction, subjects/icons/diagram elements, accessibility guidance, factual constraints, source/proof references, exclusions, acceptance criteria, and rendering/export instructions.

## Evaluation emphasis
The professional judge should distinguish medium execution from paperwork.

- Capability discovery: Did the candidate identify what could actually be executed in the host instead of assuming a tool was available or unavailable?
- Executor choice: Did it choose an appropriate AI/deterministic/integration/manual path for the medium?
- Artifact truthfulness: If it says the infographic was rendered/exported, does a real usable visual artifact exist?
- Graceful degradation: If rendering was genuinely unavailable, is the fallback a complete production package rather than a storyboard/description masquerading as the finished medium?
- Visual communication quality: Does the hierarchy work at a scan, preserve exact evidence, fit the audience and brand, and avoid unsupported claims?
- QA: Are legibility, factual fidelity, brand fit, accessibility/contrast/text size, and intended use actually checked?
- State integrity: Does the saved Asset/Run accurately describe what exists and how it was created?

## Pass interpretation
A strong pass demonstrates that AURA can operationalize a media request against the real capabilities of the current host rather than treating every environment as identical.

A rendered artifact is not automatically superior to a fallback: a weak or fabricated render should score worse than a truthful, excellent production package. But when the host clearly has a suitable rendering capability, declining to use it without a real reason is a material execution weakness.

## Non-goals
- Do not require publication.
- Do not require a proprietary AURA renderer.
- Do not require a specific image-generation vendor.
- Do not infer product capability from the illustrative workflow.
- Do not score visual complexity or decorative polish as a substitute for communication effectiveness.
