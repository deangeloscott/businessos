# Shared Intelligence Foundation

AURA helps organizational intelligence accumulate across sessions, models, and tools without becoming a crawler platform, semantic router, scheduler, or separate intelligence product.

## Architectural invariants

- **The organization is the durable unit of intelligence.** Material evidence, Observations, Insights, decisions, measurements, and Learning can survive the conversation/model/harness that discovered them.
- **Shared mechanics, domain-specific meaning.** AURA can preserve sources, evidence, subject/watch state, references, and current/history mechanics. The capable model/user determines what evidence means for customers, competitors, industry, discovery, content, persuasion, or customer progression.
- **Tool/model neutral.** Workflows describe the evidence, business outcome, real constraints, and useful method in natural language. The active model/harness chooses the best appropriate tools, providers, Skills, and execution methods it actually has. AURA does not inventory, bind, or limit them through its own tool ontology.
- **Minimum sufficient research.** Do not research, archive, or monitor everything because it is technically possible. Expand depth, coverage, cadence, or modalities only when doing so can materially improve the decision, reduce important uncertainty, preserve a useful baseline, or satisfy a real evidence requirement.
- **No competing truth stores.** Canonical organization state and linked evidence remain authoritative. Human-readable views are replaceable interfaces, not a second truth system.

## Multimodal evidence

Relevant evidence may be text, webpages, PDFs, tables, screenshots, images, audio, video, transcripts, captions, comments, structured records, or mixed-media pages.

When a material conclusion depends on non-text evidence:
1. inspect the underlying media using the best appropriate tools/resources available to the host;
2. preserve the smallest auditable evidence or reproducible pointer needed for the claim;
3. distinguish what was observed from the model's interpretation;
4. record material acquisition limitations;
5. never treat an AI-generated summary of unseen media as support-grade evidence.

Use `core/policies/research-evidence.md` for the support boundary. Large source systems and media archives should usually remain in the systems that own them; AURA keeps bounded evidence, references, hashes, or derived organizational meaning when useful.

## Durable subjects and sources

`SourceProfile` is a lightweight source/watch memory primitive. A tracked subject may be an organization, the active business, competitor, substitute, partner, creator, public figure, publication, product/brand, platform, regulator, community, or other decision-relevant actor.

Identity resolution is a semantic judgment. Deterministic AURA may preserve exact identifiers and candidate records, but it must not merge namesakes merely because names/keywords look similar. The active model/user resolves real-world identity from evidence; unresolved identity stays unresolved.

Different domains may reuse the same source evidence while preserving their own meaning. This does not require a deterministic semantic-routing layer.

## Evidence closure and subject relevance

Evidence closure is a reasoning boundary, not a demand for exhaustive research. For material subjects and decision-relevant dimensions, important conclusions should be support-grade, explicitly limited, visibly unknown/blocked, or marked not material before synthesis is treated as decision-grade.

Material claims should preserve a traceable evidence chain at the level needed to audit them. **Evidence about one subject does not become evidence about another subject** merely because both appear in the same analysis. Cross-subject comparison is valid only when the underlying subject-specific facts are independently supported.

Keep these truth types distinct when they materially affect the decision:
- **observed fact** — what evidence directly shows;
- **inference** — a reasoned interpretation of supported observations;
- **sentiment pattern** — a scoped pattern in a defined sample/population;
- **hypothesis** — a proposition to test or investigate;
- **effectiveness/outcome evidence** — evidence that a tactic or condition produced or correlates with a result at the confidence stated.

A confidence score or polished narrative does not repair missing provenance. A test threshold or decision rule may be deliberately chosen without pretending it is a forecast; predicted impact requires its own evidence.

## Monitoring design

A durable watch may remember:
- why the subject/source matters;
- questions and material-change signals;
- useful source classes/modalities;
- user-stated or model-suggested cadence intent;
- notification intent;
- last checked/material-change state;
- when another check would be useful.

**Cadence is organizational intent; scheduling is host execution state.** A saved `next_check_at` does not prove that any future task exists. The model may suggest a proportionate cadence when recurring monitoring is requested; user-specified cadence wins.

The host/runtime that actually creates or observes a schedule is the authority on whether automation is active. AURA may preserve a bounded reference to the relevant external schedule when that reference materially helps continuity, but it does not cache scheduler status or create, mirror, verify, or maintain scheduler bindings.

Unchanged checks should update source/watch checkpoints rather than create duplicate findings or alert noise. AURA may remember notification intent; actual delivery belongs to the runtime/channel that sends it.

## Contextual comparison

Do not use one flat comparison set for every decision. Relevant comparison dimensions can include geography, customer overlap, category/substitute role, scale/stage, price tier, business model, channel, use case, or aspirational/benchmark role.

The active model chooses comparison context based on the question and evidence. AURA preserves useful resolved context; it does not need a deterministic semantic comparison router.

## Decision context

Audience/customer segment, awareness state, lifecycle role, desired next action, objections, proof needs, switching friction, and evidence-backed motivations can materially improve synthesis. These are lenses, not mandatory labels. Do not infer customer psychology merely because a framework contains it.

Customer Intelligence should ground customer claims when evidence exists. Marketing/Content may use explicitly labeled hypotheses when needed. Preferences for a framework do not establish business facts, promises, or authorization.

## Human and machine legibility

When useful, human views should make it easy to understand:
- what AURA currently knows;
- what changed;
- why it believes it;
- confidence/limitations;
- source/evidence links;
- what remains unknown;
- what decision this affects;
- whether recurring execution is actually external/active or merely intended.

Do not create Markdown mirrors for every canonical object. Generate views when they reduce cognitive load; canonical state and evidence remain authoritative.
