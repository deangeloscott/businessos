---
id: content.qa.brand
type: playbook
owner_system: content-synthesis
reads:
- Asset
writes:
- Asset
- VerificationRecord
capabilities:
  required:
  - none
  optional:
  - none
evidence_inputs:
- Business Constraints
context:
- Brand
---
# Brand Voice & Policy QA

## Purpose
Ensure content applies canonical Brand communication without inventing new brand rules or sacrificing clarity.

## Business Outcome
Create or improve brand voice & policy qa so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Run when an Opportunity or WorkRequest requires brand voice & policy qa and existing Assets do not already satisfy the communication need.

## Process
1. [AI] Compare asset language/visual behavior with canonical Brand voice, claims, prohibited language, examples, and applicable constraints.
2. [AI] Identify deviations in tone, vocabulary, level of formality, framing, visual identity, and claim style.
3. [HYBRID] Distinguish genuine brand violation from context-appropriate variation; brand consistency should not make every platform sound identical.
4. [AI] Revise only the parts necessary to align while preserving audience/platform fit and factual meaning.
5. [HYBRID] Escalate ambiguous or strategically significant brand conflicts as a context review rather than silently redefining Brand.
6. [DETERMINISTIC] Record QA result and version changes.
