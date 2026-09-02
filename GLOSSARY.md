# ViralTrac AURA Glossary

Use these terms consistently.

- **Business Context** — Durable organization-owned facts and constraints about the business: Brand, products/services, offers, audiences, markets, objectives, economics, and other relevant context.
- **SourceRecord** — Where evidence came from and when/how it was obtained.
- **Observation** — Something directly observed from a source, system, event, or measurement.
- **Insight** — An evidence-backed interpretation owned by the domain responsible for its meaning.
- **Opportunity** — An optional durable record of a potentially valuable intervention or improvement worth considering.
- **Initiative** — Optional coordination state for several genuinely distinct pieces of work toward one larger outcome.
- **DecisionRecord** — A durable organizational decision worth remembering, including who/what made it, when, scope, and basis. It is not a permission token.
- **WorkRequest** — A real durable handoff whose purpose, expected output, context, and unresolved state should survive the current session. It is not a mirror of subagents or tool routing.
- **AttentionItem** — A deduplicated material condition worth future organizational awareness. AURA owns the meaning and lifecycle, not notification delivery.
- **Asset** — A persistent business artifact or durable reference to one, such as a page, video, email, image, report, presentation, campaign asset, or sales document.
- **ChangeEvent** — An optional durable record that a material state changed and future work may benefit from remembering it.
- **VerificationRecord** — Optional durable evidence that an important claimed state was checked, when the task, consequence, or reusable method warrants it.
- **MetricObservation** — A measured value at a time/window.
- **OutcomeEvaluation** — An evidence-backed judgment about what happened and how confidently an intervention contributed.
- **Learning** — An evidence-backed proposition that should influence future work under stated conditions inside the active organization.
- **Domain Learning** — Learning scoped to one specialized domain inside the active organization.
- **Business Learning** — Learning that genuinely applies across the active organization.
- **Canonical owner** — The one AURA domain responsible for the authoritative semantic meaning of a canonical responsibility/object.
- **Playbook** — A human-meaningful end-to-end business job that bundles useful AURA operating knowledge, such as Competitor Research or Customer Research. A Playbook is not an execution graph or permission boundary.
- **Workflow** — A reusable procedure that helps accomplish part of a Playbook and may also be useful independently. Workflows describe outcomes, evidence/quality requirements, and minimum useful procedure in natural language rather than binding tools/providers.
- **Step** — The minimum procedural guidance inside a Workflow that materially improves repeatability, truth, evidence discipline, scope, or quality. A Step should not micromanage implementation the capable model/harness can choose better itself.
- **Skill** — A host/harness package of reusable instructions, procedures, scripts, references, or other resources. AURA can coexist with external Skills; the included AURA Skill is a thin awareness adapter, not a replacement for them.
- **Tool** — A concrete ability exposed by the active harness/runtime, such as browsing, file operations, an API, renderer, shell command, connector, or MCP tool. AURA does not maintain a universal tool/capability ontology.
- **PreferenceProfile** — Durable business-scoped preferences for a business, team, role, or operator label. Preferences guide otherwise-valid choices but do not become business truth or authorization.
- **Operator ref** — An optional opaque workspace/session label used for attribution or scoped preferences. It grants no authority and need not contain personal information.
- **Run** — An optional bounded organization-owned work receipt for material continuity/provenance. A Run may record an AURA Playbook, AURA Workflow, external Skill, model-created method, or ad-hoc method; it is not required to do or save work.
- **Context Plan** — A bounded set of AURA policy, Workflow, schema, and organization objects selected to help a piece of work. It does not describe the host's full runtime state or choose how the work must execute.
- **ProcessExtension** — Organization-scoped reusable Workflow knowledge that augments an installed Workflow or defines a local Workflow without mutating canonical AURA product source.
- **WorkflowEvolutionProposal** — An evidence-backed candidate improvement to reusable Workflow knowledge. It is not an automatic self-modification mechanism or approval gate.
- **InnovationPackage** — An explicitly prepared portable package for sharing reusable process knowledge across organization boundaries without implicitly exposing another organization's private state.
- **PlatformChange** — A durable, refreshable record of a material external platform/topic state, kept distinct from measured business outcomes.

## ProofRecord
A source-linked record of evidence that supports a specific claim, outcome, transformation, customer experience, or other business assertion. It records what the evidence actually supports plus relevant usage constraints.

## Content Intelligence
The Content Synthesis function that studies content trends, creators, creative structures, platform patterns, and business-specific content performance to extract reusable communication mechanisms. It learns why patterns may work rather than copying popular content.
