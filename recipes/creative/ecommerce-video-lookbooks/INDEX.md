# E-Commerce Video Lookbooks
### Master Directory, Kinesthetic Motion Architecture & Adaptable Director's Craft References
*Version 1.3 — Evidence-aware kinetic video system*

---

## 1. How This Video System Works

This library is a set of reusable motion and production references for digital commerce video. It helps a model or operator choose camera movement, action, pacing, continuity, sound, and platform treatment across available tools. It is not a required operating system, model allowlist, or guarantee of conversion performance.

Video adds time, change, and sensory context to the product story. It can make a mechanism, ritual, problem, or relief easier to understand and more emotionally immediate. A generated sequence can illustrate a mechanism or ideal outcome; it does not establish empirical performance unless the conditions and result come from a real, documented demonstration.

### The Core Architectural Workflow: The Bilateral Anchor Pipeline

Generative video models often drift on logos, packaging, and rigid geometry, especially when the source identity is weak or the action is overloaded.

When the tool supports image conditioning, this library recommends an **optional bilateral anchor pipeline**:
1. **Frame 0 (Start Anchor):** A photorealistic, studio-grade static image generated via the [E-Commerce Image Lookbooks](../ecommerce-image-lookbooks/INDEX.md).
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

## 2. Six Working Principles for E-Commerce AI Video

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

## 3. The "World Model" Physical Intelligence Engine

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

## 4. Cinematographic Optical Cues (In Plain Language)

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

## 5. Full-Funnel Placement & User Intent Matrix

In commercial e-commerce, video creative cannot be treated as a one-size-fits-all asset. A high-converting top-of-funnel ad will cause immediate bounces if embedded on a Product Detail Page (PDP), and a calm PDP loop will fail to stop the thumb on a social feed.

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                FULL-FUNNEL PLACEMENT & USER INTENT MATRIX                              │
├────────────────────┬──────────────┬──────────────────┬────────────────────┬────────────────────────────┤
│ PLACEMENT          │ USER INTENT  │ ATTENTION STATE  │ PRIMARY OBJECTIVE  │ OPTIMAL KINETIC ARCHETYPE  │
├────────────────────┼──────────────┼──────────────────┼────────────────────┼────────────────────────────┤
│ 1. Cold Social Ad  │ Zero / Cold  │ Passive scrolling│ Stop the scroll /  │ The Shock Torture Hook,    │
│    (Meta / TikTok) │ (Unaware)    │ feed trance      │ create curiosity   │ The Viscous Pour Climax    │
├────────────────────┼──────────────┼──────────────────┼────────────────────┼────────────────────────────┤
│ 2. Retargeting Ad  │ Mid / Warm   │ Skeptical,       │ Resolve objections │ The Polarizing Split       │
│    (BOFU / Cart)   │ (Problem)    │ price-sensitive  │ with evidence or a │ Contrast / Documented Demo  │
│                    │              │                  │ useful illustration│                            │
├────────────────────┼──────────────┼──────────────────┼────────────────────┼────────────────────────────┤
│ 3. PDP Carousel #1 │ High / Hot   │ Focused,         │ Confirm 360° form, │ The Zero-Cut Turntable,    │
│    (Primary Hero)  │ (Evaluating) │ rational         │ scale & finish     │ The Floating Exploded Build│
├────────────────────┼──────────────┼──────────────────┼────────────────────┼────────────────────────────┤
│ 4. PDP Rich Media  │ High / Hot   │ Detail-seeking,  │ Demonstrate utility│ The Mechanical ASMR Click, │
│    (Mid-Page Spec) │ (Validating) │ technical        │ & daily workflow   │ The Ergonomic Hand Grip    │
├────────────────────┼──────────────┼──────────────────┼────────────────────┼────────────────────────────┤
│ 5. Post-Purchase   │ Confirmed    │ Relieved,        │ Eliminate remorse, │ The Unboxing Pull,         │
│    (Email / Box QR)│ (Buyer)      │ eager to set up  │ guide rapid setup  │ The 3-Step Assembly Guide  │
└────────────────────┴──────────────┴──────────────────┴────────────────────┴────────────────────────────┘
```

### Placement Deep-Dive

* **Placement 1: Cold Acquisition Ad (Paid Social Prospecting)**
  * *Constraint:* Earn immediate context or tension in the opening moments; set a benchmark from the account's own baseline and platform reporting.
  * *Execution:* Use high kinetic contrast, sudden physical movement, or unexpected tension when it serves the audience (e.g. tumbler inverted over a laptop, knife slicing an expensive shoe). Branding may appear after tension is established when that sequencing helps the message.
* **Placement 2: Retargeting & Consideration Ad (Bottom-of-Funnel)**
  * *Constraint:* The buyer already knows what the product is; they are hesitating on price, quality, fit, or the cost of staying with the current problem.
  * *Execution:* Use a documented stress test, a generic ideal-versus-poor contrast, or a mechanism explanation. Close with a supported offer, warranty, or next step; do not let a generated scene stand in for a test.
* **Placement 3: PDP Primary Carousel Video (Slot 1 or 2)**
  * *Constraint:* The buyer is on the page. Aggressive music, fast cuts, and hype copy cause annoyance and cognitive overload.
  * *Execution:* A calm loop, clean rotation, or short mechanism sequence can work when it answers the PDP question. Design and inspect the loop seam; do not require a 360° turn or a specific background.
* **Placement 4: PDP Mid-Page Feature Modules**
  * *Constraint:* Inline video embedded in Shopify / headless product descriptions should protect page speed and Core Web Vitals (LCP/INP); test the real page on representative devices.
  * *Execution:* Short micro-loops showing a specific mechanism or sensory interaction (e.g. documented water behavior, magnetic lid snap, dial click), with conditions and captions matched to the evidence.
* **Placement 5: Post-Purchase / Unboxing & Onboarding**
  * *Constraint:* Sent via post-purchase email or accessed via QR code on the packaging insert.
  * *Execution:* Clear, reassuring, unhurried demonstration of unboxing, first-time setup, and maintenance. It can reduce avoidable support questions and returns; measure those outcomes rather than assuming them.

---

## 6. Platform Ecosystem Specifications & Nuances

Every major commerce platform has distinct algorithmic incentives, technical encoding standards, user interface overlays, and sound cultures:

| Placement | Useful starting point | Audio route | UI / technical check | Measure in context |
|---|---|---|---|---|
| TikTok Shop / Ads | 9:16; often short vertical cuts | Sound-on can carry texture or narration; keep the proposition legible on mute when needed | Verify the current icon, caption, and commerce-card overlays in the destination | Early comprehension, hold, and action against the account baseline |
| Meta Reels / Instagram Ads | 9:16 with alternate crops prepared when useful | Sound-on and sound-off routes can coexist; captions are optional when they clarify | Validate each Reel/Feed/Story crop and current UI buffers | Scroll-stop, hold, and action against a matched baseline |
| YouTube Shorts / In-Stream | 9:16 for Shorts; adapt to the placement | Sound can deepen the demonstration; make the key route resilient to mute/skip behavior | Check player controls, crop, and skip context | Viewed/swiped, watch time, and action in the actual placement |
| Amazon PDP / Brand Video | Use the current accepted ratio and duration for the placement | Often muted or autoplay; make product detail clear without relying on sound | Check current marketplace policy, moderation, overlays, and product prominence | Product-page engagement and downstream action |
| Shopify / D2C PDP | Use the ratio and loop length that fit the gallery and page | Sound optional; autoplay/accessibility policy applies | Test encoded payload, poster/fallback, LCP/INP, and seamless loop behavior on representative devices | Page performance and product interaction |

### Platform-Specific Strategic Directives

#### 1. TikTok & TikTok Shop
* **Aesthetic Choice:** Native-feeling UGC, engineered lo-fi, or polished craft can all work. Match the audience's expectation and make the first beat understandable; do not import a universal swipe-time claim.
* **Audio Choice:** Design the action to work with sound on when the placement supports it, while keeping the central proposition legible on mute. Sync tactile Foley or spoken narration to the action when it helps. Treat UI coordinates as a current-placement check, not a universal box.
* **UI Safe-Zone:** Keep primary text and product focus clear of the placement's current controls; verify the rendered crop in the target app.

#### 2. Meta Reels & Instagram Ads
* **Aesthetic Standard:** Elevated, aspirational, editorial. High production value and beautiful lighting perform exceptionally well.
* **Audio Choice:** Make the essential proposition understandable on sound-off when the placement needs it; add captions or concise callouts only when they clarify the visible action. Do not force text into every frame.
* **Multi-Format Adaptation:** Prepare alternate crops when the distribution plan needs them; preserve the subject, comparison, labels, and CTA in each actual placement rather than assuming one crop will hold.

#### 3. Amazon Product Detail Page (PDP) & Sponsored Video
* **Aesthetic Standard:** Follow the current placement and marketplace policy. Check the account's current moderation rules before publishing; common risks include:
  * Unsubstantiated superlative claims (*"World's #1"*, *"Best Ever"*).
  * Time-sensitive promotional language (*"Limited Time Offer"*, *"Sale"*).
  * External URLs, customer reviews with star ratings, or off-Amazon mentions.
* **Visual Rule:** Keep the physical product prominent and legible, using the current placement's requirements and the product's actual scale. White or light grey studio grounds can help when they fit the brand; they are not a universal requirement.

#### 4. Shopify & Headless D2C PDPs
* **Performance Budget:** Encode efficiently and validate the actual page impact:
  * **Dual Codec Delivery:** Deliver both modern `.webm` (for Chrome/Android) and `.mp4` (H.264/H.265 for Safari/iOS).
  * **File Size Target:** Set a payload budget from the page's performance target and test LCP/INP on representative devices; 5 MB and 2 MB can be starting budgets, not guarantees.
  * **Loop Rule:** Render and inspect a seamless start/end transition, preserving a fallback poster and respecting autoplay/accessibility behavior.

---

## 7. Four Video Commerce Archetype Jobs

Most commercial video assets serve one or more of these jobs. Choose the job from the viewer's question and available evidence; combine, rename, or omit a class when the work calls for it:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FOUR VIDEO COMMERCE JOBS                                │
├──────────────────────┬──────────────────────┬───────────────────────────────┤
│ CLASS                │ COMMERCIAL ROLE      │ CORE COGNITIVE OBJECTIVE      │
├──────────────────────┼──────────────────────┼───────────────────────────────┤
│ 1. KINETIC SPECIMEN  │ Spatial Truth & Form │ 360° Form, Scale, Assembly    │
│ 2. DOCUMENTED DEMO   │ Objection Resolver  │ Stress Test, Incline, Deluge  │
│ 3. SENSORY RITUAL    │ Visceral Craving     │ Slow-Mo Viscosity, ASMR Melt  │
│ 4. KINETIC HABITAT   │ Lifestyle in Motion  │ Commuter Glide, Daily Ritual  │
└──────────────────────┴──────────────────────┴───────────────────────────────┘
```

