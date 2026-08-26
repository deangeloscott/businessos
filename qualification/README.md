# AURA Business Capability Qualification Suite

This directory tests **ViralTrac AURA as a business operating system**, not the intelligence brand of a particular model or harness.

The governing question is:

> **Does every AURA playbook/process actually deliver the business capability it claims, at a professionally usable and outcome-ready level, while leaving correct governed AURA state behind?**

## Qualification standard

Every AURA contract is treated as a product claim. A contract that says it can create an article, landing page, presentation, carousel, competitor analysis, customer Insight, experiment, publication, or other result must create the real result when the environment provides the required capability. A description of what could be created is not a substitute.

Passing has layers:

1. **Process correctness** — AURA's declared workflow, required subcontracts, evidence/provenance, lifecycle, authorization, and completion rules were followed.
2. **Professional quality** — the business work is genuinely usable, sufficiently detailed for its audience/task, accurate, and clear.
3. **Competitive / outcome readiness** — where the domain is competitive, AURA inspects the current field and does the work a strong practitioner would reasonably expect to maximize the intended outcome.
4. **Observed outcome** — later real-world/longitudinal testing can determine whether rankings, citations, conversions, revenue, retention, or other results actually changed. Outcome readiness must never be misreported as an observed result.

For SEO/AEO, competitive readiness normally requires inspecting live search/AI-answer surfaces, comparing multiple leaders, understanding common expectations and meaningful leader differences, and producing work that is intentionally more useful/appropriate while acknowledging authority and external constraints. For advertising/marketing, it normally requires sampling relevant competitors and current ad-transparency/creative surfaces, analyzing recurring messages/offers/creative families and landing paths, and treating longevity/engagement as proxies rather than proof of profitability. For organic content, visible views/shares/comments/velocity should be normalized to account baseline, format, age, distribution, and audience where possible. For visual/content artifacts, “better” means better fit for the intended audience/task—not simply more detail.

## What gets tested

- **Contract acceptance:** one generated event for every installed contract. Contract metadata/body are the specification source; no second manual contract list is maintained.
- **Capability coverage:** every declared AURA capability is mapped to contract tests that require or optionally use it; unreferenced declarations are surfaced.
- **Domain missions:** full Core, Customer Intelligence, Competitor Intelligence, Industry Intelligence, SEO/AEO, Content Synthesis, Marketing Synthesis, and Customer Optimization missions.
- **Cross-domain missions:** business problems where AURA must choose and compose domains rather than being told which contract to run.
- **Marathon missions:** continuous accumulated operation where later evidence, outcomes, contradictions, and changes must alter future work without resetting the workspace.
- **Concurrency missions:** two independent operators/harnesses work the same business and shared workspace simultaneously to test deduplication, semantic ownership, operator provenance, collisions, and shared-state integrity.

The suite is deliberately capable of hours-long execution. Candidate instructions tell the agent to continue through the queue without pausing for permission between events.

## Controlled benchmark businesses

The suite currently uses three synthetic business worlds:

- **AtlasOps** — B2B field-service workforce software.
- **Harbor HVAC** — local residential HVAC service business.
- **Northline Coffee** — DTC specialty-coffee ecommerce.

Synthetic does not mean the candidate is allowed to invent whatever it wants. The benchmark supplies controlled first-party facts/evidence so the evaluator can know what information was available. Where the task is inherently competitive/current, the candidate still uses legitimate live evidence: current search/AI-answer surfaces, competitor sites, ad transparency/creative centers, public content performance, reviews, current industry evidence, and similar surfaces.

`prepare_run.py` initializes each benchmark and uses AURA's canonical explicit-context bootstrap to ground its starting Business/Market/Objective/Brand/etc. state. The candidate therefore starts at **Level 2+** rather than spending the gauntlet re-proving onboarding.

The richer first-party benchmark evidence is placed under:

`attachments/qualification-inputs/<fixture>.json`

### No future-information leakage

Later-period benchmark evidence is deliberately withheld from initial candidate inputs. The raw authored benchmark files are not copied into the staged candidate product. Hidden timeline releases live outside the workspace under the evaluator area until a designated event begins.

