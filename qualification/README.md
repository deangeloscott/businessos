# AURA Business Capability Qualification

Qualification exists for one reason:

> **Prove that a normal user can give AURA real business work and receive a real, truthful, professionally useful result.**

Qualification is maintainer tooling. It is not part of the packaged product and must never become an execution architecture that AURA has to satisfy.

Before changing qualification—or changing AURA because of a qualification result—read [`PRINCIPLES.md`](PRINCIPLES.md).

## Keep three things separate

### 1. AURA product integrity

```bash
python3 tests/run_all.py
```

This checks things AURA itself owns: schemas, references, business isolation, retrieval/state semantics, truth boundaries, packaging, continuity behavior, and other architectural invariants.

It does **not** test the model/harness's generic ability to open files, decode images, parse PDFs, browse, call APIs, render media, schedule work, run code, use subagents, or choose tools.

### 2. Qualification-harness integrity

```bash
python3 qualification/self_test.py
```

This checks the maintainer-only evaluator: blind candidate isolation, recovery, benchmark integrity, and staged-product observation. These checks make the evaluator trustworthy enough to use; they are **not AURA product tests** and do not prove AURA produces good work.

### 3. Real-work qualification

Give a capable model/harness the normal AURA product, organization workspace, ordinary business materials, and an ordinary-language business request. Judge the actual business result.

This is the evidence that matters most.

## Preferred pre-user qualification: blind real-world use cases

The simplest useful pre-user proof is the maintainer-only library under [`use-cases/`](use-cases/README.md).

Each use case pairs:

- an ordinary business request;
- ordinary organization context/fixtures;
- separate hidden expected-outcome guidance for an independent judge;
- small evaluator-only coverage metadata.

The candidate never receives the use-case folder, case ID, coverage metadata, judge file, rubric, or evaluator state. `prepare_run.py --case <id>` copies a neutral AURA product and organization workspace outside the source checkout, gives the candidate only the plain request text, and stages the matching judge guidance only in the physically separate evaluator tree.

The library should stay compact and realistic. One strong case may naturally exercise several Workflows or operating areas. We care about whether AURA helps solve the real business job, not about manufacturing one synthetic prompt for every implementation detail.

A longitudinal case is simply several ordinary requests against the same organization workspace, with fresh model context where useful and later evidence released naturally. This tests whether useful work actually compounds and whether organizational understanding evolves when evidence changes.

Example preparation:

```bash
python3 qualification/prepare_run.py \
  --case saas-positioning-page
```

Then use the same blind controller/evaluator flow described below.

## What qualification protects

A strong qualification run asks whether the candidate:

- understood the ordinary business request;
- used real/current evidence when the job required it;
- performed the material business method instead of skipping essential work;
- created the actual useful result or a truthful fallback when the final medium genuinely could not be produced;
- preserved facts, evidence, results, decisions, unresolved work, and other organizational meaning truthfully when persistence was useful;
- produced work a competent customer could actually use;
- held up against strong current alternatives when competitive comparison was relevant.

It does **not** require the candidate to manufacture a particular Run, method trace, checkpoint, evaluator observation, or benchmark-shaped artifact.

It also does **not** test generic model/harness competence as though it belonged to AURA. Files, browsers, APIs, renderers, code execution, schedulers, subagents, and other host capabilities are environmental inputs. When available, the candidate may use them normally. When a genuinely required capability is unavailable, the evaluator should record that external limitation instead of adding product machinery or inventing an AURA failure.

An AURA Workflow may be the hidden job under test. Its essential business method and quality invariants matter. Incidental implementation details do not: a capable model/harness may use a better tool, delegation pattern, execution order, or equivalent method when the result remains rigorous and truthful.

## Blind candidate rule

The candidate sees only:

1. a normal staged AURA product;
2. the organization workspace;
3. available model/harness capabilities;
4. an ordinary-language business request.

The candidate must not receive the source checkout, qualification directory, use-case library, case ID, target Workflow/mission ID, judge criteria, rubric, checkpoints, evaluator observations, scoring rules, or benchmark metadata.

The candidate runtime should be scoped to the neutral staged product/workspace tree, not the maintainer repository. File/folder names and supplied business material should look like ordinary organizational work, not benchmark fixtures.

Checkpoints, timed fixture release, evaluation mapping, and controller observations are evaluator bookkeeping. They exist to observe the test—not to tell AURA how to work.

## Representative real-work Workflow

The older atomic Workflow path remains useful when diagnosing one specific body of operating knowledge:

