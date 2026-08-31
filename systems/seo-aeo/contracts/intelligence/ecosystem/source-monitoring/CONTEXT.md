---
id: seo.intelligence.ecosystem.source-monitoring
type: playbook
version: 1.1.0
owner_system: seo-aeo
reads:
- type: Insight
  owner_system: industry-intelligence
- type: Learning
  owner_system: seo-aeo
writes:
- SourceRecord
- Observation
- Event
capabilities:
  required:
  - research.web.read
  optional:
  - search.observe
  - news.read
  - document.read
schedule:
  class: recurring
  default: weekly
  configurable: true
evidence_inputs:
- SEO ecosystem source map
- Official search answer engine guidance
---
# SEO Ecosystem Source Monitoring

## Purpose
Continuously capture material official search/answer-engine changes and credible SEO/AEO research as reusable sources and observations without automatically changing operating rules.

## Business Outcome
Keep SEO/AEO strategy current, evidence-governed, policy-safe, and connected to measurable organic and business outcomes without creating a parallel strategy-evidence store.

## Run When
Run on the configured ecosystem-monitoring cadence or when a priority source changes.

## Do Not Run When
Do not treat a publication, practitioner opinion, competitor behavior, or one business result as a validated tactic by itself. Do not use private cross-business evidence unless Core System Learning governance explicitly permits it.

## Process
1. [AI] Maintain a source map grouped by official documentation/changelogs, primary research, replicated practitioner evidence, case studies, communities, and speculative commentary; record which fact types each source can credibly support.
2. [INTEGRATION] Retrieve new or changed items at the configured cadence and record publication/event time separately from retrieval time.
3. [DETERMINISTIC] Deduplicate syndicated or repeated items, preserve the original source identity, and record a content/version hash when useful.
4. [AI] Classify each material item by affected SEO/AEO mechanism, surface, market applicability, urgency, and which existing contracts or Learnings could be affected.
5. [HYBRID] Record direct factual statements as Observations with SourceRecord lineage; do not turn recommendations or speculative claims into facts.
6. [HYBRID] Route distinct material strategy claims to claim extraction, evidence assessment, and official-policy contradiction checking before they can influence standard guidance.

## Decisions / Routing
- Route material source claims → `seo.intelligence.ecosystem.claim-extraction`.
- Route urgent operational/policy risk → relevant SEO Incident or Core policy review.

## Verification
- Validate every canonical object written, preserve SourceRecord/Observation lineage, and keep evidence strength, conclusion confidence, policy status, and risk as separate dimensions.
- Any later external state mutation must use an ActionPacket, ChangeEvent, and independent VerificationRecord.

## Measurement
- Strategy claims become stronger only through relevant observations, experiments, OutcomeEvaluations, replication, or authoritative policy evidence; popularity and confidence language are not outcome evidence.

## Learning
- Maintain SEO-specific strategy knowledge as SEO Domain Learning. Propose broader Business or System Learning only when evidence and applicability justify the broader scope.

## Failure / Fallback
- If a source cannot be retrieved automatically, create a manual evidence-retrieval Action or use another authoritative source; do not invent the missing evidence.
- If evidence remains contradictory or insufficient, preserve the uncertainty and keep the claim at hypothesis/experimental maturity instead of forcing a conclusion.

## Completion Criteria
- Outputs use current Core Observation/Insight/Experiment/Learning objects rather than legacy strategy-evidence object.
- Source provenance, contradictory evidence, applicability, confidence, risk, and policy status remain inspectable.
- No tactic is promoted, deprecated, or blocked for a reason that cannot be traced to evidence or policy.