### Class 1: The Kinetic Specimen (Spatial Truth & Geometry)
* **Definition:** A controlled motion study that makes supplied product form, scale, finish, or assembly easier to inspect. Keep it neutral when that serves the viewer; lifestyle context is optional.
* **Primary Funnel Role:** Shopify PDP primary video slot, Amazon product carousel slot 1, technical spec verification, B2B wholesale portals.
* **Core Mechanisms:**
  * *The 360° Precision Turntable:* Motorized turntable rotates the product 180°–360° at steady velocity while a fixed key light sweeps specular glints across edges.
  * *The Floating Exploded Assembly:* Internal CAD-like components separate smoothly along the Z-axis, pausing to reveal engineering integrity (brass boilers, multi-layer foam, copper heat pipes) before snapping back into place.
  * *The Orthographic Dimensional Orbit:* Camera sweeps around the product while subtle visual laser-lines or graphic callouts indicate true physical scale.

### Class 2: The Documented Kinetic Demonstration (Validation & Objection Clearance)
* **Definition:** A continuous-motion demonstration of a performance claim when the product, conditions, and result are documented. A generated sequence can be a clearly framed illustration of the intended contrast; it is not a test record by itself.
* **Primary Funnel Role:** Paid social performance ads (Meta/TikTok), PDP objection sections, landing page guarantee blocks, and return-rate reduction when the conditions and result are real; otherwise use an explicit illustrative contrast.
* **Core Mechanisms:**
  * *The Hydrostatic Deluge Demonstration:* Show a documented water exposure with the fabric, pressure, duration, angle, and result labeled when those details matter; otherwise frame a generic poor-versus-ideal contrast as an illustration.
  * *The High-Stakes 180° Inversion Demonstration:* A full container or tumbler is rotated over a valuable device only with a controlled, documented setup. A synthetic scene may dramatize the pain and relief, but cannot claim a zero-leak result without the record.
  * *The Hill-Climb Torque Demonstration:* Show the supplied grade, rider/load, speed, mode, and battery/test conditions when claiming performance; use a generic steep-slope contrast when the data is not available.
  * *The Friction Demonstration:* Rapid abrasion, scratch tests, or weight drops can dramatize durability; name the actual material, load, cycles, and outcome or label the sequence conceptual.

### Class 3: The Visceral Sensory Ritual (Sensory Climax & Craving)
* **Definition:** Hyper-tactile macro cinematography that makes texture, fluidity, sound, appetite, or craft easy to imagine. It can create desire without claiming a universal neural or conversion effect.
* **Primary Funnel Role:** Top-of-funnel paid social thumb-stops (0–3s hooks), organic viral Reels/Shorts, brand identity films.
* **Core Mechanisms:**
  * *The 120fps Viscous Pour:* Golden oil, syrup, or concentrate cascades onto food or into a vessel, with ribbons folding in hyper-detailed micro-droplet slow motion.
  * *The Dermal Absorption & Melt:* Dropper releases a single botanical drop onto the cheekbone; fingertips glide once, and the formula transforms from a glossy bead into an absorbed, radiant finish.
  * *The Mechanical Actuation ASMR:* Knurled dials clicking into place, magnetic lids snapping shut with crisp tactile resistance, switches throwing with solid weight.

