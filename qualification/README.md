# AURA Business Capability Qualification Suite

This directory tests **ViralTrac AURA as a business operating system**, not the intelligence brand of a particular model or harness.

The governing question is: **Does every AURA playbook/process actually deliver the business capability it claims, at a professionally usable and outcome-ready level, while leaving correct governed AURA state behind?**

## Qualification standard

Every AURA contract is treated as a product claim. A contract that says it can create an article, landing page, presentation, carousel, competitor analysis, customer Insight, experiment, publication, or other result must create the real result when the environment provides the required capability. A description of what could be created is not a substitute.

Passing has layers:

1. **Process correctness** — AURA's declared workflow, required subcontracts, evidence/provenance, lifecycle, authorization, and completion rules were followed.
2. **Professional quality** — the business work is genuinely usable, sufficiently detailed for its audience/task, accurate, and clear.
3. **Competitive / outcome readiness** — where the domain is competitive, AURA inspects the current field and does the work a strong practitioner would reasonably expect to maximize the intended outcome.
4. **Observed outcome** — later longitudinal testing can determine whether rankings, citations, conversions, revenue, retention, or other results actually changed. Outcome readiness must never be misreported as an observed result.

For SEO/AEO, competitive readiness normally requires inspecting live search/AI-answer surfaces, comparing multiple leaders, understanding common expectations and meaningful leader differences, and producing work that is intentionally more useful/appropriate while acknowledging authority and external constraints. For advertising/marketing, it normally requires sampling relevant competitors and current ad-transparency/creative surfaces, analyzing recurring messages/offers/creative families and landing paths, and treating longevity/engagement as proxies rather than proof of profitability. For organic content, visible views/shares/comments/velocity should be normalized to account baseline, format, age, distribution, and audience where possible. For visual/content artifacts, “better” means better fit for the intended audience/task—not simply more detail.

## What gets tested

- **Contract acceptance:** one generated event for every installed contract. The contract metadata and body are the specification source; no second manual contract list is maintained.
- **Capability coverage:** every declared AURA capability is mapped to the contract tests that require or optionally use it; unused declarations are surfaced explicitly.
- **Domain missions:** full Core, Customer Intelligence, Competitor Intelligence, Industry Intelligence, SEO/AEO, Content Synthesis, Marketing Synthesis, and Customer Optimization missions.
- **Cross-domain missions:** business problems where AURA must choose and compose domains rather than being told which contract to run.
- **Marathon missions:** continuous accumulated operation where later evidence, outcomes, contradictions, and changes must alter future work without resetting the workspace.
- **Concurrency missions:** two independent operators/harnesses work the same business and shared workspace simultaneously to test deduplication, semantic ownership, operator provenance, collisions, and shared-state integrity.

The suite is deliberately capable of hours-long execution. Candidate instructions tell the agent to continue through the queue without pausing for permission between events.

## Files

- `build_suite.py` — discovers every `contracts/**/CONTEXT.md`, extracts declared behavior, generates acceptance tests, and maps declared capabilities.
- `prepare_run.py` — creates a **fresh staged AURA product copy** plus an external qualification workspace, initializes synthetic benchmark businesses, and builds the uninterrupted candidate queue plus hidden evaluator specification.
- `checkpoint.py` — deterministic before/after workspace snapshots and validation for every event.
- `launch.py` — optional generic shell-command adapter for launching a harness once against the uninterrupted queue while capturing stdout/stderr.
- `evaluate_run.py` — verifies Runs, root evidence, required-subcontract evidence, validation, artifact existence, state changes, competitive-field evidence, blockers, and merges professional-quality judgments.
- `build_judge_prompt.py` — creates an independent review instruction file after hard-gate evaluation.
- `compare_runs.py` — compares two independently evaluated gauntlets and surfaces repeated failures as likely AURA hotspots.
- `prepare_concurrency.py` / `launch_concurrent.py` — stage and launch two independent candidates simultaneously against one shared AURA workspace.
- `rubrics/rubrics.json` — common, domain-specific, cross-domain, marathon, and concurrency professional/competitive quality standards.
- `missions/missions.json` — domain, cross-domain, marathon, and concurrency missions.
- `fixtures/*.json` — controlled business worlds. They include first-party evidence and later-period changes; live research is still expected where the test requires the current competitive field.

## Run the full gauntlet

From the AURA product root:

```bash
python3 qualification/build_suite.py
python3 qualification/prepare_run.py --profile full
```

`prepare_run.py` prints a run directory, **clean staged product copy**, external workspace, queue, and `RUN-INSTRUCTIONS.md`. Point the candidate AI/harness at the staged product root and give it the instruction file. The candidate should run the entire queue continuously.

The candidate must retain:

```bash
export BUSINESSOS_WORKSPACE=/path/printed/by/prepare_run
export AURA_QUALIFICATION_RUN=/path/to/qualification/run
```

If the harness exposes a CLI that can accept the instruction file, use the portable launcher to capture the whole run:

```bash
python3 qualification/launch.py /path/to/run \
  --label candidate-a \
  --command 'YOUR_HARNESS_COMMAND {instructions}'
```

Available command-template placeholders are `{instructions}`, `{workspace}`, `{run_dir}`, and `{product_root}`. The harness command is deliberately not hard-coded into AURA.

