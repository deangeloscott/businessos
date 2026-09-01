---
id: core.context.owned-business-discovery
type: playbook
owner_system: core
reads:
- Business
- Brand
- ProductService
- Offer
- AudienceSegment
- Market
- Objective
- SourceRecord
- Observation
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
  - crawler.run
  - browser.interact
  - research.web.read
  - social.observe
  - review.read
  - news.read
  - search.observe
  - document.read
  - business.data.query
  - business.data.explain
context:
- Business
- Brand
- ProductService
- Offer
- AudienceSegment
- Market
- Objective
---
# Adaptive Owned Business Discovery

## Purpose
Build an evidence-backed map of the organization and its owned/official surfaces only to the depth that can materially improve the current work or future reuse.

## Business Outcome
Reduce repeat questions and improve business context while preserving the difference between authoritative owned facts, provisional inference, public perception, and unknowns.

## Run When
Use when broader owned-business context is genuinely useful—for example during deliberate onboarding, after material organization changes, or when the current job depends on first-party facts not already known.

## Process
1. [AI] Choose discovery depth from the actual decision/job. A bounded task may need only one surface or fact; a broader organization-mapping request may justify deeper coverage. Do not perform exhaustive onboarding merely because discovery tools are available.
2. [HYBRID] Establish authoritative first-party anchors from explicit user statements, supplied files, known primary domains/properties, and relevant connected first-party sources. Reuse current evidence before asking the user or rediscovering the same fact. If a surface is not supplied and cannot be confidently resolved, keep it **unknown/unverified**; search misses are not proof of absence.
3. [HYBRID] When a credible owned anchor exists, inspect only the relevant surfaces—such as website navigation, sitemaps, products/services, offers/pricing, proof/case studies, resources, legal/about/contact, locations, help/docs, conversion paths, or connected business-data results—to the depth warranted by the current question.
4. [AI] Resolve whether external profiles/listings actually belong to the organization using first-party links and corroborating identity evidence. Exact identifiers/URLs may be handled mechanically; real-world identity remains model/user judgment and similar names alone are insufficient.
5. [AI] Structure explicit/verified owned facts into the appropriate Business/Brand/ProductService/Offer/AudienceSegment/Market/Objective context. Keep reputation, reviews, social discussion, search presentation, news, and other third-party/public observations distinct from what the organization officially is or claims.
6. [AI] Compare newly observed state with current canonical context. Update established truth when authority/evidence supports it. Use `ContextUpdateProposal` only when an unresolved candidate change to existing durable context is itself useful to remember; it is not a required change-control or approval step.
7. [AI] Identify any additional domain-specific research that could materially improve the current request. The active model/user chooses whether and how to do that work; owned-business discovery does not route tasks merely because modules/playbooks are installed and external research is never a substitute for missing first-party truth.
8. [DETERMINISTIC] Persist exact source references, retrieval timestamps, bounded snapshots/hashes where useful, and schema-valid context/evidence chosen by the model/user. Keep large/raw operational histories in their authoritative systems. The model/user decides when additional discovery is unlikely to improve the job; deterministic AURA validates what is saved.

## Verification
- Material owned-business facts are traceable to authoritative or explicitly qualified evidence.
- Owned facts are not conflated with public perception, inference, or search misses.
- Real-world identity, relevance, freshness, and stopping depth remain model/user judgments rather than deterministic routing or text matching.
- ContextUpdateProposal is optional unresolved-context memory, not an approval lifecycle.

## Completion Criteria
- The current work has the smallest sufficient first-party/owned context that could materially improve it, with checked/skipped/unavailable/unknown surfaces represented truthfully and no unnecessary onboarding or routing ceremony.
