# Shared Intelligence Foundation

AURA's intelligence should become richer without becoming a separate intelligence product, required knowledge graph, crawler platform, or monitoring daemon. Core owns the shared mechanics that let domain systems acquire, preserve, reuse, compare, and refresh evidence; semantic owners still decide what that evidence means for customers, competitors, industry, discovery, content, persuasion, or customer progression.

## Architectural invariants

- **The organization is the durable unit of intelligence.** Material evidence, Observations, Insights, source history, decisions, measurements, and Learning survive the conversation/model/harness that discovered them.
- **Shared mechanics, domain-specific meaning.** Core may resolve sources/subjects, preserve multimodal evidence, maintain watch state, compare current versus prior evidence, and route signals. Customer, Competitor, Industry, SEO/AEO, Content, Marketing, and Customer Optimization retain their existing semantic ownership.
- **Portable-first.** A watch plan or tracked subject must remain useful as organization-owned state without requiring a proprietary server, database, crawler, scheduler, model provider, or ViralTrac connection. Optional infrastructure may execute checks more conveniently.
- **Capability-neutral.** State the evidence/business job first. Use the best available model/harness/tool path for webpages, documents, images, audio, video, transcripts, comments, APIs, or structured exports. Missing native multimodal capability changes the acquisition/extraction method, not the required evidence standard. Trusted optional local capability packs may raise the local execution ceiling without becoming hard dependencies.
- **Minimum sufficient research.** Do not archive or monitor everything because it is technically possible. Depth, source coverage, cadence, and modalities should expand only when they can materially change a decision, reduce important uncertainty, preserve a material baseline, or satisfy verification.
- **No competing truth stores.** Canonical JSON remains machine-authoritative. Human-readable summaries/views may be generated from canonical state and linked evidence, but must not become a second source of truth.

## Multimodal evidence

Treat source modality as an evidence property, not a separate research universe. Relevant evidence may include text, webpages, PDFs, tables, screenshots, images, audio, video, transcripts, captions, comments, structured records, or mixed-media pages.

When a material conclusion depends on non-text evidence:
1. inspect the underlying media when the available capability permits it;
2. preserve the smallest auditable representation needed for the claim, such as source URL/ID, timestamp or page, bounded transcript/excerpt, representative frame/screenshot, structured record, content hash, or durable external pointer;
3. distinguish what was visible/spoken/measured from the model's interpretation;
4. record acquisition limitations (for example transcript-only analysis when the visuals were unavailable);
5. never treat an AI-generated summary of unseen media as support-grade evidence.

Use `core/policies/research-evidence.md` for the support boundary. For large media, preserve bounded evidence or reproducible pointers instead of copying an unnecessary archive into the workspace.

Optional deterministic tools may improve acquisition/processing. For example, `yt-dlp` can provide permitted media/subtitle acquisition mechanics and FFmpeg/ffprobe can provide media conversion/frame/audio/metadata mechanics. Those tools do not themselves establish what a video means. Follow `core/policies/local-capability-packs.md` and preserve the same evidence/modality boundaries.

## Durable subject and source tracking

`SourceProfile` is the shared lightweight watch primitive. A SourceProfile represents one public/authorized source or surface. Related profiles may carry the same `subject_key` when they have been explicitly resolved to the same real-world subject.

A tracked subject may be an organization, the active business, competitor, substitute, partner, creator, public figure, publication, product/brand, platform, regulator, community, or other decision-relevant actor. Tracking does not change semantic ownership:
- competitor strategy/state remains Competitor Intelligence;
- broad external events remain Industry Intelligence;
- customer beliefs/experience remain Customer Intelligence;
- creator/content mechanisms remain Content Synthesis;
- search/local-discovery competition remains SEO/AEO;
- active-business facts remain governed Business Context/first-party truth.

Do not merge namesakes or accounts merely because names look similar. Preserve unresolved identity as separate/candidate source profiles until evidence is sufficient.

## Monitoring design

A durable watch should answer:
- why this subject/source matters to the organization;
- which decisions it could affect;
- which questions/signals are worth monitoring;
- which sources/modalities are decision-relevant;
- what counts as a material change;
- how quickly those signals can reasonably change;
- when deeper research or human attention is justified.

Prefer change detection and semantic deduplication over repeated full re-research. Unchanged checks should update checkpoint state rather than create duplicate Insights/alerts.

**Cadence is semantic organizational intent; scheduling is host execution state.** AURA owns the cadence/next useful check and may infer a proportionate starting cadence when recurring monitoring is clearly requested. User-specified cadence wins. Different subjects/sources/signals may use different cadences. A saved `next_check_at` does not prove a future task is scheduled.

AURA owns the monitoring state and meaning, not a mandatory scheduler. A harness, OS scheduler, workflow runner, ViralTrac, or future provider may execute the next check. Automatic monitoring may be called active only when a verified scheduler binding exists in the current environment. Otherwise preserve reminder-only, due-on-next-start, paused/blocked, or manual state and follow `core/policies/monitoring-continuity.md`.

## Contextual comparison

Do not use one flat comparison set for every decision. Select comparables according to the question. Relevant dimensions may include:
- geography/service area;
- customer/audience overlap;
- offer/category and substitute overlap;
- scale/stage;
- market position/price tier;
- business model;
- channel/discovery surface;
- use case/job-to-be-done;
- direct, substitute, emerging, aspirational, attention, or benchmark role.

A nationally famous company may be useful as an aspirational/category benchmark while being irrelevant to a local-map-pack decision. State what each comparison group is being used to learn.

## Decision context and persuasion/customer intelligence

Where useful, resolve the decision context before synthesis:
- audience/customer segment;
- awareness/knowledge state;
- funnel or lifecycle role;
- desired next action/outcome;
- objections, proof/risk needs, switching/friction;
- evidence-backed motivations such as gain, loss avoidance, certainty, control, speed, simplicity, status/identity, convenience, autonomy, belonging, effort reduction, or financial outcome;
- relevant commercial/customer value and constraints.

These are lenses, not mandatory labels. Do not infer a psychological motive merely because a framework contains it. Customer Intelligence should ground customer motivations when evidence exists; Marketing/Content may use provisional hypotheses when needed and must label them accordingly.

Organization or operator marketing doctrine belongs in governed Brand/PreferenceProfile/BusinessClaim context according to its meaning. A preference for a persuasion framework does not establish a business fact, create a guarantee, authorize scarcity/urgency, or override evidence.

## Human and machine legibility

Canonical state should be precise enough for models, deterministic helpers, validators, and future providers. When humans need to inspect the same intelligence, generate concise views that answer:
- what AURA currently knows;
- what changed;
- why it believes it;
- confidence/limitations;
- source/evidence links;
- what remains unknown;
- what decision/action this affects;
- whether monitoring is actually automated or only planned.

Do not create Markdown mirrors for every canonical object. Generate human views when they reduce cognitive load or aid review; canonical state and evidence remain authoritative. Normal-user responses should describe the human concept/location first (for example `AtlasOps → Knowledge → Tracked Subjects → Alex Hormozi`) and reserve raw JSON/runtime paths for advanced inspection/debugging.
