# Video Technical Checks & Scale Map

> Optional video craft notes. Open this only when it materially helps the selected starting point; the compact index and standalone assembly remain usable without it.
>
> Preserves safe-zone, render, and paired image-scale guidance.

## Mobile Safe-Zone Geometry & Technical Specifications

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

## Master Video Scale Navigator

| Video Scale / Paired Reference | Physical Bracket | Core Motion Craft | Primary Failure Mode Avoided |
| :--- | :--- | :--- | :--- |
| **Scale 01 — [micro-intimate image reference](../../ecommerce-image-lookbooks/01-micro-intimate.md)** | Under 6 inches | Fluid viscosity, dropper surface tension, skin spread | Disappearing droppers, melting fingers |
| **Scale 02 — [handheld-tabletop image reference](../../ecommerce-image-lookbooks/02-handheld-tabletop.md)** | 6 to 18 inches | Inversion demonstrations, pour cascades, unboxing pulls | Label morphing, rubbery tumbler warping |
| **Scale 03 — [body-worn apparel image reference](../../ecommerce-image-lookbooks/03-body-worn-apparel.md)** | Body-Worn | Stride drape, water exposure, stretch recovery | Floating garments, anatomical distortion |
| **Scale 04 — [countertop appliance image reference](../../ecommerce-image-lookbooks/04-countertop-appliances.md)** | 1.5 to 3 feet | Exploded assemblies, extraction streams, lever actuation | Plastic melting, boiler geometry loss |
| **Scale 05 — [architectural macro image reference](../../ecommerce-image-lookbooks/05-architectural-macro.md)** | 3 to 10+ feet | Door swings, steam sanctuary reveals, living walkthroughs | Warping walls, inconsistent perspective |
| **Scale 06 — [mobility transport image reference](../../ecommerce-image-lookbooks/06-mobility-transport.md)** | 4 to 12+ feet | Hill-climb illustration, transit folds, road tracking | Oval wheel warping, spoke flickering |

---

