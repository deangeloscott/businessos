---
id: customer.evidence-collection.interview-guide
type: playbook
owner_system: customer-intelligence
reads:
- Insight
- Observation
writes:
- Asset
capabilities:
  required:
  - none
  optional:
  - document.read
context:
- AudienceSegment
- Objective
---
# Customer Interview Guide Design

## Purpose
Create a neutral interview guide that elicits concrete customer experience before abstract preference.

## Business Outcome
Produce interviews capable of revealing actual decisions, context, language, and causality without leading the participant.

## Run When
Run after a customer research plan identifies interviews as a required evidence method.

## Process
1. [AI] Convert each research question into observable experiences, decisions, events, or comparisons the participant can describe.
2. [AI] Order questions from context and recent concrete behavior to motives, alternatives, outcomes, and reflection.
3. [AI] Include probes for what happened before, what changed, alternatives considered, decision criteria, friction, and consequences.
4. [HYBRID] Remove leading, loaded, double-barreled, hypothetical-leading, and product-pitch questions.
5. [AI] Add contradiction probes and questions that can falsify the current hypothesis.
6. [AI] Tailor optional probes by segment/journey while keeping comparison questions consistent where needed.
7. [DETERMINISTIC] Produce interviewer instructions for consent, recording, note-taking, time allocation, and evidence labeling.
