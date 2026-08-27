# AURA Business Capability Qualification

This directory exists for one practical reason:

> **Prove that a normal user can give ViralTrac AURA real business work and receive a real, professionally useful result.**

Qualification is maintainer tooling. It is not the product, it is excluded from normal packaged distributions, and AURA must never be redesigned merely to make this machinery easy to satisfy.

## North-star question

For each representative workflow/playbook, ask:

> If a user gave AURA this task in ordinary language, did AURA actually do the work, use real evidence/tools where required, produce the requested result, and deliver something a competent customer would use and value?

A pass is not “the schema validated.” A pass means the business work itself was good.

## Golden rules

1. **Test normal use, not test-taking.** Candidate tasks are ordinary business requests. The candidate queue uses opaque task IDs and does not expose the target contract, rubric, hard gates, or evaluator metadata. The evaluator retains that information separately under `evaluator/`.
2. **Real work beats qualification paperwork.** Research must inspect real evidence. Production must create the actual deliverable or a truthful graceful-degradation artifact when rendering/execution is genuinely unavailable. QA must inspect a real target. Never reward plausible paperwork that substitutes for the job.
3. **Deterministic gates prove integrity, not excellence.** They may establish that evidence exists, references resolve, state is valid, the promised medium is truthful, and claimed automated work has support. They must not encode business quality as arbitrary word counts, slide counts, magic phrases, or other benchmark-shaped passwords.
4. **Professional review judges quality.** A human or independent model reviews the actual artifact and evidence for usefulness, accuracy, specificity, competitive readiness, and outcome readiness.
5. **A truthful blocker is better than fabricated completion.** If required authorization, data, capability, or external access is genuinely unavailable, record the specific blocker. Do not manufacture a source, metric, tool action, asset, or outcome.
6. **Diagnose before changing AURA.** A poor result may be a workflow problem, model problem, tool problem, fixture problem, or execution mistake. Change the product only when the failure reveals a reusable AURA weakness.
7. **Do not overfit fixes to one bad artifact.** If a 207-word article is bad because it is incomplete, improve the requirement that the reader task be fully satisfied; do not conclude that every valid article must exceed one universal word count. Apply the same principle to slide counts, timecodes, formatting, and other incidental shapes.

## Recommended qualification sequence

The primary quality loop is **one representative workflow in a fresh run**:

```bash
python3 tests/run_all.py
python3 qualification/prepare_run.py \
  --profile atomic \
  --contract content.production.article
```

Then point the candidate harness at the printed staged product and `candidate/RUN-INSTRUCTIONS.md`.

After the task finishes:

```bash
python3 qualification/evaluate_run.py /path/to/run
python3 qualification/build_judge_prompt.py /path/to/run
```

Have an independent reviewer produce `evaluator/judgments.json`, then rerun:

```bash
python3 qualification/evaluate_run.py /path/to/run
```

Inspect the actual artifact yourself when a decision matters. Independent judges are useful, but they are not infallible.

Once a workflow is good, repeat it with another representative task/model or a small related batch. Use broader domain/cross-domain/endurance runs only after individual work quality is understood.

## What qualification means

Qualification has four layers:

1. **Authentic execution** — the claimed work really happened; important evidence is real and reconstructable; state/provenance is valid.
2. **Professional usefulness** — a competent practitioner/customer could use the result without rebuilding the missing core work.
3. **Competitive / outcome readiness** — where the task depends on the current field, AURA inspects relevant current alternatives/evidence and produces work deliberately suited to winning the intended outcome.
4. **Observed outcome** — later real-world pilots may measure rankings, citations, leads, conversion, revenue, retention, or other business results. Never confuse readiness with an outcome that has not yet happened.

For SEO/AEO, this may require inspecting current search/AI-answer leaders. For advertising, it may require current ad-transparency/creative/landing-path evidence. For organic content, visible views/shares/comments/velocity are proxies and should be normalized to obvious context when possible. “Better” always means better for the audience, task, and intended result—not simply longer or more elaborate.