### Class 4: The Kinetic Habitat (Contextual Motion & Aspiration)
* **Definition:** The product operating in its natural or aspirational environment during purposeful movement. Separate the visual mood from any unverified speed, safety, capacity, or durability claim.
* **Primary Funnel Role:** Brand campaign hero video, homepage background loops, retargeting social ads.
* **Core Mechanisms:**
  * *The Dawn Commuter Glide:* Low-angle tracking shot moving alongside a commuter traversing a sun-drenched bridge at 20 mph, capturing motion blur in the road and wheel spokes.
  * *The Architectural Sanctuary Reveal:* Slow push-in through a steaming sauna doorway or into a sun-drenched kitchen, establishing elevated lifestyle status.
  * *The Dynamic Stride & Fabric Drape:* Tracking shot following a model walking briskly through rain-slicked city streets, showcasing authentic garment movement and silhouette.

---

## 8. Optional 7-Block Kinesthetic Director's Rig Scaffold

To direct a complex generative shot, an operator can assemble the relevant blocks below. They are a checklist of useful decisions, not a mandatory syntax or a promise of repeatability. Omit blocks that do not serve the shot, and use a real plate, storyboard, 3D scene, or tool-specific control when that is more reliable.

```text
BLOCK 1: [ANCHORS & CONTINUITY]
→ Identify a supplied start/end frame, storyboard, real clip, or single reference when identity needs protection. Declare which rigid parts must remain stable and which materials may deform.

BLOCK 2: [CAMERA KINEMATICS & TRAJECTORY]
→ Choose a camera path (orbital arc, dolly push, crane, locked tripod), perspective, and speed curve that make the intended action legible.

BLOCK 3: [SPEED & RHYTHM]
→ Specify timing only where it helps. If using slow motion, distinguish capture rate from playback rate (for example, 120→24 fps = 0.2×; 120→30 fps = 0.25×).

BLOCK 4: [SUBJECT ACTION & MICRO-MECHANICS]
→ Describe the visible action: fluid thickness/cohesion, latch resistance, fabric flutter, spray, wheel rotation, contact, and result. Use measured values only when sourced.

BLOCK 5: [LIGHT & SHADOW]
→ Describe the highlight path, contact shadow, and contrast that help the viewer read material and depth; inspect the final render.

BLOCK 6: [DEPTH & ENVIRONMENT]
→ Use depth separation or particles (steam, mist, dust, road spray) only when they support the communication job and do not obscure the product.

BLOCK 7: [CHECKS & EXCLUSIONS]
→ List the few failures that would invalidate the shot (logo/label drift, impossible joints, finger penetration, unreadable result, seam flash, or frame judder), then inspect and rerender or recut as needed. A negative prompt is not a guarantee.
```

---

## 9. The Multi-Shot Commercial Narrative & Continuity Bridge

Many e-commerce video ads and product demonstrations benefit from a **10 to 30-second multi-cut sequence composed of 3 to 5 distinct shots**, while a single clear shot can be the better answer.

When creating multi-shot video sequences with generative AI models or human production crews, a common failure is **visual amnesia**: the product's color shifts between cuts, logo placement jumps, lighting flips from warm afternoon sun to cool morning light, or camera momentum abruptly dead-stops at the cut.

