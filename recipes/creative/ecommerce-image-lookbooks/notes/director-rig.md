# Image Director's Rig & Worked Examples

> Optional craft notes. Open this only when it materially helps the selected image recipe; the scale menu and individual archetype are usable without it.
>
> This is the optional five-block prompt scaffold and the original worked examples. Use the scaffold when it reduces ambiguity; it is not required syntax.

## Optional 5-Block Director's Rig Prompt Scaffold

The five blocks are a compact way to specify a visual when they help the task. They are modular fields, not a required grammar: a native image tool, a human photographer, a compositing workflow, or another prompt structure may be clearer. Keep the blocks that improve the outcome and omit the rest.

```text
BLOCK 1: [HERO SUBJECT & BOUNDING BOX]
BLOCK 2: [OPTICAL & CAMERA RIG]
BLOCK 3: [LIGHTING RIG & SPECULAR CONTROL]
BLOCK 4: [SUBORDINATE STAGE & DEPTH SEPARATION]
BLOCK 5: [NEGATIVE CONSTRAINTS & EXCLUSIONS]
```

### The 5 Blocks Defined:

* **BLOCK 1: [HERO SUBJECT & BOUNDING BOX]**
  * *Purpose:* States what the viewer should understand first.
  * *Content:* Product type, source/reference identity, known dimensions, materials, finish, label orientation, and a compositionally appropriate prominence. Use a reference image or post-render label when exact geometry or typography matters.
* **BLOCK 2: [OPTICAL & CAMERA RIG]**
  * *Purpose:* Enforces physical optical geometry instead of AI defaults.
  * *Content:* Exact lens focal length (50mm, 85mm prime, 100mm macro), camera elevation (eye-level, low-angle 15°, axle-height), f-stop (`f/2.8` for shallow subject separation, or `f/8` for edge-to-edge sharpness), and shutter speed for kinetic motion.
* **BLOCK 3: [LIGHTING RIG & SPECULAR CONTROL]**
  * *Purpose:* Makes material and contact readable.
  * *Content:* Key/fill relationship, light source, color temperature, reflections, and a believable contact shadow when the product touches a surface. Choose contrast for label legibility and the intended dialect; no shadow or ratio is mandatory in every scene.
* **BLOCK 4: [SUBORDINATE STAGE & DEPTH SEPARATION]**
  * *Purpose:* Puts the product in a meaningful setting without losing the hierarchy.
  * *Content:* Surface texture, scene context, and the treatment of secondary props. Use blur, tonal separation, crop, or deliberate equal-weight comparison according to the communication job.
* **BLOCK 5: [NEGATIVE CONSTRAINTS & EXCLUSIONS]**
  * *Purpose:* Names the failure modes that would damage this particular asset.
  * *Content:* Exclude only relevant errors such as warped labels, wrong components, extra limbs, impossible reflections, false dimensions, or distracting clutter. “Negative” text is a request for inspection, not a guarantee of absence.

---

### Production Assembly Examples

#### Example 1: Scale 01 (Micro) — The Proof Class (Skincare Absorption)
```text
[BLOCK 1: HERO]: A crisp e-commerce skincare illustration or documented demonstration on a clean, seamless neutral white studio surface. The subject is a woman's natural forearm positioned horizontally across the lower half of the frame, occupying 70% of visual weight, with natural unretouched skin pores visible.
[BLOCK 2: COMPARISON GRAMMAR]: A clean two-stage side-by-side demonstration directly on her skin. ON THE LEFT: A single, concentrated micro-droplet of [FORMULA COLOR / TEXTURE FROM SOURCE] resting on the surface of the skin. ON THE RIGHT: The identical formula rubbed smoothly into the skin, showing the supplied or observed finish. If the absorption result is not documented, treat the scene as a concept and avoid a performance caption.
[BLOCK 3: OPTICS]: 100mm True Macro prime lens, f/8 tack-sharp focus on natural skin pores and micro-texture.
[BLOCK 4: STAGE & LIGHT]: In the soft-focus background (f/2.8 blur, 2 stops darker), the 30ml amber glass dropper bottle rests out of focus. Clean 5200K high-CRI clinical daylight with subtle soft fill.
[BLOCK 5: EXCLUSIONS]: Negative: multiple skin patches, makeup foundation swatches, floating blue blobs, brown oil drops, messy droppers, cluttered bathroom props, airbrushed plastic skin, four arms.
```

