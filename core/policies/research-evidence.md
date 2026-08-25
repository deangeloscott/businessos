# Research Evidence Preservation

Research is useful only when important conclusions can be checked later. A URL, search-result snippet, or the agent's memory of a page is a discovery lead, not enough preserved evidence for a material supported claim.

## Preserve the evidence before interpreting it
For public reviews, posts, forum comments, complaint pages, competitor pages, articles, and similar sources, inspect the underlying source when the available capability permits it. Preserve a bounded evidence packet for each material item used in analysis:

- durable source URL, permalink, record ID, or other source reference;
- retrieval time and source/platform type;
- the exact review/comment/source text or a bounded exact excerpt when text can be retained;
- rating, date, title, product/location/thread context, and public author label only when actually available and useful;
- a content hash when content was captured;
- a screenshot/snapshot Asset when visual preservation materially helps and the source/access rules permit it.

Do not copy an unnecessary archive of the internet into the workspace. Preserve enough original evidence to audit the conclusion. Large, sensitive, high-volume, or system-owned data may remain in an authoritative external system when a durable evidence pointer/hash can reproduce or inspect the underlying record.

## Search results are discovery, not evidence
Search-result snippets, AI summaries of search results, directory previews, and unvisited URLs can help find sources. They do not by themselves qualify an Insight as `supported` when the underlying claim depends on source content that was not inspected and preserved.

If the underlying source cannot be captured or reliably revisited, keep resulting interpretation provisional/candidate and state the limitation.

## SourceRecord evidence packet
For newly researched external sources, use `SourceRecord.extensions.businessos_evidence` when applicable. It may include:

- `capture_status`: `captured`, `external_pointer`, or `pointer_only`;
- `capture_method`: what was preserved, for example `text_excerpt`, `snapshot`, `api_record`, `external_pointer`, or `mixed`;
- `acquisition_method`: how the underlying evidence was actually obtained, such as `direct_page_read`, `browser_read`, `browser_capture`, `api_response`, `downloaded_document`, `uploaded_document`, `user_provided`, `first_party_export`, or `authoritative_record`;
- `captured_text`: exact source text/excerpt when permitted;
- `title`, `author_label`, `rating`, `context` when actually present;
- `asset_refs`: linked screenshot/snapshot Assets;
- `evidence_pointer`: durable provider/export/record reference when raw content stays outside the workspace;
- `capture_notes`: limitations or access constraints.

A plain URL with `capture_status=pointer_only` may be saved for discovery/history, but it is not sufficient support for a material Observation/Insight that depends on the unseen content. The same is true when `captured_text` exists but `acquisition_method` is only `search_result`, `search_snippet`, `directory_preview`, `ai_summary`, `unvisited_url`, or `unknown`. Filling in a text field does not turn search discovery into inspected evidence.


## Acquisition method vs. capture method
These answer two different questions:

- **Acquisition method:** How did we get the underlying evidence? Did we open/read the page, retrieve an API record, inspect an uploaded document, or only see a search result?
- **Capture method:** What did we save? Text/excerpt, structured record, screenshot/snapshot, external pointer, or a mix?

For material public-source claims, BusinessOS requires a support-grade acquisition method. Search results and snippets are useful for finding sources, but remain discovery-only even if an agent copies their text into a bundle. BusinessOS records the agent/provider-declared acquisition method; in a portable harness it cannot independently prove every tool call, so this metadata is an integrity boundary rather than a cryptographic audit trail. When the host can provide stronger receipts or tool provenance, preserve them in `acquisition_reference` or the linked Asset/provider record.

## Observation and Insight support
- An Observation states what was directly observed and points to the SourceRecord(s) that preserve or durably identify the underlying evidence.
- An Insight is interpretation. `supported` or `active` Insights require a traceable support chain through Observations to adequate source evidence.
- If adequate evidence has not been preserved, use `candidate` status or gather the missing evidence before strengthening the claim.
- Keep frequency and superlative claims honest. Say things like “in the sampled evidence” or “among the reviews examined” unless you have a representative/measured population that supports a broader claim such as “top,” “#1,” “most common,” or “dominant.”
- Schema-valid means structurally valid; it does not automatically mean evidence-supported. Run `scripts/validate_research_evidence.py <business-id>` or normal business validation before calling research complete.

## Screenshots
Screenshots are useful but are not required for every review. Prefer them when exact visual context matters, a source is likely to change, a proof/testimonial candidate may be reused, or the image itself has downstream value. Preserve searchable text/metadata when available even when a screenshot exists.

## Business truth and recommendations
External evidence stays external evidence. It may justify a market Insight or candidate Opportunity; it does not establish that the active business has the same customers, problems, services, capabilities, hours, guarantees, pricing, or performance.

Separate these stages:

1. **Observed market evidence** — what sources actually show.
2. **Supported interpretation** — what the evidence reasonably suggests.
3. **Candidate opportunity** — something the business may investigate or prioritize.
4. **Business promise/change** — only after active-business capability, feasibility, scope, and required authorization are established.

For example, evidence that customers value fast emergency response may support investigating rapid-response positioning. It does not authorize claiming “same-day guaranteed” or “24/7 emergency service” for the active business.

## Normal persistence path
During ordinary business work, use the supported deterministic persistence helpers instead of writing custom BusinessOS scripts or reverse-engineering schemas. For bounded research evidence, prefer:

`python3 scripts/persist_research_bundle.py <business-id> --bundle-file runtime/<bundle>.json`

If the helper rejects the bundle, correct the structured input using `--help`. Do not patch BusinessOS product internals or create a replacement canonical writer during normal operation.
