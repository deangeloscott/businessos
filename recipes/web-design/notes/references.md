# Web Directory, Workflow Links & Foundational References

> Optional web craft notes. Open this only when it materially helps the selected track or page; the track files and dialect file remain usable without loading the notes.
>
> Preserves the original directory and source map, with direct links to existing AURA workflows that can supply organizational context and QA.

## Existing AURA workflows to pair when useful

These recipes are optional starting points. Follow a link only when the job needs that deeper operating context:

- [Positioning](../../../systems/marketing-synthesis/workflows/strategy/positioning/CONTEXT.md) and [core message](../../../systems/content-synthesis/workflows/strategy/core-message/CONTEXT.md) for category, audience, and outcome decisions.
- [Landing-page copy](../../../systems/marketing-synthesis/workflows/landing-page/copy/CONTEXT.md) and [ad copy](../../../systems/marketing-synthesis/workflows/ads/copy/CONTEXT.md) for channel-specific messaging.
- [Voice-of-customer analysis](../../../systems/customer-intelligence/workflows/analysis/voice-of-customer/CONTEXT.md) and [objection analysis](../../../systems/customer-intelligence/workflows/analysis/objections/CONTEXT.md) when customer language or hesitation is unknown.
- [Fact-check QA](../../../systems/content-synthesis/workflows/qa/fact-check/CONTEXT.md), [accessibility QA](../../../systems/content-synthesis/workflows/qa/accessibility/CONTEXT.md), and [pre-publish QA](../../../systems/content-synthesis/workflows/qa/pre-publish/CONTEXT.md) before a customer-facing page is shipped.
- [Experiment design](../../../core/workflows/measurement/design-experiment/CONTEXT.md) and [friction diagnosis](../../../systems/customer-optimization/workflows/diagnosis/friction/CONTEXT.md) when a page or funnel will be measured or debugged.

## Directory Map: How to Navigate This Library

When executing specific business objectives, proceed to the corresponding domain file:

* **[DIALECTS.md](../DIALECTS.md):** Ten Web UI/UX Design Dialects (color palettes, font pairings, border radii, surface depth, and animation tokens).
* **[01-ecommerce-stores.md](../01-ecommerce-stores.md):** E-Commerce (faceted PLP, modular PDP, sticky buy box, cart drawer, and checkout patterns).
* **[02-lead-generation.md](../02-lead-generation.md):** Lead Generation (lead magnets, qualification friction, quiz funnels, applications, and calendar booking).
* **[03-brand-business-websites.md](../03-brand-business-websites.md):** Brand Authority (positioning, persona-based information architecture, product demonstration, and proof placement).
* **[04-multistep-sales-funnels.md](../04-multistep-sales-funnels.md):** Direct-Response Funnels (advertorials, book funnels, challenges, webinars, VSLs, community, and upsells).

---

## Foundational References, Theoretical Attribution & Source Directory

The following directory records useful research, standards, and practitioner frameworks behind the library. It is a reading map, not proof that every number or tactic applies universally. Verify current primary sources, scope, and assumptions before turning a reference into customer-facing copy or an implementation target:

### 1. Empirical Usability & Conversion Research Institutes
* **Baymard Institute (Copenhagen & Global):**
  * *Primary Contribution:* Large-scale empirical e-commerce usability testing.
  * *Key Findings Used:* Cart-abandonment context, checkout and product-page failure modes, selector usability, and the value of reducing unnecessary form work. Treat published rates and recovery estimates as study-specific baselines, not promises.
  * *Source & Reference:* Baymard Institute E-Commerce Usability Reports & PDP/Checkout Benchmark Studies.
* **Nielsen Norman Group (NN/g — Jakob Nielsen, Don Norman, Bruce Tognazzini):**
  * *Primary Contribution:* Human-computer interaction (HCI), ocular tracking research, and cognitive ergonomics.
  * *Key Findings Used:* Bruce Tognazzini's *False Bottom (Illusion of Completeness)* phenomenon; F-shaped and Layer-Cake scanning patterns; plain language readability standards.
  * *Seminal Works:* *Prioritizing Web Usability* (Nielsen & Loranger); NN/g Research Articles on Scanning & Scrolling Behavior.
