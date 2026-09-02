---
id: seo.execution.local.nap-consistency
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- Observation
writes:
- SEOAssetState
- ChangeEvent
- Asset
evidence_inputs:
- location/profile data, local-result observations, and local competitors
---
# Business Identity / NAP Consistency

## Purpose
Keep the organization's public local identity accurate and coherent across owned and important third-party sources.

## Business Outcome
Reduce customer confusion and entity inconsistency without chasing trivial formatting differences or maximizing citation uniformity for its own sake.

## Use When
Use when names, addresses/service areas, phone numbers, URLs, hours, identifiers, or other important identity fields are wrong, stale, duplicated, or materially inconsistent across sources that matter.

## Process
1. Establish the canonical current business identity for each relevant location from reliable organization truth, including public name, address or service-area representation, phone(s), URLs, hours, and meaningful identifiers.
2. Inspect the important owned and third-party sources that customers, platforms, or data ecosystems actually use. Normalize variations enough to distinguish true inconsistencies from harmless formatting differences.
3. Classify each difference as acceptable formatting, outdated information, duplicate entity, wrong entity, unresolved uncertainty, or material inconsistency.
4. Prioritize corrections on sources with the greatest customer, ecosystem, or business impact rather than attempting to normalize every obscure citation.
5. If correction is requested and the host has the real account/channel access, submit, claim, or update through legitimate mechanisms and verify the published state. Otherwise prepare the correction without claiming execution.
6. After consequential moves, rebrands, phone/URL changes, mergers, or closures, preserve monitoring intent for sources where drift materially matters; the host/runtime owns recurring checks.

## Proportional Scope
Focus on identity fields and sources capable of affecting customers, local discovery, entity understanding, or operations. Ignore cosmetic variation that does not change meaning.
