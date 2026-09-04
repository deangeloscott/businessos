# AURA Real-World Use-Case Library

This library exists to answer one question:

> **When a normal user gives AURA real business work, does AURA help capable intelligence produce an excellent result and preserve useful organizational meaning?**

The library is maintainer-only. **Candidates must never see this directory, its file names, its coverage metadata, or any judge criteria.**

## Minimal structure

```text
qualification/use-cases/
  library.json          # maintainer-only coverage and pairing metadata
  requests/             # ordinary user requests, source material for the harness
  judges/               # hidden expected-outcome guidance for independent review
```

Business context continues to come from ordinary staged organization material. When a case is prepared, the candidate receives only:

1. a neutral staged AURA product with no `qualification/` or test files;
2. a neutral organization workspace containing normal business files;
3. the request text itself as a normal user message;
4. the model/harness's ordinary tools and Skills.

The candidate does **not** receive a case folder, case ID, target Workflow, coverage metadata, rubric, judge file, expected outcome, checkpoint, receipt, evaluator state, or benchmark terminology.

## Requests

A request should sound like something a real owner, operator, marketer, researcher, or team member would naturally ask.

Good:

> Qualified traffic is healthy, but demo conversion has slipped. Figure out what is actually going wrong and make the highest-value improvement you can from the evidence available.

Bad:

> Execute the customer-optimization conversion workflow and satisfy the qualification rubric.

A request may naturally exercise one Workflow, several related Workflows, several operating areas, or a sequence of work over time. We care about whether the real business job succeeds, not whether the model follows a hidden execution graph.

## Judges

Each request has separate hidden judge guidance describing what a genuinely strong outcome should accomplish. Judge guidance specifies **business outcomes and quality expectations**, not exact files, tool calls, step ordering, source counts, or AURA ceremony.

The independent judge should inspect the actual result, evidence, relevant organization state, and applicable AURA operating knowledge. Equivalent or better methods are valid. Missing substantive work is not.

## Coverage

`library.json` records only enough maintainer metadata to answer questions such as:

- which industries and business shapes are represented;
- which operating areas are exercised;
- which authored Workflows are exercised directly or as part of larger work;
- whether the case is atomic, composed, cross-domain, or longitudinal.

Coverage metadata is never candidate-visible and is not an execution specification.

The goal is not one synthetic prompt per Workflow. The goal is a compact set of **high-value, realistic business jobs** whose combined coverage gives strong evidence that AURA's operating knowledge works in actual use.

## Longitudinal cases

A longitudinal case is simply an ordered series of ordinary requests against the same organization workspace, with fresh model context where the scenario requires it. Later requests should be able to benefit from prior durable AURA state. New or contradictory evidence should update the organization's understanding rather than leave stale truth dominant.

No special AURA memory-test protocol is required.

## Candidate isolation

The existing qualification staging boundary remains mandatory:

- candidate product/workspace and evaluator state are physically separate;
- `qualification/`, tests, judge files, case metadata, checkpoints, and evaluator files are not copied into the staged product;
- candidate-visible paths use neutral names;
- hidden criteria remain evaluator-side for the entire run.

If a harness cannot enforce that boundary, do not use it for blind qualification.

## Product-template possibility

Strong cases may later inspire public examples, starter prompts, or business-use templates. If that happens, create a separate user-facing version. Do not expose the hidden qualification/judge source directly, because preserving blind qualification remains useful.