* **Medill Spiegel Research Center (Northwestern University):**
  * *Primary Contribution:* Quantitative research on consumer reviews and purchase probability.
  * *Key Findings Used:* Review credibility, rating context, and the role of negative reviews. The reported ranges depend on study design and category; do not optimize every business toward a universal star-rating target.
  * *Seminal Study:* *"How Online Reviews Influence Sales"* (Spiegel Research Center).
* **CXL Institute & Speero (Peep Laja):**
  * *Primary Contribution:* Conversion research, experimentation, and form/interaction analysis.
  * *Key Findings Used:* Nonlinear form-friction patterns, inline validation, and intent-based form-length calibration. Use an organization's baseline and experiment results for local decisions.
* **Steven Hoober (4ourth Mobile):**
  * *Primary Contribution:* Observational research on mobile device touch mechanics (1,333+ participant field studies).
  * *Key Findings Used:* Mobile reachability and thumb-zone patterns that can inform placement. Validate the layout on the actual device mix instead of treating a single study percentage as a universal rule.

### 2. Cognitive Psychology & Behavioral Economics
* **Daniel Kahneman & Amos Tversky:**
  * *Primary Contribution:* Behavioral economics, cognitive heuristics, and dual-process cognition.
  * *Key Findings Used:* Dual-process decision models and Prospect Theory's loss-aversion framing. Use loss framing to clarify real costs of inaction, not to invent them.
  * *Seminal Work:* *Thinking, Fast and Slow* (Kahneman, 2011).
* **Robert B. Cialdini, Ph.D.:**
  * *Primary Contribution:* Widely used principles of influence.
  * *Key Findings Used:* Reciprocity (free value first), Commitment & Consistency (quiz micro-steps), Social Proof, Authority, Liking, Scarcity (authentic inventory constraints), and Unity.
  * *Seminal Work:* *Influence: The Psychology of Persuasion* (1984, expanded 2021).
* **Classical Ergonomic & Interaction Laws:**
  * *Hick's Law (William Edmund Hick):* Decision time generally increases with the number and complexity of choices; use it to simplify navigation when the task benefits, not as a fixed item cap.
  * *Fitts's Law (Paul Fitts):* Movement time depends on target distance and width; use it alongside accessibility guidance and device testing when sizing controls.
  * *Working-memory research:* Chunk related information and use clear hierarchy; avoid treating a single capacity estimate as a universal content limit.
  * *The Von Restorff Effect (Hedwig von Restorff):* Distinctive elements attract attention; use contrast intentionally and preserve accessibility rather than reserving a color by rote.

### 3. Direct-Response Architecture, Copywriting & Funnel Systems
* **Eugene Schwartz:**
  * *Primary Contribution:* The definitive foundations of market-aware copywriting.
  * *Key Frameworks Used:* The 5 Stages of Prospect Awareness (Unaware $\to$ Most Aware); The 5 Stages of Market Sophistication (Virgin Claim $\to$ Elaborated Mechanism $\to$ Identity).
  * *Seminal Work:* *Breakthrough Advertising* (1966).
* **Alex Hormozi (Acquisition.com):**
  * *Primary Contribution:* Modern offer architecture, value engineering, and high-velocity acquisition.
  * *Key Frameworks Used:* The Value Equation ($(\text{Outcome} \times \text{Likelihood}) / (\text{Delay} \times \text{Effort})$); Grand Slam Offers; Acute-Problem Lead Magnets; "Give away secrets, sell implementation."
  * *Seminal Works:* *$100M Offers* (2021), *$100M Leads* (2023).
* **Russell Brunson (ClickFunnels):**
  * *Primary Contribution:* Modern digital direct-response sales funnel frameworks.
  * *Key Frameworks Used:* The Value Ladder; The Perfect Webinar (The Big Domino, Epiphany Bridge, 3 False Beliefs); Hook-Story-Offer; Free + Shipping Book Funnels; In-Line Order Bumps ($17–$37) and 1-Click Upsell sequences.
  * *Seminal Works:* *DotCom Secrets* (2015), *Expert Secrets* (2017), *Traffic Secrets* (2020).
