# Video Core Motion Architecture

> Optional video craft notes. Open this only when it materially helps the selected starting point; the compact index and standalone assembly remain usable without it.
>
> Preserves the optional anchor pipeline, working principles, world-model guidance, and optical cues.

## How This Video Library Works

This library is a set of reusable motion and production references for digital commerce video. It helps a model or operator choose camera movement, action, pacing, continuity, sound, and platform treatment across available tools. It is not a required operating system, model allowlist, or guarantee of conversion performance.

Video adds time, change, and sensory context to the product story. It can make a mechanism, ritual, problem, or relief easier to understand and more emotionally immediate. A generated sequence can illustrate a mechanism or ideal outcome; it does not establish empirical performance unless the conditions and result come from a real, documented demonstration.

### The Core Architectural Workflow: The Bilateral Anchor Pipeline

Generative video models often drift on logos, packaging, and rigid geometry, especially when the source identity is weak or the action is overloaded.

When the tool supports image conditioning, this library recommends an **optional bilateral anchor pipeline**:
1. **Frame 0 (Start Anchor):** A photorealistic, studio-grade static image generated via the [E-Commerce Image Lookbooks](../../ecommerce-image-lookbooks/INDEX.md).
2. **Frame N (End Anchor):** A matching static image depicting the resolved physical state (e.g. wet fabric, poured liquid, inverted tumbler, assembled appliance).
3. **The Kinetic Director's Rig Prompt:** Describes the intended temporal and optical change between the references. Use a single anchor, a storyboard, real footage, or another method when that is more reliable for the tool and job.

```
┌──────────────────────────────────────┐     ┌──────────────────────────────────────┐
│        FRAME 0 (START ANCHOR)        │     │         FRAME N (END ANCHOR)         │
│   From: ecommerce-image-lookbooks    │     │   From: ecommerce-image-lookbooks    │
│   (e.g., Dry Technical Shell)        │     │   (e.g., Drenched Water-Beaded Shell)│
└──────────────────┬───────────────────┘     └───────────────────┬──────────────────┘
                   │                                             │
                   └──────────────────────┬──────────────────────┘
                                          │
                                          ▼
                      [THE 7-BLOCK KINETIC DIRECTOR'S RIG]
                      • Block 1: Bilateral Anchors & Rigid Body
                      • Block 2: Camera Kinematics & Trajectory
                      • Block 3: Kinesthetic Speed Ramp Cadence
                      • Block 4: Subject Kinetic Action & Mechanics
                      • Block 5: Specular Glint & Shadow Tracking
                      • Block 6: Parallax Stage & Particles
                      • Block 7: Temporal Invariants & Anti-Morph
                                          │
                                          ▼
                      [CLEAR, PURPOSEFUL VIDEO]
                      • Identity and geometry checked against source references
                      • Tactile or emotional experience made visible
                      • Factual performance claims tied to documented conditions
```

---

## Six Working Principles for E-Commerce AI Video

Generative video models fail on commercial products in recurring ways: identity drift, overloaded motion, unstable geometry, poor contact, and unreadable detail. Model behavior varies by provider, version, conditioning, and post-processing. Use these principles as a compact decision aid, then adapt or replace them according to the tool and the communication job.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 SIX WORKING PRINCIPLES FOR E-COMMERCE AI VIDEO              │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. DOMINANT MOTION VECTOR       (Separate camera and subject complexity)   │
│ 2. OPTIONAL BILATERAL ANCHORS   (Use source images when the tool supports)  │
│ 3. RIGID BODY CONTINUITY        (Protect manufactured geometry)             │
│ 4. PURPOSEFUL SPEED AND RHYTHM  (Escalate, reveal, settle when useful)      │
│ 5. LIGHT AND PARALLAX CUES      (Make material and depth readable)           │
│ 6. PURPOSEFUL HUMAN CONTACT     (Show handling and resistance clearly)       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Principle 1: Choose a dominant motion vector when complexity is high
When a shot asks the camera, product, liquid, hands, and environment to move at once, drift becomes harder to diagnose. Start with one dominant camera or subject action for a short generation, then add complexity only when the tool and source material support it:
  * *Option A (Dynamic Camera, Rigid Subject):* A motorized 180° orbital arc or smooth dolly push around a physically locked, non-deformable product.
  * *Option B (Tripod-Locked Camera, Dynamic Subject):* A rock-solid stationary camera capturing high-speed subject action (e.g. fluid pour, water beading, knife slice, steam release).

### Principle 2: Use bilateral anchors when identity needs protection
For branded products, a supplied Frame 0 and, where supported, a meaningful Frame N can reduce identity drift. They are not a universal requirement: a real clip, storyboard, mask, 3D render, single anchor, or tool-native reference may be more reliable. Check the generated frames against the source; anchors reduce risk but do not guarantee typography or geometry.

