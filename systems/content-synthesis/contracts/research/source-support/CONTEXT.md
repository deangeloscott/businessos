---
id: content.research.source-support
type: playbook
version: 1.1.0
owner_system: content-synthesis
risk: low
autonomy_ceiling: 4
reads:
- WorkRequest
- Insight
- SourceRecord
- Observation
writes:
- SourceRecord
- Observation
- WorkRequest
capabilities:
  required:
  - none
  optional:
  - research.web.read
  - document.read
---
# Content Source & Evidence Support

## Purpose
Fill source/evidence gaps needed to communicate an already valid idea accurately without recreating broad customer/competitor/industry research.

## Business Outcome
Create or improve content source & evidence support so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
When a content brief or WorkRequest identifies specific factual/example/source needs not satisfied by canonical intelligence.

## Process
1. [AI] List exact claims, examples, data, demonstrations, or expert evidence needed for the content job.
2. [DETERMINISTIC] Search canonical SourceRecords/Insights first and assess freshness/scope.
3. [HYBRID] If missing, route refresh to the semantic owner for customer/competitor/industry questions that materially require domain interpretation.
4. [INTEGRATION] Perform bounded source research for factual support, primary documents, examples, definitions, or citations needed for production.
5. [AI] Extract direct facts/quotes/data with source context and avoid creating foreign-domain strategic conclusions.
6. [DETERMINISTIC] Publish reusable Observations where useful and return source references to the content production run.
