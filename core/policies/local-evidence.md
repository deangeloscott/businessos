# Local / First-Party Evidence Policy

Use this policy when SEO/AEO or another Workflow makes direct factual observations about local files, websites, repositories, first-party exports, configuration, screenshots, APIs, or other inspectable organization-controlled evidence.

## Core rule
Preserve enough evidence/provenance that future work can distinguish what was actually observed from what was inferred. AURA does **not** require one particular inspector, parser, browser, persistence helper, or sentence renderer as the only legitimate way to know a first-party fact.

The active model/harness may inspect evidence through its real capabilities: browser/devtools, filesystem tools, code/search tools, screenshots, APIs/connectors, structured exports, external Skills, or another sound method. When the evidence matters beyond the current session, preserve the relevant source/capture/pointer and observation so future work can understand where the fact came from.

## Optional deterministic site capture

`scripts/inspect_site_evidence.py` and `scripts/persist_site_observation.py` remain useful optional helpers for mechanically reproducible inspection of local website exports. Use them when deterministic extraction materially improves confidence, repeatability, before/after comparison, or debugging.

When their `businessos_local_evidence` manifest metadata is used, AURA may deterministically validate its internal integrity:
- source locator/identity consistency;
- snapshot/content hashes;
- manifest existence and parseability;
- referenced deterministic fact IDs.

That validation establishes the integrity of **that capture method**. It does not mean other model/harness evidence paths are invalid, and it does not require an Observation's natural-language statement to equal an AURA-generated sentence.

## Evidence identity and immutable history
For deterministic local captures, source identity and snapshot hash distinguish where evidence came from and what state was captured. Historical evidence remains historical evidence even when the source later changes.

Two byte-identical directories may still be different evidence sources because their source locators differ. A new source state can become a new capture while prior evidence remains available for before/after reasoning when useful.

## Observation, inference, outcome
Keep these meanings distinct when the distinction matters:
- **Direct observation:** what the inspected first-party evidence supports.
- **Inference:** what the observed condition may imply.
- **Measured outcome:** what analytics, search, customer, revenue, or answer-surface evidence actually demonstrates.
- **Unknown:** material state that has not been established.

A technical condition can be valuable evidence without automatically proving a downstream outcome. For example, a `noindex` directive can be directly observed; the model may reasonably treat correcting an unintended directive as prerequisite work while still leaving actual traffic/revenue impact unknown if it was not measured.

## Scope and judgment
Use the strongest evidence path appropriate to the consequence. Do not force deterministic capture when ordinary direct inspection is sufficient, and do not treat a model assertion with no preserved evidence as stronger than it is.

AURA preserves evidence and epistemic distinctions. The active model/user decides what the evidence means, how much verification is warranted, and what to do next.