For an event with `release_fixture`, the candidate must first take the `before` checkpoint and then run:

```bash
python3 qualification/release_fixture.py <EVENT_ID>
```

The helper refuses release unless the current before-checkpoint exists and all prior queue events have their after-checkpoints. This makes “new evidence arrives now” deterministic rather than merely advisory.

## Missing benchmark inputs are not AURA failures

The candidate may **not** create a convenient synthetic business condition merely to make a contract easy to pass.

If a contract needs controlled input that is not present and cannot legitimately be obtained from current research or accumulated AURA state, the candidate records:

`qualification_fixture`

The evaluator reports this as:

`BLOCKED-QUALIFICATION-FIXTURE`

That means the qualification benchmark needs enrichment and the event must be rerun. It is neither an AURA pass nor an AURA failure.

## Files

- `build_suite.py` — discovers every `contracts/**/CONTEXT.md`, extracts declared behavior, generates acceptance tests, and maps declared capabilities.
- `prepare_run.py` — creates a **fresh staged AURA product copy**, an external qualification workspace, grounded benchmark context, sanitized initial evidence, hidden future releases, and the uninterrupted candidate queue plus evaluator specification.
- `release_fixture.py` — releases intentionally withheld later-period evidence at the correct event boundary.
- `checkpoint.py` — deterministic before/after workspace snapshots and `--require-context` validation for every event.
- `launch.py` — optional generic shell-command adapter for launching a harness once against the uninterrupted queue while capturing stdout/stderr.
- `evaluate_run.py` — verifies Runs, root evidence, required-subcontract evidence, validation, artifact existence, state changes, competitive-field evidence, timed releases, blockers, and merges professional-quality judgments.
- `build_judge_prompt.py` — creates an independent review instruction file after hard-gate evaluation.
- `compare_runs.py` — compares two independently evaluated gauntlets and surfaces repeated failures as likely AURA hotspots while separating external/fixture/review gaps.
- `prepare_concurrency.py` / `launch_concurrent.py` — stage and launch two independent candidates simultaneously against one shared AURA workspace.
- `rubrics/rubrics.json` — common, domain-specific, cross-domain, marathon, and concurrency professional/competitive quality standards.
- `missions/missions.json` — domain, cross-domain, marathon, concurrency, and timed-release missions.
- `fixtures/*.json` — authored controlled benchmark worlds. These are qualification-authoring inputs and are deliberately excluded from staged candidate product copies.

## Preflight validation

Before spending hours on an AI gauntlet, run the normal release gate:

```bash
python3 tests/run_all.py
```

`tests/run_qualification_framework.py` is included in that gate. It checks the contract/capability mapping and **actually prepares a disposable smoke qualification run**. The smoke run verifies that:

- all benchmark bootstrap facts can be persisted through AURA's canonical helper;
- `validate_business.py --require-context` passes;
- candidate fixtures contain current evidence but no future timeline;
- future releases are staged separately;
- raw authored fixtures are not copied into the candidate product;
- bootstrap audits exist for all benchmark businesses.

The hours-long AI gauntlet itself is intentionally not a release-unit test.

## Prepare the full gauntlet

From the AURA product root:

```bash
python3 qualification/build_suite.py
python3 qualification/prepare_run.py --profile full
```

`prepare_run.py` prints a run directory, clean staged product copy, external workspace, queue, and `RUN-INSTRUCTIONS.md`.

Point the candidate AI/harness at the printed staged **product root** and give it the printed **RUN-INSTRUCTIONS.md**. Do not point the candidate at the authored `qualification/fixtures/` source directory.

The candidate should run the entire queue continuously.

The candidate must retain:

```bash
export BUSINESSOS_WORKSPACE=/path/printed/by/prepare_run
export AURA_QUALIFICATION_RUN=/path/to/qualification/run
```

If the harness exposes a CLI that can accept the instruction file, use the portable launcher:

```bash
python3 qualification/launch.py /path/to/run \
  --label candidate-a \
  --command 'YOUR_HARNESS_COMMAND {instructions}'
```

Available command-template placeholders are `{instructions}`, `{workspace}`, `{run_dir}`, and `{product_root}`. The harness command is deliberately not hard-coded into AURA.

## Profiles

