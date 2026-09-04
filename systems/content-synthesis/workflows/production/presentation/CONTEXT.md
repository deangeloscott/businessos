---
id: content.production.presentation
type: workflow
owner_system: content-synthesis
reads:
- WorkRequest
- Opportunity
- Insight
- SourceRecord
- Asset
writes:
- Asset
- Observation
context:
- AudienceSegment
- Brand
---
# Presentation / Slideshow Production

## Purpose
Build a presentation that supports a live or asynchronous audience journey instead of turning a document into slides.

## Business Outcome
Create or improve presentation / slideshow production so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Run when an Opportunity or WorkRequest requires presentation / slideshow production and existing Assets do not already satisfy the communication need.

## Process
1. [AI] Define audience, setting, presenter/no-presenter mode, decision/learning objective, duration, and expected prior knowledge. Draw on current message, narrative, evidence/proof, outline, visual-direction, or related operating knowledge only when it improves the result.
2. [AI] Build narrative arc and section sequence around audience questions/decisions rather than source-document headings.
3. [AI] Assign one main message per slide; choose charts, diagrams, examples, demonstrations, quotes, or sparse text according to the slide job.
4. [HYBRID] Separate speaker notes from visible slide content and prevent slide text from becoming a transcript.
5. [INTEGRATION] Render slides through available presentation capability or preserve a complete slide-by-slide production specification when rendering is unavailable and the specification remains useful.
6. [HYBRID] Check narrative continuity, readability at viewing distance, data accuracy, source attribution, brand, and timing. Draw on pre-publish QA operating knowledge when an additional integrated review is useful.
7. [DETERMINISTIC] Save the useful final presentation Asset and supporting notes/source references.
