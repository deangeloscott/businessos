#!/usr/bin/env python3
"""AURA product-integrity gate.

Run every product-owned regression even when one fails so one local execution reveals
the complete failure set. Qualification-harness self-tests run separately under
`qualification/self_test.py` and are not counted as AURA product tests.
"""
from pathlib import Path
import os,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1';env['PYTHONUTF8']='1'
TESTS=[
    'tests/run_distribution.py',
    'tests/run_playbook_discovery.py',
    'tests/run_canonical_model_boundary.py',
    'tests/run_ecosystem_intelligence.py',
    'tests/run_intelligence_maturation.py',
    'tests/run_intelligence_evidence_closure.py',
    'tests/run_competitor_composition.py',
    'tests/run_monitoring_continuity.py',
    'tests/run_monitoring_pause.py',
    'tests/run_attention_platform_lifecycle.py',
    'tests/run_workflow_evolution_exchange.py',
    'tests/run_explicit_operating_knowledge.py',
    'tests/run_workspace_human_knowledge.py',
    'tests/run_component_distributions.py',
    'tests/run_workspace_migration_path_guard.py',
    'tests/run_agent_hardening.py',
    'tests/run_aura_entry.py',
    'tests/run_first_principles_interface.py',
    'tests/run_memory_interface.py',
    'tests/run_bootstrap_reference_ids.py',
    'tests/run_preferences_multioperator.py',
    'tests/run_preference_task_constraint_separation.py',
    'tests/run_onboarding_context_hardening.py',
    'tests/run_brand_onboarding.py',
    'tests/run_run_provenance.py',
    'tests/run_run_continuity_receipt.py',
    'tests/run_organizational_state_truth.py',
    'tests/run_platform_python_compat.py',
    'tests/run_platform_semantic_reverification.py',
    'tests/run_local_evidence.py',
    'tests/run_decision_grounding.py',
    'tests/run_customer_facing_draft_provenance.py',
    'tests/run_customer_facing_qa_invariant.py',
    'tests/run_claim_manifest_operational_promises.py'
]
failures=[]
for rel in TESTS:
    print(f'== {rel} ==',flush=True)
    completed=subprocess.run([sys.executable,str(ROOT/rel)],cwd=ROOT,env=env)
    if completed.returncode!=0:failures.append((rel,completed.returncode))
if failures:
    print(f'\nAURA product-integrity gate failed: {len(failures)}/{len(TESTS)} suites failed')
    for rel,code in failures:print(f'- {rel} (exit {code})')
    raise SystemExit(1)
print(f'all AURA product-integrity tests passed: {len(TESTS)} suites')