The following principles provide the **connective tissue** that allows models and operators to bridge individual shots into cohesive, multi-shot commercial narratives without constraining creative storytelling.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                     THE 3 CONTINUITY BRIDGES (CONNECTIVE TISSUE)                       │
├────────────────────────────────┬───────────────────────────────────────────────────────┤
│ BRIDGE                         │ HOW IT PREVENTS DISORIENTATION ACROSS CUTS            │
├────────────────────────────────┼───────────────────────────────────────────────────────┤
│ 1. The Match-Cut on Action     │ Kinetic momentum carries across the cut seam          │
│    (Momentum Bridge)           │ (e.g. bottle tipped in Shot 1 → liquid stream in Shot 2)│
├────────────────────────────────┼───────────────────────────────────────────────────────┤
│ 2. The Spatial Axis Bridge     │ Respects the 180° rule; avoid an unexplained side flip│
│    (Directional Consistency)   │ unexpectedly, preserving left-to-right orientation.   │
├────────────────────────────────┼───────────────────────────────────────────────────────┤
│ 3. The DNA Invariant Bridge    │ Color temperature (Kelvin), key-light azimuth, and    │
│    (Identity Lock)             │ product surface finish remain locked across all cuts. │
└────────────────────────────────┴───────────────────────────────────────────────────────┘
```

### The 3 Continuity Bridges (Connecting the Shots)

1. **The Match-Cut on Action (Kinetic Momentum Bridge):**
   * *Principle:* Cut on a continuous physical motion rather than between static moments when the seam benefits from it. If an actor begins unzipping a jacket or tipping a bottle in Shot 1, Shot 2 can cut mid-motion to a tighter angle where the zipper or liquid stream completes the trajectory at a compatible velocity.
   * *Natural Language Guidance:* *"Shot transition cuts on action: the forward momentum initiated in Shot 1 continues seamlessly across the cut into Shot 2 along the same directional vector."*

2. **The Spatial Axis Bridge (The 180-Degree Rule):**
   * *Principle:* Keep the camera on one side of the primary axis when directional continuity matters. If a runner or e-bike is traveling left-to-right in Shot 1, avoid placing the camera on the opposite side in Shot 2 unless the reversal is intentional and legible.
   * *Natural Language Guidance:* *"Camera maintains spatial axis discipline along the 180-degree line; subject motion maintains consistent left-to-right trajectory across sequential cuts."*

3. **The DNA Invariant Bridge (Identity & Set Lock):**
   * *Principle:* Define the persistent physical constants in each prompt when the generative model needs help preserving identity across cuts.
   * *The 3 Invariants:*
     * **Material DNA:** Specific hex color, surface texture, and finish (e.g., *"matte-olive 6061 aluminum with satin anodized sheen"*).
     * **Lighting DNA:** Fixed key light angle and color temperature (e.g., *"5600K key light positioned at 45° stage left across all cuts"*).
     * **Geometric DNA:** Relative proportions of bezels, logos, and dimensions remain locked.

---

### The 4-Beat Commercial Narrative Arc (Flexible Structural Grammar)

Rather than dictating a rigid script, this 4-beat arc is an optional commercial rhythm for 10-to-30-second video assets:

* **Beat 1: The Inciting Friction / Hook (0.0s – 2.5s)**
  * *Commercial Role:* Thumb-stop. Ruptures feed inertia through high visual contrast, an unexpected sensory dilemma, or extreme macro detail.
* **Beat 2: The Mechanism / Demonstration (2.5s – 7.0s)**
  * *Commercial Role:* Objection clearance. Shows *why* and *how* the product is intended to perform (internal exploded components, water beading, torque climb, scratch test), with claims tied to supplied evidence.
* **Beat 3: The Tactile Habitat & Human Workflow (7.0s – 11.0s)**
  * *Commercial Role:* Psychological ownership. Bridges the product to real-world human interaction (in-hand grip, smooth dial actuation, effortless unboxing, daily routine).
* **Beat 4: The Settled Specimen & Value Anchor (11.0s – 15.0s)**
  * *Commercial Role:* Decision settlement. Motion decelerates smoothly into a locked, pristine, illuminated packshot with clear branding and value realization.

---

### Illustrative Multi-Shot Assembly Walkthrough (Reference Guidance, Not an Allowlist)

* **Product Category:** Premium Insulated Thermal Tumbler (Scale 02)
* **Total Narrative Length:** 12.0s (4 Sequential Cuts)

* **Shot 1 (Beat 1: The Inversion Hazard Hook — 2.5s):**
  * *Prompt Guidance:* *"Tight medium shot. A human hand lifts a brushed stainless steel tumbler and rotates it completely upside down directly over an open, illuminated laptop keyboard. Camera pushes in slightly. Use a natural motion-blur treatment and a controlled contrast. Motion cuts mid-shake as the lid holds; use the supplied documented result or frame the dry-keyboard outcome as a conceptual pain-to-relief contrast."*
* **Shot 2 (Beat 2: The Internal Vacuum Seal Teardown — 3.5s):**
  * *Prompt Guidance:* *"Match-cut on action into an extreme macro exploded view of the supplied lid mechanism. As the tumbler is inverted, internal CAD-like components separate along the Z-axis, catching controlled specular wipes along the polished edges. Use only documented construction details; an exploded render explains a mechanism but does not prove airtight performance by itself."*
* **Shot 3 (Beat 3: The Tactile Countertop Workflow — 3.0s):**
  * *Prompt Guidance:* *"Spatial axis maintained. Cut to medium lifestyle shot. The tumbler is placed firmly onto a natural stone counter with a readable contact shadow. Hand presses the supplied slider lid with a visible tactile click and smooth mechanical resistance under warm daylight; match the lighting to the source."*
* **Shot 4 (Beat 4: The Settled Packshot & Brand Anchor — 3.0s):**
  * *Prompt Guidance:* *"Decelerating camera arc into a locked 85mm macro hero packshot. The tumbler sits motionless, illuminated by soft rim lighting with a clean specular glint along the rim, perfectly upright and stable, branding crisp and centered."*

---

## 10. End-to-End Production Assembly Walkthroughs

The following four production assemblies demonstrate the 7-Block protocol in practice across diverse product scales:

### Assembly 1: Micro/Cosmetics (Scale 01) — Dermal Absorption & Viscous Squeeze
* **Class:** Class 3 (The Visceral Sensory Ritual)
* **Scale File:** `01-micro-intimate.md` | **Duration:** 4.0s (96 frames at 24fps)
* **Placement & Intent:** Cold Social Paid Ad (Meta/TikTok 9:16)
* **Frame 0 (Start Anchor):** 30ml amber glass dropper bottle held above clean forearm skin, single drop suspended at pipette tip.
* **Frame N (End Anchor):** Dewy, radiant skin patch with the supplied or clearly labeled conceptual finish; bottle resting in background bokeh. A generated end state is not an absorption or safety result.

```text
BLOCK 1 (ANCHOR & RIGID BODY):
Image-to-Video conditioned on Frame 0 start anchor and Frame N end anchor. The 30ml amber glass bottle, white rubber bulb, and glass pipette are rigid non-deformable solids with permanent structural volume conservation.

BLOCK 2 (CAMERA KINEMATICS):
Camera locked on a rock-solid tripod rig, 85mm macro lens, ultra-shallow f/2.0 depth of field. Center-frame framing focused on the forearm skin surface.

BLOCK 3 (SPEED RAMP CADENCE):
0.0s–0.8s real-time 24fps as pipette positions. 0.8s–2.8s slow motion as the droplet releases and impacts; if captured at 120fps and played at 24fps, that segment is 0.2×. 2.8s–4.0s smooth return to 24fps as the formula spreads and settles.

BLOCK 4 (SUBJECT KINETIC ACTION):
Pipette releases a single, visibly viscous golden-amber droplet. The droplet falls a short, deliberate distance, impacts the skin surface, and flattens into a glistening dome. Clean natural fingertips glide across the skin once, spreading it into the supplied or conceptual finish. Do not turn the render into a claim about absorption, hydration, residue, or safety unless those outcomes are documented.

BLOCK 5 (SPECULAR & SHADOW):
Key light overhead creates a sharp pinpoint specular glint on the falling oil droplet. As the droplet spreads, a broad soft reflection expands across the hydrated skin surface. Crisp contact occlusion shadow under the droplet that dissolves as it absorbs.

BLOCK 6 (PARALLAX STAGE):
Subordinate studio background rendered 3 stops darker in deep warm sepia bokeh. Microscopic skin pores and natural micro-texture remain razor-sharp in the focal plane.

BLOCK 7 (TEMPORAL INVARIANTS):
Inspect logo and amber-bottle continuity, hand anatomy, skin blending or phase-through, droplet trajectory, and frame interpolation; rerender or recut visible failures.
```

---

### Assembly 2: Handheld CPG (Scale 02) — High-Stakes 180° Inversion Demonstration
* **Class:** Class 2 (The Documented Kinetic Demonstration)
* **Scale File:** `02-handheld-tabletop.md` | **Duration:** 5.0s (120 frames at 24fps)
* **Placement & Intent:** Retargeting / Consideration Ad (BOFU Objection Killer)
* **Frame 0 (Start Anchor):** 16oz stainless steel insulated tumbler upright on concrete counter next to an open, illuminated MacBook keyboard.
* **Frame N (End Anchor):** Tumbler held completely upside down (180° inverted) directly over the dry laptop keyboard; use a documented dry result or label the frame as a conceptual relief state.

```text
BLOCK 1 (ANCHOR & RIGID BODY):
Image-to-Video conditioned on Frame 0 start anchor and Frame N end anchor. Tumbler body is a rigid, non-deformable brushed 18/8 stainless steel cylinder. The matte black polymer lid and latch mechanism are solid rigid bodies.

BLOCK 2 (CAMERA KINEMATICS):
Smooth 35mm wide-angle push-in on a motorized slider, tracking forward 12 inches at eye level, maintaining both the inverted tumbler lid and the laptop keyboard in sharp crisp focus at f/4.0.

BLOCK 3 (SPEED RAMP CADENCE):
0.0s–1.0s fast 1.5x speed as hand grips and inverts the tumbler. 1.0s–4.0s held in tense, rock-solid real-time (24fps) inversion. 4.0s–5.0s settled locked hold with zero motion.

