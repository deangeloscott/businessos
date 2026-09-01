---
id: content.strategy.platform-profile-refresh
type: playbook
owner_system: content-synthesis
reads:
- PlatformProfile
- SourceRecord
- Observation
- Learning
writes:
- SourceRecord
- Observation
- PlatformProfile
capabilities:
  required:
  - none
  optional:
  - social.observe
  - research.web.read
  - analytics.read
context:
- AudienceSegment
---
# Platform Profile Refresh

## Purpose
Build or refresh a sourced PlatformProfile so content decisions use current platform behavior instead of model memory or stale best-practice assumptions.

## Business Outcome
Reduce avoidable creative and distribution mismatch by grounding platform-native decisions in current evidence and business-specific performance Learning.

## Run When
Run when a consequential content decision lacks a current PlatformProfile, the profile is past its review window, or new evidence materially contradicts it.

## Process
1. [DETERMINISTIC] Define the exact platform/surface, market where relevant, profile freshness requirement, and decisions the profile must support.
2. [INTEGRATION] Retrieve current authoritative platform documentation where available, direct platform observations, and relevant business analytics/Content Learning.
3. [AI] Separate durable interaction/format behavior from speculative algorithm folklore and from business-specific performance patterns.
4. [HYBRID] Record current native behaviors, format constraints, attention/interaction patterns, distribution notes, contradictions, and confidence with source references.
5. [DETERMINISTIC] Set `observed_at`, an appropriate `review_after`, status, and supersession link/state where a prior profile exists.
6. [HYBRID] Validate that every consequential rule is either sourced, business-learned, or explicitly marked uncertain before publishing the PlatformProfile.
