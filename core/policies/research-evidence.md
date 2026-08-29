# Research Evidence Preservation

Research is useful only when important conclusions can be checked later. A URL, search-result snippet, AI summary, or the agent's memory of a source is a discovery lead, not enough preserved evidence for a material supported claim. Evidence may be textual, visual, audio, video, document, structured, or mixed-media; the support boundary is the same even when the acquisition method changes.

## Preserve the evidence before interpreting it
For public reviews, posts, forum comments, complaint pages, competitor pages, articles, images, documents, podcasts/audio, videos, social media, and similar sources, inspect the underlying source when the available capability permits it. Preserve a bounded evidence packet for each material item used in analysis:

- durable source URL, permalink, record ID, file reference, timestamp/page/frame locator, or other source reference;
- retrieval time and source/platform type;
- the exact review/comment/source text or a bounded exact excerpt when text can be retained;
- for audio/video, the relevant bounded transcript/excerpt and timestamps when spoken content matters;
- for visual evidence, representative screenshot/frame/page Assets when the visual itself materially supports the claim;
- rating, date, title, product/location/thread context, and public author label only when actually available and useful;
- a content hash when content was captured;
- a clear acquisition/capture limitation when only part of a mixed-media source was inspected (for example transcript-only, audio-only, sampled frames, inaccessible comments, or missing captions).

Do not copy an unnecessary archive of the internet into the workspace. Preserve enough original evidence to audit the conclusion. Large, sensitive, high-volume, or system-owned data may remain in an authoritative external system when a durable evidence pointer/hash can reproduce or inspect the underlying record.

## Modality-specific support boundary
- **Text/web/document text:** directly read content or a support-grade downloaded/uploaded/authoritative record may support claims about that text.
- **Images/visual pages:** directly inspect the image/page and preserve an Asset or reproducible pointer when the visual is material. OCR or a model-written description alone is not equivalent to inspecting an unavailable original.
- **Audio:** direct audio inspection may support audible claims. A transcript may support spoken-language claims when its provenance is adequate, but does not establish tone, music, sound design, or other unrepresented audio properties.
- **Video:** direct video inspection may support visual/audible claims when the relevant segment is actually inspected. Transcript-only evidence can support spoken-language claims, not editing, on-screen demonstrations, visual composition, gestures, thumbnails, or other visual mechanisms.
- **Mixed-media social/content pages:** inspect the modalities that materially carry the conclusion. A caption does not prove what occurs in a video; a thumbnail does not prove the full video; comments/reactions are separate evidence from the creator's content.
- **Structured/API/first-party records:** preserve the record payload or authoritative reproducible pointer and its definitions/context where needed.

Use the best available provider-neutral capability. Missing native media understanding changes the acquisition/fallback path and may narrow what can be supported; it does not authorize pretending unseen media was inspected.

## Search results are discovery, not evidence
Search-result snippets, AI summaries of search results, directory previews, and unvisited URLs can help find sources. They do not by themselves qualify an Insight as `supported` when the underlying claim depends on source content that was not inspected and preserved.

Reserved or placeholder public URLs such as `.invalid`, `.test`, `.example`, or localhost never establish current public evidence. If the real item cannot be opened and preserved, keep the finding unresolved rather than inventing a plausible locator, creator, quote, metric, frame, or timestamp.

If the underlying source cannot be captured or reliably revisited, keep resulting interpretation provisional/candidate and state the limitation.

## SourceRecord evidence packet
For newly researched external sources, use `SourceRecord.extensions.businessos_evidence` when applicable. It may include:

- `capture_status`: `captured`, `external_pointer`, or `pointer_only`;
- `capture_method`: what was preserved, for example `text_excerpt`, `snapshot`, `transcript_excerpt`, `key_frame`, `document_page`, `api_record`, `external_pointer`, or `mixed`;
- `acquisition_method`: how the underlying evidence was actually obtained, such as `direct_page_read`, `browser_read`, `browser_capture`, `downloaded_document`, `uploaded_document`, `image_inspection`, `audio_inspection`, `video_inspection`, `transcript_read`, `document_visual_inspection`, `api_response`, `user_provided`, `first_party_export`, or `authoritative_record`;
- `captured_text`: exact source text/transcript excerpt when permitted;
- `title`, `author_label`, `rating`, `context` when actually present;
- `asset_refs`: linked screenshot/snapshot/frame/page/evidence Assets;
- `evidence_pointer`: durable provider/export/record/media reference when raw content stays outside the workspace;
- `capture_notes`: limitations, sampled ranges, timestamp/page context, transcript provenance, or access constraints.

When the evidence is about one or more resolved subjects, also use top-level `SourceRecord.subject_refs` to identify those subjects. Subject scoping is optional when the source is genuinely general or unresolved, but decision-grade research should populate it when material claims depend on distinguishing entities, products, locations, creators, competitors, or other subjects.

