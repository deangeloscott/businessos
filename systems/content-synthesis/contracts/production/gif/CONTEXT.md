---
id: content.production.gif
type: playbook
version: 1.2.0
owner_system: content-synthesis
risk: low
autonomy_ceiling: 4
reads:
- Insight
- Asset
- WorkRequest
- PlatformProfile
writes:
- Asset
capabilities:
  required:
  - none
  optional:
  - creative.animation.generate
  - creative.video.generate
  - video.render
context:
- AudienceSegment
- Brand
---
# GIF / Looping Motion Production

## Purpose
Create a short looping motion Asset that demonstrates, emphasizes, or explains one idea more effectively than a static image.

## Business Outcome
Add lightweight motion where it improves comprehension or attention without forcing a full video production workflow.

## Run When
Run when a WorkRequest or Content plan calls for a GIF/short loop for demonstration, reaction, UI/process illustration, visual proof, or repeated motion.

## Process
1. [AI] Define the one action/idea the loop must communicate and the target platform's file, duration, autoplay, caption, and accessibility constraints.
2. [AI] Choose source material or storyboard the minimum frames needed; avoid unnecessary narrative that belongs in a full video.
3. [HYBRID] Confirm factual/brand accuracy and permission for any source footage, screenshots, customer proof, or third-party material.
4. [INTEGRATION] Generate/edit/render the loop with smooth entry/exit and readable pacing, or create a manual production specification when tooling is unavailable.
5. [DETERMINISTIC] Optimize dimensions, duration, file size, frame rate, text legibility, and looping behavior for the intended surface.
6. [HYBRID] QA whether the loop communicates correctly without sound and whether a static fallback/alt explanation is needed.
7. [DETERMINISTIC] Save the Asset with source lineage and intended usage/platform metadata.
