# Efficient use of AURA

AURA should help a capable model produce useful work with less repeated discovery.
Context is useful when it changes the work, not because it fills a checklist.

- Start with `scripts/enter.py` or equivalent direct retrieval. Entry returns bounded
  organization context, applicable preferences, and navigation candidates. The model
  chooses what to read and whether any Playbook or Workflow helps.
- Ordinary entry reuses one canonical snapshot for saved-work discovery, local Workflow
  candidates, preferences, and generated-knowledge freshness. It does not keep a daemon
  or cache business truth indefinitely. Read diagnostics remain part of the result.
- A selected Workflow's context plan includes its relevant guidance and actual object
  references. Schemas, policies, and other supporting references remain available on
  demand; inspect the returned primary and supporting files rather than assuming every
  referenced document was loaded.
- Reuse durable decisions, preferences, evidence and artifacts. Do not save routine
  tool calls, full chats, or receipts merely to prove that work happened. Runs are optional.
- The native harness owns model selection, context management, tools and execution.
  Use its actual usage reports when measuring cost. Cumulative input includes repeated
  and cached context; it is not all newly loaded AURA content.

Measure time to a usable result, repeated questions or research avoided, correction
effort, and actual model/context usage when available. Use the same task, workspace
and harness for a useful before/after comparison. File counts, word budgets and passing
suites do not establish better business outcomes.

Entry, memory, preference, setup and workspace regressions in `tests/run_all.py` protect
the relevant behavior. Add a focused regression when fixing a meaningful boundary
failure. Qualification is for real quality questions, not mandatory ceremony for every
change. See [operating knowledge](operating-knowledge.md) and
[qualification](../qualification/README.md).