BLOCK 4 (SUBJECT KINETIC ACTION):
A confident human hand firmly grips the stainless steel tumbler, lifts it, and rotates it completely upside down (180° inversion) directly above the open laptop keys. The tumbler is given two deliberate downward shakes. If this is a documented demonstration, show the supplied fill, hold time, shake protocol, and observed result; if it is synthetic, frame the dry-keyboard outcome as an illustration of the desired relief rather than a test claim.

BLOCK 5 (SPECULAR & SHADOW):
Hard overhead studio directional light sweeps a crisp linear specular highlight along the brushed steel body during the rotation. Sharp contact occlusion shadow cast by the inverted tumbler directly across the laptop spacebar and trackpad.

BLOCK 6 (PARALLAX STAGE):
Foreground tumbler moves rapidly down-frame, creating dynamic parallax over the stationary keyboard. Background minimalist concrete wall sits in soft focus 2 stops underexposed.

BLOCK 7 (TEMPORAL INVARIANTS):
Inspect tumbler and lid continuity, liquid behavior, keyboard geometry, hand anatomy, contact shadows, and frame stability. Treat visual stability as a craft check, not evidence of seal performance.
```

---

### Assembly 3: Body-Worn Apparel (Scale 03) — Hydrostatic Deluge Demonstration & Stride
* **Class:** Class 2 (The Documented Kinetic Demonstration)
* **Scale File:** `03-body-worn-apparel.md` | **Duration:** 4.5s (108 frames at 24fps)
* **Placement & Intent:** PDP Rich Media & Paid Social Performance
* **Frame 0 (Start Anchor):** Technical storm-shell jacket worn by an athletic model in a dark studio cyclorama.
* **Frame N (End Anchor):** Torso under the supplied or conceptual water exposure; use the documented result when available and label an idealized dry-fabric state as illustrative.

```text
BLOCK 1 (ANCHOR & RIGID BODY):
Image-to-Video conditioned on Frame 0 start anchor and Frame N end anchor. Jacket anatomical shell geometry is conserved; ripstop face fabric possesses intentional mechanical drape without implausible synthetic stretching.

BLOCK 2 (CAMERA KINEMATICS):
Camera tracking backward on a motorized dolly at 4 mph, matching the model's forward walking stride. 50mm prime lens at f/2.8, framed medium-close from chest to mid-thigh.

BLOCK 3 (SPEED RAMP CADENCE):
0.0s–0.8s real-time stride. 0.8s–3.5s slowed as the deluge strikes the chest; if captured at 120fps and played at 24fps, that segment is 0.2×. 3.5s–4.5s returns to 24fps stride with water rolling away.

BLOCK 4 (SUBJECT KINETIC ACTION):
Model strides forward with natural athletic cadence. A supplied or clearly illustrative water exposure strikes the jacket. Show the observed beading, wetting, runoff, or saturation behavior and label the pressure, duration, angle, and result when making a performance claim; a synthetic ideal-beading scene is a visual contrast, not a hydrostatic test.

BLOCK 5 (SPECULAR & SHADOW):
High-contrast directional rim lighting illuminates each individual falling water bead like a glistening crystal prism. Specular highlights trace the micro-textured ripstop weave without blowing out the dark storm-grey matte fabric.

BLOCK 6 (PARALLAX STAGE):
Wet studio cyclorama floor reflects the model's footsteps with dark liquid reflections. Background dark void sits 3 stops darker, creating strong separation for the water droplets.

BLOCK 7 (TEMPORAL INVARIANTS):
Inspect jacket seam and logo continuity, face anatomy, fabric drape, water-to-fabric contact, and any phase-through. Do not infer waterproofing from a clean-looking render alone.
```

---

### Assembly 4: Mobility & Transport (Scale 06) — Hill-Climb Torque Demonstration
* **Class:** Class 2 (The Documented Kinetic Demonstration)
* **Scale File:** `06-mobility-transport.md` | **Duration:** 5.0s (120 frames at 24fps)
* **Placement & Intent:** Retargeting Ad & Amazon Video Hero
* **Frame 0 (Start Anchor):** Electric all-terrain commuter bike at the base of a supplied or illustrative steep paved incline.
* **Frame N (End Anchor):** E-bike midway up the incline; if speed, grade, load, effort, and battery state matter, use the documented test result rather than inventing them.

```text
BLOCK 1 (ANCHOR & RIGID BODY):
Image-to-Video conditioned on Frame 0 start anchor and Frame N end anchor. Hydroformed aluminum bike frame, battery casing, motor hub, and handlebars remain visually rigid; inspect for implausible structural flex.

BLOCK 2 (CAMERA KINEMATICS):
Low-angle tracking camera mounted on a stabilization chase vehicle parallel to the e-bike, 35mm lens at f/3.5, keeping the bottom bracket and rear motor hub locked in the lower-third frame.

BLOCK 3 (SPEED RAMP CADENCE):
0.0s–0.6s real-time entry into the hill. 0.6s–3.5s steady-speed tracking up the supplied grade at the documented or deliberately illustrative pace. 3.5s–5.0s gentle crane-up revealing the crest of the hill.

BLOCK 4 (SUBJECT KINETIC ACTION):
The rider leans slightly forward with a controlled posture as the rear hub motor and tires carry the bike uphill. If this is a performance claim, show the documented grade, rider and payload, speed, mode, cadence, battery state, and observed effort; if synthetic, use the motion to illustrate intended torque relief without claiming measured wattage or effortless performance.

BLOCK 5 (SPECULAR & SHADOW):
Low-angle morning sun creates long crisp contact shadows of the spinning tires on the steep asphalt. Golden specular edge highlights sweep along the matte-olive top tube as the bike ascends.

BLOCK 6 (PARALLAX STAGE):
Steep hillside grade provides dramatic diagonal perspective. A distant skyline may move through the frame to make the climb legible, but parallax is a visual cue, not proof of measured elevation gain.

BLOCK 7 (TEMPORAL INVARIANTS):
Inspect frame geometry, wheel circles and spoke motion, pedal cadence, rider anatomy, clothing flutter, and background continuity. Treat these as render checks separate from the measured performance record.
```

---

## 11. Direct-Response Video Funnel Architecture & Measurement

To learn whether a video is doing its job, map each segment to a measurable viewer or business question. The figures below are not universal benchmarks: set targets from the account baseline, spend, audience, platform, and experiment design, then compare like with like.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   THE DIRECT-RESPONSE VIDEO FUNNEL METRICS MATRIX                      │
├─────────────────────┬──────────────────┬─────────────────┬─────────────────────────────┤
│ VIDEO SEGMENT       │ FUNNEL ROLE      │ BENCHMARK KPI   │ KINETIC AI OBJECTIVE        │
├─────────────────────┼──────────────────┼─────────────────┼─────────────────────────────┤
│ 0.0s – 1.5s         │ The Thumb-Stop   │ Set from baseline│ Context, contrast, tension  │
│ 1.5s – 5.0s         │ The Demonstration│ Set from baseline│ Evidence or useful contrast │
│ 5.0s – 10.0s        │ The Mechanism    │ Set from baseline│ Internal teardown / how     │
│ 10.0s – 15.0s       │ The Conversion   │ Set from baseline│ Packaging reveal & clear CTA│
└─────────────────────┴──────────────────┴─────────────────┴─────────────────────────────┘
```

