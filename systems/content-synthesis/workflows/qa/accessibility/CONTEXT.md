---
id: content.qa.accessibility
type: workflow
owner_system: content-synthesis
reads:
- Insight
- Opportunity
- WorkRequest
- ProofRecord
- Asset
- PlatformProfile
writes:
- Asset
- WorkRequest
context:
- Brand
- AudienceSegment
- Objective
- Offer
---
# Content Accessibility QA

## Purpose
Check whether the Asset can be perceived and understood by relevant users across common accessibility needs.

## Business Outcome
Reduce avoidable exclusion and improve clarity without treating accessibility as a post-production checkbox.

## Run When
Run before publication for visual, audio, video, document, or interactive Assets.

## Process
1. [DETERMINISTIC] Identify applicable accessibility needs by medium: captions/transcript, contrast, text alternatives, reading order, keyboard/interaction, motion, audio clarity, or document structure.
2. [DETERMINISTIC] Run available exact checks for contrast, caption presence/timing, heading/document structure, alt text presence, and file metadata.
3. [AI] Evaluate whether alt text/captions/transcripts communicate the actual information rather than merely labeling decorative objects.
4. [HYBRID] Inspect cognitive load, flashing/motion, color-only distinctions, jargon, and information conveyed only through audio/visual channel.
5. [AI] Prioritize issues that block understanding or action and define concrete fixes.
6. [DETERMINISTIC] Recheck corrected Asset and record residual limitations.
7. [HYBRID] Escalate formal compliance requirements to appropriate expert/process when needed.