```bash
# Every individual contract in one domain
python3 qualification/prepare_run.py --profile atomic --domain seo-aeo

# Full domain missions only
python3 qualification/prepare_run.py --profile domains

# Cross-domain missions only
python3 qualification/prepare_run.py --profile cross-domain

# Accumulated-state endurance missions only
python3 qualification/prepare_run.py --profile marathon

# Entire sequential gauntlet
python3 qualification/prepare_run.py --profile full
```

`full` is the main “freak athlete” test: individual contract acceptance, full-domain missions, cross-domain missions, then marathon behavior in one persistent run.

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

The hard evaluator checks checkpoint/receipt existence, real AURA Runs, root-contract match, root completion evidence, required subcontract evidence, workspace/business context validation, truthful completion, actual artifact creation when promised, declared state writes, customer-facing completion governance, reconstructable competitive-field evidence, and timed-release evidence when applicable.

A human or independent judge then reviews the **actual business output**, evidence, state diff, and competitive field. Build ready-to-use judge instructions with:

```bash
python3 qualification/build_judge_prompt.py /path/to/run
```

The judge writes every required 0–5 rubric score to `evaluator/judgments.json`. Then rerun:

```bash
python3 qualification/evaluate_run.py /path/to/run
```

Final classifications include:

- `FAIL`
- `BLOCKED-EXTERNAL`
- `BLOCKED-QUALIFICATION-FIXTURE`
- `FUNCTIONAL-NOT-ACCEPTABLE`
- `ACCEPTABLE`
- `COMPETITIVE`
- `EXCEPTIONAL`

A mechanically valid but shallow output cannot qualify as competitive merely because files and schemas are correct.

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

The comparison separates:

- robust passes;
- candidate-sensitive outcomes;
- external/environment-sensitive outcomes;
- qualification-fixture gaps;
- incomplete reviews;
- repeated failures / likely AURA hotspots.

Repeated failures across competent independent candidates are especially important evidence that the AURA contract/process itself needs improvement.

## Shared-workspace concurrency

After the independent sequential runs are understood, prepare one shared workspace with two operator lanes:

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
- timed released-evidence references when applicable;
- workspace/business context validation;
- deterministic gate failures;
- independent quality scores and notes.

This makes it possible to inspect both **what the business received** and **what AURA became internally** after each event.

## Blockers

Candidate blockers are classified as:

- `external_capability`
- `authorization`
- `missing_required_data`
- `external_service`
- `qualification_fixture`
- `aura_process`

Genuine external blockers are `BLOCKED-EXTERNAL`. A missing controlled benchmark condition is `BLOCKED-QUALIFICATION-FIXTURE`. An `aura_process` inability remains an AURA failure.

## Recommended operational sequence

Do not make the first use of a brand-new qualification framework a many-hour full run.

1. Run `python3 tests/run_all.py`.
2. Prepare one substantial domain calibration run (SEO/AEO or Content is a good choice).
3. Verify that checkpoints, receipts, artifact capture, evaluator gates, and judge packets behave as intended.
4. Run **Full Candidate A** continuously.
5. Run **Full Candidate B** from a fresh copy.
6. Judge both and run `compare_runs.py`.
7. Enrich any qualification-fixture gaps and rerun them.
8. Fix AURA hotspots and rerun failed/marginal events.
9. Run the shared-workspace concurrency gauntlet.
10. After AURA is outcome-ready in controlled qualification, add real-world pilots to measure actual ranking, AI citation, conversion, revenue, retention, and other observed business outcomes.

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

`tests/run_qualification_framework.py` verifies that the qualification generator maps the current manifest contract count and capability count, all required subcontracts resolve, every contract has gates/rubrics/tasks, every domain has a full mission, the cross-domain/marathon/concurrency layers remain present, benchmark context is grounded, later evidence is withheld, and a disposable preparation smoke run succeeds. It is included in `tests/run_all.py`.

## Non-goals

This qualification framework is not a mandatory AURA runtime, server, database, scheduler, UI, or model adapter. It uses AURA's existing local-first workspace architecture and can be driven by any harness capable of working from the filesystem. Harness-specific automation may be added as optional adapters without changing qualification semantics.
