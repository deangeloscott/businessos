# Keeping Knowledge Current

An ongoing watch should leave the organization knowing more, not holding more. New information is folded into what is already known; it is added only when it is genuinely new. This applies to every repeated check: research, competitors, prices, grants, regulations, local search, content, opportunities.

The model judges meaning (relevance, identity, what a source shows, how it relates to current findings). The harness runs and schedules the work. AURA keeps the records consistent: stable identities, statuses, dates, sources checked, links and notifications. AURA never filters meaning with keywords.

## Two layers

- **Things** — the items a watch tracks (papers, grants, competitors, prices, posts, opportunities). They live in the watch's maintained collection, where they appear, change, expire or are replaced. See [projects and results](../../docs/projects-and-results.md).
- **Understanding** — what the things add up to: findings such as "method X beats Y on reasoning benchmarks" or "two competitors now offer same-day service". Findings are `Insight` records linked to the collection with `extensions.businessos.collection_refs`. They carry their status and evidence, and they are what future work retrieves.

A grants watch is mostly things; a research watch is mostly understanding; a competitor watch is both. Not every run produces a finding. Do not create findings merely because a run happened.

## Each run

1. **Ask for what is new.** Read the collection first (`workspace_collections.py show`): its purpose, current entries, latest check, findings, source setting and dismissed results. Use each source's own filters (category, keyword, date, "posted since", newest first) and the last check date. Start with unread links in the latest check’s `coverage.deferred`, even when they predate that check.
2. **Triage on the cheapest useful signal.** Title, abstract, snippet, opening paragraph, publisher, or who cites it. When an item has no summary, read its opening. Keep borderline items; the full read decides. Dismissed results show what the person does not want. An item skipped wrongly can return when later sources cite it.
3. **Read only what passed, within a budget.** If more items pass than a proportionate run should read, read the most promising and leave the rest for the next run, recording their links in `coverage.deferred`. Carry each link forward until it is read or deliberately dismissed. Send an empty deferred list when all are resolved. A watch should never exhaust the person's plan or context.
4. **Update the things.** Apply the collection with stable identities, real coverage and a reason for each material change. Unchanged checks record coverage only.
5. **Fold into understanding.** For each item that matters, decide what it does to current findings:
   - **supports** or **extends** a finding: add an evidence link (`supports` or `extends`) and refresh `reviewed_at`;
   - **challenges** a finding: add a `contradicts` link; mark the finding `contradicted` when the conflict is material and unresolved;
   - **replaces** a finding: save the new finding with `extensions.businessos.supersedes` naming the old one, and mark the old one `superseded` (it stays as history and leaves ordinary retrieval);
   - **adds** a genuinely new finding;
   - **changes nothing** (the most common outcome).

   Status follows the evidence: `candidate` for a single or unverified source, `supported` when inspected evidence supports it, `contradicted` while materially challenged, `stale` when it is due for review and not yet rechecked. Strength comes from visible factors: independent sources (a repost is not a second source), source quality, replication, and conflicts. State them briefly in the finding. Keep the source's claim separate from the conclusion drawn from it, and never state a conclusion more strongly than its evidence.
6. **Set when to look again.** Give each finding `extensions.businessos.review_after` matching how fast the subject moves: weeks for news and prices, months for research.
7. **Report only real change.** A run with material changes is surfaced to the person once; a run without them records coverage and stays quiet.

New evidence for a finding is saved with `scripts/persist_research_bundle.py` (sources, observations and insights in one validated write). Changes to an existing finding (status, links, review date, supersession) use `scripts/remember.py` with its `object_ref`.

## Sources

Keep sources at the collection's `source_copies` setting:

- **`quotes`** (default): a stable link, the citation, and the exact passages that support each part of a finding, with their fingerprint. Quotes are verbatim and as short as checking allows: the sentence with the result, the sentence with the limitation. This is support-grade under [research evidence](research-evidence.md).
- **`full`**: also keep a copy or snapshot of the whole source in the workspace.

Whatever the setting, keep a copy or snapshot when a finding depends on a **fragile** source: one likely to change or disappear. Examples: social posts, forums, personal pages, live coverage, pricing and competitor pages that change by design, and reporting on contested topics or conflict regions where removal or suppression is plausible. Stable sources include versioned papers (arXiv, DOI) and official registries. Save a public archive link (for example the Internet Archive) when one exists, and look for independent sources on contested topics. A source that later disappears is recorded as a fact, never as proof its claim was false. A bare link is a lead, not support. Copies stay private to the workspace.

## Upkeep

Upkeep runs inside the watch's own task when it is due (about monthly, or as the person prefers), not as a second task. Mark it with `"upkeep": true` in that run's collection apply so the next run knows when it last happened. Upkeep looks only at:

- findings past `review_after`, which are rechecked, confirmed, marked `stale` or retired;
- findings challenged since the last upkeep;
- findings that overlap, which are merged with the older one marked `superseded`;
- dismissed results, which sharpen triage.

Do not rewrite the watch's purpose without the person; suggest a change in the run's report instead. Nothing is deleted. Evidence that no current finding cites simply stops appearing in current views.

## Keep the pieces connected

- Bind the scheduled task that runs a watch to its collection, so the collection shows what keeps it current and the task shows what it updates: `python scripts/workspace_projects.py bind --business-id <id> --input '{"kind":"task","ident":"<native task id>","collection":"<collection id>"}'`. Put the output of `python scripts/workspace_collections.py instructions --business-id <id> --id <collection id>` in the task's instructions so every run knows its collection and this method. Tasks created through AURA's scheduled-task form get both automatically.
- When a single source deserves its own memory (a particular competitor, regulator or publication), keep it as a `SourceProfile` with `extensions.businessos.collection_refs` naming the watch.
- Findings and source memory belong to one organization. Findings read from another workspace are read-only context: cite where they came from and never write or link across workspaces.

## Cadence and cost

Prefer the slowest cadence that stays useful; weekly is a sensible default. Each run happens in its own scheduled session, so it does not use the person's chat context, and a smaller model is often enough for triage. Later work retrieves a few current findings, not the whole history.
