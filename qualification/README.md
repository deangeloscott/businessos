# AURA Business Capability Qualification

This directory exists for one practical reason:

> **Prove that a normal user can give ViralTrac AURA real business work and receive a real, professionally useful result.**

Qualification is maintainer tooling. It is not the product, it is excluded from normal packaged distributions, and AURA must never be redesigned merely to make qualification easy to satisfy.

## North-star question

For each representative workflow/playbook, ask:

> If a user gave AURA this task in ordinary language, did AURA actually do the work, use real evidence/tools where required, produce the requested result, and deliver something a competent customer would use and value?

A pass is not “the schema validated.” A pass means the business work itself was real and professionally useful.

## Golden rules

1. **Test normal use, not test-taking.** The candidate/model sees only a normal staged AURA product, the organization workspace, and the ordinary business request. It does not receive the qualification directory, target contract, rubric, checkpoints, receipts, evaluator files, event IDs, scoring rules, or hidden benchmark metadata.
2. **Keep bookkeeping outside the candidate.** Before/after checkpoints, timed evidence release, event mapping, and qualification receipts are maintainer/controller responsibilities. They must not consume candidate attention or shape the artifact.
3. **Real work beats qualification paperwork.** Research must inspect real evidence. Production must create the actual deliverable or a truthful graceful-degradation artifact when rendering/execution is genuinely unavailable. QA must inspect a real target.
4. **Deterministic gates prove integrity, not excellence.** They may establish that evidence exists, references resolve, state is valid, the promised medium is truthful, and claimed automated work has support. They must not encode quality as arbitrary word counts, slide counts, magic phrases, or benchmark-shaped passwords.
5. **Professional review judges quality.** A human or independent model reviews the actual artifact/evidence for usefulness, accuracy, specificity, competitive readiness, and outcome readiness.
6. **A truthful blocker is better than fabricated completion.** If authorization, data, capability, or external access is genuinely unavailable, record the specific blocker through maintainer-side qualification state instead of manufacturing success.
7. **Diagnose before changing AURA.** A poor result may be a workflow problem, model problem, tool problem, fixture problem, or execution mistake. Change the product only when the failure reveals a reusable AURA weakness.
8. **Do not overfit fixes to one artifact.** Improve the requirement that the actual business job be satisfied; do not convert one weak result into a universal output quota.

## Preferred representative workflow

Start with the public release gate:

```bash
python3 tests/run_all.py
```

Prepare one representative workflow:

```bash
python3 qualification/prepare_run.py \
  --profile atomic \
  --contract content.production.article
```

Preparation prints the run directory, staged product, workspace, and the next maintainer command. It does **not** create candidate-facing qualification instructions or copy qualification code into the staged product.

Start the business task externally:

```bash
python3 qualification/task_controller.py start /path/to/run
```

The controller takes the hidden `before` checkpoint, releases any scheduled business evidence, and prints a `candidate_message`.

Give the candidate/harness only:

- the printed staged **AURA product** path;
- the printed **workspace** path;
- the plain-language **candidate_message**.

Do **not** give the candidate the qualification run directory or evaluator files.

When the candidate finishes the business work:

```bash
python3 qualification/task_controller.py finish /path/to/run
```

The controller takes the hidden `after` checkpoint and derives the bookkeeping receipt from observed AURA Runs, evidence, canonical changes, and workspace changes. The candidate does not write a qualification receipt.

For a genuine external blocker, the maintainer may finish with an explicit classification:

```bash
python3 qualification/task_controller.py finish /path/to/run \
  --blocker-classification external_capability \
  --blocker-detail "Live browser access was unavailable in this harness."
```

Then evaluate:

```bash
python3 qualification/evaluate_run.py /path/to/run
python3 qualification/build_judge_prompt.py /path/to/run
```

Have an independent reviewer produce `evaluator/judgments.json`, then rerun:

```bash
python3 qualification/evaluate_run.py /path/to/run
```

Inspect the actual artifact yourself when the decision matters. Independent judges are useful, not infallible.

## What the candidate actually sees

A prepared run intentionally has **no `candidate/` qualification directory** and the staged product has **no `qualification/` or developer `tests/` directory**.

The organization workspace uses ordinary-looking state/materials such as:

`attachments/supplied/<business-material>.json`

Benchmark fixture names, future evidence, rubrics, contract targets, controller receipts, product snapshots, and checkpoints remain evaluator-side.

The benchmark business IDs themselves are ordinary organization IDs such as:

- `atlasops`
- `harbor-hvac`
- `northline-coffee`

The model should be able to behave exactly as it would for a normal business workspace.

## Timed/longitudinal evidence

Some missions include later-period first-party evidence. It remains hidden under evaluator control until the relevant work boundary.

`task_controller.py start` automatically performs the hidden before-checkpoint first and then calls the maintainer-side release logic. Candidate-visible released material appears as a normal business-supplied update under `attachments/supplied/` and contains no event ID, fixture ID, scoring metadata, or qualification instructions.

## Interruption and recovery

The durable unit is the **run directory + staged product + organization workspace**, not one model session.

Inspect status with:

```bash
python3 qualification/task_controller.py status /path/to/run
```

or:

```bash
python3 qualification/resume_status.py /path/to/run
```

