# AURA Business Capability Qualification

> **Before modifying qualification or changing AURA because of a qualification result, read [`PRINCIPLES.md`](PRINCIPLES.md).** It is the durable qualification doctrine. The benchmark should evolve around real-world AURA quality; AURA must not be redesigned merely to make the benchmark easier to satisfy.

This directory exists for one practical reason:

> **Prove that a normal user can give ViralTrac AURA real business work and receive a real, professionally useful result.**

Qualification is maintainer tooling. It is not the product and it is excluded from normal packaged distributions.

The minimal longitudinal record is [`ledger.jsonl`](ledger.jsonl). Keep it small: one record for a meaningful completed qualification, not a telemetry dump. The current first staged campaign is [`cases/SEO-AEO-001.md`](cases/SEO-AEO-001.md).

## North-star question

For each representative workflow/playbook, ask:

> If a user gave AURA this task in ordinary language, did AURA actually do the work, use real evidence/tools where required, produce the requested result, and deliver something a competent customer would use and value?

A pass is not “the schema validated.” A pass means the business work itself was real and professionally useful.

## Golden rules

1. **Test normal use, not test-taking.** The candidate/model sees only a normal staged AURA product, the organization workspace, and the ordinary business request. It does not receive the qualification directory, target contract, rubric, checkpoints, receipts, evaluator files, event IDs, scoring rules, or hidden benchmark metadata.
2. **Keep bookkeeping outside the candidate.** Before/after checkpoints, timed evidence release, event mapping, and qualification receipts are maintainer/controller responsibilities. They must not consume candidate attention or shape the artifact.
3. **Real work beats qualification paperwork.** Research must inspect real evidence. Production must create the actual deliverable when the environment can; if final rendering/execution is genuinely unavailable, produce a truthful portable production specification rather than pretending the final medium exists. QA must inspect a real target.
4. **Use minimum-sufficient research.** Start with enough evidence to do an excellent job and expand only when more investigation could materially change the result, confidence, or competitive judgment. Do not reward exhaustive research for its own sake.
5. **Deterministic gates prove integrity, not excellence.** They may establish that evidence exists, references resolve, state is valid, the promised medium is truthful, and claimed automated work has support. They must not encode quality as arbitrary word counts, slide counts, magic phrases, or benchmark-shaped passwords.
6. **Professional review judges quality.** A human or independent model reviews the actual artifact/evidence for usefulness, accuracy, specificity, competitive readiness, and outcome readiness. Where a current competitive field matters, the evaluator independently samples enough of it to establish a credible comparison.
7. **A truthful blocker is better than fabricated completion.** If authorization, data, capability, or external access is genuinely unavailable, record the specific blocker through maintainer-side qualification state instead of manufacturing success.
8. **Diagnose before changing AURA.** A poor result may be a workflow problem, model problem, tool problem, missing-context problem, fixture problem, evaluator problem, random variance, or execution mistake. Change the product only when the failure reveals a reusable AURA weakness that matters to normal users.
9. **Do not overfit fixes to one artifact.** Improve the underlying business job; do not convert one weak result into a universal output quota.
10. **A benchmark rule belongs in AURA only when it improves ordinary customer work.** If its main value is easier scoring, keep it evaluator-side or remove it.

## Preferred representative workflow

Start with the public release gate:

```bash
python3 tests/run_all.py
```

Prepare one representative workflow:

```bash
python3 qualification/prepare_run.py \
  --profile atomic \
  --contract <contract-id>
```

The first planned SEO/AEO run uses:

```bash
python3 qualification/prepare_run.py \
  --profile atomic \
  --contract seo.intelligence.organic-competition.page-analysis
```

See `cases/SEO-AEO-001.md` for the maintainer-side intent and evaluation plan. Do not give that file to the candidate.

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

Inspect the actual artifact/evidence yourself when the decision matters. Independent judges are useful, not infallible.

## What the candidate actually sees

A prepared run intentionally has **no `candidate/` qualification directory** and the staged product has **no `qualification/` or developer `tests/` directory**.

The organization workspace uses ordinary-looking state/materials such as:

`attachments/supplied/<business-material>.json`

Benchmark fixture names, future evidence, rubrics, contract targets, controller receipts, product snapshots, checkpoints, evaluator competitive research, and the ledger remain evaluator-side.

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

## Qualification layers

The authoritative layered model is in `PRINCIPLES.md`:

0. software integrity;
1. atomic job quality;
2. competitive / field readiness;
3. composition quality;
4. capability and media execution;
5. domain and cross-domain missions;
6. reliability;
7. observed real-world outcomes.

These layers answer different questions. Do not use one giant run as a substitute for understanding them separately.

For SEO/AEO, competitive readiness may require current search/AI-answer leaders. For advertising, it may require current ad-transparency/creative/landing-path evidence. For organic content, visible views/shares/comments/velocity are proxies and should be normalized to obvious context when possible. “Better” means better for the audience, task, and intended result—not simply longer, more elaborate, or more exhaustively researched.

Observed outcomes come later from authorized real-world use. Never describe ranking readiness, conversion readiness, or competitive readiness as a business result that has already happened.

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

Repeated failures across competent candidates are stronger evidence of an AURA problem than one weak run. Candidate-sensitive outcomes should be investigated before redesigning the workflow. Sampling depth should match importance, risk, and uncertainty rather than multiplying every contract across every model by default.

## Ledger and field evidence

After a meaningful qualification is complete, append one small record to `ledger.jsonl` using the recommended fields in `PRINCIPLES.md`. The ledger should make it possible to answer:

- what was actually tested;
- on which AURA version;
- with which model/harness and important capabilities;
- whether integrity/professional/competitive readiness passed;
- where the evidence lives;
- what limitations remain;
- whether any later observed field outcome exists.

Community/customer evidence can later strengthen this record, support case studies, and inform AURA improvements. Preserve provenance and scope; one organization's result does not become universal law.

## Frozen diagnostic evidence

Once a run has been used as diagnostic/qualification evidence, do not repair its candidate artifacts or canonical state in place. Fix AURA in source, prepare a fresh run, and compare.

## Key files

- `PRINCIPLES.md` — authoritative qualification philosophy and anti-drift rules.
- `ledger.jsonl` — minimal longitudinal record of meaningful completed qualifications.
- `cases/` — small maintainer-side plans/case notes when a qualification is important enough to preserve.
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
