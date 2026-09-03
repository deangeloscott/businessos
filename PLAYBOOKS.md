# What AURA Can Do

AURA gives capable AI reusable **Playbooks** and **Workflows** while leaving reasoning, tool choice, orchestration, and execution to the active model/harness. Tell the AI what outcome you want in normal language; you do not need to choose a Playbook or Workflow manually.

This edition currently exposes **42 Playbooks** backed by **472 detailed Workflows**. Playbook count is intentionally much smaller than Workflow count because a Playbook is an end-to-end business job, not every reusable procedure.

## The hierarchy

**Playbook → Workflow → Step**

- **Playbook** — a meaningful end-to-end business job that bundles relevant operating knowledge.
- **Workflow** — a reusable procedure that helps accomplish part of a Playbook and may also be useful independently.
- **Step** — the minimum guidance needed inside a Workflow to make the intended result reliably achievable.

A Playbook is not an execution graph. The model chooses which Workflows matter, how to sequence or parallelize them, which host tools or external Skills to use, and whether another sound method is better.

## Business areas

### [Competitive Intelligence](docs/playbooks/competitor-intelligence.md)

Understand competitors, substitutes, competitive movement, and supported implications.

**2 Playbooks** in this area.

- **Competitor Research** — Identify the competitors and substitutes that matter, understand what they are doing, compare the business against them, and derive supported implications.
- **Competitor Monitoring** — Keep important competitive movement current and distinguish observed changes from unsupported assumptions about effectiveness or intent.

### [Customer Intelligence](docs/playbooks/customer-intelligence.md)

Understand customers, prospects, needs, language, decisions, and experiences from appropriate evidence.

**2 Playbooks** in this area.

- **Customer Research** — Resolve an important customer knowledge need with evidence appropriate to the decision, using the relevant research and analysis Workflows.
- **Voice of Customer** — Build reusable evidence-backed understanding of the language, pains, desires, objections, outcomes, and decision criteria customers actually express.

### [Industry Intelligence](docs/playbooks/industry-intelligence.md)

Understand material external developments in the market, regulation, research, technology, and industry.

**2 Playbooks** in this area.

- **Industry Intelligence** — Discover and evaluate material news, research, regulation, technology, market shifts, and other external changes that could affect the organization.
- **Industry Rapid Response** — Build a fast, evidence-backed understanding of a time-sensitive external development and its plausible business implications.

### [SEO/AEO](docs/playbooks/seo-aeo.md)

Improve valuable organic discovery across search, answer engines, AI interfaces, local discovery, and related surfaces.

**3 Playbooks** in this area.

- **SEO/AEO Growth** — Find and improve the highest-value realistic opportunities for organic discovery across search engines, answer engines, AI interfaces, and local discovery.
- **SEO/AEO Experimentation and Learning** — Test uncertain SEO/AEO tactics when testing is worthwhile, evaluate results without overstating causality, and preserve reusable Learning when supported.
- **SEO/AEO Site Migration** — Plan and execute a domain, CMS, architecture, or URL migration while protecting organic discovery, attribution, and recoverability.

### [Content Synthesis](docs/playbooks/content-synthesis.md)

Turn useful ideas, evidence, and source material into strong audience-appropriate content.

**16 Playbooks** in this area.

- **Content Strategy and Synthesis** — Turn audience context, evidence, ideas, performance signals, and communication goals into a strong content approach before or across specific formats.
- **Animation / Motion Production** — Use motion to explain change, sequence, causality, demonstration, or attention hierarchy.
- **Article Production** — Produce a useful, evidence-backed article with appropriate depth, structure, and reader progression.
- **Audio Asset Production** — Produce voiceover, narration, clip, or other audio asset optimized for its actual use context.
- **Carousel / Slideshow Production** — Turn an idea into a sequential visual argument where each frame earns the next.
- **Customer Case Study** — Turn verified customer evidence and ProofRecords into a useful, accurate account of context, intervention, mechanism, and outcome.
- **Demonstration Asset Production** — Produce a clear, verifiable demonstration that visibly proves or teaches the intended mechanism, use case, or result.
- **FAQ Content Production** — Create evidence-backed answers to recurring audience questions in a form that is easy to find and understand.
- **Image / Graphic Production** — Create a visual asset whose composition communicates the intended idea rather than adding decoration.
- **Infographic Production** — Turn evidence or a structured idea into a clear visual explanation whose information hierarchy works even when the viewer only scans it.
- **Long-Form Video Production** — Create sustained video communication with narrative or educational progression, demonstrations, and retention-aware structure.
- **Newsletter Production** — Create a relationship-oriented email or newsletter suited to inbox context and the audience expectation.
- **Podcast Episode Production** — Create an audio-first episode whose structure and delivery fit listening context.
- **Presentation / Slideshow Production** — Build a presentation that supports a live or asynchronous audience journey instead of turning a document into slides.
- **Short-Form Video Production** — Express one useful idea quickly through platform-native visual and audio pacing and proof.
- **Content Repurposing & Adaptation** — Turn a validated core asset or idea into the smallest useful set of derivative and platform-native assets without unnecessary variants or distorted meaning.

