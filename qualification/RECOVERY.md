# Qualification interruption recovery

Long AURA qualification runs are expected to survive model/provider outages, terminal closures, host restarts, and agent-session replacement without restarting completed work.

The durable unit is the **qualification run directory and its AURA workspace**, not one chat/session/model connection.

## Inspect an interrupted run

From a source checkout containing the qualification tools:

```bash
python3 qualification/resume_status.py /path/to/qualification/run --write-instructions
```

This inspects the queue, event receipts, before/after checkpoints, and candidate AURA Runs. It reports:

- terminal events: receipt is `completed` or `blocked` and the required after-checkpoint exists;
- in-progress event: some event evidence exists but the terminal receipt/after boundary is incomplete;
- pending events: not yet started;
- the first unfinished event;
- compatible candidate Runs created since that event's before-checkpoint.

It also writes:

`candidate/RESUME-INSTRUCTIONS.md`

## Recovery rules

1. **Never restart the whole qualification merely because the AI/provider/session stopped.**
2. Terminal events are immutable qualification history for that run. Do not redo them unless a reviewer explicitly invalidates and resets the event.
3. If the first unfinished event has no before-checkpoint, start it normally.
4. If its before-checkpoint already exists, preserve that checkpoint as the event baseline. Do not overwrite it because a new agent session started.
5. Inspect compatible active/incomplete AURA Runs created after the event baseline and resume from the smallest incomplete point under AURA's normal local-state-and-recovery policy. Do not create a duplicate root Run merely because the model/harness changed.
6. If a terminal receipt exists but the after-checkpoint is missing, verify the receipt and underlying AURA work are truthful and complete, then take the after-checkpoint. If the work is not complete, repair/resume it first.
7. A provider outage, rate limit, model retirement, lost network connection, or terminal closure is an **execution-environment interruption**, not by itself an AURA pass or failure.
8. A replacement model/harness may continue the same qualification run when necessary. Record the environment change in the run's external log/notes so later evaluation can distinguish AURA behavior from execution-environment sensitivity.
9. Continue sequentially from the first unfinished event until the queue is exhausted.

## Resume with a replacement candidate

Point the replacement candidate at the same staged `product/` directory and the same external workspace. Give it both:

- `candidate/RUN-INSTRUCTIONS.md`
- `candidate/RESUME-INSTRUCTIONS.md`

The replacement candidate must preserve all existing business state, evidence, Runs, receipts, and checkpoints.

## Why this matters

A full qualification may run for many hours and hundreds of events. Restarting from zero after an infrastructure interruption would waste work, contaminate repeated-test interpretation, and make long-horizon qualification impractical. Recovery is therefore part of the qualification infrastructure rather than a manual exception.
