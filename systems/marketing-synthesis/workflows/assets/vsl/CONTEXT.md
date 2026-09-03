---
id: marketing.assets.vsl
type: workflow
owner_system: marketing-synthesis
reads:
- Opportunity
- type: Insight
  domain: customer-intelligence
- type: Insight
  domain: competitor-intelligence
- Asset
- WorkRequest
- ProofRecord
writes:
- Asset
context:
- AudienceSegment
- Brand
- Offer
---
# Video Sales Letter

## Purpose
Build a sustained video persuasion narrative tied to an Offer and measurable commercial action.

## Business Outcome
Increase the likelihood of the desired commercial action through an evidence-backed VSL matched to audience awareness, Offer, proof, and acquisition context.

## Run When
Use when the organization needs a VSL to remove a commercial persuasion gap or create/improve a conversion asset. An Opportunity, prior Asset, or real WorkRequest may provide context but is not required.

## Process
1. Define prospect state, desired action, Offer, dominant problem/desire, mechanism, objections, proof, acquisition context, and expected viewing environment.
2. Use relevant VSL operating knowledge—such as persuasion architecture, scripting, visual planning, or QA—only where it materially improves the requested result. The active model may combine, skip, adapt, or replace those methods when another sound approach better fits the job.
3. Build the persuasion arc appropriate to the audience and Offer, commonly moving through context/stakes → desired future → mechanism/new understanding → proof → objections/risk → Offer/value → CTA without treating that sequence as a mandatory template.
4. Ensure every material business claim/proof segment is evidence-backed and no fabricated scarcity, urgency, guarantee, or outcome is introduced.
5. Write natural spoken-language material with demonstrations, visual proof, pacing, transitions, and CTA moments appropriate to the audience and complexity.
6. Match length to the communication job rather than an arbitrary VSL convention; specify only the visual/audio treatment that materially improves understanding or persuasion.
7. If actual video/media production is within the user’s request and the harness has suitable capabilities, produce it directly using those capabilities. Otherwise preserve the script/visual brief as usable Assets or create a WorkRequest only when a real durable handoff to another actor must survive the current interaction.
8. Apply customer-facing claim checks and QA appropriate to the artifact and preserve the resulting Asset(s). Publication, deployment, and measured outcome remain separate facts.

## Proportionate Scope
Use only the research, persuasion depth, proof, production detail, and supporting methods needed for the actual audience, Offer complexity, decision risk, and requested fidelity. Expand when the commercial decision is high-consideration or evidence is uncertain; do not maximize length or production complexity merely because more is possible.

## Verification
- The VSL’s promises, proof, Offer terms, urgency, and CTA stay within current organizational truth/evidence.
- Script, visual treatment, and persuasion architecture fit the actual viewing/audience context.
- Relevant Workflows are operating knowledge, not required execution stages.
- Media production is composed directly when available; AURA does not delegate work between internal domains.
- A WorkRequest is used only for a real durable organizational handoff.

## Completion Criteria
- The requested VSL is available at the fidelity the user asked for—such as script/production brief or completed media—with truthful limitations and no internal AURA request chain.
