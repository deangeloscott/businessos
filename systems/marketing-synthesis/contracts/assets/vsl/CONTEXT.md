---
id: marketing.assets.vsl
type: playbook
owner_system: marketing-synthesis
artifact_role: customer_facing_production_root
reads:
- Opportunity
- type: Insight
  owner_system: customer-intelligence
- type: Insight
  owner_system: competitor-intelligence
- Asset
- WorkRequest
- ProofRecord
writes:
- Asset
capabilities:
  required:
  - none
  optional:
  - creative.text.generate
  - cms.page.publish
  - experiment.run
  - tracking.read
context:
- AudienceSegment
- Brand
- Offer
subcontracts:
  required:
  - marketing.intake.persuasion-brief
  - marketing.vsl.persuasion-architecture
  - marketing.vsl.script
  - marketing.vsl.visual-brief
  - marketing.vsl.offer-cta
  - marketing.vsl.qa
---
# Video Sales Letter

## Purpose
Build a sustained video persuasion narrative tied to an Offer and measurable commercial action.

## Business Outcome
Increase the likelihood of the desired commercial action through an evidence-backed VSL matched to audience awareness, Offer, proof, and acquisition context.

## Run When
Use when the organization needs a VSL to remove a commercial persuasion gap or create/improve a conversion asset. An Opportunity, prior Asset, or real WorkRequest may provide context but is not required.

## Process
1. [AI] Define prospect state, desired action, Offer, dominant problem/desire, mechanism, objections, proof, acquisition context, and expected viewing environment.
2. [AI] Use the authored VSL submethods as relevant composition/quality knowledge to design the persuasion arc: pattern/context → stakes/problem → desired future → mechanism/new understanding → proof → objections → Offer/value/risk → CTA.
3. [HYBRID] Ensure every material business claim/proof segment is evidence-backed and no fabricated scarcity, urgency, guarantee, or outcome is introduced.
4. [AI] Write natural spoken-language script with demonstrations, visual proof, pacing, transitions, and CTA moments appropriate to the audience and complexity.
5. [AI] Match length to the communication job rather than an arbitrary VSL convention; specify only the visual/audio treatment that materially improves understanding or persuasion.
6. [HYBRID] If actual video/media production is within the user's request and the harness has suitable capabilities, produce it directly using those capabilities. Otherwise preserve the script/visual brief as usable Assets or create a WorkRequest only when a real durable handoff to another actor must survive the current interaction.
7. [HYBRID] Apply customer-facing claim checks/QA appropriate to the artifact and preserve the resulting Asset(s). Publication, deployment, and measured outcome remain separate facts.

## Verification
- The VSL's promises, proof, Offer terms, urgency, and CTA stay within current organizational truth/evidence.
- Script, visual treatment, and persuasion architecture fit the actual viewing/audience context.
- Media production is composed directly when available; AURA does not delegate work between internal domains.
- A WorkRequest is used only for a real durable organizational handoff.

## Completion Criteria
- The requested VSL is available at the fidelity the user asked for—such as script/production brief or completed media—with truthful limitations and no internal AURA request chain.