### The Atomic Modular Creative Matrix ($4 \times 3 \times 2 = 24$ Ads)
For algorithmic advertising, a modular matrix can make testing and iteration cheaper than one monolithic edit. Treat the matrix as a planning example, not a claim about every platform or a guaranteed fatigue window. Build **Atomic Modular Bricks** when the account has enough evidence and traffic to learn from them:

* **4 Distinct Hooks (0.0s – 3.0s):**
  1. *The Torture Impact Hook:* High-velocity drop, scratch, or water blast.
  2. *The Inversion Hazard Hook:* Tumbler inverted over expensive electronics.
  3. *The Extreme Macro ASMR Hook:* 120fps slow-mo droplet or tactile click.
  4. *The Polarizing Split Hook:* Side-by-side generic lower-quality reference vs. our supplied hero; do not imply a named competitor or unsupported product fact.
* **3 Distinct Demonstration Bodies (3.0s – 8.0s):**
  1. *Internal Engineering Teardown:* Exploded view showing supplied materials/components versus a generic poor construction reference when that contrast is relevant.
  2. *Real-World Stress Demonstration:* Supplied hill-climb or deluge conditions, or a clearly illustrative generic contrast.
  3. *Multi-Body Fit / Absorption Test:* Side-by-side demonstration across use cases.
* **2 Distinct Conversion Outros (8.0s – 12.0s):**
  1. *In-Hand Ergonomic Scale & Unboxing:* Clean studio unboxing and hand grip.
  2. *Supported Offer & Guarantee:* Crisp product packshot settle with a real guarantee, availability, or next step; never invented scarcity.

$$\text{Total Production Yield} = 4 \text{ Hooks} \times 3 \text{ Bodies} \times 2 \text{ Outros} = \mathbf{24\text{ Unique Video Ads}}$$

---

## 12. Bimodal Sensory Architecture & ASMR Foley Specifications

Sound-on and sound-off behavior varies by audience, placement, device, and account. Design an intentional route for each: let the visual carry the essential proposition when needed, and use tactile sound to deepen the action when audio is available. Measure the effect in the actual account rather than importing a universal lift.

### Mode 1: Silent Visual Autonomy (Muted Feeds)
* When the placement commonly starts muted, make the core problem, contrast, action, and next step understandable without audio. This is a design choice, not a universal requirement.
* Use **Kinetic Micro-Labels** when they clarify a visible or documented detail. Pull specs from the supplied record (for example, *"[SUPPORTED WATER TEST]"* or *"[DOCUMENTED MATERIAL]"*); do not invent ratings, purity, or airtightness.
* Visual cues can make physical force legible (water splashing, tire flex, steam expansion) without exaggerating an unverified performance claim.

### Mode 2: Tactile ASMR Psychoacoustics (Unmuted Feeds)
When unmuted, the video can use **hyper-isolated, tactile Foley sound design** when that serves the product and audience. Generic music is an optional creative choice, not a universal failure:

| Product Scale | Tactile Visual Action | Foley Sound Specification | Psychoacoustic Impact |
| :--- | :--- | :--- | :--- |
| **Scale 01 (Micro)** | Dropper bulb release & skin spread | Soft air-suction release, velvet skin glide | Intimacy, premium purity |
| **Scale 02 (Handheld)** | Tumbler lid snap, bottle cap twist | Crisp metallic mechanical click, deep closure "thwip" | Secure-feeling closure, craft |
| **Scale 03 (Apparel)** | Storm shell deluge impact | High-frequency water droplet pitter-patter, clean fabric snap | Weather confidence / relief |
| **Scale 04 (Countertop)**| Espresso lever pull, steam vent | Heavy solid brass mechanical clunk, pressurized steam hiss | Commercial power, luxury engineering |
| **Scale 05 (Macro)** | Sauna door latch, cold plunge dip | Heavy solid cedar door latch thud, deep water displacement | Sanctuary peace, high ticket justification |
| **Scale 06 (Mobility)** | Bike tire on asphalt, folding frame latch | Low-frequency tire hum, sharp solid aluminum pin click | Torque confidence, rugged reliability |

---

## 13. Mobile Safe-Zone Geometry & Technical Specifications

For vertical placements, composition must respect the current platform interface overlays. Treat the diagram as an approximate starting composition, then validate the crop and controls in the actual destination:

```
┌─────────────────────────────────────────────────────────┐
│ [TOP UI BUFFER — VERIFY IN DESTINATION]                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│                                                         │
│             THE CORE KINETIC ACTION ZONE               │
│            • Product bounding boxes                    │
│            • Critical demonstrations                   │
│            • Helpful micro-labels                      │
│                                                         │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ [BOTTOM UI BUFFER — VERIFY IN DESTINATION]             │
└─────────────────────────────────────────────────────────┘
```

### Technical Render Specifications
* **Primary Aspect Ratio:** `9:16` (1080×1920) for paid social and mobile PDPs.
* **Secondary Aspect Ratio:** `1:1` (1080×1080) for desktop PDP carousels and multi-platform catalogs.
* **Framerate:** Choose capture, playback, and delivery rates for the source, motion, platform, and tool. 24fps can suit a cinematic treatment; 30fps or another rate may be the right choice. Validate cadence and motion blur.
* **Slow-Motion Example:** 120fps captured and played at 24fps yields 0.2×; 120fps played at 30fps yields 0.25×. Preserve the source/timebase math in the edit.
* **Post-Processing:** Use denoising, upscaling, stabilization, or a tool such as Topaz only when inspection shows a problem and the pass preserves detail, type, texture, and brand identity.

---

## 14. Master Video Scale Navigator

| Video Scale / Paired Reference | Physical Bracket | Core Motion Craft | Primary Failure Mode Avoided |
| :--- | :--- | :--- | :--- |
| **Scale 01 — [micro-intimate image reference](../ecommerce-image-lookbooks/01-micro-intimate.md)** | Under 6 inches | Fluid viscosity, dropper surface tension, skin spread | Disappearing droppers, melting fingers |
| **Scale 02 — [handheld-tabletop image reference](../ecommerce-image-lookbooks/02-handheld-tabletop.md)** | 6 to 18 inches | Inversion demonstrations, pour cascades, unboxing pulls | Label morphing, rubbery tumbler warping |
| **Scale 03 — [body-worn apparel image reference](../ecommerce-image-lookbooks/03-body-worn-apparel.md)** | Body-Worn | Stride drape, water exposure, stretch recovery | Floating garments, anatomical distortion |
| **Scale 04 — [countertop appliance image reference](../ecommerce-image-lookbooks/04-countertop-appliances.md)** | 1.5 to 3 feet | Exploded assemblies, extraction streams, lever actuation | Plastic melting, boiler geometry loss |
| **Scale 05 — [architectural macro image reference](../ecommerce-image-lookbooks/05-architectural-macro.md)** | 3 to 10+ feet | Door swings, steam sanctuary reveals, living walkthroughs | Warping walls, inconsistent perspective |
| **Scale 06 — [mobility transport image reference](../ecommerce-image-lookbooks/06-mobility-transport.md)** | 4 to 12+ feet | Hill-climb illustration, transit folds, road tracking | Oval wheel warping, spoke flickering |