Starting an already-in-progress task preserves its original before-checkpoint. A new model/harness should be pointed to the same normal product/workspace and given the same ordinary business request. Recovery instructions remain evaluator-side; never create a candidate-facing “qualification resume” prompt.

## What qualification means

Qualification has four layers:

1. **Authentic execution** — the claimed work really happened; important evidence is real/reconstructable; state/provenance is valid.
2. **Professional usefulness** — a competent practitioner/customer could use the result without rebuilding the missing core work.
3. **Competitive / outcome readiness** — where the task depends on the current field, AURA inspects relevant current alternatives/evidence and produces work deliberately suited to the intended outcome.
4. **Observed outcome** — later real-world pilots may measure rankings, citations, leads, conversion, revenue, retention, or other business results. Never confuse readiness with an outcome that has not happened.

For SEO/AEO, this may require inspecting current search/AI-answer leaders. For advertising, it may require current ad-transparency/creative/landing-path evidence. For organic content, visible views/shares/comments/velocity are proxies and should be normalized to obvious context when possible. “Better” means better for the audience, task, and intended result—not simply longer or more elaborate.

## Benchmark businesses

Controlled benchmark worlds provide known first-party context while allowing repeatability:

- **AtlasOps** — B2B field-service workforce software;
- **Harbor HVAC** — local residential HVAC service business;
- **Northline Coffee** — DTC specialty-coffee ecommerce.

Synthetic business context does **not** authorize synthetic public evidence. If a task requires current external research, the candidate must use legitimate current sources/tools available in the environment. Placeholder domains and invented public records do not count as external evidence.

## Blockers

Maintainer-side blocker classifications are:

- `external_capability`
- `authorization`
- `missing_required_data`
- `external_service`
- `qualification_fixture`
- `aura_process`

A genuine external blocker is not fabricated completion. A missing controlled fixture is a benchmark problem. An `aura_process` inability remains an AURA failure to investigate.

## Profiles

Use the smallest profile that answers the question:

```bash
# Preferred: one exact representative workflow
python3 qualification/prepare_run.py --profile atomic --contract <contract-id>

# Small domain batch when useful
python3 qualification/prepare_run.py --profile atomic --domain content-synthesis

# Domain-level orchestration missions
python3 qualification/prepare_run.py --profile domains

# Cross-domain routing/composition missions
python3 qualification/prepare_run.py --profile cross-domain

# Accumulated-state endurance only
python3 qualification/prepare_run.py --profile marathon

# Everything sequentially — optional stress/endurance, not primary quality proof
python3 qualification/prepare_run.py --profile full
```

The `full` profile is intentionally not the default proof that each workflow is excellent. Long multi-job sessions introduce model/context fatigue and are useful mainly for integration/endurance questions after atomic quality is understood.

Concurrency uses the same blind principle:

```bash
python3 qualification/prepare_concurrency.py
```

The maintainer receives separate lane requests/controller event IDs. Each model gets only the shared AURA product/workspace, its normal operator identity, and the lane’s plain business request. Controller IDs remain outside the model prompt.

## Evaluation outputs

`evaluate_run.py` creates:

- `evaluator/hard-and-merged-results.json`
- `evaluator/review-packets.json`
- `evaluator/summary.json`
- `REPORT.md`

Possible verdicts include:

- `FAIL`
- `BLOCKED-EXTERNAL`
- `BLOCKED-QUALIFICATION-FIXTURE`
- `FUNCTIONAL-NOT-ACCEPTABLE`
- `ACCEPTABLE`
- `COMPETITIVE`
- `EXCEPTIONAL`

A deterministic hard-pass is only an integrity floor. It cannot turn shallow or mediocre work into `ACCEPTABLE`.

## Repetition and comparison

Models are probabilistic. Repeat important workflows enough to distinguish one-off variance from a systematic weakness:

```bash
python3 qualification/compare_runs.py /path/to/run-a /path/to/run-b
```

Repeated failures across competent candidates are stronger evidence of an AURA problem than one weak run. Candidate-sensitive outcomes should be investigated before redesigning the workflow.

## Frozen diagnostic evidence

Once a run has been used as diagnostic/qualification evidence, do not repair its candidate artifacts or canonical state in place. Fix AURA in source, prepare a fresh run, and compare.

## Key files

- `build_suite.py` — evaluator specifications + production-like ordinary business requests.
- `prepare_run.py` — stages clean runtime product/workspace and hidden evaluator metadata.
- `task_controller.py` — external start/finish/status orchestration; candidate never runs it.
- `checkpoint.py` — maintainer-side before/after snapshots.
- `release_fixture.py` — maintainer-side timed business-evidence release.
- `resume_status.py` — evaluator-side interruption recovery.
- `evaluate_run.py` — integrity/state/hard-gate evaluation and quality-result merge.
- `build_judge_prompt.py` — independent professional-quality review instructions.
- `compare_runs.py` — repeated-run comparison.
- `integrity.py` — qualification-only integrity diagnostics.
- `fixtures/`, `missions/`, `rubrics/` — benchmark authoring/evaluation material; never ordinary runtime content.

## The standard to protect

**The product is AURA. Qualification only observes whether AURA works.**

When a rule makes AURA more likely to create real, truthful, useful business work for ordinary users, it may belong in the product. When a rule mainly makes outputs easier to score, game, or standardize for the benchmark, keep it evaluator-side—or remove it.
