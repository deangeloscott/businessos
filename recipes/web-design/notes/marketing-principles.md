# Web Marketing Principles & Section Patterns

> Optional web craft notes. Open this only when it materially helps the selected track or page; the track files and dialect file remain usable without loading the notes.
>
> Preserves the behavioral frameworks, section archetypes, and compact web brief for adaptable marketing decisions.

## How This Library Works

This library is a set of **optional, platform-agnostic craft references** for designing, structuring, writing, and engineering high-converting digital web properties. It provides a shared vocabulary across **four specialized architectural tracks**, **ten design dialects**, reusable section patterns, and a **7-block briefing pattern**.

In modern digital business, web design cannot be treated as decorative canvas art or as crude, dated direct-response hype. A strong standard is **Conversion-First Kinetic Architecture**: a unified discipline where cognitive psychology, direct-response copywriting, visual ergonomics, measurable web performance, and machine-readable content support one another.

An operator or AI model may use:
1. **A Domain Track File** (`01` through `04`) matching the commercial objective (E-Commerce, Lead Generation, Brand Website, or Multi-Step Funnel).
2. **A Section Archetype Flow** that answers the visitor's actual decision questions.
3. **A Design Dialect** from `DIALECTS.md` when a consistent visual system helps.
4. **The 7-Block Web Brief** when a compact prompt or audit frame improves clarity.

Use the fewest references that improve the requested outcome. Existing AURA Workflows own organizational truth, evidence, claim quality, and workflow-level QA; this library supplies optional craft knowledge and never requires a fixed route or prompt syntax.

```
┌─────────────────────────┐     ┌─────────────────────────┐     ┌─────────────────────────┐
│     1. DOMAIN TRACK     │  +  │  2. SECTION ARCHETYPES   │  +  │    3. DESIGN DIALECT    │
│  (01-ecomm, 02-leadgen, │     │ (Hero, Agitation, Proof,│     │   (From DIALECTS.md:    │
│   03-brand, 04-funnels) │     │  Showcase, Buy Box, etc)│     │    Precision Slate, etc)│
└─────────────────────────┘     └─────────────────────────┘     └─────────────────────────┘
                                             │
                                             ▼
                        [OPTIONAL 7-BLOCK WEB BRIEF]
                                             │
                                             ▼
                 [WEB EXPERIENCE FITTED TO THE REAL CONTEXT]
                 • Measured performance targets chosen for the page and audience
                 • Semantic, accessible content where discoverability matters
                 • Calibrated friction and evidence-backed persuasion
```

---

## Seven Behavioral Frameworks for Web Conversion & Usability

Generative AI models and human designers often fail in web production for predictable reasons: prioritizing aesthetic trends over visual contrast, creating cognitive overload, failing to provide continuation cues, and treating all traffic as having identical awareness. The following seven frameworks are useful starting points. Apply them when they fit the audience, evidence, platform, and commercial objective; adapt or omit them when they do not.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│          SEVEN WEB CONVERSION & USABILITY FRAMEWORKS                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. THE FRICTION VALVE                   (Calibrate Friction to Stakes)      │
│ 2. THE FIRST-SCREEN POSITIONING FILTER  (Category, Audience, Outcome)       │
│ 3. THE CONTINUATION CUE                 (Avoiding a False Bottom)           │
│ 4. BALANCED CREDIBILITY SIGNALS         (Contextual Social Proof)            │
│ 5. LAYER-CAKE SCANNING                  (Subheadings Carry the Argument)    │
│ 6. DUAL-CONSUMER CLARITY                (Humans + Machines)                 │
│ 7. VISUAL CONTRAST & ACCENT ISOLATION   (A 60-30-10 Starting Point)         │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Framework 1: The Friction Valve (Calibrate Friction to Stakes)
* **The Principle:** Friction is not universally bad; it is an economic valve. Removing every qualification step from a high-ticket B2B or complex service can increase unqualified demand and strain fulfillment. Adding unnecessary friction to an impulse consumer purchase can reduce completion. Calibrate the exchange to the decision, audience, and delivery capacity.
* **The Practice:**
  * *Low-stakes entry:* Reduce avoidable effort and ask only for information needed to deliver the promised value.
  * *High-stakes or capacity-limited decision:* Add only the qualification questions that improve fit, readiness, economics, or service quality. Thoughtful qualification can signal competence; irrelevant questions simply lose good prospects.

