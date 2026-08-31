---
id: customer.monitoring.theme-change
type: playbook
version: 1.1.0
owner_system: customer-intelligence
reads:
- Observation
- Insight
- SourceRecord
writes:
- Insight
- Observation
capabilities:
  required:
  - none
  optional:
  - customer_feedback.read
  - crm.opportunity.read
  - support.ticket.read
  - review.read
  - community.read
events:
  consumes:
  - none
  emits:
  - customer.insight.updated
schedule:
  class: recurring
  default: weekly
  configurable: true
---
# Customer Theme Change Monitoring

## Purpose
Detect material changes in customer concerns, language, criteria, or expectations without overreacting to noise.

## Business Outcome
Reduce uncertainty about customers through customer theme change monitoring, so downstream decisions reflect current customer evidence rather than assumption.

## Run When
Run when a decision requires current customer theme change monitoring and existing Customer Insights are missing, stale, too broad, or insufficiently supported.

## Process
1. [DETERMINISTIC] Refresh configured evidence windows and validate source coverage against the prior period.
2. [AI] Compare theme prevalence, intensity, language, segment mix, and new/vanishing themes against current active Customer Insights.
3. [HYBRID] Separate real theme change from seasonality, source-mix changes, campaign-driven discussion, or collection changes.
4. [AI] Identify active Insights that should be refreshed, narrowed, strengthened, or challenged.
5. [HYBRID] Require a materiality threshold tied to decision impact before notifying downstream systems.
6. [DETERMINISTIC] Update affected Insights and emit customer.insight.updated/contradicted when material.