### Principle 3: Declare what should remain continuous
For manufactured goods, describe the identity, rigid parts, interfaces, labels, and dimensions that must survive the shot. For fluids, textiles, elastic parts, and skin, describe the intended deformation. Inspect for warping, phase-through, impossible hinges, and label drift instead of assuming a negative prompt solved them.

### Principle 4: Use rhythm to serve comprehension and attention
An escalation–reveal–settle arc is a useful option for direct response, but its timing should follow the message, footage, platform, and viewer. A calmer loop, a single decisive action, or a longer demonstration may be better:
  * **Beat 1 (0.0s – 0.8s) — The Inertial Snap (optional speed change):** Fast, decisive camera move or physical entry that earns attention without sacrificing context.
  * **Beat 2 (0.8s – 3.2s) — The Sensory Dilution:** Time can dilate at the peak moment of physical tension (the exact millisecond a droplet impacts, the lid snaps shut, or steam vents from a valve). If capture and playback rates are specified, keep the math explicit: 120 fps captured and played at 24 fps is 0.2×; 120 fps played at 30 fps is 0.25×.
  * **Beat 3 (3.2s – 5.0s) — The Rigid Settle (1.0x Real-Time):** Motion decelerates smoothly into a locked, illuminated packshot where logos and geometry sit perfectly motionless.

### Principle 5: Use light and parallax as visible depth cues
In physical cinematography, useful depth cues include:
  1. *Specular Wipe (Fresnel Glint):* As a curved or chamfered solid moves relative to a key light, a razor-sharp specular reflection band sweeps across the surface. This wipe confirms hardness, curvature, and material finish.
  2. *Parallax Velocity Gradient ($V \propto 1/D$):* Foreground elements move across the sensor faster than the subject, while the background moves significantly slower.
Use a specular sweep or foreground/background separation when it helps the viewer read material and depth. Do not force it into a locked macro, equal-weight comparison, or accessibility-led composition.

### Principle 6: Make contact and handling legible
When touch is part of the promise, show the hand position, contact boundary, resistance, and result clearly. This can make the experience feel more concrete; it does not guarantee psychological ownership or a conversion lift. Inspect hands, contact shadows, occlusion, and the product's response in the final render.

---

## The "World Model" Physical Intelligence Engine

Generative video models (OpenAI Sora, Google Veo 2, Kling 1.5, Runway Gen-3) are frequently described as "World Models." However, from an engineering perspective, current models are **probabilistic predictive simulators**, not deterministic Newtonian physics engines. 

