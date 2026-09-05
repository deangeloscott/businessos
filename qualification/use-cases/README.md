# AURA Real-World Use-Case Library

This library exists to answer one question:

> **When a normal user gives AURA real business work, does AURA help capable intelligence produce an excellent result and preserve useful organizational meaning?**

The library is maintainer-only. **Candidates must never see this directory, its file names, its coverage metadata, or any judge criteria.**

## Minimal structure

```text
qualification/use-cases/
  library.json          # maintainer-only pairing and descriptive coverage metadata
  requests/             # ordinary user requests, source material for the harness
  judges/               # hidden expected-outcome guidance for independent review
```

Business context comes from ordinary staged organization material under `qualification/fixtures/`. When a case is prepared, the candidate receives only:

1. a neutral staged AURA product with no `qualification/` or test files;
2. a neutral organization workspace containing normal business files;
3. the request text itself as a normal user message;
4. the model/harness's ordinary tools and Skills.

The candidate does **not** receive a case folder, case ID, target Workflow, coverage metadata, rubric, judge file, expected outcome, checkpoint, receipt, evaluator state, or benchmark terminology.

## Current shape

The library is intentionally organized around **real business jobs**, not around one artificial prompt per Workflow. It currently includes dozens of cases spanning:

- B2B SaaS;
- local services;
- ecommerce;
- creator/media;
- professional services;
- customer research and objection/segment work;
- competitor/pricing/positioning work;
- industry and market-change research;
- SEO/AEO and local discovery;
- content and creative production;
- offers, pages, campaigns, and nurture;
- conversion, retention, and subscription work;
- cross-domain prioritization;
- longitudinal memory and contradictory/new evidence.

Run the small maintainer coverage view at any time:

```bash
python3 qualification/use_case_coverage.py
```

That report is descriptive only. It summarizes the breadth represented by the current library; it never creates a release obligation or tells the candidate how to work.

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
- which authored Workflows are obviously exercised directly in a case;
- whether the case is composed, cross-domain, or longitudinal.

Coverage metadata is never candidate-visible and is not an execution specification.

The goal is **not** one synthetic prompt per Workflow, complete Playbook inventory coverage, or a hidden release checklist. The goal is a compact but broad set of high-value, realistic business jobs whose combined evidence gives confidence that AURA's operating knowledge works in actual use.

Workflow tags are optional descriptive annotations for cases that clearly exercise a particular Workflow. An authored Workflow being untagged is not by itself a qualification gap, and adding a Workflow does not create an obligation to add a matching case. Use a focused Workflow diagnostic only when real evidence gives a reason to isolate that body of operating knowledge.

## Longitudinal cases

A longitudinal case is simply an ordered series of ordinary requests against the same organization workspace, with fresh model context where the scenario requires it. Later requests should be able to benefit from prior durable AURA state. New or contradictory evidence should update the organization's understanding rather than leave stale truth dominant.

No special AURA memory-test protocol is required.

## Candidate isolation

The existing qualification staging boundary remains mandatory:

- candidate product/workspace and evaluator state are physically separate;
- `qualification/`, tests, judge files, case metadata, checkpoints, and evaluator files are not copied into the staged product;
- candidate-visible paths use neutral names;
- hidden criteria remain evaluator-side for the entire run;
- the candidate should not have filesystem access to the source checkout.

If a harness cannot enforce that boundary, do not use it for blind qualification.

## How to run one case

```bash
python3 qualification/prepare_run.py --case <case-id>
python3 qualification/task_controller.py start /path/to/run
```

Give the worker only the neutral product/workspace and the printed ordinary request. After the worker finishes:

```bash
python3 qualification/task_controller.py finish /path/to/run
python3 qualification/evaluate_run.py /path/to/run
python3 qualification/build_judge_prompt.py /path/to/run
```

Use a fresh independent judge context, then rerun `evaluate_run.py` after `evaluator/judgments.json` is written.

## Product-template possibility

Strong cases may later inspire public examples, starter prompts, or business-use templates. If that happens, create a separate user-facing version. Do not expose the hidden qualification/judge source directly, because preserving blind qualification remains useful.
