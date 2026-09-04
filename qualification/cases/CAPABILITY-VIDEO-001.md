# CAPABILITY-VIDEO-001 — Level 4 Dependent Media Outcome Quality

## Purpose
Test whether a capable model/harness using AURA can fulfill one ordinary request that creates a new product image and then uses that exact new image as the grounded visual source for a real short-form video, while preserving the organizational continuity and lineage that materially help future work.

This is a maintainer-side qualification case. The candidate must not see this file, the hidden target Workflow, evaluator criteria, checkpoints, prior runs, or scoring metadata.

## Layer
Level 4 — medium-specific outcome quality with dependent media composition.

## Hidden target
`content.production.short-video`

## Fixture
`northline-commerce` with supplied first-party product reference media.

## Candidate-visible request
For Northline Coffee, use the supplied Discovery Box product reference image to create a new polished lifestyle product image for social use, then use that **new image you created** as the visual source for a polished 10–15 second vertical short-form video. In the still image, keep the actual product materially faithful to the supplied reference—the cream box silhouette, NORTHLINE wordmark, DISCOVERY BOX label, three-pouch count, and rust/olive/charcoal pouch appearance should remain recognizable—while placing it in a warm, natural morning coffee setting with tasteful premium-but-unpretentious art direction. Then turn that derived image into the video with subtle purposeful motion, restrained on-screen text, and audio or ambience when useful. The video should communicate the grounded Discovery Box idea that a customer can try three rotating coffees before committing to full bags, without inventing sourcing claims, tasting claims, health claims, discounts, customer outcomes, or other product facts. Use the strongest image/video tools genuinely available in the environment; if a dedicated image-to-video method is unavailable, use the strongest truthful rendering/animation path that still produces an actual playable video when possible. Preserve the supplied source image, the new derived image, and the final video as reconstructable stages of the work so it is clear which image the video came from. Inspect the derived image before using it downstream, and inspect the actual final video for product-appearance drift, visual artifacts, text/crop/safe-area problems, timing, audio, and source-to-video continuity before completion. Do not publish, send, or contact anyone.

## What Level 4 is testing
This is deliberately a **single-request dependent chain**, not two separate user turns.

The requested outcome is:

1. supplied first-party product image;
2. newly created product-image Asset or durable artifact reference;
3. final video derived specifically from step 2.

The intermediate image matters because it is both a real deliverable and the exact source for the downstream video. Preserve it when that lineage and future reuse are materially valuable; do not require a Run or other execution record merely to make it durable.

Preferred work pattern:
1. Resolve Northline business, offer, brand, and the supplied product reference image from the ordinary workspace.
2. Inspect the supplied reference and identify material appearance constraints that should not drift.
3. Create the new lifestyle product image with the strongest appropriate image-generation/editing method actually available.
4. Inspect the resulting image for package count, text/logo integrity, product-shape/color continuity, obvious generation artifacts, crop, and brand fit; correct material problems before downstream use.
5. Preserve the derived image as an Asset or durable artifact reference with enough source/provenance to reconstruct its relationship to the supplied reference when future work benefits.
6. Use that exact derived image—not an independently reimagined product—as the grounded visual source for the requested video.
7. Create the actual playable 10–15 second vertical video when the environment supports video/image-to-video/render execution. If direct image-to-video is unavailable, another truthful animation/render path may satisfy the request if it genuinely produces the video and preserves the derived image as its visual basis.
8. Inspect the final video itself for source-image continuity, product drift, broken text/glyphs, crop/safe-area issues, motion artifacts, duration, audio quality where present, and unsupported audience-facing claims; correct material problems when possible.
9. Preserve the final video Asset/reference and enough lineage/provenance/evidence for future work to reconstruct source image → derived image → video when that continuity is materially useful.
10. Complete the entire original request in one user-visible outcome unless a real external constraint prevents a required result.

## Evaluation emphasis
The professional judge should inspect the supplied product reference, newly created still, and final video together.

- **Chain completion:** Did one request actually result in both the new image and final video when the environment could create them?
- **Intermediate artifact integrity:** Is the newly created image a real reusable artifact rather than disposable scratch when its lineage/future reuse matters?
- **Lineage:** Can a reviewer reconstruct source reference → derived image → video from preserved artifacts/state without relying only on the candidate's prose claim?
- **Downstream source fidelity:** Does the video actually use the newly created image as its grounded visual source/reference?
- **Product appearance integrity:** Are the cream box, NORTHLINE wordmark, DISCOVERY BOX label, three-pouch count, and rust/olive/charcoal pouch appearance materially preserved unless a clearly justified creative choice explains a difference?
- **Image quality:** Is the derived lifestyle image polished, plausible, brand-appropriate, compositionally strong, and free of material generation defects?
- **Video quality:** Is the final video genuinely playable, purposeful, visually coherent, and appropriate to the requested short duration rather than merely a file-format trick?
- **Motion continuity:** Does motion enhance the approved still without causing product morphing, duplicate/missing packages, logo/text corruption, or unexplained scene identity changes?
- **Message/claim discipline:** Does the content stay within grounded Northline product truth and avoid invented sourcing, tasting, health, discount, outcome, or performance claims?
- **Audio/text execution:** Where audio/on-screen text is used, is it legible/intelligible, restrained, timed appropriately, and consistent with the visible product/story?
- **Tool truthfulness:** Did the model/harness use genuinely available image/video/render methods or state a real limitation without claiming nonexistent execution?
- **Final-output inspection:** Were both the actual derived still and final video inspected and material problems corrected where possible?
- **Durable continuity:** Does AURA preserve the useful artifacts/lineage/provenance accurately when they matter later, without requiring a Run, QA object, capability record, or completion-evidence profile merely to prove the work happened?

## Pass interpretation
A strong pass demonstrates more than isolated image generation or isolated video rendering. It shows AURA's organizational memory and operating knowledge can support a dependent media job while the active model/harness performs the actual generation, rendering, inspection, and tool selection.

This is evidence for same-request media composition, not proof of cross-session or cross-harness continuity. A later reliability test may deliberately create the image in one session/harness and ask another session/harness to continue from the persisted Asset.

This does not prove real-world views, watch time, shares, orders, repeat purchase, or revenue. Those require authorized publication and subsequent measurement.

## Non-goals
- Do not require a specific image model, video model, editor, codec implementation, voice provider, or proprietary AURA renderer.
- Do not require direct generative image-to-video if another available truthful method can create the requested playable video from the derived image.
- Do not test generic image/video generation as an AURA-owned capability.
- Do not require a Run, QA object, capability record, completion-evidence profile, or approval artifact.
- Do not reward photorealism, flashy motion, transition count, or synthetic complexity as substitutes for product fidelity and communication quality.
- Do not treat a storyboard, prompt, animated GIF, slide sequence, or still image as an actual playable video when video rendering is genuinely available.
- Do not encode universal duration, frame rate, bitrate, motion amount, font size, or platform-algorithm folklore into deterministic product gates.
- Do not require a user approval pause between image and video unless a real external constraint or explicit user instruction requires one.