### Framework 2: The First-Screen Positioning Filter (Category, Audience, Outcome)
* **The Principle:** A first-time visitor should quickly understand what the offer is, who it serves, and why it may matter. The exact time depends on traffic, device, and page complexity.
* **The Practice:** The primary above-the-fold hero section should communicate:
  1. *What is this product/service?* (The Market Category).
  2. *Who is it specifically for?* (The Target Audience).
  3. *What transformation or measurable outcome does it produce?* (The Core Promise).
  * *Banned Anti-Pattern:* Vague poetic aspirations (*"Empowering seamless global workflow synergy"*).

### Framework 3: Continuation Cues (Avoiding a False Bottom)
* **The Principle:** A full-bleed hero can look complete and hide the next decision. Test whether the layout makes continuation obvious for the actual device and audience.
* **The Practice:** Where further information is important, let the next section, a directional cue, or a clear navigation affordance signal that useful content continues. A full viewport hero can still be right when the context calls for it.

### Framework 4: Balanced Credibility Signals (The Review Context)
* **The Principle:** Some review datasets report stronger purchase confidence in a credible mid-to-high rating range than at a perfect score, but the relationship varies by category, sample, and source. A rating is not a universal conversion target.
* **The Practice:** Preserve authentic review distributions, useful negative feedback, dates, sample size, and context. Never manufacture criticism or suppress material defects to create an artificial credibility signal.

### Framework 5: Layer-Cake Scanning (Subheadings Carry the Argument)
* **The Principle:** Users do not read web pages word-for-word; they scan in layer-cake and F-shaped patterns.
* **The Practice:** A visitor who scans the H1, H2s, H3s, and bold bullet lead-ins should be able to reconstruct the main value proposition, mechanism, proof, and next step. Body copy supplies the detail needed for verification and fit.

### Framework 6: Dual-Consumer Clarity (Humans + Machines)
* **The Principle:** Web properties are consumed by biological humans operating touchscreens and autonomous AI agents/crawlers (ChatGPT Search, Perplexity, Gemini, Claude, procurement bots) parsing semantic text.
* **The Practice:** Render core text, pricing, and meaningful navigation in accessible semantic HTML whenever practical. Add structured data, a sitemap, and other machine-readable references when they accurately describe the page and the target systems use them. A proposed file such as `/llms.txt` can assist some consumers, but it does not ensure crawling, citation, or recommendation.

### Framework 7: Visual Contrast and Accent Isolation (A 60-30-10 Starting Point)
* **The Principle:** When every visual element is saturated, nothing commands attention. The eye requires vast neutral ground to identify the singular point of action (The Von Restorff Isolation Effect).
* **The Starting Point:**
  * **60% Dominant Base:** Clean canvas background (neutral light or deep slate) providing whitespace.
  * **30% Structural Secondary:** Typographic hierarchy, container cards, subtle borders, and navigation.
  * **10% High-Energy Conversion Accent:** Often reserved for primary actions so they are easy to find; adapt the ratio and accent use to brand, accessibility, hierarchy, and interaction evidence.

---

## Eight Reusable Web Section Archetypes

