---
id: content.qa.fact-check
type: playbook
owner_system: content-synthesis
reads:
- Asset
- SourceRecord
- Observation
- Insight
writes:
- Asset
- VerificationRecord
capabilities:
  required:
  - none
  optional:
  - research.web.read
  - document.read
---
# Fact & Source QA

## Purpose
Verify consequential factual claims against valid evidence and preserve uncertainty/attribution.

## Business Outcome
Create or improve fact & source qa so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Run when an Opportunity or WorkRequest requires fact & source qa and existing Assets do not already satisfy the communication need.

## Process
1. [AI] Extract consequential factual, quantitative, comparative, causal, regulatory, scientific, customer, and competitor claims from the asset.
2. [DETERMINISTIC] Map each claim to cited SourceRecord/Observation/Insight references and flag missing or stale support.
3. [HYBRID] Verify claims against the appropriate authoritative source type and current state; distinguish fact from inference/opinion.
4. [AI] Check whether wording overstates scope, causality, certainty, recency, or generality relative to evidence.
5. [HYBRID] Correct, qualify, attribute, or remove unsupported claims and ensure numbers/units/dates are internally consistent.
6. [DETERMINISTIC] Record verification results and unresolved claims requiring human/domain review.
