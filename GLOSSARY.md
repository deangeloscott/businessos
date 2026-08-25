# Business OS Glossary

Use these terms consistently.

- **Business Context** — Controlled facts about the business: Brand, Products/Services, Offers, Audiences, Markets, Objectives, economics, and constraints.
- **SourceRecord** — Where evidence came from and when/how it was retrieved.
- **Observation** — Something directly observed from a source, system, event, or measurement.
- **Insight** — An evidence-backed interpretation owned by the domain responsible for its meaning.
- **Opportunity** — A potentially valuable intervention with exactly one semantic owner.
- **Initiative** — Coordination of multiple genuinely distinct Opportunities toward one larger outcome.
- **ActionPacket** — The executable plan for an Opportunity.
- **WorkRequest** — Delegated specialized work. Delegation does not create another Opportunity.
- **Asset** — A persistent business artifact such as a page, video, email, image, report, or sales document.
- **ChangeEvent** — The externally observable state changed by an Action.
- **VerificationRecord** — Independent evidence that the intended change actually happened correctly.
- **MetricObservation** — A measured value at a time/window.
- **OutcomeEvaluation** — The evidence-backed judgment about what happened after an intervention and how confidently it contributed.
- **Learning** — An evidence-backed proposition that should influence future decisions under stated conditions.
- **Domain Learning** — Learning owned by one specialized OS.
- **Business Learning** — Cross-domain Learning specific to one business.
- **System Learning** — Carefully governed Learning that may generalize across businesses.
- **Canonical owner** — The one system responsible for the authoritative semantic meaning of a responsibility/object.
- **Fan-out** — One Insight independently creates distinct Opportunities in multiple domains.
- **Delegation** — One Opportunity uses another system's specialized execution through a WorkRequest.
- **Capability** — Provider-neutral ability such as `crm.opportunity.read` or `cms.page.publish`.
- **AttentionItem** — A deduplicated, business-scoped condition that currently needs user/harness awareness because work is blocked, approval/input/capability is required, or a material change needs review. It is not a notification channel.
- **PlatformChange** — The current/versioned verified state of an external platform/topic, independently refreshable from BusinessOS software releases and explicitly separated from measured business outcomes.
- **Event** — A bounded reference to an authoritative occurrence that may trigger evaluation; it is not an action command, permission, exposure, or outcome.
- **EventReactionDecision** — The idempotent BusinessOS disposition of an Event (ignore, defer, coalesce, evaluate, block, or fallback), including materiality, route, trace lineage, and reason codes.
- **PreferenceProfile** — Business-scoped durable preferences for a business, team, role, or operator. Preferences guide valid choices but do not override mandatory rules, authorize actions, or become business truth.
- **Operator ref** — A stable, potentially opaque workspace/session label recorded on a Run for attribution and preference resolution; it does not grant authority and need not contain personal information.
- **Run** — A bounded execution of one contract for one active business.
- **Context Plan** — The smallest set of rules, objects, schemas, and references needed for the active contract.

## ProofRecord
A shared, source-linked record of evidence that supports a specific claim, outcome, capability, transformation, or customer experience. It records what the proof actually supports plus permission and usage constraints.

## Content Intelligence
The Content Synthesis function that studies content trends, creators, creative structures, platform patterns, and business-specific content performance to extract reusable communication mechanisms. It learns why patterns may work rather than copying popular content.

- **Provider** — Software/service implementation capable of supplying one or more provider-neutral Business OS capabilities.
- **Provider Preference** — Transparent preferred/allowed/blocked provider configuration at business, environment, or distribution scope; preference is not authorization.
- **Capability Resolver** — Deterministic selection logic that uses existing bindings first, then scoped preferences, compatible providers, and finally manual fallback.
- **Publisher Provenance** — Machine-readable origin/update metadata in `PUBLISHER.json` that can travel with distributable copies.
