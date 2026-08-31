# AURA Business Capability Qualification

Qualification exists for one reason:

> **Prove that a normal user can give AURA real business work and receive a real, truthful, professionally useful result.**

Qualification is maintainer tooling. It is not part of the packaged product and must never become an execution architecture that AURA has to satisfy.

Before changing qualification—or changing AURA because of a qualification result—read [`PRINCIPLES.md`](PRINCIPLES.md).

## What qualification protects

A strong qualification run asks whether the candidate:

- understood the ordinary business request;
- used real/current evidence when the job required it;
- performed the material business method instead of skipping essential work;
- created the actual useful result or a truthful fallback when the final medium genuinely could not be produced;
- preserved facts, evidence, results, decisions, unresolved work, and other organizational meaning truthfully when persistence was useful;
- produced work a competent customer could actually use;
- held up against strong current alternatives when competitive comparison was relevant.

It does **not** require the candidate to manufacture a particular Run ID, contract-execution ledger, subcontract file, checkpoint, qualification receipt, or evaluator-shaped artifact.

An AURA playbook may still be the hidden job under test. Its essential business method and quality invariants matter. Incidental implementation details do not: a capable model/harness may use a better tool, delegation pattern, execution order, or equivalent method when the result remains rigorous and truthful.

## Blind candidate rule

The candidate sees only:

1. a normal staged AURA product;
2. the organization workspace;
3. available model/harness capabilities;
4. an ordinary-language business request.

The candidate must not receive the qualification directory, target contract/mission ID, rubric, checkpoints, receipts, evaluator research, scoring rules, or benchmark metadata.

Checkpoints, timed fixture release, evaluation mapping, and controller receipts are evaluator bookkeeping. They exist to observe the test—not to tell AURA how to work.

## Representative workflow

Run the software gate first when practical:

```bash
python3 tests/run_all.py
```

Prepare one representative job:

```bash
python3 qualification/prepare_run.py \
  --profile atomic \
  --contract <contract-id>
```

Start it:

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

The controller derives its receipt from **observed material business changes and deliverables**. AURA Runs, when present, are optional method/continuity provenance rather than universal proof that work occurred.

## Genuine external blockers

A truthful external limitation is better than fabricated completion. Maintainer-side blocker classes include:

- `external_capability`
- `external_authority`
- `missing_required_data`
- `external_service`
- `qualification_fixture`
- `no_material_result`

`external_authority` means a real permission/scope boundary outside AURA—for example the user, account, platform, law, or organization has not permitted an external act. It is **not** an AURA Approval object or generic AURA authority system.

Example:

```bash
python3 qualification/task_controller.py finish /path/to/run \
  --blocker-classification external_capability \
  --blocker-detail "Live browser access was unavailable in this harness."
```

## Evaluation model

Deterministic gates are deliberately small. They protect things such as:

- evaluator/checkpoint integrity;
- valid AURA/workspace state;
- truthful completion claims;
- actual event-specific deliverables when an artifact was promised;
- reconstructable current field evidence when the job depends on current external reality;
- customer-facing claim/state integrity;
- exact duplicate reuse that proves distinct promised work was not really performed.

High similarity, automation, unusual execution structure, or absence of an AURA Run may be useful review signals, but they are not automatic failures by themselves.

Professional review decides whether the work is actually good. The reviewer scores the real artifact/evidence for accuracy, evidence quality, method rigor, completeness, professional quality, business alignment, outcome readiness, state integrity, and relevant domain-specific dimensions.

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

## Qualification layers

Use the smallest layer that answers the question:

0. software integrity;
1. atomic job quality;
2. competitive / field readiness;
3. composition quality;
4. capability and media execution;
5. domain and cross-domain missions;
6. reliability across repeated/model/harness runs where material;
7. observed real-world outcomes.

Do not use one giant run as a substitute for understanding these layers separately.

## Benchmark businesses

Controlled benchmark organizations provide grounded first-party context while keeping tests repeatable. Synthetic business context never authorizes synthetic external evidence: when a task requires current public research, the candidate must use legitimate sources/capabilities available in the environment.

## Repetition and diagnosis

Models are probabilistic. Repeat important workflows enough to distinguish systematic AURA weaknesses from model variance or one-off execution mistakes.

When output is weak, diagnose before changing AURA. Possible causes include:

- AURA method/SOP weakness;
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