---

## 15. Complete Directory Structure

* **[`INDEX.md`](INDEX.md)** *(This file)* — Adaptable motion craft references, optical cues, optional director scaffold, continuity bridges, video jobs, platform checks, and measurement guidance.
* **Paired image references:** The six scale-specific image lookbooks in `../ecommerce-image-lookbooks/` provide still-image archetypes and scale context. This video directory intentionally has no unadvertised per-scale files or motion-dialect registry.

---

## 16. Foundational References, Theoretical Attribution & Source Directory

The references below inform selected craft ideas in this lookbook. They are not proof that a prompt block, aesthetic choice, or performance target will work universally. Read them when a decision needs deeper grounding, and validate the resulting asset in its actual context:

### I. Cinematographic Optics & Camera Physics
* **American Society of Cinematographers (ASC):**
  * *Primary Contribution:* Foundational cinematographic standards, optical mechanics, and camera operation protocols.
  * *Key Frameworks Used:* Shutter-angle and exposure starting points; natural motion blur; optical focal-length characteristics for commercial packshots.
  * *Seminal Work:* *American Cinematographer Manual* (ASC Press, 10th/11th Eds., ed. Michael Goi / Stephen H. Burum).
* **Blain Brown:**
  * *Primary Contribution:* Practical cinematography theory, lighting contrast, and visual storytelling mechanics.
  * *Key Frameworks Used:* Key-to-fill lighting contrast ratios (2:1 commercial high-key vs. 6:1 luxury chiaroscuro); camera movement axes (dolly, truck, pedestal, pan, tilt); dynamic lens perspective.
  * *Seminal Work:* *Cinematography: Theory and Practice: Image Making for Cinematographers and Directors* (Routledge / Focal Press, 4th Ed., 2021).
* **Sidney F. Ray:**
  * *Primary Contribution:* Applied photographic and cinematographic optics.
  * *Key Frameworks Used:* Focal Length Compression & Geometric Rectification (Principle 1); eliminating wide-angle barrel distortion on manufactured goods using telecentric and 85mm–105mm optical perspectives.
  * *Seminal Work:* *Applied Photographic Optics: Lenses and Optical Systems for Photography, Film, Video, Electronic and Digital Imaging* (Focal Press, 3rd Ed., 2002).
* **David Bordwell & Kristin Thompson:**
  * *Primary Contribution:* Film form, shot duration, and temporal continuity.
  * *Key Frameworks Used:* Time-remapping, variable frame-rate kinematics, and shot-to-shot spatial-temporal continuity.
  * *Seminal Work:* *Film Art: An Introduction* (McGraw-Hill, 12th Ed., 2019).

### II. Classical Mechanics, Optical Physics & Computer Vision
* **Herbert Goldstein, Charles P. Poole, & John L. Safko:**
  * *Primary Contribution:* Classical mechanics and rigid-body dynamics.
  * *Key Frameworks Used:* Rigid-body dynamics and conservation concepts as useful language for protecting manufactured geometry during rotational camera moves; a prompt cannot enforce them in a generative model.
  * *Seminal Work:* *Classical Mechanics* (Addison-Wesley / Pearson, 3rd Ed., 2001).
* **Augustin-Jean Fresnel, Kenneth E. Torrance, & Ephraim M. Sparrow:**
  * *Primary Contribution:* Physical optics, Fresnel reflectance equations, and microfacet specular reflection models.
  * *Key Frameworks Used:* Fresnel reflectance and microfacet behavior as references for making a highlight sweep across a chamfered surface; the resulting render still needs inspection.
  * *Seminal Works:* *Mémoire sur la loi des modifications que la réflexion imprime à la lumière polarisée* (Fresnel, 1823); "Theory for Off-Specular Reflection From Roughened Surfaces" (Torrance & Sparrow, *Journal of the Optical Society of America*, 1967).
* **Hermann von Helmholtz & James J. Gibson:**
  * *Primary Contribution:* Physiological optics, ecological approach to visual perception, and motion parallax.
  * *Key Frameworks Used:* Motion parallax and optical flow as staging cues for depth; differential movement can make volume easier to read but does not prove physical depth or measurement.
  * *Seminal Works:* *Handbuch der physiologischen Optik* (Helmholtz, 1867); *The Perception of the Visual World* (Gibson, Houghton Mifflin, 1950); *The Senses Considered as Perceptual Systems* (Gibson, 1966).

### III. Perception, Touch & Viewer Simulation
* **Giacomo Rizzolatti, Leonardo Fogassi, & Vittorio Gallese (University of Parma):**
  * *Primary Contribution:* Research on mirror-neuron systems and embodied simulation.
  * *Key Frameworks Used:* Purposeful, tactile human interaction can make an action easier to imagine. Do not turn this literature into a guaranteed neural, ownership, or conversion effect.
  * *Seminal Works:* "The Mirror-Neuron System" (Rizzolatti & Craighero, *Annual Review of Neuroscience*, 2004); "Embodied Simulation: From Neurons to Phenomenal Experience" (Gallese, *Phenomenology and the Cognitive Sciences*, 2005).
* **Joann Peck, Suzanne B. Shu, & S. Adam Brasel:**
  * *Primary Contribution:* Haptic interfaces, psychological ownership, and consumer touch psychology.
  * *Key Frameworks Used:* Visual and actual touch can influence perceived ownership in particular contexts. Use firm grip, micro-compression, and material deformation to make handling legible; do not import a universal percentage lift.
  * *Seminal Works:* "The Effect of Mere Touch on Perceived Ownership" (Peck & Shu, *Journal of Consumer Research*, 2009); "Tablets, Touchscreens, and Touchpads: How Touch Interfaces Influence Psychological Ownership" (Brasel & Gips, *Journal of Consumer Psychology*, 2014).
* **Alfred L. Yarbus:**
  * *Primary Contribution:* Eye movements, fixations, and visual habituation.
  * *Key Frameworks Used:* Eye movements and task-dependent viewing. Use an early visual change when it serves the communication job; the source does not establish a universal 0.8-second drop-off rule.
  * *Seminal Work:* *Eye Movements and Vision* (Plenum Press, 1967).

