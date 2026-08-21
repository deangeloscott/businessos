---
id: customer.evidence-collection.survey-design
type: playbook
version: 1.3.0
owner_system: customer-intelligence
risk: low
autonomy_ceiling: 2
reads:
- Insight
- Observation
writes:
- Asset
- ActionPacket
capabilities:
  required:
  - none
  optional:
  - survey.read
context:
- AudienceSegment
- Objective
---
# Customer Survey Design

## Purpose
Design a survey whose questions, scales, sample, and analysis can answer the defined customer research question.

## Business Outcome
Collect structured customer evidence without introducing avoidable wording, response, or analysis bias.

## Run When
Run when a research plan requires a survey rather than interviews or existing evidence alone.

## Process
1. [AI] Define the decision, constructs to measure, population, and how each response will be used before writing questions.
2. [AI] Select question types and scales appropriate to the construct; avoid asking respondents to quantify things they cannot reliably know.
3. [HYBRID] Remove leading, loaded, double-barreled, ambiguous, exhaustive-list, and unnecessary demographic questions.
4. [AI] Order questions to reduce priming and fatigue; place sensitive/optional questions only when necessary.
5. [DETERMINISTIC] Define branching, required/optional fields, randomization where useful, and response validation.
6. [AI] Define the analysis/segmentation plan and minimum coverage before fielding so analysis is not reverse-engineered after results.
7. [HYBRID] Pilot the survey or perform cognitive QA for high-impact studies, then revise before launch.