```bash
python3 qualification/prepare_run.py \
  --profile atomic \
  --workflow <workflow-id>
```

For pre-user product proof, prefer the realistic use-case library unless an isolated Workflow question actually needs answering.

Start a prepared event:

```bash
python3 qualification/task_controller.py start /path/to/run
```

Give the candidate only the printed product path, workspace path, and `candidate_message`.

When the candidate finishes:

```bash
python3 qualification/task_controller.py finish /path/to/run
python3 qualification/evaluate_run.py /path/to/run
python3 qualification/build_judge_prompt.py /path/to/run
```

Have an independent capable reviewer create `evaluator/judgments.json`, rerun `evaluate_run.py`, and inspect the actual evidence/artifact yourself when the decision matters.

The controller derives its evaluator-side observation from **observed material business changes and deliverables**. AURA Runs, when present, are optional method/continuity provenance rather than universal proof that work occurred.

## Genuine external blockers

A truthful external limitation is better than fabricated completion. Maintainer-side blocker classes include:

- `external_capability`
- `external_authority`
- `missing_required_data`
- `external_service`
- `qualification_fixture`
- `no_material_result`

`external_capability` means the active model/harness genuinely lacks something needed for the requested external result. That is an environment limitation, not evidence that AURA should acquire or own the capability.

`external_authority` means a real permission/scope boundary outside AURA—for example the user, account, platform, law, or organization has not permitted an external act. It is **not** an AURA Approval object or generic AURA authority system.

Example:

```bash
python3 qualification/task_controller.py finish /path/to/run \
  --blocker-classification external_capability \
  --blocker-detail "Live browser access was unavailable in this harness."
```

## Evaluation model

Deterministic gates are deliberately small and universal. They protect things such as:

- evaluator/checkpoint integrity;
- valid AURA/workspace state;
- whether a material result was actually observed;
- truthful completion claims;
- staged-product integrity;
- hidden evaluator isolation;
- exact duplicate artifact reuse when it could masquerade as distinct completed work.

They do **not** infer from a Workflow ID that a particular artifact, source count, research shape, medium, QA record, or field snapshot must exist.

Professional review decides whether the work is actually complete and good. For real-world use cases, the reviewer also receives the separate evaluator-only expected-outcome guidance paired with the request. That guidance describes what excellent business work should accomplish; it is not an execution checklist.

High similarity, automation, unusual execution structure, or absence of an AURA Run may be useful review signals, but they are not automatic failures by themselves.

The reviewer scores the real artifact/evidence for accuracy, evidence quality, method rigor, completeness, professional quality, business alignment, outcome readiness, state integrity, and relevant mission/domain dimensions.

Possible verdicts include:

- `EVALUATOR-ERROR`
- `FAIL`
- `BLOCKED-EXTERNAL`
- `BLOCKED-QUALIFICATION-FIXTURE`
- `FUNCTIONAL-NOT-ACCEPTABLE`
- `ACCEPTABLE`
- `COMPETITIVE`
- `EXCEPTIONAL`

A deterministic hard-pass is only an integrity floor. It cannot turn mediocre work into `ACCEPTABLE`.

## Benchmark businesses

Controlled benchmark organizations provide grounded first-party context while keeping tests repeatable. Synthetic business context never authorizes synthetic external evidence: when a task requires current public research, the candidate must use legitimate sources/capabilities available in the environment.

Ordinary supplied files may be part of a benchmark scenario because real users also provide files. The evaluator should not test whether the host can generically decode or open those file types. If the chosen environment cannot use a genuinely necessary input, classify the limitation rather than teaching AURA to own file transport or parsing.

## Repetition and diagnosis

Models are probabilistic. Repeat important cases enough to distinguish systematic AURA weaknesses from model variance or one-off execution mistakes.

When output is weak, diagnose before changing AURA. Possible causes include:

- AURA Workflow/operating-knowledge weakness;
- model capability;
- harness/tool availability;
- missing business context;
- execution mistake;
- random variance;
- fixture/evaluator problem.

Change AURA only when the failure reveals a reusable weakness that matters to ordinary users.

## Minimal longitudinal record

`qualification/ledger.jsonl` should remain small: one record for a meaningful completed qualification, not a telemetry dump. Preserve what was tested, AURA version, model/harness, important capabilities, quality/integrity verdicts, evidence location, meaningful limitations, and later field outcomes when they exist.

## Key principle

**The product is AURA. Qualification observes whether AURA helps capable intelligence do excellent real business work. AURA must never be redesigned merely to satisfy the evaluator.**