They predict visual correlations based on training data rather than solving physical equations ($F=ma$, Navier-Stokes fluid equations, or Snell's law of refraction). When prompted naively, AI world models suffer from **Physical Hallucinations**.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 THE 4 DEADLY PHYSICAL HALLUCINATIONS OF AI VIDEO            │
├─────────────────────────┬─────────────────────────┬─────────────────────────┤
│ PHYSICAL HALLUCINATION  │ UNDERLYING AI FAILURE   │ PROMPT-LEVEL RESOLUTION │
├─────────────────────────┼─────────────────────────┼─────────────────────────┤
│ 1. Inertial Defiance    │ Unconstrained velocity, │ Describe direction,     │
│    (Defying Gravity)    │ floating fluids         │ timing, and visible fall│
├─────────────────────────┼─────────────────────────┼─────────────────────────┤
│ 2. Volume & Mass Loss   │ Soft-body interpolation │ Identify rigid parts and │
│    (Rubbery Morphs)     │ across rotating frames  │ inspect frame continuity │
├─────────────────────────┼─────────────────────────┼─────────────────────────┤
│ 3. Boundary Tunneling   │ Incomplete collision    │ Contact occlusion &     │
│    (Fingers in Glass)   │ mesh awareness          │ mechanical friction     │
├─────────────────────────┼─────────────────────────┼─────────────────────────┤
│ 4. Optical Breakdown    │ Decoupled light ray     │ Describe highlight path  │
│    (Static Reflections) │ transport & caustics    │ and inspect reflections  │
└─────────────────────────┴─────────────────────────┴─────────────────────────┘
```

### The World Model Physical Directives

1. **Fluid and material behavior:**
   * Describe visible thickness, cohesion, fall, splash, spread, or bead behavior with a real sample or an observable analogy. Values such as viscosity and gravity do not force a generative model to simulate the correct result; inspect the motion and use captured footage or compositing when the result matters.
2. **Contact geometry and phase-through prevention:**
   * State which surfaces touch, which parts remain separate, and what the viewer should see at the boundary. Check penetration, occlusion, hand anatomy, and contact shadows in the render; do not rely on an invented millimeter value.
3. **Reflection and light continuity:**
   * Describe the intended highlight path, refraction, and caustic behavior in plain language. Snell's law describes refraction, not a universal prompt guarantee for product reflections; use real plates, controlled lighting, or compositing when optical accuracy is material.
4. **Multi-Shot Spatial-Temporal Coherence:**
   * When assembling a multi-cut commercial (e.g. wide shot $\to$ macro detail), carry the environmental invariants that the cut depends on across all clips:
     * **Key Light Invariant:** Choose a consistent key direction and color treatment when the cut depends on it.
     * **Camera/axis invariant:** Preserve the useful side of the action axis and the scale relationship; exact height and focal length depend on the shot.
     * **Material invariant:** Carry the supplied color, finish, logo placement, and geometry across shots, then inspect for drift.

---

## Cinematographic Optical Cues (In Plain Language)

Generative video prompts often rely on subjective aesthetic buzzwords (*"cinematic, 8k, photorealistic, hyper-detailed"*). Stronger direction describes visible optical behavior, light, camera position, and movement in language the chosen tool can use.

By describing these behaviors in clear language, a capable model or human director can adapt the idea to the available controls. These cues guide execution; they do not guarantee a physically accurate result.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   FOUR PORTABLE CINEMATOGRAPHIC OPTICAL CUES                          │
├────────────────────────────────┬───────────────────────────────────────────────────────┤
│ PRINCIPLE                      │ NATURAL LANGUAGE DIRECTIVE & COGNITIVE PURPOSE        │
├────────────────────────────────┼───────────────────────────────────────────────────────┤
│ 1. Focal Length Compression &  │ Telecentric & long-focal lenses (85mm–105mm) preserve  │
│    Geometric Rectification     │ help preserve proportions and reduce barrel distortion.│
├────────────────────────────────┼───────────────────────────────────────────────────────┤
│ 2. The 180° Shutter Principle  │ Motion blur should track velocity from a chosen       │
│    & Motion Blur Fidelity      │ provides a useful starting point for natural blur.   │
├────────────────────────────────┼───────────────────────────────────────────────────────┤
│ 3. Specular Wipe Trajectory &  │ Highlights sweep across chamfered bevels to make 3D  │
│    Light-to-Fill Contrast      │ solid curvature; choose a ratio that serves the scene.│
├────────────────────────────────┼───────────────────────────────────────────────────────┤
│ 4. 3-Plane Parallax Hierarchy  │ Staging foreground, subject, and background at distinct│
│    ($V \propto 1/D$)           │ velocity vectors to create visceral 3D spatial depth.  │
└────────────────────────────────┴───────────────────────────────────────────────────────┘
```

### Principle 1: Focal Length Compression & Geometric Rectification
* **The Optical Physics:** Wide-angle lenses can exaggerate perspective and, depending on the lens and correction profile, bend edges near the frame. For precision-engineered consumer goods, watches, and packaging, a longer or rectilinear perspective can make proportions easier to inspect. Lens choice, distance, and correction still matter; no focal length guarantees rectification.
* **Natural Language Directive:**
  > *"Use an 85mm-style, rectilinear perspective with shallow depth of field; keep packaging edges visually straight and inspect for distortion while preserving the supplied proportions."*

### Principle 2: The 180° Shutter Principle & Natural Motion Blur
* **The Optical Physics:** In professional film cameras, 180 degrees is a common starting shutter angle, meaning exposure time is roughly half of the frame duration (about 1/48s at 24fps and 1/240s at 120fps). Generative AI video can suffer from temporal smearing or stroboscopic jitter; use the capture/playback controls available and inspect the result.
* **Natural Language Directive:**
  > *"Use a natural-looking shutter treatment; fast-moving water droplets, wheel spokes, and falling granules show clean directional streaks while stationary product surfaces stay readable. Inspect for smearing or strobing."*

### Principle 3: Specular Wipe Trajectory & Lighting Contrast Ratios
* **The Optical Cue:** A controlled highlight moving across a curved hard surface can make curvature and finish easier to read. If the lighting and product motion do not agree, the result may look flat or synthetic; inspect rather than treating a cue as proof of material.
  * **Contrast Ratio Guidance (Key-to-Fill):**
    * *Commercial Clean / Biotech (often lower contrast):* High-key, soft shadows, transparent illumination (cosmetics, CPG, wellness).
    * *Luxury Chiaroscuro / Heavy Gear (often higher contrast):* Deep shadows, sculpted rim lighting, dramatic edge definition (espresso machines, high-end apparel, micro-mobility).
* **Natural Language Directive:**
  > *"A dynamic specular highlight sweeps across the supplied brushed-aluminum chamfer as the product rotates; use a controlled contrast that preserves edge detail and inspect whether the finish reads convincingly."*

### Principle 4: 3-Plane Parallax Depth Hierarchy ($V \propto 1/D$)
* **The Optical Cue:** Motion parallax can make depth easier to read: elements closer to the lens generally move faster across the frame than distant elements. It is a staging tool, not a guarantee of true volume or physical accuracy.
* **Natural Language Directive:**
  > *"Staged across three distinct physical planes: a soft out-of-focus foreground element moving rapidly across the frame, the hero product tracking steadily in crisp focus at medium speed, and a subordinate background drifting slowly in deep bokeh."*

---