### [Marketing Synthesis](docs/playbooks/marketing-synthesis.md)

Create and improve persuasive strategy, campaigns, offers, and customer-facing marketing assets.

**15 Playbooks** in this area.

- **Marketing Strategy and Messaging** — Develop or improve positioning, messaging, value proposition, mechanism, proof, objection handling, and offer presentation around current customer and business truth.
- **Campaign Development** — Build a coherent campaign concept and the useful persuasive work needed to carry it across the relevant customer-facing surfaces.
- **Offer Design & Optimization** — Diagnose and improve how value is packaged, priced, de-risked, and presented so the offer is more compelling without inventing unsupported value or urgency.
- **Advertising Creative & Copy** — Create persuasive ad concepts, copy, and creative requirements matched to audience, awareness, journey role, placement context, evidence, and destination.
- **Advertorial** — Create clearly compliant editorial-style persuasion that educates while transparently serving a commercial objective.
- **Commercial Email Sequence** — Design a multi-email persuasion sequence where each message has a distinct job and builds appropriately on prior context.
- **Comparison & Alternative Persuasion** — Help qualified buyers evaluate alternatives honestly using customer decision criteria and current competitive evidence.
- **Landing Page Persuasion** — Create a landing page or homepage that continues acquisition intent and moves the right visitor toward the desired action without overstating business truth.
- **Lead Magnet** — Create an exchange-worthy asset that solves a bounded valuable problem and naturally relates to the next commercial step.
- **Lead Nurture Strategy** — Move not-yet-ready prospects toward a better-informed decision over time rather than repeatedly asking for the sale.
- **Quiz / Assessment Conversion Asset** — Create a diagnostic experience that gives the participant useful feedback while qualifying or segmenting toward a relevant next action.
- **Sales Enablement Asset** — Create persuasive evidence and tools that help sellers and buyers resolve real decision questions consistently.
- **Sales Letter** — Create long-form written persuasion appropriate to audience sophistication and offer complexity.
- **Video Sales Letter** — Build a sustained video persuasion narrative tied to an Offer and measurable commercial action.
- **Webinar Persuasion** — Design a webinar that creates genuine understanding and value while logically leading qualified attendees to an Offer.

### [Customer Optimization](docs/playbooks/customer-optimization.md)

Improve the customer journey from qualification and purchase through value, retention, expansion, recovery, and referral.

**2 Playbooks** in this area.

- **Customer Journey Optimization** — Understand the journey, identify the most important progression problem, diagnose the likely cause, improve it, and evaluate what changed.
- **Retention and Churn** — Understand why customers leave or fail to realize value, improve the relevant experience, and evaluate durable retention rather than manipulating short-term staying behavior.

## AURA Core

AURA Core supplies shared organizational memory, truth/evidence handling, decisions, continuity, measurement, Learning, and workspace integrity. It is support for the business work rather than another business Playbook. See [AURA Core Workflows](docs/playbooks/core.md).

## For advanced users

- `TASK-NAVIGATOR.md` shows the installed Playbooks and common Workflow entry points.
- `WORKFLOW-INDEX.md` lists all detailed Workflow IDs.
- Each Workflow `CONTEXT.md` contains its outcome, when-to-use guidance, steps, evidence needs, and quality requirements.
- `docs/operating-knowledge.md` explains the minimum-sufficient-guidance philosophy.
