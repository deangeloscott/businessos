# Image Creative Principles & Selection

> Optional craft notes. Open this only when it materially helps the selected image recipe; the scale menu and individual archetype are usable without it.
>
> These notes preserve the shared composition, persuasion, and selection guidance for adapting the standalone archetypes.

## How This Library Works

This library is a set of **90 reusable visual archetypes** organized across **6 physical product scales** (15 archetypes per scale), **4 commerce jobs**, and **16 optional brand dialects**. It is a craft reference: the model or operator selects, combines, adapts, or replaces a pattern according to the actual outcome, platform, tool, source material, and evidence available.

One useful way to browse the library is to select:
1. **The Product Scale File** (`01` through `06`) matching the product's physical dimensions.
2. **The Commerce Archetype Class** (*The Specimen*, *The Proof*, *The Habitat*, or *The Ritual*).
3. **The Desired Archetype** (each designed to address a customer question or fulfill a platform requirement).
4. *(Optional)* **A Brand Dialect** from `DIALECTS.md` to establish lighting, mood, color grade, and material palette.

Start from the communication job and the viewer's hesitation. A forceful problem-to-relief sequence, a generic ideal-versus-poor comparison, or a premium best-choice position can be excellent persuasion when the contrast is legible and the product facts behind any specific claim are supplied. A generic reference state is an illustration of an alternative experience; it is not a named competitor, test result, or established fact about the hero product. Keep those categories distinct in the brief and in the final asset.

Before generation, provide the strongest available product references, dimensions, label/package files, formula or material facts, test conditions, and usage constraints. When a source fact is unknown, choose a composition that does not assert it, or mark the result as a concept. Inspect the rendered output against those inputs; prompting for “accurate” text or geometry does not make it accurate.

```
┌─────────────────────────┐     ┌─────────────────────────┐     ┌─────────────────────────┐
│   1. PRODUCT SCALE      │  +  │   2. ARCHETYPE CLASS    │  +  │   3. BRAND DIALECT      │
│ (e.g. 06-mobility-      │     │ (Specimen, Proof,       │     │ (e.g. High-Performance  │
│  transport.md)          │     │  Habitat, Ritual)       │     │  from DIALECTS.md)      │
└─────────────────────────┘     └─────────────────────────┘     └─────────────────────────┘
                                             │
                                             ▼
                 [OPTIONAL 5-BLOCK DIRECTOR'S RIG SCAFFOLD]
                                             │
                                             ▼
                 [STUDIO-GRADE, BRAND-ALIGNED PRODUCT PHOTOGRAPH]
```

---

## Five Working Principles for E-Commerce AI Photography

Generative vision models fail in recurring ways, but behavior changes across providers, versions, inputs, and post-processing. Use the following principles as compact diagnosis and design prompts. They are conditional craft guidance, not universal model laws or a mandatory prompt syntax.

### Principle 1: Lead with the subject when subject fidelity matters
Name the product, source reference, material, finish, dimensions, and intended prominence early enough that the model understands the communication priority. This is a useful saliency heuristic; there is no reliable universal “first 15 tokens” threshold. Use a supplied image, vector label, mask, or post-render compositing when exact geometry or typography matters more than prose order.

### Principle 2: Give each asset a dominant viewer job
One clear claim or hesitation usually produces a more legible asset. A comparison, before/after, or staged sequence is still valid when its states are deliberately separated and the viewer can tell what is being compared. If the frame must carry multiple facts, use panels, labels, or a sequence rather than asking one ambiguous scene to do everything.

### Principle 3: Build hierarchy with observable contrast
Use focus, scale, luminance, color, depth, and negative space to keep the hero legible. “Two stops darker,” `f/2.8`, or a fixed occupancy percentage can be a starting point, not a universal requirement; adjust for white-background compliance, transparent goods, accessibility, the platform crop, and the brand dialect. Review the actual output at the intended display size.

### Principle 4: Use comparison direction as a visual metaphor, not a law
Left = problem/old/generic state and right = solution/hero state is a powerful, familiar grammar for pain-to-relief communication. Reverse it when the platform, culture, reading direction, narrative, or composition benefits. A generic poor-quality reference may be intentionally exaggerated to clarify the cost of the problem; do not attach a competitor's name, logo, or unverified attribute to it.

### Principle 5: Ground the scene and inspect the failure modes
Ask for believable contact, material texture, anatomy, fluid behavior, and edge continuity, then inspect the result for floating objects, warped type, extra limbs, impossible reflections, false measurements, and misleading performance. Prompts can guide these checks; they cannot replace them.

