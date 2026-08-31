---
id: core.context.bootstrap-business
type: playbook
version: 1.11.0
owner_system: core
reads: []
writes:
- Business
- Brand
- PreferenceProfile
- ProductService
- Offer
- AudienceSegment
- Market
- Objective
- SourceRecord
- Observation
- ContextUpdateProposal
capabilities:
  required:
  - none
  optional:
  - webpage.fetch
  - webpage.snapshot
  - research.web.read
  - document.read
  - crawler.run
  - browser.interact
  - social.observe
  - review.read
  - news.read
  - search.observe
  - business.data.query
  - business.data.explain
context: []
subcontracts:
  required:
  - core.context.owned-business-discovery
---
# Bootstrap Business Context

## Purpose
Turn minimal business identity and available evidence into a usable initial Business Context, using adaptive owned-business discovery before asking the user for information that can be safely obtained.

## Business Outcome
Let a new BusinessOS copy begin useful work from as little as a business name, URL, and goal while preserving evidence, uncertainty, and modular ownership.

## Run When
When initializing a new business instance or materially rebuilding its base context from authoritative sources.

## Process
1. [HYBRID] Confirm the active business identity, primary website/domain if known, supplied files, explicit user statements, installed modules, current goal, non-negotiable brand/operating constraints, and the user's full original request. If the instance does not exist, initialize it with `scripts/init_business.py`. Persist explicit user-supplied facts first as canonical objects (prefer `scripts/bootstrap_explicit_context.py` for initial setup); repeated `--source-file` inputs preserve multi-source provenance without a hand-built merged source. If the supplied setup includes explicit organization Brand instructions, create a small grounded Brand manifest and pass it with `--brand-profile-file` (or use the grounded facts `brand` field) so first-class Brand context exists before residual work; do not flatten those instructions into generic claim constraints. If the active user supplies reusable preferences, persist the applicable PreferenceProfile in the same onboarding handoff before any downstream Run. Do not turn these into free-form profile Markdown.
2. [HYBRID] If an authoritative connected business-data capability is already bound, use `core.data.query-business-truth` first for supported first-party context that can reduce questions (for example connected domains/channels, conversion definitions, tracking/measurement coverage, or other governed business facts). Treat unavailable/missing provider data as unknown, not zero/absent. Then use `core.context.owned-business-discovery` only at the smallest sufficient depth. If no authoritative owned-surface anchor (domain/profile/file/connected source) is supplied or confidently resolved, record those surfaces as **unknown/unverified** rather than launching broad searches to prove absence. Rapid depth is enough to unblock a bounded job; Standard is for normal setup when useful anchors exist; Comprehensive is only when the user asks the system to learn/map the business broadly.
3. [AI] Consolidate explicit and discovered first-party facts into candidate Business, Brand, ProductService, Offer, AudienceSegment, Market, and Objective objects; keep observed facts separate from inference, public perception, stale information, and assumptions. Omit unknown fields. Never invent plausible geography, pricing, margins, KPIs, audiences, offers, value propositions, targets, performance, or commercial terms simply to make context complete.
4. [AI] Capture durable brand expression cues including voice, positioning, visual identity, content style, channel preferences, approved examples, prohibited styles, and stated rules. Explicit organization-supplied Brand notes may be grounded during bootstrap; cues inferred from public assets remain provisional until authoritative enough to adopt. Keep personal/team working preferences in PreferenceProfile rather than silently turning them into organization Brand truth.
5. [AI] Identify material unknowns or contradictions that would change near-term work. Before asking, reuse any current authoritative answer already stored for this business. Ask only for information that cannot safely be discovered/inferred/reused and materially affects execution, authorization, compliance, economics, or brand identity; persist durable answers at the correct scope so later workflows do not ask again.
6. [HYBRID] Create evidence-supported initial context where authority is clear as schema-valid canonical JSON objects under the active business instance, with lineage to SourceRecord/evidence where applicable. Supplemental Markdown may be created for humans but never substitutes for declared canonical writes. For ambiguous business decisions, commercial terms, inferred facts, or inferred changes to existing canonical context, create a ContextUpdateProposal/Observation as appropriate instead of silently deciding for the business.
7. [DETERMINISTIC] Validate schemas, business isolation, references, IDs, installed-module state, and source lineage with `scripts/validate_business.py <business-id> --require-context`; reject unsupported canonical writes. Do not run `tests/run_distribution.py` against the active business workspace.
8. [AI] Return a concise business map: what is known, provisional, contradictory, unknown, and what surfaces were covered. Never report an unverified/missing surface as nonexistent merely because it was not supplied or a search did not find it. Then inspect the user's original request: if setup was a prerequisite and any requested goal/problem remains unresolved, route and continue it automatically **within the original action scope**. A broad request such as "what should we do next?" or "grow profitably" continues through `core.opportunity.discover-next-best-work`; do not stop with a menu of internal modules/tactics and do not implement the resulting tactic unless execution was also requested/authorized.

## Verification
The instance contains enough validated Business Context for installed modules to begin bounded work from minimal user input, and the user was not asked to manually supply information that credible discovery already established.