#### Example 2: Scale 03 (Apparel) — The Proof Class (Two-Model Fit Comparison)
```text
[BLOCK 1: HERO]: A commercial e-commerce sizing and fit comparison photograph of two athletic men standing naturally side-by-side on a clean, seamless light-gray studio cyclorama with zero background clutter. The jackets occupy 80% of the visual frame.
[BLOCK 2: COMPARISON GRAMMAR]: ON THE LEFT: An athletic runner (5'11", 170 lbs) wearing the matte charcoal technical mountain shell in Size Medium over a lightweight base layer, showing a clean, tailored athletic fit with sleeves ending cleanly at the wrist. ON THE RIGHT: A taller, broader man (6'2", 210 lbs) wearing the identical jacket in Size Large layered over an insulated hoodie, showing comfortable layering volume across the chest and shoulders without bunching.
[BLOCK 3: OPTICS]: 75mm prime portrait lens, f/8 tack-sharp focus across both jackets from collar to hem, eye-level perspective.
[BLOCK 4: STAGE & LIGHT]: Clean 5500K commercial catalog studio lighting with soft contact floor shadows, seamless neutral studio cyclorama with zero props.
[BLOCK 5: EXCLUSIONS]: Negative: wax figures, stiff mannequins, wooden barn, uncanny valley, CGI render, cartoon, 3D model, four men, identical faces, distorted hands, stiff poses, cluttered background.
```

#### Example 3: Scale 04 (Appliances) — The Proof Class (Engineering Cutaway)
```text
[BLOCK 1: HERO]: A side-by-side e-commerce engineering comparison photograph of two espresso machines on a clean, seamless neutral light-gray studio cyclorama with zero background clutter, occupying 85% of total frame width.
[BLOCK 2: COMPARISON GRAMMAR]: ON THE LEFT (45% of width): A generic budget-style reference machine cutaway, intentionally showing the weak construction the buyer wants to avoid. ON THE RIGHT (55% of width — THE HERO): [HERO PRODUCT] with the side panel removed, showing only the supplied, documented internals. Label the left side “GENERIC LOWER-COST REFERENCE” and the right side with the hero product's verified material claims; do not invent a competitor, component, or test result. The contrast may be deliberately stark to make the pain and relief immediately legible.
[BLOCK 3: OPTICS]: 60mm prime lens, eye-level perspective, tack-sharp f/8 depth of field across both machines.
[BLOCK 4: STAGE & LIGHT]: High-contrast commercial catalog lighting (5500K) with crisp contact floor shadows and zero reflections on back wall.
[BLOCK 5: EXCLUSIONS]: Negative: kitchen background, countertops, blenders, messy wires, dark shadows, tilted horizon, artistic blur, café background.
```

#### Example 4: Scale 06 (Mobility) — The Habitat / Ritual Class (Axle-Height Velocity)
```text
[BLOCK 1: HERO]: Close-tracking commercial hero shot of a matte olive-sage commuter e-bike with Gates carbon belt drive. The e-bike frame and drive components occupy 75% of the frame, shot from a 45-degree front-three-quarter profile at axle height.
[BLOCK 2: OPTICS]: 50mm lens at axle height, 1/40s tracking shutter speed creating smooth horizontal motion blur in background while bike frame remains tack-sharp.
[BLOCK 3: LIGHT & TEXTURE]: Low-angle crisp twilight lighting, matte olive frame, hydroformed downtube, and hydraulic disc brakes are tack-sharp in foreground.
[BLOCK 4: SUBORDINATE STAGE]: Soft-focus urban bridge at twilight with smooth 1/40s horizontal motion-blurred lights, keeping full visual focus on the sharp e-bike.
[BLOCK 5: EXCLUSIONS]: Negative: distant landscape, tiny bike, wide shot, daytime, parked cars, suburban houses, distracting scenery.
```

---