### Persuasion modes the operator can choose
The model may reason with the common white-hat / grey-hat / black-hat labels when selecting a persuasive approach. White-hat work is direct and evidence-led. Grey-hat work uses selective emphasis, strong contrast, urgency, and emotional pain framing while keeping the underlying statement supportable. Black-hat describes deceptive pressure such as fabricated scarcity, invented test results, impersonation, or dark-pattern concealment; treat it as a high-risk category to surface and evaluate, never as permission to turn an unknown into a fact. In every mode, the operator should understand which elements are generic illustration, hypothesis, supplied claim, or observed result.

---

## Four Commerce Archetype Jobs

The 90 archetypes across Scales `01` through `06` (15 per scale) are grouped into four common commerce jobs. A useful asset may combine jobs, use another structure, or omit a class when the viewer's question calls for it:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FOUR COMMERCE ARCHETYPE JOBS                             │
├──────────────────────┬──────────────────────┬───────────────────────────────┤
│ CLASS                │ COMMERCIAL ROLE      │ CORE COGNITIVE OBJECTIVE      │
├──────────────────────┼──────────────────────┼───────────────────────────────┤
│ 1. THE SPECIMEN      │ Truth & Geometry     │ Clear form, scale, and fit    │
│ 2. THE PROOF         │ Objection Resolution │ Explains a material hesitation  │
│ 3. THE HABITAT       │ Contextual Sanctuary │ Lifestyle aspiration & status │
│ 4. THE RITUAL        │ Sensory Climax       │ Desire, texture & contact     │
└──────────────────────┴──────────────────────┴───────────────────────────────┘
```

### Class 1: The Specimen (Truth & Geometry)
* **Definition:** A clear product reference for form, scale, fit, or included contents. A neutral cyclorama is useful when compliance or comparison is the job; context may be better when spatial understanding matters.
* **Primary Funnel Role:** Amazon/Google Shopping main image compliance, Shopify primary gallery slot 1, technical spec sheets.
* **Scale Archetype Examples:**
  * Scale 01: *The Compliant Hero Packshot* (Look 01), *Caustic Light & Glass* (Look 06), *Palm & Pocket Scale* (Look 07), *Regimen Bundle Trio* (Look 10), *Precision Micro-Tolerances* (Look 15)
  * Scale 02: *The Compliant Packshot* (Look 01), *In-Hand Grip & Scale* (Look 05), *Unboxing & Mailer Delivery* (Look 09), *4-Angle Contact Sheet* (Look 10), *Bundle Routine Matrix* (Look 14)
  * Scale 03: *The Ghost Mannequin Hero* (Look 01), *Curated Outfit Knolling* (Look 08), *Luxury Unboxing Presentation* (Look 10)
  * Scale 04: *The Master Countertop Hero* (Look 01), *Under-Cabinet Clearance Anchor* (Look 03), *Rear Utility & Cable Routing* (Look 07), *Accessory Bundle* (Look 10), *Floating Exploded Void* (Look 13)
  * Scale 05: *Ergonomic Headroom Clearance* (Look 03), *Spatial Door-Swing Footprint* (Look 06), *Utility & Drainage Access* (Look 07), *Dimensional Orthographic Blueprint* (Look 10), *Multi-Human Capacity Blueprint* (Look 12), *Freight Gateway Access* (Look 15)
  * Scale 06: *Studio Side-Profile Hero* (Look 01), *Trunk-Fold Compact Spatial Proof* (Look 04), *Dimensional Fit Blueprint* (Look 11), *Multi-Modal Transit Fold* (Look 15)

### Class 2: The Proof (Objection Resolution & Demonstration)
* **Definition:** The objection-crusher. A visual explanation, generic comparison, or documented demonstration that makes a performance, durability, material, sizing, or mechanism question easier to decide. A generated illustration can dramatize the mechanism or pain-to-relief contrast; it becomes evidence of a specific claim only when the depicted conditions and result are established by supplied or observed sources.
* **Primary Funnel Role:** Mobile PDP slots 2, 4, 6; paid social performance ads; landing page objection sections; return-rate reduction.
* **Scale Archetype Examples:**
  * Scale 01: *Microscopic Actives & Raw Extraction* (Look 02), *Formulation Purity Split* (Look 09), *Temporal Shelf-Life Stability* (Look 11), *Multi-Tone Compatibility Matrix* (Look 12), *Dermal Absorption & Clear Finish* (Look 13)
  * Scale 02: *Ingredients Knolling Purity* (Look 07), *Us vs. Them Quality Split* (Look 08), *Decadal Patina Maturation* (Look 11), *High-Stakes Inversion Zero-Leakage* (Look 13), *Thermal Barrier Condensation Proof* (Look 15)
  * Scale 03: *Macro Fabric Weave & Seams* (Look 03), *Pocket & Interior Capacity* (Look 04), *Gorpcore Weather Torture* (Look 06), *Multi-Body Fit Diversity* (Look 07), *Elasticity & Stretch Tension* (Look 09), *5-Year Break-In* (Look 11), *Dual-Model Real Fit Comparison* (Look 12), *Hydrostatic Deluge Beading* (Look 13), *Range-of-Motion Articulation* (Look 14)
  * Scale 04: *Precision Interface Knurling* (Look 04), *Easy-Clean Disassembly* (Look 06), *Sensory Output Proof* (Look 09), *10-Year Workhorse Resilience* (Look 11), *Engineering Teardown vs. Competitor* (Look 12), *Thermal PID Stability* (Look 14), *Acoustic Whisper-Quiet Proof* (Look 15)
  * Scale 05: *Structural Joinery & Timber Macro* (Look 04), *Material Weather Torture* (Look 09), *Noble Silvered Timber Decadal Weathering* (Look 11), *Problem vs. Sanctuary Relief Proof* (Look 14)
  * Scale 06: *Cockpit & Display Interface Macro* (Look 05), *Night Commuter Safety Architecture* (Look 08), *All-Weather Water & Mud Torture* (Look 09), *10,000-Mile Commuter Battle Proof* (Look 10), *30% Incline Hill-Climb Torque Proof* (Look 12), *Monsoon Electronic Immersion* (Look 14)

### Class 3: The Habitat (Contextual Sanctuary)
* **Definition:** The product residing in its natural, elevated, or useful environment. The room or setting can telegraph brand equity, taste, and lifestyle while the product retains the hierarchy appropriate to the frame; no occupancy percentage is universal.
* **Primary Funnel Role:** Homepage hero headers, brand campaign lookbooks, catalog editorial spreads, editorial press kits.
* **Scale Archetype Examples:**
  * Scale 01: *Domestic Vanity Altar* (Look 04), *Olfactory & Botanical Landscape* (Look 14)
  * Scale 02: *Luminous Morning Kitchen* (Look 02), *Countertop Flex (Foodie Pride)* (Look 04)
  * Scale 03: *High-Fashion Direct Flash* (Look 05), *Architectural Fashion Editorial Drape* (Look 15)
  * Scale 04: *Natural Habitat (Patio / Workshop / Studio)* (Look 08)
  * Scale 05: *Architectural Sanctuary Hero* (Look 01), *Twilight / Blue Hour Glow* (Look 02), *Multi-User Living Context* (Look 05), *Lived-In Domestic Sanctuary* (Look 08), *Biophilic Alpine / Coastal Dawn Sanctuary* (Look 13)
  * Scale 06: *Cargo Capacity & Utility Rigging* (Look 06), *Overland Wilderness Camp Setup* (Look 07)

### Class 4: The Ritual (Sensory Climax & Human Contact)
* **Definition:** A moment of sensory or human contact. Capture the physical act of use—liquid pouring, cream spreading, lather foaming, tactile button turning, coffee dripping, foot striking gravel—when it answers the viewer's question or creates useful desire.
* **Primary Funnel Role:** Conversion triggers, paid social thumb-stoppers, PDP carousel slots 3 and 5.
* **Scale Archetype Examples:**
  * Scale 01: *Viscosity, Slump & Micro-Macro Texture Swatch* (Look 03), *Fingertip Touch & Application* (Look 05), *Direct-Flash Night-Out Editorial* (Look 08)
  * Scale 02: *Kinetic Pour & High-Speed Viscosity* (Look 03), *Direct-Flash Bodega Candid* (Look 06), *Viscosity Flow & Sensory Climax* (Look 12)
  * Scale 03: *Streetwear Candid Movement* (Look 02)
  * Scale 04: *Active Performance State* (Look 02), *Ergonomic Hand-in-Action Operation* (Look 05)
  * Scale 05: *(Sensory immersion captured through Archetype 02 and Archetype 13)*
  * Scale 06: *Kinetic Urban Commute (Panning Velocity)* (Look 02), *Battery Swap & Modular Charging* (Look 03), *Close-Tracking 45° Axle Velocity* (Look 13)

---

## Master Scale Navigator

| Scale File | Primary Categories & Products | Core Physical Dimensions | Primary Anxieties Solved | Archetype Count |
| :--- | :--- | :--- | :--- | :--- |
| **[`01-micro-intimate.md`](../01-micro-intimate.md)** | Skincare, serums, cosmetics, jewelry, fragrance, supplements, watches. | Under 6 inches (< 15 cm) | Viscosity texture, skin absorption, ingredient purity, micro-machining tolerances. | 15 Archetypes |
| **[`02-handheld-tabletop.md`](../02-handheld-tabletop.md)** | CPG, bottled beverages, packaged foods, coffee/tea, everyday carry, small tech. | 6 to 18 inches (15–45 cm) | Flavor craving, daily ritual fit, zero-leakage seal integrity, material patina. | 15 Archetypes |
| **[`03-body-worn-apparel.md`](../03-body-worn-apparel.md)** | Apparel, footwear, eyewear, bags, activewear, outerwear, accessories. | Worn on the human body | Sizing/layering fit, deluge waterproofing, stretch opacity, 5-year break-in. | 15 Archetypes |
| **[`04-countertop-appliances.md`](../04-countertop-appliances.md)**| Espresso machines, pizza ovens, power stations, blenders, heavy power tools. | 1.5 to 3 feet (45–90 cm) | Cabinet clearance, metal vs plastic internals, acoustic noise, cleaning ease. | 15 Archetypes |
| **[`05-architectural-macro.md`](../05-architectural-macro.md)** | Saunas, cold plunges, modular sectionals, home gyms, outdoor fire pits. | 3 to 10+ feet (1–3+ meters) | Spatial footprint, multi-user clearance, $5k+ justification, timber aging. | 15 Archetypes |
| **[`06-mobility-transport.md`](../06-mobility-transport.md)** | E-bikes, scooters, cargo rigs, overland rooftop tents, adventure trailers. | 4 to 12+ feet (Kinetic) | Incline hill torque, transit folding, monsoon water sealing, 10,000-mile proof. | 15 Archetypes |
| **[`DIALECTS.md`](../DIALECTS.md)** | 16 cross-cutting aesthetic modifiers for any archetype. | N/A | Aligns any scale archetype with specific brand identities (HexClad, Aesop, Arc'teryx, etc.). | 16 Dialects |

---

## Cognitive Framing: Awareness Stages & Temporal Horizons

### Eugene Schwartz's 5 Stages of Awareness
1. **Unaware:** Needs pattern-interrupting visual poetry, aspirational lifestyle (*The Habitat* or *The Ritual*).
2. **Problem Aware:** Needs ergonomic relief, comfort, and restorative sanctuary (*The Habitat* or *The Proof*).
3. **Solution Aware:** Needs visual proof of superior mechanism, pure ingredients, active engineering (*The Proof*).
4. **Product Aware:** Needs definitive de-risking imagery for fit, dimensions, cleaning, longevity (*The Proof* and *The Specimen*).
5. **Most Aware:** Needs bundle value, finish verification, pure clarity (*The Specimen*).

### Temporal Horizons: The Dimension of Time
* **Horizon 0 (Unboxing / Arrival):** Crisp tear-strips, pristine folds, letterpress tags (*Archetype 10 in Scales 02, 03; Archetype 09 in Scale 02; Archetype 15 in Scale 05*).
* **Horizon 1 (Active Daily Ritual):** Steam, pouring oil, kinetic commute, foaming lather (*Archetypes 02, 03, 05, 12 across scales*).
* **Horizon 2 (Maturity & Patina — 1 to 5 Years):** Rich vegetable-tanned leather burnishing, raw selvedge fades, seasoned copper/brass (*Archetype 11 across scales*).
* **Horizon 3 (Decadal Legacy — 10+ Years / 10,000 Miles):** Noble silvered cedar, commercial brass group heads, intact titanium frame welds (*Archetypes 10 & 11 in Scales 04, 05, 06*).

---

## Fast-Lookup Decision Matrices

### Matrix A: By Funnel Slot & Universal Class

| Funnel Slot / Channel Placement | Universal Class | Recommended Archetypes Across Scales |
| :--- | :--- | :--- |
| **Amazon / Google Shopping Slot 1** | **The Specimen** | **Archetype 01** in Scales 01–06 *(Compliant Hero Packshot / Profile)* |
| **Shopify / Hero Landing Page Header** | **The Habitat** | **Archetype 02/04/14** in Scale 01/02; **Archetype 15** in Scale 03; **Archetype 01/13** in Scale 04/05/06 |
| **Mobile PDP Slot 2: Mechanism & Proof** | **The Proof** | **Archetype 02/09/13** in Scale 01; **Archetype 03/08/13** in Scale 02; **Archetype 03/12/13** in Scale 03; **Archetype 12/14** in Scale 04; **Archetype 12/14** in Scale 06 |
| **Mobile PDP Slot 3: Sensory Climax / Ritual** | **The Ritual** | **Archetype 03/05/08** in Scale 01; **Archetype 04/12** in Scale 02; **Archetype 02/06** in Scale 03; **Archetype 02/05** in Scale 04; **Archetype 02/13** in Scale 06 |
| **Mobile PDP Slot 4: Scale, Fit & Dimensions** | **The Specimen** | **Archetype 07** in Scale 01; **Archetype 05** in Scale 02; **Archetype 07/12** in Scale 03; **Archetype 03/07** in Scale 04; **Archetype 03/06/10/12** in Scale 05; **Archetype 04/11/15** in Scale 06 |
| **Mobile PDP Slot 5: Durability & Torture Proof**| **The Proof** | **Archetype 11** in Scales 01–05; **Archetype 06/13** in Scale 03; **Archetype 11/12** in Scale 04; **Archetype 09/11** in Scale 05; **Archetype 09/10/12/14** in Scale 06 |
| **Mobile PDP Slot 6: Unboxing & Delivery** | **The Specimen** | **Archetype 10** in Scale 01/03/04; **Archetype 09** in Scale 02; **Archetype 15** in Scale 05 |
| **Paid Social Ads (Meta / TikTok)** | **The Ritual / The Proof** | **Archetype 08/13** in Scale 01; **Archetype 06/13** in Scale 02; **Archetype 05/13** in Scale 03; **Archetype 02/12** in Scale 04; **Archetype 02/12** in Scale 06 |

---

### Matrix B: By Primary Customer Anxiety to Dismantle

| Customer Doubt / Friction Point | Universal Class | The Exact Archetype to Deploy |
| :--- | :--- | :--- |
| **"I can't touch it — is the texture cheap, sticky, or synthetic?"** | **The Proof / Ritual** | *Viscosity Swatch* (`01`, Look 03) • *Dermal Absorption* (`01`, Look 13) • *Textile Macro* (`03`, Look 03) |
| **"Will this leak in my bag and ruin my laptop or clothes?"** | **The Proof** | *High-Stakes Inversion Test* (`02`, Look 13) — use a documented test for a factual seal claim, or a clearly illustrative contrast for concept work |
| **"Will this actually fit my body, countertop, room, or elevator?"** | **The Specimen / Proof** | *Dual-Model Fit* (`03`, Look 12) • *Under-Cabinet Anchor* (`04`, Look 03) • *Seated Clearance* (`05`, Look 03) • *Transit Fold* (`06`, Look 15) |
| **"Why does this cost $800–$10,000+? Is it built to last?"** | **The Proof** | *Engineering Teardown* (`04`, Look 12) • *10-Year Workhorse* (`04`, Look 11) • *Decadal Weathering* (`05`, Look 11) • *10,000-Mile Commuter* (`06`, Look 10) |
| **"Will the motor die or short-circuit in rain or mud?"** | **The Proof** | *Monsoon Immersion Test* (`06`, Look 14) • *Water & Mud Torture* (`06`, Look 09) |
| **"Will active skincare ingredients spoil before I finish the bottle?"** | **The Proof** | *Temporal Stability & Shelf-Life Proof* (`01`, Look 11) — show the supplied stability result or use a neutral concept frame |
| **"Will this leave an ashy white cast on my deep skin tone?"** | **The Proof** | *Multi-Tone Compatibility Matrix* (`01`, Look 12) — compare documented swatches or label the render as a concept |
| **"Will this climb my steep hill without me sweating or stalling?"** | **The Proof** | *30% Incline Hill-Climb Torque Proof* (`06`, Look 12) — use the actual grade, rider, conditions, and test data |
| **"How hard is this to clean, disassemble, or maintain?"** | **The Proof** | *Easy-Clean Disassembly* (`04`, Look 06) • *Utility & Drainage Access* (`05`, Look 07) |

---


