# BusinessOS Core Playbooks

Figure out what the business needs, keep business facts organized, choose the right work, and coordinate work across BusinessOS.

**You can ask for the outcome in normal language.** You do not need to know the names below. This page is here so you can see what is possible.

*Example:* “What should we work on first?”

## Common jobs

- **[Resolve User Intent](../../core/contracts/routing/resolve-intent/CONTEXT.md)** — Interpret an ordinary-language request and choose the smallest valid direct, diagnostic, prioritization, or multi-domain route without forcing an uncertain lexical match.
- **[Diagnose Broad Business Problem](../../core/contracts/diagnosis/business-problem/CONTEXT.md)** — Find the most likely causes of a broad business problem and decide what should be investigated or done next before jumping to a fix.
- **[Discover Next Best Work](../../core/contracts/opportunity/discover-next-best-work/CONTEXT.md)** — Turn a broad growth/prioritization goal into the highest-value next work supported by current evidence and installed modules.
- **[Coordinate Multi-Domain Request](../../core/contracts/coordination/multi-domain-request/CONTEXT.md)** — Break one larger request into the right BusinessOS areas, put the work in the right order, and keep the handoffs clear.
- **[Bootstrap Business Context](../../core/contracts/context/bootstrap-business/CONTEXT.md)** — Create evidence-based initial business context from minimal identity, first-party sources, and user-provided information.
- **[Adaptive Owned Business Discovery](../../core/contracts/context/owned-business-discovery/CONTEXT.md)** — Adaptively map owned/official business surfaces and evidence at the depth needed for the current job.
- **[Capture Brand Profile](../../core/contracts/context/brand-profile/CONTEXT.md)** — Capture durable brand voice, visual, content, channel, reference, and prohibited-style rules.
- **[Query Governed Business Truth](../../core/contracts/data/query-business-truth/CONTEXT.md)** — Query connected first-party business truth through the best governed/provider-neutral data surface and preserve evidence-linked BusinessOS references.
- **[React to Governed Business Event](../../core/contracts/monitoring/react-to-business-event/CONTEXT.md)** — Turn an authorized business occurrence into a deduplicated BusinessOS evaluation trigger without bypassing routing or approval.
- **[Configure Reactive Monitoring](../../core/contracts/monitoring/configure-reactive-monitoring/CONTEXT.md)** — Configure an event-driven BusinessOS monitoring path only when provider runtime readiness and host delivery are actually available, with explicit fallback otherwise.
- **[Diagnose Reactive Event Trace](../../core/contracts/monitoring/diagnose-event-trace/CONTEXT.md)** — Explain and repair reason-coded reactive-event failures or no-action outcomes without guessing or unsafe replay.

## More detailed playbooks

These are smaller, specific playbooks BusinessOS can use inside the larger jobs above. The names are kept simple here; open the linked contract or ask BusinessOS to explain one if you want the exact steps.

### Actions and approvals

- [Authorize Action](../../core/contracts/action-control/authorize-action/CONTEXT.md)
- [Return Delegated Work](../../core/contracts/action-control/return-work/CONTEXT.md)

### Business context

- [Adaptive Owned Business Discovery](../../core/contracts/context/owned-business-discovery/CONTEXT.md) *(main entry playbook)*
- [Bootstrap Business Context](../../core/contracts/context/bootstrap-business/CONTEXT.md) *(main entry playbook)*
- [Capture Brand Profile](../../core/contracts/context/brand-profile/CONTEXT.md) *(main entry playbook)*
- [Propose Canonical Context Update](../../core/contracts/context/propose-update/CONTEXT.md)

### Business data

- [Query Governed Business Truth](../../core/contracts/data/query-business-truth/CONTEXT.md) *(main entry playbook)*

### Coordination

- [Coordinate Multi-Domain Request](../../core/contracts/coordination/multi-domain-request/CONTEXT.md) *(main entry playbook)*
- [Create Initiative](../../core/contracts/coordination/create-initiative/CONTEXT.md)

### Diagnosis

- [Diagnose Broad Business Problem](../../core/contracts/diagnosis/business-problem/CONTEXT.md) *(main entry playbook)*

### Incidents and recovery

- [Manage Incident](../../core/contracts/incident/manage/CONTEXT.md)

### Intelligence and research

- [Evaluate Cross-System Relevance](../../core/contracts/intelligence/evaluate-relevance/CONTEXT.md)
- [Register Reusable Proof](../../core/contracts/intelligence/register-proof/CONTEXT.md)
- [Request Intelligence Refresh](../../core/contracts/intelligence/request-refresh/CONTEXT.md)

### Measurement

- [Design Experiment](../../core/contracts/measurement/design-experiment/CONTEXT.md)
- [Publish Metric Observation](../../core/contracts/measurement/publish-metric/CONTEXT.md)

### Monitoring

- [Configure Reactive Monitoring](../../core/contracts/monitoring/configure-reactive-monitoring/CONTEXT.md) *(main entry playbook)*
- [Diagnose Reactive Event Trace](../../core/contracts/monitoring/diagnose-event-trace/CONTEXT.md) *(main entry playbook)*
- [React to Governed Business Event](../../core/contracts/monitoring/react-to-business-event/CONTEXT.md) *(main entry playbook)*

### Opportunities

- [Discover Next Best Work](../../core/contracts/opportunity/discover-next-best-work/CONTEXT.md) *(main entry playbook)*

## Want to see exactly how one works?

Ask BusinessOS something like:

> “Show me the exact steps for Authorize Action, including what it reads, what it saves, and how it knows when it is done.”

The linked contract is the authoritative version. This page is only a simpler map for people.
