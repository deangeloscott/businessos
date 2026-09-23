# Video Motion Principles

> Optional craft notes. Use these when a selected video idea needs help with motion, continuity, or physical readability. They are portable decisions, not a required prompt grammar or a runtime guard.

## Start with the action

Choose the one thing the viewer should feel or understand: inspect the product, see a mechanism, experience a texture, watch a problem resolve, or imagine the product in its habitat. A short single action is often easier to read and keep stable than a crowded sequence. A multi-shot story, a real clip, a storyboard, a 3D scene, or a tool-native control may be the better method.

When a shot becomes complex, give it one dominant motion vector. Either keep the camera mostly stable while the subject acts, or move the camera around a mostly stable subject. Add other motion only when it supports the message and the tool can hold identity, contact, and timing.

## Protect what must stay the same

For a manufactured product, identify the supplied identity, label, rigid parts, interfaces, and proportions that should survive the shot. For fluids, fabric, skin, and other deformable material, describe the intended change rather than demanding rigid continuity. A reference frame, start/end pair, mask, real footage, or 3D asset can help, but no conditioning method guarantees fidelity.

Inspect the result for label drift, melting geometry, impossible hinges, extra limbs, phase-through, floating objects, broken contact, unstable shadows, and a discontinuous background. Keep this inspection separate from any factual performance record.

## Give time a job

Pacing should make the idea easier to understand or more compelling. A useful optional arc is:

1. **Set up:** establish the product and the situation.
2. **Act:** perform the one action that carries the point.
3. **Reveal or resolve:** hold the important result long enough to read it.

This can be a fast hook, a calm loop, a slow sensory reveal, or a longer documented demonstration. A 120 fps capture played at 24 fps is 0.2×; use that math only when the source and tool actually support it. Generated video may need a simple speed direction instead. Change the timing when the platform, source, or viewer needs a different rhythm.

## Use visible physical cues

- **Contact:** show where hand, product, surface, liquid, or fabric meet. Give the contact a clear boundary and believable occlusion.
- **Material:** use a glint, reflection, shadow, ripple, bead, fold, or resistance that makes the surface easier to read. These are visual cues, not proof of a material or performance claim.
- **Depth:** use foreground, subject, and background movement at different speeds when parallax helps the viewer read space. A nearby object generally crosses frame faster than a distant one; do not force parallax into a locked comparison or accessibility-led composition.
- **Light:** let the highlight or shadow follow the motion and preserve the label or detail the viewer needs. A moving specular highlight can reveal curvature; it does not establish composition or engineering.
- **Human handling:** show grip, pressure, direction, and response when touch is part of the idea. Keep hands and anatomy believable and inspect them in the final sequence.

## Camera choices in plain language

Camera position and distance shape perspective; focal length mainly helps choose the framing from that position. A longer, more distant view can keep proportions calm, while a close wide view can exaggerate depth and energy. Use a macro or telephoto look when it helps a small detail read, and a wider view when the relationship to the environment matters. Exact focal lengths, shutter angles, frame rates, and apertures are optional production choices, not universal model instructions.

## Optional anchor approach

When the tool supports image conditioning, a start frame and meaningful end frame can make a transformation easier to describe. Use one anchor, real footage, a storyboard, or another method when that is more reliable. The key prompt is the change between the references: what moves, what stays rigid, where contact happens, how the light changes, and where the viewer should end up.

## Quick adaptation prompt

If a recipe needs more direction, give the model this in ordinary language:

```text
Make [PRODUCT] show [VIEWER JOB] through one clear action: [ACTION]. Keep [IDENTITY / PARTS / CONTACT] continuous and make [MATERIAL CUE OR RESULT] easy to read. Choose the camera, pace, light, and duration for [PLACEMENT]. Use supplied conditions for any factual claim; otherwise treat the result as an illustration. Inspect the finished sequence for identity, geometry, anatomy, contact, timing, and continuity.
```

The model or user can use a better prompt, a different motion plan, or no prompt at all. These notes exist to make a good starting point easier to find.