### IV. Generative Video Architectures & Temporal Diffusion Mechanics
* **Jonathan Ho, Tim Salimans, Alexey Gritsenko, William Chan, Mohammad Norouzi, & David J. Fleet:**
  * *Primary Contribution:* Video Diffusion Models (VDMs) and spatial-temporal factorized attention.
  * *Key Frameworks Used:* Temporal error accumulation as a useful way to reason about drift; start/end anchors can reduce uncertainty in some tools but cannot eliminate it.
  * *Seminal Work:* "Video Diffusion Models" (NeurIPS, 2022).
* **Andreas Blattmann, Robin Rombach, Huan Ling, Tim Dockhorn, Seung Wook Kim, Sanja Fidler, & Karsten Kreis:**
  * *Primary Contribution:* Stable Video Diffusion (SVD) and high-resolution latent video synthesis.
  * *Key Frameworks Used:* Image-to-video conditioning mechanisms and the practical value of separating camera and subject complexity; no prompt law prevents attention or identity drift.
  * *Seminal Work:* "Stable Video Diffusion: Scaling Latent Video Diffusion Models to Large Datasets" (arXiv:2311.15127, 2023).
* **John Lasseter (Pixar Animation Studios):**
  * *Primary Contribution:* The 12 basic principles of animation applied to computer-generated motion.
  * *Key Frameworks Used:* Squash and stretch (restricted to fluids/soft goods); anticipation and staging; slow-in and slow-out (kinesthetic speed ramps); solid drawing (rigid body invariance).
  * *Seminal Work:* "Principles of Traditional Animation Applied to 3D Computer Animation" (*ACM SIGGRAPH Computer Graphics*, 1987).

### V. Direct-Response Video Funnel Economics & Algorithmic Creative
* **Meta Business Engineering & Performance Marketing Standards:**
  * *Primary Contribution:* Algorithmic feed video metrics, drop-off curves, and creative diversification.
  * *Key Frameworks Used:* A funnel measurement matrix (thumb-stop, hold, mechanism, and action) and modular creative testing. Set KPI thresholds from the account baseline and experiment design; a 4 × 3 × 2 matrix yields 24 edit combinations as a planning example, not a guaranteed fatigue or auction outcome.
  * *Documentation & Industry Data:* Meta Business Help Center — *Video View & Engagement Metrics Benchmarks* (Continuous updates).
* **TikTok Creative Center Research:**
  * *Primary Contribution:* Short-form mobile video retention dynamics.
  * *Key Frameworks Used:* Vertical composition, changing mobile UI overlays, early context, and concise micro-labels. Validate current safe zones and retention behavior in the destination rather than treating fixed percentages as laws.
  * *Reference:* *TikTok What's Next Report & Creative Playbook* (TikTok for Business, Annual Benchmark Studies).
* **Eugene Schwartz:**
  * *Primary Contribution:* Prospect awareness levels and market sophistication.
  * *Key Frameworks Used:* Mapping cold acquisition ads (Unaware / Problem Aware) vs. retargeting demonstrations (Solution / Product Aware) vs. PDP loops (Most Aware).
  * *Seminal Work:* *Breakthrough Advertising* (1966).

### VI. Psychoacoustics, Foley Sound & Crossmodal Sensory Perception
* **Charles Spence (Oxford University Crossmodal Research Laboratory):**
  * *Primary Contribution:* Crossmodal sensory integration, multisensory flavor/product perception, and audio-visual correspondence.
  * *Key Frameworks Used:* Crossmodal Foley design (Section 12); crisp clicks, releases, and liquid pours can shape how a scene is interpreted. Treat the effect as contextual, then measure it.
  * *Seminal Works:* *Crossmodal Correspondences: A Tutorial Review* (*Attention, Perception, & Psychophysics*, 2011); *The Perfect Meal: The Multisensory Science of Food and Dining* (Wiley-Blackwell, 2014).
* **Emma L. Poerio, Ernestine C. Blake, Thomas J. Hostler, & Giulia L. Poerio:**
  * *Primary Contribution:* Physiological and psychological validation of Autonomous Sensory Meridian Response (ASMR).
  * *Key Frameworks Used:* Near-field tactile sound can produce different affective responses for some listeners. Use whisper, soft tap, or liquid draw when it fits the audience; do not promise lower heart rate, trust, or purchase intent.
  * *Seminal Work:* "More Than a Feeling: Autonomous Sensory Meridian Response (ASMR) Is Characterized by Reliable Changes in Affect and Physiology" (*PLOS ONE*, 2018).
* **Mobile sound-off research (platform or publisher studies):**
  * *Primary Contribution:* Sound-off behavior varies by surface, audience, device, and time.
  * *Key Frameworks Used:* Offer a sound-off route when the placement needs it, then test comprehension and completion in the actual account. Do not reuse a fixed muted-viewing percentage or completion lift as a universal fact.

### VII. Legendary Direct-Response Video Directors & Modern Performance Operators
* **The Harmon Brothers (Daniel & Benton Harmon, Harmon Brothers Agency):**
  * *Primary Contribution:* Well-known direct-response video practitioners whose public work demonstrates pattern interruption, physical problem dramatization, mechanism explanation, and comparative positioning.
  * *Key Frameworks Used:* The Pattern-Interrupt / Shock Torture Hook; the Visceral Physical Problem Dramatization; the Internal Teardown Mechanism; addressing price resistance through comparative demonstration. Adapt the intensity to the product, audience, and evidence.
  * *Seminal Work / Resource:* *From Script to Screen: The Harmon Brothers Video Ad Blueprint* (2018).
* **Sir Roger Deakins (CBE, ASC, BSC):**
  * *Primary Contribution:* 2-time Academy Award-winning cinematographer (*1917*, *Blade Runner 2049*, *Skyfall*, *No Country for Old Men*).
  * *Key Frameworks Used:* Motivated naturalistic lighting; disciplined eye-level camera placement; practical camera movement along a singular deliberate axis when it helps; texture rendering through contrast rather than saturation.
  * *Seminal Works:* *Byways* (2021); *Team Deakins Cinematography Podcast & Lighting Masterclass Archives*.
* **Cody Plofker (CMO, Jones Road Beauty) & Dara Denney (Performance Creative Director):**
  * *Primary Contribution:* Foremost modern practitioners of algorithmic direct-response video advertising on Meta and TikTok.
  * *Key Frameworks Used:* The Atomic Modular Creative Matrix ($4 \text{ Hooks} \times 3 \text{ Bodies} \times 2 \text{ Outros}$); rapid iteration based on platform drop-off curves (Thumb-Stop / Hook Rate vs. Hold Rate); native mobile safe-zone composition; unboxing and texture application pacing.
  * *Practical Resources:* *Cody Plofker's DTC Growth Newsletter*; *Dara Denney's Performance Creative Masterclasses & Video Ad Breakdown Series*.
* **Nick Green & Todd Sullivan (Founders, Thrive Market & ButcherBox):**
  * *Primary Contribution:* High-retention subscription e-commerce video merchandising and cold traffic acquisition.
  * *Key Frameworks Used:* The "Unboxing Pull" and "Pantry Stockup Ritual" video archetypes; translating raw physical volume and packaging tactile quality into perceived subscription value.