Many high-performing pages use some of these section archetypes, but no page needs all eight. Select the sections that answer the visitor's actual decision questions:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 EIGHT REUSABLE WEB SECTION ARCHETYPES                       │
├──────────────────────┬──────────────────────┬───────────────────────────────┤
│ ARCHETYPE            │ COMMERCIAL ROLE      │ CORE COGNITIVE OBJECTIVE      │
├──────────────────────┼──────────────────────┼───────────────────────────────┤
│ 1. THE CONTEXT HERO  │ Orientation & Hook   │ The 5-second filter; clarity  │
│ 2. THE TRUST STRIP   │ Pre-Emptive Credibility│ Authority by association    │
│ 3. THE MECHANISM SPLIT│ Agitation & Solution│ Status quo vs. new vehicle    │
│ 4. THE PROVING GROUND│ Empirical Validation │ Demonstrations & torture tests│
│ 5. THE SOCIAL VAULT  │ Distributed Evidence │ Reviews, metrics, case studies│
│ 6. THE INTERACTIVE DOCK│ Engagement & Fit   │ Buy box, calculator, or quiz  │
│ 7. THE HESITATION SHIELD│ Objection Removal │ Accordion FAQs & guarantees   │
│ 8. THE TERMINAL ANCHOR│ Final Commitment    │ Frictionless closing on-ramp  │
└──────────────────────┴──────────────────────┴───────────────────────────────┘
```

### Archetype 1: The Context Hero
* **Function:** Stops the scroll, hooks attention, and establishes market context.
* **Components:** Category kicker label (uppercase, 12px), primary outcome H1 (40–64px), clarifying mechanism H2 (18–22px), high-contrast primary CTA, secondary exploratory micro-link, and an authentic product simulation or hero visual.

### Archetype 2: The Trust Strip
* **Function:** Defuses early cynicism immediately below the hero fold.
* **Components:** Monochromatic SVG client/press marquees (uniform visual weight), current accreditations that the organization actually holds, or supported customer/usage metrics (*"Over 40,000+ teams onboarded"* only when verified).

### Archetype 3: The Mechanism Split (Old Way vs. New Way)
* **Function:** Dismantles false vehicle beliefs and proves why existing alternative solutions fail.
* **Components:** A two-column contrast grid: Left column highlights the painful, fragmented, manual "Old Way"; right column highlights the automated, unified, superior "New Way."

### Archetype 4: The Proving Ground (Empirical Demonstrations)
* **Function:** Makes the mechanism easier to believe through relevant evidence or a clearly labeled demonstration.
* **Components:** Documented test clips, teardowns, interactive ROI calculators, side-by-side split screens, or clinical-trial metric graphs when the underlying method, sample, and scope are available.

### Archetype 5: The Social Vault (Distributed Proof)
* **Function:** Validates the experience of real peers across different use cases.
* **Components:** Clickable star rating distribution bars, searchable review feeds, video testimonial reels with transcripts, and named B2B case studies highlighting quantified before/after deltas.

### Archetype 6: The Interactive Dock (The Transaction Surface)
* **Function:** The primary surface where value is selected or customized.
* **Components:** The E-Commerce Buy Box with pill variant selectors; the Lead-Gen Multi-Step Form; the Interactive Quiz Card; or the Pricing Matrix with a prominent "Recommended" tier.

### Archetype 7: The Hesitation Shield (Risk Reversal & FAQs)
* **Function:** Systematically answers the top five unresolved objections before purchase.
* **Components:** High-legibility accordion cards answering the hardest questions directly, paired with a guarantee or risk-reversal term that the business actually offers and can honor.

### Archetype 8: The Terminal Anchor (The Closing Call-to-Action)
* **Function:** Captures visitors who have scrolled to the bottom of the page in analytical verification mode.
* **Components:** High-contrast background container, condensed restatement of the primary promise, a prominent CTA button, and reassurance text (*"No credit card required"*, *"Cancel anytime"*).

---

## The 7-Block Web Brief

To generate or audit a web page, an operator or AI model can use the **7-Block Web Brief** as a compact thinking frame. It is a prompt aid, not a required syntax or execution protocol:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         THE 7-BLOCK WEB BRIEF                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ BLOCK 1: TRAFFIC TEMPERATURE & AWARENESS STATE                              │
│ • Awareness Level: Unaware | Problem-Aware | Solution-Aware | Product-Aware │
│ • Traffic Source: Cold Social (Meta/TikTok) | High-Intent Search | Retarget │
├─────────────────────────────────────────────────────────────────────────────┤
│ BLOCK 2: COMMERCIAL ECONOMICS & VALUE EQUATION                              │
│ • Economic Goal: Zero-CAC SLO | Impulse E-Comm | High-Ticket Booking | MRR  │
│ • Hormozi Value Equation Drivers: Dream Outcome, Proof, Speed, Zero Friction│
├─────────────────────────────────────────────────────────────────────────────┤
│ BLOCK 3: INFORMATION ARCHITECTURE & SECTION FLOW                            │
│ • Candidate section sequence (e.g., 1 ──► 2 ──► 3 ──► 4 ──► 6), adapted to     │
│   the visitor's questions and the real journey                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ BLOCK 4: PERSUASION, COPYWRITING & HEADLINE CADENCE                         │
│ • H1 / H2 Formulas: Outcome + Timeframe without the Hated Obstacle          │
│ • Layer-Cake Scanning Structure: Descriptive H2/H3 subheadings              │
├─────────────────────────────────────────────────────────────────────────────┤
│ BLOCK 5: VISUAL DIALECT & DESIGN TOKENS                                     │
│ • Dialect Selected from DIALECTS.md (e.g., High-Tech Precision Slate)       │
│ • 60-30-10 Color Architecture: Explicit Canvas, Structural, and Accent hex  │
├─────────────────────────────────────────────────────────────────────────────┤
│ BLOCK 6: USABILITY, ERGONOMICS & COGNITIVE EASE                             │
│ • Mobile Thumb Zone: Pinned sticky dock with 48x48px min touch targets      │
│ • Flesch-Kincaid Grade 6–8 readability; 60–75 Characters Per Line (CPL)     │
├─────────────────────────────────────────────────────────────────────────────┤
│ BLOCK 7: TECHNICAL PERFORMANCE & MACHINE READABILITY                        │
│ • Current Core Web Vitals targets and budgets chosen from a real baseline    │
│ • Eligible speculation, semantic HTML, structured data, and accessible copy │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

