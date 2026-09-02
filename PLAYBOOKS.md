# What AURA Can Do

AURA gives capable AI reusable **Playbooks** and **Workflows** while leaving reasoning, tool choice, orchestration, and execution to the active model/harness. Tell the AI what outcome you want in normal language; you do not need to choose a Playbook or Workflow manually.

This edition currently exposes **47 Playbooks** backed by **472 detailed Workflows**. Playbook count is intentionally much smaller than Workflow count because a Playbook is an end-to-end business job, not every reusable procedure.

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

- **Customer Research** — Resolve an important customer knowledge need with evidence appropriate to the decision, using the relevant research and analysis workflows.
- **Voice of Customer** — Build reusable evidence-backed understanding of the language, pains, desires, objections, outcomes, and decision criteria customers actually express.

### [Industry Intelligence](docs/playbooks/industry-intelligence.md)

Understand material external developments in the market, regulation, research, technology, and industry.

**2 Playbooks** in this area.

- **Industry Intelligence** — Discover and evaluate material news, research, regulation, technology, market shifts, and other external changes that could affect the organization.
- **Industry Rapid Response** — Build a fast, evidence-backed understanding of a time-sensitive external development and its plausible business implications.

### [SEO/AEO](docs/playbooks/seo-aeo.md)

Improve valuable organic discovery across search, answer engines, AI interfaces, local discovery, and related surfaces.

**2 Playbooks** in this area.

- **SEO/AEO Growth** — Find and improve the highest-value realistic opportunities for organic discovery across search engines, answer engines, AI interfaces, and local discovery.
- **SEO/AEO Experimentation and Learning** — Test uncertain SEO/AEO tactics when testing is worthwhile, evaluate the results without overstating causality, and preserve reusable Learning when supported.

### [Content Synthesis](docs/playbooks/content-synthesis.md)

Turn useful ideas, evidence, and source material into strong audience-appropriate content.

**23 Playbooks** in this area.

- **Content Strategy and Synthesis** — Turn audience context, evidence, ideas, performance signals, and communication goals into a strong content approach before or across specific formats.
- **AI Avatar Video Production** — Produce an approved avatar-presented video when synthetic presentation is appropriate, transparent, and efficient for the communication job.
- **Animation / Motion Production** — Use motion to explain change, sequence, causality, demonstration, or attention hierarchy.
- **Article Production** — Produce a useful, evidence-backed article with appropriate depth, structure, and reader progression.
- **Audio Asset Production** — Produce voiceover, narration, clip, or other audio asset optimized for its actual use context.
- **Captions and On-Screen Text** — Design captions/on-screen text that improve comprehension and accessibility without overwhelming the visual.
- **Carousel / Slideshow Production** — Turn an idea into a sequential visual argument where each frame earns the next.
- **Content Thumbnail Concept** — Design a thumbnail/cover image that quickly communicates the content’s real subject, tension, or outcome at browsing scale.
- **Customer Case Study** — Turn verified customer evidence and ProofRecords into a useful, accurate account of context, intervention, mechanism, and outcome.
- **Demonstration Asset Production** — Execute an approved demonstration plan and produce a clear, verifiable demonstration Asset.
- **Derivative Asset Package** — Create only the useful supporting or derivative forms of an approved core Asset—such as full/bullet scripts, shot list, captions, clips, thumbnail concepts, audio, or graphics—without creating unnecessary variants.
- **FAQ Content Production** — Create evidence-backed answers to recurring audience questions in a form that is easy to find and understand.
- **GIF / Looping Motion Production** — Create a short looping motion Asset that demonstrates, emphasizes, or explains one idea more effectively than a static image.
- **Image / Graphic Production** — Create a visual asset whose composition communicates the intended idea rather than adding decoration.
- **Infographic Production** — Turn evidence or a structured idea into a clear visual explanation whose information hierarchy works even when the viewer only scans it.
- **LinkedIn Native Content** — Create professional-network content that is native to feed behavior rather than an article pasted into a post.
- **Long-Form Clip Extraction** — Identify self-contained short clips from a longer Asset without distorting the original meaning.
- **Long-Form Video Production** — Create sustained video communication with narrative/educational progression, demonstrations, and retention-aware structure.
- **Newsletter Production** — Create a relationship-oriented email/newsletter suited to inbox context and the audience expectation.
- **Platform-Native Adaptation** — Transform a validated core idea into genuinely native expressions for selected platforms rather than superficial reformatting.
- **Podcast Episode Production** — Create an audio-first episode whose structure and delivery fit listening context.
- **Presentation / Slideshow Production** — Build a presentation that supports a live or asynchronous audience journey instead of turning a document into slides.
- **Short-Form Video Production** — Express one useful idea quickly through platform-native visual/audio pacing and proof.

### [Marketing Synthesis](docs/playbooks/marketing-synthesis.md)

Create and improve persuasive strategy, campaigns, offers, and customer-facing marketing assets.

**14 Playbooks** in this area.

- **Marketing Strategy and Messaging** — Develop or improve positioning, messaging, value proposition, mechanism, proof, objection handling, and offer presentation around current customer and business truth.
- **Campaign Development** — Build a coherent campaign concept and the useful persuasive work needed to carry it across the relevant customer-facing surfaces.
- **Advertising Creative & Copy** — Create persuasive ad concepts/copy/creative requirements matched to audience, awareness, funnel/journey role, channel/placement context, current field evidence where useful, and destination.
- **Advertorial** — Create clearly compliant editorial-style persuasion that educates while transparently serving a commercial objective.
- **Commercial Email Sequence** — Design a multi-email persuasion sequence where each message has a distinct job and builds appropriately on prior context.
- **Comparison & Alternative Persuasion** — Help qualified buyers evaluate alternatives honestly using customer decision criteria and current competitive evidence.
- **Landing Page Persuasion** — Create a landing page or homepage that continues acquisition intent and moves the right visitor toward the desired action without overstating business truth.
- **Lead Magnet** — Create an exchange-worthy asset that solves a bounded valuable problem and naturally relates to the next commercial step.
- **Lead Nurture Strategy** — Move not-yet-ready prospects toward a better-informed decision over time rather than repeatedly asking for the sale.
- **Quiz / Assessment Conversion Asset** — Create a diagnostic experience that gives the participant useful feedback while qualifying/segmenting toward a relevant next action.
- **Sales Enablement Asset** — Create persuasive evidence/tools that help sellers and buyers resolve real decision questions consistently.
- **Sales Letter** — Create long-form written persuasion appropriate to audience sophistication and Offer complexity.
- **Video Sales Letter** — Build a sustained video persuasion narrative tied to an Offer and measurable commercial action.
- **Webinar Persuasion** — Design a webinar that creates genuine understanding/value while logically leading qualified attendees to an Offer.

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
