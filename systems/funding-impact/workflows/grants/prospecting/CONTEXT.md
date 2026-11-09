---
id: funding.grants.prospecting
type: workflow
owner_system: funding-impact
reads:
- Business
- BusinessClaim
- Objective
- Opportunity
- SourceRecord
- Learning
writes:
- Opportunity
- SourceRecord
context:
- Business
- ProductService
- Objective
evidence_inputs:
- funder guidelines and calls for proposals, public grant databases and filings, past award records
---
# Grant Prospecting and Fit

## Purpose
Find grants the organization is eligible for and likely to win, and decide which are worth the effort.

## Business Outcome
A short, current, prioritized list of real funding opportunities, so time goes into applications with a genuine chance instead of long shots.

## Run When
Use when the organization wants grant funding, needs to refresh its pipeline, or is checking for new opportunities on a schedule. Not needed for a single opportunity the person already chose; go straight to the application.

## Process
1. [AI] Establish what makes the organization eligible: legal status (nonprofit, business, individual, school, agency, tribal or other), location, field, program areas, budget size and project stage. Use saved facts; ask only for what is missing.
2. [INTEGRATION] Search the sources that fit the organization: government opportunity listings, foundation and corporate giving programs, community foundations, field-specific funders, and public filings or award databases showing who funders actually supported. Use any connected grant database the person has; none is required.
3. [AI] For each candidate, read the funder's own guidelines. Check eligibility, geographic focus, priorities, typical award size, past grantees similar to this organization, deadlines, application stages (letter of inquiry, invitation only, full proposal) and reporting burden.
4. [HYBRID] Judge fit honestly: strong, possible, or poor, with the reason. Weigh award size and likelihood against application effort and any matching or compliance requirements. Note relationship opportunities such as contacting a program officer.
5. [DETERMINISTIC] Save worthwhile opportunities to a maintained collection with funder, program, amount, deadline (as the result's expiry), eligibility notes, fit, effort, source link and a status field (Prospect, Drafting, Submitted, Awarded, Declined) so the board view shows the pipeline. Keep the source and date for each fact.
6. [AI] Recommend the next few applications to pursue, the soonest deadlines, and any eligibility gaps the organization could close (for example a fiscal sponsor). Government applications usually require registrations, such as SAM.gov and Grants.gov in the United States, that can take weeks; flag them early.

## Proportionate Scope
A first search may cover a few strong-fit sources. Broaden to more funder types when the pipeline is thin or the organization's needs grow.

## Verification
- Eligibility and deadlines come from each funder's current published guidelines, with links and dates; uncertain items are marked for confirmation.
- Fit judgments give a reason and do not overstate odds.
- Closed or ineligible opportunities are not presented as open.
