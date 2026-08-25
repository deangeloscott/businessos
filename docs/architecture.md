# Architecture

Core owns canonical context and collaboration mechanics; specialized systems own domain meaning. Persistent intelligence uses SourceRecord → Observation → Insight → Opportunity → Action → Change/Asset → Verification → OutcomeEvaluation → Learning. One Insight may fan out into distinct domain Opportunities; delegated work uses WorkRequest and does not duplicate the Opportunity.

## Adaptation and workers
BusinessOS standardizes **what must remain true**—business semantics, evidence/provenance, ownership, authorization, required outputs, and validation—while leaving **how valid work is executed** to the model/harness/capability layer where possible. Business/Brand configuration, scoped `PreferenceProfile` state, task instructions, and measured `Learning` can adapt execution without rewriting BusinessOS product logic.

BusinessOS is not an agent runtime. One model, sequential sessions, harness-managed subagents, or different compatible harnesses may participate in the same durable business state. Runs and WorkRequests preserve execution/handoff semantics. The harness owns spawning/scheduling/parallelism; BusinessOS currently does not claim arbitrary simultaneous independent writes to the same canonical object are conflict-safe.
