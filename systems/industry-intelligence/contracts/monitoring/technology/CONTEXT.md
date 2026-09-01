---
id: industry.monitoring.technology
type: playbook
owner_system: industry-intelligence
reads:
- SourceRecord
- Observation
- Insight
writes:
- SourceRecord
- Observation
- IndustryEvent
- Insight
- PlatformChange
capabilities:
  required:
  - research.web.read
  optional:
  - research.web.read
  - news.read
  - alert.read
  - market_data.read
context:
- Business
- Market
- Objective
- ProductService
---
# Technology & Platform Change Review

## Purpose
Review technology/platform changes that may alter capabilities, customer expectations, channel behavior, dependencies, or business risk/opportunity.

## Business Outcome
Give the organization current, evidence-backed understanding of material technology/platform change without creating an AURA-owned watcher or notification router.

## Run When
Use when a current decision or saved monitoring intent needs fresh technology/platform evidence and existing organizational knowledge may be stale, incomplete, or unresolved. Any recurring execution is owned by the active harness/runtime.

## Process
1. [INTEGRATION] Retrieve the most relevant primary vendor/platform announcements, technical documentation, release notes, standards, and credible independent evidence for the current question using the host's available capabilities.
2. [AI] Extract what capability, policy, interface, availability, requirement, or behavior changed; who/what is affected; relevant dates; and any migration/deprecation conditions supported by the evidence.
3. [HYBRID] Separate announced/future capability from generally available current state, marketing claims from verified functionality, and observed behavior from inferred business impact.
4. [AI] Identify which active business products/services, markets, channels, customers, workflows, or dependencies may be affected and preserve uncertainty where applicability is not established.
5. [AI] Judge materiality and timing from the actual business decision, external effective dates, operational exposure, competitive implications, reversibility, and strategic upside rather than a generic urgency score.
6. [HYBRID] Preserve a current PlatformChange when the external platform/topic state has durable organizational value, using the shared versioned state path so materially unchanged rechecks can update verification without multiplying current objects. Preserve an IndustryEvent or Insight only when those meanings genuinely add value. Do not emit notifications or route work merely because a platform state changed.
7. [AI] When future rechecking matters, preserve the semantic reason, date/deadline, or condition worth revisiting. The active harness/runtime owns any actual reminder, recurring check, or notification.

## Verification
- Current versus announced/future platform state is explicit.
- Material claims trace to appropriate evidence.
- Business impact/applicability remains distinct from the external platform fact.
- Saved review intent is not represented as an active schedule or notification.

## Completion Criteria
- Future work can reuse the best current verified platform/technology state and understand why it may matter to this organization without depending on AURA runtime monitoring or routing.
