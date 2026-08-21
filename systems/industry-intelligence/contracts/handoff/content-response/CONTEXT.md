---
id: industry.handoff.content-response
type: playbook
version: 1.2.0
owner_system: industry-intelligence
risk: low
autonomy_ceiling: 4
reads:
- IndustryEvent
- Insight
- Opportunity
- WorkRequest
writes:
- WorkRequest
capabilities:
  required:
  - none
  optional:
  - none
context:
- AudienceSegment
- Brand
- Objective
---
# Industry Event to Content WorkRequest

## Purpose
Delegate an approved Industry-owned communication action to Content Synthesis with a clean separation between verified facts, Industry interpretation, audience value, and creative execution.

## Business Outcome
Turn material external developments into timely, useful communication without letting Content re-research the event or Industry Intelligence dictate the creative format.

## Run When
Run only when an Industry-owned Opportunity/Action already requires communication and Content Synthesis is the appropriate executor; otherwise publish the Insight and let Content evaluate independent relevance.

## Process
1. [DETERMINISTIC] Confirm the originating Industry Opportunity/Action, verified IndustryEvent/Insight, affected audience, desired business outcome, timing/expiry, and that no equivalent WorkRequest already exists.
2. [AI] Prepare the factual basis: verified event summary, source refs, effective dates, unresolved facts, and claims that must not be exceeded.
3. [AI] Prepare the audience value: why it matters, practical implications, potential actions/protections/opportunities, and what is scenario versus confirmed fact.
4. [HYBRID] Specify communication objective, urgency, constraints, required sources/proof/disclosures, and success criteria without prescribing platform/format unless the originating Opportunity requires it.
5. [DETERMINISTIC] Create one Content WorkRequest linked to the Industry Opportunity/Action and canonical Insight; do not create a duplicate Content Opportunity.
6. [DETERMINISTIC] Route to Content intake/strategy and preserve the Industry owner as authority for event facts/interpretation while Content owns native expression.
7. [HYBRID] On return, verify that the produced Asset has not collapsed factual summary, interpretation, and speculation into one unsupported claim.