A plain URL with `capture_status=pointer_only` may be saved for discovery/history, but it is not sufficient support for a material Observation/Insight that depends on the unseen content. The same is true when `captured_text` exists but `acquisition_method` is only `search_result`, `search_snippet`, `directory_preview`, `ai_summary`, `unvisited_url`, or `unknown`. Filling in a text field does not turn search discovery into inspected evidence.

## Acquisition method vs. capture method
These answer two different questions:

- **Acquisition method:** How did we get the underlying evidence? Did we open/read the page, inspect the image/video/audio, read a sufficiently grounded transcript, retrieve an API record, inspect an uploaded/downloaded document, or only see a search result?
- **Capture method:** What did we save? Text/transcript excerpt, structured record, screenshot/frame/page snapshot, external pointer, or a mix?

For material public-source claims, BusinessOS requires a support-grade acquisition method. Search results and snippets are useful for finding sources, but remain discovery-only even if an agent copies their text into a bundle. BusinessOS records the agent/provider-declared acquisition method; in a portable harness it cannot independently prove every tool call, so this metadata is an integrity boundary rather than a cryptographic audit trail. When the host can provide stronger receipts or tool provenance, preserve them in `acquisition_reference` or the linked Asset/provider record.

A support-grade acquisition method establishes only that the represented modality was inspected. The semantic claim must still fit the preserved evidence and any stated modality limitation.

## Observation and Insight support
- An Observation states what was directly observed and points to the SourceRecord(s) that preserve or durably identify the underlying evidence.
- An Insight is interpretation. `supported` or `active` Insights require a traceable support chain through Observations to adequate source evidence.
- If adequate evidence has not been preserved, use `candidate` status or gather the missing evidence before strengthening the claim.
- Keep frequency and superlative claims honest. Say things like “in the sampled evidence” or “among the reviews examined” unless you have a representative/measured population that supports a broader claim such as “top,” “#1,” “most common,” or “dominant.”
- Schema-valid means structurally valid; it does not automatically mean evidence-supported. Run `scripts/validate_research_evidence.py <business-id>` or normal business validation before calling research complete.

### Subject relevance
When a SourceRecord and its Observation both identify resolved subjects, their subject scopes must overlap. Evidence about one competitor, customer segment, creator, product, location, or other subject does not support a factual Observation about another merely because the sources were gathered in the same research run. Similarly, a supported/active Insight with resolved subjects should be supported by Observations whose subject scopes overlap or by evidence whose cross-subject relationship is explicitly explained.

Cross-subject comparisons are valid when each side has its own support and the comparison is derived from those supported facts. Do not attach convenient unrelated evidence to a canonical subject record to make the record appear sourced.

## Evidence closure before decision-grade synthesis
Evidence closure means the material conclusion is bounded by the evidence actually obtained. It does **not** mean exhaustive research or a universal source quota.

Before producing or finalizing a decision-grade research synthesis:

1. **Resolve the decision scope.** Identify the material subjects, requested/material dimensions, time/geography/audience constraints, and the decisions the synthesis is intended to support.
2. **Track coverage.** For each material subject/dimension, use a useful state such as `supported`, `limited`, `unknown/blocked`, or `not_material`. Preserve why the state is appropriate and the strongest relevant evidence refs where support exists.
3. **Close material claims.** Important factual claims should resolve to subject-relevant support-grade evidence. Important inferences should identify the supported facts they derive from. Sentiment patterns should state the sample/population boundary. Hypotheses should remain hypotheses.
4. **Do not manufacture precision.** Do not create numeric ranges, dates, contract terms, implementation timelines, prevalence, rankings, or other specificity beyond what the evidence establishes. When sources conflict or cannot be normalized, preserve the disagreement or compare structure instead of inventing a clean number.
5. **Bound confidence.** Source count, model confidence, polished prose, and agreement among derivative sources do not substitute for directness, authority, freshness, relevance, representativeness, and contrary evidence. One anecdote may be useful evidence without establishing a recurring pattern.
6. **Separate forecasts from decision rules.** A deliberately chosen test threshold, minimum detectable effect, stop rule, or success criterion is not a prediction. Do not present an unsupported impact range or outcome forecast as though research established it.
7. **Stop proportionately.** If an important gap could materially change the decision and accessible evidence is available, research further. If the evidence is unavailable or further work is not proportionate, keep the gap visible and narrow/downgrade the conclusion. Never close a gap by guessing.

A decision-grade artifact should make it possible to answer: what is supported, by which evidence, about which subject and scope, with what limitations, what remains unknown, and which recommendations are facts versus interpretations or hypotheses. Claim-level provenance may be expressed through canonical Observation/Insight refs, source refs adjacent to material claims, or another auditable mapping appropriate to the artifact; a bibliography detached from the claims is not enough when the synthesis contains many material factual assertions.

## Screenshots, frames, and media captures
Screenshots/frames are useful but are not required for every source. Prefer them when exact visual context matters, a source is likely to change, a proof/testimonial candidate may be reused, or the image/visual mechanism itself has downstream value. Preserve searchable text/transcript/metadata when available even when a visual Asset exists. For long audio/video, preserve the bounded segments needed to audit material conclusions instead of copying the whole source without reason.

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