* **Jason Fladlien (Rapid Crush):**
  * *Primary Contribution:* One-to-many live sales choreography, webinar sales methodology, and affiliate bridge bonus architecture.
  * *Key Frameworks Used:* The "Two Paths" Seamless Pitch Transition; The "Solving Problems Created by the Solution" Bonus Framework; The 5 Master Closes (If All This Did, Money as Stored Energy, Divided by 365, Us vs. Them, Future Pace); The Affiliate Bridge Funnel & Exclusive Differentiating Bonus Stack.
  * *Seminal Work:* *One to Many: The Secret to Webinar Success* (2018).
* **April Dunford (Ambient Strategy):**
  * *Primary Contribution:* Enterprise positioning and market category context.
  * *Key Frameworks Used:* The 5-Second Positioning Filter (Category, Audience, Outcome); elimination of aspirational corporate jargon.
  * *Seminal Work:* *Obviously Awesome: How to Nail Product Positioning so Customers Get It, Buy It, Love It* (2019).
* **Dan Henry (GetClients.com):**
  * *Primary Contribution:* High-ticket consulting and application sales funnels.
  * *Key Frameworks Used:* VSL-to-Application call funnels; the 12-phase consultative sales script; direct-to-high-ticket validation before building low-ticket funnels.
  * *Seminal Work:* *Digital Millionaire Secrets* (2018).
* **Ryan Levesque (The ASK Method Company):**
  * *Primary Contribution:* Zero-party data collection and interactive diagnostic funnels.
  * *Key Frameworks Used:* The Ask Method; 4-stage quiz funnels; micro-commitments; dynamic bucket segmentation.
  * *Seminal Work:* *Ask: The Counterintuitive Online Method to Discover Exactly What Your Customers Want to Buy* (2015).
* **Pedro Adao:**
  * *Primary Contribution:* The 5-Day Challenge Funnel model.
  * *Key Frameworks Used:* Free admission + VIP double-dip upgrades ($97–$197); daily micro-commitments; graduation day stack pitches.
* **Sam Ovens (Skool / Consulting.com):**
  * *Primary Contribution:* Community-driven customer acquisition and continuity.
  * *Key Frameworks Used:* Free community as the master lead magnet; Level 1–9 gamified leaderboard course unlocking; peer-proof organic ascension to paid masterminds.
* **Alex Becker (Hyros):**
  * *Primary Contribution:* Multi-touch server-side ad attribution and long-tail customer lifetime value.
  * *Key Frameworks Used:* The 90-Day to 2-Year LTV cash payback horizon; unlisted high-density YouTube VSLs; multi-layered objection retargeting.
* **Daniel Fazio ("Cold Email Wizard" / Client Ascension):**
  * *Primary Contribution:* Lean B2B customer acquisition and outbound infrastructure.
  * *Key Frameworks Used:* Google Doc/Notion/Loom minimalist VSL funnels; AI-assisted agency fulfillment; organic-to-community acquisition.
* **Ravi Abuvala (Scaling With Systems):**
  * *Primary Contribution:* Sales floor operational division of labor.
  * *Key Frameworks Used:* The Setter-Closer framework (15-min triage call $\to$ 45-min closing strategy session); the Critical Constraint™ diagnostic.
* **Joshua Gavin (Josh Gavin):**
  * *Primary Contribution:* Backend-first offer publishing and self-liquidating digital offer funnels.

### 4. Technical Performance & Autonomous AI Agent Standards
* **W3C & Google Chrome Platform Team:**
  * *Primary Contribution:* Web platform standards and user-experience measurement.
  * *Key Standards Used:* Current Core Web Vitals guidance, semantic HTML, and the Speculation Rules API for eligible predictive prefetch/prerender. Use current official thresholds and measure deployed behavior; no API guarantees 0ms navigation.
* **Jeremy Howard (Answer.AI / Fast.ai):**
  * *Primary Contribution:* A proposed convention for machine-readable web curation.
  * *Key Standards Used:* The `/llms.txt` and `/llms-full.txt` proposal. Treat adoption and retrieval benefits as conditional on the consuming system.
* **Schema.org Consortium (W3C, Google, Microsoft, Yahoo):**
  * *Primary Contribution:* Structured semantic data vocabularies.
  * *Key Standards Used:* The JSON-LD `@graph` architecture (`Organization`, `Product`, `Offer`, `AggregateRating`, `Service`, `FAQPage`) for Generative Engine Optimization (GEO).


