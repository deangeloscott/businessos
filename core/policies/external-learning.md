# External Ecosystem Intelligence and Learning

BusinessOS may learn from the external world, but external popularity must never become operating truth by accident. This policy governs recurring and on-demand discovery of tactics, claims, events, research, platform changes, customer signals, competitor movements, and other outside developments across installed domains.

## Division of responsibility

- **BusinessOS** defines the required discovery coverage, evidence standards, provenance, freshness, corroboration, contradiction, applicability, routing, experiment, and learning rules.
- **The model** performs semantic interpretation, generates context-appropriate searches, recognizes equivalent or conflicting claims, and reasons about applicability.
- **The harness/host** supplies retrieval tools, APIs, browser access, scheduling, concurrency, and other execution machinery.
- **Deterministic helpers** handle IDs, hashes, deduplication, validation, timestamps, persistence, and other operations that should not depend on model judgment.

A recurring schedule declared by a contract is execution intent. It does not make BusinessOS a scheduler or daemon. If no scheduler is available, the same radar must remain runnable on demand.

## Discovery rules

1. A known-source watchlist is a seed, not the search universe. Each broad radar cycle must include reasonable open discovery when the available capabilities permit it.
2. Discovery must not depend only on literal keywords. Use domain taxonomy, mechanisms, entities, semantic variants, citation trails, source/person discovery, communities, research, and official changes when relevant.
3. Search results, snippets, feeds, and social previews are discovery leads until the underlying material is inspected and preserved according to `core/policies/research-evidence.md`.
4. Preserve original publication/event time separately from retrieval time. Prefer the earliest traceable originating source rather than the most viral repeater.
5. Do not copy an unnecessary archive of the web. Preserve enough bounded evidence and lineage to audit material conclusions.

## Source attention is not source truth

SourceProfiles may help decide where to spend limited attention. Priority may reflect authority for a particular fact type, directness, original-research history, methodological quality, timeliness, access stability, historical usefulness, or repeated later support/contradiction.

Never convert this into a universal trust score. A source that is strong for policy statements may be weak for causal performance claims, and vice versa. Follower count, engagement, prestige, virality, confidence language, or repeated citation are not evidence that a new claim is true.

Historical source performance is an **attention prior only**. The current claim must still be evaluated from its own evidence.

## Independence, corroboration, and contradiction

- Trace whether apparently separate reports originate from one experiment, dataset, announcement, or anecdote.
- Twenty posts repeating one source are one evidence lineage, not twenty independent replications.
- Count independent support separately from echoes, extensions, commentary, and direct contradictions.
- For decision-relevant claims, deliberately search for disconfirming evidence, failed replications, counterexamples, methodological criticism, alternative explanations, and current authoritative guidance when applicable.
- Preserve unresolved contradictions. Do not force a binary conclusion when evidence is mixed or insufficient.

## Freshness and novelty

Freshness is mechanism-specific. Rapidly changing platform behavior may decay quickly; durable customer or business mechanisms may decay slowly; a regulation remains authoritative until changed or superseded.

Record the evidence date, retrieval date, last corroboration, and relevant platform/market/version context when available. Compare new claims with existing Insights and Learnings so renamed or newly viral old tactics are not misclassified as novel. Novelty changes attention and investigation value; it does not change truth.

## Applicability and business relevance

External evidence can establish what happened elsewhere. It does not establish that the active business has the same audience, assets, economics, capabilities, market, customer behavior, or expected outcome.

Before expensive research, testing, or adoption, evaluate:
- active Objective and likely business value;
- domain mechanism and applicability conditions;
- evidence strength, independence, freshness, and causal ambiguity;
- implementation cost, reversibility, policy, customer harm, and operational risk;
- what new information a test would actually provide.

## From signal to learning

Use the narrowest justified state:
`SourceRecord -> Observation -> Insight -> Opportunity / Experiment -> OutcomeEvaluation -> Learning`.

A promising uncertain claim normally remains a hypothesis or candidate Insight until stronger evidence or an active-business test exists. Promotion to durable Learning must follow Core learning governance. Negative, null, contradictory, and superseding evidence must remain inspectable.

No external discovery automatically authorizes a customer-facing claim, operational mutation, policy change, or BusinessOS product-file change. Execution still requires the normal ActionPacket, authorization, ChangeEvent, verification, and outcome pathways.
