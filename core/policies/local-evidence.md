# Local / First-Party Evidence Policy

Use this policy when SEO/AEO or another workflow makes **direct factual observations about deterministic local files or first-party exports** such as HTML, robots.txt, sitemap XML, JSON, CSV, configuration, or similar inspectable artifacts.

## Core rule
A model saying that it inspected a local file is not itself evidence that the file contains what the model says it contains.

For mechanically inspectable website facts, preserve a deterministic evidence layer before creating canonical direct Observations:

1. Run `scripts/inspect_site_evidence.py <business_id> <site_root>`.
2. Use the returned deterministic fact IDs for the facts that materially support the diagnosis.
3. Persist direct site Observations with `scripts/persist_site_observation.py` rather than hand-authoring the Observation statement.
4. Put interpretation, severity, business consequence, prioritization, or hypotheses in an Insight/Opportunity/plan — not inside the direct Observation as if those conclusions were file contents.

`validate_business.py` validates the capture's internal provenance and requires direct Observations linked to a deterministic local-site SourceRecord to match their captured fact IDs exactly. A capture is historical evidence: later changes to the source do **not** erase or invalidate what was observed at capture time. However, `persist_site_observation.py` requires the source to still match the captured snapshot before that capture may support a **new current Observation**. If the source changed, capture the new state first.


## Evidence identity and immutable history
Local evidence has two independent identities:
- **source identity:** a deterministic hash of the normalized workspace-relative source locator;
- **snapshot hash:** a deterministic hash of the files and their content at capture time.

Evidence capture identity is the pair **(source identity, snapshot hash)**, not the content hash alone.

This means two byte-identical directories such as a diagnostic baseline and a writable implementation copy remain different evidence sources. Capturing one must never overwrite or relabel evidence captured from the other. If one source later changes, the new snapshot becomes a new evidence capture while the prior capture remains intact as historical before-state evidence.

Idempotent reuse is allowed only when both the source identity and snapshot hash match. `SourceRecord.source_reference`, the manifest `source_root`, and the local-evidence `source_identity` must agree; validation rejects provenance relabeling even when two locations contain identical bytes.

## What the deterministic inspector verifies
For local website exports the helper captures, where applicable:
- file hashes and a workspace snapshot hash;
- page title and H1;
- meta description;
- canonical URL;
- meta robots directives;
- JSON-LD block count, JSON parse validity, `@context`, and `@type`;
- local internal links and whether their local targets exist;
- image alt presence;
- robots.txt disallow rules;
- sitemap URLs and page membership;
- whether a page path is blocked by parsed wildcard robots rules.

The model remains responsible for reasoning about significance and next-best work. Deterministic extraction exists only to prevent directly inspectable facts from being hallucinated or silently altered.

## Truth classes
Keep these separate:
- **Direct observation:** a fact reproduced from the deterministic evidence manifest.
- **Inference:** what the observed condition may imply (for example, a canonical configuration may impair independent indexing).
- **Measured outcome:** what analytics/search/answer-surface evidence actually demonstrates.
- **Unknown:** performance or visibility state that has not been measured.

Do not turn a technical condition into a measured outcome. For example, a `noindex` directive is directly observable; "traffic is down because of it" is not established without performance evidence. Likewise, missing/limited structured data may be a machine-understanding opportunity, but actual AI-answer citation behavior remains unknown until observed.

## Scope
This does not replace `core/policies/research-evidence.md` for external research. It is the first-party/local counterpart: deterministic local evidence should be reproducible before a material direct Observation is allowed to become canonical.