## Evaluate the run

After the queue finishes:

```bash
python3 qualification/evaluate_run.py /path/to/run
```

This creates:

- `evaluator/hard-and-merged-results.json`
- `evaluator/review-packets.json`
- `evaluator/summary.json`
- `REPORT.md`

The hard evaluator checks checkpoint/receipt existence, real AURA Runs, root-contract match, root completion evidence, required subcontract evidence, workspace/business validation, truthful completion, actual artifact creation when promised, declared state writes, customer-facing completion governance, and reconstructable competitive-field evidence for live competitive tests.

A human or independent judge then reviews the **actual business output**, evidence, state diff, and competitive field. Build a ready-to-use judge instruction file with:

```bash
python3 qualification/build_judge_prompt.py /path/to/run
```

The judge writes every required 0–5 rubric score to `evaluator/judgments.json`. Rerun:

```bash
python3 qualification/evaluate_run.py /path/to/run
```

Final quality classifications include:

- `FAIL`
- `BLOCKED-EXTERNAL`
- `FUNCTIONAL-NOT-ACCEPTABLE`
- `ACCEPTABLE`
- `COMPETITIVE`
- `EXCEPTIONAL`

A mechanically valid but shallow output cannot qualify as competitive merely because files and schemas are correct.

## Focused runs

```bash
# every contract in one domain
python3 qualification/prepare_run.py --profile atomic --domain seo-aeo

# domain missions only
python3 qualification/prepare_run.py --profile domains

# cross-domain missions only
python3 qualification/prepare_run.py --profile cross-domain

# endurance / accumulated-state missions
python3 qualification/prepare_run.py --profile marathon
```

## Two independent full candidates

Prepare the same profile twice. Each gets a clean AURA product copy and isolated workspace:

```bash
python3 qualification/prepare_run.py --profile full --run-id candidate-a
python3 qualification/prepare_run.py --profile full --run-id candidate-b
```

Run and judge both independently, then compare them:

```bash
python3 qualification/compare_runs.py /path/to/candidate-a /path/to/candidate-b
```

The comparison classifies events as robust passes, candidate-sensitive, environment-sensitive, or **repeated failure / AURA hotspot**. Repeated failures across competent independent candidates are especially important evidence that the AURA contract/process itself needs improvement.

## Shared-workspace concurrency

Prepare one shared workspace with two operator lanes:

```bash
python3 qualification/prepare_concurrency.py
```

Then either give lane A and lane B instruction files to two candidates manually, or launch both commands simultaneously:

```bash
python3 qualification/launch_concurrent.py /path/to/run \
  --command-a 'HARNESS_A {instructions}' \
  --command-b 'HARNESS_B {instructions}'
```

Both candidates share the business workspace but retain distinct `BUSINESSOS_OPERATOR_REF` values. Evaluate the result with the same `evaluate_run.py` and independent quality review.

## How every event is audited

The uninterrupted candidate must create a deterministic `before` checkpoint, execute the real business work, write a structured receipt, create an `after` checkpoint, and immediately continue. The result package therefore preserves:

- candidate stdout/stderr and launch metadata when launched through the helper;
- workspace tree and object hashes before/after;
- AURA Runs and contract-execution manifests;
- root and subcontract evidence;
- actual created artifacts;
- canonical/source references;
- reconstructable competitive-field references when applicable;
- workspace/business validation;
- deterministic gate failures;
- independent quality scores and notes.

This makes it possible to inspect both **what the business received** and **what AURA became internally** after the event.

## Blockers

A candidate may record a real blocker instead of fabricating execution. Blockers are classified as `external_capability`, `authorization`, `missing_required_data`, `external_service`, or `aura_process`. Genuine external blockers are reported separately as `BLOCKED-EXTERNAL`; an AURA-process inability remains an AURA failure. This prevents missing tools from being confused with successful capability while also preventing AURA from being blamed for an unavailable external system.

## Interpreting failures

A failed event is not automatically a model failure. Review the contract, transcript/logs, artifact, Run/contract-execution record, state diff, competitive snapshot, and rubric. Useful triage categories include:

- AURA contract/process defect or ambiguity
- missing AURA capability/process
- insufficient competitive/outcome methodology
- candidate reasoning/execution failure
- harness/tool/provider failure
- unavailable external capability
- qualification fixture/evaluator defect
- acceptable probabilistic variance

If multiple competent candidates fail the same maneuver in the same way, treat that as strong evidence that AURA itself needs improvement.

## Release coverage regression

`tests/run_qualification_framework.py` verifies that the qualification generator maps the current manifest contract count and capability count, all required subcontracts resolve, every contract has gates/rubrics/tasks, every domain has a full mission, and the cross-domain/marathon/concurrency layers remain present. It is included in `tests/run_all.py`, so adding a contract without qualification coverage cannot silently pass the normal release gate.

The hours-long gauntlet itself is intentionally **not** run as a release-unit test. It requires a real selected AI/harness, live competitive research for applicable events, actual artifact generation, and independent business-quality review.

## Non-goals

This qualification framework is not a mandatory AURA runtime, server, database, scheduler, UI, or model adapter. It uses AURA's existing local-first workspace architecture and can be driven by any harness capable of working from the filesystem. Harness-specific automation may be added as optional adapters without changing qualification semantics.
