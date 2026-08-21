---
id: core.context.bootstrap-business
type: playbook
version: 1.8.0
owner_system: core
risk: medium
autonomy_ceiling: 2
reads: []
writes:
- Business
- Brand
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
1. [HYBRID] Confirm the active business identity, primary website/domain if known, supplied files, explicit user statements, installed modules, current goal, and non-negotiable brand/operating constraints. Do not require a questionnaire when discovery or durable saved context can resolve the information; follow `core/policies/context-reuse-and-question-minimization.md` before asking.
2. [HYBRID] If an authoritative connected business-data capability is already bound, use `core.data.query-business-truth` first for supported first-party context that can reduce questions (for example connected domains/channels, conversion definitions, tracking/measurement coverage, or other governed business facts). Treat unavailable/missing provider data as unknown, not zero. Then use `core.context.owned-business-discovery` at the smallest sufficient depth: Rapid to unblock a bounded job, Standard for normal setup, or Comprehensive when the user asks the system to learn/map the business broadly.
3. [AI] Consolidate explicit and discovered first-party facts into candidate Business, Brand, ProductService, Offer, AudienceSegment, Market, and Objective objects; keep observed facts separate from inference, public perception, stale information, and assumptions.
4. [AI] Capture durable brand expression cues including voice, positioning, visual identity, content style, channel preferences, approved examples, prohibited styles, and stated rules. Cues inferred from public assets remain provisional until authoritative enough to adopt.
5. [AI] Identify material unknowns or contradictions that would change near-term work. Before asking, reuse any current authoritative answer already stored for this business. Ask only for information that cannot safely be discovered/inferred/reused and materially affects execution, authorization, compliance, economics, or brand identity; persist durable answers at the correct scope so later workflows do not ask again.
6. [HYBRID] Create evidence-supported initial context where authority is clear. For ambiguous business decisions, commercial terms, or inferred changes to existing canonical context, create a ContextUpdateProposal instead of silently deciding for the business.
7. [DETERMINISTIC] Validate schemas, business isolation, references, IDs, installed-module state, and source lineage; reject unsupported canonical writes.
8. [AI] Return a concise business map: what is known, provisional, contradictory, unknown, what surfaces were covered, and the highest-value next jobs available from installed modules.

## Verification
The instance contains enough validated Business Context for installed modules to begin bounded work from minimal user input, and the user was not asked to manually supply information that credible discovery already established.
