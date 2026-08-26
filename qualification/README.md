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

For SEO/AEO, competitive readiness normally requires inspecting live search/AI-answer surfaces, comparing multiple leaders, understanding common expectations and meaningful leader differences, and producing work that is intentionally more useful/appropriate while acknowledging authority and external constraints. For advertising/marketing, it normally requires sampling relevant competitors and current ad-transparency/creative surfaces, analyzing recurring messages/offers/creative families and landing paths, and treating longevity/engagement as proxies rather than proof of profitability. For organic content, visible views/shares/comments/velocity should be normalized to account baseline, format, age, distribution, and audience where possible. For visual/content artifacts, 'better' means better fit for the intended audience/task—not simply more detail.

## What gets tested

- **Contract acceptance:** one generated event for every installed contract. The contract metadata and body are the specification source; no second manual contract list is maintained.
- **Domain missions:** full Core, Customer Intelligence, Competitor Intelligence, Industry Intelligence, SEO/AEO, Content Synthesis, Marketing Synthesis, and Customer Optimization missions.
- **Cross-domain missions:** business problems where AURA must choose and compose domains rather than being told which contract to run.
- **Marathon missions:** continuous accumulated operation where later evidence, outcomes, contradictions, and changes must alter future work without resetting the workspace.

The suite is deliberately capable of hours-long execution. The candidate instructions tell the agent to continue through the queue without pausing for permission between events.

## Files

- `build_suite.py` — discovers every `contracts/**/CONTEXT.md`, extracts declared behavior, and generates acceptance tests.
- `prepare_run.py` — creates a fresh staged copy of AURA plus an external qualification workspace, initializes synthetic benchmark businesses, and builds the candidate queue plus hidden evaluator specification.
- `checkpoint.py` — deterministic before/after workspace snapshots and validation for every event.
- `launch.py` — optional generic shell-command adapter for launching a harness once against the uninterrupted queue while capturing stdout/stderr.
- `evaluate_run.py` — verifies Runs, subcontracts, validation, artifact existence, state changes, and merges optional professional-quality judgments.
- `rubrics/rubrics.json` — common and domain-specific professional/competitive quality standards.
- `missions/missions.json` — domain, cross-domain, and marathon missions.
- `fixtures/*.json` — controlled business worlds. They include first-party evidence and later-period changes; live research is still expected where the test requires the current competitive field.

## Run the full gauntlet

From the AURA product root:

```bash
python3 qualification/build_suite.py
python3 qualification/prepare_run.py --profile full
```

`prepare_run.py` prints a run directory, clean staged product copy, external workspace, queue, and `RUN-INSTRUCTIONS.md`. Give the candidate AI/harness the staged product root plus that instruction file and allow it to run continuously.

The candidate must retain:

```bash
export BUSINESSOS_WORKSPACE=/path/printed/by/prepare_run
export AURA_QUALIFICATION_RUN=/path/to/qualification/run
```

If the harness exposes a CLI that can accept the instruction file, the portable launcher can capture the whole run:

```bash
python3 qualification/launch.py /path/to/run \
  --label candidate-a \
  --command 'YOUR_HARNESS_COMMAND {instructions}'
```

Available command-template placeholders are `{instructions}`, `{workspace}`, `{run_dir}`, and `{product_root}`. The exact harness command is deliberately not hard-coded into AURA.

After the queue finishes:

```bash
python3 qualification/evaluate_run.py /path/to/qualification/run
```

This produces deterministic hard-gate results plus `evaluator/review-packets.json`. Review packets are intentionally separate from the candidate queue so the tested agent is not instructed from the evaluator's scorecard during execution.

A human or independent judge can score each packet 0–5 by every listed dimension and save an array to `evaluator/judgments.json`:

```json
[
  {
    "event_id":"CONTRACT-CONTENT-PRODUCTION-ARTICLE",
    "scores":{"accuracy":5,"evidence_quality":4,"depth_completeness":4,"professional_quality":4,"business_alignment":4,"outcome_readiness":4,"state_integrity":5,"audience_fit":4,"clarity_and_information_design":4,"appropriate_detail":4,"originality":5,"format_execution":4,"artifact_usability":4},
    "notes":"The article is production-usable and competitive with the sampled field; one evidence section could be stronger."
  }
]
```

Then rerun `evaluate_run.py`; the merged report classifies work as FAIL, FUNCTIONAL-NOT-ACCEPTABLE, ACCEPTABLE, COMPETITIVE, or EXCEPTIONAL. Incomplete judge scorecards are reported as REVIEW-INCOMPLETE rather than silently averaging a favorable subset.

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

For two independent AI/harness candidates, run `prepare_run.py` twice. Each receives a clean AURA product copy and isolated workspace. Compare the reports to find AURA capabilities that are robust across competent operators versus workflows that repeatedly fail or produce mediocre work.

## How each event is audited

The candidate must create a deterministic `before` checkpoint, execute the real work, write a receipt, and create an `after` checkpoint. The evaluator checks:

- checkpoint and receipt existence;
- a real AURA Run for the contract;
- root-contract match and completed status;
- required subcontract completion;
- workspace/business validation at the event boundary;
- truthful completion claims;
- actual artifact existence when the contract promises an artifact;
- governed customer-facing completion requirements;
- declared canonical write types changing when the contract says it writes state;
- the before/after workspace diff;
- the actual artifact/evidence package for human or independent semantic review.

The resulting run directory therefore contains both the execution logs and the evidence needed to inspect whether the AURA folder evolved as expected.

## Interpreting failures

A failed event is not automatically a model failure. Review the contract, transcript/logs, artifact, Run/contract-execution record, state diff, and rubric. A useful triage vocabulary is:

- AURA contract/process defect or ambiguity
- missing AURA capability/process
- insufficient competitive/outcome methodology
- candidate reasoning/execution failure
- harness/tool/provider failure
- unavailable external capability
- qualification fixture/evaluator defect
- acceptable probabilistic variance

If multiple competent candidates fail the same maneuver in the same way, treat that as strong evidence that AURA itself needs improvement.

## Non-goals

This qualification framework is not a mandatory AURA runtime, server, database, scheduler, UI, or model adapter. It uses AURA's existing local-first workspace architecture and can be driven by any harness capable of working from the filesystem. Harness-specific automation may be added as optional adapters without changing the qualification semantics.
