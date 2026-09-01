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
- **Asset** — A persistent business artifact such as a page, video, email, image, report, presentation, or sales document.
- **ChangeEvent** — An optional durable record that a material state changed and future work may benefit from remembering it.
- **VerificationRecord** — Optional durable evidence that an important claimed state was checked, when the task/SOP/consequence warrants it.
- **MetricObservation** — A measured value at a time/window.
- **OutcomeEvaluation** — An evidence-backed judgment about what happened and how confidently an intervention contributed.
- **Learning** — An evidence-backed proposition that should influence future work under stated conditions inside the active organization.
- **Domain Learning** — Learning scoped to one specialized domain inside the active organization.
- **Business Learning** — Learning that genuinely applies across the active organization.
- **Canonical owner** — The one AURA domain responsible for the authoritative semantic meaning of a canonical responsibility/object.
- **Capability** — A provider-neutral ability an AURA SOP may need or benefit from, such as `crm.opportunity.read` or `cms.page.publish`. Live availability and provider/tool choice belong to the active harness/runtime.
- **PreferenceProfile** — Durable business-scoped preferences for a business, team, role, or operator label. Preferences guide otherwise-valid choices but do not become business truth or authorization.
- **Operator ref** — An optional opaque workspace/session label used for attribution or scoped preferences. It grants no authority and need not contain personal information.
- **Run** — A bounded organization-owned work receipt for material continuity. A Run records the actual method used: AURA playbook, external Skill, model-created method, or ad-hoc work.
- **Context Plan** — The smallest relevant AURA policy/SOP/schema/object set selected for a piece of work. It does not describe the host's full runtime state.
- **ProcessExtension** — Business-scoped operational knowledge that augments an AURA playbook or defines a local playbook without mutating the canonical product.
- **InnovationPackage** — An explicitly prepared portable package for sharing reusable process knowledge across organization boundaries without implicitly exposing another organization's private state.
- **PlatformChange** — A durable, refreshable record of a material external platform/topic state, kept distinct from measured business outcomes.

## ProofRecord
A source-linked record of evidence that supports a specific claim, outcome, transformation, customer experience, or other business assertion. It records what the evidence actually supports plus relevant usage constraints.

## Content Intelligence
The Content Synthesis function that studies content trends, creators, creative structures, platform patterns, and business-specific content performance to extract reusable communication mechanisms. It learns why patterns may work rather than copying popular content.
