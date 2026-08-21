---
id: content.qa.editorial
type: playbook
version: 1.1.0
owner_system: content-synthesis
risk: low
autonomy_ceiling: 4
reads:
- Asset
- WorkRequest
writes:
- Asset
- VerificationRecord
capabilities:
  required:
  - none
  optional:
  - none
context:
- Brand
---
# Editorial QA

## Purpose
Ensure the finished communication is clear, coherent, useful, non-repetitive, and appropriate to audience/context.

## Business Outcome
Create or improve editorial qa so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Run when an Opportunity or WorkRequest requires editorial qa and existing Assets do not already satisfy the communication need.

## Process
1. [AI] Compare the asset against its brief/WorkRequest and identify any missing promised information, logical gaps, repetition, unsupported leaps, or irrelevant sections.
2. [AI] Review structure, transitions, examples, specificity, terminology, readability, and whether the audience can act/understand without hidden context.
3. [HYBRID] Check format/platform-native expectations and whether attention devices serve rather than distort the message.
4. [AI] Remove filler, clichés, redundant summaries, vague claims, and unnecessary jargon while preserving intended voice.
5. [HYBRID] Confirm required CTA/content action is natural and consistent with the objective.
6. [DETERMINISTIC] Record QA result and required corrections before release.
