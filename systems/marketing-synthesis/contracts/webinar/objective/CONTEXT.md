---
id: marketing.webinar.objective
type: playbook
version: 1.3.0
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
- WorkRequest
- Asset
capabilities:
  required:
  - none
  optional:
  - creative.text.generate
  - tracking.read
  - conversion.read
  - marketing.performance.read
  - experiment.run
  - cms.page.publish
  - email.send
  - social.ad.publish
context:
- Brand
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Webinar Objective and Audience

## Purpose
Define the commercial and educational job of a webinar before building teaching or slides.

## Business Outcome
Ensure the webinar creates real audience value while supporting a specific qualified commercial outcome.

## Run When
Run before designing a sales-oriented webinar.

## Process
1. [DETERMINISTIC] Resolve AudienceSegment, source/registration context, Offer, Customer Insights, objective/economics, and existing webinar performance.
2. [AI] State the audience’s starting problem/knowledge, the useful transformation they should receive even without buying, and the desired commercial action.
3. [AI] Define who the webinar is for/not for, prerequisite knowledge, and the one core topic/promise it can credibly deliver.
4. [AI] Identify persuasion barriers the webinar—not merely follow-up—must resolve.
5. [HYBRID] Ensure educational promise is substantial and not withheld value disguised as a pitch.
6. [DETERMINISTIC] Define registration, attendance, engagement, CTA, conversion, and quality metrics plus session constraints.
7. [AI] Produce objective/audience brief for teaching/persuasion design.