## Candidate vs. evaluator information

`prepare_run.py` creates two views:

- `candidate/queue.json` — opaque task IDs plus ordinary natural-language business requests and only the bookkeeping needed to complete the work run;
- `evaluator/queue.json` and `evaluator/suite.json` — hidden target contracts, rubric dimensions, expected writes, competitive profiles, and other evaluation metadata.

The candidate should route each request through AURA normally. It should not be told which internal contract is being certified or which predicates will be scored.

The current portable runner still asks the candidate to take before/after checkpoints and write a compact receipt. Treat those as external audit bookkeeping. They must not shape the substantive artifact. A future harness may move those mechanics fully outside the candidate without changing the quality standard.

## Benchmark businesses

Controlled benchmark worlds provide known first-party context while allowing repeatability:

- **AtlasOps** — B2B field-service workforce software;
- **Harbor HVAC** — local residential HVAC service business;
- **Northline Coffee** — DTC specialty-coffee ecommerce.

Synthetic business context does **not** authorize synthetic public evidence. If a task inherently requires current external research, the candidate must use legitimate current sources/tools available in the environment. Placeholder domains and invented public records do not count.

Initial candidate-visible material lives under:

`attachments/qualification-inputs/<fixture>.json`

Later-period benchmark evidence may be withheld under evaluator control and released at the appropriate task boundary.

## Blockers

Candidate blockers are classified as:

- `external_capability`
- `authorization`
- `missing_required_data`
- `external_service`
- `qualification_fixture`
- `aura_process`

A genuine external blocker is not fabricated completion. A missing controlled fixture is a benchmark problem. An `aura_process` inability remains an AURA failure to investigate.

## Profiles

Use the smallest profile that answers the question you are testing:

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

# Everything sequentially — optional stress/endurance run, not the primary quality test
python3 qualification/prepare_run.py --profile full
```

The `full` profile is intentionally **not** the default proof that each workflow is excellent. Long multi-job sessions introduce model/context fatigue and are useful mainly for integration/endurance questions after atomic quality has been established.

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

Models are probabilistic. Repeat important workflows enough to distinguish one-off variance from a systematic weakness. Two evaluated runs can be compared with:

```bash
python3 qualification/compare_runs.py /path/to/run-a /path/to/run-b
```

Repeated failures across competent candidates are stronger evidence of an AURA problem than one weak run. Candidate-sensitive outcomes should be investigated before redesigning the workflow.

## Frozen diagnostic evidence

Once a run has been used as diagnostic/qualification evidence, do not repair its candidate artifacts or canonical state in place. Fix AURA in source, prepare a fresh run, and compare. Mechanical normalization of evaluator-owned output may be documented when necessary, but candidate state remains frozen.

## Key files

- `build_suite.py` — builds evaluator specifications from installed contracts and turns each target into a production-like candidate request.
- `prepare_run.py` — stages a clean AURA copy/workspace, grounds benchmark context, and separates candidate vs. evaluator metadata.
- `checkpoint.py` — before/after state snapshots.
- `release_fixture.py` — controlled later-evidence release.
- `evaluate_run.py` — integrity/state/hard-gate evaluation and quality-result merge.
- `build_judge_prompt.py` — independent professional-quality review instructions.
- `compare_runs.py` — repeated-run comparison.
- `integrity.py` — qualification-only integrity diagnostics.
- `fixtures/`, `missions/`, `rubrics/` — benchmark authoring/evaluation material; not ordinary AURA runtime content.

## Preflight

Before spending model/tool cost on a representative run:

```bash
python3 tests/run_all.py
```

The public release gate includes qualification-framework regressions but does not run the long AI work itself.

## The standard to protect

The product is AURA. Qualification exists to answer whether AURA works.

When a test rule makes AURA more likely to create real, truthful, useful business work, it may belong in the product. When a rule mainly makes outputs easier to score, game, or standardize for the benchmark, keep it in evaluation—or remove it.
