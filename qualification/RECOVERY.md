# Qualification interruption recovery

AURA qualification should survive model/provider outages, terminal closures, host restarts, and agent-session replacement without restarting completed business work.

The durable unit is the **qualification run directory + staged AURA product + organization workspace**, not one chat/session/model connection.

The candidate/model must remain blind during recovery. Do not solve an infrastructure interruption by exposing qualification files, event IDs, receipts, checkpoints, target contracts, rubrics, or evaluator instructions.

## Inspect an interrupted run

From the source checkout containing maintainer qualification tools:

```bash
python3 qualification/task_controller.py status /path/to/run
```

or for more recovery detail:

```bash
python3 qualification/resume_status.py /path/to/run --write-instructions
```

`resume_status.py` writes maintainer-only guidance to:

`evaluator/RECOVERY.md`

It does not create candidate-facing recovery instructions.

## Recovery rules

1. **Never restart the whole run merely because the AI/provider/session stopped.**
2. Completed tasks are frozen qualification history. Do not redo them just to improve a score.
3. If the unfinished task already has a before-checkpoint, preserve it as the task baseline.
4. Reuse the same staged AURA product and organization workspace.
5. Inspect compatible active/incomplete AURA Runs created after the baseline and resume from the smallest incomplete point rather than creating duplicate work merely because the model changed.
6. Give the replacement candidate only the same normal product/workspace and the original ordinary business request. Do not give it the qualification run directory.
7. Do not set `AURA_QUALIFICATION_RUN` in the candidate process. `BUSINESSOS_WORKSPACE` is sufficient for normal AURA operation.
8. A provider outage, rate limit, model retirement, lost network connection, or terminal closure is an **execution-environment interruption**, not by itself an AURA pass or failure.
9. Record model/provider/harness changes in evaluator-side logs so later review can distinguish AURA behavior from environment sensitivity.
10. After the candidate finishes, let the external controller take the after-checkpoint and derive the bookkeeping receipt.

## Resume the same task

Run:

```bash
python3 qualification/task_controller.py start /path/to/run
```

For an in-progress task, the controller preserves the existing before-checkpoint and prints the ordinary `candidate_message` again.

Point the replacement model/harness at the printed staged `product_root` and `workspace`, then give it only that `candidate_message`.

When the business work is complete:

```bash
python3 qualification/task_controller.py finish /path/to/run
```

For a genuine external blocker, classify it maintainer-side with `--blocker-classification` and, when useful, `--blocker-detail`.

## Maintainer launcher

If using `qualification/launch.py`, the launcher performs the controller start/finish boundaries automatically around a successful candidate process.

Its command template may use only candidate-safe placeholders:

- `{request}`
- `{workspace}`
- `{product_root}`
- `{business_id}`

It deliberately does not support `{run_dir}` or `{instructions}` because those would reveal the qualification environment to the candidate.

## Why this matters

Recovery is valuable only if it preserves the meaning of the test. A replacement model should encounter the same kind of situation a real replacement agent would encounter: the organization's durable AURA state and the unresolved business request—not a benchmark-specific rescue prompt.
