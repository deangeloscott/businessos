# CAPABILITY-VIDEO-001 — Level 4 Chained Image → Video Execution

## Purpose
Test whether AURA can fulfill one ordinary user request that intentionally creates a new governed product image and then uses that exact new image as the grounded visual source for a real short-form video, while preserving provenance, appearance integrity, QA, and persistent organizational state across the dependent media steps.

This is a maintainer-side qualification case. The candidate must not see this file, the hidden target contract, evaluator criteria, checkpoints, receipts, prior runs, or scoring metadata.

## Layer
Level 4 — capability/media execution with dependent media composition.

## Hidden target
`content.production.short-video`

## Fixture
`northline-commerce` with supplied first-party product reference media.

## Candidate-visible request
For Northline Coffee, use the supplied Discovery Box product reference image to create a new polished lifestyle product image for social use, then use that **new image you created** as the visual source for a polished 10–15 second vertical short-form video. In the still image, keep the actual product materially faithful to the supplied reference—the cream box silhouette, NORTHLINE wordmark, DISCOVERY BOX label, three-pouch count, and rust/olive/charcoal pouch appearance should remain recognizable—while placing it in a warm, natural morning coffee setting with tasteful premium-but-unpretentious art direction. Then turn that derived image into the video with subtle purposeful motion, restrained on-screen text, and audio or ambience when useful. The video should communicate the grounded Discovery Box idea that a customer can try three rotating coffees before committing to full bags, without inventing sourcing claims, tasting claims, health claims, discounts, customer outcomes, or other product facts. Use the strongest image/video capabilities genuinely available in the environment; if a dedicated image-to-video capability is unavailable, use the strongest truthful rendering/animation path that still produces an actual playable video when possible. Preserve the supplied source image, the new derived image, and the final video as reconstructable stages of the work so it is clear which image the video came from. Inspect the derived image before using it downstream, and inspect the actual final video for product-appearance drift, visual artifacts, text/crop/safe-area problems, timing, audio, and source-to-video continuity before completion. Do not publish, send, or contact anyone.

## What Level 4 is testing
This is deliberately a **single-request dependent chain**, not two separate user turns.

The requested outcome is:

1. supplied first-party product image;
2. newly created governed product-image Asset;
3. final governed video Asset derived specifically from step 2.

AURA should make the chain feel like one coherent job to the user while keeping the intermediate Asset meaningful to the organization. The intermediate image must not disappear as untracked scratch merely because it is used immediately by the video step.

The case tests both capability execution and organizational continuity:

- discover and use the strongest genuine image generation/editing path available;
- preserve material product appearance and avoid misleading synthetic evidence;
- register the derived still as a governed Asset with useful source/prompt/design provenance;
- use that exact derived still as the intended visual source/reference for the downstream video rather than regenerating a materially different product from memory;
- discover and use the strongest genuine image-to-video/video-render path available;
- preserve source → derived image → final video lineage;
- perform substantive QA on both the intermediate image and the final rendered video;
- complete the user's original end-to-end request without requiring a second prompt merely to continue the already-requested chain.

## Preferred execution order
1. Resolve Northline business, offer, brand, and the supplied product reference image from the ordinary workspace.
2. Establish the governed business work/Run through normal AURA entry rather than treating the workspace as a loose media folder.
3. Inspect the supplied reference and identify material appearance constraints that should not drift.
4. Create the new lifestyle product image with the strongest authorized available image capability.
5. Inspect the actual resulting image for package count, text/logo integrity, product-shape/color continuity, obvious generation artifacts, crop, and brand fit; correct material problems before downstream use.
6. Persist/register the derived image as a governed Asset with reconstructable relation to the supplied source and useful generation/edit provenance.
7. Use the derived image—not an independently reimagined product—as the grounded visual source for the requested video.
8. Create the actual playable 10–15 second vertical video when the environment genuinely supports video/image-to-video/render execution. If direct image-to-video is unavailable, a truthful local animation/render path may satisfy the request if it genuinely produces the video and preserves the derived image as its visual basis.
9. Inspect the final video itself for source-image continuity, product drift, broken text/glyphs, crop/safe-area issues, motion artifacts, duration, audio quality where present, and any unsupported audience-facing claims.
10. Persist the final governed video Asset and enough lineage/evidence/QA/completion state for the organization to reconstruct source image → derived image → video.
11. Complete the entire original request in one user-visible outcome unless a real authorization/capability blocker requires intervention.

## Evaluation emphasis
The professional judge should inspect the source product reference, the newly created still, and the final video together.

- **Chain completion:** Did one request actually result in both the new image and final video, rather than stopping after the first step or requiring the maintainer to prompt continuation?
- **Intermediate Asset integrity:** Is the newly created image a real governed organizational Asset rather than disposable scratch?
- **Lineage:** Can a reviewer reconstruct source reference → derived image → video from persisted state/artifacts without relying on the candidate's prose claim?
- **Downstream source fidelity:** Does the video actually use the newly created image as its grounded visual source/reference?
- **Product appearance integrity:** Are the cream box, NORTHLINE wordmark, DISCOVERY BOX label, three-pouch count, and rust/olive/charcoal pouch appearance materially preserved unless a clearly authorized creative change explains a difference?
- **Image quality:** Is the derived lifestyle image polished, plausible, brand-appropriate, compositionally strong, and free of material generation defects?
- **Video quality:** Is the final video genuinely playable, purposeful, visually coherent, and appropriate to the requested short duration rather than merely a file-format trick?
- **Motion continuity:** Does motion enhance the approved still without causing product morphing, duplicate/missing packages, logo/text corruption, or unexplained scene identity changes?
- **Message/claim discipline:** Does the content stay within grounded Northline product truth and avoid invented sourcing, tasting, health, discount, outcome, or performance claims?
- **Audio/text execution:** Where audio/on-screen text is used, is it legible/intelligible, restrained, timed appropriately, and consistent with the visible product/story?
- **Capability truthfulness:** Did AURA use genuinely available image/video/render capabilities or a truthful fallback, without claiming nonexistent image-to-video execution?
- **QA:** Were both the actual derived still and actual final video inspected, with material problems corrected before completion?
- **State integrity:** Do canonical Assets, evidence/claims where applicable, Run records, QA, and completion evidence accurately describe the media that exists?

## Pass interpretation
A strong pass demonstrates more than isolated image generation or isolated video rendering. It shows AURA can coordinate a dependent media workflow from one natural-language request while preserving the intermediate creative as organizational state and carrying that exact Asset forward into the next production stage.

This is evidence for same-request media composition, not proof of cross-session or cross-harness continuity. A later reliability test may deliberately create the image in one session/harness and ask another session/harness to continue from the persisted Asset.

This does not prove real-world views, watch time, shares, orders, repeat purchase, or revenue. Those require authorized publication and subsequent measurement.

## Non-goals
- Do not require a specific image model, video model, editor, codec implementation, voice provider, or proprietary AURA renderer.
- Do not require direct generative image-to-video if another available truthful method can create the requested playable video from the derived image.
- Do not reward photorealism, flashy motion, transition count, or synthetic complexity as substitutes for product fidelity and communication quality.
- Do not treat a storyboard, prompt, animated GIF, slide sequence, or still image as an actual playable video when video rendering is genuinely available.
- Do not encode universal duration, frame rate, bitrate, motion amount, font size, or platform-algorithm folklore into deterministic product gates.
- Do not require a user approval pause between image and video unless actual organization/user authorization policy requires one.
